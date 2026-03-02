from abstract_gui import make_component,ensure_nested_list,get_screen_dimensions
from .RightClickManager import RightClickManager
from abstract_utilities import create_new_name,make_list,ThreadManager
class GUIManager:
    """
    METHODS:

    1) __init__() - Initializes the AbstractWindowManager. No inputs. Sets up lists for global windows and closed windows, and an GUIManager object.

    2) long_running_operation() - This function simulates a long running operation. The input is a function and its arguments. The function is called with its arguments. The result is returned.

    3) start_long_operation_thread() - This function starts a long running operation in a thread. It takes a window name as input, adds a thread to the thread manager, links the thread to the event threads dictionary and finally starts the thread. The thread name is returned.

    4) run() - This function reads the window and handles events. It takes as input the window name, window, list of event handlers and close events. It loops until the corresponding event thread ends, handling events using the provided event handlers.
    """
    def __init__(self,window_mgr):
        """
	Initializes the AbstractWindowManager. No inputs. Sets up lists for global windows and closed windows, and an GUIManager object.
 	"""
        self.window_mgr=window_mgr
        self.thread_manager = ThreadManager()
        self.event_threads={}
        
    def long_running_operation(self,function=None,args={}):
        """
	This function simulates a long running operation. The input is a function and its arguments. The function is called with its arguments. The result is returned.
 	"""
        # Simulate a long-running operation
        if function:
            results = function(**args)
            # Here you would have some mechanism to send data back to the GUI
        return results
    
    def start_long_operation_thread(self,window_name):
        """
	This function starts a long running operation in a thread. It takes a window name as input, adds a thread to the thread manager, links the thread to the event threads dictionary and finally starts the thread. The thread name is returned.
 	"""
        name = self.thread_manager.add_thread(name=window_name,target_function=self.long_running_operation,function_args={"window_name":window_name}, daemon=True)
        self.event_threads[name]=False
        self.thread_manager.start(name)
        return name
    def run(self,window_name,window,event_handlers=[],close_events=[]):
        """
	This function reads the window and handles events. It takes as input the window name, window, list of event handlers and close events. It loops until the corresponding event thread ends, handling events using the provided event handlers.
 	"""
        self.event_threads[window_name] = True
        event_handlers =make_list(event_handlers)
        while self.event_threads[window_name]:
            event, values = self.window_mgr.read_window(window_name=window_name)  # Non-blocking read with a timeout
            if event == None or event in close_events or self.window_mgr.exists(window_name=window_name)==False:
                self.event_threads[window_name] = False
            # ... handle other events ...
            for event_handler in event_handlers:
                event_handler(event,values,window)
        # Cleanup
        if self.event_threads[window_name]:
            self.event_threads[window_name].join()

class AbstractWindowManager:
    """

    1) get_screen_size() - This function gets the screen size. No input arguments. Returns the screen size gotten from the sg.Window class.

    2) set_window_size() - This function sets the window size. Inputs are the maximum size, height and width. It first gets the screen size, checks the dimensions are valid, calculates the new dimensions and checks they're within the maximum size. The new size is returned.

    3) add_window() - This function adds a window. Takes as input the window title, layout, name, default name, close events, event handlers, match true bool, sizes and any other arguments. It calculates the window name, adds the window to the global windows list and returns the window name.

    4) while_window() - This function handles a window's events until the window is closed. Takes the window name and window as input, and optional close events and event handlers. It gets the window's info from global windows and runs the GUI manager's run method.

    5) exists() - This function checks if a window exists. Takes the window name and window as input. Returns True if window does exist, False otherwise.

    6) close_window() - This function closes a window. Takes the window name and window as input. It finds the window, closes it and removes it from the global windows list, adding it to the closed windows list.

    7) get_window() - This function returns a window. Takes the window name and window as input. Returns the window's method attribute from the global windows list.

    8) append_output() - This function appended new content to a window's value. Takes keys of new content, window name and window as input. It gets the window enumeration, gets the current content from window's value, concatenates the new content and updates the window's value with the new content.

    9) update_value() - This function updates a window's value. Takes as input the key, new value, any other arguments, window name and window. It gets the window enumeration, gets the window's current values, checks if key is in the values, and updates the window's key value with the new value.

    10) set_current_window() - This function sets a window as the current window. Takes the window as input. It gets the window enumeration, sets all windows' current attribute to false, and sets the input window's current attribute to true.

    11) get_current_window() - This function gets the current window. No inputs. It iterates through global windows and returns the enumeration of the window with current attribute equal to true.

    12) check_window_value() - This function checks if a value is in a window's values. Takes as input the key and value. Returns the enumeration of the window if found, None otherwise.

    13) get_window_info_list() - This function gets a list of a specific window information. Takes the key of the information as input. Returns a list of all the information from all windows.

    14) enumerate_list() - This function returns the enumeration of an object in a list. The list, key and value are inputs. If value is found in the list, that number is returned.

    15) get_any_enumeration() - This function gets the enumeration of a window based on its window name or method, or if current window is true. If any of these exist, calls check_window_value to get the window enumeration and returns it.

    16) get_window_method() - This function gets a window's method. Takes the window name, window, and current window as input. Gets the window enumeration and returns the method from the global windows.

    17) update_read_values() - This function reads a window's values and updates the values in the global windows list. Inputs are the enumeration of the window and a timeout. If event is None, it closes the window. Updated event and values are returned.

    18) read_window() - This function reads a window's values. Inputs are the window name, window and timeout. It gets the window enumeration, and if found, updates and returns the read values. If no enumeration is found, prints an error message and returns None.

    19) get_window_info() - This function gets a specific window's information. Inputs are the key of the info and the window name and window. It gets the window enumeration, and if found, returns the window's info.

    20) get_event() - This function gets a window's event. Inputs are window name and window. It calls get_window_info with event as the key and returns the result.

    21) get_values() - This function gets a window's values. Inputs are window name and window. It calls get_window_info with values as the key and returns the result.

    22) get_from_value() - This function gets a value from a window's values. Inputs are the key of the value, default value if key not found, delimiter to filter value, window name and window. It get's the window's values and returns the raw value or default value if the value equals delim.

    23) expand_elements() - This function expands certain elements in a window. Inputs are window name, window object, and a list of element keys to expand. It gets the window using its name or direct object, sets a default list of keys to expand if not provided, and loops through the keys to expand each one.
    """
    def __init__(self):
        self.global_windows = []
        self.closed_windows = []
        self.undesignated_value_keys = []
        self.right_click_mgr=RightClickManager()
        self.gui_mgr = GUIManager(self)

    @staticmethod
    def set_window_size(max_size=None, height=1, width=1):
        """
	This function sets the window size. Inputs are the maximum size, height and width. It first gets the screen size, checks the dimensions are valid, calculates the new dimensions and checks they're within the maximum size. The new size is returned.
 	"""
        screen_width, screen_height = get_screen_dimensions(height=height,width=width)
        
        # If max_size is specified and valid, use it. Otherwise, default to screen dimensions.
        if max_size and isinstance(max_size, tuple) and len(max_size) == 2 and \
           isinstance(max_size[0], int) and isinstance(max_size[1], int):
            max_width, max_height = max_size
        else:
            max_width, max_height = screen_width, screen_height

        # Constrain to max dimensions
        max_width = min(max_width, screen_width)
        max_height = min(max_height, screen_height)

        # Return the new size
        return max_width, max_height
    
    def add_window(self,title=None,layout=None, window_name=None,  default_name=True,set_current=True,window_height=1,window_width=1,close_events=[], event_handlers=[],
                   match_true=False,set_size=None, *args, **kwargs):
        title = title or window_name
        window_name = window_name or title
        window_name = create_new_name(name=window_name, names_list=self.get_window_info_list(key="name"), 
                                      default=default_name, match_true=match_true)
        

        current = False
        if len(self.global_windows) == 0 or set_current:
            current = True
        sizes={}
        if set_size:
            sizes=self.set_window_size(max_size=None,height=window_height,width=window_width)
        if layout:
           layout=ensure_nested_list(layout)
        
        else:
            kwargs_layout=kwargs.get("layout")
            if kwargs_layout:
                layout=ensure_nested_list(kwargs_layout)
                del kwargs["layout"]
            elif len(args)>0:
                num = 1
                if kwargs.get("title"):
                    num-=1
                layout=ensure_nested_list(args[num])
                del args[num]
        self.global_windows.append({"name":window_name,
                                    "method":make_component('Window', title=title,layout=layout,*args, **kwargs),
                                    "event":False,
                                    "values":False,
                                    "current":current,
                                    **sizes,
                                    "close_events":close_events,
                                    "event_handlers":event_handlers})
        return window_name
    def while_window(self,window_name=None,window=None,close_events=[],event_handlers=[]):
        """
	This function handles a window's events until the window is closed. Takes the window name and window as input, and optional close events and event handlers. It gets the window's info from global windows and runs the GUI manager's run method.
 	"""
        window_enumeration = self.get_any_enumeration(window_name=window_name,window=window)
        if window_enumeration !=None:
            window_info =self.global_windows[window_enumeration]
            window_name = window_info["name"]
            window = window_info["method"]
            event_handlers = make_list(window_info["event_handlers"]) or make_list(event_handlers)
            event_handlers.append(self.right_click_mgr.right_click_event)
            close_events = window_info["close_events"] or close_events
            self.gui_mgr.run(window_name=window_name,window=window,event_handlers=event_handlers,close_events=close_events)
    def exists(self,window_name=None,window=None):
        """
	This function checks if a window exists. Takes the window name and window as input. Returns True if window does exist, False otherwise.
 	"""
        window_enumeration = self.get_any_enumeration(window_name=window_name,window=window)
        if window_enumeration != None:
            return True
        return False
    def close_window(self, window_name=None,window=None):
        """
	This function closes a window. Takes the window name and window as input. It finds the window, closes it and removes it from the global windows list, adding it to the closed windows list.
 	"""
        window_enumeration = self.get_any_enumeration(window_name=window_name,window=window)
        if window_enumeration !=None:
            self.global_windows[window_enumeration]["method"].close()  # Assuming your window object has a close method
            new_global_windows = []
            for i,window_values in enumerate(self.global_windows):
                if i == window_enumeration:
                    self.closed_windows.append(window_values)
                else:
                    new_global_windows.append(window_values)
            self.global_windows=new_global_windows
    def get_window(self,window_name=None,window=None):
        """
	This function returns a window. Takes the window name and window as input. Returns the window's method attribute from the global windows list.
 	"""
        window_enumeration = self.get_any_enumeration(window_name=window_name,window=window)
        return self.global_windows[window_enumeration]["method"]
    def append_output(self,key,new_content,window_name=None,window=None):
        """
	This function appended new content to a window's value. Takes keys of new content, window name and window as input. It gets the window enumeration, gets the current content from window's value, concatenates the new content and updates the window's value with the new content.
 	"""
        window_enumeration = self.get_any_enumeration(window_name=window,window=window)
        if window_enumeration != None:
            content = self.get_from_value(key=key,window_name=window_name,window=window)+'\n\n'+new_content
            self.update_value(key=key,value=content,window_name=window_name,window=window)
    def update_value(self, key, value=None, args=None,window_name=None,window=None,):
        """
	This function updates a window's value. Takes as input the key, new value, any other arguments, window name and window. It gets the window enumeration, gets the window's current values, checks if key is in the values, and updates the window's key value with the new value.
 	"""
        window_enumeration = self.get_any_enumeration(window_name=window,window=window)
        if window_enumeration != None:
            window = self.global_windows[window_enumeration]['method']
            values = self.get_values(window_name=window,window=window)
            if key in values:
                if args:
                    window[key].update(**args)
                else:
                    window[key].update(value=value)
### current_window
    def set_current_window(self, window):
        """
	This function sets a window as the current window. Takes the window as input. It gets the window enumeration, sets all windows' current attribute to false, and sets the input window's current attribute to true.
 	"""
        window_enumeration = self.get_any_enumeration(window_name=window,window=window,current_window=True)
        for i,window_info in enumerate(self.global_windows):
            bool_it=False
            if i == window_enumeration:
                bool_it =True
            self.global_windows[i]["current"] = bool_it
    def get_current_window(self):
        """
	This function gets the current window. No inputs. It iterates through global windows and returns the enumeration of the window with current attribute equal to true.
 	"""
        for i,window_info in enumerate(self.global_windows):
            if self.global_windows[i]["current"]==True:
                return i
### enumerate value in global window list
    def check_window_value(self,key,value):
        """
	This function checks if a value is in a window's values. Takes as input the key and value. Returns the enumeration of the window if found, None otherwise.
 	"""
        i=self.enumerate_list(list_obj=self.global_windows,key=key,value=value)
        if i != None:
            return i
    def get_window_info_list(self,key=None):
        """
	This function gets a list of a specific window information. Takes the key of the information as input. Returns a list of all the information from all windows.
 	"""
        info_list=[]
        for window_info in self.global_windows:
            info_list.append(window_info[key])
        return info_list
    def enumerate_list(self,list_obj,key,value):
        """
	This function returns the enumeration of an object in a list. The list, key and value are inputs. If value is found in the list, that number is returned.
 	"""
        for i,values in enumerate(list_obj):
            if values[key] == value:
                return i
    def get_any_enumeration(self,window_name=None,window=None,current_window=True):
        """
	This function gets the enumeration of a window based on its window name or method, or if current window is true. If any of these exist, calls check_window_value to get the window enumeration and returns it.
 	"""
        json_check = {"name":window_name,"method":window}
        if current_window:
            json_check["current"]=True
 
        for key,value in json_check.items():
            if value != None:
                window_enumeration = self.check_window_value(key,value)
                if window_enumeration != None:
                    return window_enumeration
### get window method
    def get_window_method(self,window_name=None,current_window=False):
        """
	This function gets a window's method. Takes the window name, window, and current window as input. Gets the window enumeration and returns the method from the global windows.
 	"""
        window_enumeration = self.get_any_enumeration(window_name=window_name,window=window_name,current_window=current_window)
        if window_enumeration !=None:
            return self.global_windows[window_enumeration]["method"]
### window read
    def update_read_values(self,enumeration,timeout=0):
        """
	This function reads a window's values and updates the values in the global windows list. Inputs are the enumeration of the window and a timeout. If event is None, it closes the window. Updated event and values are returned.
 	"""
        window_method = self.global_windows[enumeration]["method"]
        event,values = window_method.read()
        json_check = {"event":event,"values":values}
        for key,value in json_check.items():
            self.global_windows[enumeration][key]=value
        if event == None:
            self.close_window(window=window_method)
        return event,values
    def read_window(self,window_name=None,window=None,timeout=0):
        """
	This function reads a window's values. Inputs are the window name, window and timeout. It gets the window enumeration, and if found, updates and returns the read values. If no enumeration is found, prints an error message and returns None.
 	"""
        window_enumeration = self.get_any_enumeration(window_name=window_name,window=window)
        if window_enumeration != None:
           return self.update_read_values(window_enumeration,timeout=timeout)
        else:
            print("No current window set!")
            return None, None
        
### window event and values
    def get_window_info(self,key,window_name=None,window=None):
        """
	This function gets a specific window's information. Inputs are the key of the info and the window name and window. It gets the window enumeration, and if found, returns the window's info.
 	"""
        window_enumeration = self.get_any_enumeration(window_name=window,window=window)
        if window_enumeration != None:
            values = self.global_windows[window_enumeration][key]
            if not values:
                values = self.read_window(window=self.global_windows[window_enumeration]["method"])
                if not values:
                    self.close_window(window_name=self.global_windows[window_enumeration]['method'])
            return self.global_windows[window_enumeration][key]
    def get_event(self,window_name=None,window=None):
        """
	This function gets a window's event. Inputs are window name and window. It calls get_window_info with event as the key and returns the result.
 	"""
        return self.get_window_info("event",window_name=window_name,window=window)
    def get_values(self,window_name=None,window=None):
        """
	This function gets a window's values. Inputs are window name and window. It calls get_window_info with values as the key and returns the result.
 	"""
        return self.get_window_info("values",window_name=window_name,window=window)

    
    def get_from_value(self,key,default=None,delim=None,window_name=None,window=None):
        """
	This function gets a value from a window's values. Inputs are the key of the value, default value if key not found, delimiter to filter value, window name and window. It get's the window's values and returns the raw value or default value if the value equals delim.
 	"""
        values = self.get_values(window_name=window_name,window=window)
        if values:
            if key not in values:
                print(f'{key} has no value')
                if key not in self.undesignated_value_keys:
                    self.undesignated_value_keys.append(key)
                    print('undesignated_value_keys: \n',self.undesignated_value_keys)
                return
            value = values[key]
            if delim != None:
                if value == delim:
                    return default
            return value
    def expand_elements(self, window_name=None, window=None, element_keys=None):
        """
        Expand the specified elements in the window.

        Args:
        - window_name (str, optional): The name of the window.
        - window (object, optional): Direct window object.
        - element_keys (list, optional): List of keys of the elements to be expanded.
        """
        # Get the window using its name or direct object
        target_window = self.get_window(window_name=window_name, window=window)
            
        # If no element_keys are provided, use the default set of keys
        default_keys = ['-TABGROUP-', '-ML CODE-', '-ML DETAILS-', '-ML MARKDOWN-', '-PANE-']
        element_keys = element_keys or default_keys
        
        # Expand the elements
        for key in element_keys:
            if key in target_window:
                target_window[key].expand(True, True, True)
                

