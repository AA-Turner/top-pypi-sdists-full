import ast

def ast_parse(file_path):
    # Check file_path end with .py
    if not file_path.endswith('.py'):
        return "Not a Python file"
    # Read the contents of the file
    with open(file_path, 'r') as file:
        file_contents = file.read()

    # Parse the file contents into an AST
    parsed_ast = ast.parse(file_contents)

    # Prepare a string to collect function information
    function_info = ""

    # Loop through the AST nodes and collect function definitions
    for node in ast.walk(parsed_ast):
        if isinstance(node, ast.FunctionDef):
            function_info += f"Function name: {node.name}\n"
            function_info += f"Arguments: {[arg.arg for arg in node.args.args]}\n"
            function_info += f"Line number: {node.lineno}\n"
            function_info += "-" * 20 + "\n"
    
    return function_info

def ast_parse_from_content(file_contents):
    try:
        # Parse the file contents into an AST
        parsed_ast = ast.parse(file_contents)

        # Prepare a string to collect function information
        function_info = ""

        # Loop through the AST nodes and collect function definitions
        for node in ast.walk(parsed_ast):
            if isinstance(node, ast.FunctionDef):
                function_info += f"Function name: {node.name}\n"
                function_info += f"Arguments: {[arg.arg for arg in node.args.args]}\n"
                function_info += f"Line number: {node.lineno}\n"
                function_info += "-" * 20 + "\n"
        
        return function_info
    except Exception as e:
        return ""