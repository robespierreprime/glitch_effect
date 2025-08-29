# Glitch Effect Generator

Python library for creating digital glitch effects on images.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Basic usage
python glitch_effect_improved.py input/image.jpg -o output/glitched.jpg

# With parameters
python glitch_effect_improved.py input/image.jpg -o output/glitched.jpg -s 20 -a 15 -w 4 -p 0.8 -q 25

# Batch process
python glitch_effect_improved.py input/ -o output/
```

## Python API

```python
from glitch_effect_improved import GlitchEffect

glitch = GlitchEffect(shift_intensity=15, shift_angle=30)
result = glitch.apply_glitch_to_array(image_array)
```

## Parameters

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| `-s, --shift` | 0-50 | 10 | Pixel displacement |
| `-a, --angle` | -90 to 90 | 0 | Shift direction |
| `-w, --width` | 1-10 | 3 | Line thickness |
| `-p, --probability` | 0.0-1.0 | 0.8 | Coverage amount |
| `-q, --quality` | 1-95 | 30 | JPEG compression |

## Requirements

```
Pillow>=9.0.0
numpy>=1.21.0
```
