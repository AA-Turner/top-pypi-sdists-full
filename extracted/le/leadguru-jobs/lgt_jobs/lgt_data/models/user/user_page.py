from typing import List

from lgt_jobs.lgt_data.models.user.user import UserModel


class UsersPage:
    users: List[UserModel]
    count: int = 0

    def __init__(self, users: List[UserModel], count: int):
        self.users = users
        self.count = count

    @staticmethod
    def from_dic(dic: dict):
        users = [UserModel.from_dic(doc) for doc in dic.get('page', [])]
        count = dic.get('count', 0)
        return UsersPage(users=users, count=count)
    