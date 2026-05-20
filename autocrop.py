from PIL import Image, ImageChops
import os
import glob

def trim(im):
    # Convert image to RGB
    bg = Image.new(im.mode, im.size, (255, 255, 255))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)
    return im

files = glob.glob('img/img*.jpg') + glob.glob('img/img*.png')
count = 0
for f in files:
    try:
        im = Image.open(f).convert('RGB')
        # Check if the left edge is white
        w, h = im.size
        # Sample left and right edges
        left_col = im.crop((0, 0, 5, h))
        right_col = im.crop((w-5, 0, w, h))
        
        def is_white(crop_im):
            colors = crop_im.getcolors(maxcolors=256)
            if not colors: return False
            for count, color in colors:
                if count > (crop_im.size[0] * crop_im.size[1]) * 0.9 and color[0] > 240 and color[1] > 240 and color[2] > 240:
                    return True
            return False
            
        if is_white(left_col) or is_white(right_col):
            cropped = trim(im)
            if cropped.size != im.size:
                cropped.save(f)
                count += 1
                print(f"Cropped white bars from {f}")
    except Exception as e:
        print(f"Error on {f}: {e}")

print(f"Total cropped: {count}")
