# Git Exercise — Project 1 (ETL Pipeline)

Use this repo to practice the git skills from the module: **branching, squashing,
rebasing, PRs, conflict resolution.** The code is real; the point is the git reps.

## Setup (one time)
```bash
cd git_project_1_etl_pipeline
git init
git add .
git commit -m "Initial commit: ETL pipeline skeleton"
# create an empty repo on GitHub named etl_pipeline (no README), then:
git remote add origin git@github.com:<you>/etl_pipeline.git
git branch -M main
git push -u origin main
```

---

## Exercise A — Feature branch + PR (the core loop, you know this)
Goal: onboard a new source table (`sales`) without touching `main` directly.

```bash
git checkout main && git pull
git checkout -b feature/add-sales-source
```
1. Add `data/sales.csv` (a few rows: SALE_ID, CUSTOMER_ID, PRODUCT_ID, TOTAL_AMOUNT).
2. Add a `sales` entry to `config/tables.yml` (target_table: SALES_SRC).
3. Test: `python main.py --table sales --dry-run`
```bash
git add data/sales.csv config/tables.yml
git commit -m "Add sales source to ETL config"
git push -u origin feature/add-sales-source
```
4. Open a PR on GitHub, review the diff, merge. Then locally:
```bash
git checkout main && git pull
git branch -d feature/add-sales-source
```
This is the dbt loop, now in raw CLI. `git branch -d` deletes the merged branch.

---

## Exercise B — Squashing (NEW)
Goal: collapse several messy WIP commits into one clean commit before merging.

```bash
git checkout -b feature/add-load-logging
```
Make THREE small commits on purpose (simulating messy work):
```bash
# edit src/load.py: add a print before CREATE TABLE
git commit -am "wip logging"
# edit again: add a print after insert
git commit -am "more logging"
# edit again: fix a typo in the message
git commit -am "fix typo"
```
Now squash those 3 into 1 with interactive rebase:
```bash
git rebase -i HEAD~3
```
In the editor, leave the **first** line as `pick`, change the other two to `squash`
(or `s`). Save. Then write one clean combined message, e.g.
`Add load-step logging`. Save again.

`git log --oneline` now shows ONE commit instead of three.

**What happened:** `rebase -i` rewrote your branch's history, combining the commits.
**Why:** a clean, single, meaningful commit is far easier to review/revert than 3 WIP
noise commits. Squash *before* you open the PR.

```bash
git push -u origin feature/add-load-logging   # (first push)
# if you squashed AFTER already pushing, you'd need: git push --force-with-lease
```

---

## Exercise C — Rebasing onto an updated main (NEW)
Goal: replay your branch on top of the latest `main` instead of merging.

Simulate `main` moving ahead while you work:
1. On `main`, make + merge a small change (e.g. tweak the README) so `main` is ahead.
2. On your feature branch (which started from the OLD main):
```bash
git checkout feature/add-load-logging
git fetch origin
git rebase origin/main
```
This takes your commit(s) and **replays them on top of the new `main`** — as if you'd
branched from the latest. Result: a clean, linear history with no merge commit.

**Rebase vs merge:**
- `git merge main` → pulls main's changes in, creates a **merge commit**. History branches and rejoins (a diamond).
- `git rebase main` → moves your commits to sit **on top of** main. History stays **linear** (a straight line).

**The golden rule:** only rebase commits that are **yours and not yet shared/public.**
Never rebase commits others have already pulled — it rewrites history out from under them.
Branch-local cleanup = safe; rewriting `main` = no.

**If a conflict appears during rebase:**
```bash
# edit the conflicted file, then:
git add <file>
git rebase --continue
# or bail out entirely:
git rebase --abort
```

---

## Cheat sheet
```
git checkout -b <branch>        # create + switch to a branch
git commit -am "msg"            # stage tracked changes + commit
git rebase -i HEAD~N            # interactive rebase last N commits (squash here)
git rebase origin/main          # replay your branch on top of latest main
git rebase --continue/--abort   # after resolving / to cancel
git push --force-with-lease     # push rewritten history safely (only YOUR branch)
git merge <branch>              # merge (creates a merge commit)
```
Rule of thumb: **merge to combine shared work; rebase to tidy your own branch before sharing.**
