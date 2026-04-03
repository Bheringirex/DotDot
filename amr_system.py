from __future__ import annotations

import json

from amr import AMROrchestrator, TaskPackage


def main() -> None:
    task = TaskPackage(
        task_id="demo-sum-even",
        objective="Implementar função Python que soma apenas números pares de uma lista.",
        acceptance_tests=[
            "assert sum_even_numbers([1, 2, 3, 4, 5, 6]) == 12",
            "assert sum_even_numbers([]) == 0",
            "assert sum_even_numbers([2, 2, 2]) == 6",
            "print('ok')",
        ],
        constraints=[
            "Não usar bibliotecas externas para cálculo",
            "Retornar inteiro",
        ],
    )

    orchestrator = AMROrchestrator(memory_path="memory_store.json")
    result = orchestrator.run(task)

    print("=== AMR RESULT ===")
    print(json.dumps({"status": result["status"], "iterations": result["iterations"]}, ensure_ascii=False, indent=2))
    print("\n=== ITERATION TRACE ===")
    for step in result["history"]:
        audit = step["audit"]
        print(f"Iter {step['iteration']} | ok={audit['ok']} | feedback={audit['feedback']}")


if __name__ == "__main__":
    main()
