# FE Civil Practice Exam

An interactive 110-question FE Civil practice exam that shows the correct answer right
after each selection, explains the specific mistake behind a wrong option, and scores
the whole sitting at the end.

## Using it

Open `docs/index.html` in any browser. Nothing to install, no internet needed. Keep
`index.html` and `bank.js` in the same folder — the page loads the question bank from
its sibling file.

To share it with someone, either send them the `docs` folder, or publish `docs/` with
GitHub Pages and send the link.

## What it does

- **110 questions, blueprint-weighted.** Question counts per knowledge area match the
  NCEES FE Civil CBT exam specification effective July 2020, verified against the
  published low/high range for all 14 areas.
- **350-minute timer**, the real exam's 6 hours less the tutorial and scheduled break.
  Pausable. It keeps counting past zero rather than locking you out, since this is a
  study tool.
- **Two feedback modes.** "Show the answer right after I choose" (the default, best for
  learning) or "Hold all answers until the end" (exam conditions).
- **Two question orders.** "Grouped by knowledge area" (the default) walks the 14 areas
  in specification order, one contiguous section at a time, with a `Section 4 of 14 · 3
  of 9 in this area` counter in the question header. "Shuffled" interleaves every area
  at random, which is harder and trains topic-switching. Either way the questions
  *within* a section are shuffled, so no two sittings are identical.
- **Wrong-answer diagnosis.** Every distractor carries the named mistake it represents,
  so a wrong choice tells you *which* error you made — dividing by `n` instead of
  `n - 1`, using `I` instead of `J`, reading a centre of pressure as a centroid.
- **Worked solution, formula, and a pitfall note** on every single question.
- **Good-luck dialog before the clock starts.** It restates the settings she picked and
  holds the timer until she presses Begin, so opening the page never silently burns
  exam time.
- **Results by knowledge area, weakest first**, banded red / amber / green: under 55%
  is "Needs work", 55&ndash;79% is "Review", 80%+ is "Strong". Each band carries a word
  and a glyph as well as the colour, so it still reads correctly in grayscale or with
  colour-vision deficiency.
- **The specification table doubles as the study plan.** Before the first attempt its
  third column shows how many questions each area will contribute. Afterwards it shows
  the last attempt's per-area score in the same red/amber/green bands, so the areas
  needing work are visible the moment she opens the page.
- **Review list** of everything missed, with full solutions.
- **Progress survives a reload or a closed tab.** Answers are written to browser
  storage the instant one is chosen; the clock is saved every 10 seconds and again on
  close. Reopening the page offers "Resume exam" with the answered count and time
  remaining. Starting a *new* exam while one is unfinished asks for confirmation first,
  since an in-progress 110-question attempt is hours of work.
- **The clock counts time spent with the page open and running, not wall-clock time.**
  Closing the tab stops it; a refresh can only ever hand back up to 10 seconds. Storage
  is per browser and per file location, so a private window or moving the folder starts
  fresh.
- **Saving results to share.** On finishing, the Save-as-PDF dialog opens on its own;
  a "Save a copy to share" card and a "Download a copy" button are there if it is
  dismissed. The download is a standalone HTML file with every worked solution expanded.
  The print stylesheet forces the light palette even in dark mode &mdash; browsers drop
  background colours when printing, so a dark theme would otherwise produce a
  white-on-white page.
- **Results survive the tab closing.** The finished attempt is persisted in full, so
  "Open my last results" on the front page restores the score, the area breakdown, and
  every missed question with its solution.
- Attempt history is kept across sittings.

## Privacy

There is no backend. The app makes no network requests of any kind &mdash; no `fetch`,
no analytics, no external resources beyond its own `bank.js`. Every answer, score, and
timer value lives in three `localStorage` keys in the browser that took the exam.

This means progress is **per browser profile**, not per person and not per IP: the same
person on two devices has two separate sets, and two people sharing one browser profile
would share one. Nobody can see anyone else's results, including whoever published the
site. The only way to share results is for the examinee to send the PDF or the
downloaded copy.
- Also offers a 30-question short set and single-area drills.

Keyboard: `1`–`4` or `A`–`D` to choose, `Enter` next, arrows to move, `f` to flag.

## Scope and honesty about it

- **The questions are original.** The NCEES practice exam PDF is copyrighted and its
  own permission flags deny copy/extraction (`/P -1340`), so nothing was taken from it.
  Only the public *exam specification* — the list of areas and question counts — shapes
  this trainer.
- **About a quarter of the items are numeric entry** rather than multiple choice. That
  is deliberate: the real CBT mixes both, and a trainer that is 100% multiple choice
  teaches students to work backwards from the options. Numeric answers are graded with
  a 1–2% tolerance.
- **70% is a study benchmark, not a passing score.** NCEES sets the real cut score by a
  criterion-referenced process, does not publish it, and reports only pass or fail.
- The bank holds 125 questions, so each 110-question sitting draws a slightly different
  mix. It is not large enough to avoid repeats across many attempts — treat repeat
  sittings as review, and lean on the per-area breakdown to decide what to study.

## Rebuilding the bank

Questions live in `build/` as Python, one module per group of knowledge areas.

```bash
cd build
python3 make_bank.py      # validates everything, writes ../docs/bank.js
```

Two rules the build enforces, and the reason for each:

1. **No numeric answer is ever typed as a literal.** Every answer and every distractor
   is computed from the stated inputs. A wrong answer in a study tool is worse than no
   tool, so the arithmetic cannot drift from the question text.
2. **Every distractor must carry a named mistake.** `make_bank.py` rejects a question
   whose options lack explanations, lack a worked solution, lack a formula reference, or
   contain two options that round to the same displayed value — that last check caught
   nine collisions where a "wrong" option computed to exactly the right answer.

It also reports whether the bank can still fill a 110-question exam inside the
blueprint ranges, and warns if a numeric answer no longer appears in its own worked
solution.

## Layout

```
build/      question source + validator  (edit here)
docs/       index.html + bank.js         (ship/share this)
preview/    screenshots
```
