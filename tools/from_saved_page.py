"""Builds achievements.json from a saved TrueAchievements achievements page (Ctrl+S in a browser).

    python -I tools/from_saved_page.py t.html achievements.json

Only each achievement's name, description, gamerscore and whether it is secret are kept; nothing else from the
page (guides, ratios, player counts, images) is copied.
"""
import datetime
import html.parser
import json
import re
import sys


class Page(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.items, self.cur, self.field, self.depth = [], None, None, 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "ul" and "ach-panels" in (a.get("class") or "").split():
            self.depth += 1
        elif tag == "li" and self.depth and self.cur is None:
            self.cur = {"name": "", "description": "", "gamerscore": 0, "secret": False}
        elif self.cur is not None and tag == "a" and "title" in (a.get("class") or "").split() and not self.cur["name"]:
            self.field = "name"
        elif self.cur is not None and tag == "p" and not self.cur["description"]:
            self.field = "description"
            self.cur["secret"] = "secret" in (a.get("data-af") or "").lower()
            m = re.match(r"\s*(\d+)", a.get("data-bf") or "")
            self.cur["gamerscore"] = int(m.group(1)) if m else 0

    def handle_endtag(self, tag):
        if tag in ("a", "p"):
            self.field = None
        elif tag == "li" and self.cur is not None:
            if self.cur["name"]:
                self.cur["name"], self.cur["description"] = self.cur["name"].strip(), self.cur["description"].strip()
                self.items.append(self.cur)
            self.cur = None
        elif tag == "ul" and self.depth:
            self.depth -= 1

    def handle_data(self, data):
        if self.cur is not None and self.field:
            self.cur[self.field] += data


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: from_saved_page.py <saved page.html> <achievements.json>")
    p = Page()
    with open(sys.argv[1], encoding="utf-8", errors="replace") as f:
        p.feed(f.read())
    seen, items = set(), []
    for it in p.items:
        if it["name"].lower() in seen:
            continue
        seen.add(it["name"].lower())
        items.append({"id": len(items) + 1, **it})
    if not items:
        sys.exit("error: no achievements found; is this the game's achievements page, saved complete?")
    doc = {
        "game": "Grand Theft Auto VI",
        "platform": "Xbox Series X|S",
        "updated": datetime.date.today().isoformat(),
        "count": len(items),
        "gamerscore": sum(i["gamerscore"] for i in items),
        "achievements": items,
    }
    with open(sys.argv[2], "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"{len(items)} achievements, {doc['gamerscore']} gamerscore, {sum(i['secret'] for i in items)} secret")


if __name__ == "__main__":
    main()
