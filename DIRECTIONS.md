# Directions: AI-Assisted Interview Skill

## Purpose

This skill supports a staff software engineering candidate during a live, AI-assisted technical interview. The candidate gets a repo and a `SPEC` file describing what to build. The session is **30 minutes** unless the candidate says otherwise, and the spec contains more work than that allows.

Treat it like a system design problem rather than a pure coding problem. The interviewer is grading the candidate's judgment: what they prioritise, the decisions they make, the risks they spot, and how they steer the agents. Working code counts, but less.

The candidate will tell the interviewer up front that they're using this skill. We're not optimising for stealth. We're optimising for **making the candidate's competence with AI visible**.

## Assumptions about the candidate and environment

- **Claude Code only.** No other tools, IDE integrations, or multiple terminals.
- **The candidate is not an advanced AI user** and has little or no multi-agent experience. Claude handles the mechanics: it launches subagents, tracks them, and reports back. The candidate never has to manage agents, terminals, or worktrees by hand.
- **The stack is unknown.** The skill stays language- and framework-agnostic and finds out the stack from the repo.
- **The interviewer is available** for clarifying questions, and the skill should prompt the candidate to ask them.

## Guiding principle: a light process guide; the candidate leads

The skill is a light process guide, not an autopilot. The interviewer has to see the candidate's thinking, so the skill must:

- **Present options and let the candidate decide.** For each meaningful choice (priority, architecture, library, assumption), give 2–3 options with tradeoffs and a recommendation, then ask the candidate to choose. Claude never makes a product or architecture decision on its own.
- **Record every decision and its reason** in writing, so the candidate can explain it later.
- **Use soft checkpoints, not hard stops.** At natural points, Claude pauses and prompts the candidate, e.g. *"Good moment to review this diff"* or *"Want me to run the critic on the plan?"*. If the candidate says go, Claude goes.
- **Keep the output reviewable.** Small diffs, plain summaries, and pointers to exactly what the candidate should read. Code the candidate can't explain is a liability.
- **Be brief.** Every word Claude writes eats the candidate's 30 minutes. Short summaries, tables over prose, no restating the spec back.

## What the interviewer evaluates, and how the skill supports it

| Attribute | What the skill does |
|---|---|
| **Prioritisation** | Builds a scope matrix with minute estimates and a cut line (IN / STRETCH / OUT), and locks it before any design work. New priorities come in as explicit swaps, never additions. Re-checks against the clock at time checkpoints. |
| **Decision quality** | Offers options with tradeoffs, asks the candidate to choose, and logs each choice with its reason in a decision log. |
| **Spotting risk** | Finds spec gaps and sorts each one as "safe to assume" or "stop and ask" (see heuristic below). Records them in `QUESTIONS.md` and prompts the candidate to ask the interviewer about the risky ones. |
| **Steering, not just prompting** | Implementation agents get focused briefs taken from the approved plan, never the raw spec. |
| **Productive workflow** | Runs research, critic, and reviewer subagents in the background while the candidate keeps working, and keeps one tracker in `PLAN.md` that shows what every agent is doing. |
| **Code quality** | Plan → review → implement → review loop. Claude prompts the candidate to review every diff, and a reviewer agent critiques the code before each commit. |

## Invocation

- The skill's source lives in this repo. `install.sh` symlinks it to `~/.claude/skills/interview/`, so edits here take effect without reinstalling.
- The candidate starts it by typing **`/interview`** in Claude Code at the root of the interview repo. An optional argument overrides the session length, e.g. `/interview 45`.
- **The files are the state.** `PLAN.md` holds the start time, the current phase, and the tracker. If the candidate runs `/interview` again mid-session (or the context gets compacted), Claude reads `PLAN.md` and picks up where it left off instead of starting over.
- Claude tracks time by running `date` at the start and at each phase change, and tells the candidate the time used and remaining (e.g. *"12 / 30 min"*) at every checkpoint.

## Workflow (30-minute default)

Minute marks below are for 30 minutes. For other lengths, scale them proportionally.

### Phase 0: Setup (0–1 min)
- Record the start time and session length in `PLAN.md`.
- Check git status. If it isn't a repo yet, offer to `git init`. Make a baseline commit if the tree is dirty.
- Create skeletons for `PLAN.md` and `QUESTIONS.md`.

### Phase 1: Understand (1–5 min)
- Read `SPEC` in full. In parallel, launch an **explorer subagent** in the background to map the repo: stack, structure, conventions, and the build/run/test commands.
- Write a problem summary of 3–5 bullets in `PLAN.md`, in Claude's own words.
- **Checkpoint:** *"Does this match your read of the spec?"*

### Phase 2a: Triage and lock scope (5–7 min)
Lessons from rehearsal 1: the planning discussion went deep on persistence, which was never built. Seven "Musts" didn't fit, and an interviewer concern got added to scope without anything coming out.
- **Scope matrix:** each requirement gets an estimate in minutes, a running total, and a call: **IN / STRETCH / OUT**. IN must fit the build budget, about 60% of Phase 3 (≈9 min for a 30-minute session), and the arithmetic is shown.
- **Ranking rules:** core flow → dependencies of IN → hard spec invariants are IN. Costly infrastructure (persistence, auth, concurrency) is OUT by default. Variants are STRETCH or OUT.
- An OUT item that affects an IN item's data model gets one "keep possible later" line, not a design.
- **No architecture during scope.** Scope covers what and why, never how. If components, patterns, or storage come up, Claude parks them for the Approach.
- **Checkpoint (scope lock):** the candidate locks the cut line before any design discussion.

### Phase 2b: Approach and spot gaps for IN items (7–10 min)
- **Architecture overview first:** the Approach always opens with a high-level view of the components and data flow (a small diagram or 2–3 lines), showing where the new code fits into the repo.
- **Approach sketch, IN items only:** data model, interfaces, and build order, at system design altitude, in a few bullets.
- **Spec gaps** in `QUESTIONS.md`, for IN items plus any OUT item that would force a data-model change. Look actively for at least one gap that would meaningfully change the build. The article singles this out as what set the strong candidate apart.
- **In the background:** a **critic subagent** reviews the plan, assumptions, and scope arithmetic. Add **researcher subagents** only if a library or approach decision is actually open.
- **Checkpoint:** show the critic's findings **one at a time**, most severe first, so the candidate decides on each without being overwhelmed (Claude does not apply them silently). Then prompt: *"These N questions are 'stop and check'. Worth asking the interviewer now before we build."* Fold the answers into `QUESTIONS.md`.

### Keeping scope locked (all phases)
- **Parking lot:** when discussion drifts to a STRETCH or OUT item, Claude names it, parks a one-line note in `PLAN.md`, and steers back. Spend ≤1 min on it.
- **Swaps, never additions:** if an interviewer answer or critic finding raises an OUT item's priority, Claude presents a trade: cut A, cut B, or keep it OUT and design it on paper only (~2 min, written as the first "Next step"). The candidate decides, and the swap is logged.

### Phase 3: Implement in slices (10–25 min)
- Split the IN work into 2–3 thin vertical slices, each testable on its own.
- Each slice gets a **focused brief**: goal, scope, files likely touched, interfaces to honour, acceptance criteria, and what is explicitly out of scope.
- **Commit the plan, then stop.** `PLAN.md` and `QUESTIONS.md` get their own commit before any code is written, and Claude waits for the candidate's go-ahead. This is the one hard stop, and it leaves a clean plan-vs-build boundary in the history.
- **Implement slices one at a time, in the main session.** That way every edit is visible to the candidate and the interviewer and goes through a permission prompt. Keep the parallelism in the background helpers (explorer, critic, researcher, reviewer), so the candidate never has to merge or juggle anything.
- Keep the **tracker** in `PLAN.md` current: slice, agent, status, notes.
- After each slice, run the **review loop**:
  1. Run the tests, lint, and build. Report failures as they are.
  2. A **reviewer subagent** critiques the diff: correctness, edge cases, slop, consistency with repo conventions.
  3. Claude gives a short diff summary that says *where to look*: non-obvious logic, risky spots, places it guessed.
  4. Claude shows a **run-it-yourself card**, unprompted, after the first slice and again whenever the commands change. It has copy-pasteable `!`-prefixed commands for all tests, this slice's tests, a single test, and a one-line way to try the new behaviour, plus a test → requirement mapping. Running the tests themselves is how the candidate shows they understand the code, and they shouldn't have to interrupt Claude to find out how.
  5. **Candidate feedback first (hard stop):** *"Run the tests yourself and take a minute on the diff. What's your feedback?"* Claude waits and applies the candidate's feedback before showing any reviewer findings, so the candidate forms their own view of the code first.
  6. Reviewer findings are then raised **one question at a time**, most severe first; a list of five at once is overwhelming mid-interview.
  7. Keep the `README.md` **Running and testing** section in sync. Commit with a meaningful message; the git history should tell the story.
- **Time checkpoints** at about 15 min and about 22 min: compare the remaining IN estimates with the time left. If behind, propose moving an IN item to OUT. If ahead, pull the next STRETCH item. Log the decision.

### Phase 4: Wrap-up (25–30 min)
- Update `PLAN.md` with what was done, what was deferred and why, known risks, and what to do next with more time.
- Make sure `QUESTIONS.md` shows the final assumption or answer for each gap.
- Run the README's commands exactly as written, to confirm they work as the interviewer will run them.
- Give the candidate a debrief of 3–5 bullets to talk from. Bullets only, never a script.

## Artifacts

### `PLAN.md`
1. Session header: start time, length, current phase
2. Problem summary
3. Scope matrix (estimate, running total, IN / STRETCH / OUT, cut line, keep-possible-later notes)
4. Approach (IN items only), opening with a high-level architecture overview
5. Parking lot
6. Decision log: `decision | options considered | choice | why`
7. Tracker: `slice / agent | status | notes`
8. Wrap-up: done / deferred / risks / next steps

### `QUESTIONS.md`
One entry per gap:
- **Gap:** what the spec doesn't say
- **Why it matters:** what changes in the implementation depending on the answer
- **Assumption:** what we're going with
- **Risk:** low / medium / high
- **Action:** assume-and-document, or ask the interviewer (+ their answer)

### `README.md` → "Running and testing"
Created if missing and updated after every slice whose commands change. It covers prerequisites, all tests, one test file, one test case, and how to run or try the code. Only this section is edited; the rest of the README is left alone.

### Spotting-risk heuristic
- **Safe to assume** (document it and move on): cheap to reverse, local in scope, has a conventional default.
- **Stop and check** (prompt the candidate to ask the interviewer): affects the data model, a public API contract, security/privacy, data loss, or anything expensive to undo, or the spec reads two plausible ways that lead to different builds.

## Subagent roster

All subagents are launched and tracked by Claude through Claude Code's built-in subagents. The candidate never manages them directly.

| Agent | When | Runs | Job |
|---|---|---|---|
| Explorer | Phase 1 | Background | Map repo structure, conventions, build/test commands |
| Critic | Phase 2, and on request | Background | Find holes in the plan and assumptions |
| Researcher | Phase 2, only if a decision is open | Background | Compare libraries/approaches for one specific decision |
| Implementer | Phase 3 | Main session | Build one slice from a focused brief. Runs in the main session so every edit is visible and permission-prompted |
| Reviewer | Phase 3, after each slice | Background | Critique the diff before the candidate reviews it |

## Guardrails (never do)

- Never suggest or use `--dangerously-skip-permissions` or blanket auto-accept.
- Never hand the raw spec to an implementation agent.
- Never make a product or architecture decision silently. Surface it, recommend, and ask.
- Never produce a diff too large to review in a couple of minutes. Split the slice instead.
- Never claim something works without running it.
- No speculative abstraction, no gold-plating, no features the plan doesn't call for.
- Don't script the candidate's spoken explanations. Give bullets they can talk from in their own words.

## Repo layout

```
skill/interview/
  SKILL.md                     # the skill: phases, checkpoints, guardrails, subagent briefs
  templates/PLAN.md            # skeleton for PLAN.md
  templates/QUESTIONS.md       # skeleton for QUESTIONS.md
install.sh                     # symlinks skill/interview/ to ~/.claude/skills/interview/
playground/                    # rehearsal starter repo (SPEC.md + small Python package)
new-playground.sh              # copies playground/ to a fresh git repo for each rehearsal
rehearsal/INTERVIEWER_NOTES.md # planted gaps, a reasonable priority call, self-score rubric
```
