"""Extension: this handler was written for the OLD article.published webhook (payload v1).
It breaks on payload v2. Your job: fix get_article_id() so it works on the v2 sample.

Usage:  python exercises/webhook_handler.py samples/webhook_article_published_v2.json
"""
import json
import sys


def get_article_id(payload):
    # Old (v1) code: reads an integer field called article_id.
    return int(payload["article_id"])


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "samples/webhook_article_published_v2.json"
    payload = json.load(open(path, encoding="utf-8"))
    try:
        article_id = get_article_id(payload)
    except KeyError as missing:
        print(f"FAILED: the payload has no field {missing}.")
        print("Fields this payload does have:", ", ".join(payload))
        sys.exit(1)
    if payload.get("payload_version") != 2 or not isinstance(article_id, str):
        print(f"NOT YET: got {article_id!r}. In v2 the ID is a string (text), not a number.")
        sys.exit(1)
    print(f"OK: handled article {article_id} from payload v{payload['payload_version']}.")


if __name__ == "__main__":
    main()