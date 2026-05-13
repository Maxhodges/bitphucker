# bitphucker

A bit-crusher reduces the *number* of amplitude levels — uniform steps across the signal range. **Bitphucker** changes the *distribution* of those levels instead. Same idea (coarse quantization), but the quantization steps aren't evenly spaced.

There are two ways to do it:

- **Method 1** — louder samples keep detail, quieter samples are destroyed. A metric ton of distortion.
- **Method 2** — the inverse: quieter samples keep detail, louder samples are smashed flat. Subtle, warm, almost crackly.

## How it works

Warp the amplitude axis, quantize uniformly in the warped domain, then unwarp. Where the warp is steep the effective step is small (detail preserved); where the warp is flat the step is large (detail destroyed).

- Method 1: `x → x^shape` (steep near ±1, flat near 0) → fine resolution for loud, coarse for quiet.
- Method 2: `x → x^(1/shape)` (steep near 0, flat near ±1) → fine resolution for quiet, coarse for loud.

`shape=1.0` falls back to a plain bit-crush.

## Install

Just `numpy`. The demo also uses the stdlib `wave` module.

```
pip install numpy
```

## Use the function

```python
import numpy as np
from bitphucker import bitphucker

# audio: numpy array of float samples in [-1, 1]
# Peak-normalize first — bitphucker quantizes against a fixed [-1, 1] grid,
# so its character (especially method 2) depends on the signal hitting the rails.
peak = float(np.max(np.abs(audio)))
norm = audio / peak

# Method 1 destroys quiet content — leave headroom (8-bit) so the loud body still breathes.
# Method 2 destroys loud content — crush hard (4-bit) so the coarse plateaus are clearly audible.
harsh = bitphucker(norm, bit_depth=8, shape=3.0, method=1) * peak
warm  = bitphucker(norm, bit_depth=4, shape=3.0, method=2) * peak
```

## Run the demo

`demo.py` reads a 16-bit PCM WAV (mono or stereo), peak-normalizes it, runs both methods, and writes the renders back at the original level next to the input.

```
python3 demo.py input.wav --bit-depth 4 --shape 3.0
```

Outputs are written next to the input using this naming pattern:

```
<stem>_bitphucker_method1_<bit>bit_shape<shape>.wav
<stem>_bitphucker_method2_<bit>bit_shape<shape>.wav
```

## Listen

The two methods have different characters, so they want different bit-depths to shine:

- `jerryzhao.wav` — original
- `jerryzhao_bitphucker_method1_8bit_shape3.wav` — method 1 at 8-bit, shape 3 (gated quiet, clean loud)
- `jerryzhao_bitphucker_method2_4bit_shape3.wav` — method 2 at 4-bit, shape 3 (warm, crackly loud)

## Parameters

- `bit_depth` — number of bits of quantization. Lower = more obvious effect. The two methods have different sweet spots: **method 1** sounds best around `6–8` (the loud body has room to breathe while quiet content gates out); **method 2** sounds best around `3–4` (so the coarse loud plateaus are unmistakable). `2` is brutal in either case.
- `shape` — how aggressively the amplitude axis is warped. `1.0` = uniform (normal bit-crush). `3.0` is a strong, clearly-audible setting. Higher pushes further in whichever direction `method` chose.
- `method` — `1` (harsh, loud-detail) or `2` (warm, quiet-detail).
