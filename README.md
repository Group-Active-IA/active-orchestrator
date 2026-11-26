# Active Orchestrator

Active Orchestrator helps choose between direct work and project foundation. It
recommends a route based on expected duration, continuity and coordination. The
user can choose either route. Direct work proceeds without creating foundation
files.

## Foundation

The orchestrator previews a checklist before any write. It lists every phase
with its benefit and the cost of skipping it, then lets you choose with the
client's selector or a numbered list. Choosing is separate from approving. A
foundation includes a knowledge base, a local roadmap, an explicit tracking
choice and agent instructions. Compatible artifacts and approved choices can be
reused. Choose whether to use ClickUp in the checklist. With ClickUp, setup
verifies the destination list and its development statuses before foundation
completes. Product discovery, visual design, skill search and the skill
registry are optional. Each selection shows its variant, dependencies and
outputs. Use native multi-select where available or reply to the numbered text
list.

Approve the ordered plan to run it. Phase-specific approvals still apply when
needed, for example when installing global skills or approving visual assets.
The orchestrator saves the approved plan in `.active-orchestrator-state.json`
and can resume after an interruption. Older foundation files remain compatible.

| Command | Purpose |
|---|---|
| `/active-orchestrator:init` | Choose a route or resume an approved plan |
| `/active-orchestrator:discovery` | Run product discovery |
| `/active-orchestrator:kb` | Create, import or reuse a KB |
| `/active-orchestrator:design` | Set or revise the visual policy |
| `/active-orchestrator:task-management` | Choose local tracking or configure ClickUp |
| `/active-orchestrator:rules` | Generate, update or reuse agent instructions |
| `/active-orchestrator:find-skill` | Find project skills |
| `/active-orchestrator:registry` | Index available skills |
| `/active-orchestrator:devops` | Run optional DevOps scaffolding when installed |

In Claude Code, write these commands with a space instead of the colon, for
example `/active-orchestrator init` or `/active-orchestrator kb`.

The skill delegates phases to available skills on Claude, Codex, OpenCode and
Antigravity. See [SKILL.md](SKILL.md) for the phase and state contract.

## Install

```bash
npx skills add https://github.com/Group-Active-IA/active-orchestrator
```

## License

MIT
