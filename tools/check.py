"""Kontrollerar lists.json innan den når apparna (körs av GitHub Actions vid varje push).

    python tools/check.py [lists.json]

Samma regler som appen (Preset.isValid): bara siffror, kända längder, högst 200 miljoner nummer
per spärr, unika id:n. En spärr som inte klarar kontrollen hoppar appen över.
"""
import json
import sys
from pathlib import Path

MAX_NUMBERS = 200_000_000


def main(path):
    errors = []
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        print(f"FEL: lists.json går inte att läsa som JSON: {e}")
        return 1

    if not isinstance(data.get("version"), int):
        errors.append('"version" ska vara ett heltal')
    presets = data.get("presets")
    if not isinstance(presets, list) or not presets:
        errors.append('"presets" ska vara en lista med minst en spärr')
        presets = []

    seen = set()
    for i, p in enumerate(presets):
        where = f'spärr {i + 1} ({p.get("id", "?")})'
        for key in ("id", "name", "countryCode", "series", "lengths", "note"):
            if key not in p:
                errors.append(f'{where}: "{key}" saknas')
        if p.get("id") in seen:
            errors.append(f"{where}: id:t finns redan")
        seen.add(p.get("id"))
        cc = str(p.get("countryCode", ""))
        if not cc.isdigit() or not 1 <= len(cc) <= 3:
            errors.append(f'{where}: "countryCode" ska vara 1–3 siffror utan +, t.ex. "45"')
        series = p.get("series", [])
        if not series or not all(isinstance(s, str) and s.isdigit() and len(s) <= 12 for s in series):
            errors.append(f'{where}: "series" ska vara siffror inom citattecken, t.ex. ["20", "21"]')
            series = []
        lengths = p.get("lengths", [])
        if not lengths or not all(isinstance(n, int) and 1 <= n <= 15 for n in lengths):
            errors.append(f'{where}: "lengths" ska vara antal siffror efter landskoden, t.ex. [8]')
            lengths = []
        total = sum(10 ** (n - len(s)) for s in series for n in lengths if n >= len(s))
        if series and lengths and not 1 <= total <= MAX_NUMBERS:
            errors.append(f"{where}: {total:,} nummer – högst {MAX_NUMBERS:,} per spärr")
        elif series and lengths:
            print(f"OK  {p['id']}: {total:,} nummer")

    msg = data.get("message")
    if msg is not None and not (isinstance(msg, dict) and msg.get("id") and msg.get("text")):
        errors.append('"message" ska vara null eller {"id": "...", "text": "...", "url": "..."}')

    for e in errors:
        print("FEL:", e)
    print("lists.json är klar att användas" if not errors else f"{len(errors)} fel")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "lists.json"))
