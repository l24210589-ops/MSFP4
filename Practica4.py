import matplotlib.pyplot as plt
import numpy as np
import control as ctrl

x0, t0, tend, dt, w, h = 0, 0, 10, 5E-5, 7.5, 4.6
n = round((tend - t0) / dt) + 1
t = np.linspace(t0, tend, n)
Ve = np.ones(n)                         

# Datos del PID (Tune)
kP = 1298.6989
kI = 312346.1725
kD = 0.17968
N  = 4964.0941

R1, L = 1e3, 0.1

def G(C, R2):
    return ctrl.tf([L, R2], [R1 * L * C, L + R1 * R2 * C, R1 + R2])

control = G(1e-6, 100e3)                
caso    = G(1e-3, 1e3)                   

s = ctrl.tf("s")
PID = kP + kI / s if kD == 0 else kP + kI / s + kD * N * s / (s + N)
sysPID = ctrl.feedback(ctrl.series(PID, caso), 1, sign=-1)
print("Polos del lazo cerrado:", sysPID.poles())

_, Vsx = ctrl.forced_response(control, t, Ve)          
_, Vsy = ctrl.forced_response(caso, t, Ve)             
_, tratamiento = ctrl.forced_response(sysPID, t, Vsx)  

print(f"Control = {Vsx[-1]:.4f} V | Caso = {Vsy[-1]:.4f} V | "
      f"PID = {tratamiento[-1]:.4f} V (max {tratamiento.max():.4f} V)")


plt.rcParams.update({"font.family": "STIXGeneral",
                     "mathtext.fontset": "stix",
                     "font.size": 12})
clr1 = np.array([138, 99, 210]) / 255     # Ve
clr2 = np.array([201, 168, 0]) / 255      # PID (tratamiento)
clr3 = np.array([42, 26, 154]) / 255      # Caso
clr4 = np.array([0, 0, 0]) / 255          # Control

fig, ax = plt.subplots(figsize=(w, h))
ax.plot(t, Ve,  "-",  color=clr1, lw=1.2, label=r"$V_e(t)$")
ax.plot(t, tratamiento, "--", color=clr2, lw=1.2, label=r"$PID(t)$ : Tratamiento")
ax.plot(t, Vsy, ":",  color=clr3, lw=1.3, label=r"$V_{sY}(t)$ : Caso")
ax.plot(t, Vsx, "-.", color=clr4, lw=1.3, label=r"$V_{sX}(t)$ : Control")

ax.set_xlim(0, 10);  ax.set_xticks(np.arange(0, 11, 1))
ax.set_ylim(-0.2, 1.2);  ax.set_yticks(np.arange(-0.2, 1.21, 0.2))
ax.set_xlabel(r"$t$ [s]")
ax.set_ylabel(r"$V_e(t)$ [V]")
ax.tick_params(direction="in", top=True, right=True)
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.03), ncol=4,
          frameon=True, fancybox=False, edgecolor="k",
          prop={"style": "italic", "size": 10},
          handlelength=2.2, columnspacing=1.0)

fig.savefig("Caso.pdf", bbox_inches="tight")
plt.show()