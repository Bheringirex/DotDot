from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List

from .models import MemoryRecord


class LocalVectorMemory:
    """Memória vetorial simples com persistência JSON.

    - Não depende de bibliotecas externas.
    - Usa embedding por hashing (bag-of-words normalizado).
    """

    def __init__(self, db_path: str = "memory_store.json", dims: int = 128) -> None:
        self.db_file = Path(db_path)
        self.dims = dims
        self.records: List[MemoryRecord] = []
        self._load()

    def _load(self) -> None:
        if self.db_file.exists():
            self.records = json.loads(self.db_file.read_text(encoding="utf-8"))

    def _save(self) -> None:
        self.db_file.write_text(json.dumps(self.records, ensure_ascii=False, indent=2), encoding="utf-8")

    def _embed(self, text: str) -> List[float]:
        vec = [0.0] * self.dims
        for token in text.lower().split():
            idx = int(hashlib.sha256(token.encode("utf-8")).hexdigest()[:8], 16) % self.dims
            vec[idx] += 1.0
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]

    @staticmethod
    def _cosine(a: Iterable[float], b: Iterable[float]) -> float:
        a_list = list(a)
        b_list = list(b)
        den = (math.sqrt(sum(x * x for x in a_list)) * math.sqrt(sum(y * y for y in b_list))) or 1.0
        return sum(x * y for x, y in zip(a_list, b_list)) / den

    def add(self, kind: str, content: str, metadata: Dict[str, object]) -> None:
        record: MemoryRecord = {
            "kind": kind,
            "content": content,
            "metadata": {**metadata, "created_at": datetime.now(timezone.utc).isoformat()},
            "embedding": self._embed(content),
        }
        self.records.append(record)
        self._save()

    def search(self, query: str, top_k: int = 3) -> List[MemoryRecord]:
        if not self.records:
            return []
        q = self._embed(query)
        ranked = sorted(self.records, key=lambda r: self._cosine(q, r["embedding"]), reverse=True)
        return ranked[:top_k]
