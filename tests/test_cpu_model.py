"""CPU model cleanup tests (no Windows-only deps).

clean_cpu_model / get_cpu_model live in metrics.py; the hardware card
draws Sample.cpu_model at the bottom, blank when unknown.
"""
from __future__ import annotations

import unittest

from metrics import Sample, clean_cpu_model, get_cpu_model


class CleanCpuModelTests(unittest.TestCase):
    def test_intel_registry_string_shortened(self) -> None:
        self.assertEqual(
            clean_cpu_model("Intel(R) Core(TM) i7-12700H CPU @ 2.30GHz"),
            "Intel Core i7-12700H",
        )

    def test_amd_string_without_frequency_kept(self) -> None:
        # 无主频后缀时保留原串，只受 34 字符上限截断。
        self.assertEqual(
            clean_cpu_model("AMD Ryzen 7 5800H with Radeon Graphics"),
            "AMD Ryzen 7 5800H with Radeon Grap",
        )

    def test_family_string_is_unusable(self) -> None:
        self.assertEqual(
            clean_cpu_model("Intel64 Family 6 Model 158 Stepping 10, GenuineIntel"),
            "",
        )

    def test_empty_and_blank(self) -> None:
        self.assertEqual(clean_cpu_model(""), "")
        self.assertEqual(clean_cpu_model("   "), "")

    def test_long_model_truncated_to_card_width(self) -> None:
        cleaned = clean_cpu_model(
            "AMD Ryzen 9 7945HX with Radeon Graphics and Extra Words Here"
        )
        self.assertLessEqual(len(cleaned), 34)
        self.assertTrue(cleaned.startswith("AMD Ryzen 9 7945HX with Radeon"))

    def test_get_cpu_model_returns_string(self) -> None:
        self.assertIsInstance(get_cpu_model(), str)

    def test_sample_carries_cpu_model(self) -> None:
        s = Sample(ts=0.0, cpu=0.0, mem=0.0, mem_used_gb=0.0,
                   mem_total_gb=0.0, gpu=None, cpu_temp=None,
                   gpu_temp=None, net_up_bps=0.0, net_down_bps=0.0)
        self.assertEqual(s.cpu_model, "")
        s2 = Sample(ts=0.0, cpu=0.0, mem=0.0, mem_used_gb=0.0,
                    mem_total_gb=0.0, gpu=None, cpu_temp=None,
                    gpu_temp=None, net_up_bps=0.0, net_down_bps=0.0,
                    cpu_model="Intel Core i7-12700H")
        self.assertEqual(s2.cpu_model, "Intel Core i7-12700H")


if __name__ == "__main__":
    unittest.main()
