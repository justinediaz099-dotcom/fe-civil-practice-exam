"""Build and validate the question bank, then emit docs/bank.js.

Run:  python3 make_bank.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import qcore                                 # noqa: E402
import a01_math_ethics_econ                   # noqa: E402,F401
import a02_statics_dyn_mech                   # noqa: E402,F401
import a03_materials_fluids_survey            # noqa: E402,F401
import a04_water_structural                   # noqa: E402,F401
import a05_geo_transpo_construction           # noqa: E402,F401

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "docs", "bank.js")
os.makedirs(os.path.dirname(OUT), exist_ok=True)

meta = qcore.dump(OUT)

print("wrote {} ({:,} bytes)".format(os.path.normpath(OUT), os.path.getsize(OUT)))
print("{} questions total\n".format(meta["count"]))
print("{:<48} {:>5} {:>7} {:>6}".format("AREA", "HAVE", "EXAM", "OK?"))
low_sum = high_sum = have_sum = 0
for a in meta["areas"]:
    low_sum += a["low"]
    high_sum += a["high"]
    have_sum += a["have"]
    ok = "yes" if a["have"] >= a["low"] else "SHORT"
    print("{:<48} {:>5} {:>3}-{:<3} {:>6}".format(
        a["name"][:48], a["have"], a["low"], a["high"], ok))
print("\nblueprint total range: {} to {}".format(low_sum, high_sum))
print("bank size: {} -> a {}-question exam is {}".format(
    have_sum, qcore.EXAM_TOTAL,
    "feasible" if low_sum <= qcore.EXAM_TOTAL <= min(high_sum, have_sum)
    else "NOT FEASIBLE"))

# Independent re-check of every numeric answer's self-consistency: the solution steps
# must mention the answer, so a formula edited without updating its narration is caught.
missing_narr = []
for q in qcore._BANK:
    if q["kind"] != "num":
        continue
    shown = " ".join(q["steps"]).replace(",", "")
    a = q["answer"]
    cands = {"{:.0f}".format(a), "{:.1f}".format(a), "{:.2f}".format(a),
             "{:.3f}".format(a), "{:.4f}".format(a)}
    cands |= {c.rstrip("0").rstrip(".") for c in list(cands)}
    if not any(c and c in shown for c in cands):
        missing_narr.append((q["id"], a))
if missing_narr:
    print("\nWARNING - numeric answer not visible in its own worked solution:")
    for qid, a in missing_narr:
        print("   {} (answer {})".format(qid, a))
else:
    print("\nall numeric answers appear in their own worked solutions")
