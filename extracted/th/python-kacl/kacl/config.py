import os

import yaml


class KACLConfig:
    def __init__(self, config_file=None):
        default_config_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "config", "kacl-default.yml"
        )
        self.__config = {}
        with open(default_config_file, "r") as df:
            self.__config = yaml.safe_load(df)
        if config_file:
            with open(os.path.expanduser(config_file), "r") as f:
                KACLConfig.merge(self.__config, yaml.safe_load(f))

        self.__config = self.__config.get("kacl", {})

        self.allowed_header_titles = self.__config.get("allowed_header_titles")
        self.allowed_version_sections = self.__config.get("allowed_version_sections")
        self.default_content = self.__config.get("default_content")
        self.add_unreleased = self.__config.get("release", {}).get(
            "add_unreleased", True
        )
        self.git_tag_name = self.__config.get("git", {}).get("tag_name")
        self.git_tag_description = self.__config.get("git", {}).get("tag_description")
        self.changelog_file_path = self.__config.get("file")
        self.git_create_tag = self.__config.get("git", {}).get("tag")
        self.git_create_commit = self.__config.get("git", {}).get("commit")
        self.git_commit_message = self.__config.get("git", {}).get("commit_message")
        self.git_commit_additional_files = self.__config.get("git", {}).get(
            "commit_additional_files"
        )
        self.link_auto_generate = self.__config.get("links", {}).get("auto_generate")
        self.link_host_url = self.__config.get("links", {}).get("host_url")
        self.links_compare_versions_template = self.__config.get("links", {}).get(
            "compare_versions_template"
        )
        self.links_unreleased_changes_template = self.__config.get("links", {}).get(
            "unreleased_changes_template"
        )
        self.links_initial_version_template = self.__config.get("links", {}).get(
            "initial_version_template"
        )
        self.post_release_version_prefix = self.__config.get("extension", {}).get(
            "post_release_version_prefix"
        )

        # issue tracker config
        self.issue_tracker_jira_host = (
            self.__config.get("issue_tracker", {}).get("jira", {}).get("host")
        )
        self.issue_tracker_jira_username = (
            self.__config.get("issue_tracker", {}).get("jira", {}).get("username")
        )
        self.issue_tracker_jira_password = (
            self.__config.get("issue_tracker", {}).get("jira", {}).get("password")
        )
        self.issue_tracker_jira_issue_patterns = (
            self.__config.get("issue_tracker", {})
            .get("jira", {})
            .get("issue_patterns", [])
        )
        self.issue_tracker_jira_comment_template = (
            self.__config.get("issue_tracker", {})
            .get("jira", {})
            .get("comment_template")
        )

        if not self.issue_tracker_jira_host:
            self.issue_tracker_jira_host = os.getenv("JIRA_HOST", None)
        if not self.issue_tracker_jira_username:
            self.issue_tracker_jira_username = os.getenv("JIRA_USERNAME", None)
        if not self.issue_tracker_jira_password:
            self.issue_tracker_jira_password = os.getenv("JIRA_PASSWORD", None)

        self.stash_dir = self.__config.get("stash", {}).get("dir", ".kacl_stash")
        self.stash_always = self.__config.get("stash", {}).get("always", False)

    @staticmethod
    def merge(a, b, path=None):
        """merge two dictionaries
        :param a: dictionary the values will be merged into
        :param b: dictionary the values will be used when overwriting values
        :param path:
        :return:
        """
        if path is None:
            path = []
        for key in b:
            if key in a:
                if isinstance(a[key], dict) and isinstance(b[key], dict):
                    KACLConfig.merge(a[key], b[key], path + [str(key)])
                elif a[key] == b[key]:
                    pass  # same leaf value
                else:
                    a[key] = b[key]

            else:
                a[key] = b[key]
        return a
