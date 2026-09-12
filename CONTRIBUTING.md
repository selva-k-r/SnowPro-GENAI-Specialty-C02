# Contributing

Corrections are the most valuable thing you can send. Snowflake changes fast and this repo will
drift.

## Reporting something wrong

Open an issue with:

1. The notebook and cell.
2. What it says.
3. The `docs.snowflake.com` link that contradicts it.

The doc link is the part that matters. "I think this is wrong" without one can't be acted on,
because the whole point of the repo is that nothing goes in unverified.

If the docs are genuinely silent on the point, say that — "I can't find this documented
anywhere" is a valid issue, and the fix is usually to delete the claim rather than to soften it.

## Sending a pull request

**Every factual claim needs a documentation link.** Not a blog post, not a Medium article, not
a Stack Overflow answer, not something a model told you. The Snowflake documentation page.

**Keep one result per cell.** Setup statements (`USE`, `SET`, `CREATE`, `GRANT`) can be grouped.
Anything that returns rows gets its own cell with its own `%%sql -r <name>` magic, so a reader
can always tell which statement produced which output. Don't rename existing `-r` result names —
other cells may reference them.

**Match the notebook structure.** A new notebook needs:

- an opening with the problem, the outcomes, prerequisites, and 3–6 documentation links
- inline definitions the first time a Snowflake term appears
- at least three `→ [More on …]` links through the body
- a `⚠️ Common misconceptions` box, framed as a belief a learner holds and what it actually
  produces when acted on — not as a changelog of what used to be wrong here
- one `🤔 Stop and think` cell of open trade-off questions
- exactly **12** `Check your understanding` questions with collapsed `<details>` answers:
  roughly 3 recall, 5 applied, 3 design judgement, 1 cross-domain. Every answer carries a doc
  link.

**Write for someone who has never used Cortex.** Problem before syntax. Say what a trade-off
costs rather than presenting one option as obviously right.

**No revision language.** Nothing in the notebooks should reference what an earlier version
said, when something was verified, or that a claim was corrected. Readers want the current truth,
not the history of how it got there. Git already has the history.

## Sample documents

If you add a document fixture:

- it must be entirely invented — no real company, person, address, or transaction
- every page carries a visible synthetic-sample stamp
- add it to the table in `README.md` and to the PUT commands in `setup/dataset.sql`
- generate it with a script committed alongside it, so the next person can regenerate or vary it

Never add a third party's PDF, including Snowflake's own study guide.

## Before you open the PR

```bash
python3 - <<'EOF'
import json, glob
for p in glob.glob('**/*.ipynb', recursive=True):
    nb = json.load(open(p, encoding='utf-8'))
    src = '\n'.join(''.join(c['source']) for c in nb['cells'])
    assert src.count('<details>') == 12, (p, src.count('<details>'))
    assert src.count('<details>') == src.count('</details>'), p
    print('ok', p)
EOF
```

Clear all cell outputs before committing. Notebook outputs make diffs unreadable and can leak
account identifiers, region names and query IDs.
