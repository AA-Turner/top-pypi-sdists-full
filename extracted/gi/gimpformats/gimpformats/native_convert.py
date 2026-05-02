"""Drive gimp directly if it exists to do a conversion. Note this is highly
experimental at present, though will likely export more accurately than gimpformats will."""

from __future__ import annotations

import os
import subprocess
import sys

from loguru import logger

logger.remove()
logger.add(sys.stdout, format="<level>{level: <8}</level> | {message}", level="INFO")


def _convert_xcf_to_flat_image_windows(xcf_path: str, output_path: str) -> list[str] | None:
	common_gimp_paths = [
		r"C:\Program Files\GIMP 2\bin\gimp-console-2.10.exe",
		r"C:\Program Files (x86)\GIMP 2\bin\gimp-console-2.10.exe",
	]

	gimp_path = None
	for path in common_gimp_paths:
		if os.path.exists(path):
			gimp_path = path

	if gimp_path is None:
		logger.error(f"GIMP is not installed or not found at common locations. {common_gimp_paths}")
		return None

	# Prepare the command to run GIMP in batch mode
	return [
		gimp_path,
		"-n",
		"-i",
		"-b",
		f'(begin (define xcf-path "{xcf_path}") '
		f"(define image (car (gimp-file-load RUN-NONINTERACTIVE xcf-path xcf-path))) "
		f"(define layer (car (gimp-image-merge-visible-layers image CLIP-TO-IMAGE))) "
		f'(gimp-file-save RUN-NONINTERACTIVE image layer "{output_path}" "{output_path}") '
		f"(gimp-image-delete image) (gimp-quit 0))",
	]


def convert_xcf_to_flat_image(xcf_path: str, output_path: str) -> None:
	# Ensure the input .xcf path exists
	if not os.path.exists(xcf_path):
		logger.error(f"Input file does not exist: {xcf_path}")
		return

	# Check if the OS is Windows
	if sys.platform == "win32":
		command = _convert_xcf_to_flat_image_windows(xcf_path, output_path)

	if command is None:
		logger.error(f"Sorry, this script is not supported on {sys.platform}")
		return

	try:
		# Run the command and convert the file
		subprocess.run(command, check=True)
		logger.info(f"Conversion successful: {output_path}")
	except subprocess.CalledProcessError as e:
		logger.error(f"Error running GIMP: {e}")
	except Exception as e:  # noqa: BLE001
		logger.error(f"Unexpected error: {e}")
