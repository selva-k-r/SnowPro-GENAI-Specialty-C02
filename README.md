# SnowPro Specialty: Gen AI (GES-C02) — a hands-on study repo

Runnable notebooks for every objective in the **SnowPro Specialty: Gen AI** exam, built to be
worked through rather than read. Every SQL statement runs against a real Snowflake account.
Every claim links back to the Snowflake documentation page it came from.

This is not a braindump and it is not a summary of the study guide. It is the lab you build
while you study.

---

## Who this is for

You know SQL. You have a Snowflake account. You have not used Cortex, or you have used one or
two functions and want the rest of the picture. You would rather run a query and look at the
output than read a bullet list about what the query would have returned.

If you have never opened Snowflake at all, start with
[Snowflake in 20 minutes](https://docs.snowflake.com/en/user-guide/tutorials/snowflake-in-20minutes)
first and come back.

---

## Getting started

**1. Create the practice data.** Run [`setup/dataset.sql`](setup/dataset.sql) once. It creates
the `GENAI_STUDY` database, two tables, a stage and a stream.

**2. Upload the sample documents.** The PUT commands are at the bottom of the same script.
They load the six files in [`sample_docs/`](sample_docs/) onto the stage that Domain 4 uses.

**3. Grant yourself Cortex access.** Most notebooks need the `SNOWFLAKE.CORTEX_USER` database
role, which `ACCOUNTADMIN` grants:

```sql
GRANT DATABASE ROLE SNOWFLAKE.CORTEX_USER TO ROLE <your_role>;
```

Notebook 3.2 explains what this role actually covers and what it does not.

**4. Open the first notebook.** These run in Snowflake Notebooks, in VS Code with the Snowflake
extension, or anywhere a `%%sql` magic is wired to a Snowflake connection.

> **Cost warning.** These notebooks call AI functions, which consume credits per token or per
> page. Working through the whole repo on a small warehouse costs a few credits, not hundreds —
> but it is not free, and a runaway `AI_COMPLETE` over a large table can surprise you. Notebook
> 3.3 covers how to see what you have spent. Run that one early, not last.

---

## The path

Work in order. Each domain assumes the one before it.

| | Notebook | What it covers | Exam weight |
|---|---|---|---|
| **1** | [1.1](Domain%201.0%20-%20Gen%20AI%20Overview/1.1.ipynb) · [1.2](Domain%201.0%20-%20Gen%20AI%20Overview/1.2.ipynb) | What Cortex is, how a model call is billed and routed, tokens, embeddings, prompting | 19% |
| **2** | [2.1](Domain%202.0%20-%20Gen%20AI%20Functions/2.1.ipynb) – [2.5](Domain%202.0%20-%20Gen%20AI%20Functions/2.5.ipynb) | The AISQL functions, Cortex Search, Cortex Analyst and semantic views, Agents, fine-tuning | 38% |
| **3** | [3.1](Domain%203.0%20-%20Gen%20AI%20Governance/3.1.ipynb) – [3.4](Domain%203.0%20-%20Gen%20AI%20Governance/3.4.ipynb) | Privileges, model access, cross-region, cost attribution, observability, guardrails | 28% |
| **4** | [4.1](Domain%204.0%20-%20Document%20Processing/4.1.ipynb) – [4.4](Domain%204.0%20-%20Document%20Processing/4.4.ipynb) | `AI_PARSE_DOCUMENT`, `AI_EXTRACT`, stages and FILE objects, document pipelines | 15% |

Then the deep dives, for the three areas that people reliably lose marks on:

- [DD1 — Snowpark Container Services](Deep%20Dives/DD1%20-%20Snowpark%20Container%20Services.ipynb)
- [DD2 — Model Registry](Deep%20Dives/DD2%20-%20Model%20Registry.ipynb)
- [DD3 — Governance end to end](Deep%20Dives/DD3%20-%20Governance%20End%20to%20End.ipynb)

And last, the capstone that spans all four domains:

- [Comprehensive exercise](Domain%200.0%20-%20Comprehensive%20Gap%20Exercise/ComprehensiveExercise.ipynb)

---

## How each notebook is built

Every notebook follows the same shape, so you always know where you are:

- **The problem this solves** — a situation before any syntax, so the feature has something to
  attach to.
- **Concept sections** — one runnable statement per cell. If a cell returns a result set, it is
  the only thing in that cell, so you can always see exactly which statement produced what.
- **⚠️ Common misconceptions** — the beliefs that produce silent NULLs, surprise bills and
  permission errors. These are the failures worth memorising, because the error message rarely
  tells you what actually went wrong.
- **🤔 Stop and think** — open questions about cost, latency and governance trade-offs. No
  answers. These are the parts the syntax does not teach.
- **Check your understanding** — twelve questions with collapsed answers. Roughly three recall,
  five applied, three design judgement, one that reaches into another domain.

---

## Sample documents

[`sample_docs/`](sample_docs/) contains six files written for this repo:

| File | Pages | Used for |
|---|---|---|
| `invoice_KF-2041.pdf` | 1 | scalar field extraction; carries a disputed line item |
| `invoice_AV-8817.pdf` | 1 | professional-services invoice, fractional quantities |
| `invoice_TS-5530.pdf` | 1 | five line items — table extraction |
| `contract_msa_harbourview.pdf` | 3 | clause question-answering, LAYOUT mode, `page_filter` |
| `financial_statement_mgc_q3_2026.pdf` | 3 | markdown tables from LAYOUT mode, `page_split` |
| `support_tickets.txt` | — | classification and sentiment over a text-format file |

**Every company, person, address, amount and contract term in these files is invented.** Each
page carries a synthetic-sample stamp. They exist so the exercises have something realistic to
run against without anyone's real documents or a third party's copyrighted PDF ending up in a
public repo.

---

## On accuracy

Every factual claim here — parameter names, defaults, limits, privileges, billing states — was
checked against `docs.snowflake.com` and carries a link to the page it came from. Where the
documentation is silent, the notebook says so rather than guessing.

Two things follow from that, and both matter:

**Snowflake ships fast.** A default that was right when a notebook was written can change. The
doc links are there so you can check the current behaviour in ten seconds, and you should,
especially for anything you are about to put in production.

**Where the docs disagree with themselves, the notebooks say which page they followed.** For
example, compute pool billing states are stated explicitly on the
[cost page](https://docs.snowflake.com/en/developer-guide/snowpark-container-services/accounts-orgs-usage-views)
and only referenced from the
[compute pool page](https://docs.snowflake.com/en/developer-guide/snowpark-container-services/working-with-compute-pool);
the notebooks follow the cost page and say so.

Found something wrong? [Open an issue](../../issues) with the doc link that contradicts it.
That is the most useful contribution you can make.

---

## Not included

- **The official study guide.** Download it from
  [Snowflake's certification pages](https://www.snowflake.com/en/resources/learn/certifications/). It is
  Snowflake's document and does not belong in a third-party repo.
- **Real exam questions.** The questions here test the same objectives; none of them are from
  the exam, and anyone offering you real ones is selling you a way to fail.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). The short version: a correction needs a documentation
link, and new content follows the structure above, including the twelve questions.

## Licence

[MIT](LICENSE). Use it, fork it, teach from it.

Snowflake, SnowPro and Snowflake Cortex are trademarks of Snowflake Inc. This repo is an
independent study resource and is not affiliated with, endorsed by, or sponsored by Snowflake.
