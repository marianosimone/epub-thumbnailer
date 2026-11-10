"""CLI usage tests for src/epub-thumbnailer.py (run with pytest from the repo root)."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "src" / "epub-thumbnailer.py"


def test_no_args_prints_usage_and_exits_2():
    """Running without arguments must print usage, not an IndexError traceback."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2
    assert "Usage:" in result.stderr
    assert "Traceback" not in result.stderr


def test_non_integer_size_exits_2():
    """A non-integer size must be a clean error, not a ValueError traceback."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "a.epub", "b.png", "big"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 2
    assert "size must be an integer" in result.stderr
    assert "Traceback" not in result.stderr
