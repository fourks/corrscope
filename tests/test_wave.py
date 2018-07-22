import warnings

import numpy as np

import pytest

from ovgenpy.wave import Wave


prefix = 'tests/wav-formats/'
wave_paths = [
    # 2000 samples, with a full-scale peak at data[1000].
    'u8-impulse1000.wav',
    's16-impulse1000.wav',
    's32-impulse1000.wav',
    'f32-impulse1000.wav',
    'f64-impulse1000.wav',
]


@pytest.mark.parametrize("wave_path", wave_paths)
def test_wave(wave_path):
    with warnings.catch_warnings(record=True) as w:
        # Cause all warnings to always be triggered.
        warnings.simplefilter("always")

        wave = Wave(None, prefix + wave_path)
        data = wave[:]

        # Audacity dithers <=16-bit WAV files upon export, creating a few bits of noise.
        # As a result, amin(data) <= 0.
        assert -0.01 < np.amin(data) <= 0
        assert 0.99 < np.amax(data) <= 1

        # check for FutureWarning (raised when determining wavfile type)
        warns = [o for o in w if issubclass(o.category, FutureWarning)]
        assert not [str(w) for w in warns]