# Agent Adapters Matrix

This repository's `skill/short-story-hit/` is a universal skill package that can be loaded by many Agent frameworks.
Loading methods per platform:

| Platform | How to load | Notes |
|----------|-------------|-------|
| **ima.copilot** | `ima_skill_create -d skill/short-story-hit` | Native platform registration; takes effect in new chats automatically |
| **Claude Code** | Copy to `~/.claude/skills/short-story-hit/` or reference `SKILL.md` | `scripts/install.sh` copies automatically |
| **Cursor** | `~/.cursor/skills/short-story-hit/` or put `SKILL.md` into rules | Same as above |
| **SkillHub** | Upload `skill/short-story-hit/` (SKILL.md + references/ + scripts/) | Loaded per skill-market spec |
| **OpenClaw / Generic Agent** | `~/.openclaw/skills/short-story-hit/` or reference `SKILL.md` | Read Markdown directly |

## Progressive Disclosure (3-tier loading)

1. **Metadata** (name + description) — always in context, used for trigger matching.
2. **SKILL.md body** — loaded when the skill triggers (dual-engine theory + 6-step flow + routing).
3. **references/ docs** — loaded on demand (scripts run without loading).

> Recommended: load `SKILL.md` first, then read the relevant reference by stage/need; avoid loading all references at once to save context.

## Cross-platform notes

- All filenames are ASCII; no absolute paths; zero external dependencies (`skill/short-story-hit/scripts/*.py` uses Python stdlib only).
- Output attribution follows `COPYRIGHT.md`, independent of any specific Agent environment.
- Long-form mode (50k-word novella) is confirmed with the user at planning time, then planned via `longform-blueprint.md`.

## Integration with drama-studio

This skill produces a **short-story skeleton**. To turn it into a script / storyboard (short drama / comic drama), hand off to `drama-studio` with: target-card + relationship-progression-table + reversal-point notes.
