import logging

from python_agent.build_scanner.entities.environment_data import EnvironmentData
from python_agent.test_listener.entities.app_data import AppData
from python_agent.test_listener.entities.file_data import FileData
from python_agent.test_listener.entities.footprint_data import FootprintData
from python_agent.test_listener.entities.footprints_request import FootprintsRequest
from python_agent.test_listener.entities.test_data import TestData

log = logging.getLogger(__name__)


class FootprintsService(object):
    def __init__(self, config_data, backend_proxy):
        self.config_data = config_data
        self.backend_proxy = backend_proxy

    def send_footprints(self, footprint_items):
        try:
            log.info("Sending Footprints. Num of Items: %s" % len(footprint_items))
            footprints_request = self.create_footprints_request(footprint_items)
            del footprint_items
            self.backend_proxy.send_footprints(self.config_data, footprints_request)
            del footprints_request
            log.info("Sent Footprints to Server")
        except Exception as e:
            log.exception("Failed Sending Footprints. Error: %s" % str(e))
            raise

    def create_footprints_request(self, footprint_items):
        app_data = AppData(
            self.config_data.appName,
            self.config_data.branchName,
            self.config_data.buildName,
            [],
        )
        environment_data = EnvironmentData(
            self.config_data.labId,
            self.config_data.testStage,
            self.config_data.testGroupId,
        )
        footprints_request = FootprintsRequest(
            self.config_data.customerId,
            environment_data,
            self.config_data,
            [],
            [app_data],
        )
        test_name_to_index = {}
        filename_to_file = {}
        unique_id_to_element = {}
        unique_id_to_hits_index = {}
        try:
            for footprint_item in footprint_items:
                test_item = self.create_test_item(footprint_item)
                test_index = self.get_or_create_test(
                    test_item, footprints_request.tests, test_name_to_index
                )
                for app in footprints_request.apps:
                    if footprint_item["footprints"].get("methods"):
                        self.add_methods(
                            footprint_item["footprints"]["methods"],
                            unique_id_to_element,
                            unique_id_to_hits_index,
                            test_index,
                            filename_to_file,
                            app.files,
                        )
                    if footprint_item["footprints"].get("lines"):
                        self.add_lines(
                            footprint_item["footprints"]["lines"],
                            unique_id_to_element,
                            unique_id_to_hits_index,
                            test_index,
                            filename_to_file,
                            app.files,
                        )
            return footprints_request
        except Exception as e:
            log.exception("Failed Creating Footprints Request. Error: %s " % str(e))

    def create_test_item(self, footprint_item):
        test_name = footprint_item["test_name"]
        execution_id = footprint_item["execution_id"]
        local_time = footprint_item["local_time"]
        test_data = TestData(test_name, execution_id, local_time)
        return test_data

    def get_or_create_test(self, test_item, tests, test_name_to_index):
        test_name = test_item.testName
        test_index = test_name_to_index.get(test_name)
        if test_index:
            return test_index
        tests.append(test_item)
        index = len(test_name_to_index)
        test_name_to_index[test_name] = index
        return index

    def get_or_create_file(self, filename, filename_to_file, files):
        file_data = filename_to_file.get(filename)
        if file_data:
            return file_data
        file_data = FileData(filename, [], [], [])
        files.append(file_data)
        filename_to_file[filename] = file_data
        return file_data

    def get_or_create_element(
        self, test_footprint_data, unique_id_to_element, elements
    ):
        element = unique_id_to_element.get(test_footprint_data["unique_id"])
        if element:
            return element
        element = FootprintData(test_footprint_data["unique_id"], [])
        elements.append(element)
        unique_id_to_element[test_footprint_data["unique_id"]] = element
        return element

    def get_or_create_hits(
        self, unique_id, test_index, unique_id_to_hits_index, element_hits
    ):
        unique_id_test_index = unique_id + "|" + str(test_index)
        hits_index = unique_id_to_hits_index.get(unique_id_test_index)
        if hits_index:
            return hits_index
        hits_element = [test_index, 0]
        hits_index = len(element_hits)
        unique_id_to_hits_index[unique_id_test_index] = hits_index
        element_hits.append(hits_element)
        return hits_index

    def add_methods(
        self,
        test_footprints,
        unique_id_to_element,
        unique_id_to_hits_index,
        test_index,
        filename_to_file,
        files,
    ):
        for test_footprint_data in test_footprints:
            filename = test_footprint_data["filename"]
            file_data = self.get_or_create_file(filename, filename_to_file, files)
            method_element = self.get_or_create_element(
                test_footprint_data, unique_id_to_element, file_data.methods
            )
            hits_index = self.get_or_create_hits(
                test_footprint_data["unique_id"],
                test_index,
                unique_id_to_hits_index,
                method_element.hits,
            )
            test_hits = method_element.hits[hits_index]
            test_hits[1] += test_footprint_data["hits"]

    def add_lines(
        self,
        test_footprints,
        unique_id_to_element,
        unique_id_to_hits_index,
        test_index,
        filename_to_file,
        files,
    ):
        for test_footprint_data in test_footprints:
            filename = test_footprint_data["filename"]
            file_data = self.get_or_create_file(filename, filename_to_file, files)
            line_element = self.get_or_create_element(
                test_footprint_data, unique_id_to_element, file_data.lines
            )
            hits_index = self.get_or_create_hits(
                test_footprint_data["unique_id"],
                test_index,
                unique_id_to_hits_index,
                line_element.hits,
            )
            test_hits = line_element.hits[hits_index]
            test_hits[1] += test_footprint_data["hits"]
