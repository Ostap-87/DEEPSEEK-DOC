#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Find + download freely licensed photos via Bing Images, keeping only known
free-license CDNs, then build a contact sheet for curation.

usage: img_pick.py <outdir> <prefix> "<query>" [n]
"""
import html, json, os, re, subprocess, sys
from urllib.parse import quote
from PIL import Image, ImageDraw

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0 Safari/537.36")

ALLOW = {
    "cdn.pixabay.com": ("Pixabay", "Pixabay License"),
    "images.pexels.com": ("Pexels", "Pexels License"),
    "upload.wikimedia.org": ("Wikimedia Commons", "CC"),
    "images.unsplash.com": ("Unsplash", "Unsplash License"),
    "live.staticflickr.com": ("Flickr", "CC"),
    "iu.isu.pub": ("", ""),
}


def curl(url, out=None, timeout=60):
    args = ["curl", "-sL", "-m", str(timeout), "-A", UA,
            "-H", "Accept: image/avif,image/webp,image/jpeg,image/*,*/*"]
    if out:
        args += ["-o", out]
    r = subprocess.run(args + [url], capture_output=True, text=False)
    return None if out else r.stdout.decode("utf-8", "ignore")


def bing(query, n=30):
    url = ("https://cn.bing.com/images/search?q=" + quote(query) +
           "&qft=+filterui:imagesize-large&form=IRFLTR&first=1")
    page = curl(url) or ""
    items = []
    for chunk in page.split('m="{')[1:]:
        blob = chunk.split('}"')[0]
        def grab(key):
            m = re.search(key + r'&quot;:&quot;(.*?)&quot;', blob)
            return html.unescape(m.group(1)) if m else ""
        u = grab("murl")
        if not u.startswith("http"):
            continue
        items.append({"murl": u, "t": grab("t"), "purl": grab("purl")})
    return items[:n]


def main():
    outdir, prefix, query = sys.argv[1], sys.argv[2], sys.argv[3]
    n = int(sys.argv[4]) if len(sys.argv) > 4 else 10
    os.makedirs(outdir, exist_ok=True)

    items = bing(query)
    seen, meta = set(), []
    for it in items:
        u = it.get("murl", "")
        host = re.sub(r"^https?://", "", u).split("/")[0].lower()
        src = ALLOW.get(host)
        if not src or u in seen:
            continue
        seen.add(u)
        fn = os.path.join(outdir, f"{prefix}-{len(meta)+1:02d}.jpg")
        try:
            curl(u, fn, 45)
            im = Image.open(fn).convert("RGB")
            if im.width < 900 or im.height < 500:
                os.remove(fn)
                continue
            im.save(fn, quality=87, optimize=True)
        except Exception:
            if os.path.exists(fn):
                os.remove(fn)
            continue
        meta.append({
            "file": fn, "src": src[0], "license": src[1],
            "query": query,
            "title": html.unescape(it.get("t", ""))[:120],
            "page": it.get("purl", ""),
            "w": im.width, "h": im.height,
        })
        if len(meta) >= n:
            break

    json.dump(meta, open(os.path.join(outdir, f"{prefix}.json"), "w"), ensure_ascii=False, indent=1)

    if meta:
        cols, tw, th = 3, 400, 260
        rows = (len(meta) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * tw, rows * (th + 20)), "white")
        d = ImageDraw.Draw(sheet)
        for i, m in enumerate(meta):
            im = Image.open(m["file"])
            im.thumbnail((tw - 10, th - 10))
            x = (i % cols) * tw + 5
            y = (i // cols) * (th + 20) + 5
            sheet.paste(im, (x, y))
            d.text((x + 4, y + th - 8), f"{i+1} · {m['src'][:14]}", fill="red")
        sheet.save(os.path.join(outdir, f"sheet-{prefix}.png"))
    print(f"{prefix}: {len(meta)} photos")


if __name__ == "__main__":
    main()
