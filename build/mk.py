#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""usage: mk.py <report_module> <out.pdf> [--preview]"""
import importlib, os, shutil, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "build"))
sys.path.insert(0, os.path.join(ROOT, "reports"))
import r_lib

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PY = os.path.join(ROOT, "work", "venv", "bin", "python")


def render_pdf(html, pdf):
    prof = "/tmp/dshc-rep"
    shutil.rmtree(prof, ignore_errors=True)
    os.makedirs("/tmp/dshdumps", exist_ok=True)
    cmd = [CHROME, "--headless=new", "--no-sandbox", "--disable-gpu",
           "--disable-crash-reporter", "--disable-breakpad",
           "--crash-dumps-dir=/tmp/dshdumps", "--user-data-dir=" + prof,
           "--no-pdf-header-footer", "--print-to-pdf=" + pdf,
           "file://" + os.path.abspath(html)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if not os.path.exists(pdf):
        print(r.stdout[-1500:], r.stderr[-1500:])
        raise SystemExit("chrome failed")


def previews(pdf, outdir):
    shutil.rmtree(outdir, ignore_errors=True)
    os.makedirs(outdir)
    subprocess.run([PY, "-c", """
import sys, pypdfium2 as pdfium
d = pdfium.PdfDocument(sys.argv[1]); o = sys.argv[2]
for i in range(len(d)):
    d[i].render(scale=1.5).to_pil().save(f"{o}/p{i+1:02d}.png")
print("pages", len(d))
""", pdf, outdir], check=True)


if __name__ == "__main__":
    mod, out = sys.argv[1], sys.argv[2]
    do_prev = "--preview" in sys.argv
    m = importlib.import_module(mod)
    html = os.path.join(ROOT, "build", f"{mod}.html")
    r_lib.render(m.REPORT, html)
    render_pdf(html, out)
    print("pdf:", out, os.path.getsize(out))
    if do_prev:
        previews(out, os.path.join(ROOT, "build", "prev_" + mod))
