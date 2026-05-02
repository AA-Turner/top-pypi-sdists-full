import os
from collections import OrderedDict
from datetime import datetime, UTC, timedelta
from typing import List, Optional

import pymongo
from bson.objectid import ObjectId
from dateutil import tz
from pymongo import MongoClient, UpdateOne

from lgt_jobs.lgt_data.enums import SourceType
from lgt_jobs.lgt_data.models.base import BaseModel
from lgt_jobs.lgt_data.models.boards.board import BoardModel
from lgt_jobs.lgt_data.models.boards.status import BoardedStatus
from lgt_jobs.lgt_data.models.bots.dedicated_bot import DedicatedBotModel
from lgt_jobs.lgt_data.models.chat.grouped_messages import GroupedMessagesModel
from lgt_jobs.lgt_data.models.chat.message import ChatMessage
from lgt_jobs.lgt_data.models.chat.request import MessageRequest
from lgt_jobs.lgt_data.models.chat.scheduled_message import ScheduledMessage
from lgt_jobs.lgt_data.models.contacts.contact import UserContact
from lgt_jobs.lgt_data.models.leads.extended_lead import ExtendedLeadModel
from lgt_jobs.lgt_data.models.leads.lead import LeadModel
from lgt_jobs.lgt_data.models.people.people import SlackMemberInformation
from lgt_jobs.lgt_data.models.templates.template import UserTemplateModel
from lgt_jobs.lgt_data.models.user.reset_password import UserResetPasswordModel
from lgt_jobs.lgt_data.models.user.subscription import Subscription
from lgt_jobs.lgt_data.models.user.user import UserModel
from lgt_jobs.lgt_data.models.user.user_follow_ups import UserFollowUps
from lgt_jobs.lgt_data.models.user.user_page import UsersPage
from lgt_jobs.lgt_data.models.user.verification import UserVerificationModel
from lgt_jobs.lgt_data.models.user_leads.extended_user_lead import ExtendedUserLeadModel
from lgt_jobs.lgt_data.models.user_leads.user_lead import UserLeadModel

client = MongoClient(os.environ.get('MONGO_CONNECTION_STRING', 'mongodb://127.0.0.1:27019/'))


def to_object_id(oid):
    if isinstance(oid, ObjectId):
        return oid
    return ObjectId(oid)


class BaseMongoRepository:
    collection_name = ''
    database_name = 'lgt_admin'
    model: BaseModel = BaseModel()

    def collection(self):
        return client[self.database_name][self.collection_name]

    def _collection(self, collection_name):
        return client[self.database_name][collection_name]

    def insert_many(self, items):
        insert_items = [item.to_dic() for item in items]
        self.collection().insert_many(insert_items)

    def insert(self, item):
        return self.collection().insert_one(item.to_dic())

    def add(self, item):
        return self.insert(item)

    def delete(self, id):
        res = self.collection().delete_one({'_id': to_object_id(id)})
        return res


class UserMongoRepository(BaseMongoRepository):
    collection_name = 'users'
    model = UserModel

    def get_inactive_users(self):
        pipeline = [
            {'$lookup': {'from': 'user_track_action', 'as': 'last_action', 'let': {'id': '$_id'}, 'pipeline':
                [
                    {'$match': {'$expr': {'$eq': ['$user_id', '$$id']}}},
                    {'$sort': {'created_at': -1}},
                    {'$project': {'created_at': 1}},
                    {'$limit': 1}
                ]}},
            {'$addFields': {'last_action_date': {'$first': '$last_action.created_at'}}},
            {'$lookup': {'as': 'subscription', 'from': 'subscriptions', 'foreignField': '_id', 'localField': 'subscription_id'}},
            {'$addFields': {'period': {'$first': '$subscription.disable_bots_period'}}},
            {'$match': {'$expr': {'$lte': ['$last_action_date', {'$dateSubtract': {'startDate': '$$NOW', 'unit': 'day', 'amount': '$period'}}]}}},
            {'$project': {'_id': 1}}]

        return {doc['_id']: None for doc in self.collection().aggregate(pipeline)}

    def get(self, _id):
        return UserModel.from_dic(self.collection().find_one({'_id': to_object_id(_id)}))

    def get_by_email(self, email: str):
        pipeline = {'email': email}
        doc = self.collection().find_one(pipeline)
        return UserModel.from_dic(doc)

    def set(self, _id, **kwargs):
        update_dict = {k: v for k, v in kwargs.items() if v is not None}
        self.collection().update_one({'_id': to_object_id(_id)}, {'$set': update_dict})

    def get_users(self, users_ids=None, include_inactive=False, name=None, **kwargs):
        pipeline = {}

        subscription_expired = kwargs.get('subscription_expired')
        connected_slack_email = kwargs.get('connected_slack_email')
        soon_subscription_expiration = kwargs.get('soon_subscription_expiration')
        has_new_message = kwargs.get('has_new_message')
        has_new_message_request = kwargs.get('has_new_message_request')
        has_deactivated_sources = kwargs.get('has_deactivated_sources')
        has_new_replies = kwargs.get('has_new_replies')
        has_new_reactions = kwargs.get('has_new_reactions')
        min_days = kwargs.get('min_days_soon_subscription_expiration', 3)
        emails = kwargs.get('emails')

        if subscription_expired:
            pipeline['subscription_expired_at'] = {'$lte': datetime.now(UTC)}
            pipeline['subscription_expiration_notified'] = False

        if soon_subscription_expiration:
            pipeline['subscription_expired_at'] = {'$lte': datetime.now(UTC) + timedelta(min_days)}
            pipeline['subscription_expiration_warning_notified'] = False

        if has_new_message:
            pipeline['notification_settings.incoming_messages.enabled'] = True
            pipeline['notification_settings.incoming_messages.need_to_notify'] = True

        if has_new_message_request:
            pipeline['notification_settings.inbox.enabled'] = True
            pipeline['notification_settings.inbox.need_to_notify'] = True

        if has_deactivated_sources:
            pipeline['notification_settings.source_deactivation.enabled'] = True
            pipeline['notification_settings.source_deactivation.need_to_notify'] = True

        if has_new_replies:
            pipeline['notification_settings.bulk_replies.enabled'] = True
            pipeline['notification_settings.bulk_replies.need_to_notify'] = True

        if has_new_reactions:
            pipeline['notification_settings.bulk_reactions.enabled'] = True
            pipeline['notification_settings.bulk_reactions.need_to_notify'] = True

        if connected_slack_email:
            pipeline['slack_users.email'] = connected_slack_email

        if users_ids is not None:
            pipeline['_id'] = {'$in': [to_object_id(_id) for _id in users_ids]}

        if emails is not None:
            pipeline['email'] = {'$in': emails}

        if name is not None:
            pipeline['user_name'] = {"$regex": name, "$options": 'i'}

        if not include_inactive:
            pipeline['inactive'] = False

        return [UserModel.from_dic(doc) for doc in self.collection().find(pipeline)]

    def get_users_page(self, skip: int = 0, limit: int = 50, **kwargs):
        pipeline: list = []
        match_pipeline = {}
        include_inactive = kwargs.get('include_inactive', False)
        email = kwargs.get('email')
        search = kwargs.get('search')
        name = kwargs.get('name')
        sort_field = kwargs.get('sort_field', 'email')
        sort_direction = kwargs.get('sort_direction', 'ASCENDING')
        sort_direction = pymongo.ASCENDING if sort_direction == 'ASCENDING' else pymongo.DESCENDING
        if not include_inactive:
            match_pipeline['inactive'] = False
        if email:
            match_pipeline['email'] = email
        if name:
            match_pipeline['user_name'] = {'$regex': name, '$options': 'i'}
        if search:
            match_pipeline['email'] = {'$regex': search, '$options': 'i'}
        pipeline.append({'$match': match_pipeline})
        pipeline.extend([
            {
                '$lookup': {
                    'from': 'user_track_action',
                    'as': 'user_actions',
                    'let': {'user_id': '$_id'},
                    'pipeline': [
                        {
                            '$match': {'$expr': {'$eq': ['$user_id', '$$user_id']}}
                        },
                        {
                            '$sort': {'created_at': -1}
                        },
                        {
                            '$limit': 1
                        }
                    ]
                }
            },
            {
                '$lookup': {
                    'from': 'subscriptions',
                    'localField': 'subscription_id',
                    'foreignField': '_id',
                    'as': 'subscription'
                }
            },
            {
                '$lookup': {
                    'from': 'subscriptions',
                    'as': 'expired_subscription',
                    'pipeline': [{'$match': {'expired': True}}]
                }
            },
            {
                '$addFields': {
                    'last_action_at': {'$first': '$user_actions.created_at'},
                    'subscription_name': {
                        '$cond': [
                            {'$gt': ['$subscription_expired_at', datetime.now(UTC)]},
                            {'$first': '$subscription.name'},
                            {'$first': '$expired_subscription.name'}
                        ]
                    },
                    'balance': {'$subtract': ['$leads_limit', '$leads_proceeded']},
                    'roles_length': {'$size': '$roles'}
                }
            },
            {
                '$unset': ['user_actions', 'slack_users', 'discord_users']
            }
        ])
        pipeline.append({'$sort': {sort_field: sort_direction}})
        pipeline.extend([{'$facet': {'page': [{'$skip': skip}, {'$limit': limit}], 'count': [{'$count': 'count'}]}},
                         {'$project': {'page': 1, 'count': {'$first': "$count.count"}}}])
        return UsersPage.from_dic(list(self.collection().aggregate(pipeline))[0])


class UserLeadMongoRepository(BaseMongoRepository):
    collection_name = 'user_leads'
    model = ExtendedUserLeadModel

    def get_leads_with_follow_ups(self):
        now = datetime.now(UTC)
        this_day = datetime(now.year, now.month, now.day, 21, 00, 00, tzinfo=UTC)
        after_week = this_day + timedelta(7)
        previous_day = this_day - timedelta(1)
        pipeline = [
            {'$match': {'archived': False, 'followup_date': {'$ne': None}}},
            {
                '$lookup': {
                    'from': 'users',
                    'localField': 'user_id',
                    'foreignField': '_id',
                    'as': 'user'
                }
            },
            {
                '$lookup': {
                    'from': 'slack_contact',
                    'localField': 'message.sender_id',
                    'foreignField': 'sender_id',
                    'as': 'contact'
                }
            },
            {'$addFields': {'contact': {'$first': '$contact'}, 'user': {'$first': '$user'}}},
            {
                '$project': {
                    'user_id': 1,
                    'user_email': '$user.email',
                    'notification_settings': '$user.notification_settings',
                    'subscription_id': "$user.subscription_id",
                    'followup_to': {
                        '$switch': {
                            'branches': [
                                {
                                    'case': {'$eq': ['$user.notification_settings.follow_ups.type', 'once_a_day']},
                                    'then': this_day
                                },
                                {
                                    'case': {'$eq': ['$user.notification_settings.follow_ups.type', 'once_a_week']},
                                    'then': after_week
                                },
                                {
                                    'case': {'$eq': ['$user.notification_settings.follow_ups.type',
                                                     'unread_for_few_minutes']},
                                    'then': {
                                        '$dateAdd': {
                                            'startDate': now,
                                            'unit': 'minute',
                                            'amount': '$user.notification_settings.follow_ups.minute'
                                        }
                                    }
                                }
                            ],
                            'default': this_day
                        }
                    },
                    'followup_date': 1,
                    'contact': 1,
                    'message.sender_id': 1,
                    'message.source': 1
                }
            },
            {'$group': {'_id': '$user_id', 'leads': {'$push': '$$ROOT'}}},
            {
                '$addFields': {
                    'actual_follow_ups': {
                        '$filter': {
                            'input': '$leads',
                            'as': 'lead',
                            'cond': {
                                '$and': [
                                    {
                                        '$gte': [
                                            '$$lead.followup_date',
                                            {'$cond': [
                                                {
                                                    '$eq': ['$$lead.notification_settings.follow_ups.type',
                                                            'unread_for_few_minutes']
                                                },
                                                now,
                                                previous_day]}]},
                                    {
                                        '$lte': ['$$lead.followup_date', '$$lead.followup_to']}]}}
                    },
                    'overdue_follow_ups': {
                        '$filter': {
                            'input': '$leads',
                            'as': 'lead',
                            'cond': {
                                '$lt': [
                                    '$$lead.followup_date',
                                    {'$cond': [
                                        {
                                            '$eq': ['$notification_settings.follow_ups.type', 'unread_for_few_minutes']
                                        },
                                        now,
                                        previous_day]}]}}}}
            },
            {
                '$addFields': {
                    'email': {'$first': '$leads.user_email'},
                    'notification_settings': {'$first': '$leads.notification_settings'},
                    'subscription_id': {'$first': '$leads.subscription_id'}
                }
            },
            {'$match': {'actual_follow_ups': {'$ne': []}}},
            {'$unset': ['leads']}
        ]
        return [UserFollowUps.from_dic(doc) for doc in list(self.collection().aggregate(pipeline))]

    def update_source(self, source_id: str, source_data: dict):
        self.collection().update_many({'message.source.source_id': source_id},
                                      {'$set': {'message.source': source_data}})

    def update_many_by_sender_id(self, sender_id: str, **kwargs):
        update_dict = {k: v for k, v in kwargs.items() if v is not None}
        self.collection().update_many({'message.sender_id': sender_id}, {'$set': update_dict}, upsert=False)

    def get_many(self, ids: list, user_id):
        docs = self.collection().find({"id": {'$in': ids}, 'user_id': to_object_id(user_id)})
        leads = [ExtendedUserLeadModel.from_dic(lead) for lead in docs]
        senders = [lead.message.sender_id for lead in leads]
        contacts = SlackContactUserRepository().find(user_id, users=senders)
        for lead in leads:
            lead.contact = next(filter(lambda x: x.sender_id == lead.message.sender_id, contacts), None)

        return leads

    def get_leads(self, user_id, skip: int, limit: int, **kwargs) -> List[ExtendedUserLeadModel]:
        pipeline = self.__create_leads_filter(user_id, **kwargs)
        sort_field = kwargs.get('sort_field', 'last_action_at')
        sort_direction = kwargs.get('sort_direction', 'ASCENDING')
        sort_direction = pymongo.ASCENDING if sort_direction == 'ASCENDING' else pymongo.DESCENDING
        docs = list(self.collection().find(pipeline).sort([(sort_field, sort_direction)]).skip(skip).limit(limit))
        leads = [ExtendedUserLeadModel.from_dic(x) for x in docs]
        senders = [lead.message.sender_id for lead in leads]
        contacts = SlackContactUserRepository().find(users=senders)
        for lead in leads:
            lead.contact = next(filter(lambda x: x.sender_id == lead.message.sender_id, contacts), None)
        return leads

    @staticmethod
    def __create_leads_filter(user_id, **kwargs):
        pipeline: dict = {'user_id': to_object_id(user_id)}

        if kwargs.get('status') is not None:
            pipeline['status'] = kwargs.get('status', '')

        if kwargs.get('board_id'):
            pipeline['board_id'] = to_object_id(kwargs.get('board_id'))
        elif kwargs.get('board_id') is not None:
            pipeline['$or'] = [{'board_id': ''}, {'board_id': None}]

        archived = kwargs.get('archived')
        from_date = kwargs.get('from_date')
        to_date = kwargs.get('to_date')
        has_followup = kwargs.get('has_followup')
        followup_to = kwargs.get('followup_to_date')
        followup_from = kwargs.get('followup_from_date')
        created_to = kwargs.get('created_to_date')
        created_from = kwargs.get('created_from_date')
        sender_ids = kwargs.get('sender_ids')
        text = kwargs.get('text')
        stop_words = kwargs.get('stop_words')
        tags = kwargs.get('tags')
        configs = kwargs.get('config')
        bots_names = kwargs.get('bots_names')
        locations = kwargs.get('locations')
        with_chat = kwargs.get('with_chat')
        leads_ids = kwargs.get('leads_ids')
        exclude_leads = kwargs.get('exclude_leads')
        exclude_senders = kwargs.get('exclude_senders')

        pipeline['message.profile.display_name'] = {
            "$ne": "Slackbot"
        }

        if leads_ids is not None:
            pipeline["id"] = {'$in': leads_ids}

        if exclude_leads:
            pipeline['id'] = {'$nin': exclude_leads}

        if exclude_senders:
            pipeline['message.sender_id'] = {'$nin': exclude_senders}

        if archived is not None:
            pipeline['archived'] = archived

        if with_chat is not None:
            pipeline['chat_history'] = {'$exists': True, '$ne': []}

        if has_followup is not None:
            pipeline['followup_date'] = {'$ne': None} if has_followup else {'$eq': None}

        if from_date or to_date:
            pipeline['last_action_at'] = {}

        if from_date:
            start = datetime(from_date.year, from_date.month, from_date.day, tzinfo=tz.tzutc())
            pipeline['last_action_at']['$gte'] = start

        if to_date:
            end = datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59, tzinfo=tz.tzutc())
            pipeline['last_action_at']['$lte'] = end

        if locations and len(locations) > 0:
            pipeline['message.locations'] = {"$in": locations}

        if sender_ids:
            pipeline['message.sender_id'] = {'$in': sender_ids}

        if followup_from or followup_to:
            pipeline['followup_date'] = {}

        if followup_from:
            followup_from = datetime(followup_from.year, followup_from.month, followup_from.day, tzinfo=tz.tzutc())
            pipeline['followup_date']['$gte'] = followup_from

        if followup_to:
            followup_to = datetime(followup_to.year, followup_to.month, followup_to.day, 23, 59, 59, tzinfo=tz.tzutc())
            pipeline['followup_date']['$lte'] = followup_to

        if created_to or created_from:
            pipeline['created_at'] = {}

        if created_to:
            created_to = datetime(created_to.year, created_to.month, created_to.day, 23, 59, 59, tzinfo=tz.tzutc())
            pipeline['created_at']['$lte'] = created_to

        if created_from:
            created_from = datetime(created_from.year, created_from.month, created_from.day, tzinfo=tz.tzutc())
            pipeline['created_at']['$gte'] = created_from

        if stop_words:
            pipeline['full_message_text'] = {'$regex': f'^(?!.*({stop_words})).*$', '$options': 'i'}
        elif text:
            pipeline['$text'] = {'$search': text}

        if tags:
            pipeline["tags"] = {"$elemMatch": {"$in": tags}}

        if configs:
            pipeline["message.configs.id"] = {"$in": configs}

        if bots_names is not None:
            pipeline['message.name'] = {'$in': bots_names}

        return pipeline

    def get_daily_analytics_by_workspace(self, user_configs: list,
                                         dedicated_only: bool | None,
                                         from_date: datetime,
                                         to_date: datetime,
                                         user_id: str):
        pipeline = [
            {
                '$addFields': {
                    'dedicated': {
                        '$anyElementTrue': {
                            '$map': {
                                'input': "$message.configs.id",
                                'as': "config",
                                'in': {'$in': ["$$config", user_configs]}
                            }
                        }
                    }
                }
            },
            {
                '$project': {
                    'created_at': {
                        '$dateToString': {
                            'format': '%Y-%m-%d',
                            'date': '$created_at'
                        }
                    },
                    'id': '$id'
                }
            },
            {
                '$group': {
                    '_id': '$created_at',
                    'data': {'$push': '$id'}
                }
            },
            {
                '$sort': {'_id': 1}
            }
        ]

        if dedicated_only:
            pipeline.insert(1, {"$match": {'dedicated': True}})
        elif dedicated_only is False:
            pipeline.insert(1, {"$match": {'dedicated': False}})

        if from_date:
            beginning_of_the_day = datetime(from_date.year, from_date.month, from_date.day, 0, 0, 0, 0)
            pipeline.insert(0, {"$match": {"created_at": {"$gte": beginning_of_the_day}}})

        if to_date:
            end_of_the_day = datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59, 999)
            pipeline.insert(0, {"$match": {"created_at": {"$lte": end_of_the_day}}})

        if user_id:
            pipeline.insert(0, {"$match": {'user_id': to_object_id(user_id)}})

        saved_messages = list(self.collection().aggregate(pipeline))
        saved_messages_dic = OrderedDict()

        for item in saved_messages:
            saved_messages_dic[item["_id"]] = item["data"]

        return saved_messages_dic

    def add_lead(self, user_id, lead: UserLeadModel) -> None:
        if not lead.created_at:
            lead.created_at = datetime.now(UTC)

        if hasattr(lead, "_id"):
            lead._id = ObjectId()

        lead.user_id = user_id
        self.insert(lead)

    def update_lead(self, user_id, lead_id: str, **kwargs):
        pipeline = {'user_id': to_object_id(user_id), 'id': lead_id}
        update_dict = {k: v for k, v in kwargs.items() if v is not None}
        if 'board_id' in update_dict:
            update_dict['board_id'] = to_object_id(update_dict['board_id']) if len(update_dict['board_id']) == 24 \
                else update_dict['board_id']
        self.collection().update_one(pipeline, {'$set': update_dict})

        return ExtendedUserLeadModel.from_dic(self.collection().find_one(pipeline))

    def update_leads_order(self, user_id, lead_ids: [str]):
        pipeline = {'user_id': to_object_id(user_id), 'id': {'$in': lead_ids}}
        docs = list(self.collection().find(pipeline))

        order = 0
        for lead_id in lead_ids:
            for doc in docs:
                if doc['id'] == lead_id:
                    self.collection().update_one({'id': lead_id}, {'$set': {'order': order}}, upsert=False)
                    order = order + 1

    def delete_lead(self, user_id, lead_id: str):
        """

        :param user_id:
        :param lead_id:
        :return: UserLeadModel
        """

        pipeline = {'user_id': to_object_id(user_id), 'id': lead_id}
        self.collection().delete_one(pipeline)

    def get_lead(self, user_id, message_id: str = None, lead_id: str = None, **kwargs):
        """

        :param user_id:
        :param message_id:
        :param lead_id:
        :return: UserLeadModel
        """

        pipeline = {'user_id': to_object_id(user_id)}
        sender_id = kwargs.get('sender_id')

        if message_id:
            pipeline['message.message_id'] = message_id

        if lead_id:
            pipeline['id'] = lead_id

        if sender_id:
            pipeline['message.sender_id'] = sender_id

        return ExtendedUserLeadModel.from_dic(self.collection().find_one(pipeline))


class UserResetPasswordMongoRepository(BaseMongoRepository):
    pass

    collection_name = 'user_reset_passwords'
    model = UserResetPasswordModel

    def get(self, _id):
        return UserResetPasswordModel.from_dic(self.collection().find_one({'_id': to_object_id(_id)}))

    def delete(self, email):
        self.collection().delete_many({'email': email})

    def add(self, email) -> str:
        model = UserResetPasswordModel()
        model.email = email
        return self.collection().insert_one({'email': email}).inserted_id


class LeadMongoRepository(BaseMongoRepository):
    pass

    database_name = 'lgt_admin'
    collection_name = 'general_leads'
    model = LeadModel

    def update_source(self, source_id: str, source_data: dict):
        self.collection().update_many({'message.source.source_id': source_id},
                                      {'$set': {'message.source': source_data}})

    def delete(self, _id):
        res = self.collection().delete_one({'id': _id})
        return res

    def get(self, _id=None, **kwargs):
        pipeline = {}
        timestamp = kwargs.get("timestamp")
        message_id = kwargs.get("message_id")
        channel_id = kwargs.get("channel_id")
        if _id:
            pipeline['id'] = _id
        if message_id:
            pipeline['message.message_id'] = message_id
        if channel_id:
            pipeline['message.channel_id'] = channel_id
        if timestamp:
            pipeline['message.timestamp'] = timestamp
        result: dict = self.collection().find_one(pipeline)
        if not result:
            return None

        return LeadModel.from_dic(result)

    def get_many(self, ids: list):
        docs = self.collection().find({"id": {'$in': ids}})
        leads = [ExtendedLeadModel.from_dic(lead) for lead in docs]
        senders = [lead.message.sender_id for lead in leads]
        contacts = SlackContactUserRepository().find(users=senders)
        for lead in leads:
            lead.contact = next(filter(lambda x: x.sender_id == lead.message.sender_id, contacts), None)

        return leads

    def get_by_sender_id(self, sender_id, exclude_leads: [str], skip: int, limit: int):
        pipeline = {'message.sender_id': sender_id, 'id': {'$nin': exclude_leads}}
        leads = self.collection().find(pipeline).sort([('created_at', pymongo.DESCENDING)]).skip(skip).limit(limit)
        return [LeadModel.from_dic(lead) for lead in leads]

    def get_by_message_id(self, message_id):
        """

        :rtype: LeadModel
        :param message_id:
        """
        doc: dict = self.collection().find_one({'message.message_id': message_id})
        if not doc:
            return None

        return LeadModel.from_dic(doc)

    def update(self, _id: str, **kwargs):
        update_dict = {k: v for k, v in kwargs.items() if v is not None}
        self.collection().update_one({'id': _id}, {'$set': update_dict}, upsert=False)

    def get_per_day(self, date: datetime):
        start_day = datetime(date.year, date.month, date.day, 0, 0, 0, tzinfo=tz.tzutc())
        end_day = datetime(date.year, date.month, date.day, 23, 59, 59, tzinfo=tz.tzutc())
        docs = self.collection().find({'created_at': {'$gte': start_day, '$lte': end_day}}).sort('created_at', 1)
        return [LeadModel.from_dic(x) for x in docs]


class SpamUserLeadsMongoRepository(UserLeadMongoRepository):
    pass

    def __init__(self):
        self.database_name = 'lgt_admin'
        self.collection_name = 'spam_leads'


class BoardsMongoRepository(BaseMongoRepository):
    pass

    collection_name = 'boards'
    model = BoardModel

    def create_board(self, user_id: str, name: str, **kwargs):
        is_primary = kwargs.get('is_primary', False)

        if is_primary:
            primary_board: dict = self.collection().find_one({'user_id': to_object_id(user_id),
                                                              'is_primary': is_primary})
            if primary_board:
                return BoardModel.from_dic(primary_board)

        board = BoardModel()
        board.name = name
        board.created_at = datetime.now(UTC)
        board.user_id = to_object_id(user_id)
        board.is_primary = is_primary
        self.collection().insert_one(BoardModel.to_dic(board))

        return BoardModel.from_dic(self.collection().find_one({'user_id': to_object_id(user_id), 'name': name}))

    def add_default_statuses(self, user_id: str, board_id: str):
        pipeline = {'user_id': to_object_id(user_id), '_id': to_object_id(board_id)}
        board = BoardModel.from_dic(self.collection().find_one(pipeline))

        if not board:
            return None

        board.statuses.append(BoardedStatus().from_dic({'id': 'Lead', 'name': 'Lead', 'order': 0}))
        board.statuses.append(BoardedStatus().from_dic({'id': 'Prospect', 'name': 'Prospect', 'order': 1}))
        board.statuses.append(BoardedStatus().from_dic({'id': 'Opportunity', 'name': 'Opportunity', 'order': 2}))
        board.statuses.append(BoardedStatus().from_dic({'id': 'Call', 'name': 'Call', 'order': 3}))
        board.statuses.append(BoardedStatus().from_dic({'id': 'Contract', 'name': 'Contract', 'order': 4}))
        board.statuses.append(BoardedStatus().from_dic({'id': 'Refused', 'name': 'Refused', 'order': 5}))

        return self.update_board(user_id, board_id, statuses=board.statuses)

    def get(self, user_id: str, **kwargs):
        pipeline = {'user_id': to_object_id(user_id)}
        is_primary = kwargs.get('is_primary')
        default = kwargs.get('default')
        name = kwargs.get('name')

        if is_primary is not None:
            pipeline['is_primary'] = is_primary

        if default is not None:
            pipeline['default'] = default

        if name:
            pipeline['name'] = name

        docs = self.collection().find(pipeline).sort('created_at', 1)
        return [BoardModel.from_dic(doc) for doc in docs]

    def get_with_stats(self, user_id: str, **kwargs):
        is_primary = kwargs.get('is_primary')
        default = kwargs.get('default')
        name = kwargs.get('name')
        match = {'user_id': to_object_id(user_id)}

        if is_primary is not None:
            match['is_primary'] = is_primary

        if default is not None:
            match['default'] = default

        if name:
            match['name'] = name

        pipeline = [
            {
                '$match': match
            },
            {
                '$unwind': {'path': '$statuses', 'preserveNullAndEmptyArrays': True}
            },
            {
                '$lookup': {
                    'from': 'user_leads',
                    'as': 'statuses.user_leads',
                    'let': {'id': '$_id', 'status': '$statuses.name'},
                    'pipeline': [
                        {
                            '$match': {
                                '$expr': {
                                    '$and': [
                                        {'$eq': ['$board_id', '$$id']},
                                        {'$eq': ['$status', '$$status']},
                                        {'$eq': ['$archived', False]}
                                    ]
                                }
                            }
                        }
                    ]
                }
            },
            {
                '$addFields': {'statuses.user_leads': {'$size': '$statuses.user_leads'}}
            },
            {
                '$set': {'statuses': {'$cond': ['$statuses.name', '$statuses', None]}}
            },
            {
                '$group': {
                    '_id': '$_id',
                    'statuses': {'$push': '$statuses'},
                    'name': {'$first': '$name'},
                    'created_at': {'$first': '$created_at'},
                    'user_id': {'$first': '$user_id'},
                    'is_primary': {'$first': '$is_primary'},
                    'default': {'$first': '$default'}}
            },
            {
                '$addFields': {
                    'statuses': {'$filter': {'input': '$statuses', 'as': 'status', 'cond': {'$ne': ['$$status', None]}}}
                }
            },
            {'$sort': {'created_at': 1}}]

        return [BoardModel.from_dic(doc) for doc in self.collection().aggregate(pipeline)]

    def get_primary(self, user_id: str):
        return BoardModel.from_dic(self.collection().find_one({'user_id': to_object_id(user_id), 'is_primary': True}))

    def get_by_id(self, id: str):
        return BoardModel.from_dic(self.collection().find_one({'_id': to_object_id(id)}))

    def delete_by_id(self, id: str):
        return self.collection().delete_many({'_id': to_object_id(id)})

    def update_board(self, user_id, board_id: str, **kwargs):
        pipeline = {'user_id': to_object_id(user_id), '_id': to_object_id(board_id)}

        if kwargs.get('statuses'):
            kwargs['statuses'] = [status.to_dic() for status in kwargs.get('statuses')
                                  if isinstance(status, BoardedStatus)]

        doc = BoardModel.from_dic(self.collection().find_one(pipeline))
        if not doc:
            return None

        update_dict = {k: v for k, v in kwargs.items() if v is not None}
        self.collection().update_one(pipeline, {'$set': update_dict})

        self._collection('user_leads').update_many({'user_id': to_object_id(user_id), 'board_id': to_object_id(doc.id)},
                                                   {'$set': {'board_id': to_object_id(board_id)}})

        return BoardModel.from_dic(self.collection().find_one(pipeline))


class DedicatedBotRepository(BaseMongoRepository):
    pass

    collection_name = 'dedicated_bots'

    def add_or_update(self, bot: DedicatedBotModel):
        bot_dict = bot.to_dic()
        if '_id' in bot_dict:
            bot_dict.pop('_id')
        update_response = self.collection().update_one({"source.source_id": bot.source.source_id,
                                                        "user_name": bot.user_name,
                                                        "user_id": to_object_id(bot.user_id)},
                                                       {'$set': bot_dict}, upsert=True)
        bot.id = update_response.upserted_id if update_response.upserted_id else bot.id
        return bot

    def get_all(self, only_valid: bool = False, **kwargs) -> List[DedicatedBotModel]:
        kwargs["only_valid"] = only_valid
        pipeline = self.__create_bots_filter(**kwargs)
        docs = self.collection().find(pipeline)
        sort_by = kwargs.get('sort_by')
        if sort_by:
            docs = docs.sort({sort_by: 1})
        return [DedicatedBotModel.from_dic(doc) for doc in docs]

    def get_source_ids_for_user(self, **kwargs):
        pipeline = self.__create_bots_filter(**kwargs)
        docs = self.collection().find(pipeline, projection={'_id': 0, 'source_id': '$source.source_id'})
        return [item['source_id'] for item in docs]

    def get_one(self, **kwargs):
        pipeline = self.__create_bots_filter(**kwargs)
        return DedicatedBotModel.from_dic(self.collection().find_one(pipeline))

    def delete(self, _id: str):
        self.collection().update_one({'_id': to_object_id(f"{_id}")}, {"$set": {"deleted": True}})

    @staticmethod
    def __create_bots_filter(**kwargs):
        pipeline: dict = {}
        name = kwargs.get('name')
        source_type = kwargs.get('source_type', None)
        user_name = kwargs.get('user_name')
        only_valid = kwargs.get('only_valid')
        include_paused = kwargs.get('include_paused', False)
        include_deleted = kwargs.get('include_deleted', False)
        bot_id = kwargs.get('id')
        user_id = kwargs.get('user_id')
        source_id = kwargs.get('source_id')
        server_id = kwargs.get('server_id')
        active_server_id = kwargs.get('active_server_id')
        invalid_creds = kwargs.get('invalid_creds')
        sort_by = kwargs.get('sort_by')
        deactivated_from = kwargs.get('deactivated_from')
        user_ids = kwargs.get('user_ids')

        if deactivated_from:
            pipeline['deactivated_at'] = {'$gte': deactivated_from}

        if bot_id:
            pipeline["_id"] = to_object_id(bot_id)

        if user_id:
            pipeline["user_id"] = to_object_id(user_id)

        if name:
            pipeline["name"] = name

        if source_type:
            pipeline["source.source_type"] = source_type

        if user_name:
            pipeline["user_name"] = user_name

        if source_id:
            pipeline["source.source_id"] = source_id

        if server_id:
            pipeline["servers"] = {'$elemMatch': {'id': server_id}}

        if active_server_id:
            pipeline["servers"] = {'$elemMatch': {'id': active_server_id, 'deleted': False}}

        if only_valid:
            pipeline['invalid_creds'] = False

        if invalid_creds is not None:
            pipeline['invalid_creds'] = invalid_creds

        if not include_deleted:
            pipeline['deleted'] = False

        if not include_paused and source_type == SourceType.DISCORD:
            pipeline['paused'] = False

        if sort_by:
            pipeline[sort_by] = {'$exists': True}

        if user_ids is not None:
            pipeline["user_id"] = {'$in': [to_object_id(_id) for _id in user_ids]}

        return pipeline


class SlackContactUserRepository(BaseMongoRepository):
    collection_name = "slack_contact"
    model = SlackMemberInformation

    def find(self, text: Optional[str] = None, skip: int = 0, limit: int = 1000, **kwargs):
        pipeline = {}

        source_id = kwargs.get("source_id")
        users = kwargs.get("users")
        presence_updated_at = kwargs.get("online_updated_at")
        if text:
            pipeline['$text'] = {'$search': text}

        if source_id:
            pipeline['source.source_id'] = source_id

        if users is not None:
            pipeline['sender_id'] = {'$in': users}

        if presence_updated_at:
            pipeline['online_updated_at'] = {'$gte': presence_updated_at}

        pipeline = {**pipeline, **kwargs}

        docs = self.collection().find(pipeline).sort([("real_name", pymongo.ASCENDING)]) \
            .skip(skip) \
            .limit(limit)
        return [SlackMemberInformation.from_dic(doc) for doc in docs]

    def find_one(self, user_id: str):
        pipeline = {"sender_id": user_id}
        return SlackMemberInformation.from_dic(self.collection().find_one(pipeline))

    def update_source(self, source_id: str, source_data: dict):
        self.collection().update_many({'source.source_id': source_id}, {'$set': {'source': source_data}})


class UserTemplatesRepository(BaseMongoRepository):
    collection_name = "user_templates"
    model = UserTemplateModel

    def get_all(self, user_id: str):
        return [UserTemplateModel.from_dic(doc) for doc in self.collection().find({'user_id': to_object_id(user_id)})]

    def get(self, id: str):
        return UserTemplateModel.from_dic(self.collection().find_one({'_id': to_object_id(id)}))

    def create_or_update(self, template: UserTemplateModel):
        result = self.collection().update_one(
            {"_id": to_object_id(template.id)},
            {'$set': template.to_dic()},
            upsert=True)

        if result.upserted_id:
            template.id = result.upserted_id

        return template

    def delete_by_id(self, id: str):
        return self.collection().find_one_and_delete({'_id': to_object_id(id)})


class UserContactsRepository(BaseMongoRepository):
    collection_name = 'user_contacts'

    def find(self, user_id: str, **kwargs):
        pipeline = {'user_id': to_object_id(user_id)}

        users = kwargs.get('users')
        spam = kwargs.get('spam')
        with_chat_only = kwargs.get('with_chat_only', False)
        source_id = kwargs.get('source_id')

        if users:
            pipeline['sender_id'] = {'$in': users}

        if spam is not None:
            pipeline['spam'] = spam

        if source_id:
            pipeline['source_id'] = source_id

        if with_chat_only:
            pipeline['chat_id'] = {'$ne': None}

        docs = self.collection().find(pipeline)
        return [UserContact.from_dic(doc) for doc in docs]

    def find_one(self, user_id: str, **kwargs):
        pipeline = {'user_id': to_object_id(user_id)}

        sender_id = kwargs.get('sender_id')
        source_id = kwargs.get('source_id')
        if sender_id:
            pipeline['sender_id'] = sender_id
        if source_id:
            pipeline['source_id'] = source_id

        if contact_instance := self.collection().find_one(pipeline):
            return UserContact.from_dic(contact_instance)

    def update(self, user_id: str | ObjectId, sender_id: str, source_id: str, **kwargs):
        pipeline = {'user_id': to_object_id(user_id), 'sender_id': sender_id, 'source_id': source_id}
        update_dict = {k: v for k, v in kwargs.items() if v is not None}
        self.collection().update_one(pipeline, {'$set': update_dict}, upsert=False)

    def update_many(self, sender_id: str, **kwargs):
        pipeline = {'sender_id': sender_id}
        update_dict = {k: v for k, v in kwargs.items() if v is not None}
        self.collection().update_many(pipeline, {'$set': update_dict}, upsert=False)

    def find_grouped_actual_contacts(self, user_id: ObjectId | str, **kwargs) -> dict[str, list[UserContact]]:
        spam = kwargs.get('spam')
        with_chat_only = kwargs.get('with_chat_only', False)
        match_pipeline = {'user_id': to_object_id(user_id), 'source_id': {'$ne': None}}
        if spam is not None:
            match_pipeline['spam'] = spam
        if with_chat_only:
            match_pipeline['chat_id'] = {'$ne': None}
        pipeline = [
            {
                '$lookup': {
                    'from': 'user_leads',
                    'as': 'user_leads',
                    'let': {
                        'sender_id': '$sender_id',
                        'user_id': '$user_id'
                    },
                    'pipeline': [
                        {
                            '$match': {'$expr': {'$and': [
                                {'$eq': ['$message.sender_id', '$$sender_id']},
                                {'$eq': ['$user_id', '$$user_id']}]}}
                        }
                    ]
                }
            },
            {
                '$match': {'user_leads.last_action_at': {'$gt': datetime.now(UTC) - timedelta(days=90)}}
            },
            {
                '$unset': 'user_leads'
            },
            {
                '$group': {'_id': '$source_id', 'contacts': {'$push': '$$ROOT'}}
            },
            {
                '$project': {'source_id': '$_id', 'contacts': 1, '_id': 0}
            }
        ]
        pipeline.insert(0, {'$match': match_pipeline})
        contacts_groups = {}
        for doc in list(self.collection().aggregate(pipeline)):
            contacts_groups[doc['source_id']] = [UserContact.from_dic(contact) for contact in doc['contacts']]
        return contacts_groups

    def find_actual_contacts_users(self, days: int = 90):
        pipeline = [
            {
                '$lookup': {
                    'from': 'user_leads',
                    'as': 'leads',
                    'let': {'user_id': '$user_id', 'sender_id': '$sender_id'},
                    'pipeline': [
                        {'$sort': {'last_action_at': -1}},
                        {
                            '$match': {
                                '$expr': {
                                    '$and': [
                                        {'$eq': ['$$sender_id', '$message.sender_id']},
                                        {'$eq': ['$$user_id', '$user_id']}
                                    ]
                                }
                            }
                        },
                        {'$limit': 1}
                    ]
                }
            },
            {
                '$match': {'leads.last_action_at': {'$gte': datetime.now(UTC) - timedelta(days)}}
            },
            {
                '$group': {'_id': '$user_id'}
            }
        ]
        user_ids = []
        for doc in list(self.collection().aggregate(pipeline)):
            user_ids.append(doc['_id'])
        return user_ids


class TeamRepository(BaseMongoRepository):
    collection_name = 'teams'

    def get_teammate(self, user_id: str, teammate_id: str):
        pipeline = [
            {
                "$match": {
                    "$or": [
                        {"author_id": to_object_id(user_id), "recipient_id": to_object_id(teammate_id)},
                        {"author_id": to_object_id(teammate_id), "recipient_id": to_object_id(user_id)}
                    ],
                    "status": "approved"
                }
            }
        ]
        return list(self.collection().aggregate(pipeline))


class ChatRepository(BaseMongoRepository):
    collection_name = 'chat_messages'

    def get_list(self, **kwargs):
        pipeline = {}
        text = kwargs.get('text')
        user_id = kwargs.get('user_id')
        bot_id = kwargs.get('bot_id')
        sender_id = kwargs.get('sender_id')
        from_date = kwargs.get('from_date')
        to_date = kwargs.get('to_date')

        if text:
            pipeline['text'] = {"$regex": text, "$options": 'i'}
        if bot_id:
            pipeline['bot_id'] = to_object_id(bot_id)
        if user_id:
            pipeline['user_id'] = to_object_id(user_id)
        if sender_id:
            pipeline['sender_id'] = sender_id

        if from_date or to_date:
            pipeline['last_action_at'] = {}

        if from_date:
            start = datetime(from_date.year, from_date.month, from_date.day, tzinfo=tz.tzutc())
            pipeline['created_at']['$gte'] = start

        if to_date:
            end = datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59, tzinfo=tz.tzutc())
            pipeline['created_at']['$lte'] = end

        return [ChatMessage.from_dic(msg)
                for msg in self.collection().find(pipeline).sort("id", pymongo.ASCENDING)]

    def get_aggregated_list(self, **kwargs):
        match_pipeline = {}
        user_id = kwargs.get('user_id')
        from_date = kwargs.get('from_date')
        to_date = kwargs.get('to_date')
        sort_by = kwargs.get('sort_by', 'id')
        viewed = kwargs.get('viewed')

        if user_id:
            match_pipeline['user_id'] = to_object_id(user_id)

        if from_date or to_date:
            match_pipeline['created_at'] = {}

        if viewed is not None:
            match_pipeline['viewed'] = viewed

        if from_date:
            start = datetime(from_date.year, from_date.month, from_date.day, tzinfo=tz.tzutc())
            match_pipeline['created_at']['$gte'] = start

        if to_date:
            end = datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59, tzinfo=tz.tzutc())
            match_pipeline['created_at']['$lte'] = end

        pipeline = [
            {'$match': match_pipeline},
            {
                '$lookup': {
                    'from': 'slack_contact',
                    'localField': 'sender_id',
                    'foreignField': 'sender_id',
                    'as': 'user'
                }
            },
            {
                '$lookup': {
                    'from': 'dedicated_bots',
                    'localField': 'bot_id',
                    'foreignField': '_id',
                    'as': 'bot'
                }
            },
            {
                '$match': {'user': {'$ne': []}}
            },
            {
                '$addFields': {'user': {'$first': '$user'}, 'bot': {'$first': '$bot'}}
            },
            {
                '$sort': {sort_by: 1}
            }]

        return self.collection().aggregate(pipeline)

    def get_grouped_messages(self, **kwargs):
        match_pipeline = {}
        pipeline = [
            {
                '$sort': {'created_at': 1}
            },
            {
                '$group': {'_id': '$bot_id', 'messages': {'$push': '$$ROOT'}}
            }
        ]

        from_date = kwargs.get('from_date')
        to_date = kwargs.get('to_date')
        user_id = kwargs.get('user_id')

        if from_date or to_date:
            match_pipeline['created_at'] = {}

        if from_date:
            start = datetime(from_date.year, from_date.month, from_date.day, tzinfo=tz.tzutc())
            match_pipeline['created_at']['$gte'] = start

        if to_date:
            end = datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59, tzinfo=tz.tzutc())
            match_pipeline['created_at']['$lte'] = end

        if user_id:
            match_pipeline['user_id'] = to_object_id(user_id)

        pipeline.insert(0, {'$match': match_pipeline})
        return [GroupedMessagesModel.from_dic(doc) for doc in list(self.collection().aggregate(pipeline))]

    def upsert_messages(self, messages: list[dict]):
        if messages:
            operations = [UpdateOne({"id": msg['id'], "user_id": msg['user_id']},
                                    {'$set': msg}, upsert=True) for msg in messages]
            self.collection().bulk_write(operations)

    def delete_message(self, user_id: str, _id: str):
        self.collection().delete_one({"id": _id, 'user_id': to_object_id(user_id)})


class MessageRequestsRepository(BaseMongoRepository):
    collection_name = 'message_requests'

    def upsert(self, user_id: str, sender_id: str, message_request: MessageRequest):
        self.collection().update_one({'user_id': to_object_id(user_id), 'sender_id': sender_id},
                                     {'$set': message_request.to_dic()}, upsert=True)

    def get_many(self, user_id: str, viewed: bool = False, sort_direction: int = pymongo.ASCENDING, **kwargs):
        match_pipeline = {'user_id': to_object_id(user_id), 'viewed': viewed}
        from_date = kwargs.get('from_date')

        if from_date:
            start = datetime(from_date.year, from_date.month, from_date.day, tzinfo=tz.tzutc())
            match_pipeline['created_at']['$gte'] = start

        pipeline = [
            {
                '$match': match_pipeline
            },
            {
                '$lookup': {
                    'from': 'slack_contact',
                    'localField': 'sender_id',
                    'foreignField': 'sender_id',
                    'as': 'user'
                }
            },
            {
                '$lookup': {
                    'from': 'dedicated_bots',
                    'localField': 'bot_id',
                    'foreignField': '_id',
                    'as': 'bot'
                }
            },
            {
                '$addFields': {'user': {'$first': '$user'}, 'bot': {'$first': '$bot'}}
            },
            {
                '$sort': {'created_at': sort_direction}
            }
        ]
        return self.collection().aggregate(pipeline)

    def find(self, user_id: str, sender_id: str):
        return self.collection().find_one({'user_id': to_object_id(user_id), 'sender_id': sender_id})

    def delete_many(self, **kwargs):
        self.collection().delete_many(kwargs)


class UserVerificationMongoRepository(BaseMongoRepository):
    pass

    collection_name = 'user_verifications'
    model = UserVerificationModel

    def get(self, _id):
        return UserVerificationModel.from_dic(self.collection().find_one({'_id': to_object_id(_id)}))

    def delete(self, email):
        self.collection().delete_many({'email': email})

    def add(self, email) -> str:
        model = UserVerificationModel()
        model.email = email
        model.created_at = datetime.now(UTC)
        return self.collection().insert_one(model.to_dic()).inserted_id


class SubscriptionsRepository(BaseMongoRepository):
    pass

    collection_name = 'subscriptions'
    model = Subscription

    def find_one(self, **kwargs):
        pipeline = {}
        subscription_id = kwargs.get('id')
        trial = kwargs.get('trial')
        expired = kwargs.get('expired')
        unverified = kwargs.get('unverified')
        if subscription_id:
            pipeline['_id'] = to_object_id(subscription_id)
        if unverified is not None:
            pipeline['unverified'] = unverified
        if trial is not None:
            pipeline['trial'] = trial
        if expired is not None:
            pipeline['expired'] = expired

        return Subscription.from_dic(self.collection().find_one(pipeline))


class ScheduledMessagesRepository(BaseMongoRepository):
    pass

    collection_name = 'scheduled_messages'

    def find_all(self, only_actual: bool = True):
        pipeline = {}
        if only_actual:
            pipeline['post_at'] = {'$lte': datetime.now(UTC)}
        return [ScheduledMessage.from_dic(doc) for doc in self.collection().find(pipeline)]
