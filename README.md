# Sega Genesis Slide Generator and Viewer

Copyright (c) 2024 Joey Parrish

See MIT License in LICENSE.txt


## Overview

Create a Sega Genesis / Mega Drive ROM from a PDF of a slide show.

Export the slides as a PDF, then run this tool to generate a ROM.

Burn the ROM to a flash cart, or run in an emulator.

Press left or right on the Sega to move through slides.

Requires ImageMagick and pdftoppm to convert images, and Docker to compile the
ROM using SGDK.  The generator script is written in Python.  On Ubuntu, install
packages "python3", "imagemagick", "poppler-utils", and "docker.io".


## Usage

```
sudo apt -y install python3 imagemagick poppler-utils docker.io

# All pages
./generate.py slides.pdf slides.rom

# A subset of pages (1-based page numbers)
./generate.py slides.pdf@1-21 slides.rom
```


## Links

 - [SGDK](https://github.com/Stephane-D/SGDK): A free and open development kit
   for Sega Mega Drive.
 - [Poppler](https://poppler.freedesktop.org/): A PDF rendering library based
   on the xpdf-3.0 code base.
 - [ImageMagick](https://imagemagick.org/): A free, open-source software suite
   used for editing and manipulating digital images.
 - [Krikzz](https://krikzz.com/our-products/cartridges/): Incredible hardware
   for retro game console hacking and development, including flash carts.
