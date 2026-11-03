# AI-assisted interview skill

A Claude Code skill, `/interview`, for live, timed, AI-assisted technical interviews. You get a repo and a spec with more work than time. The skill walks you through a plan-first process, from system design and scope through sliced implementation with review to wrap-up. Claude does the legwork and you make the calls, so the interviewer can see your judgment.

See [`DIRECTIONS.md`](DIRECTIONS.md) for the design and reasoning behind it.

## Install

Requires [Claude Code](https://claude.com/claude-code).

```sh
git clone git@github.com:slightlytyler/ai-assisted-interview-skill.git
cd ai-assisted-interview-skill
./install.sh
```

`install.sh` symlinks `skill/interview/` to `~/.claude/skills/interview`, so changes you pull or make in this repo take effect without reinstalling. To uninstall, run `rm ~/.claude/skills/interview`.

## Use it in an interview

In the root of the interview repo:

```sh
claude
```

Then in Claude Code:

```
/interview        # 30-minute session
/interview 45     # custom length in minutes
```

The phases, with timings for a 30-minute session:

| Phase | Ends at | What happens |
|---|---|---|
| 0 Setup | ~1 min | Branch, plan files, background repo explorer, read the spec |
| 1 Understand | ~4 min | Problem summary, test command confirmed |
| 2 System design | ~8 min | Claude opens the Architecture section in `PLAN.md`, you write your broad strokes there (and paste a screenshot of any diagram), then Claude tidies and locks it |
| 3 Scope | ~10 min | Requirement matrix with minute estimates and an IN / STRETCH / OUT cut line |
| 4 Approach and gaps | ~12 min | Design for IN items, spec gaps, critic review, questions to ask the interviewer |
| 5 Implement | ~25 min | Plan committed, then thin slices, each one reviewed by you first and then by a reviewer agent |
| 6 Wrap-up | 30 min | Deliverables finished and checked, debrief bullets |

The state lives in `PLAN.md`, so running `/interview` again mid-session resumes where you left off.

Unless the spec says otherwise, you hand in working code, `NOTES.md` (what you built, what you skipped and why, next steps, risks) and `QUESTIONS.md` (the ambiguities and your assumptions).

## Practice run

The `playground/` folder is a small practice repo: a Python shared-expense ledger with a spec that has more work than fits in 30 minutes, plus some planted traps. It needs Python 3.11+ and nothing else.

1. **Make a fresh copy.** This copies the playground into its own git repo, so each run starts clean and the spoilers stay behind:

   ```sh
   ./new-playground.sh                     # creates ~/interview-playground
   ./new-playground.sh ~/practice/run-2    # or pick a path
   ```

2. **Run the session.**

   ```sh
   cd ~/interview-playground
   claude
   ```

   Then type `/interview`. Ideally get someone to play the interviewer: they answer your clarifying questions and sketch the architecture with you. Solo, answer the questions yourself and draw the diagram on paper or in a drawing tool, then paste a screenshot.

3. **Score yourself.** Afterwards, read [`rehearsal/INTERVIEWER_NOTES.md`](rehearsal/INTERVIEWER_NOTES.md). It lists the planted gaps, a reasonable priority call, and a self-score checklist. **Don't read it before a run**, since it gives away the traps.

4. **Clean up.** `new-playground.sh` won't overwrite an existing folder, so delete the old copy (`rm -rf ~/interview-playground`) or pass a new path for the next run.

## Repo layout

```
skill/interview/
  SKILL.md                     # the skill: phases, checkpoints, guardrails, subagent briefs
  templates/                   # skeletons for PLAN.md, QUESTIONS.md, NOTES.md
install.sh                     # symlinks the skill into ~/.claude/skills/
DIRECTIONS.md                  # design and reasoning behind the skill
playground/                    # practice repo (SPEC.md + small Python package)
new-playground.sh              # copies playground/ into a fresh git repo for each run
rehearsal/INTERVIEWER_NOTES.md # spoilers: planted gaps, priority call, self-score
```
