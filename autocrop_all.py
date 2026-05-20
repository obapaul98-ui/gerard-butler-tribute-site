from PIL import Image, ImageChops
import os
import glob

def trim(im):
    # Try trimming white border
    bg_white = Image.new(im.mode, im.size, (255, 255, 255))
    diff_w = ImageChops.difference(im, bg_white)
    diff_w = ImageChops.add(diff_w, diff_w, 2.0, -100)
    bbox_w = diff_w.getbbox()
    
    # Try trimming black border
    bg_black = Image.new(im.mode, im.size, (0, 0, 0))
    diff_b = ImageChops.difference(im, bg_black)
    diff_b = ImageChops.add(diff_b, diff_b, 2.0, -100)
    bbox_b = diff_b.getbbox()
    
    # We want the tightest crop. If there's a white border, bbox_w will be smaller.
    # If there's a black border, bbox_b will be smaller.
    orig_area = im.size[0] * im.size[1]
    
    area_w = (bbox_w[2] - bbox_w[0]) * (bbox_w[3] - bbox_w[1]) if bbox_w else orig_area
    area_b = (bbox_b[2] - bbox_b[0]) * (bbox_b[3] - bbox_b[1]) if bbox_b else orig_area
    
    if area_w < orig_area and area_w <= area_b:
        return im.crop(bbox_w)
    elif area_b < orig_area and area_b < area_w:
        return im.crop(bbox_b)
        
    return im

files = glob.glob('img/img*.jpg') + glob.glob('img/img*.png') + glob.glob('img/*.jpg')
count = 0
for f in files:
    try:
        im = Image.open(f).convert('RGB')
        
        # Check if the top/bottom/left/right edge is white or black
        w, h = im.size
        top_row = im.crop((0, 0, w, 5))
        bottom_row = im.crop((0, h-5, w, h))
        left_col = im.crop((0, 0, 5, h))
        right_col = im.crop((w-5, 0, w, h))
        
        def is_solid_color(crop_im):
            colors = crop_im.getcolors(maxcolors=256)
            if not colors: return False
            for c, color in colors:
                if c > (crop_im.size[0] * crop_im.size[1]) * 0.8:
                    # If it's mostly white
                    if color[0] > 240 and color[1] > 240 and color[2] > 240: return True
                    # If it's mostly black
                    if color[0] < 15 and color[1] < 15 and color[2] < 15: return True
            return False
            
        if is_solid_color(top_row) or is_solid_color(bottom_row) or is_solid_color(left_col) or is_solid_color(right_col):
            cropped = trim(im)
            if cropped.size != im.size:
                cropped.save(f, quality=95)
                count += 1
                print(f"Cropped borders from {f}")
    except Exception as e:
        pass

print(f"Total cropped: {count}")
