from ..string_clean import eatOuter
def get_user_input(text,default='y'):
    choices = '(y/n)' if default in ['y','n'] else ''
    response = input(f"{text} {choices}:({default}) ") or default
    if choices:
        response = response.lower() == 'y'
    return response
    
def enter_value_text(typ="", action="to filter by", parentObject="selection"):
    return input(f"Enter {typ} value {action} in {parentObject}: ")

def capitalize(string):
    return f"{string[0].upper()}{string[1:].lower()}"

def pluralize(string):
    return f"{eatOuter(string, ['s'])}s"

def get_integer_input(prompt, min_value, max_value):
    while True:
        try:
            value = int(input(f"{prompt} ({min_value}-{max_value}): "))
            if min_value <= value <= max_value:
                return value
            else:
                print(f"Please enter a number between {min_value} and {max_value}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def enumerate_selections(obj_list=[], parentObject="column", childObject=None):
    parent_plural = pluralize(capitalize(parentObject))
    output = f"Available {parent_plural}:" if childObject is None else f"{parent_plural} in {childObject}:"
    for idx, value in enumerate(obj_list):
        print(f"{idx + 1}. {value}")
    return obj_list

def list_objects(obj_list=None, parentObject=None, object_type='column'):
    if not obj_list:
        print(f"No {pluralize(object_type)} available.")
        return None
    object_choice = get_integer_input(f"Choose a {object_type}", 1, len(obj_list)) - 1
    return obj_list[object_choice]

def get_field_choice(obj_list, parentObject=None, object_type=None):
    enumerate_selections(obj_list=obj_list, parentObject=parentObject)
    return list_objects(obj_list=obj_list, parentObject=None, object_type=object_type)
