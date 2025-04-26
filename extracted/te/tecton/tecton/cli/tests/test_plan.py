from datetime import datetime
from unittest import TestCase
from unittest import mock

from google.protobuf.timestamp_pb2 import Timestamp
from pytz import UTC

from tecton.cli.plan import IntegrationTestSummaries
from tecton.cli.plan import PlanListItem
from tecton.cli.plan import PlanSummary
from tecton.cli.plan import get_plans_list_items
from tecton_proto.auth import principal__client_pb2 as principal_pb2
from tecton_proto.data import state_update__client_pb2 as state_update_pb2
from tecton_proto.data.state_update__client_pb2 import IntegrationTestJobStatus
from tecton_proto.metadataservice import metadata_service__client_pb2 as metadata_service_pb2


def make_principle_basic(first_name="john", last_name="smith"):
    return principal_pb2.PrincipalBasic(
        user=principal_pb2.UserBasic(
            okta_id="okta-id",
            first_name=first_name,
            last_name=last_name,
            login_email=f"{first_name}.{last_name}@tecon.ai",
        )
    )


class BaseTestCase(TestCase):
    def mockPatch(self, *args, **kwargs):
        patcher = mock.patch(*args, **kwargs)
        self.addCleanup(patcher.stop)
        return patcher.start()

    def setUp(self) -> None:
        self.mock_metadata_service = mock.MagicMock()
        self.mockPatch("tecton._internals.metadata_service.instance", return_value=self.mock_metadata_service)


class TestIntegrationTestSummaries(BaseTestCase):
    def test_from_proto(self):
        resp = IntegrationTestSummaries.from_protobuf(state_update_pb2.SuccessfulPlanOutput())
        self.assertEqual(resp, IntegrationTestSummaries({}))

        resp = IntegrationTestSummaries.from_protobuf(
            state_update_pb2.SuccessfulPlanOutput(
                test_summaries=[state_update_pb2.PlanIntegrationTestSummary(feature_view_name="fv1")]
            )
        )
        self.assertEqual(resp, IntegrationTestSummaries({"fv1": []}))

    def test_summarize_status(self):
        no_tests = []
        only_succeeded = [IntegrationTestJobStatus.JOB_STATUS_SUCCEED, IntegrationTestJobStatus.JOB_STATUS_SUCCEED]
        all_statuses = [
            IntegrationTestJobStatus.JOB_STATUS_NOT_STARTED,
            IntegrationTestJobStatus.JOB_STATUS_RUNNING,
            IntegrationTestJobStatus.JOB_STATUS_CANCELLED,
            IntegrationTestJobStatus.JOB_STATUS_SUCCEED,
            IntegrationTestJobStatus.JOB_STATUS_FAILED,
        ]

        no_failed = [
            IntegrationTestJobStatus.JOB_STATUS_NOT_STARTED,
            IntegrationTestJobStatus.JOB_STATUS_RUNNING,
            IntegrationTestJobStatus.JOB_STATUS_CANCELLED,
            IntegrationTestJobStatus.JOB_STATUS_SUCCEED,
        ]

        running = [
            IntegrationTestJobStatus.JOB_STATUS_NOT_STARTED,
            IntegrationTestJobStatus.JOB_STATUS_RUNNING,
            IntegrationTestJobStatus.JOB_STATUS_SUCCEED,
        ]
        not_started = [
            IntegrationTestJobStatus.JOB_STATUS_NOT_STARTED,
            IntegrationTestJobStatus.JOB_STATUS_SUCCEED,
        ]
        case_list = [
            ("No Tests", no_tests),
            ("Succeeded", only_succeeded),
            ("Failed", all_statuses),
            ("Canceled", no_failed),
            ("Running", running),
            ("Not Started", not_started),
        ]

        for case in case_list:
            with self.subTest(case):
                self.assertEqual(case[0], IntegrationTestSummaries._summarize_status(case[1]))

    def test_summarize_status_for_all_tests(self):
        case_list = [
            {"statuses": {}, "result": "No Tests"},
            {"statuses": {"fv1": [], "fv2": []}, "result": "No Tests"},
            {
                "statuses": {
                    "fv1": [IntegrationTestJobStatus.JOB_STATUS_SUCCEED],
                    "fv2": [IntegrationTestJobStatus.JOB_STATUS_SUCCEED, IntegrationTestJobStatus.JOB_STATUS_SUCCEED],
                    "fv3": [],
                },
                "result": "Succeeded",
            },
            {
                "statuses": {
                    "fv1": [IntegrationTestJobStatus.JOB_STATUS_SUCCEED],
                    "fv2": [IntegrationTestJobStatus.JOB_STATUS_SUCCEED, IntegrationTestJobStatus.JOB_STATUS_FAILED],
                },
                "result": "Failed",
            },
        ]
        for case in case_list:
            with self.subTest(case):
                self.assertEqual(
                    case["result"], IntegrationTestSummaries(case["statuses"]).summarize_status_for_all_tests()
                )

    def test_summarize_status_by_fv(self):
        case_list = [
            {"statuses": {}, "result": {}},
            {"statuses": {"fv1": [], "fv2": []}, "result": {"fv1": "No Tests", "fv2": "No Tests"}},
            {
                "statuses": {
                    "fv1": [IntegrationTestJobStatus.JOB_STATUS_SUCCEED],
                    "fv2": [IntegrationTestJobStatus.JOB_STATUS_SUCCEED, IntegrationTestJobStatus.JOB_STATUS_SUCCEED],
                    "fv3": [],
                },
                "result": {"fv1": "Succeeded", "fv2": "Succeeded", "fv3": "No Tests"},
            },
            {
                "statuses": {
                    "fv1": [IntegrationTestJobStatus.JOB_STATUS_SUCCEED],
                    "fv2": [IntegrationTestJobStatus.JOB_STATUS_SUCCEED, IntegrationTestJobStatus.JOB_STATUS_FAILED],
                },
                "result": {"fv1": "Succeeded", "fv2": "Failed"},
            },
        ]
        for case in case_list:
            with self.subTest(case):
                self.assertEqual(case["result"], IntegrationTestSummaries(case["statuses"]).summarize_status_by_fv())


class TestListPlan(BaseTestCase):
    maxDiff = 10000

    def test_plan_list_item_from_proto_no_test_status(self):
        pb_test_date_1 = self.make_fake_date(1)
        pb_test_date_2 = self.make_fake_date(2)
        plan_list_item = PlanListItem.from_proto(
            state_update_pb2.StateUpdateEntry(
                commit_id="fake_commit",
                applied_at=pb_test_date_1,
                applied_by="me",
                created_at=pb_test_date_2,
                created_by="you",
                applied_by_principal=make_principle_basic(),
                workspace="here",
                sdk_version="0.0.0",
                successful_plan_output=state_update_pb2.SuccessfulPlanOutput(
                    test_summaries=[state_update_pb2.PlanIntegrationTestSummary(feature_view_name="fv1")]
                ),
            )
        )
        self.assertEqual(plan_list_item.integration_test_statuses, IntegrationTestSummaries({"fv1": []}))
        self.assertEqual(
            plan_list_item,
            PlanListItem(
                plan_id="fake_commit",
                applied_by="john.smith@tecon.ai(User Email)",
                applied_at=datetime(year=2024, month=1, day=1, tzinfo=UTC),
                created_by="you",
                created_at=datetime(year=2024, month=1, day=2, tzinfo=UTC),
                workspace="here",
                sdk_version="0.0.0",
                integration_test_statuses=IntegrationTestSummaries({"fv1": []}),
            ),
        )

    def test_plan_list_item_from_proto_with_test_status(self):
        pb_test_date_1 = self.make_fake_date(1)
        pb_test_date_2 = self.make_fake_date(2)
        plan_list_item = PlanListItem.from_proto(
            state_update_pb2.StateUpdateEntry(
                commit_id="fake_commit",
                applied_at=pb_test_date_1,
                applied_by="me",
                created_by="you",
                created_at=pb_test_date_2,
                applied_by_principal=make_principle_basic(),
                workspace="here",
                sdk_version="0.0.0",
                successful_plan_output=state_update_pb2.SuccessfulPlanOutput(
                    test_summaries=[
                        state_update_pb2.PlanIntegrationTestSummary(
                            feature_view_name="fv1",
                            job_summaries=[
                                state_update_pb2.IntegrationTestJobSummary(
                                    status=state_update_pb2.IntegrationTestJobStatus.JOB_STATUS_FAILED
                                )
                            ],
                        )
                    ]
                ),
            )
        )
        self.assertEqual(
            plan_list_item,
            PlanListItem(
                plan_id="fake_commit",
                applied_by="john.smith@tecon.ai(User Email)",
                applied_at=datetime(year=2024, month=1, day=1, tzinfo=UTC),
                created_by="you",
                created_at=datetime(year=2024, month=1, day=2, tzinfo=UTC),
                workspace="here",
                sdk_version="0.0.0",
                integration_test_statuses=IntegrationTestSummaries(
                    {"fv1": [state_update_pb2.IntegrationTestJobStatus.JOB_STATUS_FAILED]}
                ),
            ),
        )

    def make_fake_date(self, day):
        test_date = datetime(year=2024, month=1, day=day)
        pb_test_date = Timestamp()
        pb_test_date.FromDatetime(test_date)
        return pb_test_date

    def test_plan_list_items_from_proto_empty(self):
        plan_list_item = PlanListItem.from_proto(state_update_pb2.StateUpdateEntry())
        self.assertEqual(
            plan_list_item,
            PlanListItem(
                plan_id="",
                applied_by="",
                applied_at=None,
                created_by="",
                created_at=None,
                workspace="prod",
                sdk_version="",
                integration_test_statuses=IntegrationTestSummaries({}),
            ),
        )

    def test_get_plans_list_items(self):
        self.mock_metadata_service.GetStateUpdatePlanList.return_value = (
            metadata_service_pb2.GetStateUpdatePlanListResponse(
                entries=[
                    state_update_pb2.StateUpdateEntry(
                        commit_id="fake-commit",
                        applied_by="me",
                        created_by="you",
                        workspace="my_workspace",
                        sdk_version="0.0.0",
                        successful_plan_output=state_update_pb2.SuccessfulPlanOutput(),
                    ),
                    state_update_pb2.StateUpdateEntry(
                        commit_id="fake-commit2",
                        applied_by="you",
                        created_by="you",
                        workspace="my_workspace",
                        sdk_version="0.0.1",
                        successful_plan_output=state_update_pb2.SuccessfulPlanOutput(),
                    ),
                ]
            )
        )
        items = get_plans_list_items("my_workspace", 100)
        self.mock_metadata_service.GetStateUpdatePlanList.assert_called_with(
            metadata_service_pb2.GetStateUpdatePlanListRequest(workspace="my_workspace", limit=100)
        )
        assert items == [
            PlanListItem(
                plan_id="fake-commit",
                applied_by="me",
                applied_at=None,
                created_by="you",
                created_at=None,
                workspace="my_workspace",
                sdk_version="0.0.0",
                integration_test_statuses=IntegrationTestSummaries({}),
            ),
            PlanListItem(
                plan_id="fake-commit2",
                applied_by="you",
                applied_at=None,
                created_by="you",
                created_at=None,
                workspace="my_workspace",
                sdk_version="0.0.1",
                integration_test_statuses=IntegrationTestSummaries({}),
            ),
        ]

    def test_get_plans_list_items_empty(self):
        self.mock_metadata_service.GetStateUpdatePlanList.return_value = (
            metadata_service_pb2.GetStateUpdatePlanListResponse()
        )
        items = get_plans_list_items("my_workspace", 100)
        self.mock_metadata_service.GetStateUpdatePlanList.assert_called_with(
            metadata_service_pb2.GetStateUpdatePlanListRequest(workspace="my_workspace", limit=100)
        )
        assert items == []


class TestGetPlan(BaseTestCase):
    def test_plan_summary_from_proto_empty(self):
        plan = PlanSummary.from_proto(metadata_service_pb2.QueryStateUpdateResponseV2())
        self.assertEqual(
            plan,
            PlanSummary(
                applied=False,
                applied_by="",
                applied_at=None,
                created_by="",
                created_at=None,
                workspace="prod",
                sdk_version="",
                integration_test_statuses=IntegrationTestSummaries(statuses={}),
                plan_url="",
            ),
        )
