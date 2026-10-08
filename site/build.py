#!/usr/bin/env python3
"""Build the GitHub Pages site into _site/.

Each game is authored as a page fragment (title, links and styles first, then the body),
the shape the Artifact viewer expects. This wraps every fragment in a full HTML document
and writes a hub page that links to all of them. To add a game, add one entry to GAMES.
"""
import html
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"

GAMES = [
    {"slug": "truth-dare", "src": "truth-dare.html", "title": "حقیقت یا جرئت",
     "desc": "بطری را روی فرش بچرخان؛ هر کس بطری به او رسید، حقیقت می‌گوید یا جرئت می‌کند.",
     "tags": ["گروهی", "۲ تا ۱۰ نفر"], "accent": "#eaa632"},
    {"slug": "adabazi", "src": "charades.html", "title": "ادابازی",
     "desc": "پانتومیم دو گروهی روی صحنه‌ی تئاتر؛ بدون یک کلمه حرف، کارت را بازی کن.",
     "tags": ["دو گروه", "۴ نفر به بالا"], "accent": "#dcaa45"},
    {"slug": "esm-famil", "src": "esm-famil.html", "title": "اسم فامیل",
     "desc": "حرف را بچرخان و تا تمام شدن زمان، برای هر ستون یک کلمه پیدا کن.",
     "tags": ["گروهی", "۲ تا ۸ نفر"], "accent": "#2f8a5f"},
    {"slug": "dusk-garden", "src": "dusk-garden.html", "title": "باغچه‌ی غروب",
     "desc": "کانال‌های کاغذی را بچرخان تا آب چشمه به همه‌ی گل‌ها برسد.",
     "tags": ["تک‌نفره", "پازل"], "accent": "#5fd8d2"},
]

HEAD = """<!doctype html>
<html lang="fa">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="{theme}">
<style>body{{margin:0}}img{{max-width:100%}}[hidden]{{display:none!important}}</style>
"""


def wrap(fragment: str, theme: str) -> str:
    # the fragment opens with <title>, <meta>, <link> and one <style>; those belong in <head>
    cut = fragment.index("</style>") + len("</style>")
    return HEAD.format(theme=theme) + fragment[:cut] + "\n</head>\n<body>\n" + fragment[cut:] + "\n</body>\n</html>\n"


def card(g: dict, i: int) -> str:
    tags = "".join(f"<span>{html.escape(t)}</span>" for t in g["tags"])
    return f"""
    <a class="game" href="{g['slug']}/" style="--accent:{g['accent']};--i:{i}">
      <span class="phone"><img src="thumbs/{g['slug']}.jpg" alt="" width="360" height="779" loading="lazy"></span>
      <span class="info">
        <b>{html.escape(g['title'])}</b>
        <span class="desc">{html.escape(g['desc'])}</span>
        <span class="tags">{tags}</span>
        <span class="play">بازی کن</span>
      </span>
    </a>"""


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    built = []
    for g in GAMES:
        src = ROOT / g["src"]
        if not src.exists():
            print("skip (missing):", g["src"])
            continue
        d = OUT / g["slug"]
        d.mkdir()
        (d / "index.html").write_text(wrap(src.read_text(encoding="utf-8"), "#15101c"), encoding="utf-8")
        built.append(g)
        print("built:", g["slug"])
    shutil.copytree(ROOT / "site" / "thumbs", OUT / "thumbs")
    hub = (ROOT / "site" / "hub.html").read_text(encoding="utf-8")
    hub = hub.replace("<!--GAMES-->", "".join(card(g, i) for i, g in enumerate(built)))
    hub = hub.replace("<!--COUNT-->", "۰۱۲۳۴۵۶۷۸۹"[len(built)])
    (OUT / "index.html").write_text(hub, encoding="utf-8")
    (OUT / ".nojekyll").write_text("")
    print("hub with", len(built), "games")


if __name__ == "__main__":
    main()
