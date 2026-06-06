from tdda.serial import (
    load_metadata,
    SerialMetadata,
    serial_to_pandas_read_csv_args,
    csv_to_pandas,
)


def convert(in_path, out_path, backend=None):
    md = load_metadata(in_path)
    md_out = SerialMetadata()
    kw = serial_to_pandas_read_csv_args(md, backend=backend)
    md_out.libs = {'pandas.read_csv': kw}
    with open(out_path, 'w') as f:
        f.write(md_out.to_json())
    print(f'Written {out_path}.')
    df = csv_to_pandas(f'elements3-old.csv:{out_path}')
    print(df.info())
    print()




convert('elements3-old.serial', 'elements3-old-pandas-none.serial')
convert('elements3-old.serial', 'elements3-old-pandas-pandas.serial',
        backend='o')
convert('elements3-old.serial', 'elements3-old-pandas-nullablep3.serial',
        backend='n')
convert('elements3-old.serial', 'elements3-old-pandas-pyarrow.serial',
         backend='a')


