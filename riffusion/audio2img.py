from pathlib import Path
import argh
import numpy as np
import pydub
from PIL import Image

from riffusion.spectrogram_image_converter import SpectrogramImageConverter
from riffusion.spectrogram_params import SpectrogramParams
from riffusion.util import image_util

def audio_to_image(
    audio: str,
    image: str,
    step_size_ms: int = 10,
    num_frequencies: int = 512,
    min_frequency: int = 0,
    max_frequency: int = 10000,
    window_duration_ms: int = 100,
    padded_duration_ms: int = 400,
    power_for_image: float = 0.25,
    stereo: bool = False,
    device: str = "cuda",
):
    """
    Compute a spectrogram image from a waveform.
    """
    segment = pydub.AudioSegment.from_file(audio)

    params = SpectrogramParams(
        sample_rate=segment.frame_rate,
        stereo=stereo,
        window_duration_ms=window_duration_ms,
        padded_duration_ms=padded_duration_ms,
        step_size_ms=step_size_ms,
        min_frequency=min_frequency,
        max_frequency=max_frequency,
        num_frequencies=num_frequencies,
        power_for_image=power_for_image,
    )

    converter = SpectrogramImageConverter(params=params, device=device)
    pil_image = converter.spectrogram_image_from_audio(segment)
    pil_image.save(image, exif=pil_image.getexif(), format="PNG")
