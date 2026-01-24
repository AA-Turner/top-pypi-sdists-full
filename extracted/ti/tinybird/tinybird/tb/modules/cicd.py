from enum import Enum
from os import getcwd
from pathlib import Path
from typing import Any, Dict, List, Optional, Type, Union

import click
from tornado.template import Template

from tinybird.tb.modules.feedback_manager import FeedbackManager


class Provider(Enum):
    GitHub = 0
    GitLab = 1


WORKFLOW_VERSION = "v0.0.1"

GITHUB_CI_YML = """
name: Tinybird - CI Workflow

on:
  workflow_dispatch:
  pull_request:
    branches:
      - main
      - master
    types: [opened, reopened, labeled, unlabeled, synchronize]{% if data_project_dir != '.' %}
    paths:
      - '{{ data_project_dir }}/**'{% end %}

concurrency: ${{! github.workflow }}-${{! github.event.pull_request.number }}

env:
  TINYBIRD_HOST: ${{! secrets.TINYBIRD_HOST }}
  TINYBIRD_TOKEN: ${{! secrets.TINYBIRD_TOKEN }}

jobs:
  ci:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: '{{ data_project_dir }}'
    services:
      tinybird:
        image: tinybirdco/tinybird-local:latest
        ports:
          - 7181:7181
    steps:
      - uses: actions/checkout@v3
      - name: Install Tinybird CLI
        run: curl https://tinybird.co | sh
      - name: Build project
        run: tb build
      - name: Test project
        run: tb test run
      - name: Deployment check
        run: tb --cloud --host ${{! env.TINYBIRD_HOST }} --token ${{! env.TINYBIRD_TOKEN }} deploy --check
"""

GITHUB_CD_YML = """
name: Tinybird - CD Workflow

on:
  push:
    branches:
      - main
      - master{% if data_project_dir != '.' %}
    paths:
      - '{{ data_project_dir }}/**'{% end %}

concurrency: ${{! github.workflow }}-${{! github.event.ref }}

env:
  TINYBIRD_HOST: ${{! secrets.TINYBIRD_HOST }}
  TINYBIRD_TOKEN: ${{! secrets.TINYBIRD_TOKEN }}

jobs:
  cd:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install Tinybird CLI
        run: curl https://tinybird.co | sh
      - name: Deploy project
        run: tb --cloud --host ${{! env.TINYBIRD_HOST }} --token ${{! env.TINYBIRD_TOKEN }} deploy
"""

GITLAB_YML = """
include:
  - local: .gitlab/tinybird/*.yml

stages:
  - tests
  - deploy
"""


GITLAB_CI_YML = """
tinybird_ci_workflow:
  image: ubuntu:latest
  stage: tests
  interruptible: true
  needs: []
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      changes:
        - .gitlab/tinybird/*{% if data_project_dir != '.' %}
        - {{ data_project_dir }}/*
        - {{ data_project_dir }}/**/*{% end %}
  before_script:
    - apt update && apt install -y curl
    - curl https://tinybird.co | sh
    - for i in {1..10}; do curl -s -o /dev/null "http://$TB_LOCAL_HOST" && break; sleep 5; done
  script:
    - export PATH="$HOME/.local/bin:$PATH"
    - cd $CI_PROJECT_DIR/{{ data_project_dir }}
    - tb build
    - tb test run
    - tb --cloud --host "$TINYBIRD_HOST" --token "$TINYBIRD_TOKEN" deploy --check
  services:
    - name: tinybirdco/tinybird-local:latest
      alias: tinybird-local
  variables:
    TB_LOCAL_HOST: tinybird-local
"""

GITLAB_CD_YML = """
tinybird_cd_workflow:
  image: ubuntu:latest
  stage: deploy
  resource_group: production
  needs: []
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      changes:
        - .gitlab/tinybird/*{% if data_project_dir != '.' %}
        - {{ data_project_dir }}/*
        - {{ data_project_dir }}/**/*{% end %}
  before_script:
    - apt update && apt install -y curl
    - curl https://tinybird.co | sh
  script:
    - export PATH="$HOME/.local/bin:$PATH"
    - cd $CI_PROJECT_DIR/{{ data_project_dir }}
    - tb --cloud --host "$TINYBIRD_HOST" --token "$TINYBIRD_TOKEN" deploy
"""


class CICDFile:
    def __init__(
        self,
        template: str,
        file_name: str,
        dir_path: Optional[str] = None,
        warning_message: Optional[str] = None,
    ):
        self.template = template
        self.file_name = file_name
        self.dir_path = dir_path
        self.warning_message = warning_message

    @property
    def full_path(self) -> str:
        return f"{self.dir_path}/{self.file_name}" if self.dir_path else self.file_name


class CICDGeneratorBase:
    cicd_files: List[CICDFile] = []

    def __call__(self, path: str, params: Dict[str, Any]):
        for cicd_file in self.cicd_files:
            if cicd_file.dir_path:
                Path(f"{path}/{cicd_file.dir_path}").mkdir(parents=True, exist_ok=True)
            content = Template(cicd_file.template).generate(**params)
            if Path(f"{path}/{cicd_file.full_path}").exists():
                continue
            with open(f"{path}/{cicd_file.full_path}", "wb") as f:
                f.write(content)
            click.echo(FeedbackManager.info_file_created(file=cicd_file.full_path.replace("./.", ".")))
            if cicd_file.warning_message is not None:
                return FeedbackManager.warning_for_cicd_file(
                    file_name=cicd_file.file_name, warning_message=cicd_file.warning_message.format(**params)
                )

    def is_already_generated(self, path: str) -> bool:
        for cicd_file in self.cicd_files:
            if cicd_file.file_name and Path(f"{path}/{cicd_file.full_path}").exists():
                return True
        return False

    @classmethod
    def build_generator(cls, provider: str) -> Union["GitHubCICDGenerator", "GitLabCICDGenerator"]:
        builder: Dict[str, Union[Type[GitHubCICDGenerator], Type[GitLabCICDGenerator]]] = {
            Provider.GitHub.name: GitHubCICDGenerator,
            Provider.GitLab.name: GitLabCICDGenerator,
        }
        return builder[provider]()


class GitHubCICDGenerator(CICDGeneratorBase):
    cicd_files = [
        CICDFile(
            template=GITHUB_CI_YML,
            file_name="tinybird-ci.yml",
            dir_path=".github/workflows",
        ),
        CICDFile(
            template=GITHUB_CD_YML,
            file_name="tinybird-cd.yml",
            dir_path=".github/workflows",
        ),
    ]


class GitLabCICDGenerator(CICDGeneratorBase):
    cicd_files = [
        CICDFile(
            template=GITLAB_YML,
            file_name=".gitlab-ci.yml",
            dir_path=".",
        ),
        CICDFile(
            template=GITLAB_CI_YML,
            file_name="tinybird-ci.yml",
            dir_path=".gitlab/tinybird",
        ),
        CICDFile(
            template=GITLAB_CD_YML,
            file_name="tinybird-cd.yml",
            dir_path=".gitlab/tinybird",
        ),
    ]


def init_cicd(
    path: Optional[str] = None,
    data_project_dir: Optional[str] = None,
):
    for provider in Provider:
        path = path if path else getcwd()
        data_project_dir = data_project_dir if data_project_dir else "."
        generator = CICDGeneratorBase.build_generator(provider.name)
        params = {
            "data_project_dir": data_project_dir,
            "workflow_version": WORKFLOW_VERSION,
        }
        warning_message = generator(path, params)
        if warning_message:
            click.echo(warning_message)


def check_cicd_exists(path: Optional[str] = None) -> Optional[Provider]:
    path = path if path else getcwd()
    for provider in Provider:
        generator = CICDGeneratorBase.build_generator(provider.name)
        if generator.is_already_generated(path):
            return provider
    return None
