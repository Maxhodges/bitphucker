"""Render method-1 and method-2 Bitphucker variants of a WAV file.

Usage:
    python3 demo.py input.wav [--bit-depth 4] [--shape 3.0]

Reads a 16-bit PCM WAV (mono or stereo) using only the stdlib `wave`
module and numpy, and writes two siblings next to the input:
    <stem>_bitphucker_method1_<bit>bit_shape<shape>.wav
    <stem>_bitphucker_method2_<bit>bit_shape<shape>.wav
"""

import argparse
import wave
from pathlib import Path

import numpy as np

from bitphucker import bitphucker


def read_wav_float(path):
    with wave.open(str(path), "rb") as w:
        sampwidth = w.getsampwidth()
        if sampwidth != 2:
            raise ValueError(f"demo.py only handles 16-bit PCM; got {sampwidth * 8}-bit")
        channels = w.getnchannels()
        sr = w.getframerate()
        frames = w.readframes(w.getnframes())
    data = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
    if channels > 1:
        data = data.reshape(-1, channels)
    return data, sr, channels


def write_wav_float(path, data, sr, channels):
    clipped = np.clip(data, -1.0, 1.0)
    pcm = (clipped * 32767.0).astype(np.int16)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(channels)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("input", help="input wav (16-bit PCM, mono or stereo)")
    ap.add_argument("--bit-depth", type=int, default=4)
    ap.add_argument("--shape", type=float, default=3.0)
    args = ap.parse_args()

    in_path = Path(args.input)
    audio, sr, channels = read_wav_float(in_path)
    stem = in_path.with_suffix("").name

    for method in (1, 2):
        out = bitphucker(audio, bit_depth=args.bit_depth, shape=args.shape, method=method)
        out_path = in_path.with_name(
            f"{stem}_bitphucker_method{method}_{args.bit_depth}bit_shape{args.shape:g}.wav"
        )
        write_wav_float(out_path, out, sr, channels)
        print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
