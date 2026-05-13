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
from bitphucker import bitphucker

# audio: numpy array of float samples in [-1, 1]
harsh = bitphucker(audio, bit_depth=4, shape=3.0, method=1)
warm  = bitphucker(audio, bit_depth=4, shape=3.0, method=2)
```

## Run the demo

`demo.py` reads a 16-bit PCM WAV (mono or stereo) and writes a method-1 and method-2 render next to it.

```
python3 demo.py input.wav --bit-depth 4 --shape 3.0
```

Outputs:

```
input_bitphucker_method1_4bit_shape3.wav
input_bitphucker_method2_4bit_shape3.wav
```

## Listen

Before/after at 6 bits, shape 8.0. Source is peak-normalized before processing (the source has peak 0.857, so this is a 1.34 dB lift) and output is scaled back to original level for a fair A/B.

- `jerryzhao.wav` — original
- `jerryzhao_bitphucker_method1_6bit_shape8_peaknorm.wav` — method 1 (harsh)
- `jerryzhao_bitphucker_method2_6bit_shape8_peaknorm.wav` — method 2 (warm, crackly)

## Parameters

- `bit_depth` — number of bits of quantization. Lower = more obvious effect. `4` is a good starting point; `2` is brutal.
- `shape` — how aggressively the amplitude axis is warped. `1.0` = uniform (normal bit-crush). `3.0` is a strong, clearly-audible setting. Higher pushes further in whichever direction `method` chose.
- `method` — `1` (harsh, loud-detail) or `2` (warm, quiet-detail).
