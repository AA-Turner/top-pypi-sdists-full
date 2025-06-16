"""
    Run a scenario in a model.
    CRUD operations for model run options.

    Do not use this class directly, use FrogModel wrapper instead.
"""

import time
from typing import Optional, Literal, TypedDict, get_args, Dict
from collections import defaultdict
import optilogic
import pandas as pd
from .decorators import requires_parameter, ensure_correlation_id


class RunScenarioResponse(TypedDict):
    """ "
    Response from running a scenario
    """

    status: Literal["error", "success"]
    message: str


UI_DISPLAY_CATEGORIES = Literal["Basic", "Advanced"]

STATUS = Literal["Include", "Exclude"]

ENGINES = Literal["neo", "throg", "triad", "dendro", "hopper", "dart"]

RESOURCE_SIZES = Literal[
    "mini",
    "4xs",
    "3xs",
    "2xs",
    "xs",
    "s",
    "m",
    "l",
    "xl",
    "2xl",
    "3xl",
    "4xl",
    "overkill",
]


class ModelRunOption(TypedDict):
    """
    Model Run Option
    """

    option: str
    status: Optional[STATUS] = "Include"
    value: str = ""
    technology: Optional[ENGINES] = "neo"
    description: str = ""
    datatype: str = "String"
    uidisplayname: str = ""
    uidisplaycategory: UI_DISPLAY_CATEGORIES = "Basic"
    uidisplayorder: Optional[int]
    uidisplaysubcategory: Optional[str]


class RunScenario:
    """
    Run a scenario in a model.
    CRUD operations for model run options.

    Do not use this class directly, use FrogModel wrapper instead.
    """

    def __init__(self, frog_model=None):
        if not frog_model:
            raise ValueError("Frog model is required.")

        self.frog_model = frog_model
        self.model_name = frog_model.model_name
        self.app_key = frog_model._app_key
        self.log = frog_model.log

        if self.app_key:
            self.api = optilogic.pioneer.Api(auth_legacy=False, appkey=self.app_key)
        else:
            raise ValueError(
                "Could not authenticate, app_key is required to run a scenario"
            )

    def __handle_error__(self, _correlation_id, message):
        """
        Log an error and return a response
        """
        self.log.error("%s %s", _correlation_id, message)
        raise ValueError(message)

    @ensure_correlation_id
    def get_all_run_parameters(
        self, engine: Optional[str] = "", _correlation_id=None
    ) -> dict:
        """
        Get all run parameters for a model
        """
        try:
            self.log.info(
                "%s Getting all run parameters for model %s with engine %s",
                _correlation_id,
                self.model_name,
                engine,
            )

            sql_statement = "SELECT * FROM ModelRunOptions"
            params = {}
            if engine:
                if engine not in get_args(ENGINES):
                    return self.__handle_error__(
                        _correlation_id,
                        f"Invalid engine {engine}, list of valid engines: {get_args(ENGINES)}",
                    )

                if engine == "neo_with_infeasibility":
                    engine = "neo"
                    self.log.info(
                        "%s Running with infeasibility check enabled, setting engine to neo",
                        _correlation_id,
                    )

                sql_statement += " WHERE technology ILIKE %(engine)s"
                params["engine"] = f"%{engine}%"

            self.log.info(
                "%s Running SQL statement: %s with params %s",
                _correlation_id,
                sql_statement,
                params,
            )

            data = self.frog_model.read_sql(sql_statement, params=params)

            if not data.empty:
                self.log.info("%s Run parameters fetched successfully", _correlation_id)
                return {
                    "status": "success",
                    "message": "Run parameters fetched successfully",
                    "data": data.to_dict(orient="records"),
                }

            return self.__handle_error__(
                _correlation_id, "Error fetching run parameters"
            )
        except Exception as e:
            return self.__handle_error__(
                _correlation_id, f"Error fetching run parameters: {str(e)}"
            )

    @ensure_correlation_id
    def update_run_parameter_value(
        self, option: str, value: str, _correlation_id=None
    ) -> dict:
        """
        Update a run parameter value in a model
        """
        try:
            self.log.info(
                "%s Updating run parameter %s in model %s with value %s",
                _correlation_id,
                option,
                self.model_name,
                value,
            )

            model_run_option = self.frog_model.read_sql(
                "SELECT * FROM ModelRunOptions WHERE LOWER(option) = %(option)s;",
                params={"option": option.lower()},
            )

            if model_run_option.empty:
                return self.__handle_error__(
                    _correlation_id, f"Run parameter {option} does not exist"
                )

            self.log.info(
                "%s Run parameter %s exists in model %s",
                _correlation_id,
                option,
                self.model_name,
            )

            parameter_datatype = model_run_option.iloc[0]["datatype"]

            self.log.info(
                "%s Run parameter %s has datatype %s checking if value is valid...",
                _correlation_id,
                option,
                parameter_datatype,
            )

            self.__model_run_option_datatype_valid__(
                parameter_datatype, value, _correlation_id
            )

            value = str(value)
            self.log.info(
                "%s Value is valid. Updating run parameter %s with value %s",
                _correlation_id,
                option,
                value,
            )

            self.frog_model.exec_sql(
                f"UPDATE ModelRunOptions SET value = '{value}' WHERE LOWER(option) = '{option.lower()}';"
            )

            self.log.info(
                "%s Run parameter %s updated successfully", _correlation_id, option
            )

            return {
                "status": "success",
                "message": f"Run parameter {option} updated successfully",
            }
        except Exception as e:
            return self.__handle_error__(
                _correlation_id, f"Error updating run parameter {option}: {str(e)}"
            )

    @ensure_correlation_id
    def add_run_parameter(
        self, model_run_option: ModelRunOption, _correlation_id=None
    ) -> dict:
        """ "
        Add a run parameter to a model

        model_name: str - The name of the model
        model_run_option: ModelRunOption - The run parameter to add
            option: str - The name of the run parameter
            status: str - The status of the run parameter, default: Include. Options: Include, Exclude. If Exclude, the run parameter will not be used in the scenario run and not be shown in the UI
            value: str - The value of the run parameter, default: "", has to follow the datatype rules
            technology: str - The technology of the run parameter, default: neo. Options: neo, neo_with_infeasibility, throg, triad, dendro, hopper, dart
            description: str - The description of the run parameter, default: ""
            datatype: str - The datatype of the run parameter, default: String. Options: String, int, double, [True, False], [custom1, custom2]
            uidisplaycategory: str - The UI display category of the run parameter, default: Basic. Options: Basic, Advanced. Basic means it will be shown in the CF UI
            uidisplayname: str - The CF UI display name of the run parameter, default: option. If not set, it will be the same as the option if not provided
            uidisplayorder: int - The order of the run parameter in the CF UI, default: highest order + 1, cannot be the same as another run parameter
        _correlation_id: str - The correlation id for logging
        """
        try:
            default_model_run_option = ModelRunOption(
                option="",
                status="Include",
                value="",
                technology="neo",
                description="",
                datatype="String",
                uidisplaycategory="Basic",
                uidisplayname="",
                uidisplayorder=None,
                uidisplaysubcategory="",
            )

            model_run_option = {**default_model_run_option, **model_run_option}

            ### Validate MRO parameters ###
            if not model_run_option["option"]:
                return self.__handle_error__(
                    _correlation_id, "Option parameter is required"
                )

            if model_run_option["status"] not in get_args(STATUS):
                return self.__handle_error__(
                    _correlation_id,
                    f"Invalid status {model_run_option['status']}, list of valid statuses: {get_args(STATUS)}",
                )

            if model_run_option["technology"] == "neo_with_infeasibility":
                model_run_option["technology"] = "neo"
                self.log.info("%s Setting technology to neo", _correlation_id)

            if model_run_option["technology"] not in get_args(ENGINES):
                return self.__handle_error__(
                    _correlation_id,
                    f"Invalid technology {model_run_option['technology']}, list of valid technologies: {get_args(ENGINES)}",
                )

            if not model_run_option["uidisplaycategory"] in get_args(
                UI_DISPLAY_CATEGORIES
            ):
                return self.__handle_error__(
                    _correlation_id,
                    f"Invalid UI display category {model_run_option['uidisplaycategory']}, list of valid categories: {get_args(UI_DISPLAY_CATEGORIES)}",
                )

            self.__model_run_option_datatype_valid__(
                model_run_option["datatype"], model_run_option["value"], _correlation_id
            )

            all_model_run_options = self.get_all_run_parameters(
                _correlation_id=_correlation_id
            )

            # check if MRO with column option already exists
            for option in all_model_run_options["data"]:
                if option["option"].lower() == model_run_option["option"].lower():
                    return self.__handle_error__(
                        _correlation_id,
                        f"Run parameter {model_run_option['option']} already exists",
                    )

            if not model_run_option["uidisplayname"]:
                model_run_option["uidisplayname"] = model_run_option["option"]
                self.log.info(
                    "%s Setting uidisplayname to %s",
                    _correlation_id,
                    model_run_option["option"],
                )

            # If uidisplayorder is not set, get the highest order and increment
            # if is set check if it already exists
            if model_run_option["uidisplayorder"] is None:
                self.log.info(
                    "%s Getting highest order for uidisplayorder", _correlation_id
                )

                highest_order = 0
                for option in all_model_run_options["data"]:
                    display_order = int(option["uidisplayorder"])
                    highest_order = max(highest_order, display_order)

                model_run_option["uidisplayorder"] = highest_order + 1
                self.log.info(
                    "%s Setting uidisplayorder to %s",
                    _correlation_id,
                    model_run_option["uidisplayorder"],
                )
            else:
                for option in all_model_run_options["data"]:
                    if option["uidisplayorder"] == str(
                        model_run_option["uidisplayorder"]
                    ):
                        return self.__handle_error__(
                            _correlation_id,
                            f"Run parameter with order {model_run_option['uidisplayorder']} already exists",
                        )

            model_run_option["technology"] = (
                f"[{model_run_option['technology'].upper()}]"
            )
            self.log.info(
                "%s Setting technology to %s",
                _correlation_id,
                model_run_option["technology"],
            )

            self.frog_model.exec_sql(
                f"INSERT INTO ModelRunOptions (option, status, value, technology, description, datatype, uidisplaycategory, uidisplayname, uidisplayorder) VALUES ('{model_run_option['option']}', '{model_run_option['status']}', '{model_run_option['value']}', '{model_run_option['technology']}', '{model_run_option['description']}', '{model_run_option['datatype']}', '{model_run_option['uidisplaycategory']}', '{model_run_option['uidisplayname']}', {model_run_option['uidisplayorder']});"
            )

            self.log.info(
                "%s Run parameter %s added successfully",
                _correlation_id,
                model_run_option["option"],
            )

            return {
                "status": "success",
                "message": f"Run parameter {model_run_option['option']} added successfully",
                "model_run_option": model_run_option,
            }
        except Exception as e:
            return self.__handle_error__(
                _correlation_id,
                f"Error adding run parameter {model_run_option['option']}: {str(e)}, {model_run_option}",
            )

    @ensure_correlation_id
    def delete_run_parameter(self, option: str, _correlation_id=None) -> dict:
        """
        Delete a model run option

        Args:
            option: str -- The name of the run parameter

        Returns:
            dict: A dictionary containing the status and message
        """
        try:
            self.log.info(
                "%s Deleting run parameter %s in model %s",
                _correlation_id,
                option,
                self.model_name,
            )

            model_run_option = self.frog_model.read_sql(
                "SELECT * FROM ModelRunOptions WHERE LOWER(option) = %(option)s;",
                params={"option": option.lower()},
            )

            if model_run_option.empty:
                return self.__handle_error__(
                    _correlation_id, f"Run parameter {option} does not exist"
                )

            self.log.info(
                "%s Run parameter %s exists in model %s",
                _correlation_id,
                option,
                self.model_name,
            )

            self.frog_model.exec_sql(
                f"DELETE FROM ModelRunOptions WHERE LOWER(option) = '{option.lower()}';"
            )

            self.log.info(
                "%s Run parameter %s deleted successfully", _correlation_id, option
            )

            return {
                "status": "success",
                "message": f"Run parameter {option} deleted successfully",
            }
        except Exception as e:
            return self.__handle_error__(
                _correlation_id, f"Error deleting run parameter {option}: {str(e)}"
            )

    @ensure_correlation_id
    @requires_parameter("workspace")
    @requires_parameter("job_key")
    def get_job_logs(
        self, job_key: str, workspace: str = "Studio", _correlation_id=None
    ) -> Dict[str, str]:
        """
        Get the logs of a job

        Args:
            job_key: str -- The key of the job
            workspace: str -- The workspace of the job
            _correlation_id: str -- The correlation id for logging

        Returns:
            dict: A dictionary containing the status, message, and logs
        """
        try:
            result = self.api.wksp_job_file_result(jobkey=job_key, wksp=workspace)

            if not isinstance(result, str) and result.get("result") == "error":
                return self.__handle_error__(
                    _correlation_id,
                    f"Error fetching logs for job {job_key}: {result.get('message')}",
                )

            return {"status": "success", "message": "", "logs": result}
        except Exception as e:
            return self.__handle_error__(
                _correlation_id, f"Error fetching logs for job {job_key}: {str(e)}"
            )

    @ensure_correlation_id
    def all_scenarios_preview(self, _correlation_id=None) -> dict:
        """
        Get all scenarios preview

        Args:
            _correlation_id: str -- The correlation id for logging

        Returns:
            dict: A dictionary containing the runnable scenarios, their items, and the technology
        """

        query = """
            SELECT
                s.scenarioname AS scenario_name,
                s.technology AS technology,
                s.notes AS scenario_notes,
                si.itemname AS item_name,
                si.tablename AS table_name,
                si.action AS action,
                si.condition AS condition,
                si.conditiontype AS condition_type,
                si.namedfilters AS named_filters,
                si.notes AS item_notes,
                sia.itemorder AS item_order
            FROM
                scenarios s
            LEFT JOIN
                scenarioitemassignments sia
                ON s.scenarioname = sia.scenarioname
            LEFT JOIN
                scenarioitems si
                ON sia.itemname = si.itemname
            ORDER BY
                s.scenarioname, sia.itemorder;
        """

        # TODO:
        # filter by technology
        # paginate
        # less details
        # is this good logic with iteration if big data?

        try:
            self.log.info(
                "%s Getting all scenarios for model %s",
                _correlation_id,
                self.model_name,
            )

            data = self.frog_model.read_sql(query)

            if data.empty:
                return {"status": "success", "data": []}

            scenarios_dict = defaultdict(
                lambda: {
                    "scenarioname": "",
                    "technology": "",
                    "notes": "",
                    "scenarioitems": [],
                }
            )

            for _, row in data.iterrows():
                scenario_name = row["scenario_name"]

                # If the scenario doesn't exist, initialize it
                if not scenarios_dict[scenario_name]["scenarioname"]:
                    scenarios_dict[scenario_name]["scenarioname"] = scenario_name
                    scenarios_dict[scenario_name]["technology"] = row["technology"]
                    scenarios_dict[scenario_name]["notes"] = row["scenario_notes"]

                # If there are scenario items, add them to the list
                if pd.notna(row["item_name"]):
                    scenarios_dict[scenario_name]["scenarioitems"].append(
                        {
                            "itemname": row["item_name"],
                            "tablename": row["table_name"],
                            "action": row["action"],
                            "condition": row["condition"],
                            "conditiontype": row["condition_type"],
                            "namedfilters": row["named_filters"],
                            "notes": row["item_notes"],
                            "itemorder": row["item_order"],
                        }
                    )

            # Convert the defaultdict to a list of scenarios
            scenarios = list(scenarios_dict.values())

            # Sort scenario items by item_order
            for scenario in scenarios:
                scenario["scenarioitems"].sort(
                    key=lambda x: (
                        x["itemorder"]
                        if x.get("itemorder") is not None
                        else float("inf")
                    )
                )

            self.log.info("%s Scenarios preview fetched successfully", _correlation_id)

            return {
                "status": "success",
                "message": "Scenarios preview fetched successfully",
                "data": scenarios,
            }
        except Exception as e:
            return self.__handle_error__(
                _correlation_id, f"Error fetching scenarios: {str(e)}"
            )

    def __neo_infeasibility_check_procedure__(
        self, run_neo_with_infeasibility: bool = False, _correlation_id: str = None
    ):
        """
        Run NEO infeasibility check procedure.
        Has to update ModelRunOptions to False
        if not running infeasibility if the last check was set to True.

        Args:
            run_neo_with_infeasibility: bool -- Run the scenario with infeasibility check enabled - Default False
            _correlation_id: str -- Correlation id for logging / tracing (for internal use)

        Returns:
            None or str: The engine to run the scenario or None
        """
        infeasibility_update_value = str(run_neo_with_infeasibility)

        self.log.info(
            "%s Updating infeasibility check value to %s",
            _correlation_id,
            infeasibility_update_value,
        )

        # TODO: update or create?? There is an option that this parameter does not exist
        self.frog_model.exec_sql(
            f"UPDATE ModelRunOptions SET value = '{infeasibility_update_value}' WHERE option = 'CheckInfeasibility';"
        )

    def __check_if_contains_unkown_scenarios__(
        self, scenarios: [str], _correlation_id: str
    ) -> Dict[str, str]:
        """ "
        Check if all of the scenario names exist in the model.

        If one does not exist, return an error message.

        Args:
            scenarios: [str] -- Name of the scenario or list of scenarios to check
            _correlation_id: str -- Correlation id for logging / tracing (for internal use)

        Returns:
            dict: A dictionary containing the status and message
        """

        try:
            self.log.info(
                "%s Checking if scenario names exist in a model: %s",
                _correlation_id,
                scenarios,
            )

            if not scenarios:
                self.log.info(
                    "%s No scenarios to check in DB after filtering out baseline/all",
                    _correlation_id,
                )

                return {}

            query = f"""
                SELECT
                    ScenarioName,
                    CASE 
                        WHEN technology IS NULL OR TRIM(technology) = '' THEN 'neo'
                        ELSE technology
                    END AS technology
                FROM Scenarios
                WHERE ScenarioName IN ('{"', '".join(scenarios)}');
            """

            result_df = self.frog_model.read_sql(query)

            existing_scenarios = set(result_df["scenarioname"].unique())
            input_scenarios = set(scenarios)

            missing_scenarios = input_scenarios - existing_scenarios

            if missing_scenarios:
                self.__handle_error__(
                    _correlation_id,
                    f"Scenarios {missing_scenarios} do not exist. "
                    "Make sure the scenario names are correct and remember names are case sensitive.",
                )

            self.log.info(
                "%s Scenarios %s exist in model %s",
                _correlation_id,
                scenarios,
                self.model_name,
            )

            return result_df.groupby("technology")["scenarioname"].apply(list).to_dict()
        except Exception as e:
            return {
                "status": True,
                "message": self.__handle_error__(
                    _correlation_id,
                    f"Error checking if scenario names exist in a model: {str(e)}",
                ),
            }

    def __run_scenario_tags__(
        self, engine: ENGINES, scenarios: [str], tags: str
    ) -> str:
        final_tags = f"ModelName={self.model_name}, Engine={engine}, Scenarios={','.join(scenarios)}"
        if tags:
            final_tags += f", {tags}"

        return final_tags

    def __build_command_args_for_run__(
        self,
        scenario_list_for_engine: [str],
        engine: ENGINES,
        resource_size: RESOURCE_SIZES,
        workspace: str,
        version: str,
    ) -> str:
        command_args_example = (
            f"-m '{self.model_name}' "
            f"-s '{','.join(scenario_list_for_engine)}' "
            f"-e '{engine.lower()}' "
            f"-r '{resource_size}' "
            f"-w '{workspace}'"
        )

        if version:
            command_args_example += f" -v '{version}'"

        return command_args_example

    def __determine_engines_and_scenarios_to_run__(
        self, scenarios: [str], engine: ENGINES, _correlation_id: str
    ) -> [ENGINES, dict]:
        """
        Determine engines and scenarios to run based on the input.

        If "all" is passed then check if user passed engine or not.
        If engine is passed, group all scenarios under the engine.
        If engine is not passed, group all scenarios under the engine from the scenario table.
        If multiple engines are found, fetch and group scenarios by technology.

        If 'all' is not passed, check if all scenarios exist in the model.
        If not, return an error message.
        If all scenarios exist, group them by engine.
        If engine is passed, group all scenarios under the engine.
        If engine is not passed, group all scenarios under the engine from the scenario table.

        Then convert engine to list if it is a string.

        Validate if the engine is in the list of valid engines.

        Args:
            scenarios: [str] -- Name of the scenario or list of scenarios to run
            engine: ENGINES -- Engine to run the scenario on
            _correlation_id: str -- Correlation id for logging / tracing (for internal use)

        Returns:
            [ENGINES, dict]: The engine to run the scenario on and the grouped scenarios
        """
        grouped_scenarios = {}

        if "all" == scenarios[0].lower():
            if engine:
                self.log.info(
                    "%s Scenario name 'all' passed, engine passed as well, setting engine to %s",
                    _correlation_id,
                )

                grouped_scenarios = {engine: "All"}
            else:
                self.log.info(
                    "%s Scenario name 'all' passed, but without engine. Checking if there are more than one technology in the model",
                    _correlation_id,
                )

                query = """
                    SELECT DISTINCT 
                        CASE 
                            WHEN technology IS NULL OR TRIM(technology) = '' THEN 'neo'
                            ELSE technology
                        END AS technology
                    FROM Scenarios;
                """

                all_technologies_df = self.frog_model.read_sql(query)
                existing_technologies = set(all_technologies_df["technology"])

                if len(existing_technologies) == 0:
                    self.log.info(
                        "%s No technology found in the model, defaulting to neo",
                        _correlation_id,
                    )

                    grouped_scenarios = {"neo": "All"}
                    engine = "neo"

                if len(existing_technologies) == 1:
                    self.log.info(
                        "%s Only one technology found in the model, setting engine to %s",
                        _correlation_id,
                        existing_technologies,
                    )

                    grouped_scenarios = {all_technologies_df["technology"][0]: "All"}
                    engine = all_technologies_df["technology"][0]

                if len(existing_technologies) > 1:
                    self.log.info(
                        "%s More than one technology found in the model, fetching all scenarios and grouping by technology",
                        _correlation_id,
                    )

                    query = """
                        SELECT ScenarioName, 
                            CASE 
                                WHEN technology IS NULL OR TRIM(technology) = '' THEN 'neo'
                                ELSE technology
                            END AS technology
                        FROM Scenarios;
                    """

                    grouped_scenarios = (
                        self.frog_model.read_sql(query)
                        .groupby("technology")["scenarioname"]
                        .apply(list)
                        .to_dict()
                    )
                    engine = list(grouped_scenarios.keys())
        else:
            # Filter out "baseline" from the names to explicitly check
            names_to_check = [
                name for name in scenarios if name.lower() != "baseline"
            ]

            # Check if all of the scenario names exist in the model
            contains_unkown_scenarios_response = (
                self.__check_if_contains_unkown_scenarios__(
                    names_to_check, _correlation_id
                )
            )

            # if engine passed, group all scenarios under the engine
            # if engine not passed, group all scenarios under the engine from the scenario table
            if engine:
                grouped_scenarios = {engine: scenarios}
            else:
                grouped_scenarios = contains_unkown_scenarios_response
                self.log.info(
                    "%s No engine passed, fetching engines from the model",
                    _correlation_id,
                )
                engines = list(grouped_scenarios.keys())
                self.log.info(
                    "%s Engines found in the model: %s",
                    _correlation_id,
                    grouped_scenarios,
                )

                if len(engines) == 0:
                    self.log.info(
                        "%s No engines found in the model, defaulting to neo",
                        _correlation_id,
                    )
                    engine = "neo"

                    if len(scenarios) > 0:
                        grouped_scenarios = {"neo": scenarios}
                    else:
                        grouped_scenarios = {"neo": "Baseline"}

                if len(engines) == 1:
                    engine = engines[0]
                    self.log.info(
                        "%s One engine found in the model, setting engine to %s",
                        _correlation_id,
                        engine,
                    )

                if len(engines) > 1:
                    self.log.info(
                        "%s More than one engine found in the model, setting engine to list of engines",
                        _correlation_id,
                    )
                    engine = engines

        if isinstance(engine, str):
            engine = [engine]

        # Check if valid engines in list ENGINES
        for engine_i in engine:
            if engine_i.lower() not in get_args(ENGINES):
                return self.__handle_error__(
                    _correlation_id,
                    f"Invalid engine {engine_i}, list of valid engines: {get_args(ENGINES)}",
                )

        return engine, grouped_scenarios

    def __validate_run_parameters__(
        self,
        scenarios: [str],
        resource_size: RESOURCE_SIZES,
        engine: ENGINES,
        _correlation_id: str,
    ):
        """
        Validate run parameters before running the scenario.

        Args:
            scenarios: [str] -- Name of the scenario or list of scenarios to run
            resource_size: RESOURCE_SIZES -- Resource size to run the scenario on
            engine: ENGINES -- Engine to run the scenario on
            _correlation_id: str -- Correlation id for logging / tracing (for internal use)
        """

        if not isinstance(scenarios, list):
            return self.__handle_error__(
                _correlation_id,
                "Scenarios must be passed as a list. Example: ['Scenario']",
            )

        if not scenarios or len(scenarios) == 0:
            return self.__handle_error__(
                _correlation_id, "Must pass at least one scenario to run."
            )

        if resource_size not in get_args(RESOURCE_SIZES):
            return self.__handle_error__(
                _correlation_id,
                f"Invalid resource size {resource_size}, valid: {get_args(RESOURCE_SIZES)}",
            )

        if engine and engine not in get_args(ENGINES):
            return self.__handle_error__(
                _correlation_id,
                f"Invalid engine {engine}, list of valid engines: {get_args(ENGINES)}.",
            )

        if "all" in [name.lower() for name in scenarios] and len(scenarios) > 1:
            return self.__handle_error__(
                _correlation_id,
                "Cannot run all scenarios and specific scenarios at the same time. "
                "If you want to run all scenarios, pass ['All'] only.",
            )

    @ensure_correlation_id
    @requires_parameter("workspace")
    def run_multiple_scenarios_with_custom_configuration(
        self,
        scenarios_with_custom_configuration: list[dict],
        workspace: str = "Studio",
        fire_and_forget: bool = False,
        _correlation_id: str | None = None,
    ) -> RunScenarioResponse:
        """
            Run multiple scenarios with different configurations.

            Args:
                scenarios_with_custom_configuration (list[dict]): List of dictionaries containing scenario name, engine, and resource size
                                                                 {scenario_name: str, engine: str, resource_size: str}
                workspace (str): Workspace to run the scenario in - Default "Studio"
                fire_and_forget (bool): If True, do not monitor the job. Default False
            
            Returns:
                RunScenarioResponse: a dict describing success/failure status, job keys, etc.
        """

        try:
            self.log.info(
                "%s Starting process to run multiple scenarios with custom configurations in model %s",
                _correlation_id,
                self.model_name,
            )

            self.log.info(
                "%s Check validity of engines and resource sizes",
                _correlation_id,
            )

            # 1) Validate input and group scenarios by engine and resource size
            scenario_names = []
            grouped_scenario_by_engine_and_resource_size_dict = {}
            for scenario_configuration in scenarios_with_custom_configuration:
                scenario_name = scenario_configuration.get("scenario_name")
                engine = scenario_configuration.get("engine")
                resource_size = scenario_configuration.get("resource_size")

                if not scenario_name:
                    return self.__handle_error__(
                        _correlation_id,
                        "Scenario name is required in each object in scenarios_with_custom_configuration",
                    )

                if not engine:
                    return self.__handle_error__(
                        _correlation_id,
                        "Engine is required in each object in scenarios_with_custom_configuration",
                    )

                if engine not in get_args(ENGINES):
                    return self.__handle_error__(
                        _correlation_id,
                        f"Invalid engine {engine}, list of valid engines: {get_args(ENGINES)}",
                    )

                if not resource_size:
                    return self.__handle_error__(
                        _correlation_id,
                        "Resource size is required in each object in scenarios_with_custom_configuration",
                    )

                if resource_size not in get_args(RESOURCE_SIZES):
                    return self.__handle_error__(
                        _correlation_id,
                        f"Invalid resource size {resource_size}, valid: {get_args(RESOURCE_SIZES)}",
                    )

                scenario_names.append(scenario_name)

                key = (engine, resource_size)
                if key not in grouped_scenario_by_engine_and_resource_size_dict:
                    grouped_scenario_by_engine_and_resource_size_dict[key] = []

                grouped_scenario_by_engine_and_resource_size_dict[key].append(scenario_name)

            self.log.info(
                "%s Check if all scenarios exist in the model",
                _correlation_id,
            )

            # 2) Check if all of the scenario names exist in the model
            names_to_check = [
                name for name in scenario_names if name.lower() not in ["baseline"]
            ]
            self.__check_if_contains_unkown_scenarios__(
                names_to_check, _correlation_id
            )

            # 3) Iterate over the grouped scenarios and run solver job
            solver_job_keys = {}
            for key, scenario_list in grouped_scenario_by_engine_and_resource_size_dict.items():
                engine, resource_size = key
                command_args = self.__build_command_args_for_run__(
                    scenario_list, engine, resource_size, workspace, ""
                )

                self.log.info(
                    "%s Starting scenario(s) on engine '%s' with command_args: %s",
                    _correlation_id,
                    engine,
                    command_args,
                )

                # Run solver
                run_model_result = self.api.wksp_job_start(
                    wksp=workspace,
                    file_path="",
                    commandArgs=command_args,
                    tags=self.__run_scenario_tags__(engine, scenario_list, ""),
                    command="run_model",
                    resourceConfig="4xs",
                )

                if not run_model_result or "jobKey" not in run_model_result:
                    return self.__handle_error__(
                        _correlation_id,
                        f"Error starting scenario(s) {scenario_list} on engine '{engine}'",
                    )

                job_key = run_model_result["jobKey"]
                solver_job_keys[key] = job_key

                self.log.info(
                    "%s Scenario(s) %s started with job key %s on engine '%s' with resource size '%s'",
                    _correlation_id,
                    scenario_list,
                    job_key,
                    engine,
                    resource_size,
                )

            # 4) Return early if fire and forget
            if fire_and_forget:
                return {
                    "status": "success",
                    "message": "Scenario(s) started successfully (fire and forget).",
                    "job_keys": solver_job_keys,
                }

            # 5) Await Scenarios to complete
            jobs_information_by_engine = {}
            for key, solver_job_key in solver_job_keys.items():
                engine, resource_size = key
                self.log.info(
                    "%s Awaiting scenario(s) on engine '%s' with job key %s for resource size '%s' to complete.",
                    _correlation_id,
                    engine,
                    solver_job_key,
                    resource_size,
                )
                is_done = self.api.util_job_monitor(
                    wksp=workspace, job_key=solver_job_key, secs_max=86399, stop_when="done"
                )
                if not is_done:
                    return self.__handle_error__(
                        _correlation_id,
                        f"Scenario(s) on engine '{engine}' on resource size: '{resource_size}' did not complete within 24 hours",
                    )

                child_jobs_response = self.api.wksp_jobs(
                    wksp=workspace, tags=f"ParentJob={solver_job_key}"
                )
                jobs = []
                for job in child_jobs_response["jobs"]:
                    scenario_name = job["jobInfo"]["tags"].split(", ")
                    scenario_name = [
                        s.split("=")[1] for s in scenario_name if "Scenario=" in s
                    ][0]
                    jobs.append(
                        {
                            "job_key": job["jobKey"],
                            "status": job["status"],
                            "scenario_name": scenario_name,
                        }
                    )

                jobs_information_by_engine[engine] = {
                    "count_per_status": child_jobs_response["statusCounts"],
                    "jobs": jobs,
                }

            return {
                "status": "success",
                "message": "Scenario(s) completed successfully.",
                "job_run_information": jobs_information_by_engine,
            }
        except Exception as e:
            return {"status": "error", "message": f"Error running multiple scenarios: {str(e)}"}

    @ensure_correlation_id
    @requires_parameter("workspace")
    def run(
        self,
        scenarios: list[str] = ["Baseline"],
        workspace: str = "Studio",
        engine: None | ENGINES = None,
        run_neo_with_infeasibility: bool = False,
        resource_size: RESOURCE_SIZES = "s",
        tags: str = "",
        version: str = "",
        fire_and_forget: bool = False,
        _correlation_id: str | None = None,
        check_configuration_before_run: bool = False,
    ) -> RunScenarioResponse:
        """
        Run scenarios within a model.
        Can run all scenarios in a model by passing ["All"].
        If scenario names are not passed, will run the Baseline scenario (default).
        Scenario names are case sensitive.

        If engine is not passed, will run on the default
        engine from the scenario table (technology column).
        If technology is not set in the scenario table, will default to "neo".
        If technology is set to unknown value, will return an error.

        By default function will run the scenario on resource size S, which can be
        changed by passing resource_size parameter.

        By default function will await all of the scenarios to complete. Pass
        `fire_and_forget=True` to run in the background.

        If not sure about configuration before running, pass
        `check_configuration_before_run=True` to return the final config
        without actually running anything.

        If running with infeasibility check, set run_neo_with_infeasibility=True;
        engine parameter will be ignored and set to "neo".

        Args:
            scenarios (list[str]): Name(s) of the scenario(s) to run. Default ["Baseline"]
            workspace (str): Workspace to run the scenario in - Default "Studio"
            engine (str | None): Engine(s) to run on - Default is derived from scenario table
            run_neo_with_infeasibility (bool): If True, forcibly run "neo" with infeasibility check
            resource_size (str): Resource size to run the scenario on - default "s"
            tags (str): Tags to run the scenario with
            version (str): Version of the sovler to run
            fire_and_forget (bool): If True, do not monitor the job. Default False
            _correlation_id (str | None): Correlation ID for logs/tracing. If None, auto-generated
            check_configuration_before_run (bool): If True, only return the config, do not run anything.

        Returns:
            RunScenarioResponse: a dict describing success/failure status, job keys, etc.
        """
        # TODO:
        # What if Baseline passed but scenario does not exist in the DB?
        # Test if model has no scenarios, but passed "All" or "Baseline"
        # debug, extra logs option run...
        # model run option specific update/create ... add as parameter to function
        try:
            self.log.info(
                "%s Starting process to run scenario(s) %s in model %s",
                _correlation_id,
                scenarios,
                self.model_name,
            )

            # 1) Set engine to NEO if infeasibility check is enabled
            if run_neo_with_infeasibility:
                if (
                    engine and engine != "neo"
                ):  # Inform user that engine will be set to neo
                    self.log.info(
                        "%s Running with infeasibility check enabled, setting engine to neo",
                        _correlation_id,
                    )

                engine = "neo"

            # 2) Validate run parameters
            self.__validate_run_parameters__(
                scenarios, resource_size, engine, _correlation_id
            )

            # 3) Determine engine and scenarios to run
            engine, grouped_scenarios = self.__determine_engines_and_scenarios_to_run__(
                scenarios, engine, _correlation_id
            )

            # 4) Run NEO infeasibility check procedure
            self.__neo_infeasibility_check_procedure__(
                run_neo_with_infeasibility, _correlation_id
            )

            # Lowercase the engine names in grouped_scenarios
            # if there are 2 engines with same name when lowercase then join values
            merged_grouped_scenarios = defaultdict(list)

            for key, value in grouped_scenarios.items():
                lower_key = key.lower() # Lowercase the key.
                merged_grouped_scenarios[lower_key].extend(value)

            grouped_scenarios = dict(merged_grouped_scenarios)

            # 5) Check and return configuration before run if enabled
            if check_configuration_before_run:
                config_objects = {}

                for e in engine:
                    e = e.lower()
                    scenario_list_for_engine = grouped_scenarios.get(e, [])

                    config_objects[e] = {
                        "command_args": self.__build_command_args_for_run__(
                            scenario_list_for_engine,
                            e,
                            resource_size,
                            workspace,
                            version,
                        ),
                        "tags": self.__run_scenario_tags__(
                            e, scenario_list_for_engine, tags
                        ),
                    }

                return {
                    "status": "success",
                    "message": "Configuration check before run is enabled, no scenario run will be executed. Configuration check passed successfully. To run the scenario, set check_configuration_before_run to False",
                    "model_name": self.model_name,
                    "workspace": workspace,
                    "configurations": config_objects,
                }

            # 6) Kick off Solvers
            job_key_by_engine = {}
            for e in engine:
                e = e.lower()
                scenario_list_for_engine = grouped_scenarios.get(e, [])

                command_args = self.__build_command_args_for_run__(
                    scenario_list_for_engine, e, resource_size, workspace, version
                )

                self.log.info(
                    "%s Starting scenario(s) on engine '%s' with command_args: %s",
                    _correlation_id,
                    e,
                    command_args,
                )

                run_model_result = self.api.wksp_job_start(
                    wksp=workspace,
                    file_path="",
                    commandArgs=command_args,
                    tags=self.__run_scenario_tags__(e, scenario_list_for_engine, tags),
                    command="run_model",
                    resourceConfig="4xs",
                )

                if not run_model_result or "jobKey" not in run_model_result:
                    return self.__handle_error__(
                        _correlation_id,
                        f"Error starting scenario(s) {scenario_list_for_engine} on engine '{e}'",
                    )

                job_key = run_model_result["jobKey"]
                job_key_by_engine[e] = job_key
                self.log.info(
                    "%s Scenario(s) %s started with job key %s on engine '%s'",
                    _correlation_id,
                    scenario_list_for_engine,
                    job_key,
                    e,
                )

            # 7) If fire and forget, return job keys
            if fire_and_forget:
                return {
                    "status": "success",
                    "message": "Scenario(s) started successfully (fire and forget).",
                    "job_keys": job_key_by_engine,
                }

            # 8) Await scenarios to complete
            jobs_information_by_engine = {}
            for e, key in job_key_by_engine.items():
                e = e.lower()
                self.log.info(
                    "%s Awaiting scenario(s) on engine '%s' with job key %s to complete",
                    _correlation_id,
                    e,
                    key,
                )
                is_done = self.api.util_job_monitor(
                    wksp=workspace, job_key=key, secs_max=86399, stop_when="done"
                )
                if not is_done:
                    return self.__handle_error__(
                        _correlation_id,
                        f"Scenario(s) on engine '{e}' did not complete within 24 hours",
                    )

                child_jobs_response = self.api.wksp_jobs(
                    wksp=workspace, tags=f"ParentJob={key}"
                )
                jobs = []
                for job in child_jobs_response["jobs"]:
                    scenario_name = job["jobInfo"]["tags"].split(", ")
                    scenario_name = [
                        s.split("=")[1] for s in scenario_name if "Scenario=" in s
                    ][0]
                    jobs.append(
                        {
                            "job_key": job["jobKey"],
                            "status": job["status"],
                            "scenario_name": scenario_name,
                        }
                    )

                jobs_information_by_engine[e] = {
                    "count_per_status": child_jobs_response["statusCounts"],
                    "jobs": jobs,
                }

            return {
                "status": "success",
                "message": "Scenario(s) completed successfully.",
                "job_run_information": jobs_information_by_engine,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error running scenario(s): {str(e)}",
            }

    def __model_run_option_datatype_valid__(
        self, datatype: str, value: str, _correlation_id: str
    ) -> dict:
        """
        Check if the datatype of a model run option is valid
        """

        if datatype == "String":
            return {"status": "success", "message": "Value is a string"}

        if datatype == "int":
            try:
                int(value)
                return {"status": "success", "message": "Value is an integer"}
            except ValueError:
                return self.__handle_error__(
                    _correlation_id, "Value must be an integer, example: '1'"
                )

        if datatype == "double":
            try:
                float(value)
                return {"status": "success", "message": "Value is a float"}
            except ValueError:
                return self.__handle_error__(
                    _correlation_id, "Value must be a float, example: '1.0'"
                )

        if datatype == "[True, False]":
            if value.lower() in ["true", "false"]:
                return {"status": "success", "message": "Value is a boolean"}

            return self.__handle_error__(
                _correlation_id,
                "Value must be True or False as type string, example: 'True' or 'False'",
            )

        if datatype.startswith("[") and datatype.endswith("]"):
            custom_values = datatype[1:-1].split(", ")
            if value not in custom_values:
                return self.__handle_error__(
                    _correlation_id, f"Value must be one of {custom_values}"
                )

            return {"status": "success", "message": f"Value is one of {custom_values}"}

        return self.__handle_error__(
            _correlation_id,
            f"Unsupported datatype {datatype}, supported datatypes: String, int, double, [True, False], [custom1, custom2]",
        )

    @ensure_correlation_id
    @requires_parameter("workspace")
    def check_scenario_status(
        self,
        scenario_name: Optional[str] = "",
        job_key: Optional[str] = "",
        history: str = "7",
        workspace: str = "Studio",
        _correlation_id: str = "",
    ) -> Dict[str, str]:
        """
        Check the status of a running scenario.
        Scenario name or job key is required.
        Scenario name is case sensitive.

        For scenario name it will return statusCounts for all jobs with the scenario name. Example:

        "data": {
            "submitted": 1,
            "starting": 2,
            "started": 3,
            "running": 4,
            "done": 5,
            "stopping": 6,
            "stopped": 7,
            "canceling": 8,
            "cancelled": 9,
            "error": 10
        }

        Args:
            scenario_name: str -- Name of the scenario to check
            job_key: str -- Key of the job to check
            history: str -- Number of days to check the history for (default: 7). For all history, use all
            workspace: str -- Workspace where the scenario is running - Default Studio

        Returns:
            dict: A dictionary containing 'status' and 'message'.When using scenario name, it will also contain 'statusCounts' and 'jobs'
        """
        if not scenario_name and not job_key:
            return self.__handle_error__(
                _correlation_id, "Scenario name or job key is required."
            )

        try:
            if scenario_name and not job_key:
                tags = f"ModelName={self.model_name}, Scenario={scenario_name}"  # this is specified when running a scenario and it can't be overriden

                all_jobs = self.api.wksp_jobs(
                    wksp=workspace, tags=tags, history=history
                )

                if not all_jobs:
                    return {
                        "status": "success",
                        "message": f"No jobs with scenario name {scenario_name} in the last {history} days",
                    }

                return {
                    "status": "success",
                    "message": "",
                    "statusCounts": all_jobs["statusCounts"],
                    "jobs": all_jobs["jobs"],
                }

            job = self.api.wksp_job_status(jobkey=job_key, wksp=workspace)

            if job.get("result") == "error":
                return self.__handle_error__(
                    _correlation_id,
                    f"Error checking scenario status: {job.get('message')}",
                )

            return {"status": "success", "message": "", "job": job}
        except Exception as e:
            return self.__handle_error__(
                _correlation_id, f"Error checking scenario status: {str(e)}"
            )

    @ensure_correlation_id
    @requires_parameter("workspace")
    def stop_scenario(
        self,
        scenario_name: Optional[str] = "",
        job_key: Optional[str] = "",
        workspace: str = "Studio",
        _correlation_id: str = "",
    ) -> Dict[str, str]:
        """
        Stop a running scenario. Scenario name or job key is required.
        Scenario name is case sensitive. Will stop multiple jobs if multiple jobs are running with the same scenario name.

        Args:
            scenario_name: str -- Name of the scenario to stop
            job_key: str -- Key of the job to stop
            workspace: str -- Workspace where the scenario is running - Default Studio

        Returns:
            dict: A dictionary containing 'status' and 'message
        """
        if not scenario_name and not job_key:
            return self.__handle_error__(
                _correlation_id, "Scenario name or job key is required."
            )

        try:
            if scenario_name and not job_key:
                # this is specified when running a scenario and it can't be overriden
                tags = f"ModelName={self.model_name}, Scenario={scenario_name}"

                # Easier to fetch submitted and running jobs rather than fetching all as would have to filter through completed
                submitted_jobs = self.api.wksp_jobs(
                    wksp=workspace, tags=tags, status="submitted"
                )
                running_jobs = self.api.wksp_jobs(
                    wksp=workspace, tags=tags, status="running"
                )
                all_jobs = submitted_jobs["jobs"] + running_jobs["jobs"]

                if not all_jobs:
                    return {
                        "status": "success",
                        "message": f"No submitted or running jobs with scenario name {scenario_name}",
                    }

                for job in all_jobs:
                    job_key = job["jobKey"]
                    if job_key:
                        self.api.wksp_job_stop(wksp=workspace, jobkey=job_key)

                return {
                    "status": "success",
                    "message": f"Stopped {len(all_jobs)} jobs with scenario name {scenario_name}",
                }

            response = self.api.wksp_job_stop(wksp=workspace, jobkey=job_key)
            if response.get("result") == "error":
                return self.__handle_error__(
                    _correlation_id,
                    f"Error stopping job with key {job_key}: {response.get('message')}",
                )

            return {"status": "success", "message": f"Stopped job with key {job_key}"}

        except Exception as e:
            return {"status": "error", "message": str(e)}

    @ensure_correlation_id
    @requires_parameter("workspace")
    @requires_parameter("job_key")
    def job_records(
        self,
        job_key: str,
        workspace: str = "Studio",
        _correlation_id: str = "",
        keys: Optional[str] = None,
        show_logs: bool = True,
    ) -> dict:
        """
        Fetch the job records for a job.
        Will return all records if keys are not specified.

        Args:
            job_key: str -- Key of the job
            workspace: str -- Workspace where the job is running - Default Studio
            _correlation_id: str -- Correlation id for logging / tracing (for internal use)
            keys: str -- Keys of the records to fetch

        Returns:
            dict: A dictionary containing the status, message, and records
        """
        try:
            if show_logs:
                self.log.info(
                    "%s Fetching live logs for job %s", _correlation_id, job_key
                )

            result = self.api.wksp_job_ledger(jobkey=job_key, wksp=workspace, keys=keys)

            if result.get("result") == "error":
                return self.__handle_error__(
                    _correlation_id,
                    f"Error fetching job records for job {job_key}: {result.get('message')}",
                )

            return {"status": "success", "records": result["records"]}
        except Exception as e:
            return self.__handle_error__(
                _correlation_id, f"Error fetching live logs for job {job_key}: {str(e)}"
            )

    @ensure_correlation_id
    @requires_parameter("workspace")
    @requires_parameter("job_key")
    def get_all_jobs_for_solver_job(
        self, job_key: str, workspace: str = "Studio", _correlation_id: str = ""
    ) -> dict:
        """
        Fetch all job records for a solver job.
        If job is running, not all jobs might be available.

        Args:
            job_key: str -- Key of the job
            workspace: str -- Workspace where the job is running - Default Studio
            _correlation_id: str -- Correlation id for logging / tracing (for internal use)

        Returns:
            dict: A dictionary containing the status, message, and records
        """
        try:
            self.log.info("%s Fetching job solver status %s", _correlation_id, job_key)
            solver_job_response = self.check_scenario_status(
                job_key=job_key, workspace=workspace, _correlation_id=_correlation_id
            )
            solver_job = solver_job_response.get("job")

            if solver_job["jobInfo"]["command"] != "run_model":
                return self.__handle_error__(
                    _correlation_id, f"Job with key {job_key} is not a solver job"
                )

            solver_job_status = solver_job["status"]

            if solver_job_status in ["submitted", "starting", "started"]:
                self.log.info(
                    "%s Job status is %s, waiting for job to start running. Will try again in 5 seconds",
                    _correlation_id,
                    solver_job_status,
                )
                time.sleep(5)
                return self.get_all_jobs_for_solver_job(
                    job_key, workspace, _correlation_id
                )

            self.log.info(
                "%s Fetching all jobs for solver job %s", _correlation_id, job_key
            )

            child_jobs = self.api.wksp_jobs(wksp=workspace, tags=f"ParentJob={job_key}")

            if solver_job_status == "running":
                if child_jobs["count"] == 0:  # if zero jobs, retry
                    self.log.info(
                        "%s Job status is running, no child jobs found, will try again in 5 seconds",
                        _correlation_id,
                    )
                    time.sleep(5)
                    return self.get_all_jobs_for_solver_job(
                        job_key, workspace, _correlation_id
                    )

                self.log.info(
                    "%s Job status is running, not all jobs might be available.",
                    _correlation_id,
                )

            return {
                "status": "success",
                "message": f"All jobs for solver job {job_key} fetched successfully",
                "jobs": child_jobs["jobs"],
            }
        except Exception as e:
            return self.__handle_error__(
                _correlation_id,
                f"Error fetching child jobs for job {job_key}: {str(e)}",
            )

    @ensure_correlation_id
    @requires_parameter("workspace")
    @requires_parameter("job_key")
    def tail_job_records(
        self, job_key: str, workspace: str = "Studio", _correlation_id: str = ""
    ) -> dict:
        """
        Tail the job records for a job.
        If job is running, will tail the logs until the job is completed.
        If job is completed, will print all of the records

        Args:
            job_key: str -- Key of the job
            workspace: str -- Workspace where the job is running - Default Studio
            _correlation_id: str -- Correlation id for logging / tracing (for internal use)
        Returns:
            dict: A dictionary containing the status, message, and records
        """
        try:
            self.log.info("%s Tailing job records for job %s", _correlation_id, job_key)
            job_status_response = self.check_scenario_status(
                job_key=job_key,
                workspace=workspace,
                history="1",
                _correlation_id=_correlation_id,
            )
            job_status = job_status_response["job"]["status"]

            records = []
            if job_status in ["submitted", "starting", "started"]:
                self.log.info(
                    "%s Job status is %s, waiting for job to start running. Will try again in 5 seconds",
                    _correlation_id,
                    job_status,
                )
                time.sleep(5)
                return self.tail_job_records(job_key, workspace, _correlation_id)
            elif job_status == "running":
                while True:
                    job_status_response = self.check_scenario_status(
                        job_key=job_key,
                        workspace=workspace,
                        history="1",
                        _correlation_id=_correlation_id,
                    )
                    job_status = job_status_response["job"]["status"]
                    records_response = self.job_records(
                        job_key, workspace, _correlation_id, show_logs=False
                    )
                    new_all_records = sorted(
                        records_response["records"],
                        key=lambda record: record["timestamp"],
                    )
                    if len(new_all_records) > len(records):
                        records_for_print = new_all_records[len(records) :]
                        for record in records_for_print:
                            print(record["message"])
                        records = new_all_records

                    if job_status != "running":
                        self.log.info(
                            "%s Job status changed to %s, stopping tailing job records",
                            _correlation_id,
                            job_status,
                        )
                        break
                    time.sleep(5)
            else:
                self.log.info(
                    "%s Job has been completed, fetching all records", _correlation_id
                )
                records_response = self.job_records(job_key, workspace, _correlation_id)
                records = sorted(
                    records_response["records"], key=lambda record: record["timestamp"]
                )
                for record in records:
                    print(record["message"])

            return {"status": "success", "records": records}
        except Exception as e:
            return self.__handle_error__(
                _correlation_id,
                f"Error tailing job records for job {job_key}: {str(e)}",
            )

    @ensure_correlation_id
    @requires_parameter("workspace")
    @requires_parameter("job_key")
    def get_scenario_run_error_log(
        self, job_key: str, workspace: str = "Studio", _correlation_id: str = ""
    ) -> dict:
        """
        Fetch the error logs for a job.

        Args:
            job_key: str -- Key of the job
            wksp: str -- Workspace where the job is running - Default Studio
            _correlation_id: str -- Correlation id for logging / tracing (for internal use)

        Returns:
            dict: A dictionary containing the status, message, and error logs
        """
        try:
            result = self.api.wksp_job_file_error(jobkey=job_key, wksp=workspace)

            if not isinstance(result, str) and result.get("result") == "error":
                return self.__handle_error__(
                    _correlation_id,
                    f"Error fetching erro logs for job {job_key}: {result.get('message')}",
                )

            return {"status": "success", "message": "", "error": result}
        except Exception as e:
            return self.__handle_error__(
                _correlation_id,
                f"Error fetching error logs for job {job_key}: {str(e)}",
            )


    @ensure_correlation_id
    @requires_parameter("workspace")
    def all_running_scenarios(self, workspace: str = "Studio", _correlation_id: str = "") -> dict:
        """"
        Fetch all running scenarios in a workspace.

        Args:
            workspace: str -- Workspace to fetch the running scenarios from - Default Studio
            _correlation_id: str -- Correlation id for logging / tracing (for internal use)

        Returns:
            dict: A dictionary containing the status, message and jobs
        """
        try:
            tags = f"ModelName={self.model_name}"

            submitted_jobs = self.api.wksp_jobs(
                wksp=workspace, tags=tags, status="submitted"
            )
            running_jobs = self.api.wksp_jobs(
                wksp=workspace, tags=tags, status="running"
            )
            all_jobs = submitted_jobs["jobs"] + running_jobs["jobs"]

            return {
                "status": "success",
                "message": f"Found {len(all_jobs)} running scenarios for model {self.model_name}",
                "jobs": all_jobs,
            }
        except Exception as e:
            return self.__handle_error__(
                _correlation_id,
                f"Error fetching all running scenarios: {str(e)}",
            )

    # def get_last_run_recommendation(self, scenario_name: Optional[str] = '', job_key: Optional[str]= '', workspace: str = "Studio") -> Dict[str, str]:
    # TODO: Some of the jobs have it, some don't
    # print("get_last_run_recommendation")

    # def get_last_run_resource_metrics(self, scenario_name: Optional[str] = '', job_key: Optional[str]= '', workspace: str = "Studio") -> Dict[str, str]:
    #     wksp_job_metrics_max

    ## Can track multiple scenarios by tags -> util_job_monitor_set

    # def create scenario - validation named filter per table, name validation, technology validation
    # def all named filters/per table
