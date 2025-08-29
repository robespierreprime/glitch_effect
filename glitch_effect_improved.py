#!/usr/bin/env python3
"""
Simplified and improved image glitch effect generator.
Creates digital glitch artifacts through pixel shifting and JPEG compression.
"""

from PIL import Image
import numpy as np
import random
import io
from pathlib import Path
import argparse


class GlitchEffect:
    """Simple and efficient image glitch effect generator."""

    def __init__(
        self,
        shift_intensity=10,
        line_width=3,
        glitch_probability=0.8,
        jpeg_quality=30,
        shift_angle=0,
    ):
        self.shift_intensity = shift_intensity
        self.line_width = line_width
        self.glitch_probability = glitch_probability
        self.jpeg_quality = jpeg_quality
        self.shift_angle = shift_angle

    def angled_shift_glitch(self, image_array):
        """Apply pixel shifting along angled lines."""
        result = image_array.copy()
        height, width = image_array.shape[:2]

        # Skip if no shift intensity
        if self.shift_intensity == 0:
            return result

        # Convert angle to radians
        angle_rad = np.radians(self.shift_angle)
        dx = np.cos(angle_rad)
        dy = np.sin(angle_rad)

        # If angle is 0, use simple horizontal shifts for efficiency
        if abs(self.shift_angle) < 0.1:
            return self._horizontal_shift_simple(image_array)

        # Ensure minimum line width
        effective_line_width = max(1, self.line_width)

        # For angled shifts, process along oriented lines
        for line_idx in range(0, max(height, width), effective_line_width):
            if random.random() < self.glitch_probability:
                shift_amount = random.randint(
                    -self.shift_intensity, self.shift_intensity
                )

                # Skip if no actual shift
                if shift_amount == 0:
                    continue

                # Calculate line positions
                for pos in range(max(height, width)):
                    # Starting position on the line
                    if abs(dx) > abs(dy):  # More horizontal than vertical
                        x = pos
                        y = (
                            int(line_idx + (pos - width // 2) * dy / dx)
                            if dx != 0
                            else line_idx
                        )
                    else:  # More vertical than horizontal
                        y = pos
                        x = (
                            int(line_idx + (pos - height // 2) * dx / dy)
                            if dy != 0
                            else line_idx
                        )

                    # Calculate shifted position
                    shift_x = int(x + shift_amount * dx)
                    shift_y = int(y + shift_amount * dy)

                    # Apply shift if both positions are valid
                    if (
                        0 <= x < width
                        and 0 <= y < height
                        and 0 <= shift_x < width
                        and 0 <= shift_y < height
                    ):

                        # Apply line thickness
                        for thickness in range(effective_line_width):
                            thick_offset = thickness - effective_line_width // 2

                            # Perpendicular direction for thickness
                            perp_x = int(x - thick_offset * dy)
                            perp_y = int(y + thick_offset * dx)
                            perp_shift_x = int(shift_x - thick_offset * dy)
                            perp_shift_y = int(shift_y + thick_offset * dx)

                            if (
                                0 <= perp_x < width
                                and 0 <= perp_y < height
                                and 0 <= perp_shift_x < width
                                and 0 <= perp_shift_y < height
                            ):
                                result[perp_shift_y, perp_shift_x] = image_array[
                                    perp_y, perp_x
                                ]

        return result

    def _horizontal_shift_simple(self, image_array):
        """Optimized horizontal shifting when angle is 0."""
        result = image_array.copy()
        height, width = image_array.shape[:2]

        # Skip if no shift intensity
        if self.shift_intensity == 0:
            return result

        # Ensure minimum line width
        effective_line_width = max(1, self.line_width)

        # Vectorized approach for better performance
        for y in range(0, height, effective_line_width):
            if random.random() < self.glitch_probability:
                shift = random.randint(-self.shift_intensity, self.shift_intensity)

                # Skip if no actual shift
                if shift == 0:
                    continue

                # Process multiple rows at once
                end_row = min(y + effective_line_width, height)
                rows_to_process = slice(y, end_row)

                if shift > 0:
                    result[rows_to_process, shift:] = image_array[
                        rows_to_process, :-shift
                    ]
                elif shift < 0:
                    result[rows_to_process, :shift] = image_array[
                        rows_to_process, -shift:
                    ]

        return result

    def color_channel_shift(self, image_array):
        """Shift individual color channels for chromatic aberration effect."""
        result = image_array.copy()

        for channel in range(3):  # RGB channels
            if random.random() < 0.6:  # 60% chance per channel
                shift = random.randint(-3, 3)
                if shift != 0:
                    if shift > 0:
                        result[:, shift:, channel] = image_array[:, :-shift, channel]
                    else:
                        result[:, :shift, channel] = image_array[:, -shift:, channel]

        return result

    def jpeg_corruption(self, image):
        """Apply JPEG compression artifacts."""
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=self.jpeg_quality)
        buffer.seek(0)
        return Image.open(buffer)

    def apply_glitch_to_array(self, img_array):
        """Apply glitch effects to a numpy array (for reuse)."""
        # Apply effects
        arr = self.angled_shift_glitch(img_array)
        arr = self.color_channel_shift(arr)

        # Convert back to image
        glitched_img = Image.fromarray(arr.astype(np.uint8))

        # Apply JPEG corruption
        glitched_img = self.jpeg_corruption(glitched_img)

        return glitched_img

    def apply_glitch(self, input_path, output_path=None):
        """Apply complete glitch effect to an image."""
        # Load image
        img = Image.open(input_path).convert("RGB")
        arr = np.array(img)

        # Apply effects using the reusable method
        glitched_img = self.apply_glitch_to_array(arr)

        # Save result
        if output_path is None:
            input_path = Path(input_path)
            output_path = (
                input_path.parent / f"{input_path.stem}_glitched{input_path.suffix}"
            )

        glitched_img.save(output_path)
        print(f"Glitched image saved to: {output_path}")
        return output_path


def main():
    """Command line interface for the glitch effect."""
    parser = argparse.ArgumentParser(description="Apply glitch effects to images")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("-o", "--output", help="Output image path")
    parser.add_argument(
        "-s", "--shift", type=int, default=10, help="Shift intensity (default: 10)"
    )
    parser.add_argument(
        "-w", "--width", type=int, default=3, help="Line width (default: 3)"
    )
    parser.add_argument(
        "-p",
        "--probability",
        type=float,
        default=0.8,
        help="Glitch probability (default: 0.8)",
    )
    parser.add_argument(
        "-q", "--quality", type=int, default=30, help="JPEG quality (default: 30)"
    )
    parser.add_argument(
        "-a",
        "--angle",
        type=float,
        default=0,
        help="Shift angle in degrees (default: 0)",
    )

    args = parser.parse_args()

    # Create glitch effect with parameters
    glitch = GlitchEffect(
        shift_intensity=args.shift,
        line_width=args.width,
        glitch_probability=args.probability,
        jpeg_quality=args.quality,
        shift_angle=args.angle,
    )

    # Apply effect
    glitch.apply_glitch(args.input, args.output)


if __name__ == "__main__":
    main()
