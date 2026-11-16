"""Windows version name tests (no Windows-only deps).

windows_release_name / get_windows_version live in metrics.py; the
system card draws the version as its last row, blank when unknown.
"""
from __future__ import annotations

import unittest

from metrics import get_windows_version, windows_release_name


class WindowsReleaseNameTests(unittest.TestCase):
    def test_windows_11_known_builds(self) -> None:
        self.assertEqual(windows_release_name(26100), "Windows 11 24H2")
        self.assertEqual(windows_release_name(22631), "Windows 11 23H2")
        self.assertEqual(windows_release_name(22621), "Windows 11 22H2")

    def test_windows_10_known_builds(self) -> None:
        self.assertEqual(windows_release_name(19045), "Windows 10 22H2")
        self.assertEqual(windows_release_name(19044), "Windows 10 21H2")
        self.assertEqual(windows_release_name(19041), "Windows 10 2004")

    def test_unknown_build_falls_back_to_build_number(self) -> None:
        self.assertEqual(windows_release_name(26000), "Windows 11 (26000)")
        self.assertEqual(windows_release_name(18363), "Windows 10 (18363)")

    def test_invalid_build_is_empty(self) -> None:
        self.assertEqual(windows_release_name(0), "")
        self.assertEqual(windows_release_name(-1), "")

    def test_get_windows_version_is_empty_off_windows(self) -> None:
        # Linux 上跑测试：非 Windows 返回空串，系统卡不画版本行。
        self.assertEqual(get_windows_version(), "")


if __name__ == "__main__":
    unittest.main()
