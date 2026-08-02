from python_agent.utils import to_str_list, to_str_obj_one_line
from python_agent.common import constants


class ScmInfo(object):
    def __init__(self):
        self.scm_type = constants.NONE_SCM
        self.head_commit = None
        self.commit_history = None
        self.commit_log = None
        self.contributors = None
        self.repo_url = None

    def __str__(self):
        to_str = "SCM Info:\n"
        to_str += "scm_type=%s," % self.scm_type
        to_str += "head_commit=%s" % self.head_commit
        to_str += "\n"
        to_str += to_str_list("commit_history", self.commit_history)
        to_str += "\n"
        to_str += to_str_list("commit_log", self.commit_log)
        to_str += "\n"
        to_str += to_str_list("contributors", self.contributors)
        return to_str


class ContributorData(object):
    def __init__(self, name, email):
        self.contributorName = name
        self.contributorEmail = email

    def __eq__(self, other):
        if isinstance(other, ContributorData):
            return (self.contributorName == other.contributorName) and (
                self.contributorEmail == other.contributorEmail
            )
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__repr__())

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "ContributorData" + to_str_obj_one_line(self)


class Contributors(object):
    def __init__(self, commits):
        self.contrib_data = []
        self.init_contrib_data(commits)

    def init_contrib_data(self, commits):
        """
        Receives commit log and selects distinctive author name and email from each entry
        :param commits: commits log returned by git
        :return: nothing
        """
        self.contrib_data = [
            cont
            for cont in set(
                [ContributorData(cm.author.name, cm.author.email) for cm in commits]
            )
        ]

    def get_contrib_index(self, contributor):
        return self.contrib_data.index(contributor)

    def __str__(self):
        return to_str_list("contributors", self.contrib_data)


class CommitLogData(object):
    def __init__(self, commit, author_date, committer_date, title, contributor_index):
        self.commit = commit
        self.authorDate = author_date * 1000
        self.committerDate = committer_date * 1000
        self.title = title
        self.contributorIndex = contributor_index

    def __str__(self):
        return to_str_obj_one_line(self)
