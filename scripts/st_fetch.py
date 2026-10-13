#!/usr/bin/env python3
"""São Tomé and Príncipe: Constitution (Lei n.º 1/2003) and the legislation published on the website of the
Assembleia Nacional (hosted by the Brazilian Chamber of Deputies: www2.camara.leg.br/saotomeeprincipe).
PDFs without a usable text layer (scans with garbled OCR) are skipped and reported.
Usage: python3 st_fetch.py [--no-download]"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import st_text as T  # noqa

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(os.path.dirname(REPO), "_raw", "st")
RETRIEVED = os.environ.get("LC_RETRIEVED", "2026-10-13")
NODL = "--no-download" in sys.argv
BASE = "https://www2.camara.leg.br/saotomeeprincipe"
CONST = BASE + "/constituicao/constituicao-da-republica-democratica-de-s.tome-e"
FOLDERS = ["legislacao/eleitoral", "legislacao/gop-e-oge", "legislacao/legislacao-parlamentar"]
DELAY = 3


def get(url, name):
    dest = os.path.join(RAW, name)
    if not NODL:
        T.fetch(url, dest, delay=DELAY)
    return dest if os.path.exists(dest) else None


def plone_lines(path):
    return T.html_lines(path, "//div[@id='parent-fieldname-text']")


def write(rel, meta, body):
    T.write_md(os.path.join(REPO, rel), meta, meta["title"], body)
    print("OK", rel, sum(1 for x in body if x.startswith("#")))


def number(t):
    m = re.search(r"Lei\s*(?:n\.?\s*º)?\s*(\d+)\s*/\s*(\d{2,4})", t, re.I)
    if not m:
        return None, None
    y = m.group(2)
    y = y if len(y) == 4 else ("19" + y if int(y) > 50 else "20" + y)
    return m.group(1), y


def main():
    os.makedirs(RAW, exist_ok=True)
    rep = {"ok": [], "skipped": []}
    # Constitution (HTML page)
    p = get(CONST, "constituicao.html")
    lines = plone_lines(p)
    st = [i for i, x in enumerate(lines) if x.startswith("Preâmbulo")][-1]  # the first one is in the table of contents
    out = []
    for x in lines[st + 1:]:
        out += [x, ""]
    body = ["## Preâmbulo", ""] + T.structure(out, "pt")
    meta = {"title": "Constituição da República Democrática de São Tomé e Príncipe",
            "identifier": "Lei n.º 1/2003, de 29 de Janeiro (Lei de Revisão Constitucional), Diário da República n.º 2",
            "type": "constitution", "jurisdiction": "st", "language": "pt", "date": "2003-01-29", "status": "in_force",
            "source": CONST, "retrieved": RETRIEVED,
            "note": "Text as published by the Assembleia Nacional (constitutional revision of 2003)"}
    write("constituicao/constituicao.md", meta, body)
    rep["ok"].append(CONST)
    # legislation folders
    queue = [(BASE + "/" + f, open(get(BASE + "/" + f, f.replace("/", "_") + ".html"), encoding="utf-8").read(), BASE + "/" + f)
             for f in FOLDERS]
    while queue:
        furl, s, record = queue.pop(0)
        items = {}
        for u, t in re.findall(r'<a[^>]*href="(%s/[^"#]+)"[^>]*>(.*?)</a>' % re.escape(furl), s, re.S):
            t = T.norm(re.sub(r"<[^>]+>|\s+", " ", html.unescape(t)))
            if t and not t.startswith("Leia mais") and u.rstrip("/") != furl:
                items.setdefault(u, t)
        for u, t in items.items():
            title = re.sub(r"[.\s]+$", "", t)
            if u.endswith("/view") and re.search(r"\.pdf/view$", u, re.I):
                url = u[:-5]
                pdf = os.path.join(RAW, "pdf", T.slug(url.rsplit("/", 1)[-1]) + ".pdf")
                if not NODL:
                    T.fetch(url, pdf, delay=DELAY, check_pdf=True)
                if not pdf or not T.pdf_ok(pdf):
                    rep["skipped"].append(url + " (download)")
                    continue
                pages, _ = T.pdf_text_columns(pdf, "por", tmpdir=RAW, ocr=False)  # Diário da República: two columns
                txt = "\n".join(pages)
                if len(re.sub(r"\s", "", txt)) / max(1, len(pages)) < 400 or T.text_quality(txt) < 0.8:
                    rep["skipped"].append(url + " (no usable text layer)")
                    continue
                lines = T.clean_pages(pages)
                src = url
            elif not re.search(r"\.(zip|pdf|doc)", u, re.I):
                hp = get(u, "html_" + T.slug(u.rsplit("/", 1)[-1]) + ".html")
                lines = plone_lines(hp) if hp else []
                lines = [y for x in lines for y in (x, "")]
                src = u
                if sum(len(x) for x in lines) < 300:
                    sub = open(hp, encoding="utf-8").read() if hp else ""
                    if re.search(r'href="%s/[^"#]+\.pdf/view"' % re.escape(u), sub, re.I):
                        queue.append((u, sub, u))  # sub-folder with PDFs
                    else:
                        rep["skipped"].append(u + " (empty page)")
                    continue
            else:
                rep["skipped"].append(u + " (archive)")
                continue
            num, y = number(title)
            if "regimento" in title.lower():
                rel = "regimento/regimento-assembleia-nacional.md"
            elif num:
                rel = "leis/%s/lei-%s-%s.md" % (y, num, y)
            else:
                rel = "leis/sem-data/" + T.slug(title) + ".md"
            body = T.structure(lines, "pt")
            meta = {"title": title, "identifier": num and "Lei n.º %s/%s" % (num, y) or None, "type": "act", "jurisdiction": "st",
                    "language": "pt", "status": "unknown", "source": src, "record": record,
                    "retrieved": RETRIEVED}
            write(rel, meta, body)
            rep["ok"].append(src)
    json.dump(rep, open(os.path.join(RAW, "report.json"), "w"), indent=1, ensure_ascii=False)
    print({k: len(v) for k, v in rep.items()})
    for x in rep["skipped"]:
        print("SKIPPED", x)


if __name__ == "__main__":
    main()
