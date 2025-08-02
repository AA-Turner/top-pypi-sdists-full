import argparse
import os
import yaml
from jinja2 import Template
import shutil
from jnjrender import __version__

def render_jinja_to_yaml(jinja_file, variables, template_name, yaml_file,output_file=None):
    

    # Check if jinja_file is a directory
    if os.path.isdir(jinja_file):
        if template_name and template_name !="":
            found_template = None
            # Search for the template in the directory and subdirectories
            for root, _, files in os.walk(jinja_file):
                if template_name in files:
                    found_template = os.path.join(root, template_name)
                    break
            if found_template:
                jinja_file = found_template
            else:
                print(f"Error: Template '{template_name}' not found in directory '{jinja_file}' or its subdirectories.")
                return 2  # Error code 2: Template not found in directory
        else:
            if 'template' in variables:
                print(f"Error: cannot find a valid template in '{jinja_file}', but 'template' keys is found, try 'auto' option to look for '{variables['template']}'.")

            else:
                print(f"Error: 'template' key not found in YAML file. Cannot determine template file from directory '{jinja_file}'.")
            return 3  # Error code 3: 'template' key missing in YAML file

    try:
        # Load Jinja2 template
        with open(jinja_file) as file:
            template_content = file.read()
    except FileNotFoundError:
        print(f"Error: Jinja2 file '{jinja_file}' does not exist.")
        return 4  # Error code 4: Jinja2 file not found

    if output_file:
        print(f"* rendering '{jinja_file}' with YAML file '{yaml_file}' into '{output_file}'")

    try:
        # Render template with variables
        template = Template(template_content)
        rendered_content = template.render(variables)
    except Exception as e:
        print(f"Error: Failed to render template '{jinja_file}' with variables from '{yaml_file}': {e}")
        return 5  # Error code 5: Template rendering failed

    # Output to file or stdout
    if output_file:
        try:
            # Get the file permissions of the Jinja file
            jinja_permissions = os.stat(jinja_file).st_mode
            if os.path.isdir(output_file):
                output_file = os.path.join(output_file, os.path.basename(jinja_file).replace(".j2", ""))
            # Write the rendered content to the output file
            with open(output_file, 'w') as file:
                file.write(rendered_content)
            
            # Apply the same permissions as the Jinja file to the output file
            os.chmod(output_file, jinja_permissions)
            
            print(f"* rendered {jinja_file} -> {output_file} using {yaml_file}")
        except Exception as e:
            print(f"Error writing to output file '{output_file}': {e}")
            return 6  # Error code 6: Failed to write to output file
    else:
        print(rendered_content)

    return 0  # Success

def main():
    parser = argparse.ArgumentParser(description="Render a Jinja2 file/directory with YAML variables.")
    parser.add_argument("jinja_file",nargs="?", help="Path to the Jinja2 template file or directory.")
    parser.add_argument("yaml_file",nargs="?", help="Path to the YAML file with variables.")
    parser.add_argument("--output", "-o", help="File or directory to write rendered output. Prints to stdout if not specified.")
    parser.add_argument("--auto", action="store_true", help="Use special 'template' key in YAML file to find the Jinja2 template.")
    parser.add_argument("--template", help="If the Jinja2 file is a directory and the ourput also, use the sepecified template file/directory.")
    parser.add_argument("--version", action="store_true", help="Show the version and exit")

    args = parser.parse_args()
    if args.version:
        print(f"version {__version__}")
        exit(0)

    if not args.jinja_file:
        print("Error: The 'jinja file/directory template' argument is required.")
        exit(1)

    if not args.yaml_file:
        print("Error: The 'yaml file' argument is required.")
        exit(1)
    else:
        # check if directory or file otherwise exit
        if not(os.path.isdir(args.yaml_file) or os.path.isfile(args.yaml_file)):
            print(f"Error: YAML file '{args.yaml_file}' is neither a file nor a directory.")
            exit(1)
        
    try:
        # Load YAML variables
        with open(args.yaml_file) as file:
            variables = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: YAML file '{yaml_file}' does not exist.")
        exit(1)  # Error code 1: YAML file not found
    template_name= None
    template_dir= None
    if args.template and ags.template != "":
        template_name = f"{args.template}.yaml.j2"
        template_dir= args.template
    if args.auto and 'template' in variables:
        template_name = f"{variables['template']}.yaml.j2"
        template_dir= variables['template']
    
    # If both are directories, copy contents then render in the destination
    if os.path.isdir(args.jinja_file) and os.path.isdir(args.output):
        # If template_dir is set, find its full path under args.jinja_file
        source_dir = args.jinja_file
        if template_dir:
            found = False
            for root, dirs, files in os.walk(args.jinja_file):
                if (os.path.basename(root) == template_dir) or (template_name in files):
                    source_dir = root
                    found = True
                    break
            if not found:
                print(f"Error: Template directory neither '{template_dir}' nor '{template_name}' found under '{args.jinja_file}'")
                exit(7)  # Error code 7: Template directory not found

        # print(f"* Copying and rendering contents of '{source_dir}' to '{args.output}'")
        for root, dirs, files in os.walk(source_dir):
            rel_path = os.path.relpath(root, source_dir)
            dest_root = os.path.join(args.output, rel_path) if rel_path != "." else args.output
            os.makedirs(dest_root, exist_ok=True)
            for file in files:
                src_file = os.path.join(root, file)
                dest_file = os.path.join(dest_root, file)
                if not os.path.exists(dest_file):
                    shutil.copy2(src_file, dest_file)
        # Render all .j2 files in the destination directory
        for root, _, files in os.walk(args.output):
            for file in files:
                if file.endswith(".j2"):
                    jinja_file_path = os.path.join(root, file)
                    output_file_path = os.path.join(root, file.replace(".j2", ""))
                    exit_code = render_jinja_to_yaml(jinja_file_path, variables,template_name, args.yaml_file, output_file_path)
                    if exit_code != 0:
                        exit(exit_code)
        exit(0)  # Success
    exit_code = render_jinja_to_yaml(args.jinja_file, variables, template_name, args.yaml_file,args.output)
    exit(exit_code)  # Exit with the appropriate error code
    
if __name__ == "__main__":
    main()
