"""The foundation checklist explains each phase and makes choosing easy."""

from pathlib import Path
import re
import unittest


SKILL = (Path(__file__).resolve().parents[1] / "SKILL.md").read_text(encoding="utf-8")


def section(heading):
    match = re.search(rf"(?ms)^## {heading}\n(.*?)(?=^## |\Z)", SKILL)
    return match.group(1) if match else ""


def rows(heading):
    """Table rows of a section keyed by phase ID, in order."""
    found = re.findall(r"(?m)^\| `([a-z-]+)` \|(.*)\|$", section(heading))
    return [(phase, [cell.strip() for cell in rest.split("|")]) for phase, rest in found]


def flat(text):
    return " ".join(text.split())


class ChecklistSelectionContract(unittest.TestCase):
    def test_every_catalog_phase_has_a_benefit_and_a_cost_of_skipping(self):
        catalog = [phase for phase, _ in rows("Phase catalog")]
        benefits = rows("Phase benefits")
        self.assertTrue(catalog)
        self.assertEqual([phase for phase, _ in benefits], catalog)
        for phase, cells in benefits:
            self.assertEqual(len(cells), 2, phase)
            self.assertTrue(all(cells), phase)

    def test_required_phases_cannot_be_presented_as_skippable(self):
        required = {p for p, cells in rows("Phase catalog") if cells[0] == "Required"}
        for phase, cells in rows("Phase benefits"):
            self.assertEqual(cells[1] == "Required.", phase in required, phase)

    def test_whole_catalog_is_shown_before_asking(self):
        checklist = flat(section("Checklist and approval"))
        self.assertIn("Show every catalog phase", checklist)
        self.assertIn("benefit", checklist)
        self.assertIn("cost of skipping", checklist)
        self.assertLess(checklist.index("Show every catalog phase"), checklist.index("Let the user choose"))

    def test_checklist_stays_readable_in_a_terminal(self):
        self.assertIn("at most four columns", flat(section("Checklist and approval")))

    def test_choice_cannot_collapse_into_an_approval_question(self):
        checklist = flat(section("Checklist and approval"))
        self.assertIn("Never replace this choice with an approve, adjust or stop question", checklist)

    def test_native_selector_covers_every_optional_phase(self):
        selector = flat(section("Choosing phases"))
        optional = [p for p, cells in rows("Phase catalog") if cells[0] == "Optional"]
        native = selector.split("### Numbered list", 1)[0]
        for phase in optional:
            self.assertIn(f"`{phase}`", native)
        self.assertIn("at most four questions with two to four options", native)
        self.assertIn("ClickUp", native)

    def test_numbered_list_is_the_fallback_with_a_short_reply(self):
        fallback = flat(section("Choosing phases").split("### Numbered list", 1)[1])
        self.assertIn("numbered text list", fallback)
        self.assertIn("`ok`", fallback)
        self.assertIn("`+6 -8`", fallback)
        self.assertIn("is a selection, not an approval", fallback)

    def test_no_experimental_client_feature_is_enabled(self):
        selector = flat(section("Choosing phases"))
        self.assertIn("Never enable an experimental client feature", selector)


if __name__ == "__main__":
    unittest.main()
