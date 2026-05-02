from flowtask.components.flow import FlowComponent


class Component(FlowComponent):
    def start():
        return True

    def run():
        return True

    def close():
        return True


def test_mask_replacement_recursively_simple_string():
    """
    This test verifies that the mask_replacement_recursively function
    correctly replaces a simple string with a defined mask.
    """
    # Define the mask and replacement value
    component = Component(masks={"{name}": "John"})

    # Test string with the mask
    test_string = "Hello, {name}!"

    # Call the function and assert the replaced string
    replaced_string = component.mask_replacement_recursively(test_string)
    assert replaced_string == "Hello, John!"


def test_mask_replacement_recursively_dictionary_values():
    """
    This test verifies that the mask_replacement_recursively function
    correctly replaces values in a dict with defined masks.
    """
    # Define the mask and replacement value
    component = Component(
        masks={"{name}": "John", "{city}": "London", "{country}": "UK", "{value}": 2}
    )

    # Test string with the mask
    test_dict = {
        "name": "{name}",
        "info": {"city": "{city}", "country": "{country}"},
        "values": [0, "{value}", 8],
    }

    # Call the function and assert the replaced string
    replaced_dict = component.mask_replacement_recursively(test_dict)
    assert replaced_dict == {
        "name": "John",
        "info": {"city": "London", "country": "UK"},
        "values": [0, "2", 8],
    }


def test_mask_replacement_recursively_dictionary_keys():
    """
    This test verifies that the mask_replacement_recursively function
    correctly replaces keys in a dict with defined masks.
    """
    # Define the mask and replacement value
    component = Component(masks={"{key1}": "name", "{key2}": "city"})

    # Test string with the mask
    test_dict = {"{key1}": "John", "info": {"{key2}": "London"}}

    # Call the function and assert the replaced string
    replaced_dict = component.mask_replacement_recursively(test_dict)
    assert replaced_dict == {
        "name": "John",
        "info": {"city": "London"},
    }


def test_mask_replacement_recursively_list():
    """
    This test verifies that the mask_replacement_recursively function
    correctly replaces a simple list with a defined mask.
    """
    # Define the mask and replacement value
    component = Component(masks={"{my_masked_value}": 2})

    # Test list with the mask
    test_list = [0, "{my_masked_value}", 8]

    # Call the function and assert the replaced list
    replaced_list = component.mask_replacement_recursively(test_list)
    assert replaced_list == [0, "2", 8]


def test_mask_replacement_recursively_missing_mask():
    """
    This test verifies that the mask_replacement_recursively function
    handles a case where a mask is not defined.
    """
    # Define a mask
    component = Component(mask={"{name}": "Charlie"})

    # Test string with a missing mask
    test_string = "Hello, {unknown}!"

    # Call the function and assert the original string (mask not replaced)
    replaced_string = component.mask_replacement_recursively(test_string)
    assert replaced_string == "Hello, {unknown}!"
