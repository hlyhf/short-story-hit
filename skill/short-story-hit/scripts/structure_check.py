#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
短篇爆款结构体检脚本 v3.1（short-story-hit 配套）

v3 / v3.1 新增（在 v2 全部功能之上）:
  - 逐句信号强度评分 + ASCII 情绪曲线（▁▂▃▄▅▆█，一眼定位塌陷区）
  - 连续弱句「塌陷区」检测（≥3 句 0 信号 且 字数 ≥ max(60, 全文8%)，贴结尾标注；
    v3.1 阈值改相对值，避免把好故事的对话/情感落点段误报为塌陷）
  - 逐句改写建议（开头铺垫 / 塌陷补钩 / 结尾收束）；
    v3.1 评分≥8 的达标文本，塌陷自动降级为「○ 节奏观察」，不误伤
  - --json 输出新增 curve / suggestions / sentence_scores / collapse_runs

保留 v2:
  - 汉字字数 + 篇幅建议(800-2000)
  - 开篇前三句逐句钩子分析(冲突/悬念/反差)
  - 全篇反转信号词计数 / 高张力关系模型命中 / 钩子公式推断
  - 综合 10 分评分 + 改进建议
  - 批量检查目录(--dir)

v3.2 新增（对标拆解模式 --benchmark）:
  - 喂入任意爆文，输出「方法论骨架」：靶心情绪判定 + 钩子公式 + 关系模型 + 反转点定位
    + 结尾类型 + 与弹药库 8 篇案例的对照（命中格子 / 新格子）+ 可直接入库的拆解卡片
  - 目的：让弹药库「自我进化」——拆完即沉淀为新案例骨架 / 方法论补充

用法:
  python3 structure_check.py <故事.md/.txt> [--json]                      # 体检模式
  python3 structure_check.py --dir <文件夹> [--json]                      # 批量体检
  python3 structure_check.py <故事.md/.txt> --benchmark [--title 标题] [--json]   # 对标拆解
"""
import sys
import os
import re
import json
import argparse

HOOK_CONFLICT = ["杀", "死", "仇", "复仇", "背叛", "离婚", "逼", "威胁",
                 "倒闭", "破产", "绝症", "坠", "逃", "抓", "揭露", "真相",
                 "秘密", "隐藏", "假", "骗局", "阴谋", "下毒", "骨灰", "绑", "陷阱"]
HOOK_SUSPENSE = ["为什么", "谁", "怎么", "竟然", "竟", "原来", "没想到",
                 "背后", "到底", "究竟", "谜", "隐藏", "不过", "其实", "秘密"]
HOOK_CONTRAST_LO = ["废物", "替身", "乞丐", "佣人", "平民", "底层", "普通",
                    "无名", "入赘", "穷", "阶下囚", "仇人", "敌人", "笑话说", "洗盘子", "倒数第一"]
HOOK_CONTRAST_HI = ["继承人", "老板", "主人", "首富", "泰斗", "女主人", "皇室",
                    "黑卡", "少爷", "小姐", "豪门", "执剑人", "总裁"]

REVERSE_WORDS = ["没想到", "原来", "竟", "竟然", "其实", "真相", "揭露",
                 "发现", "可是", "但", "不过", "反转", "殊不知", "只不过", "却"]

RELATION_MODELS = {
    "替身": ["替身", "九分像", "像她", "像他", "影子", "照片里", "亡妻"],
    "复仇": ["复仇", "报仇", "仇人", "杀父", "灭门", "血仇", "纵火"],
    "错认": ["认错", "错认", "抱错", "认错了", "搞错", "认成", "顶替"],
    "阶层差": ["阶层", "门第", "云泥", "贫富", "下人", "少爷", "小姐", "豪门", "低嫁"],
    "养恩血仇": ["养育", "养恩", "灭门", "血海", "仇"],
    "契约": ["契约", "交易", "卖身", "先婚后爱", "协议", "婚约", "条款"],
}

HOOK_FORMULA_RELATION = {
    "身份逆转": ["错认", "阶层差", "契约"],
    "绝境开局": ["复仇", "养恩血仇", "契约"],
    "隐藏身份": ["替身", "复仇", "错认"],
    "倒计时": ["养恩血仇", "复仇", "契约"],
    "惊天揭露": ["错认", "替身", "复仇"],
}

# ---- 对标拆解模式（v3.2）专用常量 ----
TARGET_EMO = {
    "爽": ["复仇", "报仇", "打脸", "逆袭", "翻盘", "清算", "碾压", "揭穿", "认错",
           "跪", "自食其果", "扬眉", "扳回", "狠狠", "算账", "抵债", "哑口无言",
           "扬眉吐气", "出一口气", "狠狠打脸", "作证", "顶替", "当众"],
    "虐": ["眼泪", "泪", "心碎", "委屈", "辜负", "不值", "孤独", "疼", "离开",
           "死别", "误会", "多年", "葬", "遗", "诀别", "撑", "熬"],
    "悬": ["谜", "诡异", "阴", "鬼", "当铺", "怪谈", "到底", "悬", "惊", "恐",
           "契约", "影子", "消失", "骨灰", "录像", "监控", "档案", "替换", "偷换",
           "冒名", "假死", "失踪", "镜", "车祸", "仓库", "陌生", "线索", "骗",
           "跟踪", "调查"],
}

# 弹药库已覆盖的 8 个格子（情绪 × 关系），用于对照拆解结果
LIBRARY = [
    ("A", "爽", "错认"), ("B", "虐", "替身"), ("C", "悬", "养恩血仇"),
    ("D", "爽虐交织", "契约"), ("E", "爽", "复仇"), ("F", "虐", "阶层差"),
    ("G", "悬", "契约"), ("H", "爽虐交织", "错认"),
]

LEVELS = "▁▂▃▄▅▆█"


def count_han(text):
    return len(re.findall(r"[一-鿿]", text))


def split_sentences(text):
    parts = re.split(r"(?<=[。！？!?])", text)
    return [p.strip() for p in parts if p.strip()]


def clean_body(text):
    lines, in_code = [], False
    for ln in text.splitlines():
        if ln.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if ln.strip().startswith("#"):
            continue
        lines.append(ln)
    return "\n".join(lines)


def classify_hook(sent):
    hit = []
    if any(w in sent for w in HOOK_CONFLICT):
        hit.append("冲突")
    if any(w in sent for w in HOOK_SUSPENSE):
        hit.append("悬念")
    if any(w in sent for w in HOOK_CONTRAST_LO) or any(w in sent for w in HOOK_CONTRAST_HI):
        hit.append("反差")
    return hit


def classify_formula(text):
    """粗略推断开篇使用的钩子公式。"""
    if re.search(r"倒计时|还剩|只剩|\d+\s*小时|\d+\s*天|72|48|30\s*秒|最后", text):
        return "倒计时"
    if any(w in text for w in ["隐藏", "秘密", "通缉", "面具", "身份", "实习生", "闺蜜"]):
        return "隐藏身份"
    if any(w in text for w in ["死", "杀", "仇", "绝境", "绑", "陷阱", "处决", "坠落"]):
        return "绝境开局"
    if any(w in text for w in ["原来", "竟", "发现", "真相", "认错", "抱错", "遗嘱"]):
        return "惊天揭露"
    if any(w in text for w in HOOK_CONTRAST_LO) and any(w in text for w in HOOK_CONTRAST_HI):
        return "身份逆转"
    return ""


# ---- 对标拆解：靶心情绪 / 反转点 / 结尾类型 ----
def classify_emotion(body):
    """统计全文各情绪关键词命中数，返回 (主导情绪, 计数明细)。
    任两情绪显著（≥2）且接近（弱项≥强项40%）时判为「X+Y交织」。"""
    cnt = {k: sum(body.count(w) for w in ws) for k, ws in TARGET_EMO.items()}
    sig = {k: v for k, v in cnt.items() if v >= 2}
    if not sig:
        return "未明确", cnt
    ordered = sorted(sig, key=lambda k: -sig[k])
    hi, lo = ordered[0], (ordered[1] if len(ordered) > 1 else None)
    if lo and sig[lo] >= 0.4 * sig[hi]:
        return f"{hi}{lo}交织", cnt
    return hi, cnt


def find_reverse_points(sents):
    """定位含反转信号的句子（句序从 1 起），返回 [(序号, 前 18 字)]。"""
    return [(i, s[:18]) for i, s in enumerate(sents, 1)
            if any(w in s for w in REVERSE_WORDS)]


def classify_tail(last_sent, sents):
    """判断结尾类型：反转收束 / 余震留白 / 开放式悬念 / 金句短收 / 长尾 / 说教尾巴。"""
    if len(last_sent) > 30:
        if any(w in last_sent for w in ["明白", "懂了", "终于", "所以", "人生",
                                        "其实", "才知道", "才懂", "释然", "感悟"]):
            return "说教尾巴（⚠ 不推荐）"
        return "长尾（⚠ 建议压短）"
    if any(w in last_sent for w in REVERSE_WORDS):
        return "反转收束"
    if last_sent.endswith(("？", "?")):
        return "开放式悬念"
    if any(w in last_sent for w in ["凉", "碎", "等", "泪", "风", "灯", "夜",
                                    "空", "余", "剩", "灰", "散"]):
        return "余震留白"
    return "金句/短收"


def build_library_match(emotion, relations):
    """对照弹药库 8 篇。返回 (候选对照列表, 强命中列表, 是否全新关系轴)。
    候选 = 文中关系在库里出现过的格子；强命中 = 该格子情绪与文本显著情绪吻合。
    只有 relation 中没有任何关系出现在库里，才算「全新关系轴 / 新格子」。"""
    emo_set = set()
    if "交织" in emotion:
        emo_set.update(emotion.replace("交织", ""))
    elif emotion != "未明确":
        emo_set.add(emotion)
    candidates, strong = [], []
    for code, emo, rel in LIBRARY:
        if rel not in relations:
            continue
        lib_emos = set(emo) if "交织" not in emo else set(emo.replace("交织", ""))
        hit = bool(emo_set & lib_emos)
        rec = (code, emo, rel, hit)
        candidates.append(rec)
        if hit:
            strong.append(rec)
    return candidates, strong, (not candidates)


def sentence_score(sent):
    """逐句信号强度：冲突×2 悬念×2 反差×2 反转×2。返回 (总分, 详情)。"""
    c = sum(sent.count(w) for w in HOOK_CONFLICT)
    su = sum(sent.count(w) for w in HOOK_SUSPENSE)
    co = 1 if (any(w in sent for w in HOOK_CONTRAST_LO)
               or any(w in sent for w in HOOK_CONTRAST_HI)) else 0
    r = sum(sent.count(w) for w in REVERSE_WORDS)
    return c * 2 + su * 2 + co * 2 + r * 2, {"冲突": c, "悬念": su, "反差": co, "反转": r}


def build_curve(scores):
    """把逐句分数映射为 8 级 ASCII 曲线。"""
    if not scores:
        return ""
    mx = max(scores)
    if mx <= 0:
        return LEVELS[0] * len(scores)
    return "".join(LEVELS[min(s * 6 // mx, 6)] for s in scores)


def find_collapse_runs(sents, scores, min_len=3, total_han=0):
    """连续 0 信号句段。字数阈值取 max(60, 全文8%)，短文本也能抓到真塌陷、
    长文本的对话/情感呼吸段不误报。返回 [(起,止,字数,是否含结尾句)]，最多2个。"""
    min_chars = max(60, int(total_han * 0.08))
    runs = []
    n = len(scores)
    i = 0
    while i < n:
        if scores[i] == 0:
            j = i
            while j < n and scores[j] == 0:
                j += 1
            chars = sum(count_han(s) for s in sents[i:j])
            if (j - i) >= min_len and chars >= min_chars:
                runs.append((i, j - 1, chars, (j - 1) == n - 1))
            i = j
        else:
            i += 1
    return sorted(runs, key=lambda x: -x[2])[:2]


def build_suggestions(sents, scores, collapse_runs, tail_short, score=0):
    """逐句改写建议：开头铺垫 / 塌陷补钩 / 结尾收束。score>=8 时塌陷降级为节奏观察。"""
    sug = []
    polished = score >= 8
    # 1) 开头三句铺垫
    weak_open = [i for i in range(min(3, len(scores))) if scores[i] == 0]
    if weak_open:
        quoted = " / ".join(sents[i][:16] for i in weak_open)
        sug.append(
            f"✎ 开头弱（第{[i + 1 for i in weak_open]}句 0 信号）：「{quoted}」属背景铺垫。"
            f"铁律：前三句必出冲突/悬念/反差。套公式「[反常动作]+[身份或处境反差]+[未解悬念]」重写"
            f"（见 references/hook-design.md 第三节）")
    # 2) 塌陷区 / 节奏观察
    for (a, b, chars, touch_end) in collapse_runs:
        if polished:
            head = f"○ 节奏观察 第{a + 1}–{b + 1}句"
            if touch_end:
                tip = "贴结尾：多为爆点后骤停/情感落点，留白正常；确认不是说教尾巴即可。"
            else:
                tip = "本篇整体达标，此处属叙事呼吸段。想更抓人可塞一个反常细节或半句扎心对话（可选优化）。"
        else:
            head = f"✎ 塌陷区 第{a + 1}–{b + 1}句"
            if touch_end:
                tip = ("贴结尾：若这是爆点后的骤停余震可保留；"
                       "但确认不是「从此幸福/她明白了道理」式说教尾巴——余震要留白，不要解释。")
            else:
                tip = ("中段塌陷 = 完读率断崖。立刻补钩，四选一："
                       "①新线索（一个反常细节）②扎心对话（一句让人心里一紧的话）"
                       "③小反转（认知翻转一次）④关系递进（再揭一层身份/真相）")
        sug.append(f"{head}：连续 {b - a + 1} 句 0 信号（约 {chars} 字）。{tip}")
    # 3) 结尾句偏长
    if sents and not tail_short:
        sug.append(
            f"✎ 结尾句偏长（{len(sents[-1])} 字 > 30）：收束为 ≤30 字短句。"
            f"要么爆点骤停，要么金句留白引续集（见 references/hook-arsenal.md 第三节金句库）")
    return sug


def analyze(path):
    with open(path, encoding="utf-8") as f:
        text = f.read()
    body = clean_body(text)
    han = count_han(body)
    sents = split_sentences(body)
    first3 = sents[:3]

    # 逐句评分 + 曲线 + 塌陷区（v3.1 相对阈值）
    scored = [sentence_score(s) for s in sents]
    scores = [sc for sc, _ in scored]
    curve = build_curve(scores)
    collapse_runs = find_collapse_runs(sents, scores, min_len=3, total_han=han)

    per_sentence = [{"sent": s, "hit": classify_hook(s)} for s in first3]
    open_hook = any(c["hit"] for c in per_sentence)
    formula = classify_formula("".join(first3))
    recommended = HOOK_FORMULA_RELATION.get(formula, [])

    reverse_cnt = sum(body.count(w) for w in REVERSE_WORDS)
    rel_hits = {m: [w for w in kws if w in body] for m, kws in RELATION_MODELS.items()}
    rel_hit = {m: v for m, v in rel_hits.items() if v}

    last = sents[-1] if sents else ""
    tail_short = len(last) <= 30

    # 评分（与 v2 一致）
    score = 0
    notes = []
    if open_hook:
        score += 2
    else:
        notes.append("开篇前三句未命中钩子关键词，建议强化冲突/悬念/反差(见 references/hook-design.md)")
    if reverse_cnt >= 2:
        score += 2
    elif reverse_cnt == 1:
        score += 1
        notes.append("反转信号词偏少(1个)，建议增加认知/身份反转")
    else:
        notes.append("反转信号词过少(0个)，中后段建议安排 >=1 次反转")
    if rel_hit:
        score += 2
    else:
        notes.append("未命高张力关系模型关键词，建议明确替身/复仇/错认等关系(见 references/relationship-design.md)")
    if tail_short:
        score += 2
    else:
        score += 1
        notes.append("结尾句偏长，建议收束为短句余震/悬念(见 Phase 5)")
    if not (800 <= han <= 2000):
        notes.append(f"汉字数 {han}，建议 800-2000 字(当前{'偏少' if han < 800 else '偏多'})")

    # 逐句建议（依赖 score 分档：达标文本塌陷降级为节奏观察）
    suggestions = build_suggestions(sents, scores, collapse_runs, tail_short, score)

    return {
        "file": path,
        "han_chars": han,
        "length_ok": 800 <= han <= 2000,
        "open_hook": open_hook,
        "open_per_sentence": per_sentence,
        "hook_formula": formula or "未明确",
        "recommended_relation": recommended,
        "reverse_signals": reverse_cnt,
        "relation_models": list(rel_hit.keys()),
        "tail_short": tail_short,
        "curve": curve,
        "sentence_scores": scores,
        "collapse_runs": [
            {"from": a + 1, "to": b + 1, "chars": ch, "touch_tail": te}
            for (a, b, ch, te) in collapse_runs
        ],
        "suggestions": suggestions,
        "score_10": score,
        "notes": notes,
    }


def print_report(r):
    print(f"文件: {r['file']}")
    print(f"汉字数: {r['han_chars']}  ({'篇幅适中' if r['length_ok'] else '建议800-2000字'})")
    print(f"开篇钩子: {'命中' if r['open_hook'] else '未命中'}  公式推断: {r['hook_formula']}")
    for i, c in enumerate(r["open_per_sentence"]):
        tag = "/".join(c["hit"]) if c["hit"] else "无信号"
        print(f"  第{i + 1}句 [{tag}]: {c['sent'][:40]}")
    if r["recommended_relation"]:
        print(f"  推荐关系模型: {', '.join(r['recommended_relation'])}")
    print(f"反转信号词: {r['reverse_signals']}")
    print(f"关系模型命中: {', '.join(r['relation_models']) or '无'}")
    print(f"结尾短句余震: {'是' if r['tail_short'] else '偏长'}")
    print(f"结构评分: {r['score_10']}/10")

    # 情绪曲线
    print()
    print("【情绪曲线】逐句信号强度(█=峰值 ▁=谷底；▁ 也可能是叙事呼吸段，须结合评分判断)")
    print("   " + (r["curve"] or "(无)"))
    for run in r["collapse_runs"]:
        tag = "结尾余震?" if run["touch_tail"] else "塌陷区"
        caret = " " * (run["from"] - 1) + "^" * (run["to"] - run["from"] + 1)
        print(f"   {caret}  第{run['from']}–{run['to']}句 [{tag}] {run['chars']}字")

    # 逐句诊断
    if r["suggestions"]:
        print()
        print("【逐句诊断与改写建议】")
        for s in r["suggestions"]:
            print("  " + s)

    print("-" * 36)
    if r["notes"]:
        print("评分说明:")
        for n in r["notes"]:
            print(f"  - {n}")
    else:
        print("结构信号良好，对照 references/hit-checklist.md 做人工终检。")


def extract_title(text, fallback="未命名"):
    for ln in text.splitlines():
        s = ln.strip()
        if s.startswith("#"):
            return s.lstrip("#").strip() or fallback
    return fallback


def _all_sents(path):
    return split_sentences(clean_body(open(path, encoding="utf-8").read()))


def analyze_benchmark(path, title=None):
    """对标拆解：在体检结果上补充情绪 / 反转点 / 结尾 / 库对照 / 骨架卡片。"""
    base = analyze(path)
    sents = _all_sents(path)
    body = clean_body(open(path, encoding="utf-8").read())
    emotion, emo_cnt = classify_emotion(body)
    reverse_pts = find_reverse_points(sents)
    tail_type = classify_tail(sents[-1] if sents else "", sents)
    candidates, strong, is_new = build_library_match(emotion, base["relation_models"])

    if base["score_10"] >= 8:
        learn = "结构达标，可直接作为该格子的示范或提炼其独特钩子写法入库。"
    elif not base["open_hook"]:
        learn = "开篇钩子弱——借鉴其被验证的关系/情绪设计，但重写开头三句抓人。"
    elif not base["relation_models"]:
        learn = "关系模型模糊——保留其情绪节奏，补强明确的人物关系张力。"
    else:
        learn = "中段或结尾有塌陷——取其靶心情绪与钩子公式，补强塌陷段后入库。"

    base.update({
        "mode": "benchmark",
        "title": title or extract_title(open(path, encoding="utf-8").read()),
        "target_emotion": emotion,
        "emotion_counts": emo_cnt,
        "reverse_points": reverse_pts,
        "tail_type": tail_type,
        "library_candidates": candidates,
        "library_strong": strong,
        "is_new_grid": is_new,
        "learn": learn,
    })
    return base


def print_benchmark(r):
    emo = r["target_emotion"]
    print(f"对标拆解 · 《{r['title']}》")
    print(f"汉字数: {r['han_chars']}  机检评分: {r['score_10']}/10  ({'达标' if r['score_10'] >= 8 else '待优化'})")
    print(f"靶心情绪: {emo}  (命中统计 爽:{r['emotion_counts'].get('爽', 0)} "
          f"虐:{r['emotion_counts'].get('虐', 0)} 悬:{r['emotion_counts'].get('悬', 0)})")
    print(f"钩子公式: {r['hook_formula']}   关系模型: {', '.join(r['relation_models']) or '无'}")
    print(f"结尾类型: {r['tail_type']}")
    print()
    print("【情绪曲线】" + (r["curve"] or "(无)"))
    rp = r["reverse_points"]
    print(f"【反转点】共 {len(rp)} 处: " + ("；".join(f"第{a}句「{b}…」" for a, b in rp[:8]) or "无"))
    print()
    cands, strong, is_new = r["library_candidates"], r["library_strong"], r["is_new_grid"]
    if is_new:
        print("【弹药库对照】★ 全新关系轴（库中从未出现，强烈建议入库为新案例）")
    else:
        if strong:
            print("【弹药库对照】命中已覆盖格子: " +
                  ", ".join(f"{c[0]}({c[1]}+{c[2]})" for c in strong))
        weak = [c for c in cands if not c[3]]
        if weak:
            tag = "★ 情绪×关系新组合" if not strong else "情绪变体对照(关系已有·情绪方向不同)"
            print(f"  {tag}: " + ", ".join(f"{c[0]}({c[1]}+{c[2]})" for c in weak))
    print()
    print("【可入库骨架卡片】")
    print("---")
    print(f"### 对标拆解 · 《{r['title']}》")
    print(f"- 靶心情绪：{emo}")
    print(f"- 钩子公式：{r['hook_formula']}")
    print(f"- 关系模型：{', '.join(r['relation_models']) or '无'}")
    print(f"- 反转点：{'；'.join(f'第{a}句' for a, _ in rp) or '无'}")
    print(f"- 结尾类型：{r['tail_type']}")
    print(f"- 机检评分：{r['score_10']}/10")
    if is_new:
        lib_txt = "★ 全新关系轴（强烈建议入库）"
    elif strong:
        lib_txt = ", ".join(f"{c[0]}({c[1]}+{c[2]})" for c in strong)
    else:
        lib_txt = "★ 情绪×关系新组合（关系已有·情绪新）"
    print(f"- 弹药库对照：{lib_txt}")
    print(f"- 可借鉴点：{r['learn']}")
    print("---")


def main():
    ap = argparse.ArgumentParser(description="短篇爆款结构体检 v3.2（情绪曲线+对标拆解）")
    ap.add_argument("path", nargs="?", help="故事文件(.md/.txt)")
    ap.add_argument("--dir", help="批量检查文件夹")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("--benchmark", action="store_true", help="对标拆解模式（输出方法论骨架）")
    ap.add_argument("--title", help="对标拆解时的作品标题（默认从首行 # 提取）")
    args = ap.parse_args()

    if args.dir:
        if not os.path.isdir(args.dir):
            print(f"目录不存在: {args.dir}")
            sys.exit(1)
        files = [os.path.join(args.dir, f) for f in os.listdir(args.dir)
                 if f.endswith((".md", ".txt"))]
        if not files:
            print("目录内无 .md/.txt 文件")
            sys.exit(1)
        results = [analyze_benchmark(f) if args.benchmark else analyze(f) for f in files]
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            for r in results:
                (print_benchmark if args.benchmark else print_report)(r)
                print()
            avg = sum(r["score_10"] for r in results) / len(results)
            print(f"批量完成: {len(results)} 篇, 平均评分 {avg:.1f}/10")
        return

    if not args.path:
        ap.print_help()
        sys.exit(1)
    if not os.path.exists(args.path):
        print(f"文件不存在: {args.path}")
        sys.exit(1)
    try:
        r = analyze_benchmark(args.path, args.title) if args.benchmark else analyze(args.path)
    except Exception as e:
        print(f"分析失败: {e}")
        sys.exit(1)
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        (print_benchmark if args.benchmark else print_report)(r)


if __name__ == "__main__":
    main()
