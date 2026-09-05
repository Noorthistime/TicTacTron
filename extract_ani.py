import os
import struct
from PIL import Image
import io

ani_path = r"C:\Users\Noor  Mohammad\Downloads\Night_Diamond_Ruby_Red_v3_0_Cursor_Pack\Night Diamond v3.0 - Ruby Red\[RR] Diagonal Resize 1 v3.0.ani"

with open(ani_path, 'rb') as f:
    data = f.read()

if data[:4] != b'RIFF' or data[8:12] != b'ACON':
    print("Not a valid ANI file")
    exit(1)

frames = []
offset = 12
while offset < len(data):
    chunk_id = data[offset:offset+4]
    chunk_size = struct.unpack('<I', data[offset+4:offset+8])[0]
    
    if chunk_id == b'LIST':
        list_type = data[offset+8:offset+12]
        if list_type == b'fram':
            sub_offset = offset + 12
            end_offset = offset + 8 + chunk_size
            while sub_offset < end_offset:
                sub_id = data[sub_offset:sub_offset+4]
                sub_size = struct.unpack('<I', data[sub_offset+4:sub_offset+8])[0]
                if sub_id == b'icon':
                    icon_data = data[sub_offset+8:sub_offset+8+sub_size]
                    try:
                        img = Image.open(io.BytesIO(icon_data))
                        frames.append(img.copy())
                    except Exception as e:
                        print("Failed to open icon:", e)
                # Pad to 2 bytes
                actual_sub_size = sub_size + (sub_size % 2)
                sub_offset += 8 + actual_sub_size
    
    # Pad to 2 bytes
    actual_size = chunk_size + (chunk_size % 2)
    offset += 8 + actual_size

print(f"Extracted {len(frames)} frames")

if frames:
    # Find max dimensions
    max_w = max(f.width for f in frames)
    max_h = max(f.height for f in frames)
    
    # Create sprite sheet
    sheet = Image.new('RGBA', (max_w * len(frames), max_h), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        sheet.paste(f, (i * max_w, 0))
        
    sheet.save("idk_cursor_sprite.png")
    print(f"Saved sprite sheet: {max_w * len(frames)}x{max_h}")
