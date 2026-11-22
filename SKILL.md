---
name: active-orchestrator
description: >
  Recommend a direct route or coordinate project foundation. Preview a selectable
  plan, reuse existing artifacts, delegate the chosen phases and resume safely.
  Trigger: /active-orchestrator:init (in Claude Code: /active-orchestrator init) or
  requests to start or resume foundation.
license: MIT
metadata:
  author: juancruzrobledo
  version: "2.8"
---

# Active Orchestrator

## Route selection

Read available project files and ask only for missing facts about expected duration,
continuity, and coordination. Recommend the direct route for a bounded task with
clear acceptance and verification, expected to fit in about one day. Recommend
foundation when work is likely to extend across sessions or days, needs handoffs,
or involves coordination or durable decisions. One day is a reference. Explain
the recommendation briefly, allow the user to correct the route, and wait for their
choice. Reassess if scope or coordination grows. The direct route has no foundation writes,
installations or sub-skill dispatches.

## Checklist and approval

1. Inspect the repository read-only. Detect existing state, outputs, available
   skills, external prerequisites, target agent and interface capabilities.
2. Show a single checklist for foundation. For every phase show its purpose, expected
   artifacts, required or optional status, prerequisites, available variants, and
   reusable files with paths. Include extensions only when their contracts provide
   the same fields, their inputs and outputs, and their state owner.
3. Offer multi-select and variant choice using native controls if available.
   Otherwise show a numbered text list and accept e.g. `1=reuse, 2=local-markdown,
   3=generate, 5=off`. Require all three core outputs. Mark missing prerequisites
   as blockers and explain any prerequisites brought in by an option. Resolve all
   variants before approval. Show explicit skipped and deferred options.
4. Summarize the ordered plan, reuse choices, writes, installs and external actions.
   List every file each phase writes, including the policy record that
   `visual-design` keeps in `design-system/README.md` even for `off`.
   Get explicit approval before writing any state or artifact, running initialization,
   installing anything or connecting external services. Cancel or leave an
   unconfirmed plan without side effects. A new or changed plan requires approval.
   A reply that only selects phases or variants changes the plan but does not
   approve it: show the resulting summary and wait for explicit approval, even
   when the selection matches the recommendation. Record the approval date only
   after that explicit approval.
5. Run the approved plan. Pause for phase-specific user decisions including discovery
   answers, approval of a visual design, explicit global installation choices,
   permission to modify existing instructions and any unapproved external writes.
   Routine phase completion requires only a concise result report. Pause safely
   when the user asks to stop, a requirement is unavailable or a phase fails.

## Phase catalog

| ID | Selection | Skill | Purpose and outputs | Requirements | Variants |
|---|---|---|---|---|---|
| `discovery` | Optional | discovery-research | Reduce product uncertainty. `discovery/discovery.md` and `state.discovery`. | Evidence, user input, or competitor URLs. | interview, existing-sources, competitors, reuse |
| `kb` | Required | kb-creator | Record domain and decisions. Canonical `knowledge-base/` and `state.kb`. | User input, sources, or usable existing KB. | interview, import, reuse |
| `visual-design` | Optional | design-system | Agree on a visual policy. `state.visual_design` and visual assets when selected. | Visual surface for system generation. | system-and-mockups, system-only, off, deferred, reuse |
| `roadmap` | Required | roadmap-generator | Prioritize work and record dependencies. Local `CHANGES.md` and `state.roadmap`. | KB. | local-markdown, reuse |
| `task-management` | Optional | active-orchestrator | Choose local tracking or a ClickUp list for this project. Configuration in `.active-stack/roadmap.json`. | Validated `CHANGES.md`; for ClickUp, the `active-roadmap` skill and confirmed destination. | local, clickup |
| `team-mode` | Optional | active-orchestrator | Define the team and its working rules. `.active-stack/team.json`, `.github/pull_request_template.md`, `.github/CODEOWNERS`, ignore rules for local team files and `state.foundation.phases["team-mode"]`. | Local roadmap; for ClickUp, the `active-roadmap` skill. | new, reuse, update |
| `memory-policy` | Optional | active-orchestrator | Choose the team memory policy for this project. `.engram/config.json` and `.engram/active-stack.json` (written by `active-stack memory init`, only for `cloud-branch`), ignore rules in `.gitignore`, and `state.foundation.phases["memory-policy"]`. | The `active-stack` command; a Git repository. | cloud-branch, local, deferred, reuse |
| `find-skill` | Optional | find-skill | Recommend or install relevant skills. `state.skills`. | Project stack or user-supplied criteria. | recommend, install-selected |
| `registry` | Optional | skill-registry | Index available skills. `.atl/skill-registry.md` and `state.registry`. | Inventory, after skill installation if selected. | index, reuse |
| `agents` | Required | agent-instruction | Record operating rules and references. Applicable agent instruction file and `state.agents`. | KB and roadmap; registry when selected or reused. | generate, update, reuse |

Run discovery before KB, task management after roadmap, and the registry before
instructions when selected. Run team mode after task management and before the agent
instructions, because the team rules section is written together with them. Run memory policy after team mode and before the agent instructions. The required roadmap remains local Markdown. A
project without UI can choose visual off or omit
visual setup. Missing optional phases can be skipped with user confirmation and
their dependents must be revalidated. Missing required phases block completion
until the user approves an installation, changes the plan or provides compatible
existing outputs.

Product discovery owns top-level `state.discovery` and can delegate competitor
analysis to web-scraper. KB architecture discovery owns `state.kb.discovery` and
can use product research as input. Keep these sections independent.

## Dispatch and entrypoints

Use the host's available tools on Codex, Claude, OpenCode and Antigravity. Invoke
the selected phase inline if skill delegation is unavailable. Pass the confirmed
phase ID, variant, inputs, expected outputs and root path for
`.active-orchestrator-state.json`. The phase owner performs phase work and reports
results. The orchestrator routes, validates and tracks progress.

Run interactive phases inline when a delegate cannot ask the user. For agent
instructions, pass the global instruction file resolved by the active client,
when present, so the phase can keep project rules focused on this repository.

`/active-orchestrator:init` and direct activation start route selection or offer to
resume the approved plan. Existing standalone entrypoints `:discovery`, `:kb`,
`:design`, `:rules`, `:find-skill`, `:registry`, `:task-management`, `:team`, `:memory` and
`:devops` select only
their named phase or extension. Claude Code has no colon entrypoints: invoke the
skill as `/active-orchestrator` followed by the action, such as
`/active-orchestrator init`, `/active-orchestrator kb`, `/active-orchestrator team` or `/active-orchestrator memory`, and use that form when
suggesting a command there. Check its prerequisites and preview its effects
before confirmation. Preserve a completed foundation when running a standalone
phase. If a phase or extension is unavailable, report it and offer read-only ways
to inspect or satisfy its prerequisites.

### Task management

Resolve paths relative to the project root. Read any existing
`.active-stack/roadmap.json` and show the saved choice and destination. A project
without configuration uses local by default. Offer ClickUp only if `active-roadmap` is available
in the active client. If the skill is unavailable, explain that ClickUp setup
can be deferred, or use the local option. Preserve existing ClickUp
configuration when that capability is unavailable.

When the user chooses ClickUp, invoke `active-roadmap` in `configure` mode.
Pass the project root and saved destination, if any. Ask for the target list
and optional workspace when they are unknown. Follow the skill's diagnosis
and read-only list validation before any project configuration write. Use the
returned list identity and name to preview the validated destination and
known assignee mappings. If validation fails, explain the blocker and let the
user defer or explicitly choose local. On defer, preserve any existing configuration.
Require explicit approval before writing the configuration, including when
changing an existing destination. Save it without credentials or remote writes.
Use `{"mode":"clickup","project_id":"1db31293-15a1-442b-984e-2d4627c4cdc8","list_id":"901234567","assignees":{"Ana":"12345"}}`
as the shape, with the confirmed nonempty list ID in `list_id` and known
pairs of exact roadmap names and confirmed account IDs in `assignees`. The
`workspace_id` is optional. Include it when known. Use strings for IDs and leave
unknown accounts out of the map. Preserve the existing project ID when editing
the configuration so linked tasks keep their identity. For a new project
without a stable ID, generate a UUID once and retain it for future updates.

For an approved explicit local choice, save `{"mode":"local"}`, retaining any
established `project_id`; if skipped, record the phase choice without writing
this file. Validate the saved configuration before marking the selected phase done.
Use the backup and atomic write rules for existing project files.

The roadmap keeps scope and dependencies. ClickUp manages operational
assignees and status when configured. Point the user to `active-roadmap` for
preview, confirmation, publication and reconciliation. Foundation setup
does not publish tasks. Leave existing links and status evidence in
`.active-stack/roadmap-state.json` intact.

### Team mode

Optional phase for a repository where several people work together. Foundation
without team mode is unchanged: nothing in this section runs and no team file is
created. The phase has the variants `new`, `reuse` and `update` and the same
approval rules as the other phases. Resolve paths relative to the project root.

1. Ask whether this is a team project. If the answer is "no" or "later", nothing is
   written and the choice is recorded as `skipped` or `deferred`.
2. Ask for the team: the size is required, an integer at least 2. Names are optional
   and a missing name stays pending as `Integrante N`. Never invent names or accounts.
   Ask for the tracking tool (`local` or `clickup`) and for the primary and backup
   reviewer of risk zones. A GitHub account per member is optional.
3. Ask about privacy. If the repository is public, explain first that names in
   `team.json` become visible to anyone, and then ask: "Do we version the names in
   the repository?" Record the answer as `names_versioned`. With "no", `team.json`
   carries only `size` and the names and links go to `.active-stack/team.local.json`.
   Add the ignore rules for `.active-stack/team.local.json` and
   `.active-stack/me.local.json` to `.gitignore` inside idempotent markers.
4. For ClickUp, offer it only if `active-roadmap` is available in the active client.
   Resolve each name with `find_member_by_name` or `resolve_assignees`, confirm each
   match with the person and save the numeric ID. On no match the member stays
   unlinked: never guess. If the connector is down or unavailable, tracking stays
   `local` and the ClickUp link is deferred.
5. Show a summary of every file to write and every external action, including the
   `.gitignore` rules, `.github/pull_request_template.md` and `.github/CODEOWNERS`,
   and wait for explicit approval. A reply that only answers questions is not an
   approval.
6. Validate the draft before writing, with the shared contract of `active-delivery`:
   `sh <active-delivery-dir>/team.sh --root <project> validate --file <draft>` in POSIX
   shells, or `<active-delivery-dir>\team.bat --root <project> validate --file <draft>`
   on Windows. If `active-delivery` is not available in the active client (OpenCode
   and Antigravity do not install it), there is no automatic validator: check the draft
   against these rules instead and say so. The size is an integer at least 2; there are
   at most `size` members; ids are unique, in lowercase letters, digits and hyphens;
   `tracking` is `local` or `clickup`; `clickup_id` appears only with `clickup`; there
   are no unknown fields. No field or file accepts credentials. Show errors as they are
   and never repair team data on your own.
7. Write the files. Back up existing files before changes and write atomically. Write
   `.active-stack/team.json`, then `.github/pull_request_template.md` and
   `.github/CODEOWNERS`. Copy the template as it is from
   `assets/pull_request_template.md` (the six handoff facts) and follow the format of
   `assets/CODEOWNERS.example`; never invent other content for them. Never overwrite an existing `.github/CODEOWNERS` or
   `.github/pull_request_template.md`: show the diff and propose the merge.
   Build `CODEOWNERS` from the `Zona` of each ficha in `CHANGES.md` plus the primary
   and backup reviewer. Members without `github` are left out of the file, with a note.
8. Dispatch `agent-instruction` to write the team rules section, delimited by
   `<!-- active-stack:team-mode -->` and `<!-- /active-stack:team-mode -->`, in the
   project instruction file of each approved agent. Pass the confirmed team. The
   orchestrator does not write the project instruction file itself.
9. Protecting `main` on GitHub is only offered. Offer it once: a pull request required, a required check if
   one exists and no force-push. Show the `gh` command and run it only after explicit
   confirmation. Without permission or on an unsupported plan, say so and leave the
   convention written in the rules. Record the choice in the state so the phase does
   not ask again.
10. Record `foundation.phases["team-mode"]` in the foundation state. Mark it `done`
    only after verifying that every approved file exists and passes validation.
    `team.json`, the phase record and the rules section are written together: other
    tools read that record as the signal of a team project. Propose a single commit
    with them. Never commit or push on your own.

Foundation does not choose the person's identity on its own. After the files are
verified, offer the person doing the foundation to pick their own seat: suggest the
member that matches the account in `github` (read with `gh api user`), or let them
choose from the list, or leave them in consult mode (read-only) if nobody matches.
Write `.active-stack/me.local.json` only after the person confirms; it is local and
never versioned. The person can skip this step. Everyone else chooses theirs on their
first session through `active-delivery`.

For a fresh clone where `team.json` already exists in `.active-stack/`, use the `reuse`
variant: validate it, never rewrite an existing `team.json`, and offer to create the
missing local files (`me.local.json`, and `team.local.json` when names are not
versioned) with the same approval rules. For a partial foundation, inspect the files
first and continue only with what is missing, following the resume rules.

Foundation does not hide the phase in OpenCode and Antigravity: it records the team, the
rules and the convention there, and says that the guided delivery flow does not exist
in that client. The phase needs no Claude-only or Codex-only tools. Without
`active-roadmap`, tracking stays `local`. A project that already has the files can
`reuse` them after read-only validation.

#### Update team

Entrypoint `:team` (`/active-orchestrator team` in Claude Code); `active-delivery` can
invoke it too. It changes the team without regenerating the approved foundation:
add or remove members, rename them, complete pending names, change the team size,
link or fix GitHub and ClickUp accounts, and switch tracking between `local` and
`clickup`.

- Show a preview of the diff of `team.json`, of `CODEOWNERS` and of the fichas whose
  `Responsable` becomes orphaned. Propose reassigning them. Nothing is reassigned
  without approval, and fichas already started are not touched.
- It is idempotent: the same input produces the same bytes. Use `version` in
  `team.json` to migrate the format; an unknown version pauses with a clear error.
- A person who joins later clones the repository and chooses an identity through
  `active-delivery`; update links them if the seat is pending.
- When resuming, report what is still pending: names without a value, ClickUp
  without a link and `main` without protection.

### Memory policy

Optional phase that records how the team memory (Engram) works in this project.
Foundation without memory policy is unchanged: nothing in this section runs, no
`.engram/` file is touched and no state record is added. The phase has the choices
`cloud-branch`, `local` and `deferred`, plus `reuse` when a choice is already recorded,
and the same approval rules as the other phases. It needs a shell command and no
client-specific tool, so it is offered the same way in Codex, Claude, OpenCode and
Antigravity. Resolve paths relative to the project root.

1. Offer the choice once, with a short explanation:
   - `cloud-branch`: the project pins its Engram project name and the team policy in two
     versioned files. It invokes `active-stack memory init` (see below).
   - `local`: memory stays personal and local. It does not invoke `active-stack memory init`
     and writes no `.engram/` file; the choice is only recorded.
   - `deferred`: decide later. It does not invoke `active-stack memory init` and writes no
     `.engram/` file; the choice is only recorded and the phase never asks again.
2. For `cloud-branch`, check that the project is a Git repository and that `active-stack`
   is available. If `active-stack` is not available, say so, the phase stays `pending`
   and never create the files by hand: never write `.engram/config.json` or
   `.engram/active-stack.json` yourself, and never edit `.gitignore` for them.
3. Show a summary of what `cloud-branch` writes: `.engram/config.json` (the
   `project_name` key, completed without touching other keys), `.engram/active-stack.json`
   (`{"memory_policy":"cloud-branch"}`), the `.gitignore` block that ignores the rest of
   `.engram/`, a backup of the files that already exist, and the state record. Wait for
   explicit approval. A reply that only answers questions is not an approval.
4. Run `active-stack memory init --json --project <project root>` and read its JSON
   (`status`, `reason`, `project_name`, `files`, `warnings`, `proposed_commit`). The project
   name is derived from the `origin` remote or the folder; the person must confirm it. If
   the command stops with `name_not_confirmed`, show the derived name, ask, and run it
   again with `--name <confirmed name>`. Never pass `--yes` on the person's behalf.
   - Exit code `0` (`status: ok`): the files are ready or already up to date.
   - Exit code `3` (`status: needs_decision`): it stopped so as not to overwrite something
     of the person (`conflict_value`, `conflict_ignored_dir`, `conflict_still_ignored`,
     `conflict_not_ignored`, `name_declined`). Show the `reason` and `detail` as they are.
     Never force or overwrite, never retry with other values on your own, and leave the
     phase `pending` until the person resolves the conflict.
   - Exit code `1` (`status: error`, for example `invalid_file`, `not_git_repo`,
     `git_missing`, `backup_failed`, `failed`): report it as it is and leave the phase `pending`.
   - Exit code `2` is a wrong invocation: fix the call, not the project.
5. Show the proposed commit from `proposed_commit` (message, files and commands) and the
   `warnings` as they are. The commit is only proposed: never run `git add`, `git commit`
   or `git push`; the person runs it, or decides not to. If nothing is pending, say so.
6. Record the choice in `.active-orchestrator-state.json` as
   `foundation.phases["memory-policy"]`, and nowhere else (DA-07): do not copy it to
   `.active-stack/roadmap.json`, because the choice belongs to the foundation and a
   second copy could drift. Shape:
   `{"variant":"cloud-branch","status":"done","requires":[],"outputs":[".engram/config.json",".engram/active-stack.json"],"decided_on":"2026-11-21"}`.
   `variant` is `cloud-branch`, `local` or `deferred`; `status` is `pending`, `done` or
   `deferred`; `decided_on` is the date of the approval. The record is `done` only after
   `memory init` ended with exit code `0` and the files were verified; a `cloud-branch`
   that has not run yet or stopped is `pending`; `local` is `done` once approved and has
   no outputs; `deferred` is `deferred`. Record it outside the execution order, like the
   other optional decisions. Back up the state, write atomically, reread it, preserve
   all existing and unknown sections, and do not change the schema version or `step`.
   Versions 2 to 5 of the file stay valid: never rewind or replay a completed phase just
   to add this record, and keep `step: done` when the foundation was complete. If the
   file has no `foundation` section, add only this record after approval.

Resume and reuse work like `visual_design`: read the record before asking anything.
With `done`, report the recorded choice and do not ask again; offer to verify the two
files read-only if `cloud-branch`. With `pending`, offer to resume: run
`active-stack memory init` again, which is idempotent and reports a no-op when
everything is up to date. With `deferred`, the phase never asks again: unlike
`visual_design`, no later step revisits it, and only an explicit `:memory`
(`/active-orchestrator memory` in Claude Code) can change the choice, with a preview and
approval. With no record, the choice has not been made: offer it once as part of the
checklist, where skipping is allowed and leaves the file untouched.

The marker acts only where the `engram-cloud` harness is installed, which is Claude and
Codex. In OpenCode and Antigravity the phase still records the choice and runs the
command, and says plainly that the marker has no effect there. Never copy the
`active-stack:engram-cloud` section or its rules into any project file: the harness owns
it in the global instruction file. Write no token or credential anywhere; the command
reads and writes none.

### Skill search

For either variant, dispatch `find-skill` in **recommend-only** mode. Pass
the stack, domains and problem from `state.kb.discovery` or the user's criteria.
Tell the skill to return the full recommendations table with names, sources,
install counts and fit, and forbid it from installing anything. Record the
recommendations in `state.skills.recommended`, preserving known installations.

For `recommend`, report the table and stop the phase there. For
`install-selected`, present the table and obtain explicit approval of the exact selections
using native multi-select or the numbered text list. Users can choose none.
The orchestrator installs only the approved picks, e.g.
`npx skills add <repo> --skill <name> -g` where supported. Check what is already
installed before retrying. Record only verified installations in
`state.skills.installed`; preserve existing entries and report partial failures.
If the registry was selected, build it after these results are available.

### Missing capabilities

Check the active client's skill inventory before each dispatch. If a selected
phase is unavailable, explain how the user can provide its prerequisite.
For a cloneable skill, resolve the source from the installed Active Stack
catalog. `design-system` is bundled with Active Stack. Direct users to the
installer's Full mode or Custom selection for that skill. Installing missing
skills requires explicit approval.

## State and resume

Use the existing project-root `.active-orchestrator-state.json`. Read versions 2–5.
Keep the shared version at 5 for newly created or migrated files, and extend it
with `foundation` version 1. The orchestrator owns the new section plus the shared
`version`, `step` and `owner` fields. Each sub-skill continues to own its existing
section, with the orchestrator coordinating skill installation results and
metadata registration for read-only reuse. Preserve unknown sections, plugin
data and existing phase payloads.
Back up existing files before changes, merge only owned fields into freshly read
state and write atomically. If state is malformed or a version is unsupported,
pause and ask before repairing or migrating.

Example after approval in a fresh project:

```json
{
  "version": 5,
  "step": "kb",
  "owner": "active-orchestrator",
  "foundation": {
    "version": 1,
    "order": ["kb", "roadmap", "agents"],
    "phases": {
      "kb": {"variant": "import", "status": "pending", "requires": [], "outputs": ["knowledge-base/"]},
      "roadmap": {"variant": "local-markdown", "status": "pending", "requires": ["kb"], "outputs": ["CHANGES.md"]},
      "agents": {"variant": "generate", "status": "pending", "requires": ["kb", "roadmap"], "outputs": ["AGENTS.md"]}
    }
  }
}
```

Record optional decisions outside the execution order with `skipped` or
`deferred` status. Set legacy `step` to the next unfinished phase, or `done`
when all required and selected phases are satisfied. Never mark a required phase
as skipped.

1. When there is an approved plan, show progress and offer resume. Use the stored
   variants and dependency order. Verify output paths and the phase-owned result
   before treating a phase as `done` or `reused`. Verify reusable artifacts match
   the output contract, including references before downstream execution. A plan
   may reference earlier artifacts without regenerating them. For `reuse`,
   dispatch the phase's read-only variant to verify the outputs and return
   paths and evidence. After approval, the orchestrator may register the verified metadata
   and paths if the matching phase-owned payload is absent or incomplete.
   Merge that metadata without rewriting the files or inventing provenance.
   Preserve existing fields and leave any disagreement for explicit repair.
2. Persist `in_progress` before dispatch and `done` after validating completion.
   Persist `failed` with the reason and keep later dependent phases pending. On
   resuming an interrupted or failed phase, inspect its artifacts first. If
   completion can be independently established, record it and proceed. If it left
   partial or inconsistent output, describe the repair and obtain confirmation
   before retrying or writing. Never replay validated completed or reused phases.
3. For a legacy file without a plan, use its `step` and existing phase payloads
   as hints, verify referenced and discovered artifacts, propose a plan with
   matching reusable phases, and migrate only after approval. Do not rewind to a
   retired phase. A completed legacy foundation remains complete unless the user
   identifies missing required output or requests a separately approved update.
   Missing visual policy is undecided and can be set as a standalone phase.
   A missing `memory-policy` record means the memory policy has not been decided, not
   that the user opted out; it can be set with the standalone `:memory` phase.
   Existing approved plans keep their stored phase order. Offer standalone
   `:task-management` when the user requests task tracking for an existing
   project with a usable `CHANGES.md`.
4. If confirmed outputs are missing or changed, describe which phases and dependent
   outcomes are affected and ask for approval before repair or replanning. Preserve
   valid outputs and plugin state. A declined repair leaves the current state as is.

Completion reports list created, reused, skipped and deferred phases with output
paths, plus any concrete blockers. Use the active client's invocation syntax
when pointing to a standalone phase or a workflow the user has already chosen.
Speak the user's language.
