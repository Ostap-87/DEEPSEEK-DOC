#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Layout engine reproducing the "Global Tech Tour" report system."""
import os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = r"""
@page{
  size:A4 portrait;
  margin:15mm 15mm 15mm;
}
@page land{
  size:A4 landscape;
  margin:14mm 15mm 15mm;
}
@page:first{
  margin:0; background:#0B1F3F;
  @bottom-left{content:none}
  @bottom-right{content:none}
}
*{box-sizing:border-box; -webkit-print-color-adjust:exact; print-color-adjust:exact}
html,body{margin:0;padding:0}
body{
  font-family:Inter,"PingFang SC","Songti SC",sans-serif;
  font-size:10pt; line-height:1.52; color:#16202B;
}
p{margin:0 0 6.4pt; text-align:left; hyphens:none; orphans:2; widows:2}
strong{font-weight:700; color:#0E1A26}
a{color:#1A73E8; text-decoration:none}
.cn{font-family:"PingFang SC","Songti SC",sans-serif}

/* ---------- page frame ---------- */
.page{break-before:page; min-height:266.6mm; display:flex; flex-direction:column}
.page.land{min-height:180.9mm}
.pbody{flex:1 0 auto}
.foot{margin-top:auto; display:flex; justify-content:space-between;
  align-items:baseline; font-family:Inter,sans-serif}
.foot .fl{font-size:7pt; color:#8A97A6; letter-spacing:.02em; font-family:"Helvetica Neue",Arial,sans-serif}
.foot .pn{font-family:Oswald,sans-serif; font-weight:700; font-size:8.6pt; color:#1A73E8}
.page:first-of-type{break-before:auto}

/* ---------- titles ---------- */
.h-page{
  font-family:Oswald,sans-serif; font-weight:700; font-size:29pt; line-height:1.06;
  text-transform:uppercase; color:#1A73E8; letter-spacing:.005em; margin:0 0 3.4mm;
}
.rule{height:2.2pt; background:#1A73E8; margin:0 0 6mm}
.h-sub{
  font-family:Inter,sans-serif; font-weight:700; font-size:12.2pt; color:#1A73E8;
  margin:7mm 0 2.6mm; line-height:1.3; letter-spacing:-.01em;
}
.h-sub:first-child{margin-top:0}
.h-mini{
  font-family:Inter,sans-serif; font-weight:700; font-size:9.4pt; color:#0E1A26;
  margin:5mm 0 1.8mm; letter-spacing:.01em; text-transform:uppercase;
}
.lead{font-size:11.4pt; line-height:1.5; font-weight:500; color:#12202E; margin-bottom:5mm; text-align:left}

/* ---------- text blocks ---------- */
ul.b,ol.b{margin:0 0 5mm; padding-left:4.6mm}
ul.b li,ol.b li{margin-bottom:1.9mm; line-height:1.5; text-align:left}
ul.b{list-style:none; padding-left:4mm}
ul.b li{position:relative}
ul.b li::before{content:"•"; position:absolute; left:-4mm; color:#1A73E8; font-weight:700}
ol.b{padding-left:5.4mm}
ol.b li::marker{color:#1A73E8; font-weight:700; font-size:9.6pt}

/* ---------- callout ---------- */
.callout{
  background:#F1F5FD; border-left:2.6pt solid #1A73E8; padding:4.2mm 5mm; margin:0 0 5mm;
  break-inside:avoid;
}
.callout .lab{
  display:block; font-weight:700; font-size:8pt; letter-spacing:.1em; text-transform:uppercase;
  color:#1A73E8; margin-bottom:1.6mm;
}
.callout p{margin:0; font-size:9.8pt; line-height:1.52; text-align:left; hyphens:none}
.callout p+p{margin-top:2mm}
.callout.soft{background:#F7F9FC; border-left-color:#B9C6D6}
.callout.soft .lab{color:#5D6B7A}

/* ---------- tiles ---------- */
.tiles{display:flex; flex-wrap:wrap; gap:3mm; margin:0 0 5mm}
.tile{flex:1 1 30%; min-width:30%; background:#F1F5FD; padding:2.8mm 3.2mm; break-inside:avoid}
.tile .k{
  display:block; font-size:6.6pt; letter-spacing:.09em; text-transform:uppercase;
  color:#6B7C8C; margin-bottom:1.1mm; font-weight:600;
}
.tile .v{display:block; font-size:9.6pt; font-weight:700; color:#0E1A26; line-height:1.28}
.tile .v.hi{color:#0F8A52}
.tile .v.blue{color:#1A73E8}

/* ---------- table ---------- */
table{width:100%; border-collapse:collapse; font-size:7.6pt; margin:0 0 3mm}
table.dense{font-size:6.9pt}
.duo{display:flex; gap:6mm; align-items:flex-start; margin-bottom:2mm}
.duo>div{flex:1; min-width:0}
.duo table{margin:0; font-size:6.2pt}
.duo tbody td{padding:.82mm 1.5mm; line-height:1.22}
.duo thead th{padding:1.4mm 1.6mm; font-size:6.2pt}
table.dense tbody td{padding:1.25mm 1.9mm; line-height:1.28}
table.dense thead th{padding:1.5mm 1.9mm; font-size:6.4pt}
thead th{
  background:#1A73E8; color:#fff; text-align:left; padding:1.9mm 2.2mm;
  font-weight:700; font-size:6.8pt; letter-spacing:.06em; text-transform:uppercase;
  vertical-align:middle;
}
tbody td{padding:1.7mm 2.2mm; vertical-align:top; line-height:1.34; border-bottom:.4pt solid #E1E8F2}
tbody tr:nth-child(even) td{background:#F7F9FC}
tbody td.acc{color:#1A73E8; font-weight:700}
tbody td.name{width:47mm}
tbody td.name{font-weight:600; color:#0E1A26}

/* ---------- photos ---------- */
.pgrid{display:flex; flex-wrap:wrap; gap:5mm 5mm; margin:0}
.ph{width:calc(50% - 2.5mm); break-inside:avoid}
.ph img{width:100%; aspect-ratio:16/10; object-fit:cover; display:block; border-radius:1.4mm}
.ph .cap{font-size:7.6pt; line-height:1.4; margin-top:1.8mm; text-align:left; hyphens:none}
.ph .cap .n{color:#1A73E8; font-weight:700; margin-right:1.2mm}
.ph .src{font-size:6.8pt; color:#7C8A99; margin-top:.8mm; line-height:1.35}
.ph .src b{color:#1A73E8; font-weight:600}

/* ---------- cover ---------- */
.cover{height:297mm; position:relative; background:#0B1F3F; color:#fff; overflow:hidden; break-after:page}
.cov-grid{position:absolute; inset:0 0 auto 0; height:151mm; display:flex; flex-wrap:wrap}
.cov-grid img{width:33.3333%; height:75.5mm; object-fit:cover; display:block}
.cov-body{position:absolute; left:0; right:0; top:151mm; bottom:0}
.badge{
  position:absolute; left:15mm; top:-8.5mm; background:#fff; color:#0B1F3F; border-radius:2.6mm;
  padding:2.8mm 5mm 2.8mm 3.4mm; display:flex; align-items:center; gap:2.6mm;
  font-weight:700; font-size:7.6pt; letter-spacing:.13em; text-transform:uppercase;
}
.badge .dia{width:6.4mm; height:6.4mm; background:#1A73E8; transform:rotate(45deg); border-radius:.8mm}
.cov-kicker{
  position:absolute; top:17.5mm; left:15mm; right:15mm;
  font-size:7.4pt; letter-spacing:.22em; text-transform:uppercase; color:#8FB4EC}
.cov-title{
  position:absolute; top:23mm; left:15mm; right:15mm;
  font-family:Oswald,sans-serif; font-weight:700; font-size:44pt; line-height:.97;
  text-transform:uppercase; letter-spacing:.004em; margin:0;
}
.cov-deck{position:absolute; left:15mm; width:134mm;
  font-size:10.6pt; line-height:1.5; color:#CFDCEC; text-align:left; hyphens:none}
.cov-stats{position:absolute; left:15mm; right:15mm; bottom:36mm; display:flex; gap:12mm}
.cov-stat .n{font-family:Oswald,sans-serif; font-weight:700; font-size:22pt; line-height:1; color:#fff;
  white-space:nowrap}
.cov-stat .l{font-size:6.9pt; line-height:1.35; color:#93A6BD; margin-top:2mm; max-width:34mm}
.cov-foot{position:absolute; left:15mm; right:15mm; bottom:12mm; display:flex; justify-content:space-between;
  border-top:.5pt solid rgba(255,255,255,.22); padding-top:3mm;
  font-size:7pt; color:#8AA0BA}
.cov-foot b{color:#C9D8EA; font-weight:600}

/* ---------- closing ---------- */
.endband{background:#0B1F3F; color:#fff; padding:7mm 8mm; margin-top:6mm}
.endband .t{font-family:Oswald,sans-serif; font-weight:700; font-size:16pt; text-transform:uppercase; margin:0 0 2.5mm}
.endband p{margin:0; color:#C9D8EA; font-size:9pt; text-align:left}
"""


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def tr(s):
    return s  # content already authored with inline markup


def blocks(items):
    out = []
    for b in items:
        t = b.get("t", "p")
        if t == "p":
            out.append(f'<p>{b["x"]}</p>')
        elif t == "lead":
            out.append(f'<p class="lead">{b["x"]}</p>')
        elif t == "h":  # blue subhead
            out.append(f'<div class="h-sub">{b["x"]}</div>')
        elif t == "h3":
            out.append(f'<div class="h-mini">{b["x"]}</div>')
        elif t == "ul":
            lis = "".join(f"<li>{x}</li>" for x in b["x"])
            out.append(f'<ul class="b">{lis}</ul>')
        elif t == "ol":
            lis = "".join(f"<li>{x}</li>" for x in b["x"])
            out.append(f'<ol class="b">{lis}</ol>')
        elif t == "callout":
            lab = f'<span class="lab">{b["label"]}</span>' if b.get("label") else ""
            ps = "".join(f"<p>{x}</p>" for x in (b["x"] if isinstance(b["x"], list) else [b["x"]]))
            cls = "callout soft" if b.get("soft") else "callout"
            out.append(f'<div class="{cls}">{lab}{ps}</div>')
        elif t == "tiles":
            cells = "".join(
                f'<div class="tile"><span class="k">{c[0]}</span>'
                f'<span class="v{" " + c[2] if len(c) > 2 and c[2] else ""}">{c[1]}</span></div>'
                for c in b["x"])
            out.append(f'<div class="tiles">{cells}</div>')
        elif t == "table":
            head = "".join(f"<th>{h}</th>" for h in b["head"])
            rows = []
            for r in b["rows"]:
                tds = []
                for i, c in enumerate(r):
                    cls = ""
                    if b.get("cls") and i < len(b["cls"]) and b["cls"][i]:
                        cls = f' class="{b["cls"][i]}"'
                    tds.append(f"<td{cls}>{c}</td>")
                rows.append("<tr>" + "".join(tds) + "</tr>")
            cls = ' class="dense"' if b.get("dense") else ""
            out.append(f'<table{cls}><thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table>')
        elif t == "table2":
            def render_one(spec):
                head = "".join(f"<th>{h}</th>" for h in spec["head"])
                rows = []
                for r in spec["rows"]:
                    tds = []
                    for i, c in enumerate(r):
                        cls = ""
                        if spec.get("cls") and i < len(spec["cls"]) and spec["cls"][i]:
                            cls = f' class="{spec["cls"][i]}"'
                        tds.append(f"<td{cls}>{c}</td>")
                    rows.append("<tr>" + "".join(tds) + "</tr>")
                return f'<table class="dense">{("<thead><tr>" + head + "</tr></thead>")}<tbody>{"".join(rows)}</tbody></table>'
            out.append('<div class="duo">'
                       f'<div>{render_one(b["left"])}</div>'
                       f'<div>{render_one(b["right"])}</div></div>')
        elif t == "raw":
            out.append(b["x"])
    return "\n".join(out)


PAGE_NO = {"n": 1}
FOOTER_TEXT = ""


def foot_next():
    PAGE_NO["n"] += 1
    return foot()


def foot():
    return (f'<div class="foot"><span class="fl">{FOOTER_TEXT}</span>'
            f'<span class="pn">{PAGE_NO["n"]}</span></div>')


def page(title, body, kicker=None, land=False):
    head = ""
    if title:
        head = f'<h1 class="h-page">{title}</h1><div class="rule"></div>'
    cls = "page land" if land else "page"
    PAGE_NO["n"] += 1
    return f'<section class="{cls}"><div class="pbody">{head}{body}</div>{foot()}</section>'


def cover(m):
    grid = "".join(f'<img src="file://{p}">' for p in m["photos"])
    stats = "".join(
        f'<div class="cov-stat"><div class="n">{n}</div><div class="l">{l}</div></div>'
        for n, l in m["stats"])
    lines = m["title"].count("\n") + 1
    title = m["title"].replace("\n", "<br>")
    deck_top = round(23 + lines * 15.5 + 10, 1)
    return f"""
<section class="cover">
  <div class="cov-grid">{grid}</div>
  <div class="cov-body">
    <div class="badge"><span class="dia"></span>Global Tech Tour</div>
    <div class="cov-kicker">{m['kicker']}</div>
    <h1 class="cov-title">{title}</h1>
    <p class="cov-deck" style="top:{deck_top}mm">{m['deck']}</p>
    <div class="cov-stats">{stats}</div>
    <div class="cov-foot"><span><b>Global Tech Tour</b> · globaltechtour.ru</span><span>{m['date']} · внутренний документ</span></div>
  </div>
</section>"""


def photo_page(m):
    items = []
    for i, it in enumerate(m["items"], 1):
        items.append(
            f'<div class="ph"><img src="file://{it["file"]}">'
            f'<div class="cap"><span class="n">{i:02d}</span>{it["cap"]}</div>'
            f'<div class="src">Источник: <b>{it["src"]}</b>{(" · " + it["lic"]) if it.get("lic") else ""}</div></div>')
    body = f'<div class="pgrid">{"".join(items)}</div>'
    return page(m["title"], body)


def render(report, out_html):
    css = open(os.path.join(ROOT, "fonts", "fonts.css"), encoding="utf-8").read()
    css = css.replace("url('fonts/", "url('file://" + os.path.join(ROOT, "fonts") + "/")
    global FOOTER_TEXT
    FOOTER_TEXT = report["meta"]["footer_left"]
    PAGE_NO["n"] = 1
    parts = [cover(report["meta"]["cover"])]
    for p in report["pages"]:
        kind = p.get("type", "page")
        if kind == "page":
            parts.append(page(p.get("title", ""), blocks(p["blocks"])))
        elif kind == "landscape":
            table_html = blocks([p["table"]])
            lead = f'<p class="lead">{p["lead"]}</p>' if p.get("lead") else ""
            parts.append(
                f'<section class="page land" style="page:land"><div class="pbody">'
                f'<h1 class="h-page">{p["title"]}</h1><div class="rule"></div>'
                f'{lead}{table_html}</div>{foot_next()}</section>')
        elif kind == "photos":
            parts.append(photo_page(p))
        elif kind == "raw":
            parts.append(p["html"])

    css_ctx = CSS
    html = f"""<!doctype html><html lang="ru"><head><meta charset="utf-8">
<title>{report['meta']['doc_title']}</title>
<meta name="author" content="Global Tech Tour">
<style>
{css}
{css_ctx}
{report['meta'].get('css','')}
</style></head><body>
{"".join(parts)}
</body></html>"""
    open(out_html, "w", encoding="utf-8").write(html)
    return out_html
