from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ilm_wiki.agents import OrchestratorAgent


class PipelineSmokeTest(unittest.TestCase):
    def test_empty_pipeline_creates_required_reports(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            pdf_dir = root / "pdfs"
            manual_dir = root / "manual"
            output_dir = root / "output"
            pdf_dir.mkdir()
            manual_dir.mkdir()

            result = OrchestratorAgent(pdf_dir, manual_dir, output_dir).run()

            self.assertEqual(result.qa_report["status"], "human_review_required")
            self.assertEqual(result.qa_report["records_total"], 0)
            self.assertTrue((output_dir / "microgravity_solidification_wiki.md").exists())
            self.assertTrue((output_dir / "1g_vs_microgravity_benchmark_table.md").exists())
            self.assertTrue((output_dir / "variable_groups_consolidated.md").exists())
            self.assertTrue((output_dir / "gap_matrix.md").exists())


if __name__ == "__main__":
    unittest.main()

