#!/usr/bin/env python3

# Sega Slide Generator
#
# Copyright (c) 2024 Joey Parrish
#
# See MIT License in LICENSE.txt

"""
Create a Sega Genesis / Mega Drive ROM from a PDF of a slide show.

Export the slides as a PDF, then run this tool to generate a ROM.

Press left or right on the Sega to move through slides.

Burn the ROM to a flash cart, or run in an emulator.

Requires ImageMagick and pdftoppm to convert images, and Docker to compile the
ROM using SGDK.  On Ubuntu, install packages "python3", "imagemagick",
"poppler-utils", and "docker.io".
"""

import glob
import os
import shutil
import subprocess
import sys
import tempfile


# SGDK image to compile the ROM.
SGDK_DOCKER_IMAGE='ghcr.io/stephane-d/sgdk:latest'

# The double curly braces are escaped for Python string formatting.
SLIDES_H_TEMPLATE = '''
#ifndef _RES_SLIDES_H_
#define _RES_SLIDES_H_

#include "slide_data.h"

const Image* slides[] = {{
{image_pointers}
}};

const int num_slides = {num_slides};

#endif // _RES_SLIDES_H_
'''


def main(pdf_path, rom_path):
  with tempfile.TemporaryDirectory(prefix='sega-slides-') as tmp_dir:
    pages_dir = os.path.join(tmp_dir, 'pages')
    os.mkdir(pages_dir)

    app_dir = os.path.join(tmp_dir, 'app')
    os.mkdir(app_dir)
    os.mkdir(os.path.join(app_dir, 'src'))
    os.mkdir(os.path.join(app_dir, 'res'))

    print('Processing slides into Sega-compatible image resources...')
    process_slides(pdf_path, pages_dir, app_dir)
    print('Bootstrapping slide view source code...')
    copy_sources(app_dir)
    print('Compiling final ROM...')
    print('')
    compile_rom(app_dir, rom_path)
    print('')
    print('ROM compiled.')
    subprocess.run(args=['ls', '-sh', rom_path])


def process_slides(pdf_path, pages_dir, app_dir):
  # Split the PDF into one PNG image per page.
  subprocess.run(check=True, args=[
    'pdftoppm',
    # Write PNG format, not PPM.
    '-png',
    # Input file in PDF format.
    pdf_path,
    # Output prefix starting with the pages directory.  The tool will create a
    # series of files by appending a suffix like "-13.png", etc.
    os.path.join(pages_dir, 'page'),
  ])

  # Process those pages by downscaling and reducing colors.
  num_slides = 0
  resource_list = []
  image_pointers = []
  page_paths = sorted(glob.glob(os.path.join(pages_dir, 'page-*.png')))
  for page_path in page_paths:
    page_filename = os.path.basename(page_path)
    output_path = os.path.join(app_dir, 'res', page_filename)
    num_slides += 1

    subprocess.run(check=True, args=[
      'convert',
      # Input PNG.
      page_path,
      # Scale down to Sega resolution.  Will fit to the frame and will
      # respect aspect ratio by default.
      '-scale', '320x224',
      # Then pad it out to exactly 320x224.  If the output isn't a multiple of
      # 8 in each dimension, it won't work as an image resource.
      '-background', 'black',
      '-gravity', 'center',
      '-extent', '320x224',
      # Reduce to 15 colors (the max you can do in one palette on Sega)
      # without dithering.
      '+dither', '-colors', '15',
      # Output a PNG image with an 8-bit palette.
      'PNG8:{}'.format(output_path),
    ])

    resource_list.append(
        'IMAGE slide_{num_slides} {page_filename} BEST'.format(
            num_slides=num_slides, page_filename=page_filename))
    image_pointers.append(
        '  &slide_{num_slides},'.format(
            num_slides=num_slides))

    print('\rProcessed {} / {}... '.format(num_slides, len(page_paths)), end='')

  print('')

  with open(os.path.join(app_dir, 'src', 'slides.h'), 'w') as f:
    f.write(SLIDES_H_TEMPLATE.format(
        image_pointers='\n'.join(image_pointers), num_slides=num_slides))

  with open(os.path.join(app_dir, 'res', 'slide_data.res'), 'w') as f:
    f.write('\n'.join(resource_list) + '\n')


def copy_sources(app_dir):
  template_dir = os.path.join(os.path.dirname(__file__), 'template')
  shutil.copytree(template_dir, app_dir, dirs_exist_ok=True)


def compile_rom(app_dir, rom_path):
  subprocess.run(check=True, args=[
    # Pull the image if missing.
    'docker', 'pull', SGDK_DOCKER_IMAGE,
  ])

  subprocess.run(check=True, args=[
    # Run the image.
    'docker', 'run',
    # Remove the container when done.
    '--rm',
    # Mount the source directory into the container.
    '-v', '{}:/src'.format(app_dir),
    # Run as the current user.
    '-u', '{}:{}'.format(os.getuid(), os.getgid()),
    # Run the image we just pulled.
    SGDK_DOCKER_IMAGE,
  ], stdout=subprocess.DEVNULL)

  # Copy the output from the temporary folder to the final destination.
  shutil.copy(os.path.join(app_dir, 'out', 'rom.bin'), rom_path)

  # Make it not executable.  To SGDK, it is an "executable", but a ROM
  # shouldn't be executable to your host system.
  os.chmod(rom_path, 0o644)


if __name__ == '__main__':
  if len(sys.argv) != 3:
    print('Usage: {} <PDF> <ROM.BIN>'.format(sys.argv[0]))
    print(__doc__)
    sys.exit(1)

  main(sys.argv[1], sys.argv[2])
  sys.exit(0)
