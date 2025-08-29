#!/usr/bin/env python3
"""
Example usage of the Glitch Effect Generator.
Demonstrates different glitch styles and batch processing.
"""

from glitch_effect_improved import GlitchEffect
from PIL import Image
from pathlib import Path

def create_sample_effects():
    """Create sample glitch effects with different styles."""
    
    # Check if we have any input images
    input_dir = Path('input')
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
        image_files.extend(input_dir.glob(ext))
    
    if not image_files:
        print("No images found in input/ directory")
        print("Please add some images to the input/ directory first")
        return
    
    # Use the first image as example
    input_image = image_files[0]
    print(f"Using {input_image.name} as example")
    
    try:
        image = Image.open(input_image)
        output_dir = Path('output')
        
        # Define different glitch styles
        styles = {
            'subtle': GlitchEffect(
                shift_intensity=5,
                shift_angle=0,
                line_width=1,
                glitch_probability=0.3,
                jpeg_quality=70
            ),
            'vhs': GlitchEffect(
                shift_intensity=15,
                shift_angle=10,
                line_width=3,
                glitch_probability=0.6,
                jpeg_quality=40
            ),
            'datamosh': GlitchEffect(
                shift_intensity=25,
                shift_angle=30,
                line_width=5,
                glitch_probability=0.8,
                jpeg_quality=20
            ),
            'extreme': GlitchEffect(
                shift_intensity=40,
                shift_angle=-45,
                line_width=8,
                glitch_probability=0.9,
                jpeg_quality=10
            )
        }
        
        # Generate each style
        import numpy as np
        image_array = np.array(image)
        
        for style_name, glitch in styles.items():
            print(f"Creating {style_name} glitch...")
            
            result = glitch.apply_glitch_to_array(image_array)
            output_path = output_dir / f"{style_name}_{input_image.stem}.jpg"
            result.save(output_path, quality=95)
            
            print(f"Saved: {output_path}")
        
        print(f"\nCreated 4 different glitch styles in output/ directory")
        
    except Exception as e:
        print(f"Error processing image: {e}")

def batch_process_example():
    """Example of batch processing all images in input directory."""
    
    input_dir = Path('input')
    output_dir = Path('output')
    
    # Create a consistent glitch effect for batch processing
    glitch = GlitchEffect(
        shift_intensity=15,
        shift_angle=20,
        line_width=3,
        glitch_probability=0.7,
        jpeg_quality=30
    )
    
    # Process all images
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG']:
        image_files.extend(input_dir.glob(ext))
    
    if not image_files:
        print("No images found in input/ directory for batch processing")
        return
    
    print(f"Batch processing {len(image_files)} images...")
    
    for image_file in image_files:
        try:
            import numpy as np
            image = Image.open(image_file)
            image_array = np.array(image)
            result = glitch.apply_glitch_to_array(image_array)
            
            output_path = output_dir / f"batch_{image_file.name}"
            result.save(output_path, quality=95)
            
            print(f"Processed: {image_file.name}")
            
        except Exception as e:
            print(f"Error processing {image_file.name}: {e}")
    
    print("Batch processing complete.")

def main():
    """Run example demonstrations."""
    print("Glitch Effect Generator - Examples")
    print("=" * 40)
    
    # Ensure output directory exists
    Path('output').mkdir(exist_ok=True)
    
    print("\n1. Creating sample glitch styles...")
    create_sample_effects()
    
    print("\n2. Batch processing example...")
    batch_process_example()
    
    print("\nCheck the output/ directory to see the results.")
    print("Tip: Try different parameters in glitch_effect_improved.py for custom effects")

if __name__ == "__main__":
    main()