from typing import Dict, List, Tuple, Set

from django.forms.models import model_to_dict
from tests_description.models import TestCase, TestSuite
from tests_representation.api.v1.serializers import TestPlanInputSerializer, TestPlanOutputSerializer
from tests_representation.models import Parameter, TestPlan, Test
from tests_representation.services.testplans import TestPlanService


class TestyCreator:
    def __init__(self, suites_logs, cases_logs, parameters_logs, plans_logs, request):
        self.suites_logs = suites_logs
        self.cases_logs = cases_logs
        self.parameters_logs = parameters_logs
        self.plans_logs = plans_logs
        self.request = request

    def create_suites_cases_parameters(self, suite_case_parameters_plan: Dict[
        Tuple[str, str], List[Tuple[Dict, List[Dict], Dict]]],
                                       project) -> Dict[int, Dict[Tuple[str, str, str, str], Set[int]]]:
        """
        The function searches for a suite in a project with that name, otherwise it creates it.
        After that, it calls the function to create cases in the selected suite and parameters.
        Returns the id of the case and the parameters to be selected when creating the test plan.

        Examples:
        plan = ("Release (name)", Release (description),started_at, due_date)
        idcase = 1
        idparameters = {1, 2, 3}
        dict_idcase_plan_idparameters: Dict[int, Dict[Tuple[str, str, str, str], Set[int]]] = {idcase: {plan: idparameters]}
        """
        dict_idcase_plan_idparameters: Dict[int, Dict[Tuple[str, str, str, str], Set[int]]] = {}
        for suite, cases_parameters_plan in suite_case_parameters_plan.items():
            found_suite, created = TestSuite.objects.get_or_create(project=project, name=suite[0],
                                                                   description=suite[1])
            if created:
                self.suites_logs.created[found_suite.id] = model_to_dict(found_suite)
            else:
                if not self.suites_logs.created.get(found_suite.id) and not self.suites_logs.found.get(found_suite.id):
                    self.suites_logs.found[found_suite.id] = model_to_dict(found_suite)
            dict_idcase_plan_idparameters |= self.__create_and_bind_cases_parameters(cases_parameters_plan,
                                                                                     found_suite,
                                                                                     project)
        return dict_idcase_plan_idparameters

    def create_parameters(self, parameters, project):
        """
        The function searches for a parameters in a project with that name, otherwise it creates it.
        Returns the parameters ids.
        """
        set_of_ids_params: Set = set()
        for parameter in parameters:
            found_parameter, created = Parameter.objects.get_or_create(project=project, data=parameter["data"],
                                                                       group_name=parameter["group_name"])
            if created:
                self.parameters_logs.created[found_parameter.id] = model_to_dict(found_parameter)
            else:
                if not self.parameters_logs.created.get(found_parameter.id) and not self.parameters_logs.found.get(
                        found_parameter.id):
                    self.parameters_logs.found[found_parameter.id] = model_to_dict(found_parameter)
            set_of_ids_params.add(found_parameter.id)
        return set_of_ids_params

    def create_datas_without_suite(self, parameters_plan: List[Tuple[List[Dict], Dict]], project):
        """
        Creates parameters and test plans. Called if suites were not selected.
        """
        for parameters, plan in parameters_plan:
            set_of_ids_params: Set = self.create_parameters(parameters, project)
            if plan:
                self.create_plans(
                    {(plan.get("name"), plan.get("description", ""), plan.get("started_at"), plan.get("due_date")): (
                        set(), set_of_ids_params)},
                    project)

    def create_case(self, case, project, suite):
        """
        The function searches for a case in a project with that name, otherwise it creates it.
        Returns the case.
        """
        found_case, created = TestCase.objects.get_or_create(project=project, name=case["name"], suite=suite,
                                                             scenario=case["scenario"],
                                                             description=case.get("description", ""),
                                                             setup=case.get("setup", ""),
                                                             teardown=case.get("teardown", ""),
                                                             estimate=case.get("estimate", None))
        if created:
            self.cases_logs.created[found_case.id] = model_to_dict(found_case)
        else:
            if not self.cases_logs.created.get(found_case.id) and not self.cases_logs.found.get(found_case.id):
                self.cases_logs.found[found_case.id] = model_to_dict(found_case)
        return found_case

    def __create_and_bind_cases_parameters(self, cases_parameters_plan: List[Tuple[Dict, List[Dict], Dict]], suite,
                                           project) -> Dict[int, Dict[Tuple[str, str, str, str], Set[int]]]:
        """
        If there are cases and test plans (there may be parameters), then the
        function combines them together to further creation of test plans.
        Otherwise, it creates only cases, or creates test-plans with parameters.

        Examples:
        plan = ("Release (name)", "Release (description)", started_at, due_date)
        idcase = 1
        idparameters = {1, 2, 3}
        dict_idcase_plan_idparameters: Dict[int, Dict[Tuple[str, str, str, str], Set[int]]] = {idcase: {plan: idparameters]}
        """
        dict_idcase_plan_idparameters: Dict[int, Dict[Tuple[str, str, str, str], Set[int]]] = {}
        for case, parameters, plan in cases_parameters_plan:
            if case and plan:
                found_case = self.create_case(case, project, suite)
                found_plans = TestPlan.objects.filter(
                    name=plan.get("name"),
                    description=plan.get("description", ""),
                    started_at=plan.get("started_at"),
                    due_date=plan.get("due_date"),
                    project=project
                )
                if len(parameters) == 0:
                    if not found_plans:
                        if found_case.id not in dict_idcase_plan_idparameters:
                            dict_idcase_plan_idparameters[found_case.id] = {}
                            dict_idcase_plan_idparameters[found_case.id][
                                (plan["name"], plan.get("description", ""), plan["started_at"],
                                 plan["due_date"])] = set()
                        else:
                            dict_idcase_plan_idparameters[found_case.id][
                                (plan["name"], plan.get("description", ""), plan["started_at"],
                                 plan["due_date"])] = set()
                    else:
                        for found_plan in TestPlanOutputSerializer(found_plans, many=True,
                                                                   context={'request': self.request}).data:
                            if not self.plans_logs.created.get(found_plan["id"]) and not self.plans_logs.found.get(
                                    found_plan["id"]):
                                self.plans_logs.found[found_plan["id"]] = found_plan
                else:
                    set_of_ids_params: Set = self.create_parameters(parameters, project)
                    if len(set_of_ids_params) > 0:
                        if not found_plans:
                            if found_case.id in dict_idcase_plan_idparameters:
                                if (plan["name"], plan.get("description", ""), plan["started_at"], plan["due_date"]) in \
                                        dict_idcase_plan_idparameters[found_case.id]:
                                    idparameters = dict_idcase_plan_idparameters[found_case.id][
                                        (plan["name"], plan.get("description", ""), plan["started_at"],
                                         plan["due_date"])]
                                    idparameters |= set_of_ids_params
                                else:
                                    dict_idcase_plan_idparameters[found_case.id][
                                        (plan["name"], plan.get("description", ""), plan["started_at"],
                                         plan["due_date"])] = set_of_ids_params
                            else:
                                dict_idcase_plan_idparameters[found_case.id] = {}
                                dict_idcase_plan_idparameters[found_case.id][
                                    (plan["name"], plan.get("description", ""), plan["started_at"],
                                     plan["due_date"])] = set_of_ids_params
                        else:
                            for found_plan in TestPlanOutputSerializer(found_plans, many=True,
                                                                       context={'request': self.request}).data:
                                if not self.plans_logs.created.get(found_plan["id"]) and not self.plans_logs.found.get(
                                        found_plan["id"]):
                                    self.plans_logs.found[found_plan["id"]] = found_plan
            elif case:
                self.create_parameters(parameters, project)
                self.create_case(case, project, suite)
            elif plan:
                set_of_ids_params: Set = self.create_parameters(parameters, project)
                self.create_plans(
                    {(plan.get("name"), plan.get("description", ""), plan.get("started_at"), plan.get("due_date")): (
                        set(), set_of_ids_params)},
                    project)
        return dict_idcase_plan_idparameters

    def create_plans(self, plan_idcases_idparameters: Dict[
        Tuple[str, str, str, str], Tuple[Set, Set]], project):
        """
        The function creates test plans based on the transmitted pairs of test cases and parameters.
        """
        for plan, idcases_idparameters in plan_idcases_idparameters.items():
            found_plans = TestPlan.objects.filter(
                name=plan[0],
                description=plan[1],
                started_at=plan[2],
                due_date=plan[3],
                project=project
            )
            if not found_plans:
                idcases, idparameters = idcases_idparameters
                test_plan = {"name": plan[0],
                             "test_cases": list(idcases),
                             "parameters": list(idparameters),
                             "project": project.id,
                             "description": plan[1],
                             'started_at': plan[2], 'due_date': plan[3]}
                serializer = TestPlanInputSerializer(data=test_plan)
                serializer.is_valid(raise_exception=True)
                created_plans = []
                if serializer.validated_data.get('parameters'):
                    created_plans = TestPlanService().testplan_bulk_create(serializer.validated_data)
                else:
                    created_plans.append(TestPlanService().testplan_create(serializer.validated_data))
                for created_plan in TestPlanOutputSerializer(created_plans, many=True,
                                                             context={'request': self.request}).data:
                    self.plans_logs.created[created_plan["id"]] = created_plan
            else:
                for found_plan in TestPlanOutputSerializer(found_plans, many=True,
                                                           context={'request': self.request}).data:
                    if not self.plans_logs.created.get(found_plan["id"]) and not self.plans_logs.found.get(
                            found_plan["id"]):
                        self.plans_logs.found[found_plan["id"]] = found_plan
