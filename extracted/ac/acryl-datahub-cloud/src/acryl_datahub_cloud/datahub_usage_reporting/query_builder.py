from datetime import datetime, timedelta
from typing import Dict


class QueryBuilder:
    @staticmethod
    def get_dataset_entities_query() -> Dict:
        return {
            # "sort": [{"urn": {"order": "asc"}}],
            "_source": {
                "includes": [
                    "urn",
                    "lastModifiedAt",
                    "removed",
                    "siblings",
                    "typeNames",
                    "combinedSearchRankingMultiplier",
                ]
            },
        }

    @staticmethod
    def get_query_entities_query(days: int) -> Dict:
        thirty_days_ago = datetime.now() - timedelta(days=days)
        thirty_days_ago = thirty_days_ago.replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        epoch_ms = int(thirty_days_ago.timestamp() * 1000)

        return {
            # "sort": [{"urn": {"order": "asc"}}],
            "_source": {"includes": ["urn", "lastModifiedAt", "platform", "removed"]},
            "query": {
                "bool": {
                    "filter": [
                        {"bool": {"must_not": [{"term": {"source": "MANUAL"}}]}},
                        {"exists": {"field": "platform"}},
                        {
                            "bool": {
                                "should": [
                                    {
                                        "bool": {
                                            "filter": [
                                                {"exists": {"field": "lastModifiedAt"}},
                                                {
                                                    "range": {
                                                        "lastModifiedAt": {
                                                            "gte": epoch_ms
                                                        }
                                                    }
                                                },
                                            ]
                                        }
                                    },
                                    {
                                        "bool": {
                                            "must_not": {
                                                "exists": {"field": "lastModifiedAt"}
                                            },
                                            "filter": {
                                                "range": {
                                                    "createdAt": {"gte": epoch_ms}
                                                }
                                            },
                                        }
                                    },
                                ],
                                "minimum_should_match": 1,
                            }
                        },
                    ]
                }
            },
        }

    @staticmethod
    def get_upstreams_query() -> Dict:
        return {
            # "sort": [{"destination.urn": {"order": "asc"}}],
            "_source": {"includes": ["source.urn", "destination.urn"]},
            "query": {
                "bool": {
                    "must": [
                        {"terms": {"destination.entityType": ["dataset"]}},
                        {"terms": {"source.entityType": ["dataset"]}},
                    ]
                }
            },
        }

    @staticmethod
    def get_dashboard_usage_query(days: int) -> Dict:
        return {
            # "sort": [{"urn": {"order": "asc"}}],
            "_source": {
                "includes": [
                    "timestampMillis",
                    "systemMetadata.lastObserved",
                    "urn",
                    "eventGranularity",
                    "viewsCount",
                    "uniqueUserCount",
                    "event.userCounts",
                ]
            },
            "query": {
                "bool": {
                    "filter": [
                        {
                            "range": {
                                "@timestamp": {"gte": f"now-{days}d", "lt": "now/d"}
                            }
                        },
                        {"term": {"isExploded": False}},
                    ]
                }
            },
        }

    @staticmethod
    def get_document_usage_query(days: int) -> Dict:
        return {
            # "sort": [{"urn": {"order": "asc"}}],
            "_source": {
                "includes": [
                    "timestampMillis",
                    "systemMetadata.lastObserved",
                    "urn",
                    "eventGranularity",
                    "viewsCount",
                    "agentViewsCount",
                    "uniqueUserCount",
                    "event.userCounts",
                ]
            },
            "query": {
                "bool": {
                    "filter": [
                        {
                            "range": {
                                "@timestamp": {"gte": f"now-{days}d", "lt": "now/d"}
                            }
                        },
                        {"term": {"isExploded": False}},
                    ]
                }
            },
        }

    @staticmethod
    def get_document_view_events_query(days: int) -> Dict:
        # Human document reads: EntityViewEvent rows for urn:li:document:* in the
        # datahub_usage_event analytics index. entityUrn is dynamically mapped
        # (text + .keyword); the prefix must target the .keyword sub-field, since a
        # prefix on the analyzed text field tokenizes on ":" and matches nothing.
        return {
            "_source": {"includes": ["timestamp", "entityUrn", "actorUrn"]},
            "query": {
                "bool": {
                    "filter": [
                        {"term": {"type": "EntityViewEvent"}},
                        {"prefix": {"entityUrn.keyword": "urn:li:document:"}},
                        {
                            "range": {
                                "@timestamp": {"gte": f"now-{days}d/d", "lt": "now/d"}
                            }
                        },
                    ]
                }
            },
        }

    @staticmethod
    def get_document_agent_read_events_query(days: int) -> Dict:
        # Agent document reads: ToolInvocation rows that returned a document urn in
        # tool_result_urns. The .keyword prefix pushes the document filter into ES
        # (the field is dynamically mapped text + .keyword). tool_result_urns is
        # added by the ToolInvocationEvent URN-capture change; until that lands the
        # field is absent and the prefix matches nothing, so this returns nothing.
        # conversation_urn / session_id let us de-dupe reads per conversation (a
        # document surfaced across several tool calls in one conversation is one read).
        return {
            "_source": {
                "includes": [
                    "timestamp",
                    "tool_result_urns",
                    "actorUrn",
                    "conversation_urn",
                    "session_id",
                ]
            },
            "query": {
                "bool": {
                    "filter": [
                        {"term": {"type": "ToolInvocation"}},
                        {"prefix": {"tool_result_urns.keyword": "urn:li:document:"}},
                        {
                            "range": {
                                "@timestamp": {"gte": f"now-{days}d/d", "lt": "now/d"}
                            }
                        },
                    ]
                }
            },
        }

    @staticmethod
    def get_dataset_usage_query(days: int) -> Dict:
        return {
            # "sort": [{"urn": {"order": "asc"}}],
            "_source": {
                "includes": [
                    "timestampMillis",
                    "urn",
                    "eventGranularity",
                    "totalSqlQueries",
                    "uniqueUserCount",
                    "event.userCounts",
                    "platform",
                ]
            },
            "query": {
                "bool": {
                    "filter": [
                        {
                            "range": {
                                "@timestamp": {"gte": f"now-{days}d/d", "lt": "now/d"}
                            }
                        },
                        {"term": {"isExploded": False}},
                        {"range": {"totalSqlQueries": {"gt": 0}}},
                    ]
                }
            },
        }

    @staticmethod
    def get_dataset_write_usage_raw_query(days: int) -> Dict:
        return {
            # "sort": [{"urn": {"order": "asc"}}, {"@timestamp": {"order": "asc"}}],
            "_source": {
                "includes": [
                    "urn"  # Only field needed for platform extraction via regex
                ]
            },
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "@timestamp": {"gte": f"now-{days}d/d", "lte": "now/d"}
                            }
                        },
                        {"terms": {"operationType": ["INSERT", "UPDATE", "CREATE"]}},
                    ]
                }
            },
        }

    @staticmethod
    def get_dataset_write_usage_composite_query(days: int) -> Dict:
        return {
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "@timestamp": {"gte": f"now-{days}d/d", "lte": "now/d"}
                            }
                        },
                        {"terms": {"operationType": ["INSERT", "UPDATE", "CREATE"]}},
                    ]
                }
            },
            "aggs": {
                "urn_count": {
                    "composite": {
                        "sources": [
                            {"dataset_operationaspect_v1": {"terms": {"field": "urn"}}}
                        ]
                    }
                }
            },
        }

    @staticmethod
    def get_query_usage_query(days: int) -> Dict:
        return {
            # "sort": [{"urn": {"order": "asc"}}],
            "_source": {
                "includes": [
                    "timestampMillis",
                    "systemMetadata.lastObserved",
                    "urn",
                    "eventGranularity",
                    "queryCount",
                    "uniqueUserCount",
                    "event.userCounts",
                ]
            },
            "query": {
                "bool": {
                    "filter": [
                        {
                            "range": {
                                "@timestamp": {"gte": f"now-{days}d/d", "lt": "now/d"}
                            }
                        },
                        {"term": {"isExploded": False}},
                    ]
                }
            },
        }
