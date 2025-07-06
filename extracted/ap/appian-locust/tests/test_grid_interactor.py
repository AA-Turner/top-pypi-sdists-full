import json
import unittest
from copy import deepcopy
from appian_locust._grid_interactor import GridInteractor
from .mock_reader import read_mock_file_as_dict


class TestGridInteractor(unittest.TestCase):
    grid_interactor: GridInteractor = GridInteractor()
    grid_form_orig = read_mock_file_as_dict("report_with_rep_sales_grid.json")
    grid_record_powered = read_mock_file_as_dict("report_record_powered_grid.json")

    def setUp(self) -> None:
        self.grid_forms = deepcopy([self.grid_form_orig, self.grid_record_powered])

    def test_find_grid_by_label_success(self) -> None:
        form_labels_search = ['Top Sales Reps by Total Sales', 'Employees']
        form_labels_actual = ['Top Sales Reps by Total Sales', 'PagingGrid-Employees']
        form_label_keys = ['label', 'testLabel']
        for form_label, form_label_actual, grid_form, form_label_key in zip(form_labels_search, form_labels_actual, self.grid_forms, form_label_keys):
            grid = self.grid_interactor.find_grid_by_label(form_label, grid_form)
            self.assertEqual(grid[form_label_key], form_label_actual)

    def test_find_grid_by_label_missing(self) -> None:
        form_labels = ['Topest Sales Reps by Total Sales', 'Employed']
        for form_label, grid_form in zip(form_labels, self.grid_forms):
            with self.assertRaisesRegex(Exception, f"Grid with label '{form_label}' not found in form"):
                grid = self.grid_interactor.find_grid_by_label(form_label, grid_form)

    def test_find_grid_by_index(self) -> None:
        form_labels = ['Top Sales Reps by Total Sales', None]
        for form_label, grid_form in zip(form_labels, self.grid_forms):
            grid = self.grid_interactor.find_grid_by_index(0, grid_form)
            self.assertEqual(grid.get('label'), form_label)

    def test_find_grid_by_index_multiple_types(self) -> None:
        form_labels = ['PagingGrid-FirstPagingGrid', 'SecondGridField']
        indices = [1, 2]
        form_label_keys = ['testLabel', 'label']
        grid_form = read_mock_file_as_dict("multi_grid_types.json")
        for form_label, index, form_label_key in zip(form_labels, indices, form_label_keys):
            grid = self.grid_interactor.find_grid_by_index(index, grid_form)
            self.assertEqual(grid[form_label_key], form_label)

    def test_find_grid_by_index_out_of_range(self) -> None:
        for grid_form in self.grid_forms:
            with self.assertRaisesRegex(Exception, 'Index 5 out of range'):
                grid = self.grid_interactor.find_grid_by_index(5, grid_form)

    def test_find_grid_no_grids_found(self) -> None:
        with self.assertRaisesRegex(Exception, 'No grids found in form'):
            grid = self.grid_interactor.find_grid_by_index(5, {})

    def test_find_grid_by_label_different(self) -> None:
        form_labels = ['Orders & Sales Reps Performance', 'Employee Information']
        for form_label, grid_form in zip(form_labels, self.grid_forms):
            with self.assertRaisesRegex(Exception, f"Grid with label '{form_label}' not found in form"):
                grid = self.grid_interactor.find_grid_by_label(form_label, grid_form)

    def test_move_to_end_and_beginning(self) -> None:
        form_labels = ['Top Sales Reps by Total Sales', 'Employees']
        for form_label, grid_form in zip(form_labels, self.grid_forms):
            grid = self.grid_interactor.find_grid_by_label(form_label, grid_form)

            end_save_value = self.grid_interactor.move_to_last_page(grid)
            if end_save_value.get('pagingInfo'):
                self.assertEqual(91, end_save_value['pagingInfo']['startIndex'])
            else:
                self.assertEqual(91, end_save_value['startIndex'])

            # Now at the end
            grid['value'] = end_save_value

            beginning_save_value = self.grid_interactor.move_to_first_page(grid)
            if end_save_value.get('pagingInfo'):
                self.assertEqual(1, beginning_save_value['pagingInfo']['startIndex'])
            else:
                self.assertEqual(1, beginning_save_value['startIndex'])

    def test_move_to_right_left_boundaries(self) -> None:
        form_labels = ['Top Sales Reps by Total Sales', 'Employees']
        for form_label, grid_form in zip(form_labels, self.grid_forms):
            grid = self.grid_interactor.find_grid_by_label(form_label, grid_form)

            beginning_save_value = self.grid_interactor.move_to_the_left(grid)
            if beginning_save_value.get('pagingInfo'):
                self.assertEqual(1, beginning_save_value['pagingInfo']['startIndex'])
            else:
                self.assertEqual(1, beginning_save_value['startIndex'])

            # Now at the end
            grid['value']['startIndex'] = 91

            beginning_save_value = self.grid_interactor.move_to_the_right(grid)
            if beginning_save_value.get('pagingInfo'):
                self.assertEqual(11, beginning_save_value['pagingInfo']['startIndex'])
            else:
                self.assertEqual(91, beginning_save_value['startIndex'])

    def test_move_to_right_and_left(self) -> None:
        form_labels = ['Top Sales Reps by Total Sales', 'Employees']
        for form_label, grid_form in zip(form_labels, self.grid_forms):
            grid = self.grid_interactor.find_grid_by_label(form_label, grid_form)

            save_value = self.grid_interactor.move_to_the_right(grid)
            if save_value.get('pagingInfo'):
                self.assertEqual(11, save_value['pagingInfo']['startIndex'])
            else:
                self.assertEqual(11, save_value['startIndex'])

            grid['value'] = save_value

            save_value = self.grid_interactor.move_to_the_left(grid)
            if save_value.get('pagingInfo'):
                self.assertEqual(1, save_value['pagingInfo']['startIndex'])
            else:
                self.assertEqual(1, save_value['startIndex'])

    def test_sort_ascending_and_descending_error(self) -> None:
        form_labels = ['Top Sales Reps by Total Sales', 'Employees']
        for form_label, grid_form in zip(form_labels, self.grid_forms):
            grid = self.grid_interactor.find_grid_by_label(form_label, grid_form)
            with self.assertRaisesRegex(Exception, "Cannot sort, field 'fake' not found"):
                self.grid_interactor.sort_grid(field_name='fake', paging_grid=grid)

    def test_sort_ascending_and_descending(self) -> None:
        form_labels = ['Top Sales Reps by Total Sales', 'Employees']
        fields_to_sort = [['Total', 'AccountOwner'], ['First Name', 'Email']]
        for form_label, grid_form, field_to_sort in zip(form_labels, self.grid_forms, fields_to_sort):
            field_name = field_to_sort.pop(0)
            grid = self.grid_interactor.find_grid_by_label(form_label, grid_form)
            sort_save = self.grid_interactor.sort_grid(field_name=field_name, ascending=True, paging_grid=grid)

            if sort_save.get('pagingInfo'):
                self.assertTrue('urn:appian:record-field:v1' in sort_save['pagingInfo']['sort'][0]['field'])
            else:
                self.assertEqual(sort_save['sort'][0]['field'], field_name)
                self.assertEqual(sort_save['sort'][0]['ascending'], True)

            field_name = field_to_sort.pop(0)
            sort_save = self.grid_interactor.sort_grid(field_name=field_name, ascending=False, paging_grid=grid)

            if sort_save.get('pagingInfo'):
                self.assertTrue('urn:appian:record-field:v1' in sort_save['pagingInfo']['sort'][0]['field'])
            else:
                self.assertEqual(sort_save['sort'][0]['field'], field_name)
                self.assertEqual(sort_save['sort'][0]['ascending'], False)


if __name__ == '__main__':
    unittest.main()
