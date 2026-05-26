from PIL import Image
import glob

# Try to find the original screenshot to work from a clean slate
files = glob.glob("Screenshot*8.38.25*.png")
if not files:
    print("No original screenshot found.")
    exit(1)

file = files[0]
img = Image.open(file).convert("RGBA")

# Upscale to make it "crystal clear"
img = img.resize((img.width * 8, img.height * 8), Image.Resampling.LANCZOS)

datas = img.getdata()
new_data = []

# Better background removal: make all white and near-white pixels completely transparent
for item in datas:
    r, g, b, a = item
    
    # If the pixel is very bright (white-ish), we make it transparent
    if r > 245 and g > 245 and b > 245:
        new_data.append((255, 255, 255, 0)) # Fully transparent
    elif r > 200 and g > 200 and b > 200:
        # For anti-aliased edges, we calculate a soft alpha mask based on how white it is
        # Calculate brightness from 200 to 255 -> alpha from 255 to 0
        brightness = (r + g + b) / 3.0
        alpha = int(((245 - brightness) / 45.0) * 255)
        new_data.append((r, g, b, alpha))
    else:
        new_data.append((r, g, b, 255))

img.putdata(new_data)

# Save it as logo.png
img.save('logo.png', "PNG")
print("Saved perfect transparent logo.")
