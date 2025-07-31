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

# With dithering, defaults to FloydSteinberg method
./generate.py slides.pdf slides.rom --dithering

# With an explicit dithering method
./generate.py slides.pdf slides.rom --dithering o8x8
./generate.py slides.pdf slides.rom --dithering checks
```


## Windows

To use this from Windows, you can install dependencies via Chocolatey:

```ps1
choco install -y imagemagick docker docker-desktop

# Possibly needed to update Windows Subsystem for Linux to support Docker:
wsl --update

# The latest Poppler package on Chocolatey (25.7.0) is broken, and only
# contains sources, not executables.  Pin to an older version.
choco install -y poppler --version 0.89.0
```

Finally, you will have to run Docker Desktop once to configure it and start the
service.  Docker Desktop may or may not require you to reboot if it is newly
installed.  After that, you should be able to run this tool on Windows.


## macOS

To use this from macOS, you can install dependencies via Homebrew:

```sh
brew install imagemagick poppler docker
```

Additional Docker setup may be required if you have not used Docker on you Mac
before.


## Links

 - [SGDK](https://github.com/Stephane-D/SGDK): A free and open development kit
   for Sega Mega Drive.
 - [Poppler](https://poppler.freedesktop.org/): A PDF rendering library based
   on the xpdf-3.0 code base.
 - [ImageMagick](https://imagemagick.org/): A free, open-source software suite
   used for editing and manipulating digital images.
 - [Krikzz](https://krikzz.com/our-products/cartridges/): Incredible hardware
   for retro game console hacking and development, including flash carts.
