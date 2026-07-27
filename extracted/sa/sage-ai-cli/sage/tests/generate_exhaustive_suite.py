import os
import json
import itertools
import shutil

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_REGISTRY_PATH = os.path.join(TESTS_DIR, "../../model_servers/model_registry.json")
E2E_DIR = os.path.join(TESTS_DIR, "e2e_exhaustive")

# Use cases across different domains based on user prompt
DOMAINS = {
    "web": [
        "Build a simple HTML landing page with CSS grid and a contact form.",
        "Create a React to-do list component with state management.",
        "Build a Vite + Vue3 counter application."
    ],
    "mobile": [
        "Create a React Native screen with a flatlist and pull-to-refresh.",
        "Build a Flutter login screen layout with email and password."
    ],
    "backend": [
        "Write a FastAPI server with a single POST route that echoes JSON.",
        "Create an Express.js server that connects to a mocked Postgres database.",
        "Write a Python script to parse a CSV file and output JSON."
    ],
    "video_games": [
        "Create a simple Pygame script that draws a moving square.",
        "Write a Unity C# script for basic player movement."
    ],
    "media": [
        "Generate a simple SVG logo with a circle and text.",
        "Create an HTML5 canvas animation of a bouncing ball.",
        "Write a script that outputs a valid markdown document with a table."
    ],
    "integrations": [
        "Use a native macOS AppleScript to initiate a FaceTime audio phone call.",
        "Send an email using smtplib to a test address."
    ]
}

CLIENTS = ["cli", "website", "sms"]
SMS_DELIVERY = ["email", "sms", "imessage", "kdeconnect"]

# Commands that don't invoke LLMs but need coverage
CLI_COMMANDS = ["sync", "sync-catalog", "train-all", "train", "use", "rm", "login", "logout", "whoami", "fix-llama-cpp"]
SMS_COMMANDS = ["/help", "/models", "/model", "/autoorg", "/status", "/clear", "/exit"]

def get_models():
    if os.path.exists(MODEL_REGISTRY_PATH):
        with open(MODEL_REGISTRY_PATH, 'r') as f:
            registry = json.load(f)
            # Fetch cloud models for the exhaustive sweep
            models = []
            for k in registry.keys():
                if not k.startswith("_"):
                    models.append(f"cloud:{k}")
            return models
    # Fallback default
    return ["cloud:qwen3-coder", "cloud:llama-3", "local:mistral"]

def generate_suite():
    if os.path.exists(E2E_DIR):
        shutil.rmtree(E2E_DIR)
    
    models = get_models()
    count = 0
    
    for client in CLIENTS:
        client_dir = os.path.join(E2E_DIR, client)
        os.makedirs(client_dir, exist_ok=True)
        
        # 1. Generate Task-based Tests (iterate models)
        for model in models:
            for domain, tasks in DOMAINS.items():
                for idx, task in enumerate(tasks):
                    # For SMS, we also permutate over delivery methods
                    if client == "sms":
                        for delivery in SMS_DELIVERY:
                            filename = f"test_{client}_{model.replace(':', '_')}_{domain}_{delivery}_{idx}.py"
                            filepath = os.path.join(client_dir, filename)
                            write_test_file(filepath, client, model, domain, task, delivery)
                            count += 1
                    else:
                        filename = f"test_{client}_{model.replace(':', '_')}_{domain}_{idx}.py"
                        filepath = os.path.join(client_dir, filename)
                        write_test_file(filepath, client, model, domain, task, delivery=None)
                        count += 1
        
        # 2. Generate Utility Command Tests
        if client == "cli":
            for cmd in CLI_COMMANDS:
                filename = f"test_cli_cmd_{cmd.replace('-', '_')}.py"
                filepath = os.path.join(client_dir, filename)
                write_utility_test(filepath, "cli", cmd)
                count += 1
        elif client == "sms":
            for cmd in SMS_COMMANDS:
                for delivery in SMS_DELIVERY:
                    filename = f"test_sms_cmd_{cmd.replace('/', '')}_{delivery}.py"
                    filepath = os.path.join(client_dir, filename)
                    write_utility_test(filepath, "sms", cmd, delivery)
                    count += 1
                        
    print(f"Generated {count} exhaustive test files in {E2E_DIR}")

def write_utility_test(filepath, client, cmd, delivery=None):
    with open(filepath, 'w') as f:
        f.write(f'\"\"\"Exhaustive utility test for {client}, command {cmd}.\"\"\"\n')
        f.write('import pytest\n')
        f.write('from sage.tests.rubric_checker import verify_utility_command\n\n')
        test_name = f"test_{client}_cmd_{cmd.replace('/', '').replace('-', '_')}"
        if delivery:
            test_name += f"_{delivery}"
        
        f.write(f'def {test_name}(tmp_path):\n')
        if delivery:
            f.write(f'    verify_utility_command("{client}", "{cmd}", tmp_path, delivery="{delivery}")\n')
        else:
            f.write(f'    verify_utility_command("{client}", "{cmd}", tmp_path)\n')

def write_test_file(filepath, client, model, domain, task, delivery):
    with open(filepath, 'w') as f:
        f.write(f'\"\"\"Exhaustive test for {client}, model {model}, domain {domain}.\"\"\"\n')
        f.write('import pytest\n')
        f.write('from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric\n\n')
        
        # Test function
        safe_model_name = model.replace(":", "_").replace("-", "_")
        test_name = f"test_{client}_{safe_model_name}_{domain}"
        if delivery:
            test_name += f"_{delivery}"
        
        f.write(f'def {test_name}(tmp_path):\n')
        f.write(f'    prompt = "{task}"\n')
        # We inject the model into the prompt instructions so the CLI/backend uses it.
        f.write(f'    task_with_model = f"{{prompt}} Use model {model}."\n')
        
        if client == "cli":
            f.write(f'    verify_cli_with_rubric(task_with_model, domain="{domain}")\n')
        elif client == "sms":
            f.write(f'    verify_sms_with_rubric(task_with_model, tmp_path)\n')
        elif client == "website":
            f.write(f'    verify_website_with_rubric(task_with_model, tmp_path)\n')

if __name__ == "__main__":
    generate_suite()
