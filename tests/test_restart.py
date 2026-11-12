"""Restart command builder tests (no Windows-only deps).

glass_ui 依赖 Windows 专属模块，Linux 下无法直接 import；
这里用 ast 只抽出纯函数 _restart_command 的源码执行后断言。
"""
from __future__ import annotations

import ast
import unittest
from pathlib import Path


def _load_restart_command():
    src = (Path(__file__).resolve().parent.parent
           / "glass_ui.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "_restart_command":
            ns: dict = {}
            exec(compile(ast.Module(body=[node], type_ignores=[]),
                         "glass_ui.py", "exec"), ns)
            return ns["_restart_command"]
    raise AssertionError("_restart_command not found in glass_ui.py")


class RestartCommandTests(unittest.TestCase):
    def test_restart_command_waits_for_pid_then_relaunches(self) -> None:
        cmd = _load_restart_command()(1234, r"C:\Python314\pythonw.exe",
                                      r"C:\app\monitor.py", r"C:\app")
        self.assertEqual(cmd[0], "powershell")
        joined = " ".join(cmd)
        self.assertIn("1234", joined)
        self.assertIn(r"C:\Python314\pythonw.exe", joined)
        self.assertIn(r"C:\app\monitor.py", joined)
        self.assertIn("Hidden", joined)
        self.assertIn("Get-Process", joined)

    def test_restart_widget_wired_in_tray_menu(self) -> None:
        src = (Path(__file__).resolve().parent.parent
               / "glass_ui.py").read_text(encoding="utf-8")
        self.assertIn('"重启小部件"', src)
        self.assertIn("self._restart_widget", src)
        self.assertIn("def _restart_widget", src)


if __name__ == "__main__":
    unittest.main()
