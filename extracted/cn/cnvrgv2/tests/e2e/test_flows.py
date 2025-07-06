import time
from contextlib import contextmanager
from datetime import datetime

from cnvrgv2.modules.flows.flow import Flow
from cnvrgv2.utils.cron import Cron


class TestFlows:
    # TODO: Need to add cleanup by context + add create flow with title (in server)

    @staticmethod
    @contextmanager
    def temp_flow(project, **kwargs):
        flow = project.flows.create(**kwargs)
        yield flow
        flow.delete()

    def test_create_flow_success(self, e2e_project):
        with TestFlows.temp_flow(e2e_project) as flow:
            assert type(flow) is Flow

    def test_create_flow_with_yaml_success(self, e2e_project, e2e_flow_yaml):
        with TestFlows.temp_flow(e2e_project, yaml_path=e2e_flow_yaml["path"]) as flow:
            assert flow.title == e2e_flow_yaml["title"]

    def test_create_flow_with_yaml_string_success(self, e2e_project, e2e_flow_yaml):
        with TestFlows.temp_flow(e2e_project, yaml_string=e2e_flow_yaml["string"]) as flow:
            assert flow.title == e2e_flow_yaml["title"]

    def test_run_flow_success(self, e2e_project, e2e_flow_yaml):
        with TestFlows.temp_flow(e2e_project, yaml_path=e2e_flow_yaml["path"]) as flow:
            flow.run()

            flow_version = next(flow.flow_versions.list())
            experiments = e2e_project.experiments.list()

            assert flow_version.state == "running"
            assert len(list(experiments)) == 1

    def test_get_flow_success(self, e2e_project, e2e_flow):
        slug = e2e_flow.slug
        flow = e2e_project.flows.get(slug)
        assert slug == flow.slug

    def test_update_flow_success(self, random_name, e2e_flow):
        title = random_name(5)
        flow = e2e_flow.update(title=title)
        assert title == flow.title

    # DEV-10527: Currently disable. Missing full implementation in the server
    # def test_delete_flow_success(self, e2e_project, e2e_flow):
    #    slug = e2e_flow.slug
    #    e2e_flow.delete()
    #
    #    with pytest.raises(CnvrgHttpError) as exception_info:
    #        e2e_project.flows.get(slug).title
    #
    #    assert exception_info.value.status_code == 404

    def test_list_flows_only_success(self, e2e_project):
        num_of_flows = 5

        # Create some flows
        for i in range(num_of_flows):
            e2e_project.flows.create()

        flows_list = e2e_project.flows.list()

        assert len(list(flows_list)) == num_of_flows

        for flow in flows_list:
            flow.delete()

    def test_list_flows_sort_success(self, e2e_project):
        num_of_flows = 2
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"

        # Create some flows
        for i in range(num_of_flows):
            e2e_project.flows.create()
            time.sleep(1)

        flows = e2e_project.flows.list("-created_at")
        first_date = datetime.strptime(next(flows).created_at, date_format)
        second_date = datetime.strptime(next(flows).created_at, date_format)

        assert first_date > second_date

        for flow in flows:
            flow.delete()

    # DEV-10527: Currently disable. Missing full implementation in the server
    # def test_bulk_delete_flows_success(self, e2e_clean_flows, e2e_project):
    #    num_of_flows = 2
    #    flows = []
    #
    #    # Create some flows
    #    for i in range(num_of_flows):
    #        flow = TestFlows.create_flow(e2e_project)
    #        flows.append(flow)
    #
    #    slugs = list(flow.slug for flow in flows)
    #    e2e_project.flows.delete(slugs)
    #
    #    for slug in slugs:
    #        with pytest.raises(CnvrgHttpError) as exception_info:
    #            e2e_project.flows.get(slug).title
    #        assert exception_info.value.status_code == 404

    def test_flow_set_schedule_success(self, e2e_flow):
        cron = Cron(minute=30, hour=1)

        e2e_flow.set_schedule(str(cron))

        e2e_flow.reload()
        assert e2e_flow.cron_syntax == str(cron) + " UTC"

    def test_flow_clear_schedule_success(self, e2e_flow):
        cron = Cron(minute=30, hour=1)
        e2e_flow.set_schedule(str(cron))

        e2e_flow.clear_schedule()

        e2e_flow.reload()
        assert e2e_flow.cron_syntax is None

    def test_toggle_webhook_on_success(self, e2e_flow):
        e2e_flow.toggle_webhook(True)

        e2e_flow.reload()
        assert e2e_flow.webhook_url

    def test_toggle_webhook_off_success(self, e2e_flow):
        e2e_flow.toggle_webhook(True)
        e2e_flow.toggle_webhook(False)

        e2e_flow.reload()
        assert e2e_flow.webhook_url is None

    def test_toggle_dataset_update_on_success(self, e2e_flow, e2e_dataset):
        e2e_flow.toggle_dataset_update(True, e2e_dataset)

        e2e_flow.reload()
        assert e2e_flow.trigger_dataset

    def test_toggle_dataset_update_off_success(self, e2e_flow, e2e_dataset):
        e2e_flow.toggle_dataset_update(True, e2e_dataset)
        e2e_flow.toggle_dataset_update(False)

        e2e_flow.reload()
        assert e2e_flow.trigger_dataset is None
