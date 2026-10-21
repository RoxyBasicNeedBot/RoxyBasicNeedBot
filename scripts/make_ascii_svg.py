import sys
import os
from PIL import Image

# Brightness ramp: space for pure white/background, dense characters for dark areas
RAMP = " .`:-=+*cs#%@"

def image_to_ascii(image_path, target_width=88, char_aspect_ratio=0.47):
    """
    Loads prepped image, resizes it compensating for monospace aspect ratio,
    and returns list of strings (one per row).
    """
    img = Image.open(image_path).convert("L")
    w, h = img.size
    aspect_ratio = w / h
    
    # Calculate target height based on aspect ratio and char width/height ratio
    # target_width = target_height * (char_width / char_height) * aspect_ratio
    # target_height = target_width * char_aspect_ratio / aspect_ratio
    target_height = int((target_width * char_aspect_ratio) / aspect_ratio)
    
    # Enforce minimum height/width and prevent extreme values
    target_height = max(10, min(target_height, 70))
    
    print(f"Resizing image from {w}x{h} to character grid {target_width}x{target_height}...")
    img_resized = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    
    ascii_rows = []
    for y in range(target_height):
        row = ""
        for x in range(target_width):
            val = img_resized.getpixel((x, y))
            # Map 255 (white) -> 0 (space) and 0 (black) -> len(RAMP)-1 (@)
            ramp_idx = int((255 - val) / 255.0 * (len(RAMP) - 1))
            row += RAMP[ramp_idx]
        ascii_rows.append(row)
        
    return ascii_rows

def make_svg(ascii_rows, output_path="avi-ascii.svg", text_color="#e2e8f0", bg_color="#0d111b"):
    """
    Generates an animated, self-typing SVG from the ASCII rows.
    """
    num_rows = len(ascii_rows)
    if num_rows == 0:
        return
        
    row_width_chars = len(ascii_rows[0])
    
    # Font metrics constants
    char_w = 4.2
    char_h = 9.0
    padding_x = 10
    padding_y = 15
    
    svg_width = int(row_width_chars * char_w + padding_x * 2)
    svg_height = int(num_rows * char_h + padding_y * 2)
    
    # Staggered animation values
    start_delay = 0.2
    row_dur = 0.05  # seconds per row
    
    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="100%" height="100%">')
    svg.append('  <style>')
    svg.append(f'    rect.bg {{ fill: {bg_color}; stroke: #2e274a; stroke-width: 1.5; }}')
    svg.append(f'    text.ascii {{ font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace; font-size: 7.2px; fill: {text_color}; white-space: pre; }}')
    svg.append('    rect.cursor {{ fill: #06b6d4; }}')
    svg.append('  </style>')
    
    # Background
    svg.append(f'  <rect class="bg" width="{svg_width}" height="{svg_height}" rx="14" />')
    
    # Define ClipPaths for each row
    svg.append('  <defs>')
    for i, row in enumerate(ascii_rows):
        y_pos = padding_y + i * char_h
        # Calculate pixels for row contents (ignoring trailing spaces for cleaner clip/cursor animation)
        trimmed_len = len(row.rstrip())
        row_pixel_width = max(0.0, trimmed_len * char_w)
        delay = round(start_delay + i * row_dur, 3)
        
        svg.append(f'    <clipPath id="clip-{i}">')
        # Rect for clipping the row text. Slides width from 0 to full row length.
        svg.append(f'      <rect x="{padding_x}" y="{y_pos - 7.5}" width="0" height="10">')
        svg.append(f'        <animate attributeName="width" from="0" to="{row_pixel_width}" dur="{row_dur}s" begin="{delay}s" fill="freeze" />')
        svg.append('      </rect>')
        svg.append('    </clipPath>')
    svg.append('  </defs>')
    
    # Draw texts and cursors
    for i, row in enumerate(ascii_rows):
        y_pos = padding_y + i * char_h
        trimmed_len = len(row.rstrip())
        row_pixel_width = max(0.0, trimmed_len * char_w)
        delay = round(start_delay + i * row_dur, 3)
        
        # XML escape the text row
        escaped_row = row.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
        
        # The text element clipped by our path
        svg.append(f'  <text class="ascii" x="{padding_x}" y="{y_pos}" clip-path="url(#clip-{i})">{escaped_row}</text>')
        
        # Cursor rect if there's text to type
        if row_pixel_width > 0:
            svg.append(f'  <rect class="cursor" x="{padding_x}" y="{y_pos - 7}" width="4" height="8" opacity="0">')
            svg.append(f'    <animate attributeName="x" from="{padding_x}" to="{padding_x + row_pixel_width}" dur="{row_dur}s" begin="{delay}s" fill="freeze" />')
            # Cursor only visible while typing this specific row
            svg.append(f'    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.9;1" dur="{row_dur}s" begin="{delay}s" fill="freeze" />')
            svg.append('  </rect>')
            
    svg.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
    print(f"Successfully generated {output_path}")

def main():
    prepped_photo = "source-prepped.png"
    if not os.path.exists(prepped_photo):
        print(f"Error: {prepped_photo} not found. Please run prep_photo.py first.")
        sys.exit(1)
        
    ascii_rows = image_to_ascii(prepped_photo, target_width=88)
    make_svg(ascii_rows, "avi-ascii.svg")

if __name__ == "__main__":
    main()
