from __future__ import annotations

import html
import re
from typing import List


def _strip_tags(raw_html: str) -> str:
    text = re.sub(r"<script.*?</script>", "", raw_html, flags=re.S | re.I)
    text = re.sub(r"<style.*?</style>", "", text, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return html.unescape(text)


def heuristic_search(query: str, max_chars: int = 800) -> str:
    """Busca heurística web sem API key obrigatória."""
    try:
        import requests

        resp = requests.post("https://duckduckgo.com/html/", data={"q": query}, timeout=10)
        resp.raise_for_status()
        clean = _strip_tags(resp.text)
        return f"[web_search=true] {clean[:max_chars]}"
    except Exception as exc:
        return f"[web_search=false] {exc}"


def should_search_web(recalled: List[dict], objective: str) -> bool:
    if not recalled:
        return True
    short = objective.lower()
    return all(short not in str(item.get("content", "")).lower() for item in recalled)
