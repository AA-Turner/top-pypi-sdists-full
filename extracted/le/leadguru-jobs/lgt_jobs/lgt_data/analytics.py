import os
from typing import Optional, List, Dict, Union
from collections import OrderedDict
from datetime import timedelta, datetime
from bson import ObjectId
from dateutil import tz
from lgt_jobs.lgt_data.mongo_repository import to_object_id
from pymongo import MongoClient

client = MongoClient(os.environ.get('MONGO_CONNECTION_STRING', 'mongodb://127.0.0.1:27017/'))
db = client.get_database('lgt_admin')


def _build_date_aggregated_analytics_pipeline(source_id=None, email=None, started_at: datetime = None,
                                              ended_at: datetime = None, bots_ids: [str] = None):
    pipeline = [
        {
            "$sort": {"created_at": 1}
        },
        {
            "$project": {
                "created_at": {"$dateToString": {"format": "%Y-%m-%d", "date": "$created_at"}},
                "name": "$name"
            }
        },
        {
            "$group":
                {
                    "_id": "$created_at",
                    "count": {"$sum": 1}
                }
        },
        {
            "$project": {
                "_id": {"$dateFromString": {"format": "%Y-%m-%d", "dateString": "$_id"}},
                "count": "$count"
            }
        },
        {
            "$sort": {"_id": 1}
        },
        {"$limit": 1000}
    ]

    if source_id:
        pipeline.insert(0, {"$match": {"source.source_id": source_id}})

    if email:
        pipeline.insert(0, {"$match": {"name": email}})

    if started_at:
        beginning_of_the_day = datetime(started_at.year, started_at.month, started_at.day, 0, 0, 0, 0)
        pipeline.insert(0, {"$match": {"created_at": {"$gte": beginning_of_the_day}}})

    if ended_at:
        end_of_the_day = datetime(ended_at.year, ended_at.month, ended_at.day, 23, 59, 59, 999)
        pipeline.insert(0, {"$match": {"created_at": {"$lte": end_of_the_day}}})

    if bots_ids is not None:
        pipeline.insert(0, {"$match": {'extra_ids': {'$in': bots_ids}}})

    return pipeline


def _create_result_dic(started_at: datetime = None, ended_at: datetime = None):
    analytics_dict = OrderedDict()

    if started_at and ended_at:
        days_range = range(0, (ended_at - started_at).days + 1)
        for day in days_range:
            cur_date = started_at + timedelta(days=day)
            str_date = f'{cur_date.year}-{cur_date.month:02d}-{cur_date.day:02d}'
            analytics_dict[str_date] = 0

    return analytics_dict


def _prepare_date_analytics_doc(doc, ordered_result_dict: Dict[str, int]):
    for item in doc:
        str_date = f'{item["_id"].year}-{item["_id"].month:02d}-{item["_id"].day:02d}'
        ordered_result_dict[str_date] = item["count"]
    return ordered_result_dict


def get_channel_aggregated_analytics(from_date: datetime = None, to_date: datetime = None,
                                     bot_id: Optional[str | ObjectId] = None):
    pipeline = [
        {
            '$match': {
                'extra_ids': {"$in": [str(bot_id)]}
            }
        },
        {
            "$group": {
                '_id': {
                    '$arrayElemAt': [
                        '$attributes', 0
                    ]
                },
                'count': {"$sum": 1}
            }
        },
        {
            '$limit': 1000
        }
    ]

    if from_date:
        beginning_of_the_day = datetime(from_date.year, from_date.month, from_date.day, 0, 0, 0, 0)
        pipeline.insert(0, {"$match": {"created_at": {"$gte": beginning_of_the_day}}})

    if to_date:
        end_of_the_day = datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59, 999)
        pipeline.insert(0, {"$match": {"created_at": {"$lte": end_of_the_day}}})

    received_messages = list(db[f'received_messages'].aggregate(pipeline))
    filtered_messages = list(db[f'filtered_messages'].aggregate(pipeline))

    received_messages_dic = OrderedDict()
    filtered_messages_dic = OrderedDict()

    for item in received_messages:
        received_messages_dic[item["_id"]] = item["count"]

    for item in filtered_messages:
        filtered_messages_dic[item["_id"]] = item["count"]

    return received_messages_dic, filtered_messages_dic


def get_aggregated_user_leads(user_id: Union[ObjectId, str],
                              from_date: datetime,
                              to_date: datetime = None):
    pipeline = [
        {
            '$match': {
                'created_at': {'$gte': from_date}
            }
        }, {
            '$group': {
                '_id': {
                    '$dateFromParts': {
                        'day': {
                            '$dayOfMonth': '$created_at'
                        },
                        'month': {
                            '$month': '$created_at'
                        },
                        'year': {
                            '$year': '$created_at'
                        }
                    }
                },
                'count': {
                    '$sum': 1
                },
                'leads': {
                    '$push': {
                        'id': '$id',
                        'created_at': '$created_at'
                    }
                }
            }
        }, {
            '$sort': {
                '_id': 1
            }
        }
    ]

    if user_id:
        pipeline[0]["$match"]["user_id"] = to_object_id(user_id)

    if to_date:
        end = datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59, tzinfo=tz.tzutc())
        pipeline[0]["$match"]["created_at"]['$lte'] = end

    user_leads_data = list(client.lgt_admin.user_leads.aggregate(pipeline))
    result = _create_result_dic(from_date, to_date)

    for item in user_leads_data:
        str_date = f'{item["_id"].year}-{item["_id"].month:02d}-{item["_id"].day:02d}'
        result[str_date] = item["count"]
    return result


def get_register_users_analytics(from_date: datetime = None, to_date: datetime = None):
    pipeline = [
        {
            '$addFields': {
                'created_at_formatted': {
                    '$dateToString': {
                        'format': '%Y-%m-%d',
                        'date': '$created_at'
                    }
                }
            }
        }, {
            '$group': {
                '_id': '$created_at_formatted',
                'count': {
                    '$sum': 1
                }
            }
        }
    ]
    if from_date:
        beginning_of_the_day = datetime(from_date.year, from_date.month, from_date.day, 0, 0, 0, 0)
        pipeline.insert(0, {"$match": {"created_at": {"$gte": beginning_of_the_day}}})

    if to_date:
        end_of_the_day = datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59, 999)
        pipeline.insert(0, {"$match": {"created_at": {"$lte": end_of_the_day}}})

    users = list(client.lgt_admin.users.aggregate(pipeline))
    users_dic = OrderedDict()

    for item in users:
        users_dic[item["_id"]] = item["count"]

    return users_dic


def get_global_saved_leads_analytics(from_date: datetime = None, to_date: datetime = None):
    pipeline = [
        {
            '$addFields': {
                'created_at_formatted': {
                    '$dateToString': {
                        'format': '%Y-%m-%d',
                        'date': '$created_at'
                    }
                }
            }
        }, {
            '$group': {
                '_id': '$created_at_formatted',
                'count': {
                    '$sum': 1
                }
            }
        }
    ]

    if from_date:
        beginning_of_the_day = datetime(from_date.year, from_date.month, from_date.day, 0, 0, 0, 0)
        pipeline.insert(0, {"$match": {"created_at": {"$gte": beginning_of_the_day}}})

    if to_date:
        end_of_the_day = datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59, 999)
        pipeline.insert(0, {"$match": {"created_at": {"$lte": end_of_the_day}}})

    saved_leads = list(client.lgt_admin.user_leads.aggregate(pipeline))
    saved_leads_dic = OrderedDict()
    for item in saved_leads:
        saved_leads_dic[str(item["_id"])] = item["count"]
    return saved_leads_dic


def get_global_uniq_leads_analytics(from_date: datetime = None, to_date: datetime = None):
    pipeline = [
        {
            '$addFields': {
                'created_at_formatted': {
                    '$dateToString': {
                        'format': '%Y-%m-%d',
                        'date': '$created_at'
                    }
                }
            }
        }, {
            '$group': {
                '_id': {
                    'created_at': '$created_at_formatted',
                    'message': '$message.message_id'
                },
                'uniq_leads': {
                    '$addToSet': '$message.message_id'
                }
            }
        }, {
            '$group': {
                '_id': '$_id.created_at',
                'uniq_leads_count': {
                    '$sum': {
                        '$size': '$uniq_leads'
                    }
                }
            }
        }
    ]

    if from_date:
        beginning_of_the_day = datetime(from_date.year, from_date.month, from_date.day, 0, 0, 0, 0)
        pipeline.insert(0, {"$match": {"created_at": {"$gte": beginning_of_the_day}}})

    if to_date:
        end_of_the_day = datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59, 999)
        pipeline.insert(0, {"$match": {"created_at": {"$lte": end_of_the_day}}})

    uniq_leads = list(client.lgt_admin.user_leads.aggregate(pipeline))
    uniq_leads_dic = OrderedDict()

    for item in uniq_leads:
        uniq_leads_dic[item["_id"]] = item["uniq_leads_count"]
    return uniq_leads_dic


def get_bots_global_analytics(from_date: datetime = None, to_date: datetime = None):
    pipeline = [
        {
            '$addFields': {
                'created_at_formatted': {
                    '$dateToString': {
                        'format': '%Y-%m-%d',
                        'date': '$created_at'
                    }
                }
            }
        },
        {
            '$group': {
                '_id': {
                    'source_id': '$source.source_id',
                    'created_at': '$created_at_formatted'
                },
                'count': {
                    '$sum': 1
                }
            }
        }, {
            '$group': {
                '_id': '$_id.created_at',
                'bots': {
                    '$sum': '$count'
                },
                'sources': {
                    '$sum': {
                        '$cond': [
                            {
                                '$eq': [
                                    '$count', 1
                                ]
                            }, 1, 0
                        ]
                    }
                }
            }
        }
    ]
    if from_date:
        beginning_of_the_day = datetime(from_date.year, from_date.month, from_date.day, 0, 0, 0, 0)
        pipeline.insert(0, {"$match": {"created_at": {"$gte": beginning_of_the_day}}})

    if to_date:
        end_of_the_day = datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59, 999)
        pipeline.insert(0, {"$match": {"created_at": {"$lte": end_of_the_day}}})

    bots = list(client.lgt_admin.dedicated_bots.aggregate(pipeline))
    result = {}
    for bot in bots:
        result.update({bot['_id']: {'bots': bot['bots'], 'sources': bot['sources']}})
    return result


def get_date_aggregated_analytics(source_id=None, started_at: datetime = None,
                                  ended_at: datetime = None, bots_ids: [str] = None, configs: [str] = None):
    pipeline: list = _build_date_aggregated_analytics_pipeline(source_id=source_id, started_at=started_at,
                                                               ended_at=ended_at, bots_ids=bots_ids)

    if configs is not None:
        pipeline.insert(0, {"$match": {"configs.id": {'$in': configs}}})

    filtered_messages = list(db[f'filtered_messages'].aggregate(pipeline))
    received_messages = list(db[f'received_messages'].aggregate(pipeline))

    received_messages_dic = _create_result_dic(started_at, ended_at)
    filtered_messages_dic = _create_result_dic(started_at, ended_at)

    return (_prepare_date_analytics_doc(received_messages, received_messages_dic),
            _prepare_date_analytics_doc(filtered_messages, filtered_messages_dic))


def get_leads_aggregated_analytics(from_date: datetime = None, to_date: datetime = None, user_id: str = None):
    pipeline = [
        {
            '$project': {'_id': 0, 'user_ids': 1}
        },
        {
            '$unwind': {'path': '$user_ids', 'preserveNullAndEmptyArrays': False}
        },
        {
            '$group': {'_id': '$user_ids', 'count': {'$sum': 1}}
        }
    ]
    if user_id:
        pipeline.insert(0, {"$match": {"user_ids": {"$in": [to_object_id(user_id)]}}})

    if from_date:
        beginning_of_the_day = datetime(from_date.year, from_date.month, from_date.day)
        pipeline.insert(0, {"$match": {"created_at": {"$gte": beginning_of_the_day}}})

    if to_date:
        end_of_the_day = datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59, 999)
        pipeline.insert(0, {"$match": {"created_at": {"$lte": end_of_the_day}}})

    filtered_messages = list(client.lgt_admin.filtered_messages.aggregate(pipeline))
    filtered_messages_dic = OrderedDict()

    for item in filtered_messages:
        filtered_messages_dic[str(item["_id"])] = item["count"]

    return filtered_messages_dic


def get_contacts_aggregated_analytics(from_date: datetime = None, to_date: datetime = None):
    pipeline = [
        {
            '$group': {
                '_id': {
                    'user_id': '$user_id',
                    'sender_id': '$message.sender_id'
                },
                'count': {
                    '$sum': 1
                }
            }
        }, {
            '$project': {
                'user_id': '$_id.user_id',
                'sender_id': '$_id.sender_id',
                'count': 1,
                '_id': 0
            }
        }, {
            '$group': {
                '_id': '$user_id',
                'contacts_count': {
                    '$sum': 1
                }
            }
        }
    ]

    if from_date:
        beginning_of_the_day = datetime(from_date.year, from_date.month, from_date.day, 0, 0, 0, 0)
        pipeline.insert(0, {"$match": {"created_at": {"$gte": beginning_of_the_day}}})

    if to_date:
        end_of_the_day = datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59, 999)
        pipeline.insert(0, {"$match": {"created_at": {"$lte": end_of_the_day}}})

    contact_saved = list(client.lgt_admin.user_leads.aggregate(pipeline))
    contact_saved_dic = OrderedDict()
    for item in contact_saved:
        contact_saved_dic[str(item["_id"])] = item["contacts_count"]

    return contact_saved_dic


def get_total_active_bots_global_analytics(from_date: datetime = None, to_date: datetime = None):
    active_bot_dates = []
    while from_date <= to_date:
        active_bot_dates.append(from_date)
        from_date += timedelta(days=1)
    pipeline = [
        {
            '$match': {
                'created_at': {
                    '$lte': to_date
                },
                'deleted': False
            }
        }, {
            '$addFields': {
                'created_at_formatted': {
                    '$dateToString': {
                        'format': '%Y-%m-%d',
                        'date': '$created_at'
                    }
                }
            }
        }, {
            '$group': {
                '_id': {
                    'source': '$source.source_id',
                    'created_at': '$created_at_formatted'
                },
                'count': {
                    '$sum': 1
                }
            }
        }, {
            '$sort': {
                '_id': 1
            }
        }
    ]
    bots = list(client.lgt_admin.dedicated_bots.aggregate(pipeline))
    response = {}
    count = 0
    name = ""
    for date in active_bot_dates:
        for bot in bots:
            bot_date = datetime.strptime(bot["_id"]["created_at"], "%Y-%m-%d")
            if bot_date <= date:
                if bot["_id"]["source"] == name:
                    continue
                else:
                    count += 1
            name = bot["_id"]["source"]
        response[str(date.date())] = count
        count = 0

    return response


def get_bots_aggregated_analytics(from_date: datetime = None,
                                  to_date: datetime = None,
                                  bot_ids: Optional[List[str]] = None,
                                  configs: Optional[List[str]] = None):
    pipeline = [
        {
            "$group": {
                "_id": "$source.source_id",
                "count": {"$sum": 1}
            }
        },
        {"$limit": 1000}
    ]

    if from_date:
        beginning_of_the_day = datetime(from_date.year, from_date.month, from_date.day, 0, 0, 0, 0)
        pipeline.insert(0, {"$match": {"created_at": {"$gte": beginning_of_the_day}}})

    if to_date:
        end_of_the_day = datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59, 999)
        pipeline.insert(0, {"$match": {"created_at": {"$lte": end_of_the_day}}})

    if bot_ids is not None:
        pipeline.insert(0, {"$match": {"extra_ids": {"$in": bot_ids}}})

    received_messages = list(db.get_collection('received_messages').aggregate(pipeline))

    if configs is not None:
        pipeline.insert(0, {"$match": {"attributes": {"$in": configs}}})

    filtered_messages = list(db.get_collection('filtered_messages').aggregate(pipeline))
    received_messages_dic = OrderedDict()
    filtered_messages_dic = OrderedDict()

    for item in received_messages:
        received_messages_dic[item["_id"]] = item["count"]

    for item in filtered_messages:
        filtered_messages_dic[item["_id"]] = item["count"]

    return received_messages_dic, filtered_messages_dic


def get_users_aggregated_analytics(event_type: str = 'user-lead-extended',
                                   from_date: datetime = None,
                                   to_date: datetime = None,
                                   email: str = None):
    pipeline = [
        {
            "$group": {
                "_id": "$name",
                "count": {"$sum": 1}
            }
        },
        {"$limit": 1000}
    ]

    if email:
        pipeline.insert(0, {"$match": {"name": email}})

    if from_date:
        beginning_of_the_day = datetime(from_date.year, from_date.month, from_date.day, 0, 0, 0, 0)
        pipeline.insert(0, {"$match": {"created_at": {"$gte": beginning_of_the_day}}})

    if to_date:
        end_of_the_day = datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59, 999)
        pipeline.insert(0, {"$match": {"created_at": {"$lte": end_of_the_day}}})

    read_messages = list(db[event_type].aggregate(pipeline))
    read_messages_dic = OrderedDict()

    for item in read_messages:
        read_messages_dic[item["_id"]] = item["count"]

    return read_messages_dic


def get_user_date_aggregated_analytics(email=None, event_type: str = 'user-lead-extended',
                                       started_at: datetime = None,
                                       ended_at: datetime = None):
    pipeline = _build_date_aggregated_analytics_pipeline(email=email, started_at=started_at, ended_at=ended_at)

    messages = list(db[event_type].aggregate(pipeline))
    messages_dic = _create_result_dic(started_at, ended_at)

    for item in messages:
        str_date = f'{item["_id"].year}-{item["_id"].month:02d}-{item["_id"].day:02d}'
        messages_dic[str_date] = item["count"]

    return messages_dic


def get_user_read_count(lead_ids: [str]):
    pipeline = [
        {
            "$group":
                {
                    "_id": "$data",
                    "count": {"$sum": 1}
                }
        },
        {
            "$match": {
                "_id": {"$in": lead_ids}
            }
        }
    ]
    messages = list(db['user-lead-extended'].aggregate(pipeline))
    result = dict()

    for message in messages:
        result[message['_id']] = message['count']

    return result


def get_events_leads(email, event, from_date, to_date=None):
    pipeline = {
        'name': email,
        'created_at': {'$gte': from_date}
    }

    if to_date:
        end = datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59, tzinfo=tz.tzutc())
        pipeline['created_at']['$lte'] = end

    return list(db[event].find(pipeline))


def get_total_analytic_followup_up_date(from_date, to_date=None):
    beginning_of_the_day = datetime(from_date.year, from_date.month, from_date.day, 0, 0, 0, 0)
    end_of_the_day = datetime(to_date.year, to_date.month, to_date.day, 23, 59, 59, 999)
    pipeline = [
        {
            "$match": {
                "followup_date": {
                    "$gte": beginning_of_the_day,
                    "$lte": end_of_the_day
                }
            }
        },
        {
            "$group": {
                "_id": "$_id",
                "count": {"$sum": 1}
            }
        }
    ]
    followup_analytic = list(client.lgt_admin.user_leads.aggregate(pipeline))

    followup_analytic_dic = {item["_id"]: item["count"] for item in followup_analytic}

    return followup_analytic_dic
