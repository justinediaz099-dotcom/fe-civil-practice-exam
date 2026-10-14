"""Areas 1-3: Mathematics and Statistics, Ethics, Engineering Economics."""
import math
from qcore import mc, num, fmt

M = "Mathematics and Statistics"
E = "Ethics and Professional Practice"
C = "Engineering Economics"

# ----------------------------------------------------------------- Mathematics
# 1. Point-to-line distance. The classic error is forgetting the denominator.
px, py, A, B, Cc = 4.0, -3.0, 3.0, 4.0, -12.0
d = abs(A * px + B * py + Cc) / math.hypot(A, B)
mc("MATH-01", M, "Analytic geometry",
   "What is the shortest distance from the point (4, -3) to the line 3x + 4y - 12 = 0?",
   d, [(abs(A * px + B * py + Cc), "You stopped at |Ax+By+C| and never divided by "
        "sqrt(A^2+B^2). That numerator is not a length."),
       (abs(A * px + B * py + Cc) / (abs(A) + abs(B)), "You divided by A+B instead of "
        "sqrt(A^2+B^2)."),
       (math.hypot(px, py), "That is the distance from the origin to the point, not "
        "from the point to the line.")],
   units="units", diff=1,
   formula="d = |Ax0 + By0 + C| / sqrt(A^2 + B^2)",
   steps=["Numerator: |3(4) + 4(-3) - 12| = |12 - 12 - 12| = 12",
          "Denominator: sqrt(3^2 + 4^2) = 5",
          "d = 12 / 5 = {}".format(fmt(d))],
   pitfall="The line must be in the form Ax + By + C = 0 before you read off A, B, C. "
           "If you are handed y = mx + b, rearrange first.")

# 2. Local maximum of a cubic.
# f(x) = x^3 - 6x^2 + 9x + 2 ; f' = 3x^2 - 12x + 9 = 3(x-1)(x-3)
f = lambda x: x ** 3 - 6 * x ** 2 + 9 * x + 2
fmax, fmin = f(1.0), f(3.0)
mc("MATH-02", M, "Single-variable calculus",
   "For f(x) = x^3 - 6x^2 + 9x + 2, what is the value of f at the local maximum?",
   fmax, [(fmin, "x = 3 is the local MINIMUM. f'' = 6x - 12 is positive there."),
          (1.0, "That is the x-location of the maximum, not the value of f there."),
          (fmax - 2.0, "You dropped the constant term. f(1) = 1 - 6 + 9 + 2, and the "
           "+2 counts.")],
   diff=2,
   formula="Critical points: f'(x) = 0. Max if f''(x) < 0, min if f''(x) > 0.",
   steps=["f'(x) = 3x^2 - 12x + 9 = 3(x - 1)(x - 3), so x = 1 and x = 3",
          "f''(x) = 6x - 12. At x = 1, f'' = -6 < 0, so x = 1 is the local max",
          "f(1) = 1 - 6 + 9 + 2 = {}".format(fmt(fmax))],
   pitfall="Answer the question that was asked. 'Where' wants x; 'what is the value' "
           "wants f(x). This single reading error is worth several points per exam.")

# 3. Definite integral as area.
area = 3.0 ** 3 / 3.0
num("MATH-03", M, "Single-variable calculus",
    "Find the area bounded by y = x^2, the x-axis, and the line x = 3.",
    area, units="square units", diff=1, tol=0.01,
    formula="A = integral from a to b of f(x) dx; integral of x^n = x^(n+1)/(n+1)",
    steps=["A = integral(0 to 3) x^2 dx = [x^3 / 3] from 0 to 3",
           "A = 27/3 - 0 = {}".format(fmt(area))],
    pitfall="Raising to n+1 and then forgetting to divide by n+1 is the single most "
            "common integration slip under time pressure.")

# 4. Dot product and the angle between vectors.
Av, Bv = (2.0, -1.0, 3.0), (1.0, 4.0, -2.0)
dot = sum(a * b for a, b in zip(Av, Bv))
magA = math.sqrt(sum(a * a for a in Av))
magB = math.sqrt(sum(b * b for b in Bv))
ang = math.degrees(math.acos(dot / (magA * magB)))
mc("MATH-04", M, "Vector operations",
   "Given A = 2i - j + 3k and B = i + 4j - 2k, what is the angle between A and B?",
   ang, [(180.0 - ang, "You dropped the negative sign on the dot product. A negative "
          "dot product means the angle is obtuse (greater than 90 degrees)."),
         (math.degrees(math.acos(12.0 / (magA * magB))), "You multiplied the component "
          "magnitudes and lost the minus signs: 2 + 4 + 6 = 12 instead of 2 - 4 - 6."),
         (90.0, "The vectors are only perpendicular if A dot B = 0. Here it is "
          "{}.".format(fmt(dot)))],
   units="degrees", diff=2,
   formula="A dot B = |A||B| cos(theta)",
   steps=["A dot B = (2)(1) + (-1)(4) + (3)(-2) = 2 - 4 - 6 = {}".format(fmt(dot)),
          "|A| = sqrt(4 + 1 + 9) = {}, |B| = sqrt(1 + 16 + 4) = {}".format(
              fmt(magA), fmt(magB)),
          "cos(theta) = {} / ({} x {}) = {}".format(fmt(dot), fmt(magA), fmt(magB),
                                                    fmt(dot / (magA * magB))),
          "theta = {} degrees".format(fmt(ang))],
   pitfall="A negative dot product is a result, not an error. Do not 'fix' it.")

# 5. Cross product magnitude = parallelogram area.
Pv, Qv = (3.0, 1.0, 0.0), (1.0, 4.0, 0.0)
cx = Pv[1] * Qv[2] - Pv[2] * Qv[1]
cy = Pv[2] * Qv[0] - Pv[0] * Qv[2]
cz = Pv[0] * Qv[1] - Pv[1] * Qv[0]
cross = math.sqrt(cx * cx + cy * cy + cz * cz)
num("MATH-05", M, "Vector operations",
    "Vectors P = 3i + j and Q = i + 4j form two sides of a parallelogram. "
    "What is its area?",
    cross, units="square units", diff=2, tol=0.01,
    formula="Area of parallelogram = |P x Q|; triangle = |P x Q| / 2",
    steps=["P x Q = (1*0 - 0*4)i - (3*0 - 0*1)j + (3*4 - 1*1)k = {}k".format(fmt(cz)),
           "|P x Q| = {}".format(fmt(cross))],
    pitfall="A TRIANGLE formed by the same two vectors is half this. Read whether the "
            "question says triangle or parallelogram.")

# 6. Sample standard deviation.
data = [12.0, 15.0, 18.0, 20.0, 25.0]
n = len(data)
mean = sum(data) / n
ss = sum((x - mean) ** 2 for x in data)
s_samp = math.sqrt(ss / (n - 1))
s_pop = math.sqrt(ss / n)
mc("MATH-06", M, "Statistics",
   "A sample of five measurements reads 12, 15, 18, 20, and 25. What is the sample "
   "standard deviation?",
   s_samp, [(s_pop, "You divided by n. The SAMPLE standard deviation divides by "
             "n - 1 (Bessel's correction)."),
            (ss / (n - 1), "That is the sample VARIANCE. Take the square root."),
            (mean, "That is the mean, not the standard deviation.")],
   diff=2,
   formula="s = sqrt( sum(xi - xbar)^2 / (n - 1) )   [sample]\n"
           "sigma = sqrt( sum(xi - mu)^2 / n )        [population]",
   steps=["xbar = 90 / 5 = {}".format(fmt(mean)),
          "Deviations: -6, -3, 0, 2, 7 -> squares 36, 9, 0, 4, 49, sum = {}".format(
              fmt(ss)),
          "s = sqrt({} / 4) = {}".format(fmt(ss), fmt(s_samp))],
   pitfall="The handbook lists both forms. 'Sample' means n - 1. The FE will offer the "
           "n version as a distractor every time.")


def _phi(z):
    """Standard normal CDF via erf - exact, no table interpolation."""
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


mu, sd, xq = 100.0, 12.0, 118.0
z = (xq - mu) / sd
p_above = 1.0 - _phi(z)
mc("MATH-07", M, "Statistics",
   "Concrete cylinder strengths are normally distributed with a mean of 100 and a "
   "standard deviation of 12. What is the probability that a cylinder exceeds 118?",
   round(p_above, 4),
   [(round(_phi(z), 4), "That is P(X < 118). The question asks for the upper tail, "
     "so subtract from 1."),
    (round(2 * (1 - _phi(z)), 4), "You doubled for two tails. Only the upper tail was "
     "asked for."),
    (round(1 - _phi(xq / sd), 4), "You used x/sigma instead of (x - mu)/sigma. "
     "Subtract the mean first.")],
   diff=2,
   formula="z = (x - mu) / sigma ; P(X > x) = 1 - Phi(z)",
   steps=["z = (118 - 100) / 12 = {}".format(fmt(z)),
          "Phi({}) = {}".format(fmt(z), fmt(_phi(z), 4)),
          "P(X > 118) = 1 - {} = {}".format(fmt(_phi(z), 4), fmt(p_above, 4))],
   pitfall="Sketch the bell curve and shade what you want before touching the table. "
           "Tail-direction errors are the #1 statistics loss on the FE.")

# 8. Least-squares slope.
xs = [1.0, 2.0, 3.0, 4.0]
ys = [2.0, 5.0, 7.0, 10.0]
k = len(xs)
Sx, Sy = sum(xs), sum(ys)
Sxy = sum(a * b for a, b in zip(xs, ys))
Sxx = sum(a * a for a in xs)
slope = (k * Sxy - Sx * Sy) / (k * Sxx - Sx ** 2)
icept = (Sy - slope * Sx) / k
mc("MATH-08", M, "Statistics",
   "A least-squares line is fit to the points (1, 2), (2, 5), (3, 7), (4, 10). "
   "What is the slope?",
   slope, [(icept, "That is the y-intercept."),
           ((ys[-1] - ys[0]) / (xs[-1] - xs[0]), "You used only the first and last "
            "points. Least squares uses all of them."),
           (Sy / Sx, "That is the ratio of the sums, which is not the regression "
            "slope.")],
   diff=2,
   formula="m = (n*Sxy - Sx*Sy) / (n*Sxx - (Sx)^2) ;  b = (Sy - m*Sx) / n",
   steps=["n = 4, Sx = {}, Sy = {}, Sxy = {}, Sxx = {}".format(
       fmt(Sx), fmt(Sy), fmt(Sxy), fmt(Sxx)),
       "m = (4*{} - {}*{}) / (4*{} - {}^2)".format(fmt(Sxy), fmt(Sx), fmt(Sy),
                                                   fmt(Sxx), fmt(Sx)),
       "m = {} / {} = {}".format(fmt(k * Sxy - Sx * Sy), fmt(k * Sxx - Sx ** 2),
                                 fmt(slope))],
   pitfall="Here the two-point shortcut gives 2.67 and least squares gives 2.6. Close "
           "enough to look right, far enough to be a wrong option.")

# 9. Combinations.
comb = math.comb(8, 3)
perm = math.perm(8, 3)
mc("MATH-09", M, "Statistics",
   "A survey crew of 3 is to be chosen from 8 available technicians. How many "
   "different crews are possible?",
   comb, [(perm, "That is PERMUTATIONS, which counts order. A crew is a set, so order "
           "does not matter."),
          (8 * 3, "Multiplying the two numbers is not a counting rule."),
          (math.comb(8, 3) * 2, "No reason to double a combination count.")],
   diff=1,
   formula="C(n, r) = n! / (r! (n - r)!) ;  P(n, r) = n! / (n - r)!",
   steps=["Order does not matter for a crew, so use combinations",
          "C(8, 3) = 8! / (3! 5!) = (8 x 7 x 6) / (3 x 2 x 1) = {}".format(fmt(comb))],
   pitfall="'Crew', 'committee', 'sample' -> combinations. 'Ranking', 'schedule', "
           "'president and vice-president' -> permutations.")

# 10. Confidence interval half-width.
xbar, s_cl, n_cl, zc = 50.0, 5.0, 25, 1.96
half = zc * s_cl / math.sqrt(n_cl)
num("MATH-10", M, "Statistics",
    "A sample of 25 specimens has a mean of 50 and a standard deviation of 5. Using "
    "z = 1.96 for 95% confidence, what is the half-width of the confidence interval "
    "on the mean?",
    half, units="", diff=2, tol=0.02,
    formula="CI = xbar +/- z * s / sqrt(n)",
    steps=["Standard error = s / sqrt(n) = 5 / sqrt(25) = {}".format(
        fmt(s_cl / math.sqrt(n_cl))),
        "Half-width = 1.96 x {} = {}".format(fmt(s_cl / math.sqrt(n_cl)), fmt(half)),
        "So the interval is 50 +/- {}".format(fmt(half))],
    pitfall="Dividing by n instead of sqrt(n) is the classic slip. For n = 25 that is "
            "an error of 5x.")

# ---------------------------------------------------------------------- Ethics
mc("ETH-01", E, "Codes of ethics",
   "A licensed civil engineer is asked by a developer to stamp and seal a set of "
   "structural drawings prepared by an out-of-state firm that the engineer did not "
   "supervise. The drawings appear competent. What is the engineer's obligation?",
   "Decline to seal them, because an engineer may only seal work performed by or "
   "under their responsible charge",
   [("Seal them, since a review confirmed the drawings are technically adequate",
     "Technical adequacy is not the test. Sealing certifies responsible charge, which "
     "a review after the fact does not create."),
    ("Seal them if the developer provides written indemnification",
     "An engineer cannot contract away a licensure obligation. Indemnity shifts money, "
     "not responsibility."),
    ("Seal them if the out-of-state firm is itself licensed somewhere",
     "Another firm's license does not transfer responsible charge to this engineer.")],
   diff=1,
   formula="Responsible charge: seal only work you performed or directly supervised.",
   steps=["Plan stamping is the textbook licensure violation",
          "The only cure is actually being in responsible charge, which cannot be "
          "created retroactively",
          "The engineer must decline, and may offer to be engaged early enough on a "
          "future project to genuinely supervise"],
   pitfall="If an ethics option contains 'indemnification', 'hold harmless', or "
           "'the client accepts the risk', it is almost always the wrong answer.")

mc("ETH-02", E, "Codes of ethics",
   "During construction an engineer discovers that an already-poured foundation has "
   "significantly less reinforcement than the design requires. The contractor asks "
   "the engineer to say nothing, promising to compensate elsewhere. What must the "
   "engineer do first?",
   "Notify the owner and the appropriate authority, because protection of public "
   "health and safety is the engineer's paramount obligation",
   [("Accept the contractor's remedy if calculations show the structure still works",
     "The engineer may well accept an engineered repair, but concealment is not "
     "available. Disclosure comes first, then the fix."),
    ("Say nothing, since the engineer owes a duty of loyalty to project participants",
     "Loyalty to a client or contractor never outranks public safety. This is the "
     "first canon."),
    ("Resign from the project to avoid being implicated",
     "Walking away leaves the hazard in place and un-reported. Resignation is not "
     "disclosure.")],
   diff=1,
   formula="First canon: hold paramount the safety, health, and welfare of the public.",
   steps=["Rank the duties: public safety outranks client, employer, and contractor",
          "A known structural deficiency is a public-safety matter",
          "Disclose to the owner and the authority having jurisdiction; then evaluate "
          "an engineered repair"],
   pitfall="'Paramount' is a ranking word. When an ethics question pits safety against "
           "anything else, safety wins with no balancing test.")

mc("ETH-03", E, "Professional liability",
   "An engineer whose practice is entirely in transportation design is offered a "
   "structural seismic retrofit commission. What is the most appropriate response?",
   "Accept only if qualified by education or experience in that specialty, or "
   "associate with a qualified engineer who takes responsible charge of that work",
   [("Accept, because a professional engineer's license is not limited by discipline",
     "Most licenses are general in law but the codes of ethics restrict practice to "
     "areas of actual competence."),
    ("Accept and learn the specialty during the project, billing the research time",
     "Self-education on a live project puts the public at risk and bills the client "
     "for your training."),
    ("Decline in all cases, since changing specialty is not permitted",
     "Too absolute. Associating with a qualified engineer is a recognized and proper "
     "route.")],
   diff=2,
   formula="Perform services only in your areas of competence.",
   steps=["The license may be general, but the ethical limit is demonstrated "
          "competence",
          "Two acceptable paths: be genuinely qualified, or associate with someone who "
          "is and who takes responsible charge",
          "Either way the public gets a competent engineer on the seismic scope"],
   pitfall="Watch for 'in all cases' and 'never'. Correct ethics answers usually allow "
           "a legitimate path forward.")

mc("ETH-04", E, "Contracts and contract law",
   "An engineer serving as an independent reviewer for a city holds a small ownership "
   "stake in the firm whose design is under review. What is required?",
   "Disclose the financial interest in writing to the city, and withdraw unless the "
   "city knowingly consents",
   [("Nothing, provided the ownership stake is too small to influence judgment",
     "The engineer does not get to decide what is material. Disclosure lets the "
     "client decide."),
    ("Sell the stake quietly and continue the review without mentioning it",
     "Divestment does not erase the conflict during the period it existed, and "
     "concealment compounds it."),
    ("Continue, because a reviewer's duty runs to the public rather than the city",
     "The public duty does not cancel the disclosure duty. Both apply.")],
   diff=2,
   formula="Disclose all known or potential conflicts of interest promptly and in "
           "writing.",
   steps=["Any financial interest in the reviewed party is a conflict",
          "The remedy is disclosure to the client, in writing",
          "The client, not the engineer, decides whether to waive it"],
   pitfall="Conflict-of-interest answers are about PROCESS, not magnitude. 'Too small "
           "to matter' is never the correct reasoning.")

mc("ETH-05", E, "Licensure",
   "Which activity most clearly requires a professional engineering license?",
   "Preparing and sealing structural calculations for a public building",
   [("Operating surveying equipment as a crew member under a licensed surveyor",
     "Working under direct supervision is specifically how unlicensed staff may "
     "contribute."),
    ("Teaching an undergraduate statics course",
     "Teaching is generally exempt; it is not the practice of engineering for a "
     "client."),
    ("Selling manufactured steel connectors with published load tables",
     "This typically falls under the industrial or manufacturer exemption.")],
   diff=1,
   formula="Licensure attaches to offering or performing engineering services for the "
           "public, and to sealing documents.",
   steps=["Look for the combination of public safety plus a document that gets sealed",
          "Structural calculations for a public building hit both",
          "The other three are recognized exemption categories: supervised work, "
          "teaching, and manufacturing"],
   pitfall="Learn the exemption families (industrial, supervised, teaching, federal "
           "employment). FE licensure questions are almost always testing one of them.")

# ------------------------------------------------------- Engineering Economics
# 1. Present worth of a uniform series.
Aann, iann, nann = 10000.0, 0.06, 8
PA = (1 - (1 + iann) ** -nann) / iann
PW = Aann * PA
mc("ECON-01", C, "Time value of money",
   "A maintenance contract costs $10,000 at the end of each year for 8 years. At an "
   "interest rate of 6%, what is the present worth?",
   round(PW, 0),
   [(round(Aann * nann, 0), "You summed the payments without discounting. $80,000 is "
     "the undiscounted total, not the present worth."),
    (round(Aann * ((1 + iann) ** nann - 1) / iann, 0), "That is the FUTURE worth "
     "(F/A), not the present worth (P/A)."),
    (round(Aann / iann, 0), "That is a perpetuity (A/i), which assumes payments "
     "forever rather than 8 years.")],
   units="$", diff=2,
   formula="(P/A, i, n) = [1 - (1 + i)^-n] / i",
   steps=["(P/A, 6%, 8) = [1 - 1.06^-8] / 0.06 = {}".format(fmt(PA)),
          "PW = 10,000 x {} = ${}".format(fmt(PA), fmt(PW, 0))],
   pitfall="Confirm whether payments land at the END of each period (ordinary annuity, "
           "which these factors assume) or the BEGINNING (annuity due, multiply by "
           "1 + i).")

# 2. Single-payment compound amount.
P2, i2, n2 = 25000.0, 0.07, 10
F2 = P2 * (1 + i2) ** n2
num("ECON-02", C, "Time value of money",
    "What is the future worth of $25,000 invested for 10 years at 7% compounded "
    "annually?",
    round(F2, 0), units="$", diff=1, tol=0.01,
    formula="F = P (1 + i)^n",
    steps=["(1.07)^10 = {}".format(fmt((1 + i2) ** n2, 4)),
           "F = 25,000 x {} = ${}".format(fmt((1 + i2) ** n2, 4), fmt(F2, 0))],
    pitfall="Simple interest would give 25,000(1 + 0.07*10) = $42,500. The FE means "
            "compound interest unless it says otherwise.")

# 3. Equivalent uniform annual cost with salvage.
P3, S3, i3, n3 = 80000.0, 10000.0, 0.10, 5
AP = i3 * (1 + i3) ** n3 / ((1 + i3) ** n3 - 1)
AF = i3 / ((1 + i3) ** n3 - 1)
EUAC = P3 * AP - S3 * AF
mc("ECON-03", C, "Analyses",
   "A machine costs $80,000, has a 5-year life, and a salvage value of $10,000. At "
   "10% interest, what is the equivalent uniform annual cost?",
   round(EUAC, 0),
   [(round(P3 * AP, 0), "You ignored the salvage credit. Salvage reduces the annual "
     "cost via (A/F)."),
    (round(P3 * AP + S3 * AF, 0), "Sign error: salvage is income, so it is SUBTRACTED "
     "from the annual cost."),
    (round((P3 - S3) / n3, 0), "That is straight-line depreciation, which ignores the "
     "time value of money entirely.")],
   units="$/yr", diff=3,
   formula="EUAC = P(A/P, i, n) - S(A/F, i, n)",
   steps=["(A/P, 10%, 5) = 0.10(1.1^5) / (1.1^5 - 1) = {}".format(fmt(AP, 4)),
          "(A/F, 10%, 5) = 0.10 / (1.1^5 - 1) = {}".format(fmt(AF, 4)),
          "EUAC = 80,000({}) - 10,000({}) = ${}".format(fmt(AP, 4), fmt(AF, 4),
                                                        fmt(EUAC, 0))],
   pitfall="(A/P) and (A/F) differ by exactly i: A/P = A/F + i. Use that as a "
           "10-second check on both factors.")

# 4. Break-even volume.
FC, vc, pr = 50000.0, 15.0, 40.0
be = FC / (pr - vc)
num("ECON-04", C, "Analyses",
    "A plant has fixed costs of $50,000 per year, a variable cost of $15 per unit, and "
    "sells units at $40. How many units per year must it sell to break even?",
    be, units="units/yr", diff=1, tol=0.01,
    formula="Break-even quantity = Fixed cost / (price - variable cost)",
    steps=["Contribution margin per unit = 40 - 15 = ${}".format(fmt(pr - vc)),
           "Q = 50,000 / 25 = {} units".format(fmt(be, 0))],
    pitfall="Divide by the MARGIN, not by the price. Using 50,000/40 gives 1,250 and "
            "will be on the answer list.")

# 5. Benefit-cost ratio.
ben, cost = 1200000.0, 800000.0
bcr = ben / cost
mc("ECON-05", C, "Analyses",
   "A public project has benefits with a present worth of $1,200,000 and costs with a "
   "present worth of $800,000. What is the benefit-cost ratio, and is the project "
   "justified?",
   "{} - justified, because B/C is greater than 1".format(fmt(bcr)),
   [("{} - not justified".format(fmt(cost / ben)), "You inverted the ratio. Benefits "
     "go on top."),
    ("{} - justified".format(fmt(ben - cost, 0)), "That is net present worth in "
     "dollars, not a ratio."),
    ("{} - marginal, so defer the project".format(fmt(bcr)), "The ratio is correct but "
     "the conclusion is not. Anything above 1.0 is economically justified.")],
   diff=1,
   formula="B/C = PW(benefits) / PW(costs). Accept if B/C >= 1.",
   steps=["B/C = 1,200,000 / 800,000 = {}".format(fmt(bcr)),
          "{} > 1.0, so the project is economically justified".format(fmt(bcr))],
   pitfall="Conventional B/C puts disbenefits in the numerator as a subtraction, while "
           "modified B/C moves annual O&M to the numerator. Both appear on the FE.")

# 6. Simple payback period.
inv, savings = 120000.0, 32000.0
pb = inv / savings
num("ECON-06", C, "Cost",
    "Equipment costing $120,000 saves $32,000 per year. What is the simple payback "
    "period, ignoring interest?",
    pb, units="years", diff=1, tol=0.02,
    formula="Simple payback = initial cost / annual net savings",
    steps=["Payback = 120,000 / 32,000 = {} years".format(fmt(pb))],
    pitfall="Simple payback ignores interest and anything after payback. A discounted "
            "payback at a nonzero rate is always LONGER.")

# 7. Expected value under uncertainty.
p_fail, loss, p_ok, gain = 0.30, -20000.0, 0.70, 50000.0
ev = p_fail * loss + p_ok * gain
mc("ECON-07", C, "Uncertainty",
   "A bid has a 30% chance of losing $20,000 and a 70% chance of earning $50,000. "
   "What is the expected value?",
   round(ev, 0),
   [(round((loss + gain) / 2, 0), "You averaged the outcomes instead of weighting them "
     "by probability."),
    (round(p_ok * gain, 0), "You kept only the favorable branch. The loss branch is "
     "part of the expectation."),
    (round(p_fail * loss + p_ok * gain + loss, 0), "The loss is double-counted.")],
   units="$", diff=2,
   formula="E[X] = sum( p_i * x_i )",
   steps=["E = 0.30(-20,000) + 0.70(50,000)",
          "E = -6,000 + 35,000 = ${}".format(fmt(ev, 0)),
          "Positive expected value, so the bid is favorable on average"],
   pitfall="Probabilities must sum to 1.0. If they do not, you have missed an outcome "
           "branch.")
