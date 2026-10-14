"""Areas 7-9: Materials, Fluid Mechanics, Surveying."""
import math
from qcore import mc, num, fmt

MT = "Materials"
FL = "Fluid Mechanics"
SV = "Surveying"
g = 9.81
gam_w = 9.81          # kN/m^3
rho_w = 1000.0        # kg/m^3

# ------------------------------------------------------------------ Materials
mc("MAT-01", MT, "Mix design of concrete and asphalt",
   "Two concrete mixes use identical materials and the same cement content, but mix A "
   "has a water-cement ratio of 0.40 and mix B has 0.60. Which statement is correct?",
   "Mix A will have higher compressive strength and lower permeability than mix B",
   [("Mix B will be stronger because the extra water improves hydration",
     "Hydration needs only about 0.22 to 0.25 by mass. Water beyond that leaves "
     "capillary pores behind when it evaporates."),
    ("Both mixes will reach the same strength since the cement content is equal",
     "Strength tracks the water-cement RATIO, not cement content alone. This is "
     "Abrams' law."),
    ("Mix A will be more workable and easier to place",
     "Backwards. Less water means lower slump and harder placement, which is the "
     "trade-off a low w/c mix buys you.")],
   diff=1,
   formula="Abrams' law: compressive strength decreases as the water-cement ratio "
           "increases.",
   steps=["Lower w/c leaves fewer capillary voids after curing",
          "Fewer voids gives higher strength AND lower permeability (better "
          "durability)",
          "The cost is workability, which is recovered with admixtures rather than "
          "more water"],
   pitfall="Never add water on site to improve workability. It raises w/c and silently "
           "destroys the design strength.")

cem, wc = 350.0, 0.45
water = cem * wc
num("MAT-02", MT, "Mix design of concrete and asphalt",
    "A concrete mix uses 350 kg of cement per cubic metre at a water-cement ratio of "
    "0.45. How much water is required per cubic metre?",
    water, units="kg/m^3", diff=1, tol=0.01,
    formula="w/c = mass of water / mass of cement",
    steps=["water = (w/c) x cement = 0.45(350)",
           "water = {} kg/m^3".format(fmt(water)),
           "Since 1 kg of water is 1 litre, that is also {} L/m^3".format(fmt(water))],
    pitfall="Divide and you get 778 kg/m^3, which is physically absurd for a cubic "
            "metre of concrete. Sanity-check the magnitude.")

Gmb, Gmm = 2.350, 2.455
Va = (1 - Gmb / Gmm) * 100
mc("MAT-03", MT, "Test methods and specifications",
    "A compacted asphalt specimen has a bulk specific gravity of 2.350 and a "
    "theoretical maximum specific gravity of 2.455. What is the air void content?",
   round(Va, 2),
   [(round((1 - Gmm / Gmb) * 100, 2), "You inverted the ratio, giving a negative void "
     "content. Gmb is always the smaller of the two."),
    (round((Gmm - Gmb) * 100, 2), "You took the plain difference. The formula needs "
     "the ratio."),
    (round(Gmb / Gmm * 100, 2), "That is the percentage of the volume filled by "
     "material. Voids are the remainder.")],
   units="%", diff=2,
   formula="Va = (1 - Gmb / Gmm) x 100",
   steps=["Gmb / Gmm = 2.350 / 2.455 = {}".format(fmt(Gmb / Gmm, 4)),
          "Va = (1 - {}) x 100 = {}%".format(fmt(Gmb / Gmm, 4), fmt(Va)),
          "This sits inside the usual 3 to 5% design window for dense-graded mixes"],
   pitfall="Gmm is the void-free maximum, so it must exceed Gmb. If your voids come "
           "out negative you have the two swapped.")

dcyl, Pf = 150.0, 530000.0    # mm, N
Acyl = math.pi / 4 * dcyl ** 2
fc = Pf / Acyl
num("MAT-04", MT, "Test methods and specifications",
    "A 150 mm diameter concrete cylinder fails at a load of 530 kN. What is its "
    "compressive strength?",
    fc, units="MPa", diff=1, tol=0.02,
    formula="f'c = P / A ;  A = pi d^2 / 4",
    steps=["A = pi(150)^2 / 4 = {} mm^2".format(fmt(Acyl, 0)),
           "f'c = 530,000 / {} = {} MPa".format(fmt(Acyl, 0), fmt(fc))],
    pitfall="A 150 x 300 mm cylinder is the standard specimen. A 100 x 200 mm cylinder "
            "of the same concrete tests slightly HIGHER because of the size effect.")

ssd, od = 505.0, 495.0
absorp = (ssd - od) / od * 100
mc("MAT-05", MT, "Physical and mechanical properties",
   "An aggregate sample weighs 505 g saturated surface-dry and 495 g oven-dry. What is "
   "the absorption?",
   round(absorp, 2),
   [(round((ssd - od) / ssd * 100, 2), "You divided by the SSD mass. Absorption is "
     "referenced to the OVEN-DRY mass."),
    (round(ssd - od, 2), "That is the mass of absorbed water in grams, not a "
     "percentage."),
    (round(od / ssd * 100, 2), "That is a mass ratio, not absorption.")],
   units="%", diff=2,
   formula="Absorption (%) = (SSD mass - oven-dry mass) / oven-dry mass x 100",
   steps=["Absorbed water = 505 - 495 = {} g".format(fmt(ssd - od)),
          "Absorption = 10 / 495 x 100 = {}%".format(fmt(absorp))],
   pitfall="Absorption uses oven-dry in the denominator; moisture CONTENT of a wet "
           "aggregate also uses oven-dry. Specific gravity is where the SSD basis "
           "shows up.")

mc("MAT-06", MT, "Physical and mechanical properties",
   "Which pairing of material and modulus of elasticity is approximately correct?",
   "Structural steel, about 200 GPa (29,000 ksi)",
   [("Structural steel, about 70 GPa (10,000 ksi)",
     "That is ALUMINUM. Steel is roughly three times stiffer."),
    ("Normal-weight concrete, about 200 GPa",
     "Concrete is roughly 25 GPa, about one eighth of steel."),
    ("Douglas fir lumber, about 70 GPa",
     "Wood parallel to grain is roughly 10 to 13 GPa. 70 GPa is aluminum.")],
   diff=1,
   formula="E_steel ~ 200 GPa ; E_concrete ~ 25 GPa (4700 sqrt(f'c) MPa) ; "
           "E_aluminum ~ 70 GPa ; E_wood ~ 11 GPa",
   steps=["Anchor on steel at 200 GPa / 29,000 ksi",
          "Aluminum is about one third of steel; concrete about one eighth; wood about "
          "one twentieth",
          "These ratios let you reject three options without a calculator"],
   pitfall="Concrete's E depends on strength, roughly 4700*sqrt(f'c) in MPa. Steel's "
           "E does NOT change with grade; only its yield strength does.")

# ------------------------------------------------------------- Fluid Mechanics
hd = 6.0
pres = rho_w * g * hd / 1000.0
mc("FLU-01", FL, "Fluid statics",
   "What is the gauge pressure at a depth of 6 m in fresh water?",
   pres, [(pres + 101.3, "You reported ABSOLUTE pressure. The question asks for gauge, "
           "which excludes atmospheric."),
          (rho_w * hd / 1000.0, "You omitted g. Density times depth is not a "
           "pressure."),
          (rho_w * g * hd, "That is the answer in PASCALS. The question asks for kPa, "
           "so divide by 1000.")],
   units="kPa", diff=1,
   formula="p = rho g h = gamma h   (gamma_water = 9.81 kN/m^3)",
   steps=["p = 9.81 kN/m^3 x 6 m = {} kPa".format(fmt(pres)),
          "Equivalently 1000(9.81)(6) = {} Pa".format(fmt(rho_w * g * hd, 0))],
   pitfall="Roughly 10 kPa per metre of water is a useful field check. Also remember "
           "pressure depends only on DEPTH, never on the shape or volume of the "
           "container.")

bw, hg = 2.0, 3.0
hc = hg / 2
Ag = bw * hg
Fg = gam_w * hc * Ag
ycp = 2.0 * hg / 3.0
mc("FLU-02", FL, "Fluid statics",
   "A vertical rectangular gate 2 m wide and 3 m tall has its top edge at the water "
   "surface. What is the total hydrostatic force on the gate?",
   Fg, [(gam_w * hg * Ag, "You used the full depth rather than the depth to the "
         "CENTROID of the gate, which is h/2."),
        (gam_w * hc * bw, "You used width instead of area."),
        (gam_w * ycp * Ag, "You used the CENTRE OF PRESSURE depth (2 m). Force uses "
         "the CENTROID depth (1.5 m); the centre of pressure is only where it acts.")],
   units="kN", diff=2,
   formula="F = gamma * h_centroid * A ;  centre of pressure at 2h/3 below the surface "
           "for a surface-piercing vertical rectangle",
   steps=["Centroid depth h_c = 3/2 = {} m".format(fmt(hc)),
          "Area A = 2(3) = {} m^2".format(fmt(Ag)),
          "F = 9.81({})({}) = {} kN".format(fmt(hc), fmt(Ag), fmt(Fg)),
          "The force acts at 2(3)/3 = {} m below the surface, NOT at the "
          "centroid".format(fmt(ycp))],
   pitfall="Force uses the CENTROID depth; its line of action is at the CENTRE OF "
           "PRESSURE, which is deeper. Two different depths in one problem.")

D1, D2, V1 = 0.300, 0.150, 2.0
A1 = math.pi / 4 * D1 ** 2
A2 = math.pi / 4 * D2 ** 2
Qf = A1 * V1
V2 = Qf / A2
mc("FLU-03", FL, "Flow measurement",
   "Water flows at 2 m/s through a 300 mm diameter pipe that reduces to 150 mm. What "
   "is the velocity in the smaller pipe?",
   V2, [(V1 * (D1 / D2), "You scaled by the diameter ratio. Velocity scales with the "
         "ratio of diameters SQUARED, because area does."),
        (V1 * (D2 / D1) ** 2, "You inverted the ratio. A smaller pipe means a higher "
         "velocity."),
        (V1, "Velocity cannot be unchanged when the area changes.")],
   units="m/s", diff=2,
   formula="Q = A1 V1 = A2 V2 ;  V2 = V1 (D1/D2)^2",
   steps=["Q = (pi/4)(0.3)^2(2) = {} m^3/s".format(fmt(Qf, 4)),
          "A2 = (pi/4)(0.15)^2 = {} m^2".format(fmt(A2, 4)),
          "V2 = {} / {} = {} m/s".format(fmt(Qf, 4), fmt(A2, 4), fmt(V2)),
          "Shortcut: halving the diameter quadruples the velocity"],
   pitfall="Halving a diameter quarters the area, so velocity goes up 4x, not 2x. This "
           "factor-of-two trap is on nearly every continuity question.")

hor = 5.0
vtor = math.sqrt(2 * g * hor)
num("FLU-04", FL, "Energy, impulse, and momentum of fluids",
    "A large open tank has a small orifice 5 m below the free water surface. "
    "Neglecting losses, what is the jet velocity?",
    vtor, units="m/s", diff=1, tol=0.02,
    formula="Torricelli: v = sqrt(2 g h)",
    steps=["Bernoulli from surface to jet: all head converts to velocity head",
           "v = sqrt(2(9.81)(5)) = sqrt({})".format(fmt(2 * g * hor)),
           "v = {} m/s".format(fmt(vtor))],
    pitfall="This is Bernoulli with a free surface, so the answer is independent of "
            "the fluid's density. Water and oil exit at the same speed under the same "
            "head.")

Vr, Dr, nu_r = 1.5, 0.100, 1.0e-6
Re = Vr * Dr / nu_r
mc("FLU-05", FL, "Fluid properties",
   "Water at 20 degrees C (kinematic viscosity 1.0e-6 m^2/s) flows at 1.5 m/s in a "
   "100 mm diameter pipe. What is the Reynolds number, and what is the flow regime?",
   "{} - turbulent".format(fmt(Re, 0)),
   [("{} - laminar".format(fmt(Re, 0)), "The number is right but the regime is not. "
     "Pipe flow is turbulent above about 4000 (laminar below about 2100)."),
    ("{} - turbulent".format(fmt(Vr * 100 / nu_r, 0)), "You used the diameter in "
     "millimetres. Re is dimensionless only if every term is in consistent SI units."),
    ("{} - laminar".format(fmt(Vr * Dr / 1.0e-3, 0)), "You used dynamic viscosity in "
     "place of kinematic. Re = VD/nu uses kinematic viscosity.")],
   diff=2,
   formula="Re = V D / nu = rho V D / mu. Laminar below ~2100, turbulent above ~4000.",
   steps=["Re = 1.5(0.100) / 1.0e-6 = {}".format(fmt(Re, 0)),
          "{} is well above 4000, so the flow is turbulent".format(fmt(Re, 0)),
          "Nearly all civil water-conveyance flow is turbulent"],
   pitfall="Keep D in metres. Using millimetres inflates Re by 1000 and the inflated "
           "value will still read 'turbulent', hiding the error.")

ff, Lp, Dp, Vp = 0.02, 100.0, 0.150, 2.0
hf = ff * (Lp / Dp) * Vp ** 2 / (2 * g)
mc("FLU-06", FL, "Energy, impulse, and momentum of fluids",
   "Water flows at 2 m/s through 100 m of 150 mm pipe with a friction factor of 0.02. "
   "What is the friction head loss?",
   hf, [(ff * (Lp / Dp) * Vp ** 2 / g, "You omitted the 2 in the velocity head term. "
         "Velocity head is V^2/2g."),
        (ff * Lp * Vp ** 2 / (2 * g), "You left out the division by D."),
        (Vp ** 2 / (2 * g), "That is just the velocity head, with no friction "
         "multiplier.")],
   units="m", diff=2,
   formula="Darcy-Weisbach: hf = f (L/D) (V^2 / 2g)",
   steps=["L/D = 100 / 0.150 = {}".format(fmt(Lp / Dp, 1)),
          "V^2/2g = 4 / 19.62 = {} m".format(fmt(Vp ** 2 / (2 * g), 4)),
          "hf = 0.02({})({}) = {} m".format(fmt(Lp / Dp, 1),
                                            fmt(Vp ** 2 / (2 * g), 4), fmt(hf))],
   pitfall="L and D must be in the SAME unit so that L/D is dimensionless. Mixing "
           "metres with millimetres here is the most common error.")

Vol = 0.05
Fb = rho_w * g * Vol
mc("FLU-07", FL, "Fluid statics",
   "A fully submerged object displaces 0.05 m^3 of fresh water. What is the buoyant "
   "force on it?",
   Fb, [(rho_w * Vol, "You omitted g. Mass displaced is 50 kg; the FORCE is that times "
         "g."),
        (rho_w * g * Vol / 1000.0, "That is the answer in kN, but the question asks "
         "for newtons. Watch the requested unit."),
        (rho_w * g * Vol / 2.0, "You halved the displaced volume. The object is FULLY "
         "submerged, so it displaces its entire volume.")],
   units="N", diff=1,
   formula="Archimedes: F_buoyant = gamma_fluid x V_displaced = rho g V",
   steps=["Displaced volume = 0.05 m^3",
          "F = 1000(9.81)(0.05) = {} N".format(fmt(Fb)),
          "Equivalently 9.81 kN/m^3 x 0.05 m^3 = {} kN".format(fmt(Fb / 1000.0))],
   pitfall="Buoyancy depends on the DISPLACED volume and the FLUID's density, never on "
           "the object's own density. Density only decides whether it floats.")

Qj, Vj = 0.02, 15.0
Fj = rho_w * Qj * Vj
num("FLU-08", FL, "Energy, impulse, and momentum of fluids",
    "A water jet discharging 0.02 m^3/s at 15 m/s strikes a flat plate held normal to "
    "the jet and is deflected sideways. What force does the jet exert on the plate?",
    Fj, units="N", diff=2, tol=0.02,
    formula="F = rho Q (V_in - V_out). Normal flat plate: F = rho Q V",
    steps=["Mass flow = rho Q = 1000(0.02) = {} kg/s".format(fmt(rho_w * Qj)),
           "The jet's normal momentum drops to zero, so F = mass flow x V",
           "F = {}(15) = {} N".format(fmt(rho_w * Qj), fmt(Fj))],
    pitfall="A plate takes rho*Q*V. A curved vane turning the jet a full 180 degrees "
            "takes TWICE that, because the momentum reverses instead of merely "
            "stopping.")

# -------------------------------------------------------------------- Surveying
bm, bs, fs = 100.000, 1.520, 2.870
hi = bm + bs
elev = hi - fs
mc("SUR-01", SV, "Leveling",
   "A level is set up between a benchmark at elevation 100.000 m and a new point. The "
   "backsight on the benchmark reads 1.520 m and the foresight on the new point reads "
   "2.870 m. What is the elevation of the new point?",
   elev, [(bm + fs - bs, "You reversed backsight and foresight. The new point reads "
           "HIGHER on the rod, so it must be LOWER in elevation."),
          (hi, "That is the height of instrument, not the point elevation."),
          (bm + bs + fs, "Foresights are subtracted, not added.")],
   units="m", diff=1,
   formula="HI = known elevation + BS ;  new elevation = HI - FS",
   steps=["HI = 100.000 + 1.520 = {} m".format(fmt(hi, 3)),
          "Elevation = {} - 2.870 = {} m".format(fmt(hi, 3), fmt(elev, 3)),
          "The larger foresight reading confirms the new point is lower"],
   pitfall="Bigger rod reading means lower ground. Use that as an instant sanity check "
           "before you trust the arithmetic.")

rise, run = 3.6, 240.0
grade = rise / run * 100
num("SUR-02", SV, "Leveling",
    "A road rises 3.6 m over a horizontal distance of 240 m. What is the grade in "
    "percent?",
    grade, units="%", diff=1, tol=0.01,
    formula="Grade (%) = (rise / horizontal run) x 100",
    steps=["Grade = 3.6 / 240 = {}".format(fmt(rise / run, 4)),
           "x 100 = {}%".format(fmt(grade))],
    pitfall="Grade uses HORIZONTAL run, not slope distance. For grades under about "
            "10% the difference is negligible, which is why the shortcut survives.")

pts = [(100.0, 100.0), (200.0, 150.0), (150.0, 250.0)]
sh = 0.0
for i in range(len(pts)):
    x1, y1 = pts[i]
    x2, y2 = pts[(i + 1) % len(pts)]
    sh += x1 * y2 - x2 * y1
Atri = abs(sh) / 2.0
num("SUR-03", SV, "Area computations",
    "A triangular parcel has corners at coordinates (100, 100), (200, 150), and "
    "(150, 250), in metres. What is its area?",
    Atri, units="m^2", diff=2, tol=0.01,
    formula="Area = (1/2) |sum( x_i * y_(i+1) - x_(i+1) * y_i )|   [coordinate method]",
    steps=["Cross products: 100(150) - 200(100) = -5,000",
           "200(250) - 150(150) = +27,500",
           "150(100) - 100(250) = -10,000",
           "Sum = {}; area = |{}| / 2 = {} m^2".format(fmt(sh, 0), fmt(sh, 0),
                                                       fmt(Atri, 0))],
    pitfall="You must return to the FIRST point to close the loop. Omitting the last "
            "cross product is the standard mistake, and taking the absolute value at "
            "the end makes traverse direction irrelevant.")

Aend1, Aend2, Lsec = 25.0, 40.0, 30.0
Vol_ae = (Aend1 + Aend2) / 2 * Lsec
mc("SUR-04", SV, "Earthwork and volume computations",
   "Two cross sections 30 m apart have end areas of 25 m^2 and 40 m^2. Using the "
   "average end area method, what is the volume between them?",
   Vol_ae, [((Aend1 + Aend2) * Lsec, "You forgot to average. Divide the sum of the end "
             "areas by 2."),
            (Lsec / 6 * (Aend1 + 4 * 30.0 + Aend2), "That is the prismoidal formula "
             "with a measured middle area of 30 m^2. The question asked for the "
             "average end area method, and no middle section was given."),
            (math.sqrt(Aend1 * Aend2) * Lsec, "The geometric mean is not used in "
             "earthwork volumes.")],
   units="m^3", diff=1,
   formula="Average end area: V = L (A1 + A2) / 2",
   steps=["Average area = (25 + 40) / 2 = {} m^2".format(fmt((Aend1 + Aend2) / 2)),
          "V = {}(30) = {} m^3".format(fmt((Aend1 + Aend2) / 2), fmt(Vol_ae))],
   pitfall="Average end area OVERESTIMATES when the section changes shape, which is "
           "why the prismoidal formula exists. It is the conservative, standard "
           "method for pay quantities.")

az = 215.0
mc("SUR-05", SV, "Angles, distances, and trigonometry",
   "A line has an azimuth of 215 degrees measured clockwise from north. What is its "
   "bearing?",
   "S 35 W",
   [("N 35 W", "Azimuth 215 is in the THIRD quadrant (180 to 270), which is southwest, "
     "not northwest."),
    ("S 55 W", "You subtracted from 270 instead of 180. For the third quadrant, "
     "bearing angle = azimuth - 180."),
    ("S 35 E", "Correct angle, wrong side. East bearings come from the second "
     "quadrant (90 to 180), not the third.")],
   diff=2,
   formula="Quadrant 1 (0-90): N az E | Q2 (90-180): S (180 - az) E | "
           "Q3 (180-270): S (az - 180) W | Q4 (270-360): N (360 - az) W",
   steps=["215 degrees falls between 180 and 270, so the line heads southwest",
          "Bearing angle = 215 - 180 = 35 degrees",
          "Bearing = S 35 W"],
   pitfall="Sketch the compass and mark the quadrant before converting. Every wrong "
           "option here is a plausible arithmetic result with the wrong quadrant.")

sd, va = 150.0, 4.5
hdist = sd * math.cos(math.radians(va))
vdist = sd * math.sin(math.radians(va))
num("SUR-06", SV, "Angles, distances, and trigonometry",
    "A total station measures a slope distance of 150.00 m with a vertical angle of "
    "-4 degrees 30 minutes. What is the horizontal distance?",
    hdist, units="m", diff=2, tol=0.005,
    formula="Horizontal = S cos(vertical angle) ;  Vertical = S sin(vertical angle)",
    steps=["4 degrees 30 minutes = 4.5 degrees",
           "H = 150.00 cos(4.5) = {} m".format(fmt(hdist, 3)),
           "The elevation difference would be 150 sin(-4.5) = {} m".format(
               fmt(vdist, 3))],
    pitfall="If the instrument reports a ZENITH angle instead (measured from straight "
            "up), horizontal distance uses SINE. Confirm which convention the "
            "instrument uses.")

dlat, ddep, perim = 0.08, -0.06, 800.0
misc = math.hypot(dlat, ddep)
prec = perim / misc
mc("SUR-07", SV, "Coordinate systems",
   "A closed traverse with a perimeter of 800 m has a latitude misclosure of +0.08 m "
   "and a departure misclosure of -0.06 m. What is the precision of closure?",
   "1:{}".format(fmt(prec, 0)),
   [("1:{}".format(fmt(perim / (abs(dlat) + abs(ddep)), 0)), "You added the misclosures "
     "directly. They are perpendicular components, so combine them with Pythagoras."),
    ("1:{}".format(fmt(misc / perim, 4)), "The ratio is inverted. Precision is "
     "expressed as 1 over a large number."),
    ("1:{}".format(fmt(perim / abs(dlat), 0)), "You used only the latitude misclosure "
     "and ignored the departure.")],
   diff=3,
   formula="Linear misclosure = sqrt(sum_lat^2 + sum_dep^2) ; "
           "precision = perimeter / misclosure",
   steps=["Misclosure = sqrt(0.08^2 + 0.06^2) = sqrt(0.0064 + 0.0036) = {} m".format(
       fmt(misc, 3)),
       "Precision = 800 / {} = {}".format(fmt(misc, 3), fmt(prec, 0)),
       "Reported as 1:{}".format(fmt(prec, 0))],
   pitfall="A 3-4-5 triangle again (0.06, 0.08, 0.10). Precision is always written as "
           "1 : a large number, so a small ratio means you inverted it.")

Rc, delta = 250.0, 36.0
Lc = Rc * math.radians(delta)
Tc = Rc * math.tan(math.radians(delta / 2))
mc("SUR-08", SV, "Angles, distances, and trigonometry",
   "A simple horizontal curve has a radius of 250 m and a central angle of 36 degrees. "
   "What is the curve length?",
   Lc, [(Tc, "That is the TANGENT distance, T = R tan(delta/2)."),
        (Rc * delta, "You used degrees directly. Convert the central angle to radians "
         "first, or use pi*R*delta/180."),
        (2 * Rc * math.sin(math.radians(delta / 2)), "That is the LONG CHORD, which is "
         "slightly shorter than the arc.")],
   units="m", diff=2,
   formula="L = R * delta(radians) = pi R delta / 180 ;  T = R tan(delta/2) ;  "
           "LC = 2R sin(delta/2)",
   steps=["delta = 36 degrees = {} radians".format(fmt(math.radians(delta), 4)),
          "L = 250({}) = {} m".format(fmt(math.radians(delta), 4), fmt(Lc)),
          "For comparison T = 250 tan(18) = {} m and LC = {} m".format(
              fmt(Tc), fmt(2 * Rc * math.sin(math.radians(delta / 2))))],
   pitfall="Arc length needs RADIANS. Using 36 directly gives 9000 m, which is "
           "obviously wrong but easy to write down in a hurry.")
