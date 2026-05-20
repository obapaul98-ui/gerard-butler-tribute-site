from PIL import Image
im = Image.open('img/img001.jpg').convert('RGB')
print(f"Size: {im.size}")
left = im.crop((0, 0, 10, im.size[1]))
top = im.crop((0, 0, im.size[0], 10))
print("Top 10 pixels colors:")
print(top.getcolors(maxcolors=256))
