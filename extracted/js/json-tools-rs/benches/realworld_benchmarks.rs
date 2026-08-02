use criterion::{criterion_group, criterion_main, Criterion};
use json_tools_rs::JSONTools;
use std::hint::black_box;
use std::time::Duration;

// ============================================================================
// PART 3: REAL-WORLD DATASET BENCHMARKS
// Tests with actual API response formats and log structures
// ============================================================================

mod realworld_data {
    /// AWS CloudTrail Log Event
    pub fn aws_cloudtrail() -> &'static str {
        r#"{
            "Records": [
                {
                    "eventVersion": "1.08",
                    "userIdentity": {
                        "type": "IAMUser",
                        "principalId": "AIDAI23HXA2QN5EXAMPLE",
                        "arn": "arn:aws:iam::123456789012:user/Alice",
                        "accountId": "123456789012",
                        "accessKeyId": "AKIAIOSFODNN7EXAMPLE",
                        "userName": "Alice",
                        "sessionContext": {
                            "attributes": {
                                "mfaAuthenticated": "false",
                                "creationDate": "2024-01-10T10:00:00Z"
                            }
                        }
                    },
                    "eventTime": "2024-01-10T10:05:32Z",
                    "eventSource": "ec2.amazonaws.com",
                    "eventName": "RunInstances",
                    "awsRegion": "us-east-1",
                    "sourceIPAddress": "192.0.2.1",
                    "userAgent": "aws-cli/2.0.0",
                    "requestParameters": {
                        "instancesSet": {
                            "items": [
                                {
                                    "instanceType": "t2.micro",
                                    "minCount": 1,
                                    "maxCount": 1,
                                    "imageId": "ami-12345678"
                                }
                            ]
                        },
                        "monitoring": {
                            "enabled": false
                        }
                    },
                    "responseElements": {
                        "instancesSet": {
                            "items": [
                                {
                                    "instanceId": "i-0123456789abcdef0",
                                    "instanceState": {
                                        "code": 0,
                                        "name": "pending"
                                    },
                                    "privateIpAddress": "10.0.1.100",
                                    "vpcId": "vpc-12345678"
                                }
                            ]
                        }
                    },
                    "requestID": "12345678-1234-1234-1234-123456789012",
                    "eventID": "87654321-4321-4321-4321-210987654321",
                    "readOnly": false,
                    "eventType": "AwsApiCall",
                    "managementEvent": true,
                    "recipientAccountId": "123456789012"
                }
            ]
        }"#
    }

    /// GitHub API Response (Repository)
    pub fn github_api_repo() -> &'static str {
        r#"{
            "id": 123456789,
            "node_id": "MDEwOlJlcG9zaXRvcnkxMjM0NTY3ODk=",
            "name": "awesome-project",
            "full_name": "octocat/awesome-project",
            "private": false,
            "owner": {
                "login": "octocat",
                "id": 1,
                "node_id": "MDQ6VXNlcjE=",
                "avatar_url": "https://github.com/images/error/octocat_happy.gif",
                "gravatar_id": "",
                "url": "https://api.github.com/users/octocat",
                "type": "User",
                "site_admin": false
            },
            "html_url": "https://github.com/octocat/awesome-project",
            "description": "An awesome project for doing awesome things",
            "fork": false,
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-10T12:00:00Z",
            "pushed_at": "2024-01-10T11:30:00Z",
            "size": 10240,
            "stargazers_count": 42,
            "watchers_count": 42,
            "language": "Rust",
            "has_issues": true,
            "has_projects": true,
            "has_downloads": true,
            "has_wiki": true,
            "has_pages": false,
            "forks_count": 10,
            "open_issues_count": 3,
            "default_branch": "main",
            "permissions": {
                "admin": true,
                "maintain": true,
                "push": true,
                "triage": true,
                "pull": true
            },
            "topics": [
                "rust",
                "json",
                "performance"
            ],
            "license": {
                "key": "mit",
                "name": "MIT License",
                "spdx_id": "MIT",
                "url": "https://api.github.com/licenses/mit",
                "node_id": "MDc6TGljZW5zZTEz"
            }
        }"#
    }

    /// Kubernetes Pod Manifest
    pub fn kubernetes_pod() -> &'static str {
        r#"{
            "apiVersion": "v1",
            "kind": "Pod",
            "metadata": {
                "name": "nginx-pod",
                "namespace": "default",
                "labels": {
                    "app": "nginx",
                    "environment": "production",
                    "tier": "frontend"
                },
                "annotations": {
                    "prometheus.io/scrape": "true",
                    "prometheus.io/port": "9090"
                }
            },
            "spec": {
                "containers": [
                    {
                        "name": "nginx",
                        "image": "nginx:1.21",
                        "ports": [
                            {
                                "containerPort": 80,
                                "protocol": "TCP"
                            }
                        ],
                        "env": [
                            {
                                "name": "ENVIRONMENT",
                                "value": "production"
                            },
                            {
                                "name": "LOG_LEVEL",
                                "value": "info"
                            }
                        ],
                        "resources": {
                            "requests": {
                                "memory": "64Mi",
                                "cpu": "250m"
                            },
                            "limits": {
                                "memory": "128Mi",
                                "cpu": "500m"
                            }
                        },
                        "volumeMounts": [
                            {
                                "name": "config",
                                "mountPath": "/etc/nginx/nginx.conf",
                                "subPath": "nginx.conf"
                            }
                        ]
                    }
                ],
                "volumes": [
                    {
                        "name": "config",
                        "configMap": {
                            "name": "nginx-config"
                        }
                    }
                ]
            },
            "status": {
                "phase": "Running",
                "conditions": [
                    {
                        "type": "Ready",
                        "status": "True",
                        "lastTransitionTime": "2024-01-10T10:00:00Z"
                    }
                ],
                "podIP": "10.244.0.5",
                "startTime": "2024-01-10T09:55:00Z"
            }
        }"#
    }

    /// Elasticsearch/OpenSearch Document
    pub fn elasticsearch_doc() -> &'static str {
        r#"{
            "_index": "logs-2024.01",
            "_type": "_doc",
            "_id": "AWxyz123",
            "_version": 1,
            "_score": 1.0,
            "_source": {
                "@timestamp": "2024-01-10T12:00:00.123Z",
                "level": "ERROR",
                "logger": "com.example.Application",
                "message": "Connection timeout",
                "thread": "http-nio-8080-exec-5",
                "context": {
                    "requestId": "req-123-456",
                    "userId": "user-789",
                    "sessionId": "sess-abc-def"
                },
                "exception": {
                    "class": "java.net.SocketTimeoutException",
                    "message": "Read timed out",
                    "stacktrace": [
                        "at java.net.SocketInputStream.socketRead0(Native Method)",
                        "at java.net.SocketInputStream.read(SocketInputStream.java:150)"
                    ]
                },
                "tags": ["error", "timeout", "database"],
                "host": {
                    "name": "app-server-01",
                    "ip": "192.168.1.100"
                },
                "application": {
                    "name": "my-app",
                    "version": "1.2.3",
                    "environment": "production"
                }
            },
            "fields": {
                "@timestamp": ["2024-01-10T12:00:00.123Z"]
            }
        }"#
    }

    /// Stripe API Payment Intent
    pub fn stripe_payment_intent() -> &'static str {
        r#"{
            "id": "pi_1234567890",
            "object": "payment_intent",
            "amount": 2000,
            "amount_capturable": 0,
            "amount_received": 2000,
            "currency": "usd",
            "customer": "cus_ABC123",
            "description": "Payment for order #12345",
            "status": "succeeded",
            "created": 1704888000,
            "livemode": false,
            "metadata": {
                "order_id": "12345",
                "customer_name": "John Doe",
                "product_ids": "prod_1,prod_2,prod_3"
            },
            "charges": {
                "object": "list",
                "data": [
                    {
                        "id": "ch_1234567890",
                        "amount": 2000,
                        "currency": "usd",
                        "status": "succeeded",
                        "paid": true,
                        "billing_details": {
                            "address": {
                                "city": "San Francisco",
                                "country": "US",
                                "line1": "123 Main St",
                                "line2": null,
                                "postal_code": "94102",
                                "state": "CA"
                            },
                            "email": "john@example.com",
                            "name": "John Doe",
                            "phone": "+15550100"
                        },
                        "payment_method_details": {
                            "card": {
                                "brand": "visa",
                                "last4": "4242",
                                "exp_month": 12,
                                "exp_year": 2025
                            },
                            "type": "card"
                        }
                    }
                ],
                "has_more": false,
                "total_count": 1
            }
        }"#
    }

    /// Twitter/X API Tweet
    pub fn twitter_tweet() -> &'static str {
        r#"{
            "data": {
                "id": "1234567890123456789",
                "text": "Just shipped a new feature! 🚀 #rust #programming",
                "author_id": "987654321",
                "created_at": "2024-01-10T12:00:00.000Z",
                "edit_history_tweet_ids": ["1234567890123456789"],
                "public_metrics": {
                    "retweet_count": 42,
                    "reply_count": 15,
                    "like_count": 128,
                    "quote_count": 7,
                    "bookmark_count": 23,
                    "impression_count": 5432
                },
                "entities": {
                    "hashtags": [
                        {
                            "start": 35,
                            "end": 40,
                            "tag": "rust"
                        },
                        {
                            "start": 41,
                            "end": 53,
                            "tag": "programming"
                        }
                    ]
                },
                "referenced_tweets": [],
                "attachments": {
                    "media_keys": []
                }
            },
            "includes": {
                "users": [
                    {
                        "id": "987654321",
                        "name": "John Developer",
                        "username": "johndev",
                        "created_at": "2010-01-01T00:00:00.000Z",
                        "verified": false,
                        "public_metrics": {
                            "followers_count": 1234,
                            "following_count": 567,
                            "tweet_count": 8901,
                            "listed_count": 45
                        }
                    }
                ]
            }
        }"#
    }
}

// ============================================================================
// REAL-WORLD BENCHMARKS
// ============================================================================

fn realworld_01_aws_cloudtrail(c: &mut Criterion) {
    let mut group = c.benchmark_group("realworld_01_aws_cloudtrail");
    group.measurement_time(Duration::from_secs(5));

    let json = realworld_data::aws_cloudtrail();

    // Basic flatten
    group.bench_function("flatten", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    // Typical CloudTrail processing
    group.bench_function("typical_processing", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .separator("_")
                .lowercase_keys(true)
                .remove_nulls(true)
                .auto_convert_types(true)
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    // Extract key fields
    group.bench_function("extract_key_fields", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .key_replacement("r'^Records\\.0\\.'", "")
                .remove_empty_objects(true)
                .remove_empty_arrays(true)
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.finish();
}

fn realworld_02_github_api(c: &mut Criterion) {
    let mut group = c.benchmark_group("realworld_02_github_api");
    group.measurement_time(Duration::from_secs(5));

    let json = realworld_data::github_api_repo();

    // Basic flatten
    group.bench_function("flatten", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    // Convert snake_case to camelCase
    group.bench_function("snake_to_camel", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .key_replacement("r'_([a-z])'", "${1}")
                .remove_nulls(true)
                .auto_convert_types(true)
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    // Extract metrics
    group.bench_function("extract_metrics", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .normal()
                .remove_nulls(true)
                .remove_empty_strings(true)
                .auto_convert_types(true)
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.finish();
}

fn realworld_03_kubernetes(c: &mut Criterion) {
    let mut group = c.benchmark_group("realworld_03_kubernetes");
    group.measurement_time(Duration::from_secs(5));

    let json = realworld_data::kubernetes_pod();

    // Basic flatten
    group.bench_function("flatten", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    // Process for monitoring
    group.bench_function("monitoring_format", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .separator("_")
                .lowercase_keys(true)
                .auto_convert_types(true)
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    // Extract labels and annotations
    group.bench_function("extract_metadata", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .key_replacement("r'^metadata\\.(labels|annotations)\\.'", "$1_")
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.finish();
}

fn realworld_04_elasticsearch(c: &mut Criterion) {
    let mut group = c.benchmark_group("realworld_04_elasticsearch");
    group.measurement_time(Duration::from_secs(5));

    let json = realworld_data::elasticsearch_doc();

    // Basic flatten
    group.bench_function("flatten", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    // Log processing
    group.bench_function("log_processing", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .key_replacement("r'^_source\\.'", "")
                .remove_nulls(true)
                .auto_convert_types(true)
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    // Flatten for CSV export
    group.bench_function("csv_export_prep", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .separator("_")
                .lowercase_keys(true)
                .remove_empty_arrays(true)
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.finish();
}

fn realworld_05_stripe_api(c: &mut Criterion) {
    let mut group = c.benchmark_group("realworld_05_stripe_api");
    group.measurement_time(Duration::from_secs(5));

    let json = realworld_data::stripe_payment_intent();

    // Basic flatten
    group.bench_function("flatten", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    // Process for database storage
    group.bench_function("database_prep", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .separator("_")
                .lowercase_keys(true)
                .remove_nulls(true)
                .auto_convert_types(true)
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    // Extract billing info
    group.bench_function("extract_billing", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .key_replacement("r'^charges\\.data\\.0\\.'", "charge_")
                .remove_nulls(true)
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.finish();
}

fn realworld_06_twitter_api(c: &mut Criterion) {
    let mut group = c.benchmark_group("realworld_06_twitter_api");
    group.measurement_time(Duration::from_secs(5));

    let json = realworld_data::twitter_tweet();

    // Basic flatten
    group.bench_function("flatten", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    // Analytics processing
    group.bench_function("analytics_processing", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .flatten()
                .separator("_")
                .key_replacement("r'^data\\.'", "tweet_")
                .auto_convert_types(true)
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    // Extract metrics only
    group.bench_function("extract_metrics", |b| {
        b.iter(|| {
            let result = JSONTools::new()
                .normal()
                .key_replacement("r'public_metrics\\.'", "")
                .auto_convert_types(true)
                .remove_empty_arrays(true)
                .execute(black_box(json))
                .expect("Failed");
            black_box(result);
        });
    });

    group.finish();
}

criterion_group!(
    realworld_benches,
    realworld_01_aws_cloudtrail,
    realworld_02_github_api,
    realworld_03_kubernetes,
    realworld_04_elasticsearch,
    realworld_05_stripe_api,
    realworld_06_twitter_api,
);

criterion_main!(realworld_benches);
