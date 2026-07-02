"""
Builds teams_payload.json — a full Adaptive Card JSON posted to the Power
Automate "when a webhook request is received" trigger. This flow's action is
"Post card in a chat or channel", which expects the raw request body to BE a
valid Adaptive Card object (top-level "type": "AdaptiveCard").

Usage: python build_teams_payload.py <content.json> <pdf_public_url> <output_payload.json>
"""
import json
import sys


def _text_block(text, size=None, weight=None, color=None, wrap=True, spacing=None):
    block = {"type": "TextBlock", "text": text, "wrap": wrap}
    if size:
        block["size"] = size
    if weight:
        block["weight"] = weight
    if color:
        block["color"] = color
    if spacing:
        block["spacing"] = spacing
    return block


def build(content_path, pdf_url, output_path):
    with open(content_path) as f:
        data = json.load(f)

    body = [
        _text_block(f"Crypto News Bot — Daily Digest", size="Large", weight="Bolder"),
        _text_block(data["date"], size="Small", color="Dark"),
    ]

    if data.get("market_note"):
        body.append(_text_block(data["market_note"], size="Small", spacing="Medium"))

    body.append(_text_block("Stablecoin News", size="Medium", weight="Bolder", color="Good", spacing="Medium"))
    for item in data.get("stablecoin_items", []):
        body.append(_text_block(item["headline"], weight="Bolder", wrap=True))
        body.append(_text_block(item["summary"], size="Small", wrap=True))

    body.append(_text_block("Hacking & Security Incidents", size="Medium", weight="Bolder", color="Attention", spacing="Medium"))
    for item in data.get("hack_items", []):
        body.append(_text_block(item["headline"], weight="Bolder", wrap=True))
        body.append(_text_block(item["summary"], size="Small", wrap=True))

    card = {
        "type": "AdaptiveCard",
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "version": "1.4",
        "body": body,
        "actions": [
            {"type": "Action.OpenUrl", "title": "Open full one-page PDF", "url": pdf_url}
        ],
    }

    with open(output_path, "w") as f:
        json.dump(card, f, indent=2)


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2], sys.argv[3])
