"""Areas 4-6: Statics, Dynamics, Mechanics of Materials."""
import math
from qcore import mc, num, fmt

S = "Statics"
D = "Dynamics"
MM = "Mechanics of Materials"
g = 9.81

# -------------------------------------------------------------------- Statics
F1, F2 = 60.0, 80.0
R1 = math.hypot(F1, F2)
th1 = math.degrees(math.atan2(F2, F1))
mc("STAT-01", S, "Resultants of force systems",
   "Two forces act at a point: 60 kN directed east and 80 kN directed north. What is "
   "the magnitude of the resultant?",
   R1, [(F1 + F2, "You added the magnitudes. Forces add as vectors, not scalars, "
         "unless they are collinear."),
        (F2 - F1, "Subtracting applies only to opposing collinear forces."),
        (math.sqrt(F1 * F2), "The geometric mean is not a vector operation.")],
   units="kN", diff=1,
   formula="R = sqrt(Fx^2 + Fy^2) ;  theta = arctan(Fy / Fx)",
   steps=["The forces are perpendicular, so R = sqrt(60^2 + 80^2)",
          "R = sqrt(3600 + 6400) = sqrt(10000) = {} kN".format(fmt(R1)),
          "Direction: arctan(80/60) = {} degrees north of east".format(fmt(th1))],
   pitfall="A 3-4-5 triangle hiding in the numbers (60-80-100) is a hint you set it up "
           "right. Learn to spot 5-12-13 too.")

ang = [30.0, 120.0, 225.0]
mag = [100.0, 150.0, 80.0]
Fx = sum(m * math.cos(math.radians(a)) for m, a in zip(mag, ang))
Fy = sum(m * math.sin(math.radians(a)) for m, a in zip(mag, ang))
R2 = math.hypot(Fx, Fy)
th2 = math.degrees(math.atan2(Fy, Fx)) % 360.0
mc("STAT-02", S, "Resultants of force systems",
   "Three concurrent forces act in a plane: 100 N at 30 degrees, 150 N at 120 degrees, "
   "and 80 N at 225 degrees, all measured counterclockwise from the +x axis. What is "
   "the magnitude of the resultant?",
   R2, [(sum(mag), "You summed the magnitudes. These forces point in different "
         "directions."),
        (abs(Fx) + abs(Fy), "You added the component magnitudes instead of taking the "
         "square root of the sum of squares."),
        (abs(Fy) - abs(Fx), "Component differences are not resultants.")],
   units="N", diff=2,
   formula="Fx = sum(F cos a), Fy = sum(F sin a), R = sqrt(Fx^2 + Fy^2)",
   steps=["Fx = 100cos30 + 150cos120 + 80cos225 = 86.6 - 75.0 - 56.6 = {}".format(
       fmt(Fx)),
       "Fy = 100sin30 + 150sin120 + 80sin225 = 50.0 + 129.9 - 56.6 = {}".format(
           fmt(Fy)),
       "R = sqrt(({})^2 + ({})^2) = {} N".format(fmt(Fx), fmt(Fy), fmt(R2)),
       "Direction = {} degrees from +x (second quadrant)".format(fmt(th2))],
   pitfall="Track component signs in a small table. Quadrant errors, not trigonometry, "
           "cause most lost points here.")

L3, P3, a3 = 12.0, 30.0, 4.0
RB3 = P3 * a3 / L3
RA3 = P3 - RB3
mc("STAT-03", S, "Equilibrium of rigid bodies",
   "A simply supported beam spans 12 m. A 30 kN point load acts 4 m from the left "
   "support A. What is the reaction at A?",
   RA3, [(RB3, "That is the reaction at B, the FAR support. The near support carries "
          "more."),
         (P3 / 2, "The load is not at midspan, so the reactions are not equal."),
         (P3, "One support does not carry the entire load.")],
   units="kN", diff=1,
   formula="Sum of moments about B = 0 ;  Sum of Fy = 0",
   steps=["Moments about B: RA(12) - 30(12 - 4) = 0",
          "RA = 30(8) / 12 = {} kN".format(fmt(RA3)),
          "Check: RB = 30 - {} = {} kN, and the near support takes the larger "
          "share".format(fmt(RA3), fmt(RB3))],
   pitfall="The reaction at a support is proportional to the distance to the FAR "
           "support. Loading near A puts most of the load into A.")

L4, w4, P4, a4 = 10.0, 12.0, 50.0, 3.0
W4 = w4 * L4
RB4 = (W4 * L4 / 2 + P4 * a4) / L4
RA4 = W4 + P4 - RB4
mc("STAT-04", S, "Equilibrium of rigid bodies",
   "A simply supported beam spans 10 m, carries a uniform load of 12 kN/m over its "
   "full length, and a 50 kN point load 3 m from support A. What is the reaction at A?",
   RA4, [(RB4, "That is the reaction at B."),
         ((W4 + P4) / 2, "Equal reactions would require a symmetric load. The point "
          "load is not centered."),
         (W4 / 2 + P4, "You gave B's share of the uniform load but all of the point "
          "load to A.")],
   units="kN", diff=2,
   formula="Replace a UDL by W = wL acting at its centroid (midspan for uniform).",
   steps=["Uniform load total W = 12(10) = {} kN acting at midspan, 5 m from "
          "A".format(fmt(W4)),
          "Moments about A: RB(10) = 120(5) + 50(3) = 600 + 150 = 750",
          "RB = {} kN".format(fmt(RB4)),
          "RA = 120 + 50 - {} = {} kN".format(fmt(RB4), fmt(RA4))],
   pitfall="Convert every distributed load to a single resultant at its centroid "
           "BEFORE writing moment equations. Mixing the two forms is where errors "
           "enter.")

A1, x1, y1 = 100.0 * 300.0, 50.0, 150.0
A2, x2, y2 = 150.0 * 100.0, 175.0, 50.0
At = A1 + A2
xb = (A1 * x1 + A2 * x2) / At
yb = (A1 * y1 + A2 * y2) / At
mc("STAT-05", S, "Centroid of area",
   "An L-shaped area is made of a vertical rectangle 100 mm wide by 300 mm tall "
   "(occupying x = 0 to 100, y = 0 to 300) and a horizontal rectangle 150 mm wide by "
   "100 mm tall (x = 100 to 250, y = 0 to 100). How far is the centroid above the "
   "base?",
   yb, [(xb, "That is the horizontal centroid location, x-bar."),
        ((y1 + y2) / 2, "You averaged the two centroid heights without weighting by "
         "area. The larger piece pulls harder."),
        (150.0, "That would be the centroid of the vertical leg alone.")],
   units="mm", diff=2,
   formula="ybar = sum(A_i * y_i) / sum(A_i)",
   steps=["Piece 1: A = {} mm^2 at y = {} mm".format(fmt(A1, 0), fmt(y1)),
          "Piece 2: A = {} mm^2 at y = {} mm".format(fmt(A2, 0), fmt(y2)),
          "ybar = [{}({}) + {}({})] / {} ".format(fmt(A1, 0), fmt(y1), fmt(A2, 0),
                                                  fmt(y2), fmt(At, 0)),
          "ybar = {} mm".format(fmt(yb))],
   pitfall="Area-weight, never average. And for a shape with a hole, subtract the "
           "hole's area and its A*y term.")

b6, h6 = 200.0, 300.0
Ibase = b6 * h6 ** 3 / 3.0
Icent = b6 * h6 ** 3 / 12.0
mc("STAT-06", S, "Area moments of inertia",
   "A rectangle is 200 mm wide and 300 mm deep. What is its area moment of inertia "
   "about the horizontal axis through its BASE?",
   Ibase, [(Icent, "That is I about the CENTROIDAL axis. Use the parallel-axis theorem "
            "to move it to the base."),
           (h6 * b6 ** 3 / 12.0, "You swapped b and h. The depth dimension gets cubed "
            "for bending about a horizontal axis."),
           (b6 * h6 ** 3 / 36.0, "bh^3/36 is for a TRIANGLE about its centroid.")],
   units="mm^4", diff=2,
   formula="I_centroid = bh^3/12 ;  I_base = bh^3/3 = I_centroid + A*d^2",
   steps=["I_centroid = 200(300)^3 / 12 = {} mm^4".format(fmt(Icent, 0)),
          "Parallel axis: d = 150 mm, A = 60,000 mm^2, A*d^2 = {} mm^4".format(
              fmt(60000.0 * 150.0 ** 2, 0)),
          "I_base = {} + {} = {} mm^4".format(fmt(Icent, 0),
                                              fmt(60000.0 * 150.0 ** 2, 0),
                                              fmt(Ibase, 0)),
          "Equivalently bh^3/3 directly"],
   pitfall="The parallel-axis theorem only moves AWAY from the centroid. You cannot "
           "add A*d^2 twice between two non-centroidal axes.")

mu7 = 0.35
th7 = math.degrees(math.atan(mu7))
num("STAT-07", S, "Static friction",
    "A block rests on an inclined plane. The coefficient of static friction is 0.35. "
    "At what incline angle does the block begin to slide?",
    th7, units="degrees", diff=2, tol=0.02,
    formula="At impending slip on an incline: tan(theta) = mu_s",
    steps=["Along the slope: W sin(theta) = mu * W cos(theta)",
           "Weight cancels, so tan(theta) = mu = 0.35",
           "theta = arctan(0.35) = {} degrees".format(fmt(th7))],
    pitfall="The angle of repose is independent of weight. If your answer contains the "
            "block's mass, you did not cancel W.")

W8, th8d, mu8 = 800.0, 20.0, 0.30
th8 = math.radians(th8d)
driving = W8 * math.sin(th8)
resist = mu8 * W8 * math.cos(th8)
Fneed = driving - resist
mc("STAT-08", S, "Static friction",
   "An 800 N block sits on a 20 degree incline with a static friction coefficient of "
   "0.30. What force, applied parallel to and up the incline, is required to prevent "
   "the block from sliding down?",
   Fneed, [(driving, "You ignored friction entirely. Friction already resists part of "
            "the sliding tendency."),
           (driving + resist, "Sign error: friction acts UP the slope when the block "
            "tends to slide down, so it helps you."),
           (mu8 * W8, "Normal force is W cos(theta) on an incline, not W.")],
   units="N", diff=3,
   formula="F = W sin(theta) - mu_s * W cos(theta)   [block tending to slide down]",
   steps=["Driving force down slope = 800 sin20 = {} N".format(fmt(driving)),
          "Maximum friction = 0.30(800 cos20) = {} N".format(fmt(resist)),
          "Since {} > {}, the block would slide; required force = {} - {} = {} N"
          .format(fmt(driving), fmt(resist), fmt(driving), fmt(resist), fmt(Fneed))],
   pitfall="First test whether the block even moves. If max friction exceeds the "
           "driving force, the required force is ZERO and friction is not fully "
           "developed.")

P9, a9d = 20.0, 40.0
T9 = P9 / math.sin(math.radians(a9d))
H9 = T9 * math.cos(math.radians(a9d))
mc("STAT-09", S, "Frames and trusses",
   "At a truss joint, a 20 kN downward load is carried by one diagonal member inclined "
   "40 degrees above the horizontal and one horizontal member. What is the force in "
   "the diagonal?",
   T9, [(P9 * math.sin(math.radians(a9d)), "You multiplied by sin instead of dividing. "
         "The diagonal must be LARGER than the vertical load it resolves."),
        (H9, "That is the force in the horizontal member."),
        (P9 / math.cos(math.radians(a9d)), "You used cos. The vertical equilibrium "
         "equation involves the sine of the angle from horizontal.")],
   units="kN", diff=2,
   formula="At a joint: sum Fy = 0 -> T sin(theta) = P",
   steps=["Vertical equilibrium at the joint: T sin40 = 20",
          "T = 20 / sin40 = 20 / 0.643 = {} kN".format(fmt(T9)),
          "Horizontal member then carries T cos40 = {} kN".format(fmt(H9))],
   pitfall="A diagonal force is always larger in magnitude than the load component it "
           "resolves. If your diagonal came out smaller than 20 kN, you divided the "
           "wrong way.")

wmax, L10 = 18.0, 6.0
R10 = 0.5 * wmax * L10
d10 = L10 / 3.0
mc("STAT-10", S, "Equivalent force systems",
   "A triangular distributed load varies from zero at the left end to 18 kN/m at the "
   "right end over a 6 m span. What is the magnitude of the resultant, and where does "
   "it act measured from the RIGHT (maximum) end?",
   "{} kN, {} m from the right end".format(fmt(R10), fmt(d10)),
   [("{} kN, {} m from the right end".format(fmt(wmax * L10), fmt(d10)),
     "You used the full rectangle wL. A triangle's area is half that."),
    ("{} kN, {} m from the right end".format(fmt(R10), fmt(L10 / 2)),
     "Magnitude is right but the centroid of a triangle is at L/3 from its base, not "
     "midspan."),
    ("{} kN, {} m from the right end".format(fmt(R10), fmt(2 * L10 / 3)),
     "That is L/3 from the ZERO end, which is 2L/3 from the maximum end. Check which "
     "end the question measures from.")],
   diff=2,
   formula="Triangular load: R = (1/2) w_max L, acting L/3 from the maximum end",
   steps=["R = area under the load diagram = 0.5(18)(6) = {} kN".format(fmt(R10)),
          "Centroid of a triangle is L/3 from the wide (maximum) end",
          "Location = 6/3 = {} m from the right end".format(fmt(d10))],
   pitfall="Read the reference end carefully. L/3 and 2L/3 both appear in the options "
           "precisely because this is where students lose the point.")

# ------------------------------------------------------------------- Dynamics
v0, vf, s1 = 25.0, 0.0, 60.0
acc = (vf ** 2 - v0 ** 2) / (2 * s1)
num("DYN-01", D, "Kinematics",
    "A car traveling at 25 m/s brakes to a complete stop in 60 m. Assuming constant "
    "deceleration, what is the magnitude of the acceleration?",
    abs(acc), units="m/s^2", diff=1, tol=0.02,
    formula="v^2 = v0^2 + 2 a s",
    steps=["0 = 25^2 + 2a(60)",
           "a = -625 / 120 = {} m/s^2".format(fmt(acc)),
           "Magnitude = {} m/s^2".format(fmt(abs(acc)))],
    pitfall="Use the equation that does NOT contain time when time is neither given "
            "nor asked. Solving for t first doubles your work and your error chances.")

m2, L2 = 12.0, 2.0
Iend = m2 * L2 ** 2 / 3.0
Icen = m2 * L2 ** 2 / 12.0
mc("DYN-02", D, "Mass moments of inertia",
   "A slender uniform rod has a mass of 12 kg and a length of 2 m. What is its mass "
   "moment of inertia about an axis through one END, perpendicular to the rod?",
   Iend, [(Icen, "That is about the CENTROID. Add m*d^2 with d = L/2 to shift it to "
           "the end."),
          (m2 * L2 ** 2 / 2.0, "mL^2/2 is the formula for a solid cylinder about its "
           "own axis, not a rod."),
          (m2 * L2 ** 2, "You omitted the coefficient entirely.")],
   units="kg*m^2", diff=2,
   formula="Rod about centroid: mL^2/12. About end: mL^2/3 = mL^2/12 + m(L/2)^2",
   steps=["I_centroid = 12(2)^2 / 12 = {} kg*m^2".format(fmt(Icen)),
          "Shift to the end: m(L/2)^2 = 12(1)^2 = {} kg*m^2".format(fmt(m2 * 1.0)),
          "I_end = {} + {} = {} kg*m^2".format(fmt(Icen), fmt(m2 * 1.0), fmt(Iend))],
   pitfall="mL^2/12 and mL^2/3 differ by a factor of 4. Always confirm which axis the "
           "question names before reaching for a formula.")

m3, mu3, Fp = 50.0, 0.25, 200.0
fric = mu3 * m3 * g
acc3 = (Fp - fric) / m3
mc("DYN-03", D, "Force acceleration",
   "A 50 kg crate on a level floor is pulled by a 200 N horizontal force. The kinetic "
   "friction coefficient is 0.25. What is the acceleration? Use g = 9.81 m/s^2.",
   acc3, [(Fp / m3, "You ignored friction. Only the NET force produces acceleration."),
          ((Fp + fric) / m3, "Friction opposes motion, so it is subtracted."),
          (fric / m3, "That is the deceleration friction alone would cause.")],
   units="m/s^2", diff=2,
   formula="sum F = ma ;  f_k = mu_k * N ;  N = mg on a level surface",
   steps=["Normal force N = 50(9.81) = {} N".format(fmt(m3 * g)),
          "Friction = 0.25({}) = {} N".format(fmt(m3 * g), fmt(fric)),
          "Net force = 200 - {} = {} N".format(fmt(fric), fmt(Fp - fric)),
          "a = {} / 50 = {} m/s^2".format(fmt(Fp - fric), fmt(acc3))],
   pitfall="If the net force comes out negative and the crate was at rest, it does not "
           "accelerate backward; it simply does not move.")

k4, x4, m4 = 800.0, 0.15, 2.0
Espr = 0.5 * k4 * x4 ** 2
v4 = math.sqrt(2 * Espr / m4)
num("DYN-04", D, "Work, energy, and power",
    "A spring with stiffness 800 N/m is compressed 0.15 m and released against a 2 kg "
    "block on a frictionless surface. What speed does the block reach?",
    v4, units="m/s", diff=2, tol=0.02,
    formula="Spring energy = (1/2) k x^2 ;  Kinetic energy = (1/2) m v^2",
    steps=["Stored energy = 0.5(800)(0.15)^2 = {} J".format(fmt(Espr)),
           "Set equal to kinetic energy: 0.5(2)v^2 = {}".format(fmt(Espr)),
           "v = sqrt(2 x {} / 2) = {} m/s".format(fmt(Espr), fmt(v4))],
    pitfall="The displacement is SQUARED in spring energy. Doubling the compression "
            "quadruples the energy and only doubles the speed.")

Fres, vel = 1500.0, 20.0
Pw = Fres * vel
mc("DYN-05", D, "Work, energy, and power",
   "A vehicle overcomes 1500 N of total resistance while traveling at a steady "
   "20 m/s. What power is required?",
   Pw / 1000.0,
   [(Fres * vel * 60.0 / 1000.0, "You multiplied by 60 as if converting to per-minute. "
     "Power in watts already is per second."),
    (Fres / vel / 1000.0, "You divided instead of multiplying. P = Fv."),
    (0.5 * Fres * vel / 1000.0, "The factor of one half belongs to kinetic energy, "
     "not power.")],
   units="kW", diff=1,
   formula="P = F v   (for force along the direction of motion)",
   steps=["P = 1500(20) = {} W".format(fmt(Pw, 0)),
          "= {} kW".format(fmt(Pw / 1000.0))],
   pitfall="Steady speed means zero net force, so the engine force exactly equals "
           "resistance. That is why no mass or acceleration appears.")

# -------------------------------------------------- Mechanics of Materials
d1, P1m, Lm, Em = 25.0, 60000.0, 2000.0, 200000.0   # mm, N, mm, MPa
Am = math.pi / 4 * d1 ** 2
sig1 = P1m / Am
delt = P1m * Lm / (Am * Em)
mc("MECH-01", MM, "Stresses and strains",
   "A steel rod 25 mm in diameter carries an axial tensile load of 60 kN. What is the "
   "normal stress?",
   sig1, [(P1m / (math.pi * d1 ** 2), "You used pi*d^2 for area. The area of a circle "
           "is pi*d^2/4."),
          (P1m / (math.pi * d1), "That is load over circumference, not over area."),
          (P1m / (d1 ** 2), "You used the area of a 25 mm SQUARE, not a circle.")],
   units="MPa", diff=1,
   formula="sigma = P / A ;  A_circle = pi d^2 / 4",
   steps=["A = pi(25)^2 / 4 = {} mm^2".format(fmt(Am)),
          "sigma = 60,000 N / {} mm^2 = {} MPa".format(fmt(Am), fmt(sig1))],
   pitfall="1 N/mm^2 is exactly 1 MPa. Working in newtons and millimetres gives MPa "
           "directly and removes a whole class of unit errors.")

num("MECH-02", MM, "Deformations",
    "The same 25 mm diameter steel rod is 2 m long with E = 200 GPa and carries 60 kN. "
    "How much does it elongate?",
    delt, units="mm", diff=2, tol=0.02,
    formula="delta = P L / (A E)",
    steps=["A = {} mm^2, L = 2000 mm, E = 200,000 MPa".format(fmt(Am)),
           "delta = 60,000(2000) / ({} x 200,000)".format(fmt(Am)),
           "delta = {} mm".format(fmt(delt))],
    pitfall="Keep every length in mm and every stress in MPa. Mixing metres with MPa "
            "throws the answer off by 1000.")

alpha, dT, Eth = 11.7e-6, 40.0, 200000.0
sig_th = Eth * alpha * dT
mc("MECH-03", MM, "Stresses and strains",
   "A steel bar is held between two rigid, immovable supports and heated 40 degrees C. "
   "With alpha = 11.7e-6 per degree C and E = 200 GPa, what thermal stress develops?",
   sig_th, [(alpha * dT, "That is the thermal STRAIN, a dimensionless number. Multiply "
             "by E to get stress."),
            (Eth * alpha, "You left out the temperature change."),
            (Eth * alpha * dT / 2, "There is no factor of one half in thermal stress.")],
   units="MPa (compression)", diff=2,
   formula="Free strain = alpha * dT ;  if fully restrained, sigma = E alpha dT",
   steps=["Unrestrained strain would be 11.7e-6 (40) = {}".format(
       fmt(alpha * dT, 6)),
       "Full restraint forces that strain to zero, generating stress",
       "sigma = 200,000({}) = {} MPa, compressive".format(fmt(alpha * dT, 6),
                                                          fmt(sig_th))],
   pitfall="Thermal stress is independent of length and cross-section. If your answer "
           "contains L or A, you have the wrong model. Heating a restrained bar "
           "produces COMPRESSION.")

dsh, Tq = 50.0, 3.0e6    # mm, N*mm
Jp = math.pi * dsh ** 4 / 32.0
tau = Tq * (dsh / 2) / Jp
mc("MECH-04", MM, "Stresses and strains",
   "A solid circular shaft 50 mm in diameter transmits a torque of 3 kN*m. What is the "
   "maximum shear stress?",
   tau, [(Tq * (dsh / 2) / (math.pi * dsh ** 4 / 64.0), "You used I = pi d^4/64. For "
          "torsion use the POLAR moment J = pi d^4/32, which is twice I."),
         (Tq / Jp, "You left out the radius. tau = T r / J."),
         (3000.0 * (dsh / 2) / Jp, "Unit error: 3 kN*m is 3,000,000 N*mm, not 3,000. "
          "Working in N and mm is what makes the answer come out in MPa.")],
   units="MPa", diff=2,
   formula="tau = T r / J ;  J_solid = pi d^4 / 32",
   steps=["J = pi(50)^4 / 32 = {} mm^4".format(fmt(Jp, 0)),
          "r = 25 mm, T = 3,000,000 N*mm",
          "tau = 3,000,000(25) / {} = {} MPa".format(fmt(Jp, 0), fmt(tau))],
   pitfall="J = 2I for a circle. Grabbing pi d^4/64 out of the handbook by mistake "
           "halves your answer, and that half-value will be one of the options.")

wb, Lb = 20.0, 8.0
Mmax = wb * Lb ** 2 / 8.0
Vmax = wb * Lb / 2.0
mc("MECH-05", MM, "Shear and moment diagrams",
   "A simply supported beam spans 8 m under a uniform load of 20 kN/m. What is the "
   "maximum bending moment?",
   Mmax, [(wb * Lb ** 2 / 2.0, "wL^2/2 is the CANTILEVER result. A simply supported "
           "beam is wL^2/8."),
          (Vmax, "That is the maximum SHEAR, in kN, which occurs at the supports."),
          (wb * Lb ** 2 / 4.0, "wL^2/4 corresponds to a central point load PL/4 with "
           "P = wL, not to a distributed load.")],
   units="kN*m", diff=1,
   formula="Simply supported, UDL: M_max = wL^2/8 at midspan, V_max = wL/2 at supports",
   steps=["M_max = 20(8)^2 / 8 = {} kN*m".format(fmt(Mmax)),
          "V_max = 20(8) / 2 = {} kN at each support".format(fmt(Vmax)),
          "Maximum moment is at midspan, where the shear crosses zero"],
   pitfall="Memorize the four standard cases cold: wL^2/8, PL/4, wL^2/2, PL. Deriving "
           "them under time pressure is wasted minutes.")

bb, hb, Mk = 150.0, 300.0, 90.0e6   # mm, mm, N*mm
Ib = bb * hb ** 3 / 12.0
cb = hb / 2
sigb = Mk * cb / Ib
mc("MECH-06", MM, "Stresses and strains",
   "A rectangular beam 150 mm wide and 300 mm deep carries a bending moment of "
   "90 kN*m. What is the maximum bending stress?",
   sigb, [(Mk * hb / Ib, "You used the full depth instead of the distance to the "
           "extreme fibre, c = h/2."),
          (Mk * cb / (hb * bb ** 3 / 12.0), "You swapped b and h in I. The depth is "
           "cubed when bending about the strong axis."),
          (Mk / (bb * hb), "Moment divided by area is not a bending stress.")],
   units="MPa", diff=2,
   formula="sigma = M c / I ;  I_rect = b h^3 / 12 ;  c = h/2",
   steps=["I = 150(300)^3 / 12 = {} mm^4".format(fmt(Ib, 0)),
          "c = 300/2 = {} mm".format(fmt(cb)),
          "sigma = 90e6({}) / {} = {} MPa".format(fmt(cb), fmt(Ib, 0), fmt(sigb))],
   pitfall="The section modulus S = I/c = bh^2/6 does this in one step: "
           "S = 150(300)^2/6 and sigma = M/S.")

sx, sy, txy = 80.0, -20.0, 30.0
avg = (sx + sy) / 2
Rm = math.hypot((sx - sy) / 2, txy)
s1p, s2p = avg + Rm, avg - Rm
mc("MECH-07", MM, "Combined stresses, principal stresses, and Mohr's circle",
   "At a point, sigma_x = 80 MPa, sigma_y = -20 MPa, and tau_xy = 30 MPa. What is the "
   "maximum principal stress?",
   s1p, [(s2p, "That is the MINIMUM principal stress, sigma_2."),
         (Rm, "That is the maximum in-plane shear stress, the radius of the circle."),
         (sx, "sigma_x is not a principal stress unless tau_xy = 0.")],
   units="MPa", diff=3,
   formula="sigma_avg = (sx + sy)/2 ;  R = sqrt( ((sx - sy)/2)^2 + txy^2 ) ;  "
           "sigma_1,2 = sigma_avg +/- R",
   steps=["sigma_avg = (80 - 20)/2 = {} MPa (circle centre)".format(fmt(avg)),
          "R = sqrt(((80 - (-20))/2)^2 + 30^2) = sqrt(50^2 + 30^2) = {} MPa".format(
              fmt(Rm)),
          "sigma_1 = {} + {} = {} MPa".format(fmt(avg), fmt(Rm), fmt(s1p)),
          "sigma_2 = {} - {} = {} MPa".format(fmt(avg), fmt(Rm), fmt(s2p))],
   pitfall="Keep the sign on sigma_y. Using +20 instead of -20 moves the centre and "
           "shrinks the radius, and both wrong values appear as options.")

Pc, Lc, Ec, Ic = 10000.0, 3000.0, 200000.0, 80.0e6   # N, mm, MPa, mm^4
dcant = Pc * Lc ** 3 / (3 * Ec * Ic)
mc("MECH-08", MM, "Deformations",
   "A cantilever beam 3 m long carries a 10 kN point load at its free end. With "
   "E = 200 GPa and I = 80e6 mm^4, what is the tip deflection?",
   dcant, [(Pc * Lc ** 3 / (48 * Ec * Ic), "PL^3/48EI is the SIMPLY SUPPORTED midspan "
            "case. A cantilever is PL^3/3EI, which is 16 times larger."),
           (Pc * Lc ** 3 / (8 * Ec * Ic), "wL^4/8EI is the cantilever under a "
            "DISTRIBUTED load. This load is a point load."),
           (Pc * Lc ** 2 / (2 * Ec * Ic), "That expression is the tip ROTATION, in "
            "radians, not the deflection.")],
   units="mm", diff=2,
   formula="Cantilever, end point load: delta = P L^3 / (3 E I)",
   steps=["L^3 = (3000)^3 = 2.7e10 mm^3",
          "delta = 10,000(2.7e10) / (3 x 200,000 x 80e6)",
          "delta = {} mm".format(fmt(dcant))],
   pitfall="Deflection goes as L CUBED. Doubling the span multiplies tip deflection by "
           "eight, which is why span control dominates serviceability design.")

nu, sig9, E9, d9 = 0.30, 150.0, 200000.0, 40.0
eax = sig9 / E9
elat = -nu * eax
dd = elat * d9
mc("MECH-09", MM, "Stresses and strains",
   "A 40 mm diameter bar is stressed to 150 MPa in tension. With E = 200 GPa and "
   "Poisson's ratio 0.30, what is the change in diameter?",
   round(dd, 5),
   [(round(eax * d9, 5), "You applied the AXIAL strain to the diameter. The lateral "
     "strain is -nu times the axial strain."),
    (round(-eax * d9 / nu, 5), "You divided by Poisson's ratio instead of multiplying."),
    (round(abs(dd), 5), "The magnitude is right but the sign is not. A bar in TENSION "
     "gets thinner, so the diameter change is negative.")],
   units="mm", diff=3,
   formula="epsilon_axial = sigma/E ;  epsilon_lateral = -nu * epsilon_axial",
   steps=["Axial strain = 150 / 200,000 = {}".format(fmt(eax, 6)),
          "Lateral strain = -0.30({}) = {}".format(fmt(eax, 6), fmt(elat, 6)),
          "Change in diameter = {}(40) = {} mm (a decrease)".format(fmt(elat, 6),
                                                                   fmt(dd, 5))],
   pitfall="Tension thins, compression fattens. Poisson's ratio for metals runs about "
           "0.25 to 0.35; a value above 0.5 is physically impossible for an isotropic "
           "material.")
