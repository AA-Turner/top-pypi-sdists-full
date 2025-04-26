import os
import glob

current_dir = os.path.dirname(os.path.abspath(__file__))
jpg_files = glob.glob(os.path.join(current_dir, '*.jpg'))
__all__ = [os.path.basename(f)[:-4] for f in jpg_files]
for jpg_file in jpg_files:
    filename = os.path.basename(jpg_file)[:-4]
    globals()[filename] = jpg_file
