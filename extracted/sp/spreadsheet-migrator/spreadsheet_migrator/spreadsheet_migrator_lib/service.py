from typing import Dict, List, Tuple, Set
import io
import pytz
from openpyxl.worksheet.worksheet import Worksheet

from spreadsheet_migrator.spreadsheet_migrator_lib import Parser
from spreadsheet_migrator.spreadsheet_migrator_lib import TestyCreator
from spreadsheet_migrator.spreadsheet_migrator_lib.logs.cases_logs import CasesLogs
from spreadsheet_migrator.spreadsheet_migrator_lib.logs.parameters_logs import ParametersLogs
from spreadsheet_migrator.spreadsheet_migrator_lib.logs.plans_logs import PlansLogs
from spreadsheet_migrator.spreadsheet_migrator_lib.logs.suites_logs import SuitesLogs
from django.forms.models import model_to_dict
import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
from django.http import FileResponse
from rest_framework.response import Response
from rest_framework import status
import csv
import openpyxl

import tempfile
import glob
import os


class Service:
    __dir_reports = "testy_spreadsheet_reports"

    @staticmethod
    def get_reports(request):
        file_name = request.query_params.get("file_name", "")
        uuid = request.query_params.get("uuid", "")
        if file_name:
            if os.path.exists(
                    tempfile.gettempdir() + os.sep + Service.__dir_reports + os.sep + request.query_params[
                        "file_name"]):
                return FileResponse(
                    open(
                        tempfile.gettempdir() + os.sep + Service.__dir_reports + os.sep + request.query_params[
                            "file_name"],
                        "rb"),
                    status=status.HTTP_200_OK)
            else:
                return Response("File is not exist", status=status.HTTP_404_NOT_FOUND)
        elif uuid:
            file_paths = glob.glob(
                tempfile.gettempdir() + os.sep + Service.__dir_reports + os.sep + f"{uuid}_*_testy_logs.json")
            reports_metadata: List[Dict] = []
            for file_path in file_paths:
                with open(file_path, "rb") as file:
                    report_dict = json.load(file)
                    reports_metadata.append(
                        {"report_file_name": os.path.basename(file.name), "report_name": report_dict["report_name"],
                         "creation_time": report_dict["creation_time"], "project": report_dict["project"]})
            return Response(reports_metadata, status=status.HTTP_200_OK)

    @staticmethod
    def fill_report(obj_logs, config):
        report = {}
        for key_info, type_info in [("config", config),
                                    ("created", obj_logs.created),
                                    ("found", obj_logs.found),
                                    ("lack_data", obj_logs.lack_data)]:
            if type_info:
                report[key_info] = type_info
        return report

    @staticmethod
    def create_report_file(uuid, parser: Parser, testy_creator: TestyCreator):
        report = {"project": model_to_dict(parser.project), "report_name": parser.request_data["file"].name,
                  "creation_time": datetime.now(pytz.UTC).isoformat().replace("+00:00", "Z")}
        for key, obj_logs, config in [("suites", testy_creator.suites_logs, parser.config.get("suite")),
                                      ("cases", testy_creator.cases_logs, parser.config.get("case")),
                                      ("parameters", testy_creator.parameters_logs, parser.config.get("parameter")),
                                      ("plans", testy_creator.plans_logs, parser.config.get("plan"))]:
            if config is not None:
                report_info = Service.fill_report(obj_logs, config)
                if report_info:
                    report[key] = report_info
        with tempfile.NamedTemporaryFile(prefix=uuid + "_", suffix="_testy_logs.json", delete=False, mode="w",
                                         dir=tempfile.gettempdir() + os.sep + Service.__dir_reports) as file:
            json.dump(report, file, cls=DjangoJSONEncoder)
        return os.path.basename(file.name)

    @staticmethod
    def delete_empty_rows(parser):
        finished = False
        for i in range(parser.excel_data_ws.max_row, 0, -1):
            for cell in parser.excel_data_ws[i]:
                if cell.value is not None:
                    finished = True
                    break
            if finished:
                break
            else:
                parser.excel_data_ws.delete_rows(idx=i)

    @staticmethod
    def start_process(request) -> str:
        testy_creator = TestyCreator(SuitesLogs(),
                                     CasesLogs(),
                                     ParametersLogs(),
                                     PlansLogs(), request)
        parser = Parser(request.data, testy_creator, json.loads(request.data["config"]))
        Service.delete_empty_rows(parser)
        if parser.config.get("suite") is not None and parser.config.get("suite").get("name") is not None:
            suite_case_parameters_plan: Dict[
                Tuple[str, str], List[Tuple[Dict, List[Dict], Dict]]] = parser.parse_datas_with_suites()
            dict_idcase_plan_idparameters: Dict[
                int, Dict[Tuple[str, str, str, str], Set[int]]] = testy_creator.create_suites_cases_parameters(
                suite_case_parameters_plan,
                parser.project)
            if len(dict_idcase_plan_idparameters) > 0:
                plan_idcases_idparameters: Dict[
                    Tuple[str, str, str, str], Tuple[Set, Set]] = Parser.union_cases_by_equal_parameters(
                    dict_idcase_plan_idparameters)
                testy_creator.create_plans(plan_idcases_idparameters, parser.project)
        else:
            parameters_plan: List[Tuple[List[Dict], Dict]] = parser.parse_datas_without_suites()
            testy_creator.create_datas_without_suite(parameters_plan, parser.project)
        return Service.create_report_file(parser.uuid, parser, testy_creator)
