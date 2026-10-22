"""Question model for the FE Civil trainer.

Design rule that matters: **no numeric answer is ever typed as a literal.** Every
answer and every distractor is COMPUTED from the stated inputs, so the bank cannot
drift from its own arithmetic. A wrong answer in a study tool is worse than no tool.

The second rule: a distractor is only allowed to exist if it has a *named mistake*
attached (`why`). That is what lets the app tell the student which error they made
instead of just "incorrect". Random plausible numbers teach nothing.
"""
import json
import math

import mathfmt

AREAS = [
    # (name, short, exam-blueprint low, high) - from FE-Civil-CBT-specs-1.pdf
    ("Mathematics and Statistics", "Math", 8, 12),
    ("Ethics and Professional Practice", "Ethics", 4, 6),
    ("Engineering Economics", "Econ", 5, 8),
    ("Statics", "Statics", 8, 12),
    ("Dynamics", "Dynamics", 4, 6),
    ("Mechanics of Materials", "Mech Mat", 7, 11),
    ("Materials", "Materials", 5, 8),
    ("Fluid Mechanics", "Fluids", 6, 9),
    ("Surveying", "Surveying", 6, 9),
    ("Water Resources and Environmental Engineering", "Water/Env", 10, 15),
    ("Structural Engineering", "Structural", 10, 15),
    ("Geotechnical Engineering", "Geotech", 10, 15),
    ("Transportation Engineering", "Transpo", 9, 14),
    ("Construction Engineering", "Construction", 8, 12),
]
AREA_NAMES = [a[0] for a in AREAS]
EXAM_TOTAL = 110

_BANK = []


def sig(x, n=3):
    """Round to n significant figures. Keeps choice lists from leaking the answer
    through spurious precision - a distractor written to 6 decimals and an answer
    written to 2 is a free giveaway."""
    if x == 0:
        return 0.0
    return round(x, -int(math.floor(math.log10(abs(x)))) + (n - 1))


def fmt(x, nd=None):
    """Human-readable number. Chooses decimals from magnitude unless told."""
    if isinstance(x, str):
        return x
    if nd is None:
        a = abs(x)
        nd = 0 if a >= 1000 else 1 if a >= 100 else 2 if a >= 10 else 3 if a >= 1 else 4
    s = "{:,.{}f}".format(x, nd)
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s or "0"


class Q:
    """One question. `kind` is 'mc' (multiple choice) or 'num' (numeric entry).

    The real FE CBT mixes both, so a trainer that is 100% multiple choice teaches
    students to reverse-engineer from the options - a skill that fails them on the
    numeric-entry items.
    """

    def __init__(self, qid, area, topic, prompt, kind="mc", diff=2,
                 answer=None, choices=None, units="", tol=0.02,
                 steps=(), formula="", note="", pitfall=""):
        assert area in AREA_NAMES, "unknown area: {}".format(area)
        assert kind in ("mc", "num")
        self.d = dict(id=qid, area=area, topic=topic, prompt=prompt, kind=kind,
                      diff=diff, units=units, steps=list(steps), formula=formula,
                      note=note, pitfall=pitfall)
        if kind == "num":
            assert answer is not None, qid
            self.d["answer"] = float(answer)
            self.d["tol"] = tol          # fractional tolerance
        else:
            # choices: list of (text_or_value, why_wrong_or_None). Exactly one None.
            assert choices, qid
            opts = []
            for val, why in choices:
                opts.append(dict(text=val if isinstance(val, str) else fmt(val),
                                 why=why))
            correct = [i for i, o in enumerate(opts) if o["why"] is None]
            assert len(correct) == 1, "{}: needs exactly one correct choice".format(qid)
            self.d["choices"] = opts
            self.d["answer"] = correct[0]
        _BANK.append(self.d)


def mc(qid, area, topic, prompt, correct, wrong, units="", diff=2,
       steps=(), formula="", note="", pitfall="", shuffle_seed=None):
    """Convenience: `correct` is a value/str, `wrong` is a list of (value, why)."""
    ch = [(correct, None)] + [(v, w) for v, w in wrong]
    # Sort numerically when all options are numbers so the option order carries no
    # signal about which one the author wrote first.
    try:
        ch.sort(key=lambda c: float(c[0]))
    except (TypeError, ValueError):
        pass
    return Q(qid, area, topic, prompt, kind="mc", diff=diff, choices=ch,
             units=units, steps=steps, formula=formula, note=note, pitfall=pitfall)


def num(qid, area, topic, prompt, answer, units="", tol=0.02, diff=2,
        steps=(), formula="", note="", pitfall=""):
    return Q(qid, area, topic, prompt, kind="num", diff=diff, answer=answer,
             units=units, tol=tol, steps=steps, formula=formula, note=note,
             pitfall=pitfall)


def dump(path):
    """Validate the whole bank, then write it as a JS module (works over file://,
    unlike fetch() against a .json sibling)."""
    ids = [q["id"] for q in _BANK]
    dupes = {i for i in ids if ids.count(i) > 1}
    assert not dupes, "duplicate ids: {}".format(dupes)

    for q in _BANK:
        assert q["steps"], "{} has no worked solution".format(q["id"])
        assert q["formula"], "{} has no formula reference".format(q["id"])
        if q["kind"] == "mc":
            assert len(q["choices"]) >= 3, q["id"]
            texts = [c["text"] for c in q["choices"]]
            assert len(set(texts)) == len(texts), \
                "{}: duplicate choice text {}".format(q["id"], texts)

    by_area = {}
    for q in _BANK:
        by_area.setdefault(q["area"], []).append(q["id"])

    meta = dict(
        areas=[dict(name=n, short=s, low=lo, high=hi, have=len(by_area.get(n, [])))
               for n, s, lo, hi in AREAS],
        exam_total=EXAM_TOTAL,
        exam_minutes=350,   # 6h total less the tutorial and scheduled break
        count=len(_BANK),
    )
    missing = [a["name"] for a in meta["areas"] if a["have"] == 0]
    assert not missing, "areas with no questions: {}".format(missing)

    # Math typography is applied once, here, so the Python sources stay greppable ASCII
    # while the shipped bank carries real symbols (x̄, √, ², π, σ).
    for q in _BANK:
        mathfmt.prettify_question(q)

    payload = dict(meta=meta, questions=_BANK)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("window.FE_BANK = ")
        json.dump(payload, fh, ensure_ascii=False, separators=(",", ":"))
        fh.write(";\n")
    return meta
