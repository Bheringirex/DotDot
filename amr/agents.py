from __future__ import annotations

import textwrap
from dataclasses import dataclass
from typing import List, Protocol

from .models import AuditResult, ErrorReport, TaskPackage
from .sandbox import run_python


class CodeGenerator(Protocol):
    def generate(self, prompt: str) -> str:
        ...


@dataclass
class RuleBasedGenerator:
    """Gerador mínimo para demo offline.

    Em produção, troque por adaptador para Groq/HF/Ollama.
    """

    def generate(self, prompt: str) -> str:
        if "NameError" in prompt:
            return textwrap.dedent(
                """
                def sum_even_numbers(nums):
                    total = 0
                    for n in nums:
                        if n % 2 == 0:
                            total += n
                    return total
                """
            ).strip()

        return textwrap.dedent(
            """
            def sum_even_numbers(nums):
                total = 0
                for n in nums:
                    if n % 2 == 0:
                        total += num
                return total
            """
        ).strip()


@dataclass
class Executor:
    generator: CodeGenerator

    def solve(self, task: TaskPackage, critic_feedback: str = "") -> str:
        prompt = (
            f"Tarefa: {task.objective}\n"
            f"Restrições: {task.constraints}\n"
            f"Feedback do Crítico: {critic_feedback}\n"
            "Produza apenas código Python."
        )
        return self.generator.generate(prompt)


class Critic:
    def audit(self, candidate_code: str, tests: List[str]) -> AuditResult:
        bundle = candidate_code + "\n\n" + "\n".join(tests)
        result = run_python(bundle)
        if result.returncode == 0:
            return AuditResult(ok=True, feedback="Todos os testes passaram.", stdout=result.stdout, stderr=result.stderr)

        feedback = self._summarize_error(result.stderr)
        return AuditResult(ok=False, feedback=feedback, error=result.stderr, stdout=result.stdout, stderr=result.stderr)

    @staticmethod
    def _summarize_error(stderr: str) -> str:
        last_line = (stderr.strip().splitlines() or ["erro desconhecido"])[-1]
        if "NameError" in stderr:
            return "NameError detectado. Revise nomes de variáveis usados em loops/acumuladores."
        return f"Falha: {last_line}"


class Archivist:
    def __init__(self, memory) -> None:
        self.memory = memory

    def remember(self, kind: str, content: str, metadata: dict) -> None:
        self.memory.add(kind, content, metadata)

    def recall(self, query: str, top_k: int = 3):
        return self.memory.search(query, top_k=top_k)


def build_error_report(task: TaskPackage, audit: AuditResult, fix_applied: str) -> ErrorReport:
    root = "Falha semântica/lógica identificada durante execução no sandbox."
    if "NameError" in audit.error:
        root = "Variável inexistente referenciada durante soma condicional."

    return ErrorReport(
        error_observed=(audit.error.strip().splitlines() or ["sem detalhe"])[-1],
        root_cause=root,
        fix_applied=fix_applied,
        prevention=(
            "Executar testes mínimos reprodutíveis + revisão de nomes de variáveis antes de aceitar resposta."
        ),
        task_context=task.objective,
    )
