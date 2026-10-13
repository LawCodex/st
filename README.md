# São Tomé and Príncipe (ST) — legislação em Markdown

Part of [LawCodex](https://github.com/LawCodex): the legislation of every country as plain Markdown in git.

**Partial repository.** Legislation of the Democratic Republic of São Tomé and Príncipe, in Portuguese, as
published on the website of the **Assembleia Nacional** (hosted by the Brazilian Chamber of Deputies under a
parliamentary cooperation programme): the Constitution, the Rules of Procedure of the National Assembly and the laws
listed in its "Legislação" section (electoral, parliamentary and budget-planning laws).

Retrieved 2026-10-13.

<!-- COUNTS -->
| Directory | Files |
|---|---|
| `constituicao/` | 1 |
| `leis/` | 13 |
| `regimento/` | 1 |
| **Total** | **15** |
<!-- /COUNTS -->

## Structure

```
constituicao/constituicao.md                Constitution, as revised by Lei n.º 1/2003 (29 January 2003)
regimento/regimento-assembleia-nacional.md  Regimento da Assembleia Nacional
leis/<year>/lei-<n>-<year>.md               laws (Diário da República PDFs)
```

Front matter: `identifier` = law number; `source` = page or PDF converted; `record` = the listing page;
`status: unknown`. Many files are amending laws, given as published. Laws are cut from Diário da República PDF
issues laid out in two columns (split automatically); page headers of the issue (date, number, summary) remain at
the top of some files.

## Source

| Source | URL |
|---|---|
| Assembleia Nacional — Constituição | https://www2.camara.leg.br/saotomeeprincipe/constituicao/constituicao-da-republica-democratica-de-s.tome-e |
| Assembleia Nacional — Legislação (eleitoral, GOP e OGE, legislação parlamentar) | https://www2.camara.leg.br/saotomeeprincipe/legislacao |

## Not covered / known gaps

* **No general collection of laws.** No official online *Diário da República* of São Tomé and Príncipe could be
  found: the domains of the Government, Ministry of Justice, courts and national press (gov.st is a citizen
  portal without legislation; presidencia.st is a JavaScript-only site; parlamento.st, stj.st,
  tribunalconstitucional.st did not answer).
* Of the PDFs on the Assembly website, 7 are scans with an unusable (garbled) OCR text layer and were skipped:
  Lei n.º 11/90 (Lei Eleitoral), Lei n.º 2/90, Lei n.º 11/92, Lei n.º 6/96, Lei n.º 2/98, and the files
  `LE1191007.pdf` (Lei Orgânica folder) and `LE2013006.pdf` (Estatuto de Deputado folder). Historical constitutional laws (1982, 1987, 1990) are offered only as ZIP
  archives: not included.
* Constitutional amendments after 2003, if any, are not included.

## Copyright

Official texts of the Democratic Republic of São Tomé and Príncipe, published by the National Assembly without
stated reuse restrictions; official legislative texts are generally not subject to copyright. The Markdown
conversion is provided as is; the authoritative text is the one published in the *Diário da República*.

## Regenerating

```sh
python3 scripts/st_fetch.py    # downloads to ../_raw/st/ (3 s between requests) and writes the Markdown
python3 scripts/st_readme.py   # updates the counts table
```
