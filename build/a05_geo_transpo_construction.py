"""Areas 12-14: Geotechnical, Transportation, and Construction Engineering."""
import math
from qcore import mc, num, fmt

GE = "Geotechnical Engineering"
TR = "Transportation Engineering"
CO = "Construction Engineering"
gam_w = 9.81

# ------------------------------------------------------- Geotechnical
npor = 0.40
evoid = npor / (1 - npor)
mc("GEO-01", GE, "Phase relations",
   "A soil has a porosity of 0.40. What is its void ratio?",
   round(evoid, 4),
   [(round(1 - npor, 4), "That is the volume fraction of solids, not the void ratio."),
    (round((1 - npor) / npor, 4), "You inverted the relation. Void ratio = n/(1-n)."),
    (npor, "Porosity and void ratio are different: porosity references TOTAL volume, "
     "void ratio references SOLIDS volume.")],
   diff=2,
   formula="e = n / (1 - n) ;  n = e / (1 + e).  "
           "n is voids/total; e is voids/solids.",
   steps=["e = 0.40 / (1 - 0.40) = 0.40 / 0.60",
          "e = {}".format(fmt(evoid, 4))],
   pitfall="Porosity is always less than 1; void ratio can exceed 1 for very loose "
           "soils. If your 'porosity' came out above 1, you computed e.")

Gs, ee = 2.68, 0.65
gam_sat = (Gs + ee) / (1 + ee) * gam_w
gam_dry = Gs / (1 + ee) * gam_w
mc("GEO-02", GE, "Index properties and soil classifications",
   "A saturated soil has a specific gravity of solids of 2.68 and a void ratio of "
   "0.65. What is its saturated unit weight?",
   gam_sat, [(gam_dry, "That is the DRY unit weight. Saturated includes the weight of "
              "water filling the voids."),
             (Gs * gam_w, "That is the unit weight of the solid mineral alone, with no "
              "voids."),
             (gam_sat - gam_w, "That is the BUOYANT (effective) unit weight, used "
              "below the water table.")],
   units="kN/m^3", diff=2,
   formula="gamma_dry = Gs*gamma_w/(1+e) ;  gamma_sat = (Gs+e)*gamma_w/(1+e) ;  "
           "gamma' = gamma_sat - gamma_w",
   steps=["gamma_sat = (2.68 + 0.65)(9.81) / (1 + 0.65)",
          "= {}(9.81) / 1.65".format(fmt(Gs + ee)),
          "= {} kN/m^3".format(fmt(gam_sat)),
          "For reference gamma_dry = {} and gamma' = {} kN/m^3".format(
              fmt(gam_dry), fmt(gam_sat - gam_w))],
   pitfall="Most natural soils fall between 15 and 22 kN/m^3. An answer of 26 kN/m^3 "
           "is the mineral unit weight, meaning you forgot the voids.")

mwet, mdry = 2150.0, 1800.0
wc_soil = (mwet - mdry) / mdry * 100
num("GEO-03", GE, "Laboratory and field tests",
    "A soil sample weighs 2150 g wet and 1800 g after oven drying. What is the water "
    "content?",
    wc_soil, units="%", diff=1, tol=0.01,
    formula="w (%) = (mass of water / mass of DRY solids) x 100",
    steps=["Water mass = 2150 - 1800 = {} g".format(fmt(mwet - mdry)),
           "w = 350 / 1800 x 100 = {}%".format(fmt(wc_soil))],
    pitfall="The denominator is DRY mass, never wet mass. Dividing by 2150 gives 16.3% "
            "and will be an option. Water content can legitimately exceed 100% in "
            "organic soils and soft clays.")

h_dry, g_dry2, h_wet, g_sat2 = 3.0, 18.0, 4.0, 20.0
sig_tot = h_dry * g_dry2 + h_wet * g_sat2
u_pore = h_wet * gam_w
sig_eff = sig_tot - u_pore
mc("GEO-04", GE, "Effective stress",
   "A profile has 3 m of sand (unit weight 18 kN/m^3) above the water table, over 4 m "
   "of saturated sand (20 kN/m^3). What is the effective vertical stress at a depth of "
   "7 m?",
   sig_eff, [(sig_tot, "That is TOTAL stress. Subtract the pore water pressure to get "
              "effective stress."),
             (u_pore, "That is the pore water pressure alone."),
             (sig_tot + u_pore, "Pore pressure is subtracted, not added. Water carries "
              "part of the load, relieving the grains.")],
   units="kPa", diff=2,
   formula="sigma = sum(gamma_i h_i) ;  u = gamma_w h_w ;  sigma' = sigma - u",
   steps=["Total stress = 3(18) + 4(20) = 54 + 80 = {} kPa".format(fmt(sig_tot)),
          "Pore pressure = 4(9.81) = {} kPa".format(fmt(u_pore)),
          "sigma' = {} - {} = {} kPa".format(fmt(sig_tot), fmt(u_pore), fmt(sig_eff))],
   pitfall="Pore pressure is measured from the WATER TABLE down, not from the ground "
           "surface. Using 7 m of water here is the standard error.")

phi_r, Hw_r, gam_r = 30.0, 5.0, 18.0
Ka = math.tan(math.radians(45 - phi_r / 2)) ** 2
Kp = math.tan(math.radians(45 + phi_r / 2)) ** 2
Pa = 0.5 * Ka * gam_r * Hw_r ** 2
mc("GEO-05", GE, "Stability of retaining structures",
   "A 5 m high retaining wall holds cohesionless backfill with a friction angle of 30 "
   "degrees and a unit weight of 18 kN/m^3. What is the total active thrust per metre "
   "of wall?",
   Pa, [(0.5 * Kp * gam_r * Hw_r ** 2, "You used the PASSIVE coefficient. Kp = 3 and "
         "Ka = 1/3 for phi = 30, so this is nine times too large."),
        (Ka * gam_r * Hw_r ** 2, "You omitted the one half. The pressure diagram is "
         "triangular."),
        (0.5 * gam_r * Hw_r ** 2, "The earth pressure coefficient is missing.")],
   units="kN/m", diff=3,
   formula="Ka = tan^2(45 - phi/2) ;  Kp = tan^2(45 + phi/2) ;  "
           "Pa = (1/2) Ka gamma H^2, acting at H/3 above the base",
   steps=["Ka = tan^2(45 - 15) = tan^2(30) = {}".format(fmt(Ka, 4)),
          "Pa = 0.5({})(18)(5^2) = {} kN/m".format(fmt(Ka, 4), fmt(Pa)),
          "The resultant acts at 5/3 = {} m above the base".format(fmt(Hw_r / 3.0))],
   pitfall="For phi = 30, Ka = 1/3 and Kp = 3 exactly. Memorize that pair as an "
           "instant check: Kp = 1/Ka.")

c_s, phi_s, sign_s = 15.0, 28.0, 120.0
tau_s = c_s + sign_s * math.tan(math.radians(phi_s))
mc("GEO-06", GE, "Shear strength",
   "A soil has an effective cohesion of 15 kPa and an effective friction angle of 28 "
   "degrees. What shear strength is available at an effective normal stress of "
   "120 kPa?",
   tau_s, [(sign_s * math.tan(math.radians(phi_s)), "You dropped the cohesion "
            "intercept."),
           (c_s + sign_s * math.sin(math.radians(phi_s)), "Mohr-Coulomb uses the "
            "TANGENT of the friction angle, not the sine."),
           (c_s * math.tan(math.radians(phi_s)) + sign_s, "The terms are scrambled: "
            "cohesion adds directly, and the normal stress is what gets multiplied by "
            "tan(phi).")],
   units="kPa", diff=2,
   formula="Mohr-Coulomb: tau = c' + sigma' tan(phi')",
   steps=["tan(28) = {}".format(fmt(math.tan(math.radians(phi_s)), 4)),
          "tau = 15 + 120({}) = 15 + {}".format(
              fmt(math.tan(math.radians(phi_s)), 4),
              fmt(sign_s * math.tan(math.radians(phi_s)))),
          "tau = {} kPa".format(fmt(tau_s))],
   pitfall="Use EFFECTIVE normal stress with effective parameters. Pairing total "
           "stress with c' and phi' overstates the strength, which is unconservative.")

c_b, gam_b, Df, Bf = 20.0, 18.0, 1.5, 2.0
Nc, Nq, Ng = 17.69, 7.44, 3.64      # Terzaghi factors for phi = 20 degrees
qult = c_b * Nc + gam_b * Df * Nq + 0.5 * gam_b * Bf * Ng
qall = qult / 3.0
mc("GEO-07", GE, "Bearing capacity",
   "A 2 m wide strip footing sits 1.5 m deep in soil with c = 20 kPa, "
   "gamma = 18 kN/m^3, and phi = 20 degrees. Using Terzaghi factors Nc = 17.69, "
   "Nq = 7.44, and N-gamma = 3.64, what is the ultimate bearing capacity?",
   qult, [(qall, "That is the ALLOWABLE capacity after applying a factor of safety of "
           "3. The question asks for ultimate."),
          (c_b * Nc + gam_b * Df * Nq, "You omitted the N-gamma term, which accounts "
           "for the footing width."),
          (c_b * Nc + gam_b * Df * Nq + gam_b * Bf * Ng, "The width term carries a "
           "factor of one half.")],
   units="kPa", diff=3,
   formula="Terzaghi strip footing: q_ult = c Nc + gamma Df Nq + 0.5 gamma B N_gamma",
   steps=["Cohesion term: 20(17.69) = {} kPa".format(fmt(c_b * Nc)),
          "Surcharge term: 18(1.5)(7.44) = {} kPa".format(fmt(gam_b * Df * Nq)),
          "Width term: 0.5(18)(2)(3.64) = {} kPa".format(fmt(0.5 * gam_b * Bf * Ng)),
          "q_ult = {} kPa (allowable at FS = 3 would be {} kPa)".format(
              fmt(qult), fmt(qall))],
   pitfall="Only the 0.5*gamma*B term carries the one half. Deeper footings gain "
           "capacity through the Nq surcharge term, which is why embedment helps.")

Cc, e0, Hc, s0, ds = 0.25, 0.80, 4.0, 100.0, 80.0
Sc = Cc * Hc / (1 + e0) * math.log10((s0 + ds) / s0)
mc("GEO-08", GE, "Consolidation and differential settlement",
   "A 4 m thick normally consolidated clay layer has Cc = 0.25 and e0 = 0.80. The "
   "effective stress at mid-depth increases from 100 kPa to 180 kPa. What is the "
   "primary consolidation settlement?",
   round(Sc * 1000.0, 0),
   [(round(Cc * Hc / (1 + e0) * math.log((s0 + ds) / s0) * 1000.0, 0), "You used the "
     "NATURAL logarithm. The consolidation equation uses log base 10."),
    (round(Cc * Hc * math.log10((s0 + ds) / s0) * 1000.0, 0), "You omitted the "
     "(1 + e0) denominator."),
    (round(Cc * Hc / (1 + e0) * math.log10(ds / s0) * 1000.0, 0), "The ratio is final "
     "over initial stress, so (100 + 80)/100, not 80/100. A ratio below 1 gives a "
     "negative settlement.")],
   units="mm", diff=3,
   formula="Sc = Cc H / (1 + e0) * log10( (sigma'0 + delta sigma) / sigma'0 )",
   steps=["Stress ratio = 180 / 100 = 1.8, and log10(1.8) = {}".format(
       fmt(math.log10(1.8), 4)),
       "Cc H / (1 + e0) = 0.25(4) / 1.80 = {} m".format(fmt(Cc * Hc / (1 + e0), 4)),
       "Sc = {}({}) = {} m = {} mm".format(fmt(Cc * Hc / (1 + e0), 4),
                                           fmt(math.log10(1.8), 4), fmt(Sc, 4),
                                           fmt(Sc * 1000.0, 0))],
   pitfall="log base 10, not ln. Using ln inflates settlement by 2.303. Also note the "
           "equation needs the stress at MID-DEPTH of the layer.")

LL, PL = 48.0, 22.0
PI = LL - PL
mc("GEO-09", GE, "Index properties and soil classifications",
   "A fine-grained soil has a liquid limit of 48 and a plastic limit of 22. What is "
   "its plasticity index, and how does it classify on the plasticity chart "
   "(A-line PI = 0.73(LL - 20))?",
   "PI = {}, which plots ABOVE the A-line, so it is a clay (CL)".format(fmt(PI)),
   [("PI = {}, which plots BELOW the A-line, so it is a silt (ML)".format(fmt(PI)),
     "The PI is right but the comparison is not. The A-line at LL = 48 is "
     "0.73(48 - 20) = {}, and {} exceeds it.".format(fmt(0.73 * (LL - 20)), fmt(PI))),
    ("PI = {}, a high-plasticity clay (CH)".format(fmt(LL + PL)),
     "PI is the DIFFERENCE of the limits, not the sum. CH would also require LL of 50 "
     "or more."),
    ("PI = {}, a non-plastic soil".format(fmt(PL / LL)),
     "That is a ratio, not the plasticity index.")],
   diff=3,
   formula="PI = LL - PL.  A-line: PI = 0.73(LL - 20).  Above the A-line = clay (C), "
           "below = silt (M). LL < 50 gives L (low), LL >= 50 gives H (high).",
   steps=["PI = 48 - 22 = {}".format(fmt(PI)),
          "A-line at LL = 48: PI = 0.73(28) = {}".format(fmt(0.73 * (LL - 20))),
          "{} > {}, so the point plots above the A-line -> clay".format(
              fmt(PI), fmt(0.73 * (LL - 20))),
          "LL = 48 is below 50, so it is LOW plasticity: CL"],
   pitfall="Two independent decisions: above/below the A-line picks C versus M, and "
           "LL versus 50 picks L versus H. Getting one right and one wrong is the "
           "usual outcome.")

g_field, g_max = 17.2, 18.5
RC = g_field / g_max * 100
num("GEO-10", GE, "Laboratory and field tests",
    "A field density test gives a dry unit weight of 17.2 kN/m^3. The Proctor maximum "
    "dry unit weight is 18.5 kN/m^3. What is the relative compaction?",
    RC, units="%", diff=1, tol=0.01,
    formula="Relative compaction (%) = gamma_d,field / gamma_d,max x 100",
    steps=["RC = 17.2 / 18.5 x 100",
           "RC = {}%".format(fmt(RC))],
    pitfall="Relative compaction is NOT relative density (Dr), which uses void ratios "
            "e_max and e_min and applies to granular soils. Specifications usually "
            "call for 95% relative compaction, so this test fails.")

phi_i, beta_i = 32.0, 18.0
FS_inf = math.tan(math.radians(phi_i)) / math.tan(math.radians(beta_i))
mc("GEO-11", GE, "Slope stability",
   "An infinite slope in dry cohesionless sand has a friction angle of 32 degrees and "
   "a slope angle of 18 degrees. What is the factor of safety against sliding?",
   FS_inf, [(math.tan(math.radians(beta_i)) / math.tan(math.radians(phi_i)), "You "
             "inverted the ratio. A friction angle larger than the slope angle must "
             "give FS greater than 1."),
            (phi_i / beta_i, "Use the TANGENTS of the angles, not the angles "
             "themselves."),
            (math.sin(math.radians(phi_i)) / math.sin(math.radians(beta_i)), "The "
             "infinite-slope relation uses tangents.")],
   diff=2,
   formula="Dry cohesionless infinite slope: FS = tan(phi) / tan(beta). "
           "FS is independent of depth and unit weight.",
   steps=["tan(32) = {}, tan(18) = {}".format(
       fmt(math.tan(math.radians(phi_i)), 4),
       fmt(math.tan(math.radians(beta_i)), 4)),
       "FS = {} / {} = {}".format(fmt(math.tan(math.radians(phi_i)), 4),
                                  fmt(math.tan(math.radians(beta_i)), 4),
                                  fmt(FS_inf)),
       "A dry sand slope is stable for any slope angle less than phi"],
   pitfall="With seepage parallel to the slope, FS is roughly halved (multiply by "
           "gamma'/gamma_sat). Dry and seeping slopes are very different problems.")

dp, Lp, fs_avg, qp_end = 0.40, 12.0, 45.0, 1200.0
Qs = math.pi * dp * Lp * fs_avg
Ap = math.pi / 4 * dp ** 2
Qp = qp_end * Ap
Qtot = Qs + Qp
mc("GEO-12", GE, "Foundation types",
   "A 0.40 m diameter driven pile is 12 m long. Average unit skin friction is 45 kPa "
   "and the unit end bearing is 1200 kPa. What is the ultimate axial capacity?",
   Qtot, [(Qs, "That is skin friction only. Add the end bearing."),
          (Qp, "That is end bearing only. For a long slender pile, skin friction "
           "usually dominates."),
          (math.pi / 4 * dp ** 2 * Lp * fs_avg + Qp, "You used the cross-sectional "
           "AREA for the shaft instead of the perimeter. Skin friction acts on the "
           "surface: pi*d*L.")],
   units="kN", diff=3,
   formula="Q_ult = Q_skin + Q_end = (pi d L) f_s + (pi d^2 / 4) q_p",
   steps=["Shaft surface area = pi(0.40)(12) = {} m^2".format(fmt(math.pi * dp * Lp)),
          "Q_skin = {}(45) = {} kN".format(fmt(math.pi * dp * Lp), fmt(Qs)),
          "Tip area = pi(0.40)^2/4 = {} m^2, so Q_end = 1200({}) = {} kN".format(
              fmt(Ap, 4), fmt(Ap, 4), fmt(Qp)),
          "Q_ult = {} + {} = {} kN".format(fmt(Qs), fmt(Qp), fmt(Qtot))],
   pitfall="Perimeter (pi*d) for the shaft, AREA (pi*d^2/4) for the tip. Mixing these "
           "is the most common pile-capacity error.")

# ------------------------------------------------------------- Transportation
Vk, tpr, fsk = 90.0, 2.5, 0.35
d_react = 0.278 * Vk * tpr
d_brake = Vk ** 2 / (254.0 * fsk)
SSD = d_react + d_brake
mc("TRA-01", TR, "Geometric design",
   "Using SSD = 0.278 V t + V^2 / (254 f), find the stopping sight distance for "
   "90 km/h, a 2.5 s reaction time, and a friction factor of 0.35 on a level road.",
   SSD, [(d_brake, "You omitted the perception-reaction distance, which is {} m at "
          "this speed.".format(fmt(d_react))),
         (d_react, "That is only the reaction distance; the braking distance is "
          "missing."),
         (0.278 * Vk * tpr + Vk / (254.0 * fsk), "The speed is SQUARED in the braking "
          "term.")],
   units="m", diff=2,
   formula="SSD = 0.278 V t + V^2 / (254 (f +/- G)), V in km/h.  "
           "Downgrade subtracts G, upgrade adds G.",
   steps=["Reaction: 0.278(90)(2.5) = {} m".format(fmt(d_react)),
          "Braking: 90^2 / (254 x 0.35) = 8100 / {} = {} m".format(
              fmt(254.0 * fsk), fmt(d_brake)),
          "SSD = {} + {} = {} m".format(fmt(d_react), fmt(d_brake), fmt(SSD))],
   pitfall="A DOWNGRADE lengthens SSD because G is subtracted from f. Sign errors on "
           "grade are the main trap, and they are always unconservative.")

Vr2, er, fr = 100.0, 0.08, 0.12
Rmin = Vr2 ** 2 / (127.0 * (er + fr))
num("TRA-02", TR, "Geometric design",
    "Using R = V^2 / (127(e + f)), what minimum radius is required for 100 km/h with "
    "a superelevation of 0.08 and a side friction factor of 0.12?",
    Rmin, units="m", diff=2, tol=0.02,
    formula="R_min = V^2 / (127 (e + f)), V in km/h, e and f as decimals",
    steps=["e + f = 0.08 + 0.12 = {}".format(fmt(er + fr)),
           "R = 100^2 / (127 x 0.20) = 10,000 / {}".format(fmt(127.0 * (er + fr))),
           "R = {} m".format(fmt(Rmin))],
    pitfall="Enter e as 0.08, not 8. Using percent inflates the denominator by 100 and "
            "gives an absurdly small radius.")

Kv, Av = 50.0, 5.0
Lv = Kv * Av
num("TRA-03", TR, "Geometric design",
    "A crest vertical curve joins a +2.0% grade to a -3.0% grade. For a design K value "
    "of 50, what curve length is required?",
    Lv, units="m", diff=2, tol=0.01,
    formula="L = K A, where A = |G2 - G1| in percent",
    steps=["A = |-3.0 - (+2.0)| = {} percent".format(fmt(Av)),
           "L = 50({}) = {} m".format(fmt(Av), fmt(Lv))],
    pitfall="A is the ALGEBRAIC difference, so opposing grades ADD. Treating it as "
            "3 - 2 = 1 gives 50 m instead of 250 m, a fivefold error.")

dens, spd = 25.0, 80.0
flow = dens * spd
mc("TRA-04", TR, "Traffic capacity and flow theory",
   "A freeway lane carries a density of 25 veh/km at an average speed of 80 km/h. What "
   "is the flow rate?",
   flow, [(spd / dens, "You divided. The fundamental relation is a product: q = k v."),
          (dens / spd, "Inverted, and this gives units of veh-h/km^2."),
          (dens + spd, "Adding a density and a speed is dimensionally meaningless.")],
   units="veh/h", diff=1,
   formula="Fundamental relation: q = k v  (flow = density x speed)",
   steps=["q = 25 veh/km x 80 km/h",
          "q = {} veh/h".format(fmt(flow, 0)),
          "This is near the typical capacity of about 2000 to 2400 veh/h/lane"],
   pitfall="Flow is maximized at a MIDDLE density, not the highest. Very high density "
           "means congestion, where speed collapses and flow drops.")

Vhr, V15 = 2400.0, 700.0
PHF = Vhr / (4 * V15)
mc("TRA-05", TR, "Traffic capacity and flow theory",
   "An hourly volume of 2400 veh/h has a peak 15-minute count of 700 vehicles. What is "
   "the peak hour factor?",
   round(PHF, 3),
   [(round(Vhr / V15, 3), "You omitted the factor of 4 that converts the 15-minute "
     "count to an equivalent hourly rate."),
    (round(4 * V15 / Vhr, 3), "Inverted. PHF cannot exceed 1.0."),
    (round(V15 / Vhr, 3), "That is the fraction of the hour's volume in the peak "
     "quarter, not the PHF.")],
   diff=2,
   formula="PHF = hourly volume / (4 x peak 15-minute volume)",
   steps=["Equivalent hourly flow rate = 4(700) = {} veh/h".format(fmt(4 * V15, 0)),
          "PHF = 2400 / {} = {}".format(fmt(4 * V15, 0), fmt(PHF, 3))],
   pitfall="PHF is always between 0.25 and 1.00. A value above 1.0 means you inverted "
           "it. Perfectly uniform flow gives exactly 1.0.")

a1, D1, a2, D2 = 0.44, 4.0, 0.14, 8.0
SN = a1 * D1 + a2 * D2
num("TRA-06", TR, "Pavement system design",
    "A flexible pavement has 4 in of asphalt concrete (layer coefficient 0.44) over "
    "8 in of granular base (0.14). What is the structural number?",
    SN, units="", diff=2, tol=0.01,
    formula="SN = sum(a_i D_i), with D in inches",
    steps=["Asphalt: 0.44(4) = {}".format(fmt(a1 * D1)),
           "Base: 0.14(8) = {}".format(fmt(a2 * D2)),
           "SN = {} + {} = {}".format(fmt(a1 * D1), fmt(a2 * D2), fmt(SN))],
    pitfall="Layers below the base carry a drainage coefficient m_i as well: "
            "SN = a1 D1 + a2 D2 m2 + a3 D3 m3. Here m was not given, so it is taken "
            "as 1.0.")

q1, q2, satf, Lt = 600.0, 500.0, 1800.0, 12.0
Y = q1 / satf + q2 / satf
Copt = (1.5 * Lt + 5) / (1 - Y)
mc("TRA-07", TR, "Traffic control devices",
   "A two-phase signal has critical lane volumes of 600 and 500 veh/h with a "
   "saturation flow of 1800 veh/h per lane and 12 s of total lost time. Using "
   "Webster's equation C = (1.5L + 5) / (1 - Y), what is the optimum cycle length?",
   Copt, [((1.5 * Lt + 5) / Y, "You divided by Y instead of (1 - Y). As Y approaches "
           "1, the cycle must grow without bound."),
          (1.5 * Lt + 5, "You omitted the denominator entirely."),
          ((1.5 * Lt + 5) / (1 - q1 / satf), "You used only one critical movement. Y "
           "sums the flow ratios of ALL critical phases.")],
   units="s", diff=3,
   formula="Y = sum(q_i / s_i) over critical movements ;  C_opt = (1.5 L + 5)/(1 - Y)",
   steps=["Y = 600/1800 + 500/1800 = {}".format(fmt(Y, 4)),
          "1 - Y = {}".format(fmt(1 - Y, 4)),
          "C = (1.5 x 12 + 5) / {} = 23 / {} = {} s".format(
              fmt(1 - Y, 4), fmt(1 - Y, 4), fmt(Copt))],
   pitfall="If Y reaches or exceeds 1.0 the intersection is oversaturated and no cycle "
           "length works. Webster's formula returns a negative or infinite answer, "
           "which is the signal to add capacity instead.")

base_trips, grate, yrs = 10000.0, 0.05, 10
fut = base_trips * (1 + grate) ** yrs
mc("TRA-08", TR, "Transportation planning",
   "Traffic of 10,000 vehicles per day is growing at 5% per year, compounded. What is "
   "the volume after 10 years?",
   round(fut, 0),
   [(round(base_trips * (1 + grate * yrs), 0), "That is SIMPLE growth. Compounded "
     "growth gives a larger figure."),
    (round(base_trips * grate * yrs, 0), "That is only the increment, and computed "
     "simply at that."),
    (round(base_trips * (1 + grate) ** (yrs - 1), 0), "Off by one year in the "
     "exponent.")],
   units="veh/day", diff=2,
   formula="Future volume = present x (1 + growth rate)^n",
   steps=["(1.05)^10 = {}".format(fmt(1.05 ** 10, 4)),
          "Volume = 10,000({}) = {} veh/day".format(fmt(1.05 ** 10, 4), fmt(fut, 0))],
   pitfall="Compound and simple growth diverge quickly. At 5% over 20 years the gap is "
           "about 15%, which can flip a lane-count decision.")

crashes, adt, yrs_c = 12.0, 15000.0, 3.0
mev = adt * 365.0 * yrs_c / 1.0e6
rate = crashes / mev
mc("TRA-09", TR, "Transportation planning",
   "A road segment had 12 crashes over 3 years with an ADT of 15,000. What is the "
   "crash rate per million entering vehicles?",
   round(rate, 3),
   [(round(crashes / (adt * 365.0 / 1.0e6), 3), "You used one year of exposure instead "
     "of three."),
    (round(crashes / adt * 1.0e6, 3), "You omitted the days and years, so exposure is "
     "a single day's traffic."),
    (round(crashes / yrs_c, 3), "That is crashes per year, which is not normalized by "
     "traffic volume at all.")],
   units="crashes/MEV", diff=3,
   formula="Rate = (crashes x 1,000,000) / (ADT x 365 x years)",
   steps=["Exposure = 15,000 x 365 x 3 = {} vehicles".format(fmt(adt * 365 * yrs_c, 0)),
          "= {} million entering vehicles".format(fmt(mev, 2)),
          "Rate = 12 / {} = {} crashes per MEV".format(fmt(mev, 2), fmt(rate, 3))],
   pitfall="Normalizing by exposure is the whole point. A high-volume road with more "
           "total crashes can be SAFER per vehicle than a quiet one.")

mc("TRA-10", TR, "Traffic control devices",
   "At a four-way stop-controlled intersection, two vehicles arrive at the same "
   "instant on perpendicular approaches. Who has the right of way?",
   "The vehicle on the right",
   [("The vehicle on the left", "The convention in the United States yields to the "
     "right, not the left."),
    ("The vehicle traveling straight, regardless of position", "That rule governs a "
     "left-turning versus oncoming conflict, not simultaneous arrival at a stop."),
    ("The vehicle on the roadway with the higher functional classification",
     "Classification governs which approach gets the stop sign in the first place, "
     "not the tie-break once both have stopped.")],
   diff=1,
   formula="Simultaneous arrival at an all-way stop: yield to the vehicle on the right.",
   steps=["Both vehicles stop, so neither has priority from arrival order",
          "The tie-break rule is to yield to the right",
          "A left-turning vehicle additionally yields to oncoming through traffic"],
   pitfall="Right-of-way is about who must YIELD, never who is entitled to proceed. "
           "No one ever 'has' right of way in a way that excuses a collision.")

mc("TRA-11", TR, "Pavement system design",
   "Rigid (concrete) and flexible (asphalt) pavements distribute wheel loads "
   "differently. Which statement is correct?",
   "A rigid slab spreads load over a wide area through slab bending, so subgrade "
   "stresses are low and relatively uniform",
   [("A rigid slab concentrates load directly beneath the wheel, raising subgrade "
     "stress",
     "That describes FLEXIBLE pavement behavior. The slab's stiffness is precisely "
     "what spreads the load."),
    ("A flexible pavement carries load mainly in slab bending",
     "Flexible pavements have negligible bending stiffness; they distribute load "
     "through successive granular layers."),
    ("Subgrade strength is irrelevant to rigid pavement design",
     "Subgrade support still matters; it enters rigid design through the modulus of "
     "subgrade reaction k.")],
   diff=2,
   formula="Rigid: load carried in slab flexure, low subgrade stress, design on "
           "concrete flexural strength. Flexible: load spread through layers, design "
           "on subgrade strain and layer thicknesses.",
   steps=["Concrete slabs are stiff in bending, so they act as a structural plate",
          "The plate distributes the wheel load over many times the contact area",
          "Asphalt layers are comparatively flexible, so stress reduces gradually with "
          "depth and the subgrade does more of the work"],
   pitfall="This is why a weak subgrade hurts flexible pavement far more. It also "
           "explains why rigid pavements fail by cracking and flexible ones by rutting.")

# -------------------------------------------------------------- Construction
EV, AC, PV = 450000.0, 500000.0, 400000.0
CPI = EV / AC
SPI = EV / PV
mc("CON-01", CO, "Project controls",
   "A project reports earned value of $450,000, actual cost of $500,000, and planned "
   "value of $400,000. What do the cost and schedule performance indices say?",
   "CPI = {} and SPI = {}, so the project is over budget but ahead of "
   "schedule".format(fmt(CPI), fmt(SPI)),
   [("CPI = {} and SPI = {}, so it is under budget but behind schedule".format(
       fmt(CPI), fmt(SPI)),
     "The indices are right but the interpretation is reversed. Below 1.0 is BAD, "
     "above 1.0 is GOOD, for both indices."),
    ("CPI = {} and SPI = {}, over budget and behind schedule".format(
        fmt(AC / EV), fmt(PV / EV)),
     "Both indices are inverted. Earned value always goes in the NUMERATOR."),
    ("CPI = {} and SPI = {}, on budget and on schedule".format(fmt(1.0), fmt(1.0)),
     "Neither index equals 1.0 here.")],
   diff=2,
   formula="CPI = EV / AC ;  SPI = EV / PV ;  CV = EV - AC ;  SV = EV - PV. "
           "Above 1.0 is favorable.",
   steps=["CPI = 450,000 / 500,000 = {} -> less than 1.0, so OVER budget".format(
       fmt(CPI)),
       "SPI = 450,000 / 400,000 = {} -> greater than 1.0, so AHEAD of "
       "schedule".format(fmt(SPI)),
       "Cost variance = 450,000 - 500,000 = -$50,000 (unfavorable)",
       "Schedule variance = 450,000 - 400,000 = +$50,000 (favorable)"],
   pitfall="Earned value is ALWAYS the numerator. Memorize that one fact and both "
           "indices follow, including the sign convention.")

dA, dB, dC, dD = 5.0, 3.0, 8.0, 6.0
path1 = dA + dB + dD
path2 = dA + dC + dD
proj = max(path1, path2)
mc("CON-02", CO, "Project controls",
   "Activity A (5 days) is followed by both B (3 days) and C (8 days) in parallel. "
   "Activity D (6 days) starts only after BOTH B and C finish. What is the project "
   "duration?",
   proj, [(path1, "That is the A-B-D path, which is not critical. D must wait for C "
           "as well."),
          (dA + dB + dC + dD, "You summed every activity. B and C run in PARALLEL, so "
           "only the longer one controls."),
          (dA + dC, "You stopped at C and never added D, which still has to follow "
           "the merge.")],
   units="days", diff=2,
   formula="Project duration = length of the longest (critical) path through the "
           "network.",
   steps=["Path A-B-D = 5 + 3 + 6 = {} days".format(fmt(path1)),
          "Path A-C-D = 5 + 8 + 6 = {} days".format(fmt(path2)),
          "The longer path governs, so the duration is {} days".format(fmt(proj)),
          "The critical path is A-C-D"],
   pitfall="Parallel activities do not add. The merge point waits for the SLOWEST "
           "predecessor, which is why only the longest path matters.")

ES_B = dA
LS_B = (dA + dC) - dB
TF_B = LS_B - ES_B
mc("CON-03", CO, "Project controls",
   "In that same network (A 5 days, then B 3 days and C 8 days in parallel, then D), "
   "what is the total float of activity B?",
   TF_B, [(0.0, "Zero float would mean B is critical. The critical path runs through "
           "C, so B has slack."),
          (dC, "That is C's duration, not B's float."),
          (dC - dB + dA, "You added A's duration into the float. Float is the "
           "difference between late and early start, and both already include A.")],
   units="days", diff=3,
   formula="Total float = LS - ES = LF - EF.  Activities on the critical path have "
           "zero float.",
   steps=["B's earliest start = {} (right after A)".format(fmt(ES_B)),
          "D cannot start until {} (when C finishes), so B's latest finish is "
          "{}".format(fmt(dA + dC), fmt(dA + dC)),
          "B's latest start = {} - 3 = {}".format(fmt(dA + dC), fmt(LS_B)),
          "Total float = {} - {} = {} days".format(fmt(LS_B), fmt(ES_B), fmt(TF_B))],
   pitfall="Total float is shared along a chain; consuming it on one activity reduces "
           "it for the others. FREE float is the part you can consume without "
           "affecting any successor.")

buck, cyc, effi = 1.5, 30.0, 0.83
prod = buck * (3600.0 / cyc) * effi
mc("CON-04", CO, "Construction operations and methods",
   "An excavator has a 1.5 m^3 bucket and a 30 second cycle time, working at 83% "
   "efficiency. What is its hourly production?",
   prod, [(buck * (3600.0 / cyc), "You ignored the efficiency factor. Real operations "
           "never achieve 60 productive minutes per hour."),
          (buck * cyc * effi, "You multiplied by cycle time instead of dividing into "
           "3600 s."),
          (buck * (60.0 / cyc) * effi, "You used 60 instead of 3600. With a cycle in "
           "SECONDS you need seconds per hour.")],
   units="m^3/h", diff=2,
   formula="Production = bucket volume x cycles per hour x efficiency ;  "
           "cycles per hour = 3600 / cycle time in seconds",
   steps=["Cycles per hour = 3600 / 30 = {}".format(fmt(3600.0 / cyc, 0)),
          "Theoretical = 1.5({}) = {} m^3/h".format(fmt(3600.0 / cyc, 0),
                                                    fmt(buck * 3600.0 / cyc)),
          "Apply efficiency: {} x 0.83 = {} m^3/h".format(
              fmt(buck * 3600.0 / cyc), fmt(prod))],
   pitfall="A 50 minute working hour is 0.83 efficiency. Also check whether the bucket "
           "volume is BANK or LOOSE measure, because that changes the answer by the "
           "swell factor.")

bank, swell, shrink = 1000.0, 0.25, 0.10
loose = bank * (1 + swell)
compacted = bank * (1 - shrink)
mc("CON-05", CO, "Construction estimating",
   "1000 m^3 of soil is measured in its bank (in-place) state. The swell is 25% and "
   "the shrinkage is 10%. What are the loose and compacted volumes?",
   "Loose {} m^3, compacted {} m^3".format(fmt(loose, 0), fmt(compacted, 0)),
   [("Loose {} m^3, compacted {} m^3".format(fmt(compacted, 0), fmt(loose, 0)),
     "The two are swapped. Excavating LOOSENS soil (volume up); compacting DENSIFIES "
     "it (volume down)."),
    ("Loose {} m^3, compacted {} m^3".format(fmt(bank / (1 + swell), 0),
                                             fmt(compacted, 0)),
     "You divided for swell. Loose volume is larger than bank volume, so multiply by "
     "1 + swell."),
    ("Loose {} m^3, compacted {} m^3".format(fmt(loose, 0), fmt(loose * (1 - shrink),
                                                               0)),
     "Shrinkage is referenced to BANK volume, not to the loose volume.")],
   diff=2,
   formula="Loose = bank (1 + swell) ;  Compacted = bank (1 - shrinkage). "
           "Bank is the reference state.",
   steps=["Loose = 1000(1.25) = {} m^3 - this is what you haul".format(fmt(loose, 0)),
          "Compacted = 1000(0.90) = {} m^3 - this is what you place".format(
              fmt(compacted, 0)),
          "So 1000 m^3 of cut yields only {} m^3 of embankment".format(
              fmt(compacted, 0))],
   pitfall="Haul is paid on LOOSE volume, excavation on BANK volume, and embankment on "
           "COMPACTED volume. Three different numbers for the same dirt, and quoting "
           "the wrong one loses money.")

Lf, Wf, Tf, waste = 3.0, 2.0, 0.6, 0.05
Vf = Lf * Wf * Tf
Vorder = Vf * (1 + waste)
num("CON-06", CO, "Construction estimating",
    "A footing measures 3.0 m by 2.0 m by 0.6 m thick. Including 5% waste, how much "
    "concrete should be ordered?",
    Vorder, units="m^3", diff=1, tol=0.01,
    formula="Order quantity = neat volume x (1 + waste allowance)",
    steps=["Neat volume = 3.0(2.0)(0.6) = {} m^3".format(fmt(Vf)),
           "With 5% waste = {}(1.05) = {} m^3".format(fmt(Vf), fmt(Vorder))],
    pitfall="Ready-mix is usually sold in fixed increments (often 0.5 m^3), so the "
            "practical order rounds UP. Rounding down guarantees a second truck.")

mc("CON-07", CO, "Project administration",
   "An owner wants a single entity contractually responsible for both design and "
   "construction, with one point of accountability for defects. Which project delivery "
   "method fits?",
   "Design-build",
   [("Design-bid-build", "This is the traditional method, with SEPARATE design and "
     "construction contracts. Gaps between them become the owner's problem."),
    ("Construction management at risk with a separate designer",
     "CMAR brings the builder in early and gives a guaranteed maximum price, but the "
     "designer still holds a separate contract with the owner."),
    ("Multiple prime contracts", "That multiplies the owner's contractual "
     "relationships, which is the opposite of what was asked.")],
   diff=2,
   formula="Design-bid-build: owner holds two contracts. Design-build: one contract "
           "for both. CMAR: builder joins early at risk, designer stays separate.",
   steps=["The requirement is single-point responsibility spanning design AND "
          "construction",
          "Only design-build puts both scopes under one contract",
          "This removes the owner from design-versus-construction disputes, which is "
          "the main reason owners choose it"],
   pitfall="Design-build transfers risk but reduces the owner's control over design "
           "detail. The trade-off, not the label, is what the FE tests.")

mc("CON-08", CO, "Construction operations and methods",
   "A worker must enter a 2.0 m deep trench in previously disturbed soil. What is "
   "required before entry?",
   "A protective system - sloping, benching, shoring, or shielding - designed for the "
   "soil conditions",
   [("Nothing, since the trench is less than 3 m deep",
     "There is no blanket shallow exemption. Protection is required at and above about "
     "1.5 m (5 ft), and this trench is deeper than that."),
    ("Only a competent person's visual inspection, with no physical system",
     "Inspection is required IN ADDITION to protection, never instead of it."),
    ("A safety harness and lanyard worn by the worker",
     "Fall protection does not prevent a cave-in. A collapse buries the worker "
     "regardless of a harness.")],
   diff=2,
   formula="Excavation protection is required at depths of roughly 1.5 m (5 ft) or "
           "more. Options: slope, bench, shore, or shield. A competent person "
           "inspects daily.",
   steps=["At 2.0 m the trench exceeds the threshold where protection is mandatory",
          "Previously disturbed soil cannot be classified as stable rock or Type A",
          "Select sloping, benching, shoring, or a trench shield sized for the actual "
          "soil class"],
   pitfall="Trench collapse is among the deadliest construction hazards because soil "
           "is far heavier than people expect - roughly a tonne per cubic metre.")

crew_cost, daily_out = 2800.0, 160.0
unit_cost = crew_cost / daily_out
num("CON-09", CO, "Construction estimating",
    "A crew costs $2,800 per day and places 160 m^2 of formwork per day. What is the "
    "unit cost of formwork?",
    unit_cost, units="$/m^2", diff=1, tol=0.01,
    formula="Unit cost = crew cost per day / daily output",
    steps=["Unit cost = 2,800 / 160",
           "= ${} per m^2".format(fmt(unit_cost))],
    pitfall="Doubling crew size rarely halves unit cost. Congestion and supervision "
            "limits mean output grows more slowly than cost, which is why crew "
            "balance matters.")

mc("CON-10", CO, "Interpretation of engineering drawings",
   "A drawing is labeled at a scale of 1:50. A wall measures 60 mm on the drawing. "
   "What is its actual length?",
   "3.0 m",
   [("0.3 m", "Off by a factor of 10. 60 mm x 50 = 3000 mm, which is 3.0 m, not "
     "0.3 m."),
    ("30 m", "Off by a factor of 10 the other way. Check the millimetre to metre "
     "conversion."),
    ("1.2 m", "That would be 60 mm divided by 50. At 1:50 the real object is LARGER "
     "than the drawing, so you multiply.")],
   diff=1,
   formula="Actual = drawing measurement x scale denominator. At 1:50, 1 mm on paper "
           "is 50 mm in reality.",
   steps=["60 mm x 50 = 3000 mm",
          "3000 mm = 3.0 m",
          "Check the direction: the real wall must be bigger than the paper, so "
          "multiply"],
   pitfall="Always verify the drawing has not been printed to a different size. A "
           "scaled PDF printed on the wrong paper makes every measurement wrong, "
           "which is why drawings carry a graphic scale bar.")
