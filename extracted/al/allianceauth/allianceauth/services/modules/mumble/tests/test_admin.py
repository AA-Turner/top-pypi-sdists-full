from django.test import TestCase
from django.forms import ValidationError

from ..admin import IdlerHandlerForm


class IdlerHandlerAdminTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form_data = {'name': 'test', 'channel': 1, 'seconds': 1, 'interval': 1, 'denylist': True}

    def test_clean_list_valid(self):
        data = self.form_data | {'list': '1,2,3'}
        form = IdlerHandlerForm(data=data)
        self.assertTrue(form.is_valid())

    def test_clean_list_spaces(self):
        data = self.form_data | {'list': '1, 2 , 3'}
        form = IdlerHandlerForm(data=data)
        self.assertTrue(form.is_valid())

    def test_clean_list_invalid(self):
        data = self.form_data | {'list': '1,2,test'}
        form = IdlerHandlerForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('list', form.errors)
        self.assertIn('test', form.errors['list'][0])

    def test_clean_list_strips_spaces(self):
        data = self.form_data | {'list': '1, 2 , 3'}
        form = IdlerHandlerForm(data=data)
        form.full_clean()
        self.assertEqual('1,2,3', form.cleaned_data['list'])

    def test_clean_list_handles_blank(self):
        data = self.form_data | {'list': ""}
        form = IdlerHandlerForm(data=data)
        self.assertTrue(form.is_valid())
