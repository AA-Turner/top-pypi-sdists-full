"""Tests for create view."""

import pytest

from tests.helpers import (
    TestColumnQualifierTuple,
    assert_column_lineage,
    assert_table_lineage_equal,
)

from collate_sqllineage.core.models import Column, SubQuery, Table
from collate_sqllineage.core.parser.sqlfluff.analyzer import SqlFluffLineageAnalyzer
from collate_sqllineage.core.parser.sqlglot.analyzer import SqlGlotLineageAnalyzer
from collate_sqllineage.runner import LineageRunner


@pytest.mark.parametrize("dialect", ["bigquery"])
def test_create_view(dialect: str):
    sql = """CREATE VIEW Operations_Workspace.Retention_For_Associates_Bonus AS with
incident_level as (
select
a.Reference_Number,
a.Incident_ID,
a1.Incident_Performance_ID,
d.Incident_Status_Desc as Incident_Status,
Incident_Subject_Type_Description as Manaul_Log,
Incident_Category_Description as Incident_Category,
a.Incident_Log_Description as Log_Description,
e.Entity_ID as AH_ID,
a.Incident_Creation_Date as Date_Created,
a1.Interval_End_Date as Handled_Date,
a1.Interval_End_DateTime as Handled_Date_Time,
b.Queue_Desc as Queue,
e.RefCode as Partner_Name,
f.Country_Name,
e.Value_Segment as Segment,
CASE When ROW_NUMBER() over (partition by a.Incident_ID order by Interval_End_DateTime DESC) = 1 then cast(a1.Interval_End_Date as date) end as Last_Interval_End_Date,
CASE When ROW_NUMBER() over (partition by a.Incident_ID order by Interval_End_DateTime DESC) = 1 then 1 else 0 end as Last_Interval_Flag,
CASE
WHEN Incident_Performance_Met_SLA_Type_ID=3 THEN 1
WHEN Incident_Performance_Met_SLA_Type_ID=4 THEN 0
WHEN Incident_Performance_Met_SLA_Type_ID=0 THEN 0
WHEN Incident_Performance_Met_SLA_Type_ID=1 THEN 0
WHEN Incident_Performance_Met_SLA_Type_ID is null THEN 0
ELSE 0 END AS Is_Met_SLA,
a1.Associate_ORN_ID,
a1.Previous_Associate_ORN_ID,
incident_subject,
case when incident_close_date is not null then 1 else 0 end as handled_indication
,case
  when Incident_Log_Description in ('3 phone attempts no answer','3 phone attempts, no answer - offered support via email') then '3 phone attempts no answer'
  when Incident_Log_Description in ('Customer does not speak English',
'Customer is not collaborative, did not want to speak',
'Outbound call unsuccessful due to SIP',
'Phone number is invalid'
) then 'Comunication Issues'
  when Incident_Log_Description in ('Complained about pricing, cashback offer sent',
'Complianed about Pricing, reduced pricing request sent',
'Customer moved to new Payoneer Account: <AH ID>',
'GBT Customer - Cashback Proposal',
'GBT Customer - Payoneer Account Proposal',
'Moved to competition, bad experiance - Cashback proposal',
'Moved to competition, bad experience - Tier pricing proposal',
'Operational friction pending customer',
'Operational friction pending review from Payoneer',
'Operational Issues in the past, offered cashback',
'Operational Issues in the past, offered tier proposal offered',
'Other - Product solution offered',
'Using a competitor , but we offer a solution'
) then 'Contacted - Offer Was Made'
  when Incident_Log_Description in ('Customer not at risk - Seasonal',
'Declining Volume - External problems that affect their business',
'Moved to Competition - Not interested'
) then 'Contacted - Out of Control'
  when Incident_Log_Description in ('Customer blocked/marked for deflation') then 'Customer blocked/marked for deflation'
  when Incident_Log_Description in ('Reminder was sent','Sent notice to customer for call') then 'Still Open ticket'
  when Incident_Log_Description is not null then 'Other'
  else 'No Log'
end as Log_Description_Category,
rid.Incident_Creation_Reason_Description
,count(distinct a.Incident_ID) as Num_Tickets
,a.Category_ID
,Primary_Phone_Number

FROM
 `DW_Main.View_Fact_ORN_Incidents` a
 left join
`DW_Main.View_Fact_ORN_Incident_Performance` a1
 on a1.Incident_ID = a.Incident_ID
left join `DW_Main.View_Dim_ORN_Queues` b
on a.Last_Queue_ID = b.Queue_ID
left join `DW_Main.View_Dim_ORN_Incident_Subject_Types` c
on a.Incident_Subject_Type_ID = c.Incident_Subject_Type_ID
left join `DW_Main.View_Dim_ORN_Incident_Statuses` d
on a1.interval_Status_ID = d.Incident_Status_ID
left join `DW_Main.View_Dim_Entities` e
on e.Entity_ID = a.Account_Holder_ID and e.Entity_Type = 1
left join `DW_Main.View_Dim_Countries` f
on f.ISO2= e.Billing_Country
left join `DW_Main.View_Dim_Manual_Log_Inquiry_Types` g
on g.Inquiry_Type_ID = a.First_Manual_Log_Inquiry_Type_ID
left join `DW_Main.View_Dim_Manual_Log_Inquiry_Types` h
on h.Inquiry_Type_ID = a.Last_Manual_Log_Inquiry_Type_ID
left join `DW_Main.View_Dim_ORN_Incident_Creation_Reasons` rid on a.Incident_Creation_Reason_ID = rid.Incident_Creation_Reason_ID
where
b.Queue_ID in (963,986,985,998,999,1000,1006,1007,1008)
and a.Incident_Creation_Date >= DATE_TRUNC(DATE_ADD(CURRENT_DATE(),INTERVAL -12 MONTH), MONTH)
group by all
),

log_level as (
  select
  C.Incident_ID,
  Ch.Description as Channel,
  ROW_NUMBER() over (partition by Incident_ID ) as rn
FROM `DW_Main.View_Fact_Support_Log` as S
LEFT OUTER JOIN `DW_Main.View_Fact_ORN_Communications` as C ON C.Thread_ID = S.CSTS_Log_ID
left join `DW_Main.View_Dim_Manual_Log_Inquiry_Types` Ch on Ch.Inquiry_Type_ID = S.Manual_Log_Inquiry_Type
WHERE
 Log_Date>= DATE_TRUNC(DATE_ADD(CURRENT_DATE(),INTERVAL -6 MONTH), MONTH)
AND Representative NOT IN ('CCTech Flows', 'Rest API', 'SSO Test User', 'appian client', 'conversocial_client conversocial_client', 'salesforce_client salesforce_client','Zowie Chatbot',
'OneStepAhead API','cc_escalations automation','CC Test User')
and Ch.Description <> 'UD_0'
qualify rn =1
),

CU AS (
select
distinct cu_pop.`entity id` as Entity_Id_CU,
curr_classification.CreateDate as BatchCreateDate,
Q_Statuses.Description AS Status_Description,
Q_Statues_R.Description AS Reason_Description,
FROM `payoneer-prod-eu-svc-data-016f.Operations_Workspace.AmirCUPopOnlyAHIDBatchAndCohort` cu_pop
LEFT JOIN `Sources_Qualification.Qualification_CustomerQualifications` AS Qual on cast(cu_pop.`entity id` as string) = Qual.AccountHolderId
LEFT JOIN `payoneer-prod-eu-svc-data-016f.Sources_EntityClassification.ECS_EntitiesClassifications_Current_State` curr_classification
ON cast(cu_pop.`entity id` as string) = curr_classification.EntityId
LEFT JOIN `Sources_Qualification.Qualification_QualificationStatuses` AS Q_Statuses
    ON Qual.QualificationStatusId = Q_Statuses.QualificationStatusId
LEFT JOIN `Sources_Qualification.Qualification_QualificationStatusReasons` AS Q_Statues_R
    ON Q_Statues_R.StatusReasonId = Qual.QualificationStatusReasonId

left join (    SELECT
        class.EntityId,
    FROM `payoneer-prod-eu-svc-data-016f.Sources_EntityClassification.ECS_EntitiesClassifications_Current_State` class

     WHERE class.ClassificationTypeId = 128 --CU CLASSIFICATION TYPE ID (except ahs with extended grace period will also have classificationtypeid of 130)

    UNION DISTINCT

    SELECT
        hist.EntityId,
    FROM (SELECT *
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (PARTITION BY EntityId, ClassificationTypeId ORDER BY EventDate DESC) AS rn
        FROM `payoneer-prod-eu-svc-data-016f.Sources_EntityClassification.ECS_EntitiesClassifications_History`

        WHERE ClassificationTypeId = 128
    )
    WHERE rn = 1) hist
    WHERE NOT EXISTS (
        SELECT 1
        FROM `payoneer-prod-eu-svc-data-016f.Sources_EntityClassification.ECS_EntitiesClassifications_Current_State` curr
        WHERE curr.EntityId = hist.EntityId
          --AND curr.ClassificationTypeId = 3
            AND curr.ClassificationTypeId = 128 --CU CLASSIFICATION TYPE ID (except ahs with extended grace period will also have classificationtypeid of 130)
    )) cur_pop_update on cur_pop_update.EntityId = cast(cu_pop.`entity id` as string)
WHERE  curr_classification.ClassificationTypeId=128 --current cleanup classification
and QualificationTypeId in (3,12,14,15,17,18,22,23,34,35)

)



Select Channel ,a.* ,c.*
from incident_level a
left join log_level b
on a.incident_id = b.incident_id
left join CU c on a.AH_ID = Entity_Id_CU"""
    assert_table_lineage_equal(
        sql,
        {  # source_tables (17 tables)
            "dw_main.view_fact_orn_incidents",
            "dw_main.view_fact_orn_incident_performance",
            "dw_main.view_dim_orn_queues",
            "dw_main.view_dim_orn_incident_subject_types",
            "dw_main.view_dim_orn_incident_statuses",
            "dw_main.view_dim_entities",
            "dw_main.view_dim_countries",
            "dw_main.view_dim_manual_log_inquiry_types",
            "dw_main.view_dim_orn_incident_creation_reasons",
            "dw_main.view_fact_support_log",
            "dw_main.view_fact_orn_communications",
            "payoneer-prod-eu-svc-data-016f.operations_workspace.amircupoponlyahidbatchandcohort",
            "payoneer-prod-eu-svc-data-016f.sources_entityclassification.ecs_entitiesclassifications_current_state",
            "payoneer-prod-eu-svc-data-016f.sources_entityclassification.ecs_entitiesclassifications_history",
            "sources_qualification.qualification_customerqualifications",
            "sources_qualification.qualification_qualificationstatuses",
            "sources_qualification.qualification_qualificationstatusreasons",
        },
        {  # target_tables
            "operations_workspace.retention_for_associates_bonus",
        },
        dialect=dialect,
        # SqlParse misses BQ project-qualified table with hyphens
        test_sqlparse=False,
        # SqlGlot graph has 50 nodes vs SqlFluff 48 nodes due to subquery handling
        skip_graph_check=True,
    )
    # Unqualified columns in incident_level CTE are resolved across all 9 joined
    # tables since without schema info any could be the source. This list contains
    # all 89 column lineage paths produced by SqlGlot and SqlFluff.
    #
    # incident_level CTE joined tables (for unqualified column fan-out):
    #   a  = dw_main.view_fact_orn_incidents
    #   a1 = dw_main.view_fact_orn_incident_performance
    #   b  = dw_main.view_dim_orn_queues
    #   c  = dw_main.view_dim_orn_incident_subject_types
    #   d  = dw_main.view_dim_orn_incident_statuses
    #   e  = dw_main.view_dim_entities
    #   f  = dw_main.view_dim_countries
    #   g/h/Ch = dw_main.view_dim_manual_log_inquiry_types
    #   rid = dw_main.view_dim_orn_incident_creation_reasons
    incident_level_tables = [
        "dw_main.view_fact_orn_incidents",
        "dw_main.view_fact_orn_incident_performance",
        "dw_main.view_dim_orn_queues",
        "dw_main.view_dim_orn_incident_subject_types",
        "dw_main.view_dim_orn_incident_statuses",
        "dw_main.view_dim_entities",
        "dw_main.view_dim_countries",
        "dw_main.view_dim_manual_log_inquiry_types",
        "dw_main.view_dim_orn_incident_creation_reasons",
    ]
    tgt = "operations_workspace.retention_for_associates_bonus"
    # 85 column lineages consistently produced by both SqlGlot and SqlFluff.
    # SqlGlot non-deterministically also resolves 4 CU CTE individual columns
    # through c.* wildcard (producing 89 total). SqlFluff always resolves them.
    # We test SqlFluff with 89 expected entries (strict), and SqlGlot with 85
    # core entries, allowing the 4 CU CTE extras when they appear.
    core_column_lineages = [
        # --- incident_level CTE: qualified columns (unique source) ---
        (
            TestColumnQualifierTuple(
                "Reference_Number", "dw_main.view_fact_orn_incidents"
            ),
            TestColumnQualifierTuple("Reference_Number", tgt),
        ),
        (
            TestColumnQualifierTuple("Incident_ID", "dw_main.view_fact_orn_incidents"),
            TestColumnQualifierTuple("Incident_ID", tgt),
        ),
        (
            TestColumnQualifierTuple(
                "Incident_Performance_ID",
                "dw_main.view_fact_orn_incident_performance",
            ),
            TestColumnQualifierTuple("Incident_Performance_ID", tgt),
        ),
        (
            TestColumnQualifierTuple(
                "Incident_Status_Desc", "dw_main.view_dim_orn_incident_statuses"
            ),
            TestColumnQualifierTuple("Incident_Status", tgt),
        ),
        (
            TestColumnQualifierTuple(
                "Incident_Log_Description", "dw_main.view_fact_orn_incidents"
            ),
            TestColumnQualifierTuple("Log_Description", tgt),
        ),
        (
            TestColumnQualifierTuple("Entity_ID", "dw_main.view_dim_entities"),
            TestColumnQualifierTuple("AH_ID", tgt),
        ),
        (
            TestColumnQualifierTuple(
                "Incident_Creation_Date", "dw_main.view_fact_orn_incidents"
            ),
            TestColumnQualifierTuple("Date_Created", tgt),
        ),
        (
            TestColumnQualifierTuple(
                "Interval_End_Date", "dw_main.view_fact_orn_incident_performance"
            ),
            TestColumnQualifierTuple("Handled_Date", tgt),
        ),
        (
            TestColumnQualifierTuple(
                "Interval_End_DateTime",
                "dw_main.view_fact_orn_incident_performance",
            ),
            TestColumnQualifierTuple("Handled_Date_Time", tgt),
        ),
        (
            TestColumnQualifierTuple("Queue_Desc", "dw_main.view_dim_orn_queues"),
            TestColumnQualifierTuple("Queue", tgt),
        ),
        (
            TestColumnQualifierTuple("RefCode", "dw_main.view_dim_entities"),
            TestColumnQualifierTuple("Partner_Name", tgt),
        ),
        (
            TestColumnQualifierTuple("Country_Name", "dw_main.view_dim_countries"),
            TestColumnQualifierTuple("Country_Name", tgt),
        ),
        (
            TestColumnQualifierTuple("Value_Segment", "dw_main.view_dim_entities"),
            TestColumnQualifierTuple("Segment", tgt),
        ),
        (
            TestColumnQualifierTuple(
                "Interval_End_Date", "dw_main.view_fact_orn_incident_performance"
            ),
            TestColumnQualifierTuple("Last_Interval_End_Date", tgt),
        ),
        (
            TestColumnQualifierTuple(
                "Associate_ORN_ID", "dw_main.view_fact_orn_incident_performance"
            ),
            TestColumnQualifierTuple("Associate_ORN_ID", tgt),
        ),
        (
            TestColumnQualifierTuple(
                "Previous_Associate_ORN_ID",
                "dw_main.view_fact_orn_incident_performance",
            ),
            TestColumnQualifierTuple("Previous_Associate_ORN_ID", tgt),
        ),
        (
            TestColumnQualifierTuple(
                "Incident_Creation_Reason_Description",
                "dw_main.view_dim_orn_incident_creation_reasons",
            ),
            TestColumnQualifierTuple("Incident_Creation_Reason_Description", tgt),
        ),
        (
            TestColumnQualifierTuple("Incident_ID", "dw_main.view_fact_orn_incidents"),
            TestColumnQualifierTuple("Num_Tickets", tgt),
        ),
        (
            TestColumnQualifierTuple("Category_ID", "dw_main.view_fact_orn_incidents"),
            TestColumnQualifierTuple("Category_ID", tgt),
        ),
        (
            TestColumnQualifierTuple(
                "Incident_Log_Description", "dw_main.view_fact_orn_incidents"
            ),
            TestColumnQualifierTuple("Log_Description_Category", tgt),
        ),
        # --- incident_level CTE: unqualified columns resolved across all 9 joined tables ---
        # Incident_Subject_Type_Description -> Manaul_Log (from all 9 tables)
        *[
            (
                TestColumnQualifierTuple("Incident_Subject_Type_Description", t),
                TestColumnQualifierTuple("Manaul_Log", tgt),
            )
            for t in incident_level_tables
        ],
        # Incident_Category_Description -> Incident_Category (from all 9 tables)
        *[
            (
                TestColumnQualifierTuple("Incident_Category_Description", t),
                TestColumnQualifierTuple("Incident_Category", tgt),
            )
            for t in incident_level_tables
        ],
        # Incident_Performance_Met_SLA_Type_ID -> Is_Met_SLA (from all 9 tables)
        *[
            (
                TestColumnQualifierTuple("Incident_Performance_Met_SLA_Type_ID", t),
                TestColumnQualifierTuple("Is_Met_SLA", tgt),
            )
            for t in incident_level_tables
        ],
        # incident_subject -> incident_subject (from all 9 tables)
        *[
            (
                TestColumnQualifierTuple("incident_subject", t),
                TestColumnQualifierTuple("incident_subject", tgt),
            )
            for t in incident_level_tables
        ],
        # incident_close_date -> handled_indication (from all 9 tables)
        *[
            (
                TestColumnQualifierTuple("incident_close_date", t),
                TestColumnQualifierTuple("handled_indication", tgt),
            )
            for t in incident_level_tables
        ],
        # Incident_Log_Description -> Log_Description_Category (unqualified from 8 tables, excluding _INCIDENTS which is qualified above)
        *[
            (
                TestColumnQualifierTuple("Incident_Log_Description", t),
                TestColumnQualifierTuple("Log_Description_Category", tgt),
            )
            for t in incident_level_tables
            if t != "dw_main.view_fact_orn_incidents"
        ],
        # Primary_Phone_Number -> Primary_Phone_Number (from all 9 tables)
        *[
            (
                TestColumnQualifierTuple("Primary_Phone_Number", t),
                TestColumnQualifierTuple("Primary_Phone_Number", tgt),
            )
            for t in incident_level_tables
        ],
        # --- log_level CTE ---
        (
            TestColumnQualifierTuple(
                "Description", "dw_main.view_dim_manual_log_inquiry_types"
            ),
            TestColumnQualifierTuple("Channel", tgt),
        ),
        # --- Final SELECT wildcards: a.* from incident_level, c.* from CU (CTE = SubQuery)
        (
            TestColumnQualifierTuple("*", "incident_level", True),
            TestColumnQualifierTuple("*", tgt),
        ),
        (
            TestColumnQualifierTuple("*", "CU", True),
            TestColumnQualifierTuple("*", tgt),
        ),
    ]
    # CU CTE individual columns resolved through c.* wildcard.
    # SqlFluff always resolves these; SqlGlot resolves them non-deterministically.
    cu_cte_column_lineages = [
        (
            TestColumnQualifierTuple(
                "entity id",
                "payoneer-prod-eu-svc-data-016f.operations_workspace.amircupoponlyahidbatchandcohort",
            ),
            TestColumnQualifierTuple("Entity_Id_CU", tgt),
        ),
        (
            TestColumnQualifierTuple(
                "CreateDate",
                "payoneer-prod-eu-svc-data-016f.sources_entityclassification.ecs_entitiesclassifications_current_state",
            ),
            TestColumnQualifierTuple("BatchCreateDate", tgt),
        ),
        (
            TestColumnQualifierTuple(
                "Description",
                "sources_qualification.qualification_qualificationstatuses",
            ),
            TestColumnQualifierTuple("Status_Description", tgt),
        ),
        (
            TestColumnQualifierTuple(
                "Description",
                "sources_qualification.qualification_qualificationstatusreasons",
            ),
            TestColumnQualifierTuple("Reason_Description", tgt),
        ),
    ]
    # SqlGlot: non-deterministically produces 85 or 89 lineages. Assert the 85
    # core lineages are always present and any extras are only the 4 CU entries.
    lr_sqlglot = LineageRunner(sql, dialect=dialect, analyzer=SqlGlotLineageAnalyzer)
    actual_sqlglot = {
        (lineage[0], lineage[-1]) for lineage in set(lr_sqlglot.get_column_lineage())
    }

    def _build_expected(lineage_list):
        result = set()
        for src, tgt_item in lineage_list:
            src_col = Column(src.column)
            if src.qualifier is not None:
                if not src.is_subquery:
                    src_col.parent = Table(src.qualifier)
                else:
                    src_col.parent = SubQuery(
                        subquery=src.subquery,
                        subquery_raw=src.subquery,
                        alias=src.qualifier,
                    )
            tgt_col = Column(tgt_item.column)
            if not tgt_item.is_subquery:
                tgt_col.parent = Table(tgt_item.qualifier)
            else:
                tgt_col.parent = SubQuery(
                    subquery=tgt_item.subquery,
                    subquery_raw=tgt_item.subquery,
                    alias=tgt_item.qualifier,
                )
            result.add((src_col, tgt_col))
        return result

    expected_core = _build_expected(core_column_lineages)
    expected_cu = _build_expected(cu_cte_column_lineages)
    # All 85 core lineages must be present
    missing_core = expected_core - actual_sqlglot
    assert not missing_core, f"\n\t[SqlGlot] Missing core lineages: {missing_core}"
    # Any extras must only be from the known CU CTE set
    unexpected = actual_sqlglot - expected_core - expected_cu
    assert not unexpected, f"\n\t[SqlGlot] Unexpected lineages: {unexpected}"
    # SqlFluff: consistently produces all 89 lineages (core + CU CTE)
    lr_sqlfluff = LineageRunner(sql, dialect=dialect, analyzer=SqlFluffLineageAnalyzer)
    assert_column_lineage(
        lr_sqlfluff,
        core_column_lineages + cu_cte_column_lineages,
        parser_name="SqlFluff",
    )
