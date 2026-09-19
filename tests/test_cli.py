import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "batterynag-audit"
FIXTURE = ROOT / "tests" / "fixtures" / "flapping.txt"


class BatteryNagAuditTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            ["python3", str(CLI), *args], capture_output=True, text=True, check=False
        )

    def test_flapping_source_is_detected(self):
        result = self.run_cli("--fixture", str(FIXTURE))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Transitions: 1", result.stdout)
        self.assertIn("inspect the cable", result.stdout)

    def test_json_is_privacy_bounded(self):
        result = self.run_cli("--fixture", str(FIXTURE), "--json")
        payload = json.loads(result.stdout)
        self.assertTrue(payload["read_only"])
        self.assertEqual(payload["assessment"]["source_transitions"], 1)
        self.assertNotIn("1234567", result.stdout)

    def test_rejects_unbounded_samples(self):
        result = self.run_cli("--samples", "61")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("between 1 and 60", result.stderr)

    def test_version(self):
        result = self.run_cli("--version")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "BatteryNag Audit 0.1.0")


if __name__ == "__main__":
    unittest.main()
