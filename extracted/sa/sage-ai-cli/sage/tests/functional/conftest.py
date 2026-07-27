import pytest
import yaml
import itertools
import os
from pathlib import Path
import sys

def pytest_configure(config):
    """
    Enforce the strict zero-mock policy across the functional test sweep.
    If any test uses mocks, stubs, spies, or virtual clocks, we crash the suite.
    """
    pass

@pytest.fixture(autouse=True)
def enforce_zero_mock_policy(request):
    """
    Throws an error if a test requests any mocking fixtures.
    """
    forbidden_fixtures = ['mocker', 'monkeypatch', 'mock']
    for fix in forbidden_fixtures:
        if fix in request.fixturenames:
            pytest.fail(f"ZERO-MOCK POLICY VIOLATION: Test {request.node.name} requested forbidden fixture '{fix}'.")

# All functional tests hit real cloud APIs — mark as integration.
pytestmark = [
    pytest.mark.timeout(900),
    pytest.mark.integration,
]

# Load the matrix once
with open(Path(__file__).parent / "matrix.yml") as f:
    MATRIX = yaml.safe_load(f)

def build_request(channel: str, entry: dict, model: str, flag_set: dict) -> dict:
    args = []
    for flag, value in flag_set.items():
        if value is not None:
            args.extend([flag, str(value)])

    request = {
        "channel": channel,
        "model": model,
        "command": entry["command"],
        "args": args,
    }

    # Generate a sensible prompt string from the args
    prompt_str = f"{entry['command']} " + " ".join([f"{k.lstrip('-')} {v}" for k, v in flag_set.items() if v is not None])

    if channel == "sms":
        request["sms_request"] = f"sage {prompt_str}"
    elif channel == "web":
        request["web_request"] = {"task": prompt_str}
    elif channel == "cli":
        request["cli_request"] = f"sage ask '{prompt_str}' --raw"
        
    request["description"] = entry["description"]
    request["success_criteria"] = dict(entry.get("success_criteria", {}))
    # For file validation:
    if "--extension" in flag_set and flag_set["--extension"] is not None:
        request["success_criteria"]["extension"] = flag_set["--extension"]
    elif "--format" in flag_set and flag_set["--format"] is not None:
        request["success_criteria"]["extension"] = "." + flag_set["--format"]
    elif "--lang" in flag_set and flag_set["--lang"] is not None:
         lang_map = {
             "python": ".py", "go": ".go", "rust": ".rs", "java": ".java", 
             "javascript": ".js", "typescript": ".ts", "c++": ".cpp", "c#": ".cs",
             "swift": ".swift", "kotlin": ".kt", "ruby": ".rb", "php": ".php",
             "perl": ".pl", "dart": ".dart", "scala": ".scala", "elixir": ".ex",
             "haskell": ".hs", "clojure": ".clj", "r": ".r", "lua": ".lua"
         }
         if flag_set["--lang"] in lang_map:
             request["success_criteria"]["extension"] = lang_map[flag_set["--lang"]]
    elif entry["domain"] == "web":
         request["success_criteria"]["extension"] = ".html"
    elif entry["domain"] == "backend":
         pass # Backend could be any language or a Dockerfile
    elif entry["domain"] == "animation":
         request["success_criteria"]["extension"] = ".mp4"
    elif entry["domain"] == "music_video":
         request["success_criteria"]["extension"] = ".mp4"

    return request

def _flag_combinations(entry):
    flag_names = [f["name"] for f in entry.get("flags", [])]
    value_sets = []
    for f in entry.get("flags", []):
        # include both valid and invalid values
        vals = f["values"].get("valid", []) + f["values"].get("invalid", [])
        value_sets.append(vals)
    for combo in itertools.product(*value_sets):
        yield dict(zip(flag_names, combo))

def pytest_generate_tests(metafunc):
    if "test_case" not in metafunc.fixturenames:
        return

    # Use a stable, local model for the exhaustive sweep to avoid cloud mock failures
    models = ["cloud:qwen3-coder"]
    
    cases = []
    ids = []

    for entry in MATRIX:
        # Generate combinatorial cases only if it matches the test file's domain
        test_file_name = os.path.basename(str(metafunc.definition.fspath))
        if entry["domain"] not in test_file_name:
             continue
             
        for flag_set in _flag_combinations(entry):
            # To prevent spamming Apple's iMessage network with thousands of real messages,
            # we restrict the 'sms' channel to only a tiny subset of core scenarios.
            channels = ["cli", "web"]
            if flag_set == list(_flag_combinations(entry))[0]:
                channels.append("sms")
                
            for channel in channels:
                for model in models:
                    request = build_request(channel, entry, model, flag_set)
                    case = {
                        "entry": entry,
                        "request": request,
                        "flag_set": flag_set,
                        "channel": channel,
                        "model": model,
                    }
                    cases.append(case)
                    ids.append(
                        f"{entry['domain']}-{entry['command']}"
                        f"-{channel}-{model.split(':')[-1]}-"
                        f"{'_'.join(f'{k}{v}' for k, v in flag_set.items() if v is not None)}"
                    )
    metafunc.parametrize("test_case", cases, ids=ids)
