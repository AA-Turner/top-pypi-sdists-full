from django.test import TestCase
from django.urls import reverse

from app_utils.testdata_factories import UserMainFactory


class TestHooks(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = UserMainFactory()

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.html_menu = f"""
            <a class="nav-link flex-fill align-self-center me-auto active" href="{reverse('aa_contacts:index')}">
                Contacts
            </a>
        """

    def test_menu_hook(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('aa_contacts:dashboard'))
        self.assertContains(response, self.html_menu, html=True)
