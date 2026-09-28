"""Build a tiny document through the API with the installed PreTeXt CLI.

Run from the repo root: python scripts/smoke_test.py
Exits non-zero if the standalone HTML or zipped builds fail.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ["BUILD_TOKEN"] = "smoke-test"

from app import app  # noqa: E402

client = app.test_client()
source = "<p>Smoke test: <m>x^2</m>.</p>"

html = client.post("/", data={"token": "smoke-test", "source": source, "title": "Smoke"})
if html.status_code != 200 or "Smoke test" not in html.get_data(as_text=True):
    print(f"HTML build failed ({html.status_code}):\n{html.get_data(as_text=True)[:4000]}")
    sys.exit(1)

zipped = client.post("/", data={"token": "smoke-test", "source": source, "title": "Smoke", "format": "zip"})
if zipped.status_code != 200 or not zipped.data.startswith(b"PK"):
    print(f"Zipped build failed ({zipped.status_code}):\n{zipped.get_data(as_text=True)[:4000]}")
    sys.exit(1)

print("Smoke test passed.")
