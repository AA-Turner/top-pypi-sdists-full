# Standard Library
from unittest.mock import MagicMock, patch

# Django
from django.test import TestCase

# Alliance Auth AFAT
from afat.helper.fatlinks import get_doctrines


class TestGetDoctrines(TestCase):
    """
    Test get_doctrines function
    """

    @patch("afat.helper.fatlinks.use_fittings_module_for_doctrines", return_value=True)
    @patch("fittings.models.Doctrine.objects")
    @patch("fittings.models.Fitting.objects")
    @patch("afat.helper.fatlinks.Prefetch", return_value=MagicMock())
    def test_returns_doctrines_with_fittings_module_enabled(
        self,
        mock_prefetch,
        mock_fitting_objects,
        mock_doctrine_objects,
        mock_use_fittings,
    ):
        """
        Test returns doctrines with fittings module enabled

        :param mock_prefetch:
        :type mock_prefetch:
        :param mock_fitting_objects:
        :type mock_fitting_objects:
        :param mock_doctrine_objects:
        :type mock_doctrine_objects:
        :param mock_use_fittings:
        :type mock_use_fittings:
        :return:
        :rtype:
        """

        mock_fitting_objects.select_related.return_value = MagicMock()

        # Ensure all common queryset chain methods return the same mock queryset
        mock_doctrine_objects.prefetch_related.return_value = mock_doctrine_objects
        mock_doctrine_objects.filter.return_value = mock_doctrine_objects
        mock_doctrine_objects.distinct.return_value = mock_doctrine_objects
        mock_doctrine_objects.values_list.return_value = mock_doctrine_objects
        mock_doctrine_objects.union.return_value = mock_doctrine_objects
        mock_doctrine_objects.order_by.return_value = mock_doctrine_objects

        # Make iterating the final queryset yield the expected doctrines
        mock_doctrine_objects.__iter__.return_value = iter(["Doctrine1", "Doctrine2"])

        result = get_doctrines()
        self.assertEqual(list(result), ["Doctrine1", "Doctrine2"])

    @patch("afat.helper.fatlinks.use_fittings_module_for_doctrines", return_value=True)
    @patch("afat.models.Doctrine.objects")
    @patch("fittings.models.Fitting.objects")
    @patch("afat.helper.fatlinks.Prefetch", return_value=MagicMock())
    def test_handles_empty_doctrines_with_fittings_module_enabled(
        self,
        mock_prefetch,
        mock_fitting_objects,
        mock_doctrine_objects,
        mock_use_fittings,
    ):
        mock_fitting_objects.select_related.return_value = MagicMock()
        mock_doctrine_objects.prefetch_related.return_value = mock_doctrine_objects
        mock_doctrine_objects.union.return_value.order_by.return_value = (
            mock_doctrine_objects
        )
        mock_doctrine_objects.__iter__.return_value = iter([])

        result = get_doctrines()
        self.assertEqual(list(result), [])

    @patch("afat.helper.fatlinks.use_fittings_module_for_doctrines", return_value=False)
    @patch("afat.models.Doctrine.objects")
    def test_handles_empty_doctrines_with_fittings_module_disabled(
        self, mock_doctrine_objects, mock_use_fittings
    ):
        mock_doctrine_objects.filter.return_value = mock_doctrine_objects
        mock_doctrine_objects.distinct.return_value = mock_doctrine_objects
        mock_doctrine_objects.order_by.return_value = mock_doctrine_objects
        mock_doctrine_objects.values_list.return_value = []

        result = get_doctrines()
        self.assertEqual(list(result), [])
