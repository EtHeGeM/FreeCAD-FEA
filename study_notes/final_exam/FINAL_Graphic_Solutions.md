# MECT2222 Final Exercise Questions - Graphic Solution Notes

Source file: `FINAL_Exercise_Questions.pdf`

This document is a graphical study solution set. All problems require a free-body diagram; therefore the solution strategy is organized around FBDs, shear/moment diagrams, Mohr circles, stress distributions, and vibration response plots.

## 1. Vibration Problems

### Problem 22-56

Given: `m = 40 kg`, `k = 800 N/m`, `F = 100 cos(2t) N`.

Equation of motion about static equilibrium:

`m x'' + kx = F0 cos(omega t)`

Natural frequency:

`omega_n = sqrt(k/m) = sqrt(800/40) = 4.472 rad/s`

Steady-state displacement amplitude:

`X = F0 / |k - m omega^2| = 100 / |800 - 40(2)^2| = 0.15625 m`

Maximum speed:

`v_max = omega X = 2(0.15625) = 0.3125 m/s`

![22-56 response](final_graphic_solutions/22-56_response.png)

### Problem 22-42

For a block-spring system subjected to `F = F0 cos(omega t)` and measured from static equilibrium:

`m x'' = F0 cos(omega t) - kx`

Therefore:

`x'' + (k/m)x = (F0/m) cos(omega t)`

Let `omega_n = sqrt(k/m)`. For `omega != omega_n`,

`x(t) = C1 cos(omega_n t) + C2 sin(omega_n t) + [F0/(k - m omega^2)] cos(omega t)`

At resonance, `omega = omega_n`, the particular solution must be written in resonant form.

### Problem 22-37

Rod data: `m = 6 kg`, `L = 4 m`, springs located `2 m` below the pin, each `k = 200 N/m`.

For a small rotation `theta`, spring point displacement is:

`x = 2 theta`

Each spring force is `kx`, and two springs act together. Restoring moment:

`M_s = 2 k (2 theta)(2) = 8k theta`

Mass moment of inertia about the pin:

`I_O = (1/3)mL^2 = (1/3)(6)(4^2) = 32 kg m^2`

Natural frequency:

`omega_n = sqrt(8k/I_O) = sqrt(1600/32) = 7.071 rad/s`

![22-37 restoring moment](final_graphic_solutions/22-37_restoring_moment.png)

### Problem 22-36

Four identical vertical springs act in parallel:

`k_eq = 4k`

The equation of motion is:

`m x'' + 4kx = 0`

Natural frequency and period:

`omega_n = sqrt(4k/m)`

`T_n = 2 pi sqrt(m/(4k))`

### Problem 22-23

Disk data: `m = 10 kg`, `r = 150 mm = 0.150 m`, two springs with `k = 80 N/m`.

For no slip between cord and disk, spring deformation is proportional to disk rotation:

`x = r theta`

Two springs produce restoring torque:

`M_s = 2 k r^2 theta`

Disk inertia:

`I_O = (1/2)mr^2`

Natural frequency:

`omega_n = sqrt((2kr^2)/I_O) = sqrt(4k/m) = sqrt(4(80)/10) = 5.657 rad/s`

Natural period:

`T_n = 2pi/omega_n = 1.111 s`

### Problem 22-15

Uniform bar pinned at the center with one spring at the left end.

For a small bar rotation `theta`, end displacement is `(L/2)theta`.

Restoring moment:

`M_s = k(L theta/2)(L/2) = kL^2 theta/4`

Bar inertia about center:

`I_O = mL^2/12`

Natural frequency:

`omega_n = sqrt((kL^2/4)/(mL^2/12)) = sqrt(3k/m)`

Natural period:

`T_n = 2pi sqrt(m/(3k))`

## 2. Buckling Problems

### Problem 13-40

Use a joint FBD at `A`. Member `AC` is a two-force member with geometry `3-4-5`. The horizontal load `P = 18 kN` is balanced by the horizontal component of the diagonal member force.

From joint equilibrium:

`F_AC(3/5) = P`

`F_AC = 5P/3`

The vertical component transmitted to member `AB` is:

`F_AB = F_AC(4/5) = 4P/3 = 24 kN`

Then compare `F_AB` with the column buckling load about the weak `y-y` axis:

`P_cr = pi^2 E I_y / (KL)^2`

For pin-pin buckling, `K = 1`. Factor of safety:

`FS = P_cr / F_AB`

### Problem 13-34

Column `AB` is pin connected at both ends. Beam `BC` carries uniform load `w` over `5 m`.

1. Draw FBD of beam `BC`.
2. Find vertical reaction at `B`.
3. That reaction is the axial compression in column `AB`.
4. Apply Euler buckling about the weak axis:

`P_allow = P_cr / FS`

`P_cr = pi^2 E I_min / L^2`

5. Solve `R_B(w) <= P_allow` for `w`.

### Problem 13-13

The deck is supported by two columns with different effective length factors:

- Column `AB`: pinned at `A`, fixed at `B`
- Column `CD`: pinned at `C` and `D`

For the maximum load position, the deck load should be placed so that both columns reach their allowable critical loads at the same time:

`R_A / P_cr,AB = R_C / P_cr,CD`

Use deck equilibrium to relate `R_A`, `R_C`, total load `P`, and load eccentricity `d`.

## 3. Shaft and Combined Loading Problems

### Problems R11-3 and R11-4

These are shaft sizing problems with bearing reactions in two transverse planes plus torque from gear forces.

General graphical solution:

1. Draw FBD of the shaft.
2. Resolve gear forces into `x` and `z` components.
3. Solve bearing reactions in the `x-y` and `z-y` planes.
4. Draw bending moment diagrams `M_x(y)` and `M_z(y)`.
5. Combine bending moments:

`M_R = sqrt(M_x^2 + M_z^2)`

6. Determine torque:

`T = F_t r`

7. For a solid circular shaft:

`sigma = 32M_R/(pi d^3)`

`tau = 16T/(pi d^3)`

Maximum distortion energy:

`sigma_VM = sqrt(sigma^2 + 3tau^2)`

Maximum shear stress theory:

`tau_max = sqrt((sigma/2)^2 + tau^2)`

### Problem 11-43

The gears impose tangential forces and an equilibrium torque. Use torque balance between meshing gears:

`T = F_t r`

Then size the shaft using:

`sigma_VM = sqrt((32M/(pi d^3))^2 + 3(16T/(pi d^3))^2) <= sigma_allow`

### Problem 11-30

For the beam, draw the reaction FBD and determine the maximum internal shear `V_max` and bending moment `M_max`.

Allowable bending:

`sigma_max = M c / I <= 140 MPa`

Allowable shear:

`tau_max = VQ/(It) <= 90 MPa`

The maximum safe load is the smaller value obtained from bending and shear.

### Problem 11-20

For the hollow shaft:

1. Determine reactions from the overhanging load `P = 5 kN`.
2. Find the maximum bending moment.
3. For outer radius `r_o = 40 mm` and wall thickness `t`, inner radius is `r_i = r_o - t`.
4. Use:

`I = pi(r_o^4 - r_i^4)/4`

`J = pi(r_o^4 - r_i^4)/2`

5. Check:

`sigma = Mc/I <= 150 MPa`

`tau = Tc/J <= 85 MPa`

Round the required wall thickness up to the nearest millimeter.

### Problem 10-87

A-36 steel torsion design using maximum distortion energy with `FS = 1.5`.

For pure torsion:

`sigma_VM = sqrt(3) tau`

Allowable shear by von Mises:

`tau_allow = S_y/(sqrt(3) FS)`

Check both segments:

Solid segment:

`tau_s = Tc/J_s`, `J_s = pi d^4/32`

Hollow segment:

`tau_h = Tc/J_h`, `J_h = pi(d_o^4 - d_i^4)/32`

The maximum allowable torque is the smaller torque from the two segments.

## 4. Stress Transformation and Failure Theory

### Problems 10-73 and 10-74

From the figure, the plane stress state is:

`sigma_x = 560 MPa`, `tau_xy = 175 MPa`, `sigma_y = 0`

Principal stresses:

`sigma_avg = (sigma_x + sigma_y)/2`

`R = sqrt(((sigma_x - sigma_y)/2)^2 + tau_xy^2)`

`sigma_1 = sigma_avg + R`

`sigma_2 = sigma_avg - R`

Maximum shear stress theory:

`S_y >= sigma_1 - sigma_2 = 2R`

Maximum distortion energy:

`S_y >= sqrt(sigma_x^2 - sigma_x sigma_y + sigma_y^2 + 3tau_xy^2)`

### Problem 10-69

Given: concrete cylinder, `d = 50 mm`, `T = 500 N m`, axial compression `P = 2 kN`.

Area:

`A = pi d^2/4`

Polar moment:

`J = pi d^4/32`

Axial stress:

`sigma = -P/A = -1.019 MPa`

Torsional shear stress:

`tau = Tc/J = 20.372 MPa`

Principal stresses:

`sigma_1 = 19.869 MPa`

`sigma_2 = -20.887 MPa`

Since concrete is brittle, use maximum normal stress theory. Compare the largest tensile/compressive principal stress magnitude with `sigma_ult = 28 MPa`.

Conclusion: `max |sigma_i| = 20.887 MPa < 28 MPa`, so it does not fail by maximum normal stress theory.

![10-69 Mohr circle](final_graphic_solutions/10-69_mohr.png)

### Problem 10-58

Given lateral strain constraints:

`epsilon_x = epsilon_y = 0`

For isotropic material under axial stress `sigma_z`, the constrained lateral stresses satisfy:

`sigma_x = sigma_y = nu sigma_z/(1 - nu)`

The axial strain becomes:

`epsilon_z = sigma_z/E * [(1 + nu)(1 - 2nu)/(1 - nu)]`

Therefore the apparent modulus is:

`E_app = sigma_z/epsilon_z = E(1 - nu)/[(1 + nu)(1 - 2nu)]`

For `nu = 0.3`:

`E_app/E = 0.7 / (1.3*0.4) = 1.346`

The apparent stiffness increases by a factor of `1.346`.

### Problem 10-56

Thin-walled pressure vessel:

`sigma_hoop = pr/t`

`sigma_long = pr/(2t)`

Strains:

`epsilon_hoop = (sigma_hoop - nu sigma_long)/E`

`epsilon_long = (sigma_long - nu sigma_hoop)/E`

For `p = 15 MPa`, `r = 0.5 m`, `t = 10 mm`, `E = 200 GPa`, `nu = 0.3`:

`sigma_hoop = 750 MPa`

`sigma_long = 375 MPa`

`epsilon_hoop = 0.0031875`

`epsilon_long = 0.000750`

Increase in diameter:

`Delta D = epsilon_hoop D = 3.1875 mm`

Increase in length:

`Delta L = epsilon_long L = 2.25 mm`

![10-56 pressure vessel](final_graphic_solutions/10-56_pressure_vessel.png)

### Problem 10-57

For a thin pressure vessel:

`Delta V / V ≈ 2 epsilon_hoop + epsilon_long`

Using Problem 10-56:

`Delta V / V = 2(0.0031875) + 0.000750 = 0.007125`

Initial volume:

`V = pi r^2 L = pi(0.5)^2(3) = 2.356 m^3`

Volume increase:

`Delta V = 0.007125(2.356) = 0.0168 m^3`

### Problem 10-41

Rigid cavity prevents lateral expansion in `x` and `y`; top is open, so the material can expand in `z` until it reaches the top clearance. Include thermal strain:

`epsilon_i = (1/E)[sigma_i - nu(sigma_j + sigma_k)] + alpha DeltaT`

Boundary conditions:

`epsilon_x = 0`, `epsilon_y = 0`

If the top is still not contacted:

`sigma_z = 0`

Then solve for `sigma_x = sigma_y`, and compute `epsilon_z`.

If the free thermal vertical expansion exceeds the `0.3 mm` clearance, then contact occurs and an additional constraint on `epsilon_z` must be imposed.

## 5. Combined Stress Examples

### Problem 9-63

Given: helicopter rotor shaft, `d = 150 mm`, tensile force `P = 225 kN`, torque `T = 15 kN m`.

Axial stress:

`sigma = P/A = 12.732 MPa`

Torsional shear:

`tau = Tc/J = 22.635 MPa`

Principal stresses:

`sigma_1 = 29.880 MPa`

`sigma_2 = -17.147 MPa`

Maximum in-plane shear:

`tau_max = 23.514 MPa`

![9-63 Mohr circle](final_graphic_solutions/9-63_mohr.png)

### Problems 9-38, 9-39, 9-85

These problems use the same combined loading pattern:

- bending normal stress: `sigma = Mc/I`
- transverse shear stress: `tau_V = VQ/(It)` when the point is not on the outer boundary
- torsional shear stress: `tau_T = Tc/J`
- combine shear components vectorially if they act on the same plane
- use Mohr circle for principal stresses

At an outside point of a solid circular shaft, transverse shear from `V` is zero at the boundary, while torsional shear is maximum.

### Problems 9-74 and 9-75

At point `D`, first determine the internal axial force `N`, shear `V`, and bending moment `M` just to the left of the 10-kN load.

Normal stress:

`sigma_x = N/A - My/I`

Shear stress:

`tau_xy = VQ/(It)`

For stresses parallel/perpendicular to wood grain at angle `theta = 30 deg`, use stress transformation:

`sigma_theta = (sigma_x + sigma_y)/2 + (sigma_x - sigma_y)cos(2theta)/2 + tau_xy sin(2theta)`

`tau_theta = -(sigma_x - sigma_y)sin(2theta)/2 + tau_xy cos(2theta)`

For principal stresses:

`sigma_1,2 = sigma_avg +/- sqrt(((sigma_x - sigma_y)/2)^2 + tau_xy^2)`

### Problems 9-34 and 9-35

At section `a-a`, resolve the 500-N load and cable force using the arm FBD. Determine section resultants:

`N`, `V`, `M`, `T`

At point `A`:

`sigma = N/A + Mc/I`

`tau = Tc/J + VQ/(It)` if transverse shear acts at the point.

Then use Mohr circle to find principal stress and maximum in-plane shear.

### Problem 9-30

For the rectangular beam:

1. Draw the beam FBD.
2. Find reactions.
3. At the section just left of the 20-kN load, determine `N`, `V`, and `M`.
4. At points `A` and `B`:

`sigma_x = N/A - My/I`

`tau_xy = VQ/(It)`

5. Use Mohr circle for principal stresses.

### Problems 8-68 and 8-69

At a circular rod section:

`sigma_x = N/A + Mc/I`

`tau = Tc/J`

At point `A` or `B`, choose the correct sign of bending stress from the point's location on the cross section.

### Problem R8-3

Wooden frame problem. At section `b-b`, point `F`:

1. Replace the 20-kg drum by its weight `W = mg = 196.2 N`.
2. Use frame FBD to find axial force, shear, and bending moment at section `b-b`.
3. Rectangular section properties:

`A = 75 mm * 75 mm`

`I = bh^3/12`

4. Stress at `F`:

`sigma = N/A +/- Mc/I`

`tau = VQ/(It)`

### Problems 8-49, 8-31, 8-32

These are state-of-stress problems at points on circular sections:

`A = pi r^2`

`I = pi r^4/4`

`J = pi r^4/2`

Normal stress comes from axial force and bending; shear stress comes from torsion and transverse shear.

For points on the outer surface of a circular section, transverse shear due to `V` is zero at the boundary, but torsional shear is maximum.

## 6. Shear Stress Problems

### Problem 7-26

Beam: simply supported, total length `1.8 m`, loads `P` at `0.6 m` and `2P` at `1.2 m`. Rectangular section: `b = 50 mm`, `d = 100 mm`.

Reactions:

`R_A = 5P/3`

`R_B = 4P/3`

Maximum shear force:

`V_max = 5P/3`

For a rectangular section:

`tau_max = 1.5 V/A`

Area:

`A = 50(100) = 5000 mm^2`

Allowable shear:

`3 MPa = 1.5(5P/3)/5000`

`P_max = 6000 N = 6.0 kN`

![7-26 shear and moment diagrams](final_graphic_solutions/7-26_shear_moment.png)

### Problem 7-25

Cantilever rectangular beam with end load `P`.

Maximum bending stress:

`sigma_max = Mc/I = PL(h/2)/(bh^3/12) = 6PL/(bh^2)`

Maximum transverse shear stress:

`tau_max = 1.5P/(bh)`

Set `sigma_max = tau_max`:

`6PL/(bh^2) = 1.5P/(bh)`

`L = h/4`

### Problem 7-22

For an I-section web:

`tau = VQ/(I t_web)`

Use the given:

`V = 15 kN`, `w = 125 mm`, `I_NA = 0.2182(10^-3) m^4`, `y_bar = 0.1747 m`

At each point, compute `Q` as the first moment of area above or below the cut and divide by `I t`.

### Problem 7-18

For a circular rod under transverse shear, the distribution is parabolic:

`tau(y) = (4V/(3A))(1 - y^2/c^2)`

Maximum occurs at the neutral axis:

`tau_max = 4V/(3A)`

Average shear:

`tau_avg = V/A`

Ratio:

`tau_max/tau_avg = 4/3`

![7-18 shear distribution](final_graphic_solutions/7-18_shear_distribution.png)

## 7. What To Draw In Exam Solutions

For every problem, include:

1. Complete FBD with support reactions and applied loads.
2. Internal section cut at the point/section of interest.
3. Shear and bending moment diagram when a beam or shaft is involved.
4. Stress element at the requested point.
5. Mohr circle for principal stress / maximum shear questions.
6. Failure-theory comparison when material strength is given.

