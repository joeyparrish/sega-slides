/**
 * Sega Slide Generator
 *
 * Copyright (c) 2024 Joey Parrish
 *
 * See MIT License in LICENSE.txt
 */

#include <genesis.h>

__attribute__((externally_visible))
const ROMHeader rom_header = {
  // Standard header, which emulators will use to emulate a standard Sega with
  // a plain ROM chip plugged in.
  "SEGA MEGA DRIVE ",
  // Copyright line.
  "(C) Joey Parrish",
  // Game title.
  "SLIDE SHOW                                      ",
  // Localized game title.
  "SLIDE SHOW                                      ",
  // Serial number. GM prefix means "game". The rest is meaningless.
  "GM 08765309-01",
  // ROM checksum.
  0x0000,
  // Device support.  "J" means 3-button controller.
  "J               ",
  // Cartridge ROM/RAM address range.
  0x00000000,
  0x003FFFFF,
  // RAM address range.
  0x00FF0000,
  0x00FFFFFF,
  // No SRAM.
  "  ",
  // A0 = 16-bit SRAM, 20 = reserved.
  0xA020,
  // SRAM address range.
  0x00000000,
  0x00000000,
  // No modem support.
  "            ",
  // Reserved, just spaces.
  "                                        ",
  // Region support: Japan, US, Europe.
  "JUE             "
};
