from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from amr import AMROrchestrator, TaskPackage
from amr.memory import LocalVectorMemory


class TestLocalVectorMemory(unittest.TestCase):
    def test_add_and_search(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            db = Path(td) / "mem.json"
            mem = LocalVectorMemory(str(db))
            mem.add("note", "erro NameError em acumulador", {"case": 1})
            mem.add("note", "solução com variável correta", {"case": 2})
            result = mem.search("NameError acumulador", top_k=1)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["kind"], "note")


class TestOrchestrator(unittest.TestCase):
    def test_self_correction_loop(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            memory_path = str(Path(td) / "memory_store.json")
            orchestrator = AMROrchestrator(memory_path=memory_path)
            task = TaskPackage(
                task_id="t1",
                objective="Somar pares",
                acceptance_tests=[
                    "assert sum_even_numbers([1,2,3,4,5,6]) == 12",
                    "print('ok')",
                ],
            )
            outcome = orchestrator.run(task, max_iters=3)
            self.assertEqual(outcome["status"], "success")
            self.assertGreaterEqual(outcome["iterations"], 2)

            persisted = json.loads(Path(memory_path).read_text(encoding="utf-8"))
            kinds = {entry["kind"] for entry in persisted}
            self.assertIn("failure_pattern", kinds)
            self.assertIn("resolved_pattern", kinds)


if __name__ == "__main__":
    unittest.main()
