from cuga.backend.utils.consts import (
    HUMAN_IN_THE_LOOP_FUNC_NAME,
    ONLY_VALUE_ACTIONS,
    STATELESS_ACTIONS,
)


def transform_action(action):
    name = action['name']
    try:
        state = action['args']['state']
    except Exception:
        return f"# Unsupported action or missing state: {name}: {action}"

    # try to extract id and value from state if exists
    if isinstance(state, dict):
        if name in STATELESS_ACTIONS:
            return f"{name}()"

        if len(state) == 0:
            return f"# Unsupported action or missing state: {name}"

        keys = list(state.keys())
        if name in ONLY_VALUE_ACTIONS:
            value = state.get(keys[0], None)
            state = {'message': value}
        else:
            id = state.get(keys[0], None)
            value = state.get(keys[1], None)
            if id and value:
                state = {id: value}

    if name == 'read_page':
        return "read_page()"

    elif name in ['answer', 'human_in_the_loop']:
        name = HUMAN_IN_THE_LOOP_FUNC_NAME if name == 'human_in_the_loop' else name
        # Try to extract the answer content from various possible formats
        if isinstance(state, dict):
            # If state is a dictionary, look for common keys
            answer_keys = ['text', 'content', 'answer', 'message']
            for key in answer_keys:
                if key in state:
                    return f"{name}('''{state[key]}''')"

            # If no common keys found, use the first value in the dictionary
            if state:
                return f"{name}('''{next(iter(state.values()))}''')"

        # If state is not a dictionary or is empty, use it directly
        return f"{name}('''{state}''')"

    elif name == 'type':
        return f"fill('{id}', '''{value}''')"

    elif name == 'click':
        return f"click('{id}')"

    elif name == 'select_option':
        if isinstance(value, list):
            value_str = "[" + ", ".join(f"'{v}'" for v in value) + "]"
        else:
            value_str = f"'{value}'"
        return f"select_option('{id}', {value_str})"

    elif name == 'hover':
        return f"hover('{id}')"

    elif name == 'select':
        options = state['value']
        if isinstance(options, list):
            options = [f"'{opt}'" for opt in options]
            options = f"[{', '.join(options)}]"
        else:
            options = f"'{options}'"
        return f"select_option('{id}', {options})"

    elif name == 'check':
        return f"check('{id}')"

    elif name == 'uncheck':
        return f"uncheck('{state[0]}')"

    elif name == 'press':
        return f"press('{id}', '{value}')"

    elif name == 'focus':
        return f"focus('{id}')"

    elif name == 'clear':
        return f"clear('{id}')"

    elif name == 'drag_and_drop':
        return f"drag_and_drop('{state['from_id']}', '{state['to_id']}')"

    elif name == 'scroll':
        return f"scroll({state['delta_x']}, {state['delta_y']})"

    elif name == 'mouse_move':
        return f"mouse_move({state['x']}, {state['y']})"

    elif name == 'mouse_up':
        button = state.get('button', 'left')
        return f"mouse_up({state['x']}, {state['y']}, '{button}')"

    elif name == 'mouse_down':
        button = state.get('button', 'left')
        return f"mouse_down({state['x']}, {state['y']}, '{button}')"

    elif name == 'mouse_click':
        button = state.get('button', 'left')
        return f"mouse_click({state['x']}, {state['y']}, '{button}')"

    elif name == 'mouse_dblclick':
        button = state.get('button', 'left')
        return f"mouse_dblclick({state['x']}, {state['y']}, '{button}')"

    elif name == 'mouse_drag_and_drop':
        return f"mouse_drag_and_drop({state['from_x']}, {state['from_y']}, {state['to_x']}, {state['to_y']})"

    elif name == 'keyboard_press':
        return f"keyboard_press('{state['key']}')"

    elif name == 'keyboard_up':
        return f"keyboard_up('{state['key']}')"

    elif name == 'keyboard_down':
        return f"keyboard_down('{state['key']}')"

    elif name == 'keyboard_type':
        return f"keyboard_type('{state['text']}')"

    elif name == 'keyboard_insert_text':
        return f"keyboard_insert_text('{state['text']}')"

    elif name == 'goto':
        return f"goto('{state['url']}')"

    elif name == 'go_back':
        return "go_back()"

    elif name == 'go_forward':
        return "go_forward()"

    elif name == 'new_tab':
        return "new_tab()"

    elif name == 'tab_close':
        return "tab_close()"

    elif name == 'tab_focus':
        return f"tab_focus({state['index']})"

    elif name == 'upload_file':
        files = state['file']
        if isinstance(files, list):
            files = [f"'{file}'" for file in files]
            files = f"[{', '.join(files)}]"
        else:
            files = f"'{files}'"
        return f"upload_file('{state['id']}', {files})"

    elif name == 'mouse_upload_file':
        files = state['file']
        if isinstance(files, list):
            files = [f"'{file}'" for file in files]
            files = f"[{', '.join(files)}]"
        else:
            files = f"'{files}'"
        return f"mouse_upload_file({state['x']}, {state['y']}, {files})"

    else:
        return f"# Unsupported action: {name}"
