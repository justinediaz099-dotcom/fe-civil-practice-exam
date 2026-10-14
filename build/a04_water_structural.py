"""Areas 10-11: Water Resources and Environmental Engineering, Structural Engineering."""
import math
from qcore import mc, num, fmt

W = "Water Resources and Environmental Engineering"
ST = "Structural Engineering"
g = 9.81
gam_w = 9.81     # kN/m^3

# ----------------------------------------- Water Resources and Environmental
Cr, ir, Ar = 0.60, 50.0, 5.0        # runoff coeff, mm/hr, hectares
Qr = Cr * ir * Ar / 360.0
mc("WAT-01", W, "Basic hydrology",
   "Using the rational method in SI units, find the peak runoff from a 5 hectare "
   "catchment with a runoff coefficient of 0.60 and a rainfall intensity of 50 mm/hr.",
   Qr, [(Cr * ir * Ar, "You omitted the 360 conversion. C*i*A with mm/hr and hectares "
         "is not m^3/s."),
        (ir * Ar / 360.0, "You dropped the runoff coefficient. Not all rainfall becomes "
         "runoff."),
        (Cr * ir * Ar / 3600.0, "The SI constant is 360, not 3600.")],
   units="m^3/s", diff=2,
   formula="SI: Q(m^3/s) = C i A / 360, with i in mm/hr and A in hectares.\n"
           "US: Q(cfs) = C i A, with i in in/hr and A in acres.",
   steps=["Q = 0.60(50)(5) / 360",
          "Q = 150 / 360 = {} m^3/s".format(fmt(Qr, 4))],
   pitfall="The US form needs NO conversion constant because 1 acre-inch per hour is "
           "almost exactly 1 cfs. The SI form needs 360. Know which units you are in.")

bch, ych, nch, Sch = 3.0, 1.2, 0.015, 0.002
Ach = bch * ych
Pch = bch + 2 * ych
Rch = Ach / Pch
Vch = (1.0 / nch) * Rch ** (2.0 / 3.0) * math.sqrt(Sch)
Qch = Ach * Vch
mc("WAT-02", W, "Basic hydraulics",
   "A rectangular channel 3 m wide flows 1.2 m deep. Manning's n is 0.015 and the bed "
   "slope is 0.002. What is the discharge?",
   Qch, [(Ach * (1.0 / nch) * (Ach / (bch + ych)) ** (2.0 / 3.0) * math.sqrt(Sch),
          "Your wetted perimeter is wrong. An open rectangular channel wets the bed "
          "plus BOTH sides: P = b + 2y."),
         (Ach * (1.0 / nch) * ych ** (2.0 / 3.0) * math.sqrt(Sch), "You used depth as "
          "the hydraulic radius. R = A/P, which is smaller than y here."),
         (Ach * (1.0 / nch) * Rch ** (2.0 / 3.0) * Sch, "You forgot the square root on "
          "the slope.")],
   units="m^3/s", diff=3,
   formula="SI: V = (1/n) R^(2/3) S^(1/2) ;  US: V = (1.486/n) R^(2/3) S^(1/2) ;  "
           "R = A / P",
   steps=["A = 3(1.2) = {} m^2".format(fmt(Ach)),
          "P = 3 + 2(1.2) = {} m, so R = {} / {} = {} m".format(
              fmt(Pch), fmt(Ach), fmt(Pch), fmt(Rch)),
          "V = (1/0.015)({})^(2/3)(0.002)^(1/2) = {} m/s".format(fmt(Rch), fmt(Vch)),
          "Q = {}({}) = {} m^3/s".format(fmt(Ach), fmt(Vch), fmt(Qch))],
   pitfall="The 1.486 (often written 1.49) coefficient belongs ONLY to US customary "
           "units. Using it in SI inflates your answer by 49%.")

Qp, Hp, eff = 0.10, 25.0, 0.75
Pwr = gam_w * Qp * Hp / eff
mc("WAT-03", W, "Pumps",
   "A pump delivers 0.10 m^3/s against a total head of 25 m at 75% efficiency. What "
   "input power is required?",
   Pwr, [(gam_w * Qp * Hp, "That is the WATER power (useful output). Divide by "
          "efficiency to get the required input."),
         (gam_w * Qp * Hp * eff, "You multiplied by efficiency. Input power is always "
          "LARGER than output power."),
         (Qp * Hp / eff, "The specific weight of water is missing.")],
   units="kW", diff=2,
   formula="Water power = gamma Q H ;  Input power = gamma Q H / efficiency",
   steps=["Water power = 9.81(0.10)(25) = {} kW".format(fmt(gam_w * Qp * Hp)),
          "Input power = {} / 0.75 = {} kW".format(fmt(gam_w * Qp * Hp), fmt(Pwr))],
   pitfall="Efficiency always makes the required input BIGGER. If your answer shrank, "
           "you multiplied where you should have divided.")

Qin, Qout, dur = 1.2, 0.5, 30.0 * 60.0
Vstor = (Qin - Qout) * dur
num("WAT-04", W, "Stormwater",
    "A detention basin receives a steady inflow of 1.2 m^3/s while releasing "
    "0.5 m^3/s for 30 minutes. What storage volume accumulates?",
    Vstor, units="m^3", diff=1, tol=0.01,
    formula="Storage = (inflow - outflow) x time   [continuity / routing]",
    steps=["Net inflow = 1.2 - 0.5 = {} m^3/s".format(fmt(Qin - Qout)),
           "Duration = 30 min = {} s".format(fmt(dur, 0)),
           "Volume = 0.7({}) = {} m^3".format(fmt(dur, 0), fmt(Vstor, 0))],
    pitfall="Convert minutes to seconds before multiplying by a m^3/s flow. Forgetting "
            "the 60 is a factor-of-60 error, not a rounding error.")

kperm, igrad, Aseep, poros = 2.5e-4, 0.015, 200.0, 0.30
Qseep = kperm * igrad * Aseep
vdarcy = kperm * igrad
vseep = vdarcy / poros
mc("WAT-05", W, "Groundwater",
   "An aquifer has a hydraulic conductivity of 2.5e-4 m/s and a hydraulic gradient of "
   "0.015. For a cross-sectional area of 200 m^2, what is the discharge?",
   round(Qseep, 6),
   [(round(kperm * Aseep, 6), "You omitted the gradient. Flow is driven by the head "
     "gradient."),
    (round(vseep * Aseep, 6), "You used the SEEPAGE velocity. Darcy's law uses the "
     "bulk (discharge) velocity for Q."),
    (round(kperm * igrad / Aseep, 6), "Area multiplies, it does not divide.")],
   units="m^3/s", diff=2,
   formula="Darcy: Q = k i A ;  v_Darcy = k i ;  v_seepage = k i / n",
   steps=["v_Darcy = 2.5e-4(0.015) = {} m/s".format(fmt(vdarcy, 8)),
          "Q = {}(200) = {} m^3/s = {} L/s".format(fmt(vdarcy, 8), fmt(Qseep, 6),
                                                   fmt(Qseep * 1000.0, 3)),
          "For reference the seepage velocity is {} / 0.30 = {} m/s".format(
              fmt(vdarcy, 8), fmt(vseep, 8))],
   pitfall="Darcy velocity is fictitious (flow spread over the whole area). Actual "
           "particle travel uses SEEPAGE velocity = v/n, which is always larger.")

Vtank, Qday = 500.0, 2000.0
hrt_d = Vtank / Qday
hrt_h = hrt_d * 24.0
num("WAT-06", W, "Water and wastewater treatment",
    "A treatment tank has a volume of 500 m^3 and receives 2000 m^3/day. What is the "
    "hydraulic residence time in hours?",
    hrt_h, units="hours", diff=1, tol=0.01,
    formula="HRT = Volume / Flow rate",
    steps=["HRT = 500 / 2000 = {} day".format(fmt(hrt_d)),
           "x 24 = {} hours".format(fmt(hrt_h))],
    pitfall="Check the unit the question wants. The same tank is 0.25 day, 6 hours, or "
            "360 minutes, and at least two of those will be on the answer list.")

bod_in, bod_out = 220.0, 20.0
rem = (bod_in - bod_out) / bod_in * 100
mc("WAT-07", W, "Water quality",
   "A wastewater plant reduces BOD from 220 mg/L to 20 mg/L. What is the removal "
   "efficiency?",
   round(rem, 1),
   [(round((bod_in - bod_out) / bod_out * 100, 1), "You divided by the EFFLUENT "
     "concentration. Efficiency is referenced to the influent."),
    (round(bod_out / bod_in * 100, 1), "That is the fraction REMAINING, not the "
     "fraction removed."),
    (round(bod_in - bod_out, 1), "That is the concentration removed in mg/L, not a "
     "percentage.")],
   units="%", diff=1,
   formula="Removal (%) = (C_in - C_out) / C_in x 100",
   steps=["Removed = 220 - 20 = {} mg/L".format(fmt(bod_in - bod_out)),
          "Efficiency = 200 / 220 x 100 = {}%".format(fmt(rem))],
   pitfall="Secondary treatment is typically specified around 85 to 95% BOD removal. "
           "An answer near 1000% means you used the effluent as the reference.")

Qcl, dose = 4000.0, 2.5
masscl = Qcl * dose / 1000.0
num("WAT-08", W, "Water and wastewater treatment",
    "A plant treating 4000 m^3/day applies a chlorine dose of 2.5 mg/L. What mass of "
    "chlorine is needed per day?",
    masscl, units="kg/day", diff=2, tol=0.01,
    formula="Mass (kg/d) = Q(m^3/d) x dose(mg/L) / 1000",
    steps=["1 mg/L in 1 m^3 is 1 gram, since 1 m^3 = 1000 L",
           "Mass = 4000 x 2.5 = {} g/day".format(fmt(Qcl * dose, 0)),
           "= {} kg/day".format(fmt(masscl))],
    pitfall="Memorize the SI shortcut: Q(m^3/d) x C(mg/L) = grams/day. In US units it "
            "is lb/day = Q(MGD) x C(mg/L) x 8.34.")

ca_mg, eq_ca, eq_caco3 = 80.0, 20.04, 50.04
hard = ca_mg * eq_caco3 / eq_ca
mc("WAT-09", W, "Water quality",
   "Water contains 80 mg/L of calcium ion (Ca2+, atomic mass 40.08). Expressed as "
   "CaCO3 (molar mass 100.09), what is the hardness?",
   round(hard, 0),
   [(round(ca_mg * eq_ca / eq_caco3, 0), "You inverted the equivalent-weight ratio. "
     "Converting to CaCO3 always INCREASES the number, because CaCO3 is heavier per "
     "equivalent."),
    (round(ca_mg * eq_caco3 / 40.08, 0), "You used calcium's full molar mass instead "
     "of its equivalent weight. Divide by the charge of 2 first."),
    (ca_mg, "No conversion was applied.")],
   units="mg/L as CaCO3", diff=3,
   formula="mg/L as CaCO3 = mg/L of ion x (equivalent weight of CaCO3 / equivalent "
           "weight of the ion). Equivalent weight = molar mass / charge.",
   steps=["Equivalent weight of Ca2+ = 40.08 / 2 = {}".format(fmt(eq_ca)),
          "Equivalent weight of CaCO3 = 100.09 / 2 = {}".format(fmt(eq_caco3)),
          "Hardness = 80 x {} / {} = {} mg/L as CaCO3".format(
              fmt(eq_caco3), fmt(eq_ca), fmt(hard, 0))],
   pitfall="Always divide molar mass by CHARGE to get equivalent weight. For Ca2+ and "
           "CaCO3 both charges are 2 so it cancels, but for Na+ it does not.")

Lw, Hw = 2.0, 0.30
Qweir = 1.84 * Lw * Hw ** 1.5
mc("WAT-10", W, "Flow measurement",
   "A sharp-crested rectangular weir 2.0 m long carries a head of 0.30 m. Using "
   "Q = 1.84 L H^1.5 (SI), what is the discharge?",
   Qweir, [(1.84 * Lw * Hw, "The head is raised to the 1.5 power, not the first "
            "power."),
           (1.84 * Lw * Hw ** 2.5, "The 2.5 exponent belongs to a TRIANGULAR "
            "(V-notch) weir, not a rectangular one."),
           (1.84 * Hw ** 1.5, "The weir length is missing.")],
   units="m^3/s", diff=2,
   formula="Rectangular weir: Q = 1.84 L H^1.5 ;  "
           "V-notch (90 deg): Q = 1.38 H^2.5   [SI]",
   steps=["H^1.5 = 0.30^1.5 = {}".format(fmt(Hw ** 1.5, 4)),
          "Q = 1.84(2.0)({}) = {} m^3/s".format(fmt(Hw ** 1.5, 4), fmt(Qweir))],
   pitfall="Exponent 1.5 for rectangular, 2.5 for V-notch. A V-notch is far more "
           "sensitive at low flow, which is why it is used for small discharges.")

Qcr, bcr = 8.0, 3.0
qcr = Qcr / bcr
ycr = (qcr ** 2 / g) ** (1.0 / 3.0)
num("WAT-11", W, "Basic hydraulics",
    "A rectangular channel 3 m wide carries 8 m^3/s. What is the critical depth?",
    ycr, units="m", diff=3, tol=0.02,
    formula="Rectangular channel: y_c = (q^2 / g)^(1/3), where q = Q / b",
    steps=["Unit discharge q = 8 / 3 = {} m^2/s".format(fmt(qcr)),
           "q^2 / g = {} / 9.81 = {}".format(fmt(qcr ** 2), fmt(qcr ** 2 / g, 4)),
           "y_c = ({})^(1/3) = {} m".format(fmt(qcr ** 2 / g, 4), fmt(ycr))],
    pitfall="Critical depth depends ONLY on discharge and width, never on slope or "
            "roughness. If n or S appears in your work, you are computing NORMAL "
            "depth instead.")

mc("WAT-12", W, "Basic hydraulics",
   "In an open channel the Froude number is computed as 0.65. What is the flow regime, "
   "and what does it imply?",
   "Subcritical - flow is deep and slow, and downstream conditions control the water "
   "surface",
   [("Supercritical - flow is shallow and fast, and upstream conditions control",
     "Supercritical requires Fr greater than 1. At 0.65 the flow is subcritical."),
    ("Critical - the specific energy is at its minimum",
     "Critical flow is Fr exactly equal to 1."),
    ("Subcritical - but upstream conditions control the water surface",
     "The regime is right and the control is wrong. Subcritical flow is controlled "
     "from DOWNSTREAM, which is why backwater curves propagate upstream.")],
   diff=2,
   formula="Fr = V / sqrt(g y). Fr < 1 subcritical, Fr = 1 critical, Fr > 1 "
           "supercritical.",
   steps=["Fr = 0.65 < 1, so the flow is subcritical",
          "Subcritical flow is deep and slow relative to critical",
          "Disturbances travel upstream, so the CONTROL is downstream - this is why a "
          "culvert or weir raises the water surface upstream of itself"],
   pitfall="A hydraulic jump happens only going from supercritical to subcritical. The "
           "reverse transition is smooth and gradual.")

# -------------------------------------------------------- Structural Engineering
mtr, jtr, rtr = 11, 7, 3
mc("STR-01", ST, "Structural determinacy and stability analysis",
   "A planar truss has 11 members, 7 joints, and 3 reaction components. Is it "
   "statically determinate?",
   "Determinate, because m + r = 2j",
   [("Indeterminate to the first degree", "Check the arithmetic: 11 + 3 = 14 and "
     "2(7) = 14. They are equal, so there is no redundancy."),
    ("Unstable, because it has too few members", "Too few members would give "
     "m + r < 2j. Here they are equal."),
    ("Indeterminate to the third degree", "You may have counted the 3 reactions as "
     "redundants. Reactions belong on the LEFT side of m + r = 2j.")],
   diff=2,
   formula="Planar truss: m + r = 2j determinate ; m + r > 2j indeterminate ; "
           "m + r < 2j unstable",
   steps=["m + r = 11 + 3 = {}".format(mtr + rtr),
          "2j = 2(7) = {}".format(2 * jtr),
          "{} = {}, so the truss is statically determinate".format(mtr + rtr, 2 * jtr)],
   pitfall="Equality is necessary but NOT sufficient. A truss can satisfy m + r = 2j "
           "and still be unstable if the members are badly arranged (geometric "
           "instability).")

Ecol, Icol, Lcol, Kp = 200000.0, 20.0e6, 4000.0, 1.0
Pcr = math.pi ** 2 * Ecol * Icol / (Kp * Lcol) ** 2
Pcr_ff = math.pi ** 2 * Ecol * Icol / (0.5 * Lcol) ** 2
mc("STR-02", ST, "Column analysis",
   "A pinned-pinned steel column is 4 m long with E = 200 GPa and I = 20e6 mm^4. What "
   "is the Euler buckling load?",
   Pcr / 1000.0,
   [(Pcr_ff / 1000.0, "That is the FIXED-FIXED case with K = 0.5, which is four times "
     "stronger. A pinned column has K = 1.0."),
    (math.pi ** 2 * Ecol * Icol / (2.0 * Lcol) ** 2 / 1000.0, "That uses K = 2, the "
     "fixed-free (flagpole) case, which is the weakest."),
    (math.pi * Ecol * Icol / (Kp * Lcol) ** 2 / 1000.0, "pi is SQUARED in the Euler "
     "formula.")],
   units="kN", diff=2,
   formula="P_cr = pi^2 E I / (K L)^2.  K: pinned-pinned 1.0, fixed-fixed 0.5, "
           "fixed-pinned 0.7, fixed-free 2.0",
   steps=["(KL)^2 = (1.0 x 4000)^2 = 1.6e7 mm^2",
          "P_cr = pi^2(200,000)(20e6) / 1.6e7",
          "P_cr = {} N = {} kN".format(fmt(Pcr, 0), fmt(Pcr / 1000.0))],
   pitfall="Capacity goes as 1/K^2. Fixing both ends QUADRUPLES the buckling load; "
           "a flagpole column has only one quarter of the pinned capacity.")

sx_t, sy_t, press = 6.0, 8.0, 10.0
Ptrib = sx_t * sy_t * press
num("STR-03", ST, "Loads, load combinations, and load paths",
    "An interior column in a regular grid has bays of 6 m and 8 m on all sides. For a "
    "uniform floor load of 10 kPa, what axial load does one floor deliver to the "
    "column?",
    Ptrib, units="kN", diff=1, tol=0.01,
    formula="Tributary area for an interior column = (half-span each way) x "
            "(half-span each way) = full bay x full bay",
    steps=["The column takes half of each adjacent bay, so the tributary area is "
           "6 x 8 = {} m^2".format(fmt(sx_t * sy_t)),
           "P = {} x 10 kPa = {} kN".format(fmt(sx_t * sy_t), fmt(Ptrib))],
    pitfall="An INTERIOR column's tributary area equals one full bay. An EDGE column "
            "gets half that and a CORNER column a quarter. Identify the position "
            "first.")

Dl, Ll = 30.0, 45.0
U1 = 1.4 * Dl
U2 = 1.2 * Dl + 1.6 * Ll
mc("STR-04", ST, "Loads, load combinations, and load paths",
   "A beam carries a dead load of 30 kN/m and a live load of 45 kN/m. Using LRFD "
   "combinations 1.4D and 1.2D + 1.6L, what is the governing factored load?",
   U2, [(U1, "1.4D alone gives {} kN/m, which is smaller. 1.4D only governs when the "
         "live load is very small relative to dead load.".format(fmt(U1))),
        (Dl + Ll, "That is the unfactored service load. LRFD requires load factors."),
        (1.2 * Dl + 1.0 * Ll, "The live load factor in the primary gravity combination "
         "is 1.6, not 1.0.")],
   units="kN/m", diff=1,
   formula="LRFD: U = 1.4D  or  U = 1.2D + 1.6L (take the larger)",
   steps=["1.4D = 1.4(30) = {} kN/m".format(fmt(U1)),
          "1.2D + 1.6L = 1.2(30) + 1.6(45) = 36 + 72 = {} kN/m".format(fmt(U2)),
          "The larger governs: {} kN/m".format(fmt(U2))],
   pitfall="Always evaluate BOTH and take the larger. 1.4D governs only when L is less "
           "than about one eighth of D, which is rare in buildings.")

Mu, Fy, phib = 250.0e6, 345.0, 0.90
Zreq = Mu / (phib * Fy)
num("STR-05", ST, "Design of steel components",
    "A steel beam must resist a factored moment of 250 kN*m. With Fy = 345 MPa and a "
    "flexural resistance factor of 0.90, what plastic section modulus Z is required "
    "for a compact section?",
    Zreq, units="mm^3", diff=2, tol=0.02,
    formula="phi Mn = phi Fy Z  (compact, fully braced) -> Z_req = Mu / (phi Fy)",
    steps=["Mu = 250 kN*m = 250e6 N*mm",
           "Z = 250e6 / (0.90 x 345)",
           "Z = {} mm^3, about {} x 10^3 mm^3".format(fmt(Zreq, 0),
                                                      fmt(Zreq / 1000.0, 0))],
    pitfall="Z (plastic) is for compact sections reaching the plastic moment; S "
            "(elastic) applies when the section yields only at the extreme fibre. "
            "Z is roughly 10 to 15% larger than S for rolled shapes.")

Mu2, fy2, dd2, phi2 = 200.0e6, 420.0, 400.0, 0.90
As_req = Mu2 / (phi2 * fy2 * 0.9 * dd2)
mc("STR-06", ST, "Design of reinforced concrete components",
   "A reinforced concrete beam resists a factored moment of 200 kN*m with d = 400 mm "
   "and fy = 420 MPa. Using an assumed internal lever arm of 0.9d and phi = 0.90, "
   "estimate the required tension steel area.",
   round(As_req, 0),
   [(round(Mu2 / (phi2 * fy2 * dd2), 0), "You used the full depth d as the lever arm. "
     "The compression resultant sits inside the section, so the lever arm is less "
     "than d."),
    (round(Mu2 / (fy2 * dd2), 0), "You omitted BOTH phi and the lever-arm reduction. "
     "Each one alone increases the required steel."),
    (round(Mu2 / (phi2 * fy2 * 0.9 * dd2) / 2, 0), "No factor of 2 belongs here.")],
   units="mm^2", diff=3,
   formula="Mn = As fy (d - a/2) ;  with the lever arm approximated as 0.9d, "
           "As = Mu / (phi fy 0.9d)",
   steps=["Lever arm = 0.9(400) = {} mm".format(fmt(0.9 * dd2)),
          "As = 200e6 / (0.90 x 420 x {})".format(fmt(0.9 * dd2)),
          "As = {} mm^2".format(fmt(As_req, 0)),
          "Then verify by computing a = As fy / (0.85 f'c b) and iterating once"],
   pitfall="0.9d is a FIRST ESTIMATE only. On the real exam, if f'c and b are given, "
           "compute a = As*fy/(0.85*f'c*b) and re-solve. One iteration is usually "
           "enough.")

wdl, Ldl, Edl, Idl = 15.0, 6000.0, 200000.0, 200.0e6   # N/mm, mm, MPa, mm^4
dmid = 5 * wdl * Ldl ** 4 / (384 * Edl * Idl)
mc("STR-07", ST, "Deflection of statically determinant beams",
   "A simply supported beam spans 6 m under a uniform load of 15 kN/m. With "
   "E = 200 GPa and I = 200e6 mm^4, what is the midspan deflection?",
   dmid, [(wdl * Ldl ** 4 / (8 * Edl * Idl), "wL^4/8EI is the CANTILEVER tip "
           "deflection, which is far larger."),
          (5 * wdl * Ldl ** 3 / (384 * Edl * Idl), "The span is raised to the FOURTH "
           "power for a distributed load, not the third."),
          (wdl * Ldl ** 4 / (384 * Edl * Idl), "The numerator coefficient is 5, not 1.")],
   units="mm", diff=2,
   formula="Simply supported, UDL: delta_max = 5 w L^4 / (384 E I)",
   steps=["w = 15 kN/m = 15 N/mm, L = 6000 mm",
          "L^4 = 1.296e15 mm^4",
          "delta = 5(15)(1.296e15) / (384 x 200,000 x 200e6) = {} mm".format(fmt(dmid)),
          "Span/deflection = 6000/{} = {}, comfortably better than a typical L/360 "
          "limit".format(fmt(dmid), fmt(Ldl / dmid, 0))],
   pitfall="Deflection limits are span ratios (L/240, L/360, L/480). Convert your "
           "answer to L/x and sanity-check it against the limit.")

wfe, Lfe = 24.0, 9.0
Mend = wfe * Lfe ** 2 / 12.0
Mmid_ff = wfe * Lfe ** 2 / 24.0
Mss = wfe * Lfe ** 2 / 8.0
mc("STR-08", ST, "Elementary statically indeterminate structures",
   "A beam with BOTH ends fixed spans 9 m under a uniform load of 24 kN/m. What is the "
   "magnitude of the moment at each support?",
   Mend, [(Mmid_ff, "That is the MIDSPAN moment, wL^2/24, which is half the support "
           "moment."),
          (Mss, "wL^2/8 is the simply supported midspan moment. Fixing the ends "
           "redistributes moment into the supports."),
          (wfe * Lfe ** 2 / 2.0, "wL^2/2 is a cantilever.")],
   units="kN*m", diff=2,
   formula="Fixed-fixed UDL: M_support = wL^2/12, M_midspan = wL^2/24.  "
           "Propped cantilever UDL: M_fixed = wL^2/8.",
   steps=["wL^2 = 24(81) = {} kN*m".format(fmt(wfe * Lfe ** 2)),
          "M_support = {} / 12 = {} kN*m (negative, tension on top)".format(
              fmt(wfe * Lfe ** 2), fmt(Mend)),
          "M_midspan = {} / 24 = {} kN*m".format(fmt(wfe * Lfe ** 2), fmt(Mmid_ff)),
          "Note the total 'swing' wL^2/12 + wL^2/24 = wL^2/8 matches the simply "
          "supported value"],
   pitfall="Learn the family: /8 simply supported, /12 and /24 fixed-fixed, /8 at the "
           "fixed end of a propped cantilever. The sum of support and midspan moments "
           "always returns wL^2/8.")

Ag_t, Fy_t, phi_t = 2400.0, 250.0, 0.90
Pn_y = phi_t * Fy_t * Ag_t / 1000.0
mc("STR-09", ST, "Design of steel components",
   "A steel tension member has a gross area of 2400 mm^2 and Fy = 250 MPa. What is the "
   "design tensile strength for yielding on the gross section?",
   Pn_y, [(Fy_t * Ag_t / 1000.0, "You omitted the resistance factor of 0.90 for gross "
           "yielding."),
          (0.75 * Fy_t * Ag_t / 1000.0, "0.75 is the factor for RUPTURE on the net "
           "section, paired with Fu, not Fy."),
          (phi_t * Fy_t * Ag_t / 2000.0, "Arithmetic slip of a factor of 2.")],
   units="kN", diff=2,
   formula="Gross yielding: phi Pn = 0.90 Fy Ag.  "
           "Net rupture: phi Pn = 0.75 Fu Ae.  Take the smaller.",
   steps=["phi Pn = 0.90(250)(2400) = {} N".format(fmt(phi_t * Fy_t * Ag_t, 0)),
          "= {} kN".format(fmt(Pn_y)),
          "The net-section rupture check with Fu and Ae must also be made; the "
          "governing strength is the lesser"],
   pitfall="Two limit states, two phi factors, two areas: 0.90/Fy/Ag for yielding and "
           "0.75/Fu/Ae for rupture. Mixing them up is the classic tension-member "
           "error.")

Pml, Lml = 40.0, 10.0
Mmax_pt = Pml * Lml / 4.0
mc("STR-10", ST, "Analysis of statically determinant beams",
   "A simply supported beam spans 10 m. A single 40 kN load can be positioned anywhere "
   "along the span. What is the largest bending moment it can produce?",
   Mmax_pt, [(Pml * Lml / 8.0, "PL/8 is not a standard case. For a central point load "
              "it is PL/4."),
             (Pml * Lml / 2.0, "PL/2 would require a cantilever."),
             (Pml * Lml, "PL is the cantilever moment with the load at the tip.")],
   units="kN*m", diff=2,
   formula="Moving single point load on a simple span: M_max = P L / 4, with the load "
           "at midspan.",
   steps=["For a point load at distance a from the left, M = P a (L - a) / L",
          "This is maximized at a = L/2, giving M = P L / 4",
          "M_max = 40(10) / 4 = {} kN*m".format(fmt(Mmax_pt))],
   pitfall="For a MOVING load the critical position is part of the answer. Maximum "
           "moment occurs at midspan; maximum SHEAR occurs with the load right next "
           "to a support.")

mc("STR-11", ST, "Analysis of statically determinant beams",
   "In a simply supported beam, where does the maximum bending moment occur for any "
   "transverse loading?",
   "Where the shear diagram crosses zero",
   [("Always exactly at midspan", "True only for symmetric loading. An off-centre "
     "load moves the maximum."),
    ("At the supports, where the reactions are largest", "A simply supported beam has "
     "ZERO moment at its supports by definition."),
    ("Where the load intensity is greatest", "Load intensity drives the shape of the "
     "shear curve, not the location of maximum moment.")],
   diff=2,
   formula="dM/dx = V. Moment is stationary where shear is zero; "
           "M(x) = integral of V dx = area under the shear diagram.",
   steps=["Moment is the integral of shear, so M peaks where V = 0",
          "That point coincides with midspan only when the loading is symmetric",
          "Practical method: draw V, find where it crosses zero, then take the area "
          "under V up to that point"],
   pitfall="A point load makes shear JUMP through zero without passing through it "
           "smoothly. In that case the maximum moment sits right at the load.")

mc("STR-12", ST, "Column analysis",
   "Two identical steel columns differ only in end conditions: column A is pinned at "
   "both ends, column B is fixed at both ends. How does B's elastic buckling capacity "
   "compare?",
   "B carries four times the load, because K drops from 1.0 to 0.5 and capacity varies "
   "as 1/K^2",
   [("B carries twice the load, since K is halved",
     "Capacity depends on K SQUARED, so halving K multiplies capacity by four, not "
     "two."),
    ("They are identical, because Euler buckling depends only on E and I",
     "The effective length (KL) is squarely in the denominator. End restraint matters "
     "enormously."),
    ("B carries half the load, because fixed ends add restraint moments",
     "Restraint increases capacity. Fixing the ends shortens the buckled shape and "
     "stiffens the column.")],
   diff=2,
   formula="P_cr = pi^2 E I / (K L)^2, so P_cr is proportional to 1/K^2",
   steps=["Pinned-pinned: K = 1.0 ;  fixed-fixed: K = 0.5",
          "Ratio = (1.0 / 0.5)^2 = 4",
          "Column B buckles at four times the load of column A"],
   pitfall="Real connections are never perfectly fixed. Codes give recommended design "
           "K values that are more conservative than the theoretical 0.5.")
