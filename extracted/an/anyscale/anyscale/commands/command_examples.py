JOB_STATUS_EXAMPLE = """\
id: prodjob_abc123
name: my-job
state: STARTING
runs:
- name: raysubmit_abc123
  state: SUCCEEDED
creator_id: usr_abc123
created_at: 2026-01-01 00:00:00+00:00
updated_at: 2026-01-01 00:05:00+00:00
status_updated_at: 2026-01-01 00:05:00+00:00
"""

JOB_TERMINATE_EXAMPLE = """\
Marked job 'my-job' for termination
Query the status of the job with `anyscale job status --name my-job`.
"""

JOB_ARCHIVE_EXAMPLE = """\
Job prodjob_abc123 is archived.
"""

JOB_DELETE_EXAMPLE = """\
Job 'my-job' (ID: prodjob_abc123) has been deleted.
"""

JOB_LOGS_EXAMPLE = """\
2024-08-23 20:31:10,913 INFO job_manager.py:531 -- Runtime env is setting up.
hello world
"""

JOB_WAIT_EXAMPLE = """\
Job 'my-job' transitioned from STARTING to SUCCEEDED
Job 'my-job' reached target state, exiting
"""

JOB_LIST_EXAMPLE = """\
┏━━━━━━━━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━┓
┃ ID             ┃ Name   ┃ State     ┃ Created At                ┃ Project ┃ Entrypoint     ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━┩
│ prodjob_abc123 │ my-job │ SUCCEEDED │ 2026-01-01T00:00:00+00:00 │ default │ python main.py │
└────────────────┴────────┴───────────┴───────────────────────────┴─────────┴────────────────┘
"""

JOB_TAGS_ADD_EXAMPLE = """\
Tags updated for job 'my-job'.
"""

JOB_TAGS_REMOVE_EXAMPLE = """\
Removed tag keys ['owner', 'env'] from job 'my-job'.
"""

JOB_TAGS_LIST_EXAMPLE = """\
       Tags
┏━━━━━━━┳━━━━━━━━━┓
┃ KEY   ┃ VALUE   ┃
┡━━━━━━━╇━━━━━━━━━┩
│ env   │ staging │
│ owner │ alice   │
└───────┴─────────┘
"""
JOB_QUEUE_LIST = """\
┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ NAME         ┃ ID             ┃ STATE      ┃ CREATOR EMAIL            ┃ PROJECT ID      ┃ CREATED AT                 ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ my-queue     │ jq_abc123      │ ACTIVE     │ someone@myorg.com        │ prj_abc123      │ 2026-01-01 00:00:00        │
└──────────────┴────────────────┴────────────┴──────────────────────────┴─────────────────┴────────────────────────────┘
"""

JOB_QUEUE_STATUS = """\
┏━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ NAME      ┃ ID         ┃ STATE   ┃ CREATOR EMAIL      ┃ PROJECT ID  ┃ CREATED AT           ┃ MAX CONCURRENCY  ┃ IDLE TIMEOUT S  ┃ CLOUD ID    ┃ USER PROVIDED ID ┃ EXECUTION MODE ┃ TOTAL JOBS ┃ ACTIVE JOBS ┃ SUCCESSFUL JOBS ┃ FAILED JOBS ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ my-queue  │ jq_abc123  │ ACTIVE  │ someone@myorg.com  │ prj_abc123  │ 2026-01-01 00:00:00  │ 3                │ 5000            │ cld_abc123  │ my-queue         │ PRIORITY       │ 6          │ 0           │ 6               │ 0           │
└───────────┴────────────┴─────────┴────────────────────┴─────────────┴──────────────────────┴──────────────────┴─────────────────┴─────────────┴──────────────────┴────────────────┴────────────┴─────────────┴─────────────────┴─────────────┘
"""

JOB_QUEUE_UPDATE = """\
┏━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┓
┃ NAME      ┃ ID         ┃ STATE   ┃ CREATOR EMAIL      ┃ PROJECT ID  ┃ CREATED AT           ┃ MAX CONCURRENCY  ┃ IDLE TIMEOUT S  ┃ CLOUD ID    ┃ USER PROVIDED ID ┃ EXECUTION MODE ┃ TOTAL JOBS ┃ ACTIVE JOBS ┃ SUCCESSFUL JOBS ┃ FAILED JOBS ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━┩
│ my-queue  │ jq_abc123  │ ACTIVE  │ someone@myorg.com  │ prj_abc123  │ 2026-01-01 00:00:00  │ 5                │ 5000            │ cld_abc123  │ my-queue         │ PRIORITY       │ 6          │ 0           │ 6               │ 0           │
└───────────┴────────────┴─────────┴────────────────────┴─────────────┴──────────────────────┴──────────────────┴─────────────────┴─────────────┴──────────────────┴────────────────┴────────────┴─────────────┴─────────────────┴─────────────┘
"""

JOB_QUEUE_TAGS_ADD_EXAMPLE = """\
Tags updated for job queue 'my-queue'.
"""

JOB_QUEUE_TAGS_REMOVE_EXAMPLE = """\
Removed tag keys ['team', 'priority'] from job queue 'my-queue'.
"""

JOB_QUEUE_TAGS_LIST_EXAMPLE = """\
        Tags
┏━━━━━━━━━━┳━━━━━━━┓
┃ KEY      ┃ VALUE ┃
┡━━━━━━━━━━╇━━━━━━━┩
│ priority │ high  │
│ team     │ data  │
└──────────┴───────┘
"""

JOB_QUEUE_ARCHIVE_EXAMPLE = """\
Job queue 'jq_abc123' has been archived.
Query the status with `anyscale job-queue status --id jq_abc123`.
"""

JOB_QUEUE_TERMINATE_EXAMPLE = """\
Job queue 'jq_abc123' has been marked for termination.
Query the status with `anyscale job-queue status --id jq_abc123`.
"""

JOB_QUEUE_DELETE_EXAMPLE = """\
Job queue 'jq_abc123' has been deleted.
"""

SCHEDULE_APPLY_EXAMPLE = """\
Schedule 'my-schedule' submitted, ID: 'cronjob_abc123'.
"""

SCHEDULE_LIST_EXAMPLE = """\
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━┓
┃ ID             ┃ Name        ┃ State   ┃ Cron Expression ┃ Timezone ┃ Project ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━┩
│ cronjob_abc123 │ my-schedule │ ENABLED │ 0 0 * * *       │ UTC      │ default │
└────────────────┴─────────────┴─────────┴─────────────────┴──────────┴─────────┘
"""

SCHEDULE_PAUSE_EXAMPLE = """\
Set schedule 'my-schedule' to state DISABLED
"""

SCHEDULE_RESUME_EXAMPLE = """\
Set schedule 'my-schedule' to state ENABLED
"""

SCHEDULE_STATUS_EXAMPLE = """\
id: cronjob_abc123
name: my-schedule
state: ENABLED
"""

SCHEDULE_RUN_EXAMPLE = """\
Triggered job for schedule 'my-schedule'.
"""

SCHEDULE_URL_EXAMPLE = """\
View your schedule at https://console.anyscale.com/scheduled-jobs/cronjob_abc123
"""

SCHEDULE_DELETE_EXAMPLE = """\
Schedule 'my-schedule' deleted.
"""

WORKSPACE_CREATE_EXAMPLE = """\
Workspace created successfully id: expwrk_abc123
"""

WORKSPACE_START_EXAMPLE = """\
Starting workspace 'my-workspace'
"""

WORKSPACE_TERMINATE_EXAMPLE = """\
Terminating workspace 'my-workspace'
"""

WORKSPACE_STATUS_EXAMPLE = """\
STARTING
"""

WORKSPACE_WAIT_EXAMPLE = """\
Workspace 'expwrk_abc123' reached target state, exiting
"""

WORKSPACE_SSH_EXAMPLE = """\
(base) ray@ip-10-0-0-1:~/default$
"""

WORKSPACE_RUN_COMMAND_EXAMPLE = """\
hello world
"""

WORKSPACE_PULL_EXAMPLE = """\
receiving incremental file list
created directory my-local
./
my-local/
my-local/main.py

sent 118 bytes  received 141 bytes  172.67 bytes/sec
total size is 0  speedup is 0.00
"""

WORKSPACE_PUSH_EXAMPLE = """\
sending incremental file list
my-local/
my-local/main.py

sent 188 bytes  received 39 bytes  151.33 bytes/sec
total size is 0  speedup is 0.00
"""

WORKSPACE_UPDATE_EXAMPLE = """\
Workspace updated successfully id: expwrk_abc123
"""

WORKSPACE_GET_EXAMPLE = """\
┏━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ NAME         ┃ ID            ┃ STATE   ┃ PROJECT    ┃ CLOUD      ┃ CREATED BY        ┃ CREATED AT       ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ my-workspace │ expwrk_abc123 │ RUNNING │ prj_abc123 │ cld_abc123 │ someone@myorg.com │ 2026-01-01 10:30 │
└──────────────┴───────────────┴─────────┴────────────┴────────────┴───────────────────┴──────────────────┘
"""

WORKSPACE_LIST_EXAMPLE = """\
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ NAME           ┃ ID            ┃ STATE    ┃ PROJECT    ┃ CLOUD      ┃ CREATED BY        ┃ CREATED AT       ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ my-workspace-1 │ expwrk_abc123 │ RUNNING  │ prj_abc123 │ cld_abc123 │ someone@myorg.com │ 2026-01-01 10:30 │
│ my-workspace-2 │ expwrk_def456 │ STARTING │ prj_abc123 │ cld_abc123 │ someone@myorg.com │ 2026-01-02 14:20 │
└────────────────┴───────────────┴──────────┴────────────┴────────────┴───────────────────┴──────────────────┘
"""

WORKSPACE_TAGS_ADD_EXAMPLE = """\
Tags updated for workspace 'my-workspace'.
"""

WORKSPACE_TAGS_REMOVE_EXAMPLE = """\
Removed tag keys ['team', 'env'] from workspace 'my-workspace'.
"""

WORKSPACE_TAGS_LIST_EXAMPLE = """\
      Tags
┏━━━━━━┳━━━━━━━┓
┃ KEY  ┃ VALUE ┃
┡━━━━━━╇━━━━━━━┩
│ env  │ prod  │
│ team │ ml    │
└──────┴───────┘
"""

MACHINE_POOL_CREATE_EXAMPLE = """\
Machine pool can-testing has been created successfully (ID mp_abc123).
"""

MACHINE_POOL_UPDATE_EXAMPLE = """\
Updated machine pool 'can-testing'.
"""

MACHINE_POOL_DESCRIBE_EXAMPLE = """\
Machines:
+--------------+--------+-------------+---------+--------------------+-----------------------+--------------------+------------------+---------------------+
| MACHINE ID   | TYPE   | PARTITION   | STATE   | WORKLOAD DETAILS   | WORKLOAD START TIME   | WORKLOAD CREATOR   | WORKLOAD SCORE   | CLOUD INSTANCE ID   |
+==============+========+=============+=========+====================+=======================+====================+==================+=====================+
+--------------+--------+-------------+---------+--------------------+-----------------------+--------------------+------------------+---------------------+
Requests:
+--------+----------------+--------------------+-----------------------+--------------------+--------------------+
| SIZE   | MACHINE TYPE   | WORKLOAD DETAILS   | WORKLOAD START TIME   | WORKLOAD CREATOR   | PARTITION SCORES   |
+========+================+====================+=======================+====================+====================+
+--------+----------------+--------------------+-----------------------+--------------------+--------------------+
"""

MACHINE_POOL_DELETE_EXAMPLE = """\
Deleted machine pool 'can-testing'.
"""

MACHINE_POOL_LIST_EXAMPLE = """\
┌────────────────┬───────────┬──────────┐
│ MACHINE POOL   │ ID        │ Clouds   │
├────────────────┼───────────┼──────────┤
│ can-testing    │ mp_abc123 │ my-cloud │
└────────────────┴───────────┴──────────┘
"""

MACHINE_POOL_ATTACH_EXAMPLE = """\
Attached machine pool 'can-testing' to cloud 'my-cloud'.
"""

MACHINE_POOL_DETACH_EXAMPLE = """\
Detached machine pool 'can-testing' from cloud 'my-cloud'.
"""

RESOURCE_QUOTAS_CREATE_EXAMPLE = """\
Name: my-resource-quota
Cloud name: my-cloud
Project name: my-project
User email: someone@myorg.com
Number of CPUs: 1000
Number of instances: 100
Number of GPUs: 50
Number of accelerators: {'A10G': 10}
Resource quota created successfully ID: rsq_abcdef
"""

RESOURCE_QUOTAS_LIST_EXAMPLE = """\
Resource quotas:
ID       NAME              CLOUD ID    PROJECT ID    USER ID     IS ENABLED    CREATED AT    DELETED AT    QUOTA                                                                                IS SOFT QUOTA
rsq_123  resource-quota-1  cld_abcdef  prj_abcdef    usr_abcdef  True          09/11/2024                  Quota(num_cpus=1000, num_instances=100, num_gpus=50, num_accelerators={'A10G': 10})  False
"""

RESOURCE_QUOTAS_ENABLE_EXAMPLE = """\
Enabled resource quota with ID rsq_abcdef successfully.
"""

RESOURCE_QUOTAS_DISABLE_EXAMPLE = """\
Disabled resource quota with ID rsq_abcdef successfully.
"""

RESOURCE_QUOTAS_DELETE_EXAMPLE = """\
Resource quota with ID rsq_abcdef deleted successfully.
"""

SCHEDULER_CONFIG_APPLY_EXAMPLE = """\
Once applied, all workloads in your organization will be admitted, scheduled, run, or rejected according to this new configuration.

Type "change config" to proceed, or press Ctrl+C to cancel: change config
Applied scheduler config (version 3).
"""

SCHEDULER_CONFIG_GET_EXAMPLE = """\
version: 3
is_active: true
created_at: '2026-04-25T10:00:00Z'
creator_id: usr_abc123
config:
  resource_flavors:
    - name: spot
      requirements:
        - key: market
          operator: in
          values: [spot]
"""

SCHEDULER_CONFIG_LIST_EXAMPLE = """\
VERSION  CREATED AT
3        2026-04-25T10:00:00Z
2        2026-04-20T08:30:00Z
1        2026-04-15T14:00:00Z
"""


COMPUTE_CONFIG_CREATE_EXAMPLE = """\
Created compute config: 'my-compute-config:1'
View the compute config in the UI: 'https://console.anyscale.com/configurations/cluster-computes/cpt_abc123'
"""

COMPUTE_CONFIG_GET_EXAMPLE = """\
name: my-compute-config:1
id: cpt_abc123
config:
  cloud: my-cloud
  head_node:
    instance_type: m5.8xlarge
    resources:
      CPU: 0
      GPU: 0
  worker_nodes:
  - instance_type: m5.8xlarge
    name: m5.8xlarge
    min_nodes: 5
    max_nodes: 5
    market_type: ON_DEMAND
  - instance_type: g4dn.xlarge
    name: g4dn.xlarge
    min_nodes: 1
    max_nodes: 10
    market_type: PREFER_SPOT
  min_resources:
    CPU: 1
    GPU: 1
  max_resources:
    CPU: 6
    GPU: 1
  enable_cross_zone_scaling: false
  flags: {}
"""

COMPUTE_CONFIG_ARCHIVE_EXAMPLE = """\
Compute config is successfully archived.
"""

COMPUTE_CONFIG_LIST_EXAMPLE = """\
Compute configs:
ID          NAME               CLOUD       LAST MODIFIED AT      URL
cpt_abc123  my-compute-config  my-cloud    01/15/2025, 10:30:00  https://console.anyscale.com/configurations/cluster-computes/cpt_abc123
cpt_def456  prod-config        prod-cloud  01/14/2025, 14:22:00  https://console.anyscale.com/configurations/cluster-computes/cpt_def456
"""

IMAGE_BUILD_EXAMPLE = """\
Image built successfully with URI: anyscale/image/my-image:1
"""

IMAGE_GET_EXAMPLE = """\
NAME      LATEST VERSION  LATEST URI                 CREATED BY         CREATED AT
my-image  1               anyscale/image/my-image:1  someone@myorg.com  2026-01-01 18:42
"""

IMAGE_LIST_EXAMPLE = """\
NAME       LATEST VERSION  LATEST URI                  CREATED BY         CREATED AT
my-image   3               anyscale/image/my-image:3   someone@myorg.com  2026-01-01 18:42
workspace  1               anyscale/image/workspace:1  another@myorg.com  2026-01-02 09:15
"""

IMAGE_REGISTER_EXAMPLE = """\
Image registered successfully with URI: anyscale/image/my-image:1
"""

IMAGE_ARCHIVE_EXAMPLE = """\
Image 'my-image' archived successfully.
"""

AGGREGATED_INSTANCE_USAGE_DOWNLOAD_CSV_EXAMPLE = """\
Download complete! File saved to 'aggregated_instance_usage_2024-09-01_2024-09-30.zip'
"""

USER_BATCH_CREATE_EXAMPLE = """\
2 users created.
"""

USER_LIST_EXAMPLE = """\
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ EMAIL             ┃ NAME     ┃ ID         ┃ ROLE         ┃ CREATED AT       ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ someone@myorg.com │ Some One │ usr_abc123 │ collaborator │ 2026-01-01 00:00 │
└───────────────────┴──────────┴────────────┴──────────────┴──────────────────┘
"""

USER_GET_EXAMPLE = """\
┏━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃ EMAIL             ┃ NAME     ┃ ID         ┃ ROLE         ┃ CREATED AT       ┃
┡━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│ someone@myorg.com │ Some One │ usr_abc123 │ collaborator │ 2026-01-01 00:00 │
└───────────────────┴──────────┴────────────┴──────────────┴──────────────────┘
"""

ORGANIZATION_INVITATION_CREATE_EXAMPLE = """\
Organization invitations sent to: someone@myorg.com, other@myorg.com
"""

ORGANIZATION_INVITATION_LIST_EXAMPLE = """\
ID             Email              Created At           Expires At
-------------  -----------------  -------------------  -------------------
orginv_abc123  someone@myorg.com  11/25/2024 10:24 PM  12/02/2024 10:24 PM
"""

ORGANIZATION_INVITATION_DELETE_EXAMPLE = """\
Organization invitation for someone@myorg.com deleted.
"""


PROJECT_ADD_COLLABORATORS_EXAMPLE = """\
Successfully added 3 collaborators to project my-project.
"""


PROJECT_GET_EXAMPLE = """\
id: prj_abc123
name: my-project
description: My project.
created_at: '2026-01-01 00:00:00'
creator_id: usr_abc123
parent_cloud_id: cld_abc123
is_owner: true
is_read_only: false
directory_name: default
is_default: false
"""


PROJECT_LIST_EXAMPLE = """\
┏━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ NAME       ┃ ID         ┃ DESCRIPTION ┃ CREATED AT          ┃ CREATOR    ┃ PARENT CLOUD ID ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ my-project │ prj_abc123 │ My project. │ 2026-01-01 00:00:00 │ usr_abc123 │ cld_abc123      │
└────────────┴────────────┴─────────────┴─────────────────────┴────────────┴─────────────────┘
"""


PROJECT_CREATE_EXAMPLE = """\
Created project 'my-project' with ID: prj_abc123
"""


PROJECT_DELETE_EXAMPLE = """\
Deleted project 'prj_abc123'
"""


PROJECT_GET_DEFAULT_EXAMPLE = """\
id: prj_abc123
name: default
description: My project.
created_at: '2026-01-01 00:00:00'
creator_id: usr_abc123
parent_cloud_id: cld_abc123
is_owner: true
is_read_only: false
directory_name: default
is_default: true
"""


CLOUD_SETUP_K8S_AWS_EXAMPLE = """\
Cloud registered with ID: cld_abc123
Kubernetes cloud 'my-cloud' setup completed successfully!
"""

CLOUD_SETUP_K8S_GCP_EXAMPLE = """\
Cloud registered with ID: cld_abc123
Kubernetes cloud 'my-cloud' setup completed successfully!
"""

CLOUD_SETUP_K8S_CUSTOM_VALUES_EXAMPLE = """\
Generated Helm values file: /path/to/custom-values.yaml
Kubernetes cloud 'my-cloud' setup completed successfully!
"""

CLOUD_ADD_COLLABORATORS_EXAMPLE = """\
Successfully added 2 collaborators to cloud my-cloud.
"""


CLOUD_RESOURCE_CREATE_EXAMPLE = """\
Successfully created cloud resource my-new-resource in cloud my-cloud!
"""

CLOUD_RESOURCE_DELETE_EXAMPLE = """\
Successfully removed resource my-resource from cloud my-cloud!
"""

CLOUD_GET_CLOUD_EXAMPLE = """\
name: my-cloud
id: cld_abc123
resources:
- cloud_resource_id: cldrsrc_abc123
  name: vm-aws-us-west-2
  provider: AWS
  compute_stack: VM
  region: us-west-2
  networking_mode: PUBLIC
"""

CLOUD_STATUS_EXAMPLE = """\
name: my-cloud
id: cld_abc123
created_at: 2026-01-01 00:00:00+00:00
is_default: true
resources:
- cloud_resource_id: cldrsrc_abc123
  name: k8s-aws-us-west-2
  provider: AWS
  compute_stack: K8S
  region: us-west-2
  operator_status: HEALTHY
  operator_status_details:
    operator_version: 1.2.1
    check_results:
    - name: kubernetes_permissions
      status: HEALTHY
    - name: iam_identity
      status: HEALTHY
    reported_at: '2026-01-01T00:00:00+00:00'
"""

CLOUD_GET_DEFAULT_CLOUD_EXAMPLE = """\
name: my-cloud
id: cld_abc123
provider: AWS
compute_stack: VM
region: us-west-2
is_default: true
"""

CLOUD_TERMINATE_SYSTEM_CLUSTER_EXAMPLE = """\
System cluster termination initiated for cloud cld_abcdef.
"""

SERVICE_ARCHIVE_EXAMPLE = """\
Successfully archived service: my-service
"""

SERVICE_DELETE_EXAMPLE = """\
Successfully deleted service: my-service
"""

SERVICE_LIST_EXAMPLE = """\
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓
┃ NAME       ┃ ID              ┃ CURRENT STATE ┃ CREATOR           ┃ PROJECT ┃ LAST DEPLOYED AT    ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩
│ my-service │ service2_abc123 │ RUNNING       │ someone@myorg.com │ default │ 2026-01-01 10:30:00 │
└────────────┴─────────────────┴───────────────┴───────────────────┴─────────┴─────────────────────┘
"""

SERVICE_TAGS_ADD_EXAMPLE = """\
Tags updated for service 'my-service'.
"""

SERVICE_TAGS_REMOVE_EXAMPLE = """\
Removed tag keys ['team', 'env'] from service 'my-service'.
"""

SERVICE_TAGS_LIST_EXAMPLE = """\
       Tags
┏━━━━━━┳━━━━━━━━━━┓
┃ KEY  ┃ VALUE    ┃
┡━━━━━━╇━━━━━━━━━━┩
│ env  │ prod     │
│ team │ platform │
└──────┴──────────┘
"""

# User Group Examples
USER_GROUP_LIST_EXAMPLE = """\
ID            Name
------------  ----------------
ug_abc123     Engineering
ug_def456     Data Science
ug_ghi789     Platform Team
"""

USER_GROUP_GET_EXAMPLE = """\
ID               ug_abc123
Name             Engineering
Organization ID  org_abc123
Created At       2025-01-15 10:30:00 UTC
Updated At       2025-01-15 10:30:00 UTC
"""

USER_GROUP_MEMBERSHIP_LIST_EXAMPLE = """\
{
  "Engineering": [
    "alice@example.com",
    "charlie@example.com"
  ],
  "Data Science": [
    "bob@example.com"
  ]
}
"""

# Policy Examples
POLICY_GET_EXAMPLE = """\
Policy for cloud cld_abc123:
Role          Principal (User Group ID)  Process Status
------------  -------------------------  --------------
collaborator  ug_abc123                  success
readonly      ug_def456                  success
readonly      ug_ghi789                  success
"""

POLICY_LIST_EXAMPLE = """\
cloud: cld_abc123
Role          Principal (User Group ID)  Process Status
------------  -------------------------  --------------
collaborator  ug_abc123                  success
readonly      ug_def456                  success

cloud: cld_xyz789
Role          Principal (User Group ID)  Process Status
------------  -------------------------  --------------
collaborator  ug_ghi789                  pending
"""

# SCIM Examples
SCIM_CHECK_PERMISSIONS_EXAMPLE = """\
Users with incomplete SCIM permission setup:
┏━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ User Email           ┃ Cloud      ┃ Role         ┃ Issue                   ┃
┡━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ alice@company.com    │ Production │ collaborator │ No project permissions  │
│ bob@company.com      │ Production │ collaborator │ No project permissions  │
│ bob@company.com      │ Staging    │ owner        │ No project permissions  │
└──────────────────────┴────────────┴──────────────┴─────────────────────────┘

2 users have incomplete permission setup.

Run 'anyscale policy set' to grant project-level permissions.
See https://docs.anyscale.com/administration/organization/scim for details.
"""

USER_LIST_PERMISSIONS_EXAMPLE = """\
{
  "org_owners": [
    {
      "user_email": "admin@myorg.com",
      "user_id": "usr_admin123"
    }
  ],
  "organization_id": "org_abc123",
  "users": [
    {
      "clouds": [
        {
          "cloud_id": "cld_abc123",
          "cloud_name": "my-cloud",
          "projects": [
            {
              "project_id": "prj_abc123",
              "project_name": "my-project",
              "role": "readonly"
            }
          ],
          "role": "collaborator"
        }
      ],
      "is_service_account": false,
      "user_email": "someone@myorg.com",
      "user_id": "usr_abc123"
    }
  ]
}
"""
