# short-story-hit · Hit Short-Story Writing Skill

> **🌐 Language / 语言**: [中文](README.md) ｜ [English](README.en.md)

> A methodology for writing hit short stories / flash fiction (the **Hook + Relationship dual-engine**). Turn "writing by feel" into "building by methodology."
> Version: v2.0.0 ｜ License: MIT ｜ Multi-Agent ready (ima.copilot / Claude Code / Cursor / SkillHub / OpenClaw …)

---

## 1. Features

- **Dual engine**: Hook engine (5 formulas + templates + three-sentence rule) + Relationship engine (three laws + 6 high-tension models + progression table)
- **6-step flow**: Lock the emotional target → Drop the hook → Arrange relationships → Set the reversal → End with a hook → Self-check
- **Arsenal**: 50 opening hooks + title formulas + 20 closing one-liners
- **Case matrix**: 4 emotions × 6 relationships quick reference
- **Character builder / AI expansion prompts / serialization & sequel hooks / anti-cliché innovation**
- **Long-form mode**: 50k-word novella blueprint (long-arc structure + character arc + foreshadowing system) + continuity self-check script
- **Structure checker**: sentence-by-sentence hook analysis + emotion segmentation + relationship suggestions + batch check + 10-point score + `--benchmark` teardown mode
- **Hand-off protocol to `drama-studio`** (short story → script / storyboard)

## 2. Repository Structure (GitHub standard)

```
short-story-hit/
├── skill/short-story-hit/        # The skill package (uploadable / registerable)
│   ├── SKILL.md                  # Entry: dual-engine theory + 6-step flow + routing
│   ├── scripts/                  # Self-contained tools (stdlib only, zero deps)
│   │   ├── structure_check.py    # Structure checker v3.2 (emotion curve + per-line tips + score + benchmark)
│   │   └── continuity_check.py   # Continuity checker v1.0 (long-form: dangling foreshadow + chapter hook density)
│   └── references/               # Method docs (ASCII filenames, incl. cases/ clean samples)
│       ├── hook-design.md        # Hook formulas + templates + three-sentence rule
│       ├── relationship-design.md# Relationship laws + 6 models + progression table
│       ├── emotion-curve.md      # Emotion curve and reversal rhythm
│       ├── platform-adapt.md     # Platform adaptation
│       ├── hit-checklist.md      # Self-check checklist and red lines
│       ├── examples.md           # Demonstration cases (line-by-line breakdown)
│       ├── hook-arsenal.md       # Arsenal: 50 hooks + titles + one-liners
│       ├── case-matrix.md        # Case matrix 4×6
│       ├── character-builder.md  # Character quick-builder
│       ├── ai-expand-prompt.md   # AI expansion prompts
│       ├── serial-hook.md        # Serialization & sequel hooks
│       ├── anti-cliche.md        # Anti-cliché and innovation
│       ├── information-gap.md    # Information-gap management
│       ├── death-causes.md       # Top 10 failure causes (bad → diagnose → fix)
│       ├── release-kit.md        # Publishing kit + platform checklist
│       ├── longform-blueprint.md # 50k-word long-form blueprint
│       └── cases/                # Clean sample stories (8, no annotations)
├── docs/agent-adapters.md        # Multi-Agent adapter matrix (zh)
├── docs/en/agent-adapters.md     # Multi-Agent adapter matrix (en)
├── examples/sample-story.md      # Demonstration short story (dual-engine demo, not final)
├── scripts/                      # Installers (not skill content)
│   ├── install.sh                # Linux/macOS install
│   └── install.bat               # Windows install
├── LICENSE                       # MIT
├── COPYRIGHT.md                  # Integrated copyright note
├── CONTRIBUTING.md               # Contributing guide
├── CHANGELOG.md
├── README.md / README.en.md
```

> Scripts are bundled under `skill/short-story-hit/scripts/` so the package is self-contained with zero external path dependencies.

## 3. Install

```bash
# ima.copilot (recommended, native registration)
ima_skill_create -d skill/short-story-hit

# or cross-platform one-click (Claude Code / Cursor / OpenClaw)
bash scripts/install.sh        # Linux/macOS
scripts\install.bat            # Windows
```

SkillHub users: upload the `skill/short-story-hit/` directory (SKILL.md + references/ + scripts/) directly; the platform loads it per its skill-market spec.

## 4. Quick Start

Follow the 6-step flow in SKILL.md. After writing, run the checker:

```bash
# single file
python3 skill/short-story-hit/scripts/structure_check.py your_story.md
# batch
python3 skill/short-story-hit/scripts/structure_check.py --dir your_folder/
```

For long-form (50k-word novella), run the continuity check after drafting:

```bash
python3 skill/short-story-hit/scripts/continuity_check.py your_story.md
```

## 5. Copyright

- Repository license: MIT (see `LICENSE`), copyright "灵析剧创 · 智子编辑部" (ima.copilot).
- Output attribution rules: see `COPYRIGHT.md`.
