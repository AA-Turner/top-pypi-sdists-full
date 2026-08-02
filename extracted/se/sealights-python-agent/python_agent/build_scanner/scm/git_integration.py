import logging
import os
import subprocess

isGitAvailable = False


def is_git_available():
    try:
        subprocess.run(
            ["git", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


# Import Git module conditionally
if is_git_available():
    from git import Repo

    isGitAvailable = True
else:
    isGitAvailable = False

from python_agent.build_scanner.scm.scm_info import (
    ScmInfo,
    ContributorData,
    CommitLogData,
)
from python_agent.common import constants
from python_agent.utils import to_str_dict, to_str_obj_one_line

log = logging.getLogger(__name__)


class CommitRecord(object):
    def __init__(self, raw_values):
        self.hexsha = raw_values[0]
        self.author_name = raw_values[1]
        self.author_email = raw_values[2]
        self.author_date = int(raw_values[3])
        self.committer_date = int(raw_values[4])
        self.message = raw_values[5]

    def __str__(self):
        return "CommitRecord(%s)" % to_str_obj_one_line(self)


class FileCommitsMap(object):
    def __init__(self):
        self.data = dict()

    def add_commit(self, file_name, commit_index):
        commits = []
        if file_name in self.data:
            # File name already exists
            commits = self.data[file_name]
            if commit_index in commits:
                # Commit index already exists for a file
                return
        commits.append(commit_index)
        self.data[file_name] = commits

    def __len__(self):
        return len(self.data)

    def __contains__(self, item):
        return item in self.data

    def __getitem__(self, item):
        return self.data[item]


class GitIntegration(object):
    """
    Implements filling of scm info from git repository
    """

    def __init__(self, config_data, scanned_files=dict()):
        self.repo_folder = None
        self.config_data = config_data
        self.scanned_files = scanned_files
        self.file_commits = FileCommitsMap()
        self.recent_commits = list()

    def get_repo(self):
        if self.repo_folder:
            return Repo(self.repo_folder)

        try:
            repo = None or Repo(search_parent_directories=True)
            if repo:
                self.repo_folder = os.path.dirname(repo.git_dir)
            return repo
        except Exception as e:
            log.error("Failed to load git repository. Error:%s" % (str(e)))
            return None

    def collect_scm_info(self):
        scm_info = ScmInfo()
        if not isGitAvailable:
            log.info(
                "Git executable not found. Git-related functionalities will be disabled."
            )
            return scm_info

        if self.config_data.scmType != constants.GIT_SCM:
            log.info("SCM type is not git; SCM data was not collected")
            return scm_info
        try:
            repo = self.get_repo()
            if repo:
                scm_info = self.collect_from_git_log()
                if scm_info:
                    scm_info.scm_type = constants.GIT_SCM
                    scm_info.repo_url = repo.remotes.origin.url
                    if len(scm_info.commit_history) > 0:
                        scm_info.head_commit = scm_info.commit_history[0]
                    if (len(self.scanned_files)) > 0:
                        self.fill_scanned_files_commits()
                    log.debug("Collected %s" % scm_info)
            else:
                log.warning("Failed to collect git info:repository was not found")

        except Exception as e:
            log.error("Failed to collect git info. Error:%s" % (str(e)))

        return scm_info

    def collect_from_git_log(self):
        """
        Collects scm_info by parsing the raw output of 'git log ...' command
        :return: scm_info - filled by data from git repository or empty scm_info
        if exception/error happened
        """
        try:
            scm_info = ScmInfo()
            if not is_git_available():
                log.info(
                    "Git executable not found. Git-related functionalities will be disabled."
                )
                return scm_info
            raw_output = self.call_git_log()
            commit_index = -1
            scm_info.commit_history = list()
            scm_info.commit_log = list()
            scm_info.contributors = list()
            for raw_line in raw_output:
                """ 
                raw git log output contains lines of different format and empty lines
                for example:
                '5ec9309567b488a19b702e396fe0f084d1c9d4bd$$$alasch2$$$ala.schneider@sealights.io$$$1521053029$$$1521053029$$$Removed unused backend_proxy'

                M       python_agent/build_scanner/executors/build.py
                """
                if self.try_parse_commit_line(raw_line, scm_info):
                    # the raw line was recognized as a commit line and was parsed
                    commit_index += 1
                    continue
                if len(raw_line) == 0:
                    # the raw_line is an empty line - just skip it
                    continue
                # try to recognize the raw_line as file difference line
                self.try_parse_file_diff_line(raw_line, commit_index)

            return scm_info

        except Exception as e:
            log.exception("Failed to collect git info. Error:%s" % (str(e)))
            return None

    def call_git_log(self):
        """
        Executes git command for getting recent commits data
        :param git_path: path to git
        :return: git output as array of lines
        """
        log_format = "--format='%H$$$%an$$$%ae$$$%at$$$%ct$$$%s'"
        git_args = [
            "git",
            "log",
            log_format,
            "--name-status",
            "-" + str(self.config_data.commitHistoryLength),
        ]
        raw_output = (
            subprocess.Popen(git_args, stdout=subprocess.PIPE)
            .communicate()[0]
            .decode("utf-8")
            .split("\n")
        )
        return raw_output[:-1]

    def try_parse_commit_line(self, raw_line, scm_info):
        # strip wrapping by " return by git log
        raw_line = raw_line[1:-1]
        raw_values = raw_line.split("$$$")
        if len(raw_values) != 6:
            return False

        cr = CommitRecord(raw_values)
        scm_info.commit_history.append(cr.hexsha)
        contributor_data = ContributorData(cr.author_name, cr.author_email)
        if contributor_data not in scm_info.contributors:
            scm_info.contributors.append(contributor_data)
        contrib_index = scm_info.contributors.index(contributor_data)
        scm_info.commit_log.append(
            CommitLogData(
                cr.hexsha, cr.author_date, cr.committer_date, cr.message, contrib_index
            )
        )
        return True

    def try_parse_file_diff_line(self, raw_line, commit_index):
        raw_values = raw_line.split()
        """
        File diff line contains 2 columns in case of add/delete/modify like the following:
        M       path/to/someFile.py
        File diff line has 3 columns if a file was renamed like the following:
        R001 path/to/oldName.py path/to/newName.py
        In that case both old and new files commits are collected
        """
        if len(raw_values) != 2 and len(raw_values) != 3:
            log.debug("Ignored unrecognized line:[%s]" % raw_line)
            return False

        self.file_commits.add_commit(raw_values[1], commit_index)
        if len(raw_values) == 3:
            self.file_commits.add_commit(raw_values[2], commit_index)
        return True

    def fill_scanned_files_commits(self):
        for k in self.scanned_files:
            # git path separator may differ from physical path, normalize it
            git_file_lookup = os.path.relpath(k, self.repo_folder).replace("\\", "/")
            if git_file_lookup in self.file_commits:
                self.scanned_files[k].commitIndexes = self.file_commits[git_file_lookup]
        log.debug(to_str_dict("Scanned files with commits", self.scanned_files))

    @staticmethod
    def to_str_repo(repo):
        str_repo = "Git info:\n|t{}\n".format(repo.description)
        str_repo += "\tActive branch: {}\n".format(repo.active_branch)
        str_repo += "\tRemotes:\n"
        for remote in repo.remotes:
            str_repo += '\t\tname:"{}",URL:"{}",head commit:{}\n'.format(
                remote, remote.url, str(repo.head.commit.hexsha)
            )
        return str_repo
