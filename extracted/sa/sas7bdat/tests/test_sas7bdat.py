# !/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from sas7bdat import SAS7BDAT, ParseError, RLEDecompressor
import tempfile
import io
import logging
import os
import datetime


class _DecompressorStub(object):
    logger = logging.getLogger('test')
    logger.setLevel(logging.CRITICAL)


class TestSAS7BDAT(unittest.TestCase):
    def test_read_numbers(self):
        s = SAS7BDAT('tests/data/intvalues.sas7bdat')
        for i, line in enumerate(s):
            if i == 0:
                self.assertEqual(line, ['intvalue'])
            else:
                self.assertEqual(len(line), 1)
                self.assertEqual(line[0], i)
                self.assertEqual(type(line[0]), float)
        self.assertEqual(i, 5)

    def test_read_numbers_skip_header(self):
        s = SAS7BDAT('tests/data/intvalues.sas7bdat', skip_header=True)
        for i, line in enumerate(s):
            self.assertEqual(len(line), 1)
            self.assertEqual(line[0], i + 1)
            self.assertEqual(type(line[0]), float)
        self.assertEqual(i, 4)

    def test_read_floats(self):
        s = SAS7BDAT('tests/data/floatvalues.sas7bdat', skip_header=True)
        for i, line in enumerate(s):
            self.assertEqual(len(line), 1)
            self.assertEqual(line[0], float(i) + 1.0 + float(i) * 0.1)
            self.assertEqual(type(line[0]), float)
        self.assertEqual(i, 4)

    def test_read_characters(self):
        s = SAS7BDAT('tests/data/charactervalues.sas7bdat', skip_header=True)
        characters = 'ABcdE'
        for i, line in enumerate(s):
            self.assertEqual(len(line), 1)
            self.assertEqual(line[0], characters[i])
        self.assertEqual(i, len(characters) - 1)

    def test_read_specialcharacters(self):
        s = SAS7BDAT('tests/data/specialcharactervalues.sas7bdat', skip_header=True)
        characters = u'Äéǿαאا'

        for i, line in enumerate(s):
            self.assertEqual(len(line), 1)
            self.assertEqual(line[0], characters[i])
        self.assertEqual(i, len(characters) - 1)

    def test_read_dates(self):
        s = SAS7BDAT('tests/data/datevalues.sas7bdat', skip_header=True)
        dates = ['1900-01-01', '1950-01-01', '1960-01-01', '1970-01-01', '1980-01-01', '1990-01-01',
                 '2000-01-01', '2010-01-01', '2020-01-01', '2004-02-29', '1999-12-31']

        for i, line in enumerate(s):
            self.assertEqual(len(line), 1)
            self.assertEqual(line[0], datetime.datetime.strptime(dates[i], '%Y-%m-%d').date())
        self.assertEqual(i, len(dates) - 1)

    def test_read_datetimes(self):
        s = SAS7BDAT('tests/data/datetimevalues.sas7bdat', skip_header=True)
        datetimes = ['2000-12-31T00:00:00', '2010-01-01T23:59:22', '2020-02-29T08:12:59']

        for i, line in enumerate(s):
            self.assertEqual(len(line), 1)
            self.assertEqual(line[0], datetime.datetime.strptime(datetimes[i], '%Y-%m-%dT%H:%M:%S'))
        self.assertEqual(i, len(datetimes) - 1)

    def test_read_times(self):
        s = SAS7BDAT('tests/data/timevalues.sas7bdat', skip_header=True)
        datetimes = ['00:00:00', '11:59:01', '12:00:02', '22:05:03', '23:59:04']

        for i, line in enumerate(s):
            self.assertEqual(len(line), 1)
            self.assertEqual(line[0], datetime.datetime.strptime(datetimes[i], '%H:%M:%S').time())
        self.assertEqual(i, len(datetimes) - 1)

    def test_read_mixed_data(self):
        s = SAS7BDAT('tests/data/mixedvalues.sas7bdat', skip_header=True)
        mixed = [
            [1, 0.1, 'abc', datetime.time(hour=0, minute=0), datetime.date(year=1980, month=1, day=1)],
            [2, 0.2, 'def', datetime.time(hour=2, minute=22), datetime.date(year=1990, month=12, day=31)],
            [3, 0.3, 'GHI', datetime.time(hour=23, minute=59), datetime.date(year=2004, month=2, day=29)]
        ]

        for i, line in enumerate(s):
            self.assertEqual(len(line), len(mixed[i]))
            for c, col in enumerate(mixed[i]):
                self.assertEqual(line[c], col)
        self.assertEqual(i, len(mixed) - 1)

    def test_read_mixed_data_compressed_binary(self):
        s = SAS7BDAT('tests/data/mixedvalues_compressed_binary.sas7bdat', skip_header=True)
        mixed = [
            [1, 0.1, 'abc', datetime.time(hour=0, minute=0), datetime.date(year=1980, month=1, day=1)],
            [2, 0.2, 'def', datetime.time(hour=2, minute=22), datetime.date(year=1990, month=12, day=31)],
            [3, 0.3, 'GHI', datetime.time(hour=23, minute=59), datetime.date(year=2004, month=2, day=29)]
        ]

        for i, line in enumerate(s):
            self.assertEqual(len(line), len(mixed[i]))
            for c, col in enumerate(mixed[i]):
                self.assertEqual(line[c], col)
        self.assertEqual(i, len(mixed) - 1)

    def test_read_mixed_data_compressed_yes(self):
        s = SAS7BDAT('tests/data/mixedvalues_compressed_yes.sas7bdat', skip_header=True)
        mixed = [
            [1, 0.1, 'abc', datetime.time(hour=0, minute=0), datetime.date(year=1980, month=1, day=1)],
            [2, 0.2, 'def', datetime.time(hour=2, minute=22), datetime.date(year=1990, month=12, day=31)],
            [3, 0.3, 'GHI', datetime.time(hour=23, minute=59), datetime.date(year=2004, month=2, day=29)]
        ]

        for i, line in enumerate(s):
            self.assertEqual(len(line), len(mixed[i]))
            for c, col in enumerate(mixed[i]):
                self.assertEqual(line[c], col)
        self.assertEqual(i, len(mixed) - 1)

    def test_read_mixed_data_compressed_char(self):
        s = SAS7BDAT('tests/data/mixedvalues_compressed_char.sas7bdat', skip_header=True)
        mixed = [
            [1, 0.1, 'abc', datetime.time(hour=0, minute=0), datetime.date(year=1980, month=1, day=1)],
            [2, 0.2, 'def', datetime.time(hour=2, minute=22), datetime.date(year=1990, month=12, day=31)],
            [3, 0.3, 'GHI', datetime.time(hour=23, minute=59), datetime.date(year=2004, month=2, day=29)]
        ]

        for i, line in enumerate(s):
            self.assertEqual(len(line), len(mixed[i]))
            for c, col in enumerate(mixed[i]):
                self.assertEqual(line[c], col)
        self.assertEqual(i, len(mixed) - 1)

    def test_read_mixed_data_with_empty_cell(self):
        s = SAS7BDAT('tests/data/mixedvalues_empty.sas7bdat', skip_header=True)
        mixed = [
            [1, 0.1, 'abc', datetime.time(hour=0, minute=0), datetime.date(year=1980, month=1, day=1)],
            [2, 0.2, 'def', datetime.time(hour=2, minute=22), datetime.date(year=1990, month=12, day=31)],
            [3, 0.3, 'GHI', datetime.time(hour=23, minute=59), datetime.date(year=2004, month=2, day=29)],
            [4, 0.4, '', datetime.time(hour=00, minute=00), datetime.date(year=2000, month=1, day=1)],
            [5, 0.5, 'MNO', datetime.time(hour=5, minute=55), datetime.date(year=2111, month=11, day=11)],
            [6, None, 'PQR', datetime.time(hour=5, minute=55), datetime.date(year=2111, month=11, day=11)]
        ]

        for i, line in enumerate(s):
            self.assertEqual(len(line), len(mixed[i]))
            for c, col in enumerate(mixed[i]):
                self.assertEqual(line[c], col)
        self.assertEqual(i, len(mixed) - 1)

    def test_oversized_row_length_rejected(self):
        # A malicious file can declare a huge row_length in its row-size
        # subheader; the RDC decompressor would allocate on that value and
        # exhaust memory. The field is a signed 4-byte int at this offset in
        # the RDC-compressed fixture (header page + meta page offset 65076).
        filename = 'tests/data/mixedvalues_compressed_binary.sas7bdat'
        src = open(filename, 'rb').read()
        off = 65536 + 65076
        self.assertEqual(
            int.from_bytes(src[off:off + 4], 'little'), 40,
            'fixture layout changed; update the row_length offset'
        )
        for value in (2147483647, 12000000):
            mutated = src[:off] + value.to_bytes(4, 'little') + src[off + 4:]
            with self.assertRaises(ParseError):
                SAS7BDAT(filename, log_level=50, fh=io.BytesIO(mutated))

    def test_oversized_row_count_stops_at_eof(self):
        # A malicious file can declare a huge row_count; the reader must stop
        # once the file's pages are exhausted rather than yielding that many
        # rows of garbage. row_count is the signed 4-byte int following
        # row_length in the row-size subheader.
        filename = 'tests/data/mixedvalues_compressed_binary.sas7bdat'
        src = open(filename, 'rb').read()
        off = 65536 + 65080
        self.assertEqual(
            int.from_bytes(src[off:off + 4], 'little'), 3,
            'fixture layout changed; update the row_count offset'
        )
        mutated = src[:off] + (5000000).to_bytes(4, 'little') + src[off + 4:]
        s = SAS7BDAT(filename, log_level=50, fh=io.BytesIO(mutated))
        rows = list(s.readlines())
        self.assertEqual(len(rows), 4)  # header + 3 real rows

    def test_rle_0x40_run_length(self):
        # The 0x40 RLE command repeats a byte (nibble * 256 + next + 18)
        # times. A nonzero nibble is exercised only by runs >= 274 bytes,
        # which the sample files never hit; verify the multiplier directly.
        d = RLEDecompressor(_DecompressorStub())
        page = bytes(bytearray([0x41, 0x00, 0x41]))  # nibble=1, count=0, 'A'
        out = d.decompress_row(0, len(page), 274, page)
        self.assertEqual(out, bytes(bytearray([0x41])) * 274)

    def test_rle_extra_commands(self):
        # 0x10 (copy next+64+nibble*256+4096), 0x20 (copy nibble+96),
        # 0x50 (insert nibble*256+next+17 copies of '@') were previously
        # unhandled and silently corrupted the rest of the row.
        d = RLEDecompressor(_DecompressorStub())

        payload = bytes(bytearray(range(97)))  # 0x20, nibble=1 -> copy 97
        page = bytes(bytearray([0x21])) + payload
        self.assertEqual(d.decompress_row(0, len(page), 97, page), payload)

        payload = bytes(bytearray([7])) * 4160  # 0x10, nibble=0, next=0
        page = bytes(bytearray([0x10, 0x00])) + payload
        self.assertEqual(d.decompress_row(0, len(page), 4160, page), payload)

        page = bytes(bytearray([0x50, 0x00]))  # 0x50, nibble=0, next=0 -> 17
        self.assertEqual(d.decompress_row(0, len(page), 17, page), b'@' * 17)

    def test_encoding_inferred_from_header(self):
        # The encoding is a code at header byte 70; the reader should map it
        # rather than assume UTF-8. The special-characters fixture declares
        # UTF-8 (code 20); the others declare wlatin1/cp1252 (code 62).
        s = SAS7BDAT('tests/data/specialcharactervalues.sas7bdat',
                     log_level=50)
        self.assertEqual(s.encoding, 'utf-8')
        s = SAS7BDAT('tests/data/mixedvalues.sas7bdat', log_level=50)
        self.assertEqual(s.encoding, 'cp1252')

    def test_explicit_encoding_overrides_inference(self):
        s = SAS7BDAT('tests/data/mixedvalues.sas7bdat', log_level=50,
                     encoding='latin1')
        self.assertEqual(s.encoding, 'latin1')

    def test_format_u64_big_endian(self):
        # 64-bit, big-endian file whose row/column-size subheaders store the
        # signature in the low four bytes (previously unmatched -> crash).
        s = SAS7BDAT('tests/data/format_u64_be.sas7bdat', log_level=50)
        self.assertTrue(s.properties.u64)
        self.assertEqual(s.properties.endianess, 'big')
        rows = list(s.readlines())
        self.assertEqual(len(rows), 11)  # header + 10 data rows
        self.assertEqual(rows[1][:4],
                         [0.636, 'pear', 84.0, datetime.date(1965, 12, 10)])
        self.assertEqual(rows[-1][-3:], ['crocodile', 89.0, None])

    def test_format_big_endian_rdc(self):
        # Big-endian, RDC-compressed. Exercises the RDC trailing-byte fix:
        # the physically-last column must not come back empty.
        s = SAS7BDAT('tests/data/format_be_rdc.sas7bdat', log_level=50)
        self.assertEqual(s.properties.endianess, 'big')
        self.assertEqual(s.properties.compression, SAS7BDAT.RDC_COMPRESSION)
        rows = list(s.readlines())
        self.assertEqual(len(rows), 11)
        self.assertEqual(rows[1][1], 'pear')
        self.assertEqual(rows[-1][-3], 'crocodile')  # last string column

    def test_format_meta2_page_rdc(self):
        # META2 (0x4000) pages carrying RDC-compressed rows; previously the
        # page type was skipped and the rows lost.
        s = SAS7BDAT('tests/data/format_meta2_rdc.sas7bdat', log_level=50)
        rows = list(s.readlines())
        self.assertEqual(len(rows), 1001)  # header + 1000 rows
        self.assertEqual(rows[0][0], 'date')
        self.assertEqual(rows[1][0], datetime.date(1997, 1, 1))

    def test_corrupt_file_raises_cleanly(self):
        # A file whose row-size subheader is missing/corrupt must raise
        # ParseError, not crash with a TypeError deep in the row loop.
        s = SAS7BDAT('tests/data/corrupt.sas7bdat', log_level=60)
        with self.assertRaises(ParseError):
            list(s.readlines())

    def test_context(self):
        with SAS7BDAT('tests/data/mixedvalues_empty.sas7bdat') as s:
            lines1 = [line for line in s.readlines()]
        s = SAS7BDAT('tests/data/mixedvalues_empty.sas7bdat')
        lines2 = [line for line in s.readlines()]
        self.assertEqual(lines1, lines2)

    def test_filehandler(self):
        filename = 'tests/data/mixedvalues_empty.sas7bdat'
        temp = tempfile.NamedTemporaryFile()
        f = open(filename, 'rb')
        s = SAS7BDAT(temp.name, fh=f)
        lines1 = [line for line in s.readlines()]
        f.close()

        s = SAS7BDAT(filename)
        lines2 = [line for line in s.readlines()]
        self.assertEqual(lines1, lines2)
        temp.close()

    def test_filehandler_context(self):
        filename = 'tests/data/mixedvalues_empty.sas7bdat'
        f = open(filename, 'rb')
        self.assertFalse(f.closed)
        temp = tempfile.NamedTemporaryFile()
        with SAS7BDAT(temp.name, fh=f) as s:
            _ = [line for line in s.readlines()]
            self.assertFalse(f.closed)
        self.assertTrue(f.closed)
        temp.close()

    def test_convert_file(self):
        filename = 'tests/data/mixedvalues_empty.sas7bdat'
        s = SAS7BDAT(filename)
        temp = tempfile.NamedTemporaryFile(delete=False)
        temp.close()
        success = s.convert_file(temp.name)
        self.assertTrue(success)
        os.unlink(temp.name)

    def test_convert_file_fail(self):
        filename = 'tests/data/mixedvalues_empty.sas7bdat'
        s = SAS7BDAT(filename)
        success = s.convert_file(None)
        self.assertFalse(success)


if __name__ == '__main__':
    unittest.main()
