import os
import itertools
from datetime import datetime
from pathlib import Path
import json
import subprocess
import random
import time
import mimetypes
import PyPDF2
import docx
import chardet
import openpyxl
import base64
import requests
from typing import List, Dict

from fsd.log.logger_config import get_logger

logger = get_logger(__name__)

def process_image_files(file_attachments: List[str]) -> List[str]:
        """
        Process image files from file_attachments and convert them to base64.

        Args:
            file_attachments (List[str]): List of attached file paths.

        Returns:
            List[str]: List of base64 encoded image strings with MIME type.
        """
        image_files = []
        image_extensions = ('.webp', '.jpg', '.jpeg', '.png')
        
        for file_path in file_attachments:
            if file_path.lower().endswith(image_extensions):
                try:
                    with open(file_path, "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                        file_extension = os.path.splitext(file_path)[1].lower()
                        mime_type = f"image/{file_extension[1:]}" if file_extension != '.jpg' else "image/jpeg"
                        image_files.append(f"data:{mime_type};base64,{encoded_string}")
                except Exception as e:
                    logger.error(f"Error processing image file {file_path}: {str(e)}")
        
        return image_files

def read_file_content(file_path):
    """
    Read and return the content of any type of file, including special files like PDFs,
    DOCs, XLSX, and all code file types. Works cross-platform on Windows and macOS/Linux.

    Args:
        file_path (str): Full path to the file.

    Returns:
        str: Content of the file or empty string if file doesn't exist or can't be read.
    """
    # Convert to Path object to handle cross-platform paths
    file_path = Path(file_path)
    
    if not file_path.exists():
        logger.debug(f"File does not exist: {file_path}")
        return ""

    mime_type, _ = mimetypes.guess_type(str(file_path))

    try:
        # Handle PDF files
        if mime_type == 'application/pdf':
            with file_path.open('rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text_content = []
                for page in pdf_reader.pages:
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
                content = '\n'.join(text_content)

        # Handle DOC and DOCX files
        elif mime_type in [
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        ]:
            doc = docx.Document(file_path)
            content = '\n'.join(paragraph.text for paragraph in doc.paragraphs)

        # Handle XLSX (Excel) files
        elif mime_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            workbook = openpyxl.load_workbook(file_path, data_only=True)
            sheet = workbook.active  # Read the first sheet
            data = []
            for row in sheet.iter_rows(values_only=True):
                data.append('\t'.join([str(cell) if cell is not None else "" for cell in row]))
            content = '\n'.join(data)

        # Handle text and code files
        else:
            # Attempt to read as UTF-8 first
            try:
                content = file_path.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                # If UTF-8 fails, detect encoding
                raw_data = file_path.read_bytes()
                detected = chardet.detect(raw_data)
                encoding = detected['encoding'] if detected['encoding'] else 'utf-8'
                content = raw_data.decode(encoding, errors='replace')

        return "This file is currently empty, content is \"\", this is just a note, not content" if content.strip() == "" else content

    except Exception as e:
        logger.exception(f"Failed to read file {file_path}: {e}")
        return "This file is currently empty, content is \"\", this is just a note, not content"

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".svg",
    ".tiff",
    ".ico",
    ".webp",
}
VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".avi",
    ".mkv",
    ".flv",
    ".wmv",
    ".webm",
    ".m4v",
    ".mpg",
    ".mpeg",
    ".3gp",
}

IGNORE_DIRS = {
    "node_modules",
    "venv",
    ".venv",
    "env",
    ".env",
    "vendor",
    "Pods",
    "Carthage",
    ".git",
    ".idea",
    ".vscode",
    "__pycache__",
    "build",
    "dist",
    ".gradle",
    ".m2",
    ".bundle",
    ".cxx",
    "DerivedData",
    "Assets.xcassets",
    "Preview Assets.xcassets",
    "xcuserdata",
    "xcshareddata",
    "Zinley",
}

IGNORE_FILES = {
    ".gitignore",
    ".gitattributes",
    "README.md",
    "LICENSE",
    "yarn.lock",
    "package-lock.json",
    "Pipfile.lock",
    ".DS_Store",
    ".env",
    "Gemfile.lock",
    "Cargo.lock",
    ".classpath",
    ".project",
    "Thumbs.db",
    "npm-debug.log",
    "pip-log.txt",
    ".metadata",
    ".pbxproj",
    ".xcworkspace",
    ".DS_Store",
    ".xcodeproj",
    "file_modification_times.txt",
}

CODE_EXTENSIONS = {
    # Programming languages
    ".py",
    ".pyc",
    ".pyo",
    ".pyw",
    ".pyx",
    ".pxd",
    ".pyd",  # Python
    ".js",
    ".jsx",
    ".ts",
    ".tsx",  # JavaScript/TypeScript
    ".java",
    ".class",
    ".jar",  # Java
    ".c",
    ".h",
    ".cpp",
    ".hpp",
    ".cc",
    ".cxx",
    ".hh",
    ".hxx",
    ".ino",  # C/C++
    ".cs",
    ".csproj",  # C#
    ".go",  # Go
    ".rb",
    ".rbw",
    ".rake",
    ".gemspec",
    ".rhtml",  # Ruby
    ".php",
    ".phtml",
    ".php3",
    ".php4",
    ".php5",
    ".php7",
    ".phps",
    ".phpt",  # PHP
    ".kt",
    ".kts",  # Kotlin
    ".swift",  # Swift
    ".m",
    ".mm",  # Objective-C
    ".r",
    ".rdata",
    ".rds",
    ".rda",
    ".rproj",  # R
    ".pl",
    ".pm",
    ".t",  # Perl
    ".sh",
    ".bash",
    ".bats",
    ".zsh",
    ".ksh",
    ".csh",  # Shell scripts
    ".lua",  # Lua
    ".erl",
    ".hrl",
    ".beam",  # Erlang
    ".ex",
    ".exs",  # Elixir
    ".ml",
    ".mli",
    ".fs",
    ".fsi",
    ".fsx",
    ".fsscript",  # OCaml/F#
    ".scala",
    ".sbt",
    ".sc",  # Scala
    ".jl",  # Julia
    ".hs",
    ".lhs",  # Haskell
    ".clj",
    ".cljs",
    ".cljc",
    ".edn",  # Clojure
    ".groovy",
    ".gvy",
    ".gy",
    ".gsh",  # Groovy
    ".v",
    ".vh",
    ".sv",
    ".svh",  # Verilog/SystemVerilog
    ".vhd",
    ".vhdl",  # VHDL
    ".adb",
    ".ads",
    ".ada",  # Ada
    ".d",
    ".di",  # D
    ".nim",
    ".nims",  # Nim
    ".rs",
    ".rlib",  # Rust
    ".cr",  # Crystal
    ".cmake",
    ".make",
    ".mak",
    ".mk",  # Build files
    ".bat",
    ".cmd",  # Batch files
    # Markup and stylesheets
    ".html",
    ".htm",
    ".xhtml",
    ".jhtml",  # HTML
    ".css",
    ".scss",
    ".sass",
    ".less",  # CSS and preprocessors
    ".xml",
    ".xsl",
    ".xslt",
    ".xsd",
    ".dtd",
    ".wsdl",  # XML
    ".md",
    ".markdown",
    ".mdown",
    ".mkdn",
    ".mkd",
    ".rst",
    ".adoc",
    ".asciidoc",  # Markdown/AsciiDoc/ReStructuredText
    # Configuration files
    ".json",
    ".yml",
    ".yaml",
    ".ini",
    ".cfg",
    ".conf",
    ".toml",
    ".plist",
    ".env",
    ".editorconfig",
    ".eslintrc",
    ".prettierrc",
    ".babelrc",
    ".stylelintrc",
    ".dockerfile",
    ".dockerignore",
    ".gitlab-ci.yml",
    ".travis.yml",
    ".circleci/config.yml",
    # Data files
    ".csv",
    ".tsv",
    ".parquet",
    ".avro",
    ".orc",
    ".json",
    ".xml",
    # iOS-specific
    ".nib",
    ".xib",
    ".storyboard",  # iOS
    # Android-specific
    ".gradle",
    ".pro",
    ".aidl",
    ".rs",
    ".rsh",
    ".xml",
    # Desktop app specific
    ".desktop",
    ".manifest",
    ".rc",
    ".resx",
    ".xaml",
    ".appxmanifest",
    ".csproj",
    ".vbproj",
    # Web app specific
    ".asp",
    ".aspx",
    ".ejs",
    ".hbs",
    ".jsp",
    ".jspx",
    ".php",
    ".cfm",
    # Database related
    ".sql",
    ".db",
    ".db3",
    ".sqlite",
    ".sqlite3",
    ".rdb",
    ".mdb",
    ".accdb",
    ".pdb",
    # Others
    ".tex",
    ".bib",
    ".log",
    ".txt",
}

PARSERS = {
    ".py": "python",
    ".js": "javascript",
    ".mjs": "javascript",  # mjs file extension stands for "module JavaScript."
    ".go": "go",
    ".bash": "bash",
    ".c": "c",
    ".cc": "cpp",
    ".cs": "c_sharp",
    ".cl": "commonlisp",
    ".cpp": "cpp",
    ".css": "css",
    ".dockerfile": "dockerfile",
    ".dot": "dot",
    ".el": "elisp",
    ".ex": "elixir",
    ".elm": "elm",
    ".et": "embedded_template",
    ".erl": "erlang",
    ".gomod": "gomod",
    ".hack": "hack",
    ".hs": "haskell",
    ".hcl": "hcl",
    ".html": "html",
    ".java": "java",
    ".jsdoc": "jsdoc",
    ".json": "json",
    ".jl": "julia",
    ".kt": "kotlin",
    ".lua": "lua",
    ".mk": "make",
    # ".md": "markdown", # https://github.com/ikatyang/tree-sitter-markdown/issues/59
    ".m": "objc",
    ".ml": "ocaml",
    ".pl": "perl",
    ".php": "php",
    ".ql": "ql",
    ".r": "r",
    ".R": "r",
    ".regex": "regex",
    ".rst": "rst",
    ".rb": "ruby",
    ".rs": "rust",
    ".scala": "scala",
    ".sql": "sql",
    ".sqlite": "sqlite",
    ".toml": "toml",
    ".tsq": "tsq",
    ".tsx": "typescript",
    ".ts": "typescript",
    ".vue": "vuejs",
    ".vuex": "vuejs",
    ".yaml": "yaml",
    ".swift": "swift",
    ".nib": "swift",
    ".xib": "swift",
    ".storyboard": "swift",  # iOS
}


def filename_to_lang(filename):
    file_extension = os.path.splitext(filename)[1]
    lang = PARSERS.get(file_extension)
    return lang


def get_current_time_formatted():
    current_time = datetime.now()
    formatted_time = current_time.strftime("%m/%d/%y")
    return formatted_time


def get_available_simulator_details():
    try:
        # Run the xcrun command to get a list of simulators in JSON format
        result = subprocess.run(
            ["xcrun", "simctl", "list", "devices", "--json"],
            capture_output=True,
            text=True,
            check=True,
        )

        # Parse the JSON output
        devices = json.loads(result.stdout)

        # Extract detailed information of the available iOS simulators
        available_simulator_details = []
        for device_type in devices["devices"]:
            # Filter for iOS simulators only
            if "iOS" in device_type:
                for device in devices["devices"][device_type]:
                    if device.get("isAvailable", False):
                        details = {
                            "name": device.get("name", "Unknown"),
                            "state": device.get("state", "Unknown"),
                            "udid": device.get("udid", "Unknown"),
                            "device_type": device_type,
                        }
                        available_simulator_details.append(details)

        return available_simulator_details

    except subprocess.CalledProcessError as e:
        logger.error(f"An error occurred while fetching the simulator details: {e}")
        return []


def get_preferred_simulator_uuid():
    available_simulators = get_available_simulator_details()

    # Filter for booted simulators
    booted_simulators = [
        sim for sim in available_simulators if sim["state"] == "Booted"
    ]

    if booted_simulators:
        chosen = random.choice(booted_simulators)
        logger.debug(f"Using: {chosen}")
        udid = chosen["udid"]
        return udid

    # If no simulators are booted, filter for shutdown simulators in the iPhone range
    shutdown_iphones = [
        sim
        for sim in available_simulators
        if sim["state"] == "Shutdown" and "iPhone" in sim["name"]
    ]

    if shutdown_iphones:
        chosen = random.choice(shutdown_iphones)
        logger.debug(f"Using: {chosen}")
        udid = chosen["udid"]
        return udid

    return None


def create_file_modification_times(project_path):
    file_mod_times = []
    for root, _, files in os.walk(project_path):
        for file in files:
            filepath = os.path.join(root, file)
            mod_time = (
                subprocess.check_output(["stat", "-f", "%Sm %N", filepath])
                .decode("utf-8")
                .strip()
            )
            file_mod_times.append(mod_time)
    home_directory = os.path.expanduser("~")
    hidden_zinley_folder_name = ".zinley"
    parts = project_path.split("/")
    project_name = parts[-1]
    with open(
        os.path.join(
            home_directory,
            hidden_zinley_folder_name,
            project_name,
            "Zinley",
            "Project_analysis",
            "file_modification_times.txt",
        ),
        "w",
    ) as f:
        for line in file_mod_times:
            f.write(line + "\n")


def safe_abs_path(res):
    "Gives an abs path, which safely returns a full (not 8.3) windows path"
    res = Path(res).resolve()
    return str(res)


def is_image_file(file_name):
    """
    Check if the given file name has an image file extension.

    :param file_name: The name of the file to check.
    :return: True if the file is an image, False otherwise.
    """
    file_name = str(file_name)  # Convert file_name to string
    return any(file_name.endswith(ext) for ext in IMAGE_EXTENSIONS)

def parse_payload(project_path, user_prompt_json):
    try:
        data = json.loads(user_prompt_json)
        user_prompt = data.get("prompt", "")
        file_path = data.get("file_path", [])
        tracked_file = data.get("tracked_file", [])
        tier = data.get("tier", "Free")


        if tracked_file:
            tracked_file = [os.path.join(project_path, file.lstrip('./')) for file in tracked_file]

        return user_prompt, tier, file_path, tracked_file
    except:
        return user_prompt_json, "", [], []


class Spinner:
    spinner_chars = itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])

    def __init__(self, text):
        self.text = text
        self.start_time = time.time()
        self.last_update = 0
        self.visible = False

    def step(self):
        current_time = time.time()
        if not self.visible and current_time - self.start_time >= 0.5:
            self.visible = True
            self._step()
        elif self.visible and current_time - self.last_update >= 0.1:
            self._step()
        self.last_update = current_time

    def _step(self):
        if not self.visible:
            return

    def end(self):
        return