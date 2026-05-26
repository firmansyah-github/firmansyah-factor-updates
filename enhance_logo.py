from PIL import Image, ImageEnhance
import glob

files = glob.glob("Screenshot*8.38.25*.png")
file = files[0]
img = Image.open(file).convert("RGBA")

# Upscale to retain quality
img = img.resize((img.width * 4, img.height * 4), Image.Resampling.LANCZOS)

datas = img.getdata()
new_data = []

for item in datas:
    r, g, b, a = item
    # Distance to white
    dist = ((255 - r)**2 + (255 - g)**2 + (255 - b)**2) ** 0.5
    
    if dist < 20:
        new_data.append((r, g, b, 0)) # Fully transparent
    elif dist < 100:
        alpha = int(((dist - 20) / 80.0) * 255)
        new_data.append((r, g, b, alpha))
    else:
        new_data.append((r, g, b, 255))

img.putdata(new_data)

# Sharpen
img = ImageEnhance.Sharpness(img).enhance(2.5)
img = ImageEnhance.Contrast(img).enhance(1.1)

img.save('logo.png')
print("Successfully enhanced logo and saved to logo.png")
