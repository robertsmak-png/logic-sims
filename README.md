# LOGIC sims

Simulations behind the **LOGIC** animation series by [Robert Smak](https://www.linkedin.com/in/robertsmak) (PLC LOGIC, FLOW LOGIC, MOTION LOGIC).
Every number shown in the videos comes from a simulation like these - not typed in by hand.

## MOTION LOGIC E01 - crane anti-sway

`crane_antisway.py` - pendulum on a trolley (rope 4 m, 8 m travel, 1 m/s, damping ratio 0.05), three commands:

| case | trolley stops | sway after stop | load ready (< 3 cm) |
|---|---|---|---|
| plain trapezoid (0.5 m/s²) | 10.0 s | 17.7 cm | 32.3 s |
| same ramp, ZV shaped | 12.0 s | 1.3 cm | 12.0 s |
| faster ramp (2 m/s²), ZV shaped | 10.5 s | 2.0 cm | 10.5 s |

With 0.5 m/s² the ramp time (2 s) equals half the swing period, so the two ZV half-impulses merge into one ramp lasting exactly one swing period - which is why the video shows a single, longer ramp. `zv_short` shows the classic two-step profile.

Simplifications: point-mass pendulum, fixed rope length, undamped ZV (50/50) instead of damping-corrected weights.

```
python crane_antisway.py          # results
python crane_antisway.py --plot   # speed + sway plots (matplotlib)
```

Suggestions and pull requests welcome.
