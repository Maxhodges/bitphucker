import numpy as np


def bitphucker(audio, bit_depth=4, shape=3.0, method=1):
    """Non-uniform quantizer that redistributes amplitude levels.

    Standard bit-crush: uniform steps across [-1, 1].
    Bitphucker: warp the amplitude axis, quantize uniformly in the
    warped domain, then unwarp. Where the warp is steep, the effective
    step is small (detail preserved). Where the warp is flat, the step
    is large (detail destroyed).

    method=1 — warp x -> x**shape. Flat near 0, steep near +-1.
        Quiet parts collapse, loud parts keep their shape. Harsh.
    method=2 — warp x -> x**(1/shape). Steep near 0, flat near +-1.
        Quiet parts keep detail, loud parts smash to coarse steps. Warm, crackly.

    shape=1.0 reduces to an ordinary bit-crush.
    """
    levels = 2 ** (bit_depth - 1)
    sign = np.sign(audio)
    mag = np.clip(np.abs(audio), 0.0, 1.0)

    p = shape if method == 1 else 1.0 / shape
    warped = sign * mag ** p
    quantized = np.round(warped * levels) / levels
    qsign = np.sign(quantized)
    qmag = np.clip(np.abs(quantized), 0.0, 1.0)
    return qsign * qmag ** (1.0 / p)
