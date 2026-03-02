class WindowGlobalBridge:
    """
    A class to manage the global variables shared between different scripts.

    Attributes:
        global_vars (dict): A dictionary to store global variables for each script.

    Methods:
        __init__(self):
            Initializes the WindowGlobalBridge with an empty dictionary for global_vars.

        retrieve_global_variables(self, script_name, global_variables, tag_script_name=False):
            Stores the global variables of a script in the global_vars dictionary.

        return_global_variables(self, script_name=None):
            Returns the global variables of a script.

        change_globals(self, variable, value, script_name=None):
            Modifies a global variable value for a specified script.

        search_globals_values(self, value, script_name=None):
            Searches for a specific value in the global variables of a script.

        return_global_value(self, variable, script_name=None):
            Returns the value of a specific global variable in a script.
    """
    def __init__(self):
        """
        Initializes the WindowGlobalBridge with an empty dictionary for global_vars.
        """
        self.global_vars = {}
    def create_script_name(self,script_name:str='default_script_name'):
        if script_name in self.global_vars:
            script_name = script_name+'_0'
        while script_name in self.global_vars:
            script_number = int(script_name.split('_')[-1])
            scrript_name = script_name[:-len(str(script_number))]+str(script_number+1)
        return script_name
    def retrieve_global_variables(self, script_name:str, global_variables:dict, tag_script_name:bool=False):
        """
        Stores the global variables of a script in the global_vars dictionary.

        Args:
            script_name (str): The name of the script.
            global_variables (dict): The global variables to store for the script.
            tag_script_name (bool, optional): If True, the script_name will be stored in the global_variables dictionary.
                                              Defaults to False.
        """
        self.global_vars[script_name] = global_variables
        if tag_script_name:
            self.global_vars[script_name]["script_name"] = script_name

    def return_global_variables(self, script_name=None):
        """
        Returns the global variables of a script.

        Args:
            script_name (str, optional): The name of the script. If None, all global variables will be returned.

        Returns:
            dict: The global variables of the script. If no global variables are found, it returns an empty dictionary.
        """
        if script_name is not None:
            return self.global_vars.get(script_name, {})
        else:
            return self.global_vars

    def change_globals(self, variable:str, value:any, script_name:str=None):
        """
        Modifies a global variable value for a specified script.

        Args:
            variable (str): The name of the global variable to modify.
            value (any): The new value to assign to the global variable.
            script_name (str, optional): The name of the script. If None, the global variable in the base context will be modified.
        """
        if script_name is not None:
            self.global_vars[script_name][variable] = value
            return value
    def search_globals_values(self, value:any, script_name:str=None):
        """
        Searches for a specific value in the global variables of a script.

        Args:
            value (any): The value to search for in the global variables.
            script_name (str, optional): The name of the script. If None, the search will be performed in the base context.

        Returns:
            str or False: The name of the first global variable containing the given value, or False if not found.
        """
        if script_name is not None:
            for each in self.global_vars[script_name].keys():
                if self.global_vars[script_name][each] == value:
                    return each
        return False

    def return_global_value(self, variable:str, script_name:str=None):
        """
        Returns the value of a specific global variable in a script.

        Args:
            variable (str): The name of the global variable to retrieve.
            script_name (str, optional): The name of the script. If None, the global variable in the base context will be retrieved.

        Returns:
            any: The value of the specified global variable.
        """
        if script_name is not None and variable in self.global_vars[script_name]:
            return self.global_vars[script_name][variable]
