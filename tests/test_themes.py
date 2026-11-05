"""Theme registry consistency tests (no Windows-only deps)."""
from __future__ import annotations

import unittest

from themes import THEMES, THEME_ORDER, theme_choices


class ThemeTests(unittest.TestCase):
    def test_order_ids_all_exist(self) -> None:
        for tid in THEME_ORDER:
            self.assertIn(tid, THEMES)

    def test_order_has_no_duplicates(self) -> None:
        self.assertEqual(len(THEME_ORDER), len(set(THEME_ORDER)))

    def test_every_theme_has_name_desc_and_full_style(self) -> None:
        ref_keys = set(THEMES["midnight"]["style"])
        for tid, theme in THEMES.items():
            self.assertTrue(theme["name"], tid)
            self.assertTrue(theme["desc"], tid)
            self.assertEqual(set(theme["style"]), ref_keys, tid)

    def test_choices_follow_order(self) -> None:
        self.assertEqual([c[0] for c in theme_choices()], THEME_ORDER)


if __name__ == "__main__":
    unittest.main()
