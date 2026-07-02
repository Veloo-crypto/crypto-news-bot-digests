"""
Builds teams_payload.json — the JSON body posted to the Power Automate
"when a webhook request is received" trigger.

Usage: python build_teams_payload.py <content.json> <pdf_public_url> <output_payload.json>
"""
import json
import sys


def build(content_path, pdf_url, output_path):
    with open(content_path) as f:
        data = json.load(f)

    lines = [f"**Crypto News Bot — Daily Digest — {data['date']}**", ""]
    if data.get("market_note"):
        lines.append(f"_{data['market_note']}_")
        lines.append("")

    lines.append("**Stablecoin News**")
    for item in data.get("stablecoin_items", []):
        lines.append(f"- **{item['headline']}** — {item['summary']}")
    lines.append("")

    lines.append("**Hacking & Security Incidents**")
    for item in data.get("hack_items", []):
        lines.append(f"- **{item['headline']}** — {item['summary']}")
    lines.append("")

    lines.append(f"[Full one-page PDF]({pdf_url})")

    payload = {"text": "\n".join(lines)}

    with open(output_path, "w") as f:
        json.dump(payload, f, indent=2)


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2], sys.argv[3])
