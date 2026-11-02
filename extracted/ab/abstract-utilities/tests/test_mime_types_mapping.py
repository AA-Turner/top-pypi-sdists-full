from abstract_utilities.type_utils import MIME_TYPES


def load_mapping():
    # Pulled from abstract_essentials' packaged mime_types.json.
    return MIME_TYPES


def test_comprehensive_mapping_shape_and_derived_sets():
    mime_types = load_mapping()
    assert list(mime_types) == [
        'image', 'video', 'audio', 'document', 'presentation', 'spreadsheet',
        'data_science', 'code', 'three_d', 'archive', 'font', 'executable',
        'geospatial', 'pandas_data', 'machine_learning', 'model_weights', 'tokenizer',
    ]
    assert all(extension.startswith('.') for mapping in mime_types.values() for extension in mapping)
    assert all(isinstance(m, str) and '/' in m for mapping in mime_types.values() for m in mapping.values())


def test_new_and_corrected_mime_entries_are_present():
    mime_types = load_mapping()
    expected = {
        ('image', '.avif'): 'image/avif', ('video', '.mp4v'): 'video/mp4',
        ('video', '.mpg'): 'video/mpeg', ('audio', '.ac3'): 'audio/ac3',
        ('document', '.rst'): 'text/x-rst',
        ('presentation', '.ppsx'): 'application/vnd.openxmlformats-officedocument.presentationml.slideshow',
        ('spreadsheet', '.xlsb'): 'application/vnd.ms-excel.sheet.binary.macroEnabled.12',
        ('data_science', '.zarr'): 'application/vnd.zarr',
        ('code', '.scala'): 'text/x-scala', ('three_d', '.step'): 'model/step',
        ('archive', '.tbz2'): 'application/x-bzip2',
        ('font', '.pfm'): 'application/x-font-type1',
        ('executable', '.msi'): 'application/x-msi',
        ('geospatial', '.gpkg'): 'application/geopackage+sqlite3',
        ('pandas_data', '.stata'): 'application/x-stata',
        ('machine_learning', '.gguf'): 'application/x-gguf',
        ('model_weights', '.safetensors'): 'application/x-safetensors',
        ('tokenizer', '.spm'): 'application/x-sentencepiece',
    }
    assert {key: mime_types[key[0]][key[1]] for key in expected} == expected


def test_overlapping_extensions_keep_category_specific_values():
    mime_types = load_mapping()
    assert mime_types['video']['.ogg'] == 'video/ogg'
    assert mime_types['audio']['.ogg'] == 'audio/ogg'
    assert '.tsv' not in mime_types['video']
    assert mime_types['document']['.tsv'] == 'text/tab-separated-values'
    assert mime_types['spreadsheet']['.tsv'] == 'text/tab-separated-values'


def test_shared_extensions_are_listed_in_every_category():
    mime_types = load_mapping()
    assert '.bin' in mime_types['executable'] and '.bin' in mime_types['machine_learning']
    assert '.json' in mime_types['document'] and '.json' in mime_types['code'] and '.json' in mime_types['machine_learning']
    assert set(mime_types['model_weights']) <= set(mime_types['machine_learning'])
