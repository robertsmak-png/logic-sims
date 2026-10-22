"""
Crane anti-sway (input shaping) - MOTION LOGIC E01 by Robert Smak.

Pendulum on a trolley. Same 8 m move, three commands:
  plain   - trapezoidal speed profile
  zv      - the same profile, ZV input shaped (two half impulses, second one half a swing period later)
  zv_short- ZV shaping on a faster ramp, where the two halves are visible

Run:  python crane_antisway.py           (prints results)
      python crane_antisway.py --plot    (needs matplotlib)
"""
import math
import sys

G = 9.81
ROPE = 4.0        # m
DIST = 8.0        # m
VMAX = 1.0        # m/s
DAMP = 0.05       # pendulum damping ratio
TOL = 0.03        # lower the load when |sway| < 3 cm
DT = 0.001

W = math.sqrt(G / ROPE)
T = 2 * math.pi / W          # swing period, ~4.01 s


def trapezoid(accel):
    ta = VMAX / accel
    tc = DIST / VMAX - ta
    def a(t):
        if t < 0: return 0.0
        if t < ta: return accel
        if t < ta + tc: return 0.0
        if t < 2 * ta + tc: return -accel
        return 0.0
    return a, 2 * ta + tc


def zv(acc_fn, end):
    # classic ZV shaper (undamped): 50 % now + 50 % half a period later
    return (lambda t: 0.5 * acc_fn(t) + 0.5 * acc_fn(t - T / 2)), end + T / 2


def simulate(acc_fn, stop, until=60.0):
    th = om = v = x = 0.0
    t = 0.0
    rows = []
    while t < until:
        a = acc_fn(t)
        al = -(G / ROPE) * math.sin(th) - 2 * DAMP * W * om - (a / ROPE) * math.cos(th)
        om += al * DT
        th += om * DT
        v += a * DT
        x += v * DT
        rows.append((t, x, v, a, ROPE * math.sin(th)))
        t += DT
    sway_after = max(abs(r[4]) for r in rows if stop <= r[0] < stop + T)
    ready = stop
    for r in reversed(rows):
        if abs(r[4]) > TOL:
            ready = max(stop, r[0])
            break
    return rows, sway_after, ready


CASES = {
    'plain':    trapezoid(0.5),
    'zv':       zv(*trapezoid(0.5)),
    'zv_short': zv(*trapezoid(2.0)),
}

if __name__ == '__main__':
    print(f'rope {ROPE} m, swing period {T:.2f} s, half period {T/2:.2f} s')
    res = {}
    for name, (fn, stop) in CASES.items():
        rows, sway, ready = simulate(fn, stop)
        res[name] = rows
        print(f'{name:9s} trolley stops {stop:5.2f} s | sway after stop {sway*100:5.1f} cm | load ready {ready:5.2f} s')
    print('\nNote: with accel 0.5 m/s^2 the ramp time (2 s) equals half a swing period,')
    print('so the two ZV halves merge into ONE ramp lasting one full period - same physics.')
    print("'zv_short' uses a faster ramp so the two steps are visible.")
    if '--plot' in sys.argv:
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(2, 1, figsize=(9, 6), sharex=True)
        for name, rows in res.items():
            ts = [r[0] for r in rows]
            ax[0].plot(ts, [r[2] for r in rows], label=name)
            ax[1].plot(ts, [r[4] * 100 for r in rows], label=name)
        ax[0].set_ylabel('trolley speed [m/s]'); ax[1].set_ylabel('sway [cm]'); ax[1].set_xlabel('time [s]')
        ax[0].legend(); ax[0].set_xlim(0, 30); plt.tight_layout(); plt.show()
