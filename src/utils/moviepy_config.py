"""MoviePy configuration module for ImageMagick integration."""
import os

from moviepy.config import change_settings, get_setting

# Add ImageMagick to PATH temporarily
os.environ["PATH"] = r"C:\Program Files\ImageMagick;" + os.environ["PATH"]

# Set ImageMagick binary path
magick_path = r"C:\Program Files\ImageMagick\magick.exe"
# Force MoviePy to use magick.exe instead of looking for convert.exe
os.environ["IMAGEMAGICK_BINARY"] = magick_path
change_settings({"IMAGEMAGICK_BINARY": magick_path})

# Verify the setting
print(f"ImageMagick binary set to: {get_setting('IMAGEMAGICK_BINARY')}")
