from __future__ import annotations

import subprocess
import sys
from dataclasses import dataclass


@dataclass
class SandboxRun:
    returncode: int
    stdout: str
    stderr: str


def run_python(code: str, timeout_seconds: int = 5) -> SandboxRun:
    proc = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
    )
    return SandboxRun(returncode=proc.returncode, stdout=proc.stdout, stderr=proc.stderr)
