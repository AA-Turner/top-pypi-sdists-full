import os

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from spreadsheet_migrator.spreadsheet_migrator_lib import TestyException
from spreadsheet_migrator.spreadsheet_migrator_lib.service import Service

from tests_description.models import TestCase, TestSuite
from tests_representation.models import Parameter


class SpreadsheetMigrator(APIView):

    def get(self, request):
        return Service.get_reports(request)

    def post(self, request):
        try:
            format_file = os.path.splitext(request.data["file"].name)[1]
            if format_file == ".xlsx":
                report_file_name: str = Service.start_process(request)
                return Response(report_file_name, status=status.HTTP_200_OK)
            else:
                return Response(f"This file format {format_file} does not support.",
                                status=status.HTTP_400_BAD_REQUEST)
        except TestyException as e:
            return Response(e.message, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        except TestSuite.MultipleObjectsReturned:
            return Response("Suites with the same name were found in the same project, this should not be the case.",
                            status=status.HTTP_400_BAD_REQUEST)
        except TestCase.MultipleObjectsReturned:
            return Response("Cases with the same data were found in the same project, this should not be the case.",
                            status=status.HTTP_400_BAD_REQUEST)
        except Parameter.MultipleObjectsReturned:
            return Response(
                "Parameters with the same data were found in the same project, this should not be the case.",
                status=status.HTTP_400_BAD_REQUEST)
