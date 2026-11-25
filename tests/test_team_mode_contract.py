"""Contract tests for the optional team-mode foundation phase ([EQ] Phase 3)."""

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = (ROOT / "SKILL.md").read_text(encoding="utf-8")


def section(heading):
    match = re.search(rf"(?ms)^## {heading}\n(.*?)(?=^## |\Z)", SKILL)
    return match.group(1) if match else ""


def team_mode():
    match = re.search(r"(?ms)^### Team mode\n(.*?)(?=^#{2,3} |\Z)", SKILL)
    # Markdown wraps lines; compare the text as rendered, with single spaces.
    return re.sub(r"\s+", " ", match.group(1)) if match else ""


def team_row():
    return next(
        (line for line in section("Phase catalog").splitlines() if line.startswith("| `team-mode`")),
        "",
    )


class TeamPhaseCatalogTests(unittest.TestCase):
    def test_team_mode_is_an_optional_phase_with_its_outputs_and_variants(self):
        row = team_row()
        self.assertIn("| Optional |", row)
        self.assertIn(".active-stack/team.json", row)
        self.assertIn(".github/CODEOWNERS", row)
        self.assertIn(".github/pull_request_template.md", row)
        self.assertIn("new, reuse, update", row)

    def test_team_mode_never_becomes_a_required_output(self):
        required = re.findall(r"^\| `([a-z-]+)` \| Required \|", section("Phase catalog"), re.MULTILINE)
        self.assertEqual(required, ["kb", "roadmap", "task-management", "agents"])

    def test_team_mode_runs_after_task_management_and_before_the_rules(self):
        catalog = section("Phase catalog")
        order = [name for name in re.findall(r"^\| `([a-z-]+)` \|", catalog, re.MULTILINE)]
        self.assertLess(order.index("task-management"), order.index("team-mode"))
        self.assertLess(order.index("team-mode"), order.index("agents"))
        self.assertRegex(catalog, r"(?is)team mode after task management and before .{0,40}instructions")

    def test_standalone_entrypoint_exists_for_the_phase_and_the_update(self):
        dispatch = section("Dispatch and entrypoints")
        self.assertIn("`:team`", dispatch)
        self.assertIn("/active-orchestrator team", SKILL)


class TeamFoundationFlowTests(unittest.TestCase):
    def test_no_and_later_write_nothing(self):
        flow = team_mode()
        self.assertRegex(flow, r'(?i)"no" or "later".{0,60}nothing is written')
        self.assertRegex(flow, r"(?i)foundation without team mode is unchanged")

    def test_size_is_mandatory_and_names_are_optional_and_never_invented(self):
        flow = team_mode()
        self.assertRegex(flow, r"(?i)size.{0,40}required.{0,40}integer.{0,20}(?:>=|at least) ?2")
        self.assertRegex(flow, r"(?i)names? (?:are )?optional")
        self.assertIn("`Integrante N`", flow)
        self.assertRegex(flow, r"(?i)never invent (?:names|accounts)")

    def test_names_versioning_is_asked_and_public_repos_are_explained_first(self):
        flow = team_mode()
        self.assertIn("Do we version the names in the repository?", flow)
        explain = flow.index("public")
        ask = flow.index("Do we version the names")
        self.assertLess(explain, ask)
        self.assertIn("`names_versioned`", flow)
        self.assertIn(".active-stack/team.local.json", flow)
        self.assertRegex(flow, r"(?i)only `size`")

    def test_local_files_are_ignored_by_git_inside_idempotent_markers(self):
        flow = team_mode()
        self.assertIn(".active-stack/me.local.json", flow)
        self.assertRegex(flow, r"(?i)\.gitignore.{0,80}markers")

    def test_draft_is_validated_before_writing_with_the_shared_contract(self):
        flow = team_mode()
        self.assertIn("team.sh", flow)
        self.assertIn("team.bat", flow)
        self.assertIn("validate --file", flow)
        self.assertLess(flow.index("validate --file"), flow.index("Write the files"))

    def test_clients_without_active_delivery_validate_with_inline_rules_and_warn(self):
        flow = team_mode()
        self.assertRegex(flow, r"(?i)`active-delivery` is (?:not available|unavailable)")
        self.assertRegex(flow, r"(?i)ids are unique")
        self.assertRegex(flow, r"(?i)no automatic validator")

    def test_summary_and_explicit_approval_come_before_any_write(self):
        flow = team_mode()
        self.assertRegex(flow, r"(?i)summary.{0,80}every file.{0,80}external action")
        self.assertLess(flow.index("explicit approval"), flow.index("Write the files"))

    def test_existing_files_are_backed_up_and_never_overwritten(self):
        flow = team_mode()
        self.assertRegex(flow, r"(?i)back up existing files")
        self.assertRegex(flow, r"(?i)never overwrite.{0,80}CODEOWNERS")
        self.assertRegex(flow, r"(?i)pull_request_template\.md")
        self.assertRegex(flow, r"(?i)show the diff and propose the merge")

    def test_codeowners_comes_from_zones_and_reviewers(self):
        flow = team_mode()
        self.assertRegex(flow, r"(?i)`Zona`")
        self.assertRegex(flow, r"(?i)primary and backup reviewer")
        self.assertRegex(flow, r"(?i)members without `github` are left out.{0,60}note")

    def test_clickup_members_are_resolved_confirmed_and_never_guessed(self):
        flow = team_mode()
        self.assertIn("find_member_by_name", flow)
        self.assertIn("resolve_assignees", flow)
        self.assertRegex(flow, r"(?i)confirm .{0,40}with the person")
        self.assertRegex(flow, r"(?i)no match.{0,60}unlinked")
        self.assertRegex(flow, r"(?i)connector is (?:down|unavailable)")
        self.assertIn("preserve the approved tracking mode", flow)

    def test_main_protection_is_offered_once_and_needs_confirmation(self):
        flow = team_mode()
        self.assertRegex(flow, r"(?i)offer (?:it )?once")
        self.assertIn("`gh`", flow)
        self.assertRegex(flow, r"(?i)only .{0,30}after (?:explicit )?confirmation")
        self.assertRegex(flow, r"(?i)without permission or on an unsupported plan.{0,120}convention")
        self.assertRegex(flow, r"(?i)record the choice.{0,60}(?:not|never) ask again")

    def test_rules_section_is_written_by_agent_instruction_not_by_the_orchestrator(self):
        flow = team_mode()
        self.assertIn("`agent-instruction`", flow)
        self.assertIn("active-stack:team-mode", flow)
        self.assertRegex(flow, r"(?i)does not write the project instruction file itself")

    def test_identity_is_not_written_by_foundation(self):
        flow = team_mode()
        self.assertIn("`.active-stack/me.local.json`", flow)
        self.assertRegex(flow, r"(?i)foundation does not choose (?:the person's )?identity")
        self.assertIn("`active-delivery`", flow)

    def test_phase_is_done_only_after_files_are_verified_and_commit_is_only_proposed(self):
        flow = team_mode()
        self.assertIn('`foundation.phases["team-mode"]`', flow)
        self.assertRegex(flow, r"(?i)`done` only after .{0,40}verif")
        self.assertRegex(flow, r"(?i)propose.{0,40}single commit")
        self.assertRegex(flow, r"(?i)never commit")
        self.assertRegex(flow, r"(?i)written together")

    def test_no_credentials_in_any_team_file(self):
        flow = team_mode()
        self.assertRegex(flow, r"(?i)no (?:field|file).{0,60}credentials")


class TeamUpdateTests(unittest.TestCase):
    def test_update_team_changes_the_team_without_regenerating_the_foundation(self):
        flow = team_mode()
        self.assertIn("### Update team", flow)
        update = flow.split("### Update team", 1)[1]
        for action in ("add", "remove", "rename", "size", "tracking"):
            self.assertRegex(update, rf"(?i)\b{action}", action)
        self.assertRegex(update, r"(?i)without regenerating")

    def test_update_previews_the_diff_and_handles_orphan_fichas(self):
        update = team_mode().split("### Update team", 1)[1]
        self.assertRegex(update, r"(?i)diff.{0,80}`team\.json`")
        self.assertIn("`CODEOWNERS`", update)
        self.assertRegex(update, r"(?i)orphan")
        self.assertRegex(update, r"(?i)nothing is reassigned without approval")
        self.assertRegex(update, r"(?i)fichas already started are not touched")

    def test_update_is_idempotent_and_versioned(self):
        update = team_mode().split("### Update team", 1)[1]
        self.assertRegex(update, r"(?i)idempotent")
        self.assertRegex(update, r"(?i)same input.{0,40}same bytes")
        self.assertIn("`version`", update)

    def test_update_reports_what_is_still_pending(self):
        update = team_mode().split("### Update team", 1)[1]
        for pending in ("names", "ClickUp", "`main`"):
            self.assertIn(pending, update)


class TeamClientCompatibilityTests(unittest.TestCase):
    def test_phase_is_not_hidden_in_opencode_and_antigravity(self):
        flow = team_mode()
        self.assertIn("OpenCode", flow)
        self.assertIn("Antigravity", flow)
        self.assertRegex(flow, r"(?i)does not hide the phase")
        self.assertRegex(flow, r"(?i)guided delivery flow (?:does not exist|is not available)")

    def test_phase_does_not_require_claude_or_codex_only_tools(self):
        flow = team_mode()
        self.assertRegex(flow, r"(?i)no .{0,30}Claude.{0,30}Codex.{0,30}(?:tool|capabilit)")
        self.assertIn("Use the tracking tool chosen in task management", flow)


class TeamTemplatesTests(unittest.TestCase):
    def test_pull_request_template_asset_carries_the_six_handoff_facts(self):
        template = (ROOT / "assets/pull_request_template.md").read_text(encoding="utf-8")
        for fact in ("Result", "PR and SHA", "How to verify", "What is left", "Who continues", "What blocks it"):
            self.assertRegex(template, rf"(?im)^#+ .*{fact}")
        self.assertRegex(template, r"(?i)ficha")
        self.assertNotRegex(template, r"(?i)token|secret|password|bearer|ghp_")

    def test_codeowners_example_shows_the_format_without_real_people(self):
        example = (ROOT / "assets/CODEOWNERS.example").read_text(encoding="utf-8")
        self.assertRegex(example, r"(?m)^#.*Zona")
        self.assertRegex(example, r"(?m)^\S+/\s+@\S+\s+@\S+")
        self.assertRegex(example, r"@(?:github-handle|primary|backup)")

    def test_skill_points_to_both_assets_and_never_invents_their_content(self):
        flow = team_mode()
        self.assertIn("assets/pull_request_template.md", flow)
        self.assertIn("assets/CODEOWNERS.example", flow)
        self.assertRegex(flow, r"(?i)copy the template as it is")


class TeamIdentityAtFoundationTests(unittest.TestCase):
    def test_founder_can_choose_a_seat_with_account_match_manual_choice_or_consult(self):
        flow = team_mode()
        self.assertIn("gh api user", flow)
        self.assertRegex(flow, r"(?i)suggest .{0,60}matches? .{0,40}`github`")
        self.assertRegex(flow, r"(?i)manual choice|choose from the list")
        self.assertRegex(flow, r"(?i)consult mode")
        self.assertRegex(flow, r"(?i)read-only")

    def test_identity_is_confirmed_and_only_written_locally(self):
        flow = team_mode()
        self.assertRegex(flow, r"(?i)write `\.active-stack/me\.local\.json` only after the person confirms")
        self.assertRegex(flow, r"(?i)never versioned")
        self.assertRegex(flow, r"(?i)the person can skip")

    def test_fresh_clone_with_existing_team_json_reuses_it_and_fills_local_gaps(self):
        flow = team_mode()
        self.assertRegex(flow, r"(?i)fresh clone")
        self.assertRegex(flow, r"(?i)`team\.json` already exists")
        self.assertRegex(flow, r"(?i)never rewrite (?:an existing )?`team\.json`")
        self.assertRegex(flow, r"(?i)missing local files")

    def test_partial_foundation_resumes_from_evidence(self):
        flow = team_mode()
        self.assertRegex(flow, r"(?i)partial foundation")
        self.assertRegex(flow, r"(?i)inspect the files first")


if __name__ == "__main__":
    unittest.main()
