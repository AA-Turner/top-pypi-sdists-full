from napari_resources.generate_logos import generate_logos


def test_gen_logos(tmp_path):
    generate_logos(tmp_path)

    # every variant/template/mode combination should have produced an svg
    assert list(tmp_path.glob("*.svg"))
