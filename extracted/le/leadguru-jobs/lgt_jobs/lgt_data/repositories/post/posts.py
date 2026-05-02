from bson import ObjectId

from lgt_jobs.lgt_data.models.post.post import Post
from lgt_jobs.lgt_data.mongo_repository import BaseMongoRepository


class PostsRepository(BaseMongoRepository):
    collection_name = 'posts'

    def get_users_posts(self, ids: list[str]) -> dict[ObjectId, list[Post]]:
        pipeline = [
            {
                '$lookup': {
                    'from': 'posted_messages',
                    'as': 'messages',
                    'let': {'id': '$_id'},
                    'pipeline': [
                        {'$match': {'$expr': {'$and': [{'$in': ['$id', ids]}, {'$eq': ['$$id', '$post_id']}]}}}
                    ]}},
            {
                '$match': {'messages': {'$ne': []}}
            },
            {
                '$group': {'_id': '$user_id', 'posts': {'$push': '$$ROOT'}}
            }]
        docs = self.collection().aggregate(pipeline)
        posts_map = {doc['_id']: [Post.from_dic(post) for post in doc['posts']] for doc in docs}
        return posts_map
