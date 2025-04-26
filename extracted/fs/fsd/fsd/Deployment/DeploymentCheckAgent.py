import os
import aiohttp
import asyncio
import json
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from util.portkey import AIGateway
from json_repair import repair_json
from log.logger_config import get_logger
from fsd.util.utils import read_file_content
import platform
logger = get_logger(__name__)

class DeploymentCheckAgent:
    def __init__(self, repo):
        self.repo = repo
        self.max_tokens = 4096
        self.ai = AIGateway()

    def _calculate_code_percentages(self, root_path):
        """Calculate percentages of HTML/CSS vs React code in the project"""
        html_css_lines = 0
        react_lines = 0
        
        for root, _, files in os.walk(root_path):
            # Skip ignored directories
            if any(ignored in root for ignored in self.repo.IGNORED_DIRECTORIES["default"]):
                continue

            for file in files:
                if file.endswith(('.html', '.css')):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        html_css_lines += sum(1 for _ in f)
                elif file.endswith(('.js', '.jsx', '.ts', '.tsx')):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        react_lines += sum(1 for _ in f)

        total_lines = html_css_lines + react_lines
        if total_lines == 0:
            return 0, 0

        html_css_percent = (html_css_lines / total_lines) * 100
        react_percent = (react_lines / total_lines) * 100
        
        return html_css_percent, react_percent

    def _read_package_json(self, root_path):
        """Read and analyze package.json if it exists"""
        package_json_path = os.path.join(root_path, 'package.json')
        if not os.path.exists(package_json_path):
            return None

        try:
            with open(package_json_path, 'r', encoding='utf-8') as f:
                package_data = json.load(f)
                
            # Check dependencies and devDependencies
            dependencies = package_data.get('dependencies', {})
            dev_dependencies = package_data.get('devDependencies', {})
            
            # Look for React-related dependencies
            react_deps = [
                'react', 'react-dom', 'next', 'gatsby', 
                'react-native', '@react', 'preact',
                'create-react-app', 'expo'
            ]
            
            has_react = any(
                any(dep.startswith(r) for r in react_deps)
                for dep in list(dependencies.keys()) + list(dev_dependencies.keys())
            )
            
            return {
                'has_react': has_react,
                'dependencies': dependencies,
                'dev_dependencies': dev_dependencies
            }
        except Exception as e:
            logger.error(f"Error reading package.json: {e}")
            return None

    async def get_deployment_check_plan(self):
        """
        Get a development plan for all txt files from Azure OpenAI based on the user prompt.

        Args:
            session (aiohttp.ClientSession): The aiohttp session to use for the request.
            all_file_contents (str): The concatenated contents of all files.

        Returns:
            dict: Development plan or error reason.
        """
        repo_path = self.repo.get_repo_path()
        package_info = self._read_package_json(repo_path)
        html_css_percent, react_percent = self._calculate_code_percentages(repo_path)
        
        # Check if project uses Next.js
        if package_info and package_info.get('dependencies'):
            if 'next' in package_info['dependencies'] or '@next' in package_info['dependencies']:
                return {
                    "result": "0",
                    "project_type": "1", 
                    "full_project_path": None,
                    "reason": "Next.js projects are not currently supported for deployment"
                }
        
        code_analysis = (
            f"Code Analysis:\n"
            f"HTML/CSS code: {html_css_percent:.1f}%\n"
            f"React/JS code: {react_percent:.1f}%\n"
        )

        if package_info:
            code_analysis += (
                f"package.json analysis:\n"
                f"Has React dependencies: {package_info['has_react']}\n"
                f"Total dependencies: {len(package_info['dependencies'])}\n"
                f"Total dev dependencies: {len(package_info['dev_dependencies'])}\n"
            )

        messages = [
            {
                "role": "system", 
                "content": (
                    "Check if the current project is eligible for deployment as either a static HTML/CSS website or a React-based app (including React Native, etc.). "
                    "For HTML/CSS, the project is eligible if there's an index.html file directly in the project root. "
                    "For React-based projects, the project is eligible if there's a package.json file directly in the project root. "
                    f"The root path: {repo_path}\n"
                    f"User OS: {platform.system()}\n"
                    f"Current code analysis:\n{code_analysis}\n"
                    "Here's the project structure:\n"
                    f"{self.repo.print_tree()}\n\n"
                    "Example of an eligible HTML/CSS project structure:\n"
                    "project_root/\n"
                    "├── index.html\n"
                    "├── css/\n"
                    "│   └── styles.css\n"
                    "├── js/\n"
                    "│   └── script.js\n"
                    "└── images/\n"
                    "    └── logo.png\n\n"
                    "Example of an HTML/CSS project with package.json (still considered HTML/CSS):\n"
                    "project_root/\n"
                    "├── package.json  # Only used for dev tools like sass/less\n"
                    "├── index.html    # Main entry point\n"
                    "├── css/\n"
                    "│   ├── styles.css\n"
                    "│   └── main.css\n"
                    "├── js/\n"
                    "│   └── script.js # Plain JavaScript\n"
                    "└── assets/\n"
                    "    └── images/\n"
                    "        └── logo.png\n\n"
                    "Examples of eligible React-based project structures:\n"
                    "1. Basic React project:\n"
                    "project_root/\n"
                    "├── package.json\n"
                    "├── src/\n"
                    "│   ├── App.js\n"
                    "│   └── index.js\n"
                    "└── public/\n"
                    "    └── index.html\n\n"
                    "2. React Native project:\n"
                    "project_root/\n"
                    "├── package.json\n"
                    "├── App.js\n"
                    "├── index.js\n"
                    "└── android/\n"
                    "    └── ...\n"
                    "└── ios/\n"
                    "    └── ...\n\n"
                    "3. TypeScript React project:\n"
                    "project_root/\n"
                    "├── package.json\n"
                    "├── tsconfig.json\n"
                    "└── src/\n"
                    "    ├── App.tsx\n"
                    "    └── index.tsx\n\n"
                    "4. Create React App project:\n"
                    "project_root/\n"
                    "├── package.json\n"
                    "├── src/\n"
                    "│   ├── App.js\n"
                    "│   ├── index.js\n"
                    "│   └── App.css\n"
                    "└── public/\n"
                    "    └── index.html\n\n"
                    "5. Gatsby project:\n"
                    "project_root/\n"
                    "├── package.json\n"
                    "├── gatsby-config.js\n"
                    "└── src/\n"
                    "    └── pages/\n"
                    "        └── index.js\n\n"
                    "6. Expo React Native project:\n"
                    "project_root/\n"
                    "├── package.json\n"
                    "├── App.js\n"
                    "└── app.json\n\n"
                    "7. React with Redux project:\n"
                    "project_root/\n"
                    "├── package.json\n"
                    "└── src/\n"
                    "    ├── actions/\n"
                    "    ├── reducers/\n"
                    "    ├── components/\n"
                    "    └── index.js\n\n"
                    "8. React with Webpack configuration:\n"
                    "project_root/\n"
                    "├── package.json\n"
                    "├── webpack.config.js\n"
                    "└── src/\n"
                    "    └── index.js\n\n"
                    "9. Preact project:\n"
                    "project_root/\n"
                    "├── package.json\n"
                    "└── src/\n"
                    "    ├── index.js\n"
                    "    └── components/\n"
                    "        └── app.js\n\n"
                    "Respond in this exact JSON format:\n"
                    "{\n"
                    '    "result": "0" or "1",\n'
                    '    "project_type": "0" or "1",\n'
                    '    "full_project_path": "full/path/to/project_folder" or null\n'
                    "}\n"
                    "Where 'result' is '1' if eligible, '0' if not. "
                    "'project_type' is '0' for purely static HTML/CSS, '1' for React-based project. "
                    "For HTML/CSS, 'full_project_path' must be the full path to the project root containing index.html, e.g., '/home/user/projects/mysite' for Linux/Mac or 'C:\\Users\\user\\projects\\mysite' for Windows. "
                    "For React-based projects, 'full_project_path' must be the full path to the project root containing package.json, e.g., '/home/user/projects/myapp' for Linux/Mac or 'C:\\Users\\user\\projects\\myapp' for Windows. "
                    "If you see a project with package.json but the majority of code is HTML/CSS (e.g. only using package.json for dev tools), "
                    "treat it as an HTML/CSS project with project_type '0' and set full_project_path to the folder containing index.html. "
                    "Return null if not found. "
                    "IMPORTANT: Ensure all paths returned match the user's OS format - use forward slashes for Linux/Mac and backslashes for Windows."
                )
            },
            {
                "role": "user",
                "content": "Check if this project is eligible for deployment and return full path for deploy folder."
            }
        ]

        try:
            logger.debug("\n #### `SnowX` is initiating a request to the AI Gateway")
            response = await self.ai.arch_prompt(messages, 4096, 0, 0)
            res = json.loads(response.choices[0].message.content)
            logger.debug("\n #### `SnowX` has successfully parsed the AI response")
            return res
        except json.JSONDecodeError:
            logger.debug("\n #### `SnowX` encountered a JSON decoding error and is attempting to repair it")
            good_json_string = repair_json(response.choices[0].message.content)
            plan_json = json.loads(good_json_string)
            logger.debug("\n #### `SnowX` has successfully repaired and parsed the JSON")
            return plan_json
        except Exception as e:
            logger.error(f"  `SnowX` encountered an error during the process: `{e}`")
            return {
                "reason": str(e)
            }

    async def get_deployment_check_plans(self):
        """
        Get development plans for a list of txt files from Azure OpenAI based on the user prompt.

        Args:
            files (list): List of file paths.

        Returns:
            dict: Development plan or error reason.
        """
        logger.debug("\n #### `SnowX` is beginning to retrieve deployment check plans")
        plan = await self.get_deployment_check_plan()
        logger.debug("\n #### `SnowX` has successfully retrieved deployment check plans")
        return plan
