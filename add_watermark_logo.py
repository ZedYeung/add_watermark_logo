#! python3
import os
from PIL import Image
import argparse

# commandline args
parser = argparse.ArgumentParser(description="Batch adding logo on your photos", formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('folder', default='.', help="folder having photo to add logo, default is current folder")
parser.add_argument('logo', help="where is your logo?")
parser.add_argument('-o', '--output', help="output folder to save photo with logo")
parser.add_argument('-s', '--size', nargs=2, help="logo size, {format: width height}, default is the original size")
parser.add_argument('-p', '--pos', nargs=2, default=[0, 0],
help="""{format: horizental-margin vertical-margin}
if horizental-margin > 0, it's left-margin, else is right-margin
if vertical-margin > 0, it's top-margin, else it's bottom-margin
default is 0 0, which means the right bottom
""")

# get args
args = parser.parse_args()

FOLDER = args.folder
OUTPUT = args.output
LOGO = args.logo
SIZE = args.size
POS = args.pos

logo = Image.open(LOGO)

Horizontal_Margin = int(POS[0])
Vertical_Margin = int(POS[1])

if SIZE:
    logoWidth = int(SIZE[0])
    logoHeight = int(SIZE[1])
    logo = logo.resize((logoWidth, logoHeight))
else:
    logoWidth, logoHeight = logo.size

os.chdir(FOLDER)

# Loop over all files in the working directory.
for filename in os.listdir(FOLDER):
    if not (filename.endswith('.png') or filename.endswith('.jpg')):
        continue # skip non-image files
    im = Image.open(filename)
    width, height = im.size

    # get the logo position--left top corner
    if Horizontal_Margin > 0:
        logo_x = Horizontal_Margin
    else:
        logo_x = width - logoWidth - Horizontal_Margin
    if Vertical_Margin > 0:
        logo_y = Vertical_Margin
    else:
        logo_y = height - logoHeight - Vertical_Margin

    # Add logo.
    print('Adding logo to {photo}'.format(photo=filename))
    im.paste(logo, (logo_x, logo_y), logo)

    # Save changes.
    if OUTPUT:
        im.save(os.path.join(OUTPUT, filename))
    else:
        os.makedirs('withLogo', exist_ok=True)
        im.save(os.path.join('withLogo', filename))
print('Done')
