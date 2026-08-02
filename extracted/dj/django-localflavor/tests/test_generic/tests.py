from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.test import SimpleTestCase, TestCase
from django.utils import formats

from localflavor.generic.countries.sepa import IBAN_SEPA_COUNTRIES
from localflavor.generic.forms import BICFormField, DateField, DateTimeField, IBANFormField, SplitDateTimeField
from localflavor.generic.models import BICField, IBANField
from localflavor.generic.validators import BICValidator, EANValidator, IBANValidator

from .forms import UseIncludedCountriesForm, UseNordeaExtensionsForm


class DateTimeFieldTestCase(SimpleTestCase):

    default_date_input_formats = (
        '%Y-%m-%d', '%d/%m/%Y', '%d/%m/%y', '%b %d %Y', '%b %d, %Y',
        '%d %b %Y', '%d %b, %Y', '%B %d %Y', '%B %d, %Y', '%d %B %Y',
        '%d %B, %Y',
    )

    default_datetime_input_formats = (
        '%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d', '%d/%m/%Y %H:%M:%S',
        '%d/%m/%Y %H:%M', '%d/%m/%Y', '%d/%m/%y %H:%M:%S', '%d/%m/%y %H:%M',
        '%d/%m/%y',
    )

    def assertInputFormats(self, field, formats):
        self.assertSequenceEqual(field.input_formats, formats)


class DateFieldTests(DateTimeFieldTestCase):

    def setUp(self):
        self.default_input_formats = self.default_date_input_formats

    def test_init_no_input_formats(self):
        field = DateField()
        self.assertInputFormats(field, self.default_input_formats)

    def test_init_empty_input_formats(self):
        field = DateField(input_formats=())
        self.assertInputFormats(field, self.default_input_formats)

    def test_init_custom_input_formats(self):
        input_formats = ('%m/%d/%Y', '%m/%d/%y')
        field = DateField(input_formats=input_formats)
        self.assertInputFormats(field, input_formats)


class DateTimeFieldTests(DateTimeFieldTestCase):

    def setUp(self):
        self.default_input_formats = self.default_datetime_input_formats

    def test_init_no_input_formats(self):
        field = DateTimeField()
        self.assertInputFormats(field, self.default_input_formats)

    def test_init_empty_input_formats(self):
        field = DateTimeField(input_formats=())
        self.assertInputFormats(field, self.default_input_formats)

    def test_init_custom_input_formats(self):
        input_formats = ('%m/%d/%Y %H:%M', '%m/%d/%y %H:%M')
        field = DateTimeField(input_formats=input_formats)
        self.assertInputFormats(field, input_formats)


class SplitDateTimeFieldTests(DateTimeFieldTestCase):

    default_time_input_formats = formats.get_format_lazy('TIME_INPUT_FORMATS')

    def test_init_no_input_formats(self):
        field = SplitDateTimeField()
        date_field, time_field = field.fields
        self.assertInputFormats(date_field, self.default_date_input_formats)
        self.assertInputFormats(time_field, self.default_time_input_formats)

    def test_init_empty_input_formats(self):
        field = SplitDateTimeField(input_date_formats=(),
                                   input_time_formats=())
        date_field, time_field = field.fields
        self.assertInputFormats(date_field, self.default_date_input_formats)
        self.assertInputFormats(time_field, ())

    def test_init_custom_input_formats(self):
        date_input_formats = ('%m/%d/%Y', '%m/%d/%y')
        time_input_formats = ('%H:%M', '%H:%M:%S')
        field = SplitDateTimeField(input_date_formats=date_input_formats,
                                   input_time_formats=time_input_formats)
        date_field, time_field = field.fields
        self.assertInputFormats(date_field, date_input_formats)
        self.assertInputFormats(time_field, time_input_formats)


class IBANTests(TestCase):
    def test_iban_validator__example_ibans(self):
        # IBAN Registry v101 example IBANs published here:
        # https://www.swift.com/swift-resource/11971/download
        valid_ibans = [
            "AD12 0001 2030 2003 5910 0100",
            "AE07 0331 2345 6789 0123 456",
            "AL47 2121 1009 0000 0002 3569 8741",
            "AT61 1904 3002 3457 3201",
            "AZ21 NABZ 0000 0000 1370 1000 1944",
            "BA39 1290 0794 0102 8494",
            # "BE68 5390 0754 7034", - Can't use example from the IBAN registry because 539 is not a valid bank code.
            "BE41 0630 1234 5610",  # Alternate example with a valid bank.
            "BG80 BNBG 9661 1020 3456 78",
            "BH67 BMAG 0000 1299 1234 56",
            "BI42 10000 10001 00003320451 81",
            "BR18 0036 0305 0000 1000 9795 493C 1",
            "BY13 NBRB 3600 9000 0000 2Z00 AB00",
            "CH93 0076 2011 6238 5295 7",
            "CR05 0152 0200 1026 2840 66",
            "CY17 0020 0128 0000 0012 0052 7600",
            "CZ65 0800 0000 1920 0014 5399",
            "DE89 3704 0044 0532 0130 00",
            "DJ21 0001 0000 0001 5400 0100 186",
            "DK50 0040 0440 1162 43",
            "DO28 BAGR 0000 0001 2124 5361 1324",
            "EE38 2200 2210 2014 5685",
            "EG38 0019 0005 0000 0000 2631 8000 2",
            "ES91 2100 0418 4502 0005 1332",
            "FI21 1234 5600 0007 85",
            "FK88 SC12 3456 7890 12",
            "FO62 6460 0001 6316 34",
            "FR14 2004 1010 0505 0001 3M02 606",
            "GB29 NWBK 6016 1331 9268 19",
            "GE29 NB00 0000 0101 9049 17",
            "GI75 NWBK 0000 0000 7099 453",
            "GL89 6471 0001 0002 06",
            "GR16 0110 1250 0000 0001 2300 695",
            "GT82 TRAJ 0102 0000 0012 1002 9690",
            "HN88 CABF 0000 0000 0002 5000 5469",
            "HR12 1001 0051 8630 0016 0",
            "HU42 1177 3016 1111 1018 0000 0000",
            "IE29 AIBK 9311 5212 3456 78",
            "IL62 0108 0000 0009 9999 999",
            "IQ98 NBIQ 8501 2345 6789 012",
            "IS14 0159 2600 7654 5510 7303 39",
            "IT60 X054 2811 1010 0000 0123 456",
            "JO94 CBJO 0010 0000 0000 0131 0003 02",
            "KW81 CBKU 0000 0000 0000 1234 5601 01",
            "KZ86 125K ZT50 0410 0100",
            "LB62 0999 0000 0001 0019 0122 9114",
            "LC55 HEMM 0001 0001 0012 0012 0002 3015",
            "LI21 0881 0000 2324 013A A",
            "LT12 1000 0111 0100 1000",
            "LU28 0019 4006 4475 0000",
            "LV80 BANK 0000 4351 9500 1",
            "LY83 002 048 000020100120361",
            "MC58 1122 2000 0101 2345 6789 030",
            "MD24 AG00 0225 1000 1310 4168",
            "ME25 5050 0001 2345 6789 51",
            "MK07 2501 2000 0058 984",
            "MN12 1234 1234 5678 9123",
            "MR13 0002 0001 0100 0012 3456 753",
            "MT84 MALT 0110 0001 2345 MTLC AST0 01S",
            "MU17 BOMM 0101 1010 3030 0200 000M UR",
            "NI45 BAPR 0000 0013 0000 0355 8124",
            "NL91 ABNA 0417 1643 00",
            "NO93 8601 1117 947",
            "OM81 0180 0000 0129 9123 456",
            "PK36 SCBL 0000 0011 2345 6702",
            "PL61 1090 1014 0000 0712 1981 2874",
            "PS92 PALS 0000 0000 0400 1234 5670 2",
            "PT50 0002 0123 1234 5678 9015 4",
            "QA58 DOHB 0000 1234 5678 90AB CDEF G",
            "RO49 AAAA 1B31 0075 9384 0000",
            "RS35 2600 0560 1001 6113 79",
            "RU03 0445 2522 5408 1781 0538 0913 1041 9",
            "SA03 8000 0000 6080 1016 7519",
            "SC18 SSCB 1101 0000 0000 0000 1497 USD",
            "SD21 2901 0501 2340 01",
            "SE45 5000 0000 0583 9825 7466",
            "SI56 2633 0001 2039 086",
            "SK31 1200 0000 1987 4263 7541",
            "SM86 U032 2509 8000 0000 0270 100",
            "SO21 1000 0010 0100 0100 141",
            "ST23 0001 0001 0051 8453 1014 6",
            "SV62 CENR 0000 0000 0000 0070 0025",
            "TL38 0080 0123 4567 8910 157",
            "TN59 1000 6035 1835 9847 8831",
            "TR33 0006 1005 1978 6457 8413 26",
            "UA21 3223 1300 0002 6007 2335 6600 1",
            "VA59 001 1230 0001 2345 678",
            "VG96 VPVG 0000 0123 4567 8901",
            "XK05 1212 0123 4567 8906",
            "YE15 CBYE 0001 0188 6123 4567 8912 34",
        ]
        iban_validator = IBANValidator()
        for iban in valid_ibans:
            with self.subTest(iban=iban):
                iban_validator(iban)  # No exception raised.

    def test_iban_validator(self):
        valid = [
            'GB82WeST12345698765432',
            'GB82 WEST 1234 5698 7654 32',

            'GR1601101250000000012300695',
            'GR16-0110-1250-0000-0001-2300-695',

            'GB29NWBK60161331926819',
            'GB29N-WB K6016-13319-26819',

            'SA0380000000608010167519',
            'SA0380 0 0000 06 0 8 0 1 0 1 6 7 519 ',

            'CH9300762011623852957',
            'IL620108000000099999999',
            'EE982200221111099080',
            'VA59001123000012345678',

            None,
        ]

        invalid = {
            'GB82WEST1234569876543': 'GB IBANs must contain 22 characters.',
            'CA34CIBC123425345': 'CA is not a valid country code for IBAN.',
            'GB29ÉWBK60161331926819': 'is not a valid character for IBAN.',
            'SA0380000000608019167519': 'Not a valid IBAN.',
            'EE012200221111099080': 'Not a valid IBAN.',
            'IT2813815463652787128285355': 'Not a valid IBAN.',
        }

        iban_validator = IBANValidator()
        for iban in valid:
            with self.subTest(iban=iban):
                iban_validator(iban)

        for iban in invalid:
            with self.subTest(iban=iban):
                self.assertRaisesMessage(ValidationError, invalid[iban], IBANValidator(), iban)

    def test_iban_validator_deconstruct(self):
        # Call to the required deconstruct method to see if it exists and
        # it doesn't throw an error.
        IBANValidator().deconstruct()

        test_cases = [
            {'use_nordea_extensions': True, 'include_countries': ['IS', 'IT']},
            {'use_nordea_extensions': True},
            {'include_countries': ['IS', 'IT']},
            {},
        ]

        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                iban1 = IBANValidator(**test_case)
                iban2 = IBANValidator(**test_case)
                self.assertEqual(iban1, iban2, msg="IBAN validators with equal parameters are not equal.")

    def test_iban_fields(self):
        """Test the IBAN model and form field."""
        valid = {
            'NL02ABNA0123456789': 'NL02ABNA0123456789',
            'Nl02aBNa0123456789': 'NL02ABNA0123456789',
            'NL02 ABNA 0123 4567 89': 'NL02ABNA0123456789',
            'NL02-ABNA-0123-4567-89': 'NL02ABNA0123456789',

            'NL91ABNA0417164300': 'NL91ABNA0417164300',
            'NL91 ABNA 0417 1643 00': 'NL91ABNA0417164300',
            'NL91-ABNA-0417-1643-00': 'NL91ABNA0417164300',

            'MU17BOMM0101101030300200000MUR': 'MU17BOMM0101101030300200000MUR',
            'MU17 BOMM 0101 1010 3030 0200 000M UR': 'MU17BOMM0101101030300200000MUR',
            'MU 17BO MM01011010 3030-02 000-00M UR': 'MU17BOMM0101101030300200000MUR',

            'BE31538007547055': 'BE31538007547055',
            'BE31 5380 0754 7055': 'BE31538007547055',
            'BE-315380075470 55': 'BE31538007547055',
        }

        invalid = {
            'NL02ABNA012345678999': ['NL IBANs must contain 18 characters.'],
            'NL02 ABNA 0123 4567 8999': ['NL IBANs must contain 18 characters.'],

            'NL91ABNB0417164300': ['Not a valid IBAN.'],
            'NL91 ABNB 0417 1643 00': ['Not a valid IBAN.'],

            'MU17BOMM0101101030300200000MUR12345': ['MU IBANs must contain 30 characters.'],
            'MU17 BOMM 0101 1010 3030 0200 000M UR12 345': ['MU IBANs must contain 30 characters.'],

            # This IBAN should only be valid only if the Nordea extensions are turned on.
            'BJ11B00610100400271101192591': ['BJ is not a valid country code for IBAN.'],
            'BJ11 B006 1010 0400 2711 0119 2591': ['BJ is not a valid country code for IBAN.']
        }

        self.assertFieldOutput(IBANFormField, valid=valid, invalid=invalid)

        # Test valid inputs for model field.
        iban_model_field = IBANField()
        for input, output in valid.items():
            with self.subTest(input=input, output=output):
                self.assertEqual(iban_model_field.clean(input, None), output)

        self.assertIsNone(iban_model_field.to_python(None))

        # Invalid inputs for model field.

        # The model field has max_length set which means the max length validator is used, unlike the form.
        invalid['MU17BOMM0101101030300200000MUR12345'] = [
            'MU IBANs must contain 30 characters.',
            'Ensure this value has at most 34 characters (it has 35).'
        ]
        invalid['MU17 BOMM 0101 1010 3030 0200 000M UR12 345'] = [
            'MU IBANs must contain 30 characters.',
            'Ensure this value has at most 34 characters (it has 35).',
        ]

        for input, errors in invalid.items():
            with self.subTest(input=input, errors=errors):
                with self.assertRaises(ValidationError) as context_manager:
                    iban_model_field.clean(input, None)
                # The error messages for models are in a different order.
                errors.reverse()
                self.assertEqual(context_manager.exception.messages, errors)

    def test_nordea_extensions(self):
        """Test a valid IBAN in the Nordea extensions."""
        iban_validator = IBANValidator(use_nordea_extensions=True)
        # Run the validator to ensure there are no ValidationErrors raised.
        iban_validator('Bj11B00610100400271101192591')

    def test_use_nordea_extensions_formfield(self):
        form = UseNordeaExtensionsForm({'iban': 'BJ11B00610100400271101192591'})
        self.assertFalse(form.errors)

    def test_include_countries_formfield(self):
        valid_not_included = 'CH9300762011623852957'
        form = UseIncludedCountriesForm({'iban': valid_not_included})
        self.assertRaises(ValidationError, form.fields['iban'].run_validators, valid_not_included)

    def test_form_field_formatting(self):
        iban_form_field = IBANFormField()
        self.assertEqual(iban_form_field.prepare_value('NL02ABNA0123456789'), 'NL02 ABNA 0123 4567 89')
        self.assertEqual(iban_form_field.prepare_value('NL02 ABNA 0123 4567 89'), 'NL02 ABNA 0123 4567 89')
        self.assertIsNone(iban_form_field.prepare_value(None))
        self.assertEqual(iban_form_field.to_python(None), '')

    def test_include_countries(self):
        """Test the IBAN model and form include_countries feature."""
        include_countries = ('NL', 'BE', 'LU')

        valid = {
            'NL02ABNA0123456789': 'NL02ABNA0123456789',
            'BE31538007547055': 'BE31538007547055',
            'LU280019400644750000': 'LU280019400644750000'
        }

        invalid = {
            # This IBAN is valid but not for the configured countries.
            'GB82WEST12345698765432': ['GB IBANs are not allowed in this field.']
        }

        self.assertFieldOutput(IBANFormField, field_kwargs={'include_countries': include_countries},
                               valid=valid, invalid=invalid)

        # Test valid inputs for model field.
        iban_model_field = IBANField(include_countries=include_countries)
        for input, output in valid.items():
            with self.subTest(input=input, output=output):
                self.assertEqual(iban_model_field.clean(input, None), output)

        # Invalid inputs for model field.
        for input, errors in invalid.items():
            with self.subTest(input=input, errors=errors):
                with self.assertRaises(ValidationError) as context_manager:
                    iban_model_field.clean(input, None)
                # The error messages for models are in a different order.
                errors.reverse()
                self.assertEqual(context_manager.exception.messages, errors)

    def test_misconfigured_include_countries(self):
        """Test that an IBAN field or model raises an error when asked to validate a country not part of IBAN."""
        # Test an unassigned ISO 3166-1 country code.
        self.assertRaises(ImproperlyConfigured, IBANValidator, include_countries=('JJ',))
        self.assertRaises(ImproperlyConfigured, IBANValidator, use_nordea_extensions=True, include_countries=('JJ',))

        # Test a Nordea IBAN when Nordea extensions are turned off.
        self.assertRaises(ImproperlyConfigured, IBANValidator, include_countries=('AO',))

    def test_sepa_countries(self):
        """Test include_countries using the SEPA counties."""
        # A few SEPA valid IBANs.
        valid = {
            'GI75 NWBK 0000 0000 7099 453': 'GI75NWBK000000007099453',
            'CH93 0076 2011 6238 5295 7': 'CH9300762011623852957',
            'GB29 NWBK 6016 1331 9268 19': 'GB29NWBK60161331926819'
        }

        # A few non-SEPA valid IBANs.
        invalid = {
            'SA03 8000 0000 6080 1016 7519': ['SA IBANs are not allowed in this field.'],
            'CR05 0152 0200 1026 2840 66': ['CR IBANs are not allowed in this field.'],
            'XK05 1212 0123 4567 8906': ['XK IBANs are not allowed in this field.']
        }

        self.assertFieldOutput(IBANFormField, field_kwargs={'include_countries': IBAN_SEPA_COUNTRIES},
                               valid=valid, invalid=invalid)

    def test_default_form(self):
        iban_model_field = IBANField()
        self.assertEqual(type(iban_model_field.formfield()), type(IBANFormField()))

    def test_model_field_deconstruct(self):
        # test_instance must be created with the non-default options.
        test_instance = IBANField(include_countries=('NL', 'BE'), use_nordea_extensions=True)
        name, path, args, kwargs = test_instance.deconstruct()
        new_instance = IBANField(*args, **kwargs)
        for attr in ('include_countries', 'use_nordea_extensions'):
            with self.subTest(attr=attr):
                self.assertEqual(getattr(test_instance, attr), getattr(new_instance, attr))

    def test_model_form_input_max_length(self):
        form = UseNordeaExtensionsForm({
            "iban": "RU03 0445 2522 5408 1781 0538 0913 1041 9",
        })
        self.assertEqual(None, form.fields["iban"].max_length)
        self.assertEqual(42, form.fields["iban"].widget.attrs["max_length"])

        form.save()  # Not validation error raised.

    def test_form_field_input_max_length_without_model_form(self):
        form_field = IBANFormField()
        self.assertEqual(None, form_field.max_length)
        self.assertEqual(42, form_field.widget.attrs["max_length"])


class BICTests(TestCase):
    def test_bic_validator(self):
        valid = [
            'DEUTDEFF',
            'deutdeff',

            'NEDSZAJJXXX',
            'NEDSZAJJxxx',

            'DABADKKK',
            'daBadKkK',

            'UNCRIT2B912',
            'DSBACNBXSHA',

            None,
        ]

        invalid = {
            'NEDSZAJJXX': 'BIC codes have either 8 or 11 characters.',
            '': 'BIC codes have either 8 or 11 characters.',
            'CIBCJJH2': 'JJ is not a valid country code.',
            'D3UTDEFF': 'is not a valid institution code.',
            'DAAEDEDOXXX': 'is not a valid location code.',
            'DÉUTDEFF': 'codes only contain alphabet letters and digits.',
            'NEDSZAJJ XX': 'codes only contain alphabet letters and digits.',
        }

        bic_validator = BICValidator()
        for bic in valid:
            with self.subTest():
                bic_validator(bic)

        for bic in invalid:
            with self.subTest():
                self.assertRaisesMessage(ValidationError,  invalid[bic], BICValidator(), bic)

    def test_bic_validator_deconstruct(self):
        bic1 = BICValidator()
        bic2 = BICValidator()
        self.assertEqual(bic1, bic2, msg="BIC validators are not equal.")

        # Call to the deconstruct method to see if it exists.
        bic1.deconstruct()

    def test_form_field_formatting(self):
        bic_form_field = BICFormField()
        self.assertEqual(bic_form_field.prepare_value('deutdeff'), 'DEUTDEFF')
        self.assertIsNone(bic_form_field.prepare_value(None))
        self.assertEqual(bic_form_field.to_python(None), '')

    def test_bic_model_field(self):
        valid = {
            'DEUTDEFF': 'DEUTDEFF',
            'NEDSZAJJXXX': 'NEDSZAJJXXX',
            'DABADKKK': 'DABADKKK',
            'UNCRIT2B912': 'UNCRIT2B912',
            'DSBACNBXSHA': 'DSBACNBXSHA'
        }

        invalid = {
            'NEDSZAJJXX': ['BIC codes have either 8 or 11 characters.'],
            'CIBCJJH2': ['JJ is not a valid country code.'],
            'D3UTDEFF': ['D3UT is not a valid institution code.']
        }

        self.assertFieldOutput(BICFormField, valid=valid, invalid=invalid)

        bic_model_field = BICField()

        # Test valid inputs for model field.
        for input, output in valid.items():
            with self.subTest(input=input, output=output):
                self.assertEqual(bic_model_field.clean(input, None), output)

        self.assertIsNone(bic_model_field.to_python(None))

        # Invalid inputs for model field.
        for input, errors in invalid.items():
            with self.subTest(input=input, errors=errors):
                with self.assertRaises(ValidationError) as context_manager:
                    bic_model_field.clean(input, None)
                self.assertEqual(errors, context_manager.exception.messages)

    def test_default_form(self):
        bic_model_field = BICField()
        self.assertEqual(type(bic_model_field.formfield()), type(BICFormField()))


class EANTests(TestCase):

    def test_ean_validator(self):
        valid = [
            '4006381333931',
            '73513537',

            '012345678905',
            '0012345678905',

            None,
        ]
        error_message = 'Not a valid EAN code.'
        invalid = [
            '400.6381.3339.31',
            '4006381333930',
            '',
            '0',
            'DÉUTDEFF',
        ]

        validator = EANValidator()
        for value in valid:
            with self.subTest(value=value):
                validator(value)

        for value in invalid:
            with self.subTest(value=value):
                self.assertRaisesMessage(ValidationError,  error_message, validator, value)

    def test_ean_validator_deconstruct(self):
        # Call to the required deconstruct method to see if it exists and
        # it doesn't throw an error.
        EANValidator().deconstruct()

        test_cases = [
            {'strip_nondigits': True, 'message': 'test'},
            {'message': 'test'},
            {'strip_nondigits': True},
            {},
        ]

        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                ean1 = EANValidator(**test_case)
                ean2 = EANValidator(**test_case)
                self.assertEqual(ean1, ean2, msg="EAN validators with equal parameters are not equal.")

    def test_ean_validator_strip_nondigits(self):
        valid = [
            '4006381333931',
            '400.6381.3339.31',
            '73513537',
            '73-51-3537',
            '73 51 3537',
            '73A51B3537',

            '012345678905',
            '0012345678905',

            None,
        ]
        error_message = 'Not a valid EAN code.'
        invalid = [
            '4006381333930',
            '400-63-813-339-30',
            '400 63 813 339 30',
            '',
            '0',
            'DÉUTDEFF',
        ]

        validator = EANValidator(strip_nondigits=True)
        for value in valid:
            with self.subTest(value=value):
                validator(value)

        for value in invalid:
            with self.subTest(value=value):
                self.assertRaisesMessage(ValidationError,  error_message, validator, value)
