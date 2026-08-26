from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
PAGES = (ROOT / "index.html", ROOT / "en" / "index.html")


def mobile_rules(source: str) -> str:
    match = re.search(
        r"@media \(max-width: 740px\) \{(?P<rules>.*?)\n    \}",
        source,
        re.DOTALL,
    )
    if not match:
        raise AssertionError("De mobiele mediaquery ontbreekt")
    return match.group("rules")


class MobileRouteTagLayoutTests(unittest.TestCase):
    def test_route_tags_flow_below_text_on_mobile(self) -> None:
        for page in PAGES:
            with self.subTest(page=page):
                rules = mobile_rules(page.read_text(encoding="utf-8"))
                panel_rule = re.search(r"\.route-panel \{(?P<declarations>[^}]*)\}", rules)
                tag_rule = re.search(r"\.route-tag \{(?P<declarations>[^}]*)\}", rules)
                if panel_rule is None or tag_rule is None:
                    self.fail("De mobiele routepaneel- of labelregel ontbreekt")
                panel_declarations = panel_rule.group("declarations")
                tag_declarations = tag_rule.group("declarations")

                for declaration in ("display: flex;", "flex-direction: column;", "min-height: 0;"):
                    self.assertIn(declaration, panel_declarations)
                for declaration in (
                    "position: static;",
                    "bottom: auto;",
                    "left: auto;",
                    "align-self: flex-start;",
                    "margin-top: 24px;",
                ):
                    self.assertIn(declaration, tag_declarations)


if __name__ == "__main__":
    unittest.main()
