# Prompt de Implementação — IA de Arquitetura Modular Recursiva (AMR)

Use o prompt abaixo como guia para construir/estender o sistema:

---

Você é um **Engenheiro de Machine Learning Sênior e Arquiteto de Sistemas Cognitivos**.
Projete e implemente uma IA de **Arquitetura Modular Recursiva (AMR)** com os seguintes requisitos:

## 1) Particionamento Cognitivo
Crie três agentes independentes:

1. **Executor (The Doer)**
   - Recebe uma tarefa técnica.
   - Gera plano de implementação.
   - Produz artefatos (código, explicações e hipóteses de correção).

2. **Crítico (The Auditor)**
   - Valida a solução do Executor.
   - Busca falhas lógicas, edge cases e bugs.
   - Executa testes automatizados em sandbox (Python REPL/subprocess).

3. **Arquivista (The Learner)**
   - Persiste conhecimento em memória vetorial (ex.: Chroma + embeddings gratuitos).
   - Indexa: contexto do erro, stack trace, correção aplicada, motivo da correção.
   - Fornece recuperação semântica para evitar repetição de falhas.

## 2) Loop de Auto-Correção
Implemente o ciclo:

- Executor gera solução inicial.
- Crítico executa validações e testes.
- Se falhar, o Crítico cria um "pacote de erro" contendo:
  - descrição da falha,
  - stack trace,
  - hipótese do motivo raiz,
  - sugestão de teste mínimo reprodutível.
- O pacote de erro retorna ao Executor para debug no sandbox.
- Repita até passar nos critérios de aceitação ou atingir limite de iterações.

## 3) Back-Propagation de Erros (linguagem natural)
Após cada falha, gere uma explicação em linguagem natural no formato:

- **Erro observado**
- **Por que aconteceu (causa raiz)**
- **Como corrigimos**
- **Como prevenir no futuro**

Esse relatório deve ser salvo pelo Arquivista com metadados de versão.

## 4) Pesquisa Heurística na Web
Integre busca externa quando a confiança do modelo for baixa:

- Ferramentas sugeridas: DuckDuckGo Search API, Serper, Tavily ou equivalente OSS.
- Estratégia:
  - tentar memória interna primeiro,
  - se insuficiente, acionar web search,
  - filtrar por fontes técnicas relevantes,
  - resumir evidências e anexar ao contexto.

## 5) Aprendizado Autônomo por Primeiros Princípios
Se não houver solução confiável na memória/web:

- Gerar hipóteses alternativas.
- Testar cada hipótese no sandbox.
- Medir resultado por testes e critérios objetivos.
- Selecionar melhor correção e armazenar novo padrão de conhecimento.

## 6) Infraestrutura Grátis
Utilize stack open source e gratuita:

- Orquestração: loops estilo AutoGPT + LangChain (ou implementação leve própria).
- UI opcional: Streamlit.
- LLM: Groq API (modelos gratuitos disponíveis), Hugging Face Inference, ou Ollama local.
- Vetor DB: ChromaDB local persistente.

## 7) Entregáveis
Produza:

1. Script Python inicializável com os três agentes.
2. Mecanismo de auto-correção com sandbox Python.
3. Módulo de busca web pluggable.
4. Persistência vetorial de erros/soluções.
5. Relatório final explicando fluxo de decisão e back-propagation de erros.

## 8) Critérios de Aceitação
- O sistema deve demonstrar ao menos uma iteração de correção automática.
- Deve registrar em memória vetorial um erro e sua solução.
- Deve exibir claramente quando consultou web search.
- Deve retornar explicação de causa raiz em linguagem natural.

---

## Arquitetura Lógica (explicação resumida)

A IA funciona como uma organização com departamentos especializados:

- O **Executor** age como time de construção.
- O **Crítico** atua como QA + auditoria técnica, rejeitando respostas fracas.
- O **Arquivista** funciona como memória de longo prazo semântica.

Esse arranjo cria **self-reflection operacional**: a IA não para na primeira resposta, testa, detecta falha, corrige e aprende com a própria falha.

Quando surge incerteza, ela usa a internet como "cérebro externo" para preencher lacunas. Sem solução externa confiável, entra em modo de primeiros princípios, experimentando hipóteses no sandbox até convergir.
