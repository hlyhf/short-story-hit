#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""5万字短故事·连贯性自检（长-form模式配套 v1.0）

两大防崩检查：
  1) 伏笔回收检查：扫描 【伏笔:Vxx 铺设/回收】 标记，揪出悬空伏笔
     （只铺不收 / 只收不铺）——机械防烂尾。
  2) 章级钩子密度：按 #/## 标题分章，检查每章末句是否含钩子/反转词
     （防中段塌陷，每章末应留「下一章钩」）。

用法:
  python3 continuity_check.py 故事.md
  python3 continuity_check.py 故事.md --json
"""
import sys
import os
import re
import json
import argparse

HOOK = ["死", "杀", "仇", "复仇", "秘密", "真相", "原来", "竟", "却", "发现",
        "背叛", "隐藏", "诡异", "消失", "阴谋", "假", "骗局", "绑架", "威胁",
        "逃离", "揭穿", "谜", "背后", "究竟", "到底", "失踪", "骨灰", "鬼"]
REVERSE = ["原来", "竟", "竟然", "其实", "却", "但", "不过", "殊不知",
           "反转", "发现", "可是", "只不过", "竟是"]


def scan_foreshadow(text):
    pat = re.compile(r"【伏笔:(V\w+)\s*(铺设|回收)(?:[^】]*】)?")
    data = {}
    for m in pat.finditer(text):
        vid, kind = m.group(1), m.group(2)
        data.setdefault(vid, {"铺设": 0, "回收": 0})
        data[vid][kind] += 1
    return data


def chapter_split(text):
    lines = text.splitlines()
    chapters, cur = [], None
    for ln in lines:
        if re.match(r"^#{1,2}\s", ln):
            if cur:
                chapters.append(cur)
            cur = {"title": ln.strip(), "body": ""}
        elif cur is not None:
            cur["body"] += ln + "\n"
    if cur:
        chapters.append(cur)
    return chapters


def last_sentence(body):
    sents = [s.strip() for s in re.split(r"(?<=[。！？!?])", body) if s.strip()]
    return sents[-1] if sents else ""


def has_hook(sent):
    return any(w in sent for w in HOOK) or any(w in sent for w in REVERSE)


def main():
    ap = argparse.ArgumentParser(description="5万字短故事·连贯性自检（伏笔回收+章钩密度）")
    ap.add_argument("path")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if not os.path.exists(args.path):
        print("文件不存在:", args.path)
        sys.exit(1)
    text = open(args.path, encoding="utf-8").read()

    # 1) 伏笔
    data = scan_foreshadow(text)
    foreshadow_report, dangling = [], []
    for vid, d in sorted(data.items()):
        if d["铺设"] and d["回收"]:
            status = "OK"
        elif d["回收"] and not d["铺设"]:
            status = "只收不铺(坑未挖)"
        else:
            status = "只铺不收(悬空)"
        if status != "OK":
            dangling.append(vid)
        foreshadow_report.append({"id": vid, "铺设": d["铺设"],
                                  "回收": d["回收"], "status": status})

    # 2) 章钩
    chs = chapter_split(text)
    chapter_report, weak_chapters = [], []
    for c in chs:
        tail = last_sentence(c["body"])
        hk = has_hook(tail)
        if not hk and tail:
            weak_chapters.append(c["title"])
        chapter_report.append({"chapter": c["title"], "tail_hook": hk, "tail": tail[:30]})

    result = {"foreshadow": foreshadow_report, "dangling": dangling,
              "chapters_total": len(chs), "weak_chapters": weak_chapters}

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"文件: {args.path}")
    print(f"\n【伏笔回收检查】共 {len(foreshadow_report)} 个伏笔标记")
    if not foreshadow_report:
        print("  (未检测到【伏笔:】标记——若已用标记约定，请确认格式为【伏笔:Vxx 铺设/回收】)")
    for r in foreshadow_report:
        flag = "⚠" if r["status"] != "OK" else "✓"
        print(f"  {flag} {r['id']}: 铺设{r['铺设']} 回收{r['回收']} -> {r['status']}")
    if dangling:
        print(f"  ⚠ 悬空/残缺伏笔(必填坑): {', '.join(dangling)}")

    print(f"\n【章级钩子密度】共 {len(chs)} 章")
    if not chs:
        print("  (未检测到 #/## 章节标题——按章节写作时每章用 # 或 ## 起头便于自检)")
    for r in chapter_report:
        print(f"  {'✓' if r['tail_hook'] else '⚠'} {r['chapter'][:28]}: "
              f"章末{'有钩' if r['tail_hook'] else '无钩(建议补下一章钩)'}")
    if weak_chapters:
        print(f"  ⚠ 章末无钩(易塌陷): {len(weak_chapters)} 章")


if __name__ == "__main__":
    main()
