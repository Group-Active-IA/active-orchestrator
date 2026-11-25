"""Contract tests for the optional memory-policy foundation phase ([EN] Phase 11, R-19)."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")


def flat(text):
    # Markdown wraps lines; compare the text as rendered, with single spaces.
    return re.sub(r"\s+", " ", text)


def section(heading):
    match = re.search(rf"(?ms)^## {heading}\n(.*?)(?=^## |\Z)", SKILL)
    return match.group(1) if match else ""


def memory_policy():
    match = re.search(r"(?ms)^### Memory policy\n(.*?)(?=^#{2,3} |\Z)", SKILL)
    return flat(match.group(1)) if match else ""


def memory_row():
    return next(
        (line for line in section("Phase catalog").splitlines() if line.startswith("| `memory-policy`")),
        "",
    )


def catalog_order():
    return re.findall(r"^\| `([a-z-]+)` \|", section("Phase catalog"), re.MULTILINE)


class MemoryPhaseCatalogTests(unittest.TestCase):
    def test_memory_policy_is_an_optional_phase_with_its_outputs_and_choices(self):
        row = memory_row()
        self.assertIn("| Optional |", row)
        self.assertIn(".engram/config.json", row)
        self.assertIn(".engram/active-stack.json", row)
        self.assertIn('state.foundation.phases["memory-policy"]', row)
        self.assertIn("cloud-branch, local, deferred", row)

    def test_memory_policy_never_becomes_a_required_output(self):
        required = re.findall(r"^\| `([a-z-]+)` \| Required \|", section("Phase catalog"), re.MULTILINE)
        self.assertEqual(required, ["kb", "roadmap", "task-management", "agents"])

    def test_memory_policy_runs_after_team_mode_and_before_the_rules(self):
        order = catalog_order()
        self.assertLess(order.index("team-mode"), order.index("memory-policy"))
        self.assertLess(order.index("memory-policy"), order.index("agents"))

    def test_standalone_entrypoint_exists(self):
        dispatch = section("Dispatch and entrypoints")
        self.assertIn("`:memory`", dispatch)
        self.assertIn("/active-orchestrator memory", SKILL)

    def test_existing_phases_keep_their_relative_order(self):
        order = catalog_order()
        for before, after in (("discovery", "kb"), ("kb", "visual-design"), ("roadmap", "task-management"),
                              ("task-management", "team-mode")):
            self.assertLess(order.index(before), order.index(after))


class MemoryPolicyFlowTests(unittest.TestCase):
    def test_a_project_that_does_not_choose_it_is_unchanged(self):
        flow = memory_policy()
        self.assertRegex(flow, r"(?i)foundation without memory policy is unchanged")
        self.assertRegex(flow, r"(?i)nothing in this section runs")

    def test_three_choices_are_offered_with_their_meaning(self):
        flow = memory_policy()
        for choice in ("`cloud-branch`", "`local`", "`deferred`"):
            self.assertIn(choice, flow)
        self.assertRegex(flow, r"(?i)`local`:? .{0,160}does not invoke `active-stack memory init`")
        self.assertRegex(flow, r"(?i)`deferred`:? .{0,200}does not invoke `active-stack memory init`")

    def test_cloud_branch_invokes_memory_init_with_json_output(self):
        flow = memory_policy()
        self.assertIn("active-stack memory init", flow)
        self.assertIn("--json", flow)
        self.assertIn("--project", flow)

    def test_the_orchestrator_never_writes_the_engram_files_itself(self):
        flow = memory_policy()
        self.assertRegex(flow, r"(?i)never write `\.engram/config\.json` or `\.engram/active-stack\.json` yourself")

    def test_name_is_confirmed_by_the_person_and_yes_is_not_added_on_their_behalf(self):
        flow = memory_policy()
        self.assertRegex(flow, r"(?i)project name .{0,120}confirm")
        self.assertIn("--name", flow)
        self.assertRegex(flow, r"(?i)never pass `--yes` on the person's behalf")

    def test_exit_codes_and_reasons_of_memory_init_are_handled(self):
        flow = memory_policy()
        self.assertRegex(flow, r"(?i)exit code `0`")
        self.assertRegex(flow, r"(?i)exit code `3`.{0,200}needs_decision")
        self.assertRegex(flow, r"(?i)exit code `1`")
        self.assertIn("name_not_confirmed", flow)
        self.assertRegex(flow, r"(?i)\bconflict")
        self.assertRegex(flow, r"(?i)never force or overwrite")

    def test_missing_binary_is_reported_and_the_phase_stays_pending(self):
        flow = memory_policy()
        self.assertRegex(flow, r"(?i)`active-stack` is not available")
        self.assertRegex(flow, r"(?i)stays `pending`")

    def test_summary_and_explicit_approval_come_before_any_write(self):
        flow = memory_policy()
        self.assertRegex(flow, r"(?i)summary .{0,200}\.engram/config\.json.{0,200}\.gitignore")
        self.assertRegex(flow, r"(?i)explicit approval")
        self.assertRegex(flow, r"(?i)only answers questions is not an approval")

    def test_the_commit_is_only_proposed_never_executed(self):
        flow = memory_policy()
        self.assertIn("proposed_commit", flow)
        self.assertRegex(flow, r"(?i)show the proposed commit")
        self.assertRegex(flow, r"(?i)never run `git add`, `git commit` or `git push`")
        self.assertRegex(flow, r"(?i)the person runs it")

    def test_no_credentials_or_tokens_anywhere(self):
        flow = memory_policy()
        self.assertRegex(flow, r"(?i)no token or credential")
        self.assertNotRegex(flow, r"(?i)ENGRAM_[A-Z_]*TOKEN|bearer|ghp_")


class MemoryPolicyStateTests(unittest.TestCase):
    def test_choice_lives_only_in_the_foundation_state_not_in_roadmap_json(self):
        flow = memory_policy()
        self.assertIn('foundation.phases["memory-policy"]', flow)
        self.assertRegex(flow, r"(?i)do not copy it to `\.active-stack/roadmap\.json`")
        self.assertRegex(flow, r"(?i)DA-07")

    def test_state_record_shape_is_documented(self):
        flow = memory_policy()
        for field in ('"variant"', '"status"', '"outputs"', '"decided_on"'):
            self.assertIn(field, flow)
        self.assertRegex(flow, r"(?i)`pending`")
        self.assertRegex(flow, r"(?i)`done`")

    def test_status_is_done_only_after_memory_init_reports_ok(self):
        flow = memory_policy()
        self.assertRegex(flow, r"(?i)`done` only after .{0,120}exit code `0`")

    def test_state_write_is_backed_up_atomic_and_preserves_other_sections(self):
        flow = memory_policy()
        self.assertRegex(flow, r"(?i)back up the state")
        self.assertRegex(flow, r"(?i)atomic")
        self.assertRegex(flow, r"(?i)preserve all existing and unknown sections")
        self.assertRegex(flow, r"(?i)do not change the schema version or `step`")

    def test_state_and_resume_section_covers_the_missing_record(self):
        resume = flat(section("State and resume"))
        self.assertRegex(resume, r"(?i)missing `memory-policy` record means .{0,60}not been decided")
        self.assertRegex(resume, r"(?i)standalone `:memory`")

    def test_resume_reuses_the_recorded_choice_like_visual_design(self):
        flow = memory_policy()
        self.assertRegex(flow, r"(?i)like `visual_design`")
        self.assertRegex(flow, r"(?i)`done`.{0,200}do not ask again")
        self.assertRegex(flow, r"(?i)`pending`.{0,200}run `active-stack memory init` again")
        self.assertRegex(flow, r"(?i)idempotent")

    def test_deferred_is_never_asked_again(self):
        flow = memory_policy()
        self.assertRegex(flow, r"(?i)`deferred`.{0,200}never asks again")
        self.assertRegex(flow, r"(?i)only an explicit `:memory`")
        self.assertRegex(flow, r"(?i)unlike `visual_design`")

    def test_a_completed_foundation_is_not_replayed_to_add_the_policy(self):
        flow = memory_policy()
        self.assertRegex(flow, r"(?i)never rewind or replay")
        self.assertRegex(flow, r"(?i)`step: done`")

    def test_older_state_versions_keep_working(self):
        self.assertRegex(memory_policy(), r"(?i)versions 2 to 5")


class MemoryPolicyClientsTests(unittest.TestCase):
    def test_phase_is_not_hidden_in_any_client_but_says_where_the_marker_acts(self):
        flow = memory_policy()
        self.assertRegex(flow, r"(?i)Codex, Claude, OpenCode and Antigravity")
        self.assertRegex(flow, r"(?i)`engram-cloud` harness.{0,160}Claude and Codex")
        self.assertRegex(flow, r"(?i)OpenCode and Antigravity.{0,160}no effect")

    def test_phase_needs_only_a_shell_command_and_no_client_specific_tool(self):
        self.assertRegex(memory_policy(), r"(?i)no client-specific tool")

    def test_phase_does_not_copy_the_engram_cloud_section(self):
        flow = memory_policy()
        self.assertRegex(flow, r"(?i)never copy the `active-stack:engram-cloud` section")
        self.assertNotIn("Cloud Team Memory", SKILL)


if __name__ == "__main__":
    unittest.main()
