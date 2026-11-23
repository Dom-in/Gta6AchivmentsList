"""Builds achievements.json from a saved XboxAchievements.com achievements page (Ctrl+S in a browser).

    python -I tools/from_xboxachievements.py "<saved page>.html" achievements.json

Keeps each achievement's name, description, gamerscore and whether it is secret, and saves its picture to
images/ (the site's 730 x 410 one, scaled to 480 x 270; Pillow is needed). "image" is that file's path.
"""
import datetime
import html.parser
import io
import json
import os
import re
import sys
import time
import urllib.request

from PIL import Image

AGENT = {"User-Agent": "Gta6AchivmentsList/1.0"}


def fetch(url):
    data = urllib.request.urlopen(urllib.request.Request(url, headers=AGENT), timeout=20).read()
    if data[:2] != bytes([0xFF, 0xD8]):
        raise ValueError(f"not a JPEG: {url}")
    return data


def save_picture(a, folder):
    """The site's medium picture (its small one when there is none), 480 pixels wide, as images/NN-name.jpg."""
    try:
        data = fetch(a["image"].replace("-lo.jpg", "-med.jpg"))
    except Exception:
        data = fetch(a["image"])
    im = Image.open(io.BytesIO(data)).convert("RGB")
    if im.width > 480:
        im = im.resize((480, round(im.height * 480 / im.width)), Image.LANCZOS)
    slug = re.sub(r"[^a-z0-9]+", "-", a["name"].lower()).strip("-")
    path = f"images/{a['id']:02d}-{slug}.jpg"
    im.save(os.path.join(folder, path), "JPEG", quality=88, optimize=True, progressive=True)
    return path


class Page(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.items, self.cur, self.field, self.secret_list = [], None, None, False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = (a.get("class") or "").split()
        if tag == "ul" and "achilist" in cls:
            self.secret_list = "secret" in cls
        elif tag == "li" and "achilist__item" in cls:
            self.cur = {"name": "", "description": "", "gamerscore": 0, "secret": self.secret_list, "image": ""}
        elif self.cur is None:
            return
        elif tag == "img" and not self.cur["image"]:
            src = a.get("data-src") or a.get("src") or ""
            if src.startswith("https://img.xboxachievements.com/"):
                self.cur["image"] = src
        elif tag == "h4" and "achilist__title" in cls:
            self.field = "name"
        elif tag == "span" and "achilist__value-numb" in cls:
            self.field = "gamerscore"
        elif tag == "p" and self.cur["name"] and not self.cur["description"]:
            self.field = "description"

    def handle_endtag(self, tag):
        if tag == "p" and self.cur is not None and not self.cur["description"].strip():
            self.cur["description"] = ""   # the empty paragraph next to the gamerscore; the description is the next one
        if tag in ("h4", "span", "p"):
            self.field = None
        elif tag == "li" and self.cur is not None:
            if self.cur["name"].strip():
                self.items.append(self.cur)
            self.cur = None

    def handle_data(self, data):
        if self.cur is None or not self.field:
            return
        if self.field == "gamerscore":
            digits = "".join(ch for ch in data if ch.isdigit())
            if digits:
                self.cur["gamerscore"] = int(digits)
        else:
            self.cur[self.field] += data


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: from_xboxachievements.py <saved page.html> <achievements.json>")
    p = Page()
    with open(sys.argv[1], encoding="utf-8", errors="replace") as f:
        p.feed(f.read())
    seen, items = set(), []
    for it in p.items:
        name = " ".join(it["name"].split())
        if name.lower() in seen:
            continue
        seen.add(name.lower())
        items.append({"id": len(items) + 1, "name": name, "description": " ".join(it["description"].split()),
                      "gamerscore": it["gamerscore"], "secret": it["secret"], "image": it["image"]})
    if not items:
        sys.exit("error: no achievements found; is this the game's achievements page?")
    doc = {
        "game": "Grand Theft Auto VI",
        "platform": "Xbox Series X|S",
        "updated": datetime.date.today().isoformat(),
        "count": len(items),
        "gamerscore": sum(i["gamerscore"] for i in items),
        "images": "Each achievement's picture is in images/, at the path in its \"image\" field.",
        "achievements": items,
    }
    folder = os.path.dirname(os.path.abspath(sys.argv[2]))
    os.makedirs(os.path.join(folder, "images"), exist_ok=True)
    for it in items:
        if it["image"]:
            it["image"] = save_picture(it, folder)
            time.sleep(0.2)
    with open(sys.argv[2], "w", encoding="utf-8", newline="\n") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"{len(items)} achievements, {doc['gamerscore']} gamerscore, {sum(i['secret'] for i in items)} secret, "
          f"{sum(bool(i['image']) for i in items)} pictures in images/")


if __name__ == "__main__":
    main()
