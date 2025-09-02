import os

nose_path = "/Users/aartamonov/homebrew/lib/python3.10/site-packages/nose"

for root, dirs, files in os.walk(nose_path):
    for filename in files:
        if filename.endswith(".py"):
            filepath = os.path.join(root, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            original_content = content  # Save for comparison

            # Replace patterns
            if "import collections" in content:
                content = content.replace("import collections", "from collections.abc import Callable")
            if "collections.Callable" in content:
                content = content.replace("collections.Callable", "Callable")

            if content != original_content:
                print(f"Patching: {filepath}")
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)

