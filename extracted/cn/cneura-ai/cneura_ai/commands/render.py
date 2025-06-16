import sys
import json
import yaml
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

def load_config(config_path):
    ext = Path(config_path).suffix
    with open(config_path, 'r') as file:
        if ext in ['.yaml', '.yml']:
            return yaml.safe_load(file)
        elif ext == '.json':
            return json.load(file)
        else:
            raise ValueError(f"Unsupported config file type: {ext}")

def render_template(template_file, config, output_file):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template_file)
    rendered = template.render(config)

    # Ensure the output directory exists
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(rendered)
    print(f"✅ Rendered: {output_file}")

def main():
    if len(sys.argv) != 4:
        print("Usage: python render.py <template_file> <config_file> <output_file>")
        sys.exit(1)

    template_file = sys.argv[1]
    config_file = sys.argv[2]
    output_file = sys.argv[3]

    config = load_config(config_file)
    render_template(template_file, config, output_file)

if __name__ == "__main__":
    main()
