from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class TaskPackage:
    task_id: str
    objective: str
    acceptance_tests: List[str]
    language: str = "python"
    constraints: List[str] = field(default_factory=list)


@dataclass
class AuditResult:
    ok: bool
    feedback: str
    error: str = ""
    stdout: str = ""
    stderr: str = ""


@dataclass
class ErrorReport:
    error_observed: str
    root_cause: str
    fix_applied: str
    prevention: str
    task_context: str

    def to_markdown(self) -> str:
        return (
            "[BACK-PROPAGATION DE ERRO]\n"
            f"Erro observado:\n- {self.error_observed}\n\n"
            f"Por que aconteceu (causa raiz):\n- {self.root_cause}\n\n"
            f"Como corrigimos:\n- {self.fix_applied}\n\n"
            f"Como prevenir no futuro:\n- {self.prevention}\n\n"
            f"Contexto da tarefa:\n- {self.task_context}\n"
        )


MemoryRecord = Dict[str, object]
