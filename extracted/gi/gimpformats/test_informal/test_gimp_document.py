from __future__ import annotations

import os
import sys
from pathlib import Path

THISDIR = Path(__file__).resolve().parent
sys.path.insert(0, os.path.dirname(THISDIR))

from gimpformats.gimpXcfDocument import GimpDocument

FILES = THISDIR.parent / "test_files"


def p_section(text: str):
	print()
	print("=" * 60)
	print("=", text)
	print("=" * 60)


def p_header(text: str):
	print()
	print(text)
	print("-" * 40)


# ruff:noqa:ERA001

p_section("Open 'base24.xcf'")
gimp_img = GimpDocument((FILES / "base24.xcf").as_posix())

# 2. Test the basic methods
p_header("Image Info")

# Test image's fileName and full_repr
print(f"File Name: {gimp_img.fileName}")
# print(f"Full Representation: {gimp_img.full_repr()}")

# Test basic properties
print(f"Width: {gimp_img.width}")
print(f"Height: {gimp_img.height}")
print(f"Horizontal Resolution: {gimp_img.horizontalResolution}")
print(f"Vertical Resolution: {gimp_img.verticalResolution}")

# Test color settings
print(f"Base Color Mode: {gimp_img.baseColorMode}")
print(f"Blend Mode: {gimp_img.blendMode}")
print(f"Blend Space: {gimp_img.blendSpace}")
print(f"Color: {gimp_img.color}")

# Test methods related to selection
print(f"Is Selection Active: {gimp_img.isSelection}")
print(f"Selection Attached To: {gimp_img.selectionAttachedTo}")

print(f"Alpha Locked: {gimp_img.locked}")
print(f"Mask Applied: {gimp_img.showMask}")


root_group = gimp_img.walkTree()
p_header(f"Walking through tree structure: `{root_group.name}`")

for idx, children in enumerate(root_group.children):
	print(idx, children)

print("Generating image, should take a couple seconds...")
gimp_img.image


# # Test deleting raw layer
# gimp_img.deleteRawLayer(0)
# print(f"Layer Deleted. Remaining layers: {len(gimp_img.raw_layers)}")

# 4. Test save/load functionality
p_section("Open '64x64.xcf'")
gimp_img.load((FILES / "64x64.xcf").as_posix())  # Provide an actual path to test loading
print(f"Image Loaded: {gimp_img.fileName}")


# Test encoding and decoding
encoded = gimp_img.encode
print(f"Image Encoded: {encoded}")

# This doesn't work at all :(
# decoded = gimp_img.decode(encoded)
# print(f"Image Decoded: {decoded}")

# 5. Test grouping and linking (for group layers)
p_header("Testing group and link methods")


# Test if it's linked
print(f"Is Linked: {gimp_img.isLinked}")

# Test the version and vectors (could be used to check GIMP version compatibility)
print(f"GIMP Image Version: {gimp_img.version}")
print(f"Vectors Version: {gimp_img.vectorsVersion}")

# 6. Test for active vector (if vector tools are available)
# p_header("Testing vector tools")

# if gimp_img.activeVector:
# 	print(f"Active Vector: {gimp_img.activeVector}")
# else:
# 	print("No active vector found.")

# 7. Test composite and color map (advanced image manipulation)
p_header("Testing composite methods")

print(f"Composite Mode: {gimp_img.compositeMode}")
print(f"Composite Space: {gimp_img.compositeSpace}")

print(f"Color Map: {gimp_img.colorMap}")

# 8. Test image properties for performance (expanded, pointers, precision, etc.)
p_header("Testing performance and other image properties")

print(f"Expanded: {gimp_img.expanded}")
print(f"Pointer Size: {gimp_img.pointerSize}")
print(f"Precision: {gimp_img.precision}")

# Test sample points, guidelines, and paths (advanced visualization or tracing)
print(f"Sample Points: {gimp_img.samplePoints}")
print(f"Guidelines: {gimp_img.guidelines}")
print(f"Paths: {gimp_img.paths}")

# Test walking through tree structure
root_group = gimp_img.walkTree()
p_header(f"Walking through tree structure: `{root_group.name}`")

for idx, children in enumerate(root_group.children):
	print(idx, children)

print("Attempt to access out of bounds layer:")
try:
	print(gimp_img.getLayer(500))
except RuntimeError:
	print("Raised RuntimeError as expected")
