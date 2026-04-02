from django.test import TestCase

from aa_contacts.forms import AllianceContactForm, CorporationContactForm


class TestForms(TestCase):

    def test_alliance(self):
        form = AllianceContactForm()
        for field, data in form.fields.items():
            if field != 'notes':
                self.assertTrue(data.disabled)
            else:
                self.assertFalse(data.disabled)

    def test_corporation(self):
        form = CorporationContactForm()
        for field, data in form.fields.items():
            if field != 'notes':
                self.assertTrue(data.disabled)
            else:
                self.assertFalse(data.disabled)
