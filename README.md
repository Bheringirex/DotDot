# DotDot — Projeto AMR (Arquitetura Modular Recursiva)

Implementação funcional de uma IA modular com auto-correção recursiva:

- **Executor (The Doer)**: gera solução/código.
- **Crítico (The Auditor)**: testa em sandbox e aponta falhas.
- **Arquivista (The Learner)**: persiste padrões de erro e solução em memória vetorial local.

## Estrutura

- `amr/`
  - `agents.py`: implementação dos três agentes e relatório de erro.
  - `orchestrator.py`: loop recursivo de execução/auditoria/aprendizado.
  - `memory.py`: memória vetorial local persistente (`memory_store.json`).
  - `web.py`: busca heurística web (DuckDuckGo) com fallback.
  - `sandbox.py`: execução segura de código Python em subprocess.
  - `models.py`: contratos de dados (`TaskPackage`, `AuditResult`, `ErrorReport`).
- `amr_system.py`: ponto de entrada para demo ponta-a-ponta.
- `tests/test_amr.py`: testes unitários do loop e da memória.
- `amr_blueprint.md`: prompt/guia de implementação arquitetural.

## Como executar

```bash
python amr_system.py
```

Saída esperada: primeira iteração falha (erro proposital), segunda iteração corrige automaticamente.

## Como testar

```bash
python -m unittest discover -s tests -v
```

## Back-Propagation de Erros (linguagem natural)

Ao corrigir uma falha, o sistema salva um relatório textual com:

1. Erro observado.
2. Causa raiz.
3. Correção aplicada.
4. Medidas preventivas.

Isso permite recuperação semântica futura para evitar reincidência.
