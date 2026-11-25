"""Smoke tests for the published foundation skill instructions."""

from pathlib import Path
import json
import re
import unittest


SKILL = (Path(__file__).resolve().parents[1] / "SKILL.md").read_text(encoding="utf-8")


def section(heading):
    match = re.search(rf"(?ms)^## {heading}\n(.*?)(?=^## |\Z)", SKILL)
    return match.group(1) if match else ""


class FoundationContract(unittest.TestCase):
    def test_variant_only_reply_is_not_an_approval(self):
        checklist = section("Checklist and approval")
        self.assertIn("only selects phases or variants changes the plan but does not", checklist)
        self.assertIn("wait for explicit approval", checklist)
        self.assertIn("approval date only", checklist)

    def test_claude_code_uses_space_separated_entrypoints(self):
        self.assertIn("/active-orchestrator init", SKILL)
        self.assertIn("Claude Code has no colon entrypoints", SKILL)

    def test_direct_route_has_no_foundation_side_effect(self):
        route = section("Route selection")
        self.assertIn("one day", route)
        self.assertIn("no foundation writes", route)
        self.assertRegex(route, "(?i)reassess if scope or coordination grows")

    def test_checklist_requires_foundation_outputs_and_tracking_choice(self):
        table = section("Phase catalog")
        required = re.findall(r"^\| `([a-z-]+)` \| Required \|", table, re.MULTILINE)
        self.assertEqual(required, ["kb", "roadmap", "task-management", "agents"])
        checklist = section("Checklist and approval")
        self.assertIn("numbered text list", checklist)
        self.assertIn("before writing", checklist)

    def test_task_management_is_required_and_depends_on_the_local_roadmap(self):
        phase = next(
            line for line in section("Phase catalog").splitlines()
            if line.startswith("| `task-management`")
        )
        self.assertIn("| Required |", phase)
        self.assertIn("`CHANGES.md`", phase)
        self.assertIn(".active-stack/roadmap.json", phase)
        self.assertIn("local, clickup", phase)

    def test_task_management_requires_available_skill_and_approved_config(self):
        dispatch = section("Dispatch and entrypoints")
        setup = dispatch.split("### Task management", 1)[1].split("### ", 1)[0]
        checklist = section("Checklist and approval")
        self.assertIn('Will this project use ClickUp?', checklist)
        self.assertIn("explicit yes", checklist)
        self.assertIn("answers on every client", checklist)
        self.assertIn("legacy skipped or deferred phase records", setup)
        self.assertIn("reuse the explicit choice on", setup)
        self.assertIn("before writing the configuration", setup)
        self.assertIn("without credentials or remote writes", setup)
        self.assertIn("`:task-management`", dispatch)
        self.assertIn("`list_id`", setup)
        self.assertIn("`assignees`", setup)

    def test_clickup_identity_survives_configuration_edits(self):
        setup = section("Dispatch and entrypoints").split("### Task management", 1)[1]
        example = re.search(r"Use `({.*})`", setup)
        config = json.loads(example.group(1))
        self.assertEqual(config["mode"], "clickup")
        self.assertIsInstance(config["project_id"], str)
        self.assertIsInstance(config["list_id"], str)
        self.assertEqual(config["assignees"], {"Ana": "12345"})
        self.assertIn("Preserve the existing project ID", setup)
        self.assertIn("`workspace_id` is optional", setup)

    def test_clickup_list_is_read_and_confirmed_before_configuration_write(self):
        setup = section("Dispatch and entrypoints").split("### Task management", 1)[1]
        self.assertRegex(setup, r"invoke `active-roadmap` in `configure` mode")
        validation = setup.index("read-only list validation")
        preview = setup.index("preview the validated destination")
        approval = setup.index("approval before writing the configuration")
        self.assertLess(validation, preview)
        self.assertLess(preview, approval)

    def test_failed_destination_validation_preserves_existing_configuration(self):
        setup = section("Dispatch and entrypoints").split("### Task management", 1)[1]
        self.assertIn("the list lacks required statuses", setup)
        self.assertIn("`status: pending`", setup)
        self.assertRegex(setup, r"explicitly\s+choose local")
        self.assertIn("preserve any existing configuration", setup)
        self.assertIn("Save it without credentials or remote writes", setup)

    def test_clickup_requires_workflow_statuses_before_task_management_completes(self):
        setup = section("Dispatch and entrypoints").split("### Task management", 1)[1].split("### ", 1)[0]
        self.assertIn("`clickup_get_list`", setup)
        self.assertIn("statuses <snapshot.json>", setup)
        for label in ("Pendiente", "En desarrollo", "En revisión", "Cambios solicitados", "Fusionado", "Archivado"):
            self.assertIn(label, setup)
        self.assertLess(setup.index("then read the list again"), setup.index("Mark the phase `done`"))

    def test_resume_reuses_existing_choices_and_prompts_for_unfinished_legacy_plans(self):
        resume = section("State and resume")
        self.assertIn("without an explicit task-management decision", resume)
        self.assertIn("ask the required", resume)
        self.assertIn("without replaying completed phases", resume)
        self.assertIn("completed legacy foundation remains complete", resume)

    def test_resume_preserves_sections_on_failure_or_migration(self):
        resume = section("State and resume")
        for requirement in ("versions 2–5", "unknown sections", "failed", "reused"):
            self.assertIn(requirement, resume)
        self.assertNotIn("delete .active-orchestrator-state.json", SKILL)

    def test_never_runs_sdd_initialization(self):
        self.assertNotIn("openspec init", SKILL.lower(), "The foundation must not initialize SDD")

    def test_confirmed_plan_example_is_dependency_ordered(self):
        resume = section("State and resume")
        example = re.search(r"```json\n(.*?)\n```", resume, re.DOTALL)
        state = json.loads(example.group(1))
        self.assertEqual(state["version"], 5)
        self.assertEqual(state["foundation"]["version"], 1)
        foundation = state["foundation"]
        self.assertEqual(state["step"], foundation["order"][0])
        earlier = set()
        for phase in foundation["order"]:
            entry = foundation["phases"][phase]
            self.assertEqual(entry["status"], "pending")
            self.assertTrue(entry["outputs"])
            self.assertLessEqual(set(entry["requires"]), earlier)
            earlier.add(phase)

    def test_checklist_can_skip_visual_and_build_rules_without_registry(self):
        phase_catalog = section("Phase catalog")
        visual = next(line for line in phase_catalog.splitlines() if "`visual-design`" in line)
        self.assertIn("| Optional |", visual)
        self.assertIn("off, deferred, reuse", visual)
        rules = next(line for line in phase_catalog.splitlines() if "`agents`" in line)
        self.assertIn("registry when selected or reused", rules)

    def test_rules_resolve_global_instructions_for_the_active_client(self):
        dispatch = section("Dispatch and entrypoints")
        self.assertIn("global instruction file resolved by the active client", dispatch)
        self.assertNotIn("~/.claude/CLAUDE.md", dispatch)

    def test_skill_search_requires_explicit_install_choices(self):
        dispatch = section("Dispatch and entrypoints")
        search = dispatch.split("### Skill search", 1)[1]
        recommend_only = search.index("recommend-only")
        consent = search.index("explicit approval of the exact selections")
        install = search.index("npx skills add")
        self.assertLess(recommend_only, consent)
        self.assertLess(consent, install)
        self.assertIn("`state.skills.installed`", search)
        self.assertIn("only verified installations", search)

    def test_phase_reuse_records_owner_evidence_without_rewriting_outputs(self):
        resume = section("State and resume")
        self.assertIn("register the verified metadata", resume)
        self.assertIn("without rewriting the files", resume)


if __name__ == "__main__":
    unittest.main()
