from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from .agents import Archivist, Critic, Executor, RuleBasedGenerator, build_error_report
from .memory import LocalVectorMemory
from .models import AuditResult, TaskPackage
from .web import heuristic_search, should_search_web


@dataclass
class AMROrchestrator:
    memory_path: str = "memory_store.json"

    def __post_init__(self) -> None:
        memory = LocalVectorMemory(self.memory_path)
        self.executor = Executor(generator=RuleBasedGenerator())
        self.critic = Critic()
        self.archivist = Archivist(memory=memory)

    def run(self, task: TaskPackage, max_iters: int = 4) -> Dict[str, object]:
        recalled = self.archivist.recall(task.objective)
        if should_search_web(recalled, task.objective):
            web_notes = heuristic_search(task.objective)
            self.archivist.remember(
                "web_context",
                web_notes,
                {"task_id": task.task_id, "objective": task.objective},
            )

        history: List[Dict[str, object]] = []
        critic_feedback = ""

        for i in range(1, max_iters + 1):
            code = self.executor.solve(task, critic_feedback)
            audit = self.critic.audit(code, task.acceptance_tests)
            history.append({"iteration": i, "code": code, "audit": audit.__dict__})

            if audit.ok:
                if i > 1:
                    prev = history[-2]["audit"]
                    previous_audit = AuditResult(**prev)
                    report = build_error_report(
                        task,
                        audit=previous_audit,
                        fix_applied="Corrigido acumulador com variável correta (`n`).",
                    )
                    self.archivist.remember(
                        "resolved_pattern",
                        report.to_markdown(),
                        {"task_id": task.task_id, "iteration": i},
                    )
                return {"status": "success", "iterations": i, "history": history}

            self.archivist.remember(
                "failure_pattern",
                audit.error,
                {"task_id": task.task_id, "iteration": i},
            )
            critic_feedback = audit.feedback

        return {"status": "failed", "iterations": max_iters, "history": history}
