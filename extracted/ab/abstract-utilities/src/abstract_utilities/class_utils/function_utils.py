from .imports import *
def get_proper_args(function,args:(dict or list)={}):
    """Call a function with either positional or keyword arguments based on the provided args type."""
    return function(*args) if isinstance(args, list) else function(**args)
def process_args(args):
    """
    Processes the arguments for a function, replacing nested function calls with their results.

    Args:
        args (dict): A dictionary of arguments. 

    Returns:
        dict: A dictionary of processed arguments.
    """
    for key, value in args.items():
        # check if value is a dict and has a 'type' key with value 'get'
        if isinstance(value, dict) and value.get('type') == 'get':
            function_name = value.get('name',None)
            function_args = value.get('args', {})
            instance = value.get('instance',None)
            glob = value.get('global',globals())
            # call the function and replace the arg with its result
            args[key] = call_functions(function_name, function_args, instance, glob)
    return args
def get_fun(js):
    """
    Retrieves and calls a function with the given parameters.

    Args:
        js (dict): A dictionary that contains function details, including name, arguments, instance (optional), and global scope (optional).

    Returns:
        any: The result of the function call.
    """
    # Get function details
    function_name = js.get('name',None)
    if function_name is None:
        return None
    function_args = js.get('args', {})
    instance = js.get('instance',None)
    glob = js.get('global',globals())
    # Process arguments
    function_args = process_args(function_args)
    # If instance is not None, get the function from the instance, else get from globals
    if instance is not None:
        function = getattr(instance, function_name)
    else:
        function = glob[function_name]
    # Get function's valid parameter keys
    sig = inspect.signature(function)
    valid_keys = sig.parameters.keys()
    # Filter arguments to only those accepted by the function
    filtered_args = {k: v for k, v in function_args.items() if k in valid_keys}
    return call_functions(function_name, filtered_args, instance, glob)
def call_functions(function_name: str, args: dict = {}, instance=None, glob:(dict or bool)=globals()):
    """
    Calls a function or a method with the given arguments.

    Args:
        function_name (str): The name of the function.
        args (dict, optional): A dictionary of arguments to pass to the function. Defaults to None.
        instance (optional): The instance on which to call the method. Defaults to None.
        glob (optional): The global scope from which to retrieve the function. Defaults to globals().

    Returns:
        any: The result of the function or method call.
    """
    glob = if_none_change(glob,globals())
    args = if_none_change(args,{})
    if instance is not None:
        # Calls method on instance
        method = getattr(instance, function_name)
        return get_proper_args(method,args)
    else:
        # Calls function from globals
        return get_proper_args(glob[function_name],args)
def get_all_functions_for_instance(instance):
    """
    Retrieves all callable methods/functions of an object instance.

    Args:
        instance: The object instance for which to retrieve methods/functions.

    Returns:
        list: A list of method/function names that are callable on the given instance.
    """
    return [method for method in dir(instance) if callable(getattr(instance, method))]
def get_all_params(instance, function_name):
    """
    Retrieves information about the parameters of a callable method/function of an instance.

    Args:
        instance: The object instance containing the method.
        function_name (str): The name of the method/function to inspect.

    Returns:
        dict: A dictionary containing parameter information, including names, defaults, kinds, and required parameters.
    """
    # Use getattr() to get the method by name
    method = getattr(instance, function_name, None)
    
    if callable(method):
        # Now you have the method, and you can inspect it
        func_signature = inspect.signature(method)
        parameters = func_signature.parameters
        
        params = {"names": [], "defaults": [], "kinds": [], "required": []}
        
        for param_name, param in parameters.items():
            params["names"].append(param_name)
            params["defaults"].append(param.default)
            params["kinds"].append(param.kind)
            
            if param.default == inspect._empty:
                params["required"].append(param_name)
        
        return params
    else:
        print(f"{function_name} is not a callable method of the instance.")
        return None 
def mk_fun(module,function):
    """
    Checks if a function exists in a given module.

    Args:
        module: The module in which to look for the function.
        function: The function to check.

    Prints a statement indicating whether the function exists.
    """
    if has_attribute(module,function):
      print(f"The function {function} exists.")
    else:
      print(f"The function {function} does not exist.")
def alias(*aliases):
    """
    Decorator to create multiple names for a function.
    
    Args:
        *aliases: Names to assign to the function.
    
    Returns:
        callable: Decorated function.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        # Assign aliases in the module's globals
        for name in aliases:
            globals()[name] = func
        return wrapper
    return decorator
