"""
Permanent patches for Python 3.13 compatibility with nes_py and gym_super_mario_bros.
Import this module before importing the game libraries to automatically apply fixes.
"""

import numpy as np

# Fix numpy compatibility issue
if not hasattr(np, 'bool8'):
    np.bool8 = np.bool_

def apply_overflow_patches():
    """Apply patches for Python 3.13 integer overflow issues."""
    import nes_py._rom
    import gym_super_mario_bros.smb_env

    # Store original methods
    original_prg_rom_stop = nes_py._rom.ROM.prg_rom_stop
    original_chr_rom_stop = nes_py._rom.ROM.chr_rom_stop
    original_x_position = gym_super_mario_bros.smb_env.SuperMarioBrosEnv._x_position

    def patched_prg_rom_stop(self):
        try:
            return original_prg_rom_stop.fget(self)
        except OverflowError:
            return int(self.prg_rom_start) + int(self.prg_rom_size) * 1024

    def patched_chr_rom_stop(self):
        try:
            return original_chr_rom_stop.fget(self)
        except OverflowError:
            return int(self.chr_rom_start) + int(self.chr_rom_size) * 1024

    def patched_x_position(self):
        try:
            return original_x_position.fget(self)
        except OverflowError:
            return int(self.ram[0x6d]) * 256 + int(self.ram[0x86])

    # Apply patches
    nes_py._rom.ROM.prg_rom_stop = property(patched_prg_rom_stop)
    nes_py._rom.ROM.chr_rom_stop = property(patched_chr_rom_stop)
    gym_super_mario_bros.smb_env.SuperMarioBrosEnv._x_position = property(patched_x_position)

def apply_api_compatibility():
    """Fix gym API compatibility for step function."""
    import gym_super_mario_bros.smb_env
    
    # Store original step method
    original_step = gym_super_mario_bros.smb_env.SuperMarioBrosEnv.step
    
    def patched_step(self, action):
        result = original_step(self, action)
        if len(result) == 4:
            obs, reward, done, info = result
            return obs, reward, done, False, info  # Add truncated=False
        return result
    
    # Apply API compatibility patch
    gym_super_mario_bros.smb_env.SuperMarioBrosEnv.step = patched_step

# Auto-apply all patches when this module is imported
apply_overflow_patches()
apply_api_compatibility()
