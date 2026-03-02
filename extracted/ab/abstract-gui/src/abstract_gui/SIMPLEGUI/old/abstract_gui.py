from .SimpleGuiFunctionsManager import SimpleGuiFunctionsManager,SimpleGuiFunctionsManagerSingleton,sg,ensure_nested_list,make_component,get_gui_fun
from abstract_utilities.path_utils import get_current_path
from abstract_utilities.list_utils import make_list_add
from abstract_utilities import eatAll
"""
These functions are designed to simplify and streamline the process of creating and managing PySimpleGUI windows and their layouts. The utility functions allow for more concise code when setting up GUIs.
1. **ensure_nested_list(obj)**
   - This function checks if the passed `obj` is a list. If it's not, it wraps the `obj` in a list. If the `obj` is a list but contains at least one non-list element, it wraps the entire list in another list. 

2. **create_row(*args)**
   - Creates and returns a list out of the passed arguments.

3. **create_column(*args)**
   - Creates and returns a column (list of lists) from the passed arguments. If an argument is a list, it's expanded into individual rows.

4. **concatenate_rows(*args)**
   - Concatenates multiple lists into one.

5. **concatenate_layouts(*args)**
   - Essentially appends all arguments into one list.

6. **create_row_of_buttons(*args)**
   - Creates a row of button elements from the passed arguments.

7. **get_buttons(*args)**
   - This function is designed to return a list of button components. It accepts different argument types and interprets them differently to produce the required buttons.

8. **make_list_add(obj, values)**
   - Takes an object and values, converts both to lists (if they aren't already), and appends the values to the object.

9. **if_not_window_make_window(window)**
   - Ensures the given `window` is of the proper type, potentially creating a new window if not.

10. **while_quick(window, return_events, exit_events, event_return)**
    - A utility function to simplify the window event loop. Reads events from the given window until certain conditions are met.

11. **verify_args(args, layout, title, event_function, exit_events)**
    - Ensures default values for various window arguments.

12. **get_window(title, layout, args)**
    - Retrieves a PySimpleGUI window with specified or default properties.

13. **get_browser_layout(title, type, args, initial_folder)**
    - Prepares a layout for a file or folder browser window.

14. **get_yes_no_layout(title, text, args)**
    - Prepares a layout for a Yes/No window.

15. **get_input_layout(title, text, default, args)**
    - Prepares a layout for an input window.

16. **get_yes_no(title, text, args, exit_events, return_events, event_return)**
    - Displays a Yes/No window and returns the result.

17. **get_input(title, text, default, args, exit_events, return_events)**
    - Displays an input window and returns the result.

18. **get_browser(title, type, args, initial_folder, exit_events, return_events)**
    - Displays a browser window and returns the result.
    
19. **get_gui_fun(name, args)**
    - Retrieves a PySimpleGUI function by its name and prepares it with the given arguments.

20. **expandable(size, resizable, scrollable, auto_size_text, expand_x, expand_y)**
    - Returns a dictionary of parameters suitable for creating an expandable PySimpleGUI window.

21. **create_window_manager(script_name, global_var)**
    - Creates and returns a window manager for managing PySimpleGUI windows.

These functions are designed to simplify and streamline the process of creating and managing PySimpleGUI windows and their layouts. The utility functions allow for more concise code when setting up GUIs.
"""

#nested list management
def create_row(*args):
    """
    Create a row layout containing the provided arguments.

    Args:
        *args: Elements to be placed in the row layout.

    Returns:
        list: A row layout containing the provided elements.
    """
    return [arg for arg in args]

def create_column(*args):
    """
    Create a column layout containing the provided arguments.

    Args:
        *args: Elements to be placed in the column layout.

    Returns:
        list: A column layout containing the provided elements.
    """
    elements = []
    for arg in args:
        if isinstance(arg, list):  # If the argument is a list, expand it
            elements.extend(arg)
        else:
            elements.append(arg)
    return [[element] for element in elements]

def concatenate_rows(*args):
    """
    Concatenate multiple row layouts into a single row layout.

    Args:
        *args: Row layouts to be concatenated.

    Returns:
        list: A row layout containing concatenated elements from input row layouts.
    """
    result = []
    for arg in args:
        result += arg
    return result

def concatenate_layouts(*args):
    """
    Concatenate multiple layouts into a single layout.

    Args:
        *args: Layouts to be concatenated.

    Returns:
        list: A layout containing concatenated elements from input layouts.
    """
    return concatenate_rows(args)

def create_row_of_buttons(*args):
    """
    Create a row layout containing buttons generated from the provided arguments.

    Args:
        *args: Arguments for creating buttons.

    Returns:
        list: A row layout containing buttons created from the provided arguments.
    """
    return [button for arg in args for button in get_buttons(arg)]

def get_buttons(*args):
    """
    Generate button elements based on the provided arguments.

    Args:
        *args: Arguments specifying button elements.

    Returns:
        list: Button elements generated from the provided arguments.
    """
    if isinstance(args, tuple):
        args = [list(args)]
    # If no args or more than one arg, raise an exception
    if len(args) != 1:
        raise ValueError("The function expects a single argument which can be a str, dict, list, or tuple.")
    arg = args[0]
    arg_type = type(arg)

    # If it's a dictionary, use it as arguments for a single button
    if isinstance(arg, dict):
        return get_gui_fun("Button", args=arg)
    
    # If it's a string, use it as the text for a single button
    elif isinstance(arg, str):
        return get_gui_fun("Button", args={"button_text": arg})

    # If it's a list or tuple, iterate through its items
    elif isinstance(arg, (list, tuple)):
        buttons = []
        for each in arg:
            if isinstance(each, list):
               each = tuple(each)
            # For each string item, use it as the text for a button
            if isinstance(each, str):
                component = get_gui_fun("Button", args={"button_text": each})
      
            # If it's a tuple, consider first element as text and second as dictionary
            elif isinstance(each, tuple) and len(each) == 2 and isinstance(each[0], str) and isinstance(each[1], dict):
                btn_text = each[0]
                btn_args = each[1]
                btn_args["button_text"] = btn_text  # Add button_text to the arguments
                component = get_gui_fun("Button", args=btn_args)

            # For each dict item, use it as arguments for a button
            elif isinstance(each, dict):
                component = get_gui_fun("Button", args=each)

            else:
                raise ValueError("Unsupported item type in the list/tuple: {}".format(type(each)))
            buttons.append(component)
        return buttons
    else:
        raise ValueError("Unsupported argument type: {}".format(arg_type))

#window management
def if_not_window_make_window(window):
    """
    Checks if the provided object is a window and creates a new window if it isn't.
    
    Args:
        window: The object to be checked. If not a window, it's expected to be a dictionary with layout information.
        
    Returns:
        window: The valid window object.
    """
    if isinstance(window, type(get_window())) == False:
        if isinstance(window, dict):
            if "layout" in window:
                window["layout"]=ensure_nested_list(window["layout"])
        window=get_window(args=window)
    return window
      
def create_window_manager(script_name='default_script_name',global_var=globals()):
    """
    Initializes a window manager for a given script.
    
    Args:
        script_name (str, optional): The name of the script.
        global_var (dict, optional): The global variables associated with the script.
        
    Returns:
        tuple: A tuple containing the WindowManager, bridge, and script name.
    """
    bridge = WindowGlobalBridge()
    script_name = bridge.create_script_name(script_name)
    global_var[script_name] = script_name
    js_bridge = bridge.retrieve_global_variables(script_name, global_var)
    return WindowManager(script_name, bridge),bridge,script_name

#event management
def while_quick(window,return_events:(list or str)=[],exit_events:(list or str)=[sg.WIN_CLOSED],event_return=False):
    """
    Reads events from the given window and handles them based on the provided conditions.
    
    Args:
        window: The window to read events from.
        return_events (list or str): Events that would lead to the window being closed and a value returned.
        exit_events (list or str): Events that would lead to the window being closed without returning a value.
        event_return (bool): If True, returns the event. If False, returns the values.
        
    Returns:
        event or values: Depending on the event_return flag.
    """
    exit_events = make_list_add(exit_events,[sg.WIN_CLOSED])
    return_events = list(return_events)
    last_values=[]
    while True:
        event, values = window.read()
        if event ==sg.WIN_CLOSED:
            window.close()
            values= None
            break
        elif event in return_events:
            window.close()
            break
    if event_return == True:
        return event
    return values  

def Choose_RPC_Parameters_GUI(RPC_list:list=None) -> dict or None:
    """
    Creates and launches the GUI window for selecting RPC parameters.
    
    Parameters:
    - RPC_list (list, optional): The list of RPC parameters. If not provided, it will fetch the default list.
    
    Returns:
    - dict: A dictionary containing the selected RPC parameters.
    """
    if RPC_list == None:
        RPC_list = get_rpc_list()
    elif os.path.isfile(RPC_list):
        RPC_list = get_rpc_list(file_path)
    rpc_add_global_bridge["get_rpc_list"]=[]
    for each in RPC_list:
        rpc_add_global_bridge["get_rpc_list"].append(RPCData(each).return_rpc_js())
    save_rpc_list(json_data = rpc_add_global_bridge["get_rpc_list"])
    rpc_add_global_bridge["total_bool_list"] = []
    rpc_add_global_bridge["recursed_rpc_js_list"]=rpc_add_global_bridge["get_rpc_list"] 
    rpc_add_global_bridge["check_list"]={}
    for each in list(get_js().values()):
        rpc_add_global_bridge["check_list"][each] = ''
    keyed_rpc_lists()
    rpc_add_global_bridge["Network_Names"]=rpc_add_global_bridge["keyed_lists"]["Network_Name"]
    layout = []
    for key,value in get_js().items():
        layout.append([
            get_gui_fun("Text",args={"text":key.replace('_',' ')}),
            get_gui_fun("Combo",args={"values":rpc_add_global_bridge["keyed_lists"][key],"default_text":rpc_add_global_bridge["keyed_lists"][key][0],"key":f"{value}","enable_events":True}),
            get_gui_fun("Checkbox",args={"text":"","default":(key=="Network_Name"),"key":f"{value[:-1]}_CHECK-","enable_events":True}),
            get_push()])
    layout = [[get_menu()],layout,[create_row_of_buttons("OK","Show","reset","Exit"),]]
    window = window_mgr.get_new_window(args={"title":'ADD RPC',"layout":layout,"exit_events":["OK","Exit"],"event_function":"win_while","suppress_raise_key_errors":False, "suppress_error_popups":False, "suppress_key_guessing":False,"finalize":True})
    values = window_mgr.while_basic(window=window)

#premade components
def verify_args(args:dict=None, layout:list=None, title:str=None, event_function:str=None,exit_events:(list or str)=None):
    """
    Verifies and/or sets default values for window arguments.
    
    Args:
        args (dict, optional): Dictionary containing window arguments.
        layout (list, optional): The layout for the window.
        title (str, optional): The title of the window.
        event_function (str, optional): The function to be executed when an event occurs.
        exit_events (list or str, optional): List of events that would close the window.
        
    Returns:
        dict: The verified/updated window arguments.
    """
    args = args or {}
    layout = layout or [[]]
    title = title or 'window'
    exit_events = exit_events or ["exit", "Exit", "EXIT"]
    args.setdefault("title", title)
    args.setdefault("layout", ensure_nested_list(layout))
    args.setdefault("event_function", event_function)
    args.setdefault("exit_events", list(exit_events))
    return args
def get_window(title=None, layout=None, args=None):
    """
    Get a PySimpleGUI window.

    Args:
        win_name (str, optional): The name of the window. If not provided, a unique name is generated.
        layout (list, optional): The layout of the window. If not provided, an empty layout is used.
        args (dict, optional): Additional arguments for the window.

    Returns:
        any: A PySimpleGUI window.
    """
    args = verify_args(args=args, layout=layout, title=title)
    return get_gui_fun('Window', {**args})
def get_browser_layout(title:str=None,type:str='Folder',args:dict={},initial_folder:str=get_current_path()):
    """
    Function to get a browser GUI based on the type specified.

    Parameters:
    type (str): The type of GUI window to display. Defaults to 'Folder'.
    title (str): The title of the GUI window. Defaults to 'Directory'.

    Returns:
    dict: Returns the results of single_call function on the created GUI window.
    """
    if type.lower() not in 'folderdirectory':
        type = 'File'
    else:
        type = 'Folder'
    if title is None:
        title = f'Please choose a {type.lower()}'
    layout = [
        [get_gui_fun('Text', {"text": title})],
        [get_gui_fun('Input',args={"default":initial_folder,"key":"output"}), get_gui_fun(f'{type}Browse', {**args, "initial_folder": initial_folder})],
        [get_gui_fun('OK'), get_gui_fun('Cancel')]
    ]
    return {"title": f'{type} Explorer', "layout": layout}
def get_yes_no_layout(title:str="Answer Window",text:str="would you lie to proceed?",args:dict={}):
    """
    Creates a layout for a Yes/No window.
    
    Args:
        title (str, optional): The title of the window.
        text (str, optional): The prompt text.
        args (dict, optional): Additional arguments for the window.
        
    Returns:
        dict: The layout dictionary.
    """
    layout = [
        [get_gui_fun('Text', {"text": text})],
        [sg.Button('Yes'), sg.Button('No')]
    ]
    return {"title":title, "layout": layout,**args}
def get_input_layout(title:str="Input Window",text:str="please enter your input",default:str=None,args:dict={}):
    """
    Function to get a browser GUI based on the type specified.

    Parameters:
    type (str): The type of GUI window to display. Defaults to 'Folder'.
    title (str): The title of the GUI window. Defaults to 'Directory'.

    Returns:
    dict: Returns the results of single_call function on the created GUI window.
    """
    if type.lower() not in 'folderdirectory':
        type = 'File'
    else:
        type = 'Folder'
    if title is None:
        title = f'Please choose a {type.lower()}'
    if "default" not in args:
        args["default"]=default
    if "key" not in args:
        args["key"]=key
    if "text" in args:
        text = args["text"]
    layout = [
        [get_gui_fun('Text', {"text": text})],
        [get_gui_fun('Input',args=args)],
        [get_gui_fun('OK'), get_gui_fun('Cancel')]
    ]
    return {"title":title, "layout": layout}
def get_yes_no(title:str="Answer Window",text:str="would you lie to proceed?",args:dict={},exit_events:(str or list)=[],return_events:(str or list)=["Yes","No"],event_return=True):
    """
    Creates and displays a Yes/No window, then captures the user response.
    
    Args:
        title (str, optional): The title of the window.
        text (str, optional): The prompt text.
        args (dict, optional): Additional arguments for the window.
        exit_events (str or list, optional): List of events that would close the window.
        return_events (str or list, optional): List of events that would lead to a response being returned.
        event_return (bool, optional): If True, returns the event. If False, returns the values.
        
    Returns:
        event or values: Depending on the event_return flag.
    """
    window = get_window(args=get_yes_no_layout(title=title,text=text))
    return while_quick(window=window,exit_events=exit_events,return_events=return_events,event_return=event_return)
def get_input(title:str="Input Window",text:str="please enter your input",default:str=None,args:dict={},exit_events:(str or list)=['Cancel'],return_events:(str or list)=['OK']):
    """
    Creates and displays an input window, then captures the user input.
    
    Args:
        title (str, optional): The title of the window.
        text (str, optional): The prompt text.
        default (str, optional): The default input value.
        args (dict, optional): Additional arguments for the window.
        exit_events (str or list, optional): List of events that would close the window.
        return_events (str or list, optional): List of events that would lead to an input being returned.
        
    Returns:
        values: The captured user input.
    """
    window = get_window(args=get_input_layout(title=title,text=text,args=args,default=default,initial_folder=initial_folder))
    return while_quick(window=window,exit_events=exit_events,return_events=return_events)
    
def get_browser(title:str=None,type:str='Folder',args:dict={},initial_folder:str=get_current_path(),exit_events:(str or list)=['Cancel'],return_events:(str or list)=['OK']):
    """
    Creates and displays a browser window, then captures the user-selected path.
    
    Args:
        title (str, optional): The title of the window.
        type (str, optional): The type of browser (e.g., 'Folder').
        args (dict, optional): Additional arguments for the window.
        initial_folder (str, optional): The folder to start browsing from.
        exit_events (str or list, optional): List of events that would close the window.
        return_events (str or list, optional): List of events that would lead to a path being returned.
        
    Returns:
        results: The selected path or default path if none is selected.
    """
    window = get_window(args=get_browser_layout(title=title,type=type,args=args,initial_folder=initial_folder))
    results = while_quick(window=window,exit_events=exit_events,return_events=return_events)
    if isinstance(results, dict):
        if results['output']=='':
            results['output'] = initial_folder
    if results == None:
        results={'output':initial_folder}
    return results['output']

def get_menu(menu_definition:list=[['File',  'Save', 'Exit',],['Edit', ['Paste', ['Special', 'Normal',], 'Undo'],],['Help', 'About...'],],args:dict={}):
    args["menu_definition"]=ensure_nested_list(menu_definition)
    return get_gui_fun("Menu",args=args)

def get_push()-> make_component("Push"):
    """
    Fetches the "Push" function from the GUI module.
    
    Returns:
    - function: The "Push" GUI function.
    """
    return make_component("Push")

#key management
def text_to_key(text,section=None):
    text=eatAll(text,['-'])
    if section != None:
        text=f"{text} {section}"
    return f"-{text.upper().replace(' ','_')}-"

def get_event_key_js(event,key_list=None):
    script_event_js = {"event":event,'found':event,'section':''}
    if event:
        section,found=None,None
        if event in key_list:
            found=event
        else:
            section = eatAll(event,['-']).split('_')[-1]
        script_event_js = {"event":event,'found':found,'section':section}
        for script_event in key_list:
            conversion = text_to_key(script_event,section=section)
            script_event_js[script_event]=conversion
            if event == conversion:
                script_event_js['found']=script_event
    return script_event_js

#size parameters
def get_screen_size():
    """
    This function gets the screen size. No input arguments. Returns the screen size gotten from the sg.Window class.
    """
    return make_component("Window",title='screen_size',layout=[[]]).get_screen_size()

def get_screen_dimensions(height:int,width:int)->(int,int):
    screen_width, screen_height = get_screen_size()
    # Ensure we have valid screen dimensions
    if screen_width:
        screen_width=int(screen_width * width)
    if screen_height:
        screen_height=int(screen_height * height)
    if screen_width is None or screen_height is None:
        raise ValueError("Could not determine screen dimensions.")
    return screen_width, screen_height
def expandable(size: tuple = (None, None),
               resizable: bool = True,
               scroll_vertical: bool = False,
               scroll_horizontal: bool = False,
               auto_size_text: bool = True,
               expand_x: bool = True,
               expand_y: bool = True):
    """
    Returns a dictionary with window parameters for creating an expandable PySimpleGUI window.
    """
    return {
        "size": size,
        "resizable": resizable,
        "scrollable": scroll_vertical or scroll_horizontal,  # Must be True if either vertical or horizontal is True
        "vertical_scroll_only": scroll_vertical and not scroll_horizontal,  # True only if vertical is True and horizontal is False
        "auto_size_text": auto_size_text,
        "expand_x": expand_x,
        "expand_y": expand_y
    }
