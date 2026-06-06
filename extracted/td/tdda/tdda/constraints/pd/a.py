@tag
class TestPandasDataFrameConstraints(ReferenceTestCase):

    def testDDD_df1(self):
        csv_path = os.path.join(TESTDATADIR, 'ddd.csv')
        df = pd.read_csv(csv_path)
        constraints_path = os.path.join(TESTDATADIR, 'ddd.tdda')
        v = verify(df, constraints_path)
        # expect 3 failures:
        #   - the pandas CSV reader will have read 'elevens' as an int
        #   - the pandas CSV reader will have read the date columns as strings
        self.assertEqual(v.passes, 58)
        self.assertEqual(v.failures, 3)

    def testDDD_df2(self):
        csv_path = os.path.join(TESTDATADIR, 'ddd.csv')
        df = pd.read_csv(csv_path)
        constraints_path = os.path.join(TESTDATADIR, 'ddd.tdda')
        v = verify(df, constraints_path)
        # expect 3 failures:
        #   - the pandas CSV reader will have read 'elevens' as an int
        #   - the pandas CSV reader will have read the date columns as strings
        self.assertEqual(v.passes, 58)
        self.assertEqual(v.failures, 3)



    def testDDD_csv1(self):
        csv_path = os.path.join(TESTDATADIR, 'ddd.csv')
        constraints_path = os.path.join(TESTDATADIR, 'ddd.tdda')
        v = verify(csv_path, constraints_path, verbose=False)
        # expect 1 failure:
        #   - the enhanced CSV reader will have initially read 'elevens' as
        #     an int field and then (correctly) converted it to string, but
        #     it doesn't know that it would need to pad with initial zeros,
        #     so that means it will have computed its minimum as being '0'
        #     not '00', so the minimum string length won't be the same as
        #     Miro would compute (since Miro has the advantage of having
        #     additional metadata available when it read the CSV file, to
        #     tell it that 'elevens' is a string field.
        self.assertEqual(v.passes, 60)
        self.assertEqual(v.failures, 1)
        print('TTT')

    def testDDD_discover_and_verify1(self):
        print('LLL')
        # both discovery and verification done using Pandas
        tmpdir = tempfile.gettempdir()
        actual_constraints = os.path.join(tmpdir, 'dddtestconstraints.tdda')
        actual_constraints2 = os.path.join(tmpdir, 'dddtestconstraints2.tdda')
        report_formats = ['html', 'txt', 'md', 'json', 'yaml', 'toml']
        csv_path = os.path.join(TESTDATADIR, 'ddd.csv')

        c = discover(csv_path, constraints_path=actual_constraints,
                     report_formats=report_formats, verbose=False)
        with open(actual_constraints2, 'w') as f:
            f.write(c)
        v = verify(csv_path, actual_constraints2,
                   report='fields', verbose=False)
        self.assertFileCorrect(actual_constraints, actual_constraints2)
        self.assertEqual(v.passes, 61)
        self.assertEqual(v.failures, 0)
        print('kkk')
        for fmt in report_formats:
            pass
            # self.assertFileCorrect(actual_constriants, actual_constriants2)

    def testDDD_discover_and_verify2(self):
        # both discovery and verification done using Pandas
        csv_path = os.path.join(TESTDATADIR, 'ddd.csv')
        c = discover(csv_path, constraints_path=None, verbose=False)
        tmpdir = tempfile.gettempdir()
        tmpfile = os.path.join(tmpdir, 'dddtestconstraints.tdda')
        with open(tmpfile, 'w') as f:
            f.write(c)
        v = verify(csv_path, tmpfile, report='fields', verbose=False)
        self.assertEqual(v.passes, 61)
        self.assertEqual(v.failures, 0)

    def testDDD_csv3(self):
        csv_path = os.path.join(TESTDATADIR, 'ddd.csv')
        constraints_path = os.path.join(TESTDATADIR, 'ddd.tdda')
        v = verify(csv_path, constraints_path, verbose=False)
        # expect 1 failure:
        #   - the enhanced CSV reader will have initially read 'elevens' as
        #     an int field and then (correctly) converted it to string, but
        #     it doesn't know that it would need to pad with initial zeros,
        #     so that means it will have computed its minimum as being '0'
        #     not '00', so the minimum string length won't be the same as
        #     Miro would compute (since Miro has the advantage of having
        #     additional metadata available when it read the CSV file, to
        #     tell it that 'elevens' is a string field.
        self.assertEqual(v.passes, 60)
        self.assertEqual(v.failures, 1)

    def testDDD_discover_and_verify3(self):
        # both discovery and verification done using Pandas
        csv_path = os.path.join(TESTDATADIR, 'ddd.csv')
        c = discover(csv_path, constraints_path=None, verbose=False)
        tmpdir = tempfile.gettempdir()
        tmpfile = os.path.join(tmpdir, 'dddtestconstraints.tdda')
        with open(tmpfile, 'w') as f:
            f.write(c.to_json())
        v = verify(csv_path, tmpfile, report='fields', verbose=False)
        self.assertEqual(v.passes, 61)
        self.assertEqual(v.failures, 0)

    def testDiscoverDataframeDates(self):
        df = pd.DataFrame({'a': [datetime.date(1987, 1, 1),
                                 datetime.date(2019, 1, 2)]})
        c = discover(df, verbose=False)
        ac = c.fields['a'].constraints
        self.assertEqual(ac['type'].value, 'date')
        self.assertEqual(ac['min'].value, datetime.date(1987, 1, 1))
        self.assertEqual(ac['max'].value, datetime.date(2019, 1, 2))
        self.assertEqual(ac['max_nulls'].value, 0)

    def testDiscoverDataframeDateTimes(self):
        df = pd.DataFrame({'a': [datetime.datetime(1987, 1, 1),
                                 datetime.datetime(2019, 1, 2)]})
        c = discover(df, verbose=False)
        ac = c.fields['a'].constraints
        self.assertEqual(ac['type'].value, 'date')
        self.assertEqual(ac['min'].value, datetime.datetime(1987, 1, 1))
        self.assertEqual(ac['max'].value, datetime.datetime(2019, 1, 2))
        self.assertEqual(ac['max_nulls'].value, 0)

    def testVerifySignWithWrongType(self):
        df = pd.DataFrame({'a': ['one', 'two', 'three']})
        cdict = {
            'fields': {
                'a': {
                    'type': 'int',
                    'sign': 'positive',
                }
            }
        }
        constraints = DatasetConstraints()
        constraints.initialize_from_dict(native_definite(cdict))
        v = verify(df, cdict, repair=False)
        self.assertFalse(v.fields['a']['type'])
        self.assertFalse(v.fields['a']['sign'])

    def testVerifyStringLengthWithWrongType(self):
        df = pd.DataFrame({'a': [1, 2, -1]})
        cdict = {
            'fields': {
                'a': {
                    'type': 'string',
                    'min_length': 2,
                    'max_length': 3,
                }
            }
        }
        constraints = DatasetConstraints()
        constraints.initialize_from_dict(native_definite(cdict))
        v = verify(df, cdict, repair=False)
        self.assertFalse(v.fields['a']['type'])
        self.assertFalse(v.fields['a']['min_length'])
        self.assertFalse(v.fields['a']['max_length'])

    def testDetectWithWrongTypes(self):
        df = pd.DataFrame({'a': [1, 2, 3], 'b': ['one', 'two', 'three']})
        cdict = {
            'fields': {
                'a': {
                    'type': 'string',
                    'min_length': 2,
                    'max_length': 3,
                },
                'b': {
                    'type': 'int',
                    'min': 1,
                    'max': 3,
                    'sign': 'positive',
                }
            }
        }
        constraints = DatasetConstraints()
        constraints.initialize_from_dict(native_definite(cdict))
        v = detect(df, cdict, per_constraint=True, output_fields=[],
                      interleave=True, repair=False)
        d = v.detected()
        self.assertTrue(not d['a_type_ok'].any())
        self.assertTrue(not d['b_type_ok'].any())
        self.assertTrue(not d['b_min_ok'].any())
        self.assertTrue(not d['b_max_ok'].any())

    def testVerifyWithMalformedInMemoryConstraintDict(self):
        df = pd.DataFrame({'a': [1, 2, 3], 'b': ['one', 'two', 'three']})
        cdicts = [
            [],
            {},
            {'fields': 'a'},
            {'fields': 22},
            {'fields': {
                    'a': 33,
                    'b': 'b',
                }
            }
        ]
        for cdict in cdicts:
            constraints = DatasetConstraints()
            with self.assertRaises(Exception):
                constraints.initialize_from_dict(native_definite(cdict))
                v = verify(df, cdict, repair=False)


