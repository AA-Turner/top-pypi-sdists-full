# No mocks. These tests exercise the real asset pipeline.
#
# There was previously an autouse fixture here that monkeypatched
# sprites._vertex_available / sprites._imagen_generate and
# meshes._find_blender / _blender_export / _blender_export_character so that
# asset generation wrote 4-to-8-byte stub files (a bare PNG header, the literal
# b"glTF") and reported success. That fabricated the artifacts the tests then
# asserted on, so the suite passed without ever generating an asset.
#
# It has been removed. Running these tests now requires the real toolchain:
#   - Vertex AI / Imagen credentials for sprite generation
#   - A real Blender installation on PATH for mesh export
#
# test_assets.py and test_3d_asset_pipeline.py were already exempt from the
# fixture and manage their own test doubles locally.
