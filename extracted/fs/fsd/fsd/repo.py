import io
from typing import Counter
import git
import os
from pathlib import Path, PurePosixPath
import sys
from grep_ast import filename_to_lang
import fnmatch

from fsd.io import InputOutput
from fsd.repomap import RepoMap
from fsd.util import utils
from fsd.util.tree import Tree
from fsd.util.s3 import deploy_zip_to_s3
from fsd.util.sqs import send_message_to_sqs
from fsd.system.OSEnvironmentDetector import OSEnvironmentDetector

from fsd.log.logger_config import get_logger
logger = get_logger(__name__)


class GitRepo:
    DEFAULT_DOMAIN = 'NOT_SET'
    IGNORED_DIRECTORIES = {
        "default": [
            ".git",
            ".DS_Store", 
            "Thumbs.db",
            "logs",
            "log",
            "temp",
            "tmp",
            "backup",
            "backup_*",
            "__pycache__",
            ".pytest_cache",
            "env",
            ".env",
            "venv",
            ".venv",
            "node_modules",
            "dist",
            ".cache",
            "build",
            "out",
            "obj",
            "bin",
            "target",
            ".gradle",
            ".settings",
            "pkg",
            "vendor",
            ".bundle",
            ".cargo",
            ".swiftpm",
            "Pods",
            "Podfile.lock",
            ".dart_tool",
            ".build",
            "Packages",
            "_build",
            "deps",
            "dist-newstyle",
            ".stack-work",
            "bower_components",
            "jspm_packages",
            "coverage",
            "cypress",
            "public",
            "private",
            "migrations",
            "pyvenv",
            "mix.lock",
            "*.hi",
            "*.o",
            ".idea",
            ".vscode",
            ".project",
            ".classpath",
            ".settings",
            ".metadata",
            "*.iml",
            "build/",
            "out/",
            "coverage/",
            ".nyc_output/",
            ".eslintcache",
            ".parcel-cache",
            "yarn-error.log",
            "yarn-debug.log",
            "npm-debug.log",
            "pnpm-debug.log",
            ".expo",
            "android/build",
            "ios/build",
            "ios/Pods",
            "*.xcodeproj",
            "*.xcworkspace",
            "*.pbxproj",
            "contents.xcworkspacedata",
            "xcshareddata",
            "IDEWorkspaceChecks.plist",
            "swiftpm/",
            "swiftpm/configuration",
            "xcuserdata/",
            "xcschemes/",
            "xcschememanagement.plist",
            "UserInterfaceState.xcuserstate",
            ".vs",
            "*.sln",
            "*.user",
            "*.suo",
            "*.vcxproj",
            "nbproject",
            "Eclipse/",
            "nbproject/",
            "CMakeFiles/",
            "*.code-workspace",
            "*.launch",
            ".vscode/",
            ".idea/",
            ".settings/",
            ".metadata/",
            ".project/",
            "*.sublime-project",
            "*.sublime-workspace",
        ],
        "c": ["build", "out", "obj", "bin", "lib", "lib64", "dist", "docs", "test-output"],
        "c++": ["build", "out", "obj", "bin", "lib", "lib64", "dist", "docs", "test-output"],
        "c#": ["bin", "obj", "packages", "node_modules", "dist", "out", "lib", "test-output"],
        "java": [".idea", "target", ".gradle", "out", ".settings", "build", "eclipse", "nbproject", "logs", "tmp"],
        "typescript": ["node_modules", "dist", ".cache", "temp", "tmp", "build", "out", "lib", "coverage", "logs"],
        "javascript": ["node_modules", "dist", ".cache", "temp", "tmp", "build", "out", "lib", "coverage", "logs"],
        "python": [
            "__pycache__",
            ".pytest_cache",
            "env",
            ".env",
            "venv",
            ".venv",
            "dist",
            "build",
            "migrations",
            "pyvenv",
            "envs",
            "site-packages",
            ".mypy_cache",
            ".tox",
            ".coverage",
            "htmlcov",
            "instance",
            "docs/_build",
        ],
        "ruby": ["vendor", ".bundle", "log", "tmp", "coverage", "spec/tmp", "node_modules", "bundler", "pkg", "tmp/capybara"],
        "go": ["bin", "pkg", "vendor", ".cache", "Godeps", "build", "out", "obj", "test-output"],
        "rust": ["target", ".cargo", "Cargo.lock", "build", "out", "obj", "doc"],
        "php": ["vendor", "composer.lock", "node_modules", "build", "out", "obj", "docs", "cache"],
        "swift": [".build", ".swiftpm", "Packages", "Pods", "Podfile.lock", "DerivedData", "build", "out", "obj", "Certificates"],
        "kotlin": ["build", ".gradle", ".idea", "out", "generated", "kotlin", "tmp"],
        "dart": [".dart_tool", "build", "pubspec.lock", "out", "obj", "bin"],
        "elixir": ["_build", "deps", "mix.lock", "build", "out", "obj"],
        "haskell": ["dist-newstyle", ".stack-work", "*.hi", "*.o", "build", "out"],
        "html": ["dist", "build", "out", "node_modules", "vendor", "public"],
        "vue.js": ["node_modules", "dist", "build", "out", "coverage", "public", "temp", "tmp"],
        "angular": ["node_modules", "dist", "build", "out", "coverage", "temp", "tmp"],
        "react": ["node_modules", "dist", "build", "out", "coverage", "public", "temp", "tmp"],
        "laravel": ["vendor", "node_modules", "public/storage", "storage/*.key", "build", "out", "coverage"],
        "symfony": ["vendor", "node_modules", "var/cache", "var/logs", "build", "out", "coverage"],
        "asp.net": ["bin", "obj", "packages", "node_modules", "wwwroot", "www", "out", "dist", "logs"],
        "scala": ["target", "lib_managed", "src_managed", "out", "dist", "logs", "build"],
        "perl": ["blib", "build", "out", "dist", "logs"],
        "lua": [".luarocks", "luacache", "out", "dist"],
        "r": ["*.Rproj.user", "renv", "packrat", "out", "dist", "build"],
        "shell": ["temp", "tmp", "out", "logs"],
        "objective-c": ["build", "DerivedData", "out", "obj", "logs"],
        "tex": ["*.aux", "*.log", "*.toc", "build", "out"],
        "docker": ["node_modules", "dist", "build", "out", "logs", "temp", "tmp"],
        "flutter": ["build", "out", "ios/Pods", "android/build", "ios/Flutter", "node_modules"],
        "json": []
    }

    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.tree_files = {}
        self.commit = ""
        self.detector = OSEnvironmentDetector()
        self.normalized_path = {}
        self.ignore_file_cache = {}
        
        try:
            self.main_language = self.detect_language()
            # parts = repo_path.split('/')
            # self.project_name = parts[-1]
            self.project_name = os.path.basename(repo_path.rstrip("/"))
            need_add_all_files = False
            try:
                # check if .zinley folder exists
                if not os.path.exists(os.path.join(self.repo_path, ".zinley")):
                    # create .zinley folder
                    os.makedirs(os.path.join(self.repo_path, ".zinley"), exist_ok=True)
                    need_add_all_files = True

                # init git repo
                self.repo = git.Repo(repo_path, odbt=git.GitDB)
                self.root = utils.safe_abs_path(self.repo.working_tree_dir)

                if need_add_all_files:
                    try:
                        self.ignore_default_files()
                        self.add_all_files("Zinley initialization")
                    except Exception as e:
                        logger.error(f"Error during initialization: {str(e)}")
                        if str(e) == "'gitignore'":
                            # Try to create an empty .gitignore file
                            try:
                                with open(os.path.join(self.root, ".gitignore"), "w") as f:
                                    pass
                                logger.info("Created empty .gitignore file")
                            except Exception as file_e:
                                logger.error(f"Failed to create .gitignore file: {str(file_e)}")

            except git.InvalidGitRepositoryError:
                # show message for user to init git repo, promp user to init if user choose yes
                logger.info(
                    f"#### This looks like a brand new project. `SnowX` will try to initialize the setup process.\n"
                )
                # init git repo
                self.repo = git.Repo.init(repo_path)
                self.root = utils.safe_abs_path(self.repo.working_tree_dir)
                try:
                    self.ignore_default_files()
                    self.add_all_files("Zinley initialization")
                except Exception as e:
                    logger.error(f"Error during git initialization: {str(e)}")
                    if str(e) == "'gitignore'":
                        # Try to create an empty .gitignore file
                        try:
                            with open(os.path.join(self.root, ".gitignore"), "w") as f:
                                pass
                            logger.info("Created empty .gitignore file")
                        except Exception as file_e:
                            logger.error(f"Failed to create .gitignore file: {str(file_e)}")

                logger.info(
                    f"#### `SnowX` has successfully initialized it. Feel free to start chatting with me!\n"
                )
        except Exception as e:
            logger.error(f"Error in GitRepo initialization: {str(e)}")
            # Set default values for critical attributes
            self.main_language = "Unknown"
            self.project_name = os.path.basename(repo_path.rstrip("/"))
            self.repo = None
            self.root = repo_path

    def return_os(self):
        return self.detector.get_all_info()

    def set_commit(self, commit):
        self.commit = commit

    def get_commit(self):
        return self.commit

    def get_repo_path(self):
        return self.repo_path

    def get_project_name(self):
        return self.project_name

    def ignore_default_files(self):
        # ignore default files by loop through IGNORED_DIRECTORIES with lang
        try:
            for path in self.IGNORED_DIRECTORIES["default"]:
                try:
                    self.ignored_file_update_gitignore(path)
                except Exception as e:
                    logger.error(f"Error ignoring default file {path}: {str(e)}")

            # check self.main_language != None
            if self.main_language != None and self.main_language != "Unknown":
                if self.main_language in self.IGNORED_DIRECTORIES:
                    for path in self.IGNORED_DIRECTORIES[self.main_language]:
                        try:
                            self.ignored_file_update_gitignore(path)
                        except Exception as e:
                            logger.error(f"Error ignoring language-specific file {path}: {str(e)}")
        except Exception as e:
            logger.error(f"Error in ignore_default_files: {str(e)}")

    def create_ignore_file_from_cache(self):
        # create gitignore file
        try:
            if not hasattr(self, 'root') or not self.root:
                logger.error("Root directory not properly set when creating .gitignore from cache")
                return
                
            if not self.ignore_file_cache:
                logger.debug("No ignore patterns to write to .gitignore")
                return
                
            gitignore_path = os.path.join(self.root, ".gitignore")
            with open(gitignore_path, "w") as f:
                # write all file in self.ignore_file_cache to file
                f.write("\n".join(self.ignore_file_cache.keys()))
            logger.debug(f"Created .gitignore with {len(self.ignore_file_cache)} patterns")
        except Exception as e:
            logger.error(f"Failed to create .gitignore file: {str(e)}")

    def append_ignore_file(self, fname):
        # open file .gitignore and write fname to end of file
        try:
            if not hasattr(self, 'root') or not self.root:
                logger.error("Root directory not properly set when appending to .gitignore")
                return
                
            gitignore_path = os.path.join(self.root, ".gitignore")
            with open(gitignore_path, "a") as f:
                f.write(f"{fname}\n")
            logger.debug(f"Added {fname} to .gitignore")
        except FileNotFoundError:
            # Create the .gitignore file if it doesn't exist
            try:
                if not hasattr(self, 'root') or not self.root:
                    logger.error("Root directory not properly set when creating .gitignore")
                    return
                    
                gitignore_path = os.path.join(self.root, ".gitignore")
                with open(gitignore_path, "w") as f:
                    f.write(f"{fname}\n")
                logger.debug(f"Created .gitignore with {fname}")
            except Exception as inner_e:
                logger.error(f"Failed to create .gitignore file: {str(inner_e)}")
        except Exception as e:
            logger.error(f"Failed to update .gitignore: {str(e)}")

    def add_all_files(self, commit):
        if not self.repo:
            return
        try:
            self.repo.git.add(all=True)
            if self.repo.is_dirty() or self.repo.untracked_files:
                self.repo.git.commit(m=commit)
            else:
                logger.debug("No changes to commit. Working tree is clean.")
        except git.exc.GitCommandError as e:
            logger.error(f"Git operation failed: {str(e)}")

    def get_rel_repo_dir(self):
        try:
            return os.path.relpath(self.repo.git_dir, os.getcwd())
        except ValueError:
            return self.repo.git_dir

    def read_file_content(self, fname):
        # get file content from fname
        with open(os.path.join(self.root, fname), "r") as f:
            content = f.read()
        return content

    def get_tracked_files(self):
        if not self.repo:
            return []
        try:
            commit = self.repo.head.commit
        except ValueError:
            commit = None

        files = set()
        if commit:
            if commit in self.tree_files:
                files = self.tree_files[commit]
            else:
                for blob in commit.tree.traverse():
                    if blob.type == "blob":  # blob is a file
                        files.add(blob.path)
                files = set(self.normalize_path(path) for path in files)
                self.tree_files[commit] = set(files)

        # Add staged files
        index = self.repo.index
        staged_files = [path for path, _ in index.entries.keys()]
        files.update(self.normalize_path(path) for path in staged_files)

        res = [fname for fname in files if not self.ignored_file(fname)]

        return res

    def normalize_path(self, path):
        orig_path = path
        res = self.normalized_path.get(orig_path)
        if res:
            return res

        path = str(Path(PurePosixPath((Path(self.root) / path).relative_to(self.root))))
        self.normalized_path[orig_path] = path
        return path

    def get_updated_files(self):
        status = self.repo.git.status(porcelain=True)

        updated_files = []
        for line in status.splitlines():
            # Check for modified files (M) or new files (A)
            # if line.startswith(' M') or line.startswith('A '):
            # Extract the file path
            updated_files.append(line[3:])
        return updated_files

    def get_head(self):
        try:
            return self.repo.head.commit.hexsha
        except ValueError:
            return None

    def abs_root_path(self, path):
        res = Path(self.root) / path
        return utils.safe_abs_path(res)

    def zinley_path(self):
        res = Path(self.root) / ".zinley"
        return utils.safe_abs_path(res)

    def ignored_file(self, fname):
        if fname in self.ignore_file_cache:
            return self.ignore_file_cache[fname]

        result = self.ignored_file_raw(fname)
        self.ignore_file_cache[fname] = result

        return result

    def ignored_file_update_gitignore(self, fname):
        try:
            if not hasattr(self, 'root') or not self.root:
                logger.error("Root directory not properly set")
                return False
                
            if fname in self.ignore_file_cache:
                return self.ignore_file_cache[fname]

            result = self.ignored_file_raw(fname)
            self.ignore_file_cache[fname] = result

            self.append_ignore_file(fname)
            return result
        except Exception as e:
            logger.error(f"Error in ignored_file_update_gitignore for {fname}: {str(e)}")
            return False

    def ignored_file_raw(self, fname):
        # Check if the file/directory name should be ignored
        base_name = os.path.basename(fname)
        dir_name = os.path.dirname(fname)
        
        # Check against the IGNORED_DIRECTORIES list
        ignore_list = self.IGNORED_DIRECTORIES["default"]
        if self.main_language and self.main_language != "Unknown":
            if self.main_language in self.IGNORED_DIRECTORIES:
                ignore_list += self.IGNORED_DIRECTORIES[self.main_language]
                
        for pattern in ignore_list:
            if fnmatch.fnmatch(base_name, pattern) or fnmatch.fnmatch(fname, pattern):
                return True
                
        # Also check if any parent directory should be ignored
        if dir_name:
            parts = Path(dir_name).parts
            for part in parts:
                if any(fnmatch.fnmatch(part, pattern) for pattern in ignore_list):
                    return True
                    
        return False

    def reset_previous_commit(self):
        previous_commit = self.repo.head.commit.parents[0]
        self.repo.git.reset("--soft", previous_commit)
        print(f"Reset to previous commit: {previous_commit.hexsha}")

    def print_tree(self):
        ignore = self.IGNORED_DIRECTORIES["default"]
        if self.main_language != None and self.main_language != "Unknown":
            ignore += self.IGNORED_DIRECTORIES[self.main_language]
        output_capture = io.StringIO()
        sys.stdout = output_capture
        t = Tree()
        t.walk(self.repo_path, exclude=ignore, stdout=sys.stdout)
        sys.stdout = sys.__stdout__
        combined_output = output_capture.getvalue() + t.summary()
        return combined_output


    def detect_language(self):
        # Counter to store occurrences of each language
        lang_counter = Counter()
        try:
            files = os.listdir(self.repo_path)
            for file in files:
                # Skip common non-code files and directories
                if (self.ignored_file_raw(file) or 
                    file == '.gitignore' or 
                    file.endswith(('.md', '.txt', '.json', '.yml', '.yaml', '.toml', '.ini', '.cfg', '.config')) or
                    file.startswith(('.', '_')) or
                    os.path.isdir(os.path.join(self.repo_path, file))):
                    continue
                    
                lang = filename_to_lang(file)
                lang_counter[lang] += 1

            if lang_counter:
                if lang_counter.most_common(1)[0][0] != None:
                    return lang_counter.most_common(1)[0][0]
                else:
                    return lang_counter.most_common(2)[1][0]
            else:
                return "Unknown"
        except Exception as e:
            return "Unknown"

    def print_summarize(self):
        try:
            io = InputOutput()
            rm = RepoMap(root=self.repo_path, io=io)

            files = self.get_tracked_files()
            if not files:
                return "No tracked files found"

            fnames = [os.path.join(self.repo_path, file) for file in files]
            return rm.get_ranked_tags_map(set(), fnames)
        except Exception as e:
            logger.debug(f"Error generating summary: {str(e)}")
            return "Error getting repository summary"

    def print_summarize_with_tree(self):
        tree = self.print_tree()
        summarize = self.print_summarize()
        return tree + "\n" + summarize

    def deploy_to_server(self, path, domain=DEFAULT_DOMAIN, subdomain=DEFAULT_DOMAIN, project_type=""):
        try:
            logger.debug(f"Starting deployment for path: {path}")
            logger.debug(f"Domain: {domain}, Subdomain: {subdomain}, Project Type: {project_type}")
            
            # Zip all files in repo and upload to S3
            logger.debug("Zipping files and uploading to S3...")
            s3_key = deploy_zip_to_s3(path)
            logger.debug(f"Files uploaded to S3 with key: {s3_key}")

            # Construct the full S3 URI
            s3_uri = f"s3://zinley/{s3_key}"
            logger.debug(f"Constructed S3 URI: {s3_uri}")

            # Send message to SQS
            logger.debug("Preparing to send deployment message to SQS...")
            action = "deploy"
            type = "web"  # Assuming it's a web deployment, adjust if needed
            response = send_message_to_sqs(action, type, s3_uri, domain, subdomain, project_type)
            logger.debug(f"SQS message parameters - Action: {action}, Type: {type}")

            if response.get('MessageId'):
                logger.debug(f"Deployment message successfully sent to SQS. MessageId: {response['MessageId']}")
                logger.debug(f"Deployment message sent to SQS. MessageId: {response['MessageId']}")
            else:
                logger.debug("Message sent to SQS but no MessageId received")
                logger.debug("Message sent to SQS, but no MessageId was returned.")

            return s3_uri

        except Exception as e:
            logger.error(f"An error occurred during deployment: {str(e)}")
            logger.debug(f"Deployment failed with exception: {str(e)}")
            return None
