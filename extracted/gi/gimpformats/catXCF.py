"""https://github.com/FHPythonUtils/GimpFormats/issues/4."""

from __future__ import annotations

from gimpformats.gimpXcfDocument import GimpDocument


#### XCF ####
def catXCF(file: str) -> None:
	"""Open an .xcf file into a layered image."""
	project = GimpDocument(file)
	# Iterate the layers and create a list of layers for each group, then remove
	# these from the project layers
	layers = project.raw_layers[::-1]
	index = 0
	groupIndex = 0
	groupLayers = [[]]
	while index < len(layers):
		layerOrGroup = layers[index]
		if layerOrGroup.isGroup:
			index -= 1
			while layers[index].itemPath is not None:
				layer = layers[index]
				groupLayers[groupIndex].append(
					(
						"LAYER:" + layer.name,
						layer.image,
						(layer.width, layer.height),
						(
							layer.xOffset - layerOrGroup.xOffset,
							layer.yOffset - layerOrGroup.yOffset,
						),
						layer.opacity,
						layer.visible,
						layer.blendMode,
					)
				)
				layers.pop(index)
				index -= 1
			index += 2
			groupIndex += 1
			groupLayers.append([])
		else:
			index += 1
	# Iterate the clean project layers and add the group layers in
	groupIndex = 0
	layersAndGroups = []
	for layerOrGroup in layers:
		if layerOrGroup.isGroup:
			layersAndGroups.append(
				(
					"GROUP:" + layerOrGroup.name,
					groupLayers[groupIndex][::-1],
					(layerOrGroup.width, layerOrGroup.height),
					(layerOrGroup.xOffset, layerOrGroup.yOffset),
					layerOrGroup.opacity,
					layerOrGroup.visible,
					layerOrGroup.blendMode,
				)
			)
			groupIndex += 1
		else:
			layersAndGroups.append(
				(
					"LAYER:" + layerOrGroup.name,
					layerOrGroup.image,
					(layerOrGroup.width, layerOrGroup.height),
					(layerOrGroup.xOffset, layerOrGroup.yOffset),
					layerOrGroup.opacity,
					layerOrGroup.visible,
					layerOrGroup.blendMode,
				)
			)


catXCF("test_files/test.xcf")
catXCF("test_files/base24.xcf")
