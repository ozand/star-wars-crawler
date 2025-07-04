from moviepy.config import change_settings

# Update the ImageMagick binary path
change_settings({"IMAGEMAGICK_BINARY": r"C:\Program Files\ImageMagick\magick.exe"})

# Verify the change
from moviepy.config import get_setting

print(f"ImageMagick path set to: {get_setting('IMAGEMAGICK_BINARY')}")
