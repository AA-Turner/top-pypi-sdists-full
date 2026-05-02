"""Tests for Standard Bots Python SDKs."""

import json
import time

import pytest
from standardbots import StandardBotsRobot
from standardbots.auto_generated import models
from standardbots.auto_generated.apis import RobotKind
from standardbots.auto_generated.models import RobotControlMode, RobotControlModeEnum


def approx_equal(a: float, b: float, precision: int = 3) -> bool:
    return round(a, precision) == round(b, precision)


class TestAuthenticationMiddleware:
    """Tests for authentication"""

    @pytest.mark.parametrize(
        ["robot_kind"], [(RobotKind.Live,), (RobotKind.Simulated,)]
    )
    def test_authentication_bad(
        self, robot_kind: RobotKind, api_url: StandardBotsRobot
    ) -> None:
        """Must be authenticated for endpoint (io state)"""
        client = StandardBotsRobot(
            url=api_url,
            token="invalid",
            robot_kind=robot_kind,
        )
        with client.connection():
            res = client.io.status.get_io_state()
        assert res.status == 401

    @pytest.mark.parametrize(
        ["robot_kind"], [(RobotKind.Live,), (RobotKind.Simulated,)]
    )
    def test_authentication_good(
        self, robot_kind: RobotKind, api_url: str, api_token: str
    ) -> None:
        """Must be authenticated for endpoint (io state)."""
        client = StandardBotsRobot(
            url=api_url,
            token=api_token,
            robot_kind=robot_kind,
        )
        with client.connection():
            res = client.io.status.get_io_state()

        assert res.ok()

    @pytest.mark.parametrize(
        ["robot_kind"], [(RobotKind.Live,), (RobotKind.Simulated,)]
    )
    def test_not_authentication_ok(self, robot_kind: RobotKind, api_url: str) -> None:
        """No authentication needed for endpoint (health)."""
        client = StandardBotsRobot(
            url=api_url,
            token="invalid",
            robot_kind=robot_kind,
        )
        with client.connection():
            res = client.status.health.get_health()
        ok_res = res.ok()

        assert isinstance(ok_res, models.StatusHealthResponse)
        assert ok_res.health == models.StatusHealthEnum.Ok


class TestPostRoutineEditorRoutinePlay:
    """Tests: [POST] `/api/v1/routine-editor/routines/:routineId/play`"""

    def test_routine_play_with_brakes(
        self, routine_sample_id: str, client_live: StandardBotsRobot
    ) -> None:
        """Test routine play when robot is braked"""
        client = client_live

        play_res = client.routine_editor.routines.stop()

        with client.connection():
            res = client.movement.brakes.get_brakes_state()

        assert not res.isNotOk()
        data = res.data
        assert isinstance(data, models.BrakesState)
        assert data.state is not None

        # make sure to break robot
        if data.state != models.BrakesStateEnum.Engaged:
            new_state = models.BrakesStateEnum.Engaged
            body = models.BrakesState(state=new_state)

            with client.connection():
                res = client.movement.brakes.set_brakes_state(body)

            assert not res.isNotOk()
            data = res.data
            assert isinstance(data, models.BrakesState)
            assert data.state == new_state

        #  try to play routine on braked robot
        body = models.PlayRoutineRequest(variables={})
        play_res = client.routine_editor.routines.play(
            routine_id=routine_sample_id, body=body
        )

        assert play_res.isNotOk()
        assert play_res.status == 400
        assert play_res.data.error == models.ErrorEnum.BrakesMustBeDisengaged

        #  unbrake robot
        new_state = models.BrakesStateEnum.Disengaged
        body = models.BrakesState(state=new_state)

        with client.connection():
            res = client.movement.brakes.set_brakes_state(body)

            assert not res.isNotOk()
            data = res.data
            assert isinstance(data, models.BrakesState)
            assert data.state == new_state

        #  trigger successful play
        body = models.PlayRoutineRequest(variables={})
        play_res_after = client.routine_editor.routines.play(
            routine_id=routine_sample_id, body=body
        )

        assert not play_res_after.isNotOk()
        assert play_res_after.status == 200

        client.routine_editor.routines.stop()

    def test_play_not_existing_routine(self, client_live: StandardBotsRobot) -> None:
        """Trigger start not existing routine"""
        client = client_live

        with client.connection():
            not_existing_routine_id = "not_existing_id"
            body = models.PlayRoutineRequest(variables={})
            res = client.routine_editor.routines.play(
                routine_id=not_existing_routine_id, body=body
            )

            assert res.isNotOk()
            assert res.status == 404
            assert res.data.error == models.ErrorEnum.RoutineDoesNotExist

    def test_play_routine_which_is_playing(
        self, routine_sample_id: str, client_live: StandardBotsRobot
    ) -> None:
        """Trigger start routine that is playing"""
        client = client_live

        with client.connection():
            # make sure to unbreak robot
            brakes_res = client.movement.brakes.get_brakes_state()
            if brakes_res.data.state == models.BrakesStateEnum.Engaged:
                res = client.movement.brakes.set_brakes_state(
                    models.BrakesState(state=models.BrakesStateEnum.Disengaged)
                )
                assert not res.isNotOk()
            body = models.PlayRoutineRequest(variables={})
            client.routine_editor.routines.play(routine_id=routine_sample_id, body=body)

            #  second play attempt should throw an error
            res_after = client.routine_editor.routines.play(
                routine_id=routine_sample_id, body=body
            )

            assert res_after.isNotOk()
            assert res_after.status == 400
            assert res_after.data.error == models.ErrorEnum.CannotPlayRoutine

            client.routine_editor.routines.stop()

    def test_play_paused_routine(
        self, routine_sample_id: str, client_live: StandardBotsRobot
    ) -> None:
        """Trigger play routine if it's paused"""
        client = client_live

        with client.connection():
            # make sure to unbreak robot
            brakes_res = client.movement.brakes.get_brakes_state()
            if brakes_res.data.state == models.BrakesStateEnum.Engaged:
                res = client.movement.brakes.set_brakes_state(
                    models.BrakesState(state=models.BrakesStateEnum.Disengaged)
                )
                assert not res.isNotOk()

            body = models.PlayRoutineRequest(variables={})
            client.routine_editor.routines.play(routine_id=routine_sample_id, body=body)

            pause_res = client.routine_editor.routines.pause(
                routine_id=routine_sample_id
            )

            assert not pause_res.isNotOk()
            assert pause_res.status == 200

            res = client.routine_editor.routines.play(
                routine_id=routine_sample_id, body=body
            )
            assert not res.isNotOk()
            assert res.status == 200
            assert res.data.status == models.RobotStatusEnum.RoutineRunning

            routine_res = client.routine_editor.routines.get_state(
                routine_id=routine_sample_id
            )

            assert not routine_res.data.is_paused

            client.routine_editor.routines.stop()

    def test_play_stopped_routine(
        self, routine_sample_id: str, client_live: StandardBotsRobot
    ) -> None:
        """Trigger play routine if it's stopped(and test environment variables)"""
        client = client_live

        with client.connection():
            # make sure to unbreak robot
            brakes_res = client.movement.brakes.get_brakes_state()
            if brakes_res.data.state == models.BrakesStateEnum.Engaged:
                res = client.movement.brakes.set_brakes_state(
                    models.BrakesState(state=models.BrakesStateEnum.Disengaged)
                )
                assert not res.isNotOk()
            variable_value = "9"
            variable_name = "test_public_api_global"
            body = models.PlayRoutineRequest(variables={variable_name: variable_value})

            start_res = client.routine_editor.routines.play(
                routine_id=routine_sample_id, body=body
            )
            assert not start_res.isNotOk()
            assert start_res.status == 200
            assert start_res.data.status == models.RobotStatusEnum.RoutineRunning

            # Retry mechanism for async variable loading
            max_retries = 10
            delay_seconds = 1

            for _ in range(max_retries):
                var_response = client.routine_editor.variables.load(variable_name)

                if (
                    not var_response.isNotOk()
                    and var_response.status == 200
                    and isinstance(var_response.data, models.RuntimeVariable)
                    and var_response.data.value == variable_value
                ):
                    break

                time.sleep(delay_seconds)
            else:
                pytest.fail(
                    f"Failed to retrieve expected variable value '{variable_value}' after {max_retries} retries"
                )

            client.routine_editor.routines.stop()

    #  TODO: can add tests when there is failure in routine(collision etc)


class TestGetEquipment:
    """Tests: [GET] `/api/v1/equipment`

    Not covered here: Ensuring that updates to equipment config and enabled/disabled status are reflected in the response.
    """

    def test_get_equipment(self, client_live: StandardBotsRobot) -> None:
        """Get equipment test"""
        client = client_live

        with client.connection():
            res = client.equipment.get_equipment()

            assert not res.isNotOk()
            assert res.status == 200
            assert isinstance(res.data, models.GetEquipmentConfigResponse)
            assert res.data.equipment is not None
            assert isinstance(res.data.equipment, list)
            if len(res.data.equipment) > 0:
                assert isinstance(res.data.equipment[0], models.EquipmentConfig)

                equipment = res.data.equipment[0]
                assert equipment.id is not None
                assert equipment.kind is not None
                assert equipment.is_enabled is not None
                assert equipment.config is not None

                # Can be parsed as JSON
                assert json.loads(equipment.config) is not None


class TestGetEquipmentEndEffectorConfiguration:
    """Tests: [GET] `/api/v1/equipment/end-effector/configuration`"""

    @pytest.mark.gripper("onrobot_2fg7")
    def test_2fg7_config(self, client_live: StandardBotsRobot) -> None:
        """2fg7 get config test"""
        client = client_live

        with client.connection():
            config = client.equipment.get_gripper_configuration()

            assert not config.isNotOk()
            assert config.status == 200
            assert config.data.kind == models.GripperKindEnum.Onrobot2Fg7
            assert config.data.onrobot_2fg7 is not None

    @pytest.mark.gripper("onrobot_2fg14")
    def test_2fg14_config(self, client_live: StandardBotsRobot) -> None:
        """2fg14 get config test"""
        client = client_live

        with client.connection():
            config = client.equipment.get_gripper_configuration()

            assert not config.isNotOk()
            assert config.status == 200
            assert config.data.kind == models.GripperKindEnum.Onrobot2Fg14
            assert config.data.onrobot_2fg14 is not None

    @pytest.mark.gripper("onrobot_3fg15")
    def test_3fg15_config(self, client_live: StandardBotsRobot) -> None:
        """3fg15 get config test"""
        client = client_live

        with client.connection():
            config = client.equipment.get_gripper_configuration()

            assert not config.isNotOk()
            assert config.status == 200
            assert config.data.kind == models.GripperKindEnum.Onrobot3Fg15
            assert config.data.onrobot_3fg15 is not None

    @pytest.mark.gripper("dh_ag")
    def test_dh_ag_config(self, client_live: StandardBotsRobot) -> None:
        """dh_ag get config test"""
        client = client_live

        with client.connection():
            config = client.equipment.get_gripper_configuration()

            assert not config.isNotOk()
            assert config.status == 200
            assert config.data.kind == models.GripperKindEnum.DhAg
            assert config.data.dh_ag is not None

    @pytest.mark.gripper("dh_pgc")
    def test_dh_pgc_config(self, client_live: StandardBotsRobot) -> None:
        """dh_pgc get config test"""
        client = client_live

        with client.connection():
            config = client.equipment.get_gripper_configuration()

            assert not config.isNotOk()
            assert config.status == 200
            assert config.data.kind == models.GripperKindEnum.DhPgc
            assert config.data.dh_pgc is not None

    @pytest.mark.gripper("dh_cgi")
    def test_dh_cgi_config(self, client_live: StandardBotsRobot) -> None:
        """dh_cgi get config test"""
        client = client_live

        with client.connection():
            config = client.equipment.get_gripper_configuration()

            assert not config.isNotOk()
            assert config.status == 200
            assert config.data.kind == models.GripperKindEnum.DhCgi
            assert config.data.dh_cgi is not None

    @pytest.mark.gripper("onrobot_screwdriver")
    def test_onrobot_screwdriver_config(self, client_live: StandardBotsRobot) -> None:
        """onrobot_screwdriver get config test"""
        client = client_live

        with client.connection():
            config = client.equipment.get_gripper_configuration()

            assert not config.isNotOk()
            assert config.status == 200
            assert config.data.kind == models.GripperKindEnum.OnrobotScrewdriver
            assert config.data.onrobot_screwdriver is not None

    @pytest.mark.gripper("schunk_egx")
    def test_schunk_egx_config(self, client_live: StandardBotsRobot) -> None:
        """schunk_egx get config test"""
        client = client_live

        with client.connection():
            config = client.equipment.get_gripper_configuration()

            assert not config.isNotOk()
            assert config.status == 200
            assert config.data.kind == models.GripperKindEnum.SchunkEgx


class TestPostEquipmentEndEffectorControl:
    """Tests: [POST] `/api/v1/equipment/end-effector/control`"""

    @pytest.mark.gripper("onrobot_2fg7")
    def test_2fg7_movement_live(
        self,
        client_live: StandardBotsRobot,
    ) -> None:
        # TODO add more tests to check different configs
        """2fg7 movement test: live mode"""
        client = client_live

        min_width_meters = 0.047
        max_width_meters = 0.085

        with client.connection():
            res = client.equipment.onrobot_2fg7_move(
                value=min_width_meters, unit_kind=models.LinearUnitKind.Meters
            )

            assert not res.isNotOk()
            assert res.status == 200
            res.ok()

            config = client.equipment.get_gripper_configuration()
            assert config.data.onrobot_2fg7.width_outer == min_width_meters

            res = client.equipment.onrobot_2fg7_move(
                value=max_width_meters, unit_kind=models.LinearUnitKind.Meters
            )
            assert not res.isNotOk()
            assert res.status == 200
            res.ok()

            config = client.equipment.get_gripper_configuration()
            assert config.data.onrobot_2fg7.width_outer == max_width_meters

    @pytest.mark.gripper("onrobot_2fg7")
    def test_2fg7_movement_advanced_live(
        self,
        client_live: StandardBotsRobot,
    ) -> None:
        """2fg7 movement and force test: live mode"""
        client = client_live

        width_meters = 0.07
        force = 1.0

        with client.connection():
            res = client.equipment.control_gripper(
                models.GripperCommandRequest(
                    kind=models.GripperKindEnum.Onrobot2Fg7,
                    onrobot_2fg7=models.OnRobot2FG7GripperCommandRequest(
                        control_kind=models.OnRobot2FG7ControlKindEnum.Move,
                        target_grip_width=models.LinearUnit(
                            unit_kind=models.LinearUnitKind(
                                models.LinearUnitKind.Meters
                            ),
                            value=float(width_meters),
                        ),
                        grip_direction=models.LinearGripDirectionEnum(
                            models.LinearGripDirectionEnum.Internal
                        ),
                        target_force=models.ForceUnit(
                            unit_kind=models.ForceUnitKind(
                                models.ForceUnitKind.Newtons
                            ),
                            value=float(force),
                        ),
                    ),
                )
            )

            assert not res.isNotOk()
            assert res.status == 200
            res.ok()

            config = client.equipment.get_gripper_configuration()
            assert config.data.onrobot_2fg7.width_outer == width_meters
            assert config.data.onrobot_2fg7.force == force

    @pytest.mark.gripper("onrobot_2fg14")
    def test_2fg14_movement_live(
        self,
        client_live: StandardBotsRobot,
    ) -> None:
        """2fg14 movement test: live mode"""
        client = client_live

        min_width_meters = 0.07
        max_width_meters = 0.1

        with client.connection():
            res = client.equipment.control_gripper(
                models.GripperCommandRequest(
                    kind=models.GripperKindEnum.Onrobot2Fg14,
                    onrobot_2fg14=models.OnRobot2FG14GripperCommandRequest(
                        control_kind=models.OnRobot2FG14ControlKindEnum.Move,
                        target_grip_width=models.LinearUnit(
                            unit_kind=models.LinearUnitKind(
                                models.LinearUnitKind.Meters
                            ),
                            value=min_width_meters,
                        ),
                        grip_direction=models.LinearGripDirectionEnum(
                            models.LinearGripDirectionEnum.Internal
                        ),
                    ),
                )
            )

            assert not res.isNotOk()
            assert res.status == 200
            res.ok()

            config = client.equipment.get_gripper_configuration()
            assert config.data.onrobot_2fg14.width_outer == min_width_meters

            res = client.equipment.control_gripper(
                models.GripperCommandRequest(
                    kind=models.GripperKindEnum.Onrobot2Fg14,
                    onrobot_2fg14=models.OnRobot2FG14GripperCommandRequest(
                        control_kind=models.OnRobot2FG14ControlKindEnum.Move,
                        target_grip_width=models.LinearUnit(
                            unit_kind=models.LinearUnitKind(
                                models.LinearUnitKind.Meters
                            ),
                            value=max_width_meters,
                        ),
                        grip_direction=models.LinearGripDirectionEnum(
                            models.LinearGripDirectionEnum.Internal
                        ),
                    ),
                )
            )

            assert not res.isNotOk()
            assert res.status == 200
            res.ok()

            config = client.equipment.get_gripper_configuration()
            assert config.data.onrobot_2fg14.width_outer == max_width_meters

    @pytest.mark.gripper("onrobot_3fg15")
    def test_3fg15_movement_live(
        self,
        client_live: StandardBotsRobot,
    ) -> None:
        """3fg15 movement test: live mode"""
        client = client_live

        min_diameter_meters = 0.08
        max_diameter_meters = 0.11
        force = 10.0

        with client.connection():
            res = client.equipment.control_gripper(
                models.GripperCommandRequest(
                    kind=models.GripperKindEnum.Onrobot3Fg15,
                    onrobot_3fg15=models.OnRobot3FG15GripperCommandRequest(
                        control_kind=models.OnRobot3FG15ControlKindEnum.Move,
                        target_grip_diameter=models.LinearUnit(
                            unit_kind=models.LinearUnitKind(
                                models.LinearUnitKind.Meters
                            ),
                            value=min_diameter_meters,
                        ),
                        grip_direction=models.LinearGripDirectionEnum(
                            models.LinearGripDirectionEnum.External
                        ),
                        target_force=models.ForceUnit(
                            unit_kind=models.ForceUnitKind(
                                models.ForceUnitKind.Newtons
                            ),
                            value=force,
                        ),
                    ),
                )
            )

            assert not res.isNotOk()
            assert res.status == 200
            res.ok()

            config = client.equipment.get_gripper_configuration()
            assert approx_equal(
                config.data.onrobot_3fg15.diameter, min_diameter_meters, 2
            )

            res = client.equipment.control_gripper(
                models.GripperCommandRequest(
                    kind=models.GripperKindEnum.Onrobot3Fg15,
                    onrobot_3fg15=models.OnRobot3FG15GripperCommandRequest(
                        control_kind=models.OnRobot3FG15ControlKindEnum.Move,
                        target_grip_diameter=models.LinearUnit(
                            unit_kind=models.LinearUnitKind(
                                models.LinearUnitKind.Meters
                            ),
                            value=max_diameter_meters,
                        ),
                        grip_direction=models.LinearGripDirectionEnum(
                            models.LinearGripDirectionEnum.External
                        ),
                        target_force=models.ForceUnit(
                            unit_kind=models.ForceUnitKind(
                                models.ForceUnitKind.Newtons
                            ),
                            value=force,
                        ),
                    ),
                )
            )

            assert not res.isNotOk()
            assert res.status == 200
            res.ok()

            config = client.equipment.get_gripper_configuration()
            assert config.data.onrobot_3fg15.diameter == max_diameter_meters

    @pytest.mark.gripper("dh_ag")
    def test_dh_ag_live(
        self,
        client_live: StandardBotsRobot,
    ) -> None:
        """dh_ag test: live mode"""
        client = client_live

        target_diameter = 0.0
        force = 0.6
        speed = 0.6

        with client.connection():
            res = client.equipment.dh_ag_grip(target_diameter, force, speed)

            assert not res.isNotOk()
            assert res.status == 200
            res.ok()

            config = client.equipment.get_gripper_configuration()
            assert config.data.dh_ag.diameter == target_diameter

    @pytest.mark.gripper("dh_pgc")
    def test_dh_pgc_live(
        self,
        client_live: StandardBotsRobot,
    ) -> None:
        """dh_pgc_grip test: live mode"""
        client = client_live

        target_diameter = 0.0
        target_force = 0.5
        target_speed = 0.5

        with client.connection():
            res = client.equipment.dh_pgc_grip(
                target_diameter, target_force, target_speed
            )

            assert not res.isNotOk()
            assert res.status == 200
            res.ok()

            config = client.equipment.get_gripper_configuration()
            assert config.data.dh_pgc.diameter == target_diameter

    @pytest.mark.gripper("dh_cgi")
    def test_dh_cgi_live(
        self,
        client_live: StandardBotsRobot,
    ) -> None:
        """dh_cgi_grip test: live mode"""
        client = client_live

        target_diameter = 0.0
        target_force = 10.0
        target_speed = 0.5

        with client.connection():
            res = client.equipment.dh_cgi_grip(
                target_diameter, target_force, target_speed
            )

            assert not res.isNotOk()
            assert res.status == 200
            res.ok()

            config = client.equipment.get_gripper_configuration()
            assert config.data.dh_cgi.diameter == target_diameter

    # TODO add schunk_egx tests once implemented control logic


class TestGetEquipmentCustomSensors:
    """Tests: [GET] `/api/v1/equipment/custom/sensors`"""

    @pytest.mark.gripper("custom_sensors")
    def test_basic(self, client_live: StandardBotsRobot) -> None:
        """Basic test"""
        client = client_live

        with client.connection():
            res_raw = client.sensors.get_sensors()
        assert not res_raw.isNotOk()
        res = res_raw.ok()

        assert isinstance(res.sensors, list)
        assert len(res.sensors) > 0

        sensor = res.sensors[0]
        assert sensor.name == "sensor 1"
        assert sensor.kind == "controlBoxIO"
        assert sensor.sensorValue == "low"

    @pytest.mark.gripper("custom_sensors")
    def test_basic_sim(self, client_sim: StandardBotsRobot) -> None:
        """Basic test: sim mode"""
        client = client_sim

        with client.connection():
            res_raw = client.sensors.get_sensors()
        assert not res_raw.isNotOk()
        res = res_raw.ok()

        assert isinstance(res.sensors, list)
        assert len(res.sensors) > 0

        sensor = res.sensors[0]
        assert sensor.name == "sensor 1"
        assert sensor.kind == "controlBoxIO"
        assert sensor.sensorValue == "low"


class TestGetMovementBrakes:
    """Tests: [GET] `/api/v1/movement/brakes`"""

    def test_basic(self, client_live: StandardBotsRobot) -> None:
        """Basic test"""
        client = client_live

        with client.connection():
            res = client.movement.brakes.get_brakes_state()

        assert not res.isNotOk()
        data = res.data
        assert isinstance(data, models.BrakesState)
        assert data.state is not None

    def test_basic_sim(self, client_sim: StandardBotsRobot) -> None:
        """Basic test: sim mode"""
        client = client_sim

        with client.connection():
            res = client.movement.brakes.get_brakes_state()

        assert not res.isNotOk()
        data = res.data
        assert isinstance(data, models.BrakesState)
        assert data.state is not None


class TestPostMovementBrakes:
    """Tests: [POST] `/api/v1/movement/brakes`

    NOTE Relies on "get brake state" API
    """

    def test_brake_live(self, client_live: StandardBotsRobot) -> None:
        """Basic test"""
        client = client_live

        # ######################################
        # Get initial brakes state
        # ######################################
        with client.connection():
            res = client.movement.brakes.get_brakes_state()

        assert not res.isNotOk()
        data = res.data
        assert isinstance(data, models.BrakesState)
        assert data.state is not None
        is_braked_initial = data.state == models.BrakesStateEnum.Engaged

        new_state = (
            models.BrakesStateEnum.Disengaged
            if is_braked_initial
            else models.BrakesStateEnum.Engaged
        )

        body = models.BrakesState(state=new_state)

        with client.connection():
            res = client.movement.brakes.set_brakes_state(body)

        assert not res.isNotOk()
        data = res.data
        assert isinstance(data, models.BrakesState)
        assert data.state == new_state

        # ######################################
        # Confirm new state via other means
        # ######################################
        with client.connection():
            res = client.movement.brakes.get_brakes_state()

        assert not res.isNotOk()
        data = res.data
        assert isinstance(data, models.BrakesState)
        assert data.state == new_state

        # ######################################
        # Set brakes state back to original state
        # ######################################
        final_state = (
            models.BrakesStateEnum.Disengaged
            if not is_braked_initial
            else models.BrakesStateEnum.Engaged
        )
        body = models.BrakesState(state=final_state)

        with client.connection():
            res = client.movement.brakes.set_brakes_state(body)

        assert not res.isNotOk()
        data = res.data
        assert isinstance(data, models.BrakesState)
        assert data.state == final_state

    def test_brake_twice(self, client_live: StandardBotsRobot) -> None:
        """Test (un)braking twice

        Use the `client.movement.brakes.brake()`/`client.movement.brakes.unbrake()` helper methods.
        """
        client = client_live

        # ###################################################
        # Brake
        # ###################################################
        for _ in range(2):
            with client.connection():
                res = client.movement.brakes.brake()

            assert not res.isNotOk()
            data = res.data
            assert isinstance(data, models.BrakesState)
            assert data.state == models.BrakesStateEnum.Engaged

        # ###################################################
        # Now unbrake
        # ###################################################

        for _ in range(2):
            with client.connection():
                res = client.movement.brakes.unbrake()

            assert not res.isNotOk()
            data = res.data
            assert isinstance(data, models.BrakesState)
            assert data.state == models.BrakesStateEnum.Disengaged

    def test_brakes_sim(self, client_sim: StandardBotsRobot) -> None:
        """Basic test: sim mode

        Can observe sim braking/unbraking separate from live robot.
        """
        client = client_sim

        # ######################################
        # Get initial brakes state
        # ######################################
        with client.connection():
            res = client.movement.brakes.get_brakes_state()

        assert not res.isNotOk()
        data = res.data
        assert isinstance(data, models.BrakesState)
        assert data.state is not None
        is_braked_initial = data.state == models.BrakesStateEnum.Engaged

        new_state = (
            models.BrakesStateEnum.Disengaged
            if is_braked_initial
            else models.BrakesStateEnum.Engaged
        )

        body = models.BrakesState(state=new_state)

        with client.connection():
            res = client.movement.brakes.set_brakes_state(body)

        assert not res.isNotOk()
        data = res.data
        assert isinstance(data, models.BrakesState)
        assert data.state == new_state

        # ######################################
        # Confirm new state via other means
        # ######################################
        with client.connection():
            res = client.movement.brakes.get_brakes_state()

        assert not res.isNotOk()
        data = res.data
        assert isinstance(data, models.BrakesState)
        assert data.state == new_state

        # ######################################
        # Set brakes state back to original state
        # ######################################
        final_state = (
            models.BrakesStateEnum.Disengaged
            if not is_braked_initial
            else models.BrakesStateEnum.Engaged
        )
        body = models.BrakesState(state=final_state)

        with client.connection():
            res = client.movement.brakes.set_brakes_state(body)

        assert not res.isNotOk()
        data = res.data
        assert isinstance(data, models.BrakesState)
        assert data.state == final_state


class TestPostMovementBrakesEmergencyStop:
    """Tests: [POST] `/api/v1/movement/brakes/emergency-stop`

    NOTE Rely on working recover.get_status/recover to test this.
    """

    @pytest.mark.parametrize(
        ["n_estops"], [pytest.param(1, id="1 e-stop"), pytest.param(2, id="2 e-stops")]
    )
    def test_basic(self, n_estops: int, client_live: StandardBotsRobot) -> None:
        """Basic test

        n_estops: Triggers e-stops multiple times. Ensure that can run multiple times.

        This test can be flaky at times. Sometimes the status check will return 'Idle' instead of 'EStopTriggered'.
        """
        client = client_live

        # ######################################
        # Ensure not already in error state
        # ######################################
        with client.connection():
            res_status = client.recovery.recover.get_status()

        assert not res_status.isNotOk()
        data = res_status.data
        assert isinstance(data, models.FailureStateResponse)
        assert not data.failed

        # ######################################
        # Now test e-stop operation
        # ######################################

        for _ in range(n_estops):
            body = models.EngageEmergencyStopRequest(reason="To test it out.")

            with client.connection():
                res = client.movement.brakes.engage_emergency_stop(body)

            assert not res.isNotOk()
            assert res.data is None

            # ######################################
            # Ensure status
            # ######################################

            for _ in range(2):
                with client.connection():
                    res_status = client.recovery.recover.get_status()

                assert not res_status.isNotOk()
                data = res_status.data
                assert isinstance(data, models.FailureStateResponse)
                if data.failure is None or data.failure.kind == "Idle":
                    time.sleep(1)  # Appears to take a moment to update at times?
                    continue
                if data.failure.kind == "EStopTriggered":
                    assert data.failed
                    break
                assert data.failure.kind == "EStopTriggered"

            # ######################################
            # Recover from e-stop
            # ######################################

            with client.connection():
                res_status = client.recovery.recover.recover()

    def test_estop_sim(self, client_sim: StandardBotsRobot) -> None:
        """Basic test: sim mode

        Sim does not e-stop the bot.
        """
        client = client_sim
        body = models.EngageEmergencyStopRequest(reason="To test it out.")

        with client.connection():
            res = client.movement.brakes.engage_emergency_stop(body)

        assert not res.isNotOk()
        assert res.data is None

        # ######################################
        # Sim does not e-stop the bot. So no recovery state.
        # ######################################

        with client.connection():
            res_status = client.recovery.recover.get_status()

        assert not res_status.isNotOk()
        data = res_status.data
        assert isinstance(data, models.FailureStateResponse)
        assert not data.failed


class TestGetMovementPositionArm:
    """Tests: [GET] `/api/v1/movement/position/arm`"""

    def test_basic(self, client_live: StandardBotsRobot) -> None:
        """Basic test"""
        client = client_live

        res = client.movement.position.get_arm_position()

        assert not res.isNotOk()
        assert res.status == 200

        assert isinstance(res.data, models.CombinedArmPosition)
        assert res.data.joint_rotations is not None
        assert isinstance(res.data.tooltip_position, models.PositionAndOrientation)


class TestPostMovementPositionArm:
    """Tests: [POST] `/api/v1/movement/position/arm`"""

    def test_arm_position_when_robot_not_idle(
        self, routine_running_live_fixt: None, client_live: StandardBotsRobot
    ) -> None:
        """Test arm position when robot is not in Idle state"""
        client = client_live

        brakes_res = client.movement.brakes.get_brakes_state()
        # make sure to unbrake robot
        if brakes_res.data.state == models.BrakesStateEnum.Engaged:
            res = client.movement.brakes.set_brakes_state(
                body=models.BrakesState(state=models.BrakesStateEnum.Disengaged)
            )

        target_position = (0.01, 0.01, 0.01, 0.01, 0.01, 0.01)
        target_position_body = models.ArmPositionUpdateRequest(
            kind=models.ArmPositionUpdateRequestKindEnum.JointRotation,
            joint_rotation=models.ArmJointRotations(joints=target_position),
        )
        res = client.movement.position.set_arm_position(body=target_position_body)
        assert res.isNotOk()
        assert res.status == 503
        assert res.data.error == models.ErrorEnum.RobotNotIdle

    def test_robot_arm_position_with_brakes(
        self, client_live: StandardBotsRobot
    ) -> None:
        """Test arm position when robot with brakes"""
        client = client_live

        with client.connection():
            brakes_res = client.movement.brakes.get_brakes_state()

            # engage brakes to test the flow
            if brakes_res.data.state != models.BrakesStateEnum.Engaged:
                res = client.movement.brakes.set_brakes_state(
                    body=models.BrakesState(state=models.BrakesStateEnum.Engaged)
                )

            # expecting error here
            target_position = (0.01, 0.01, 0.01, 0.01, 0.01, 0.01)
            target_position_body = models.ArmPositionUpdateRequest(
                kind=models.ArmPositionUpdateRequestKindEnum.JointRotation,
                joint_rotation=models.ArmJointRotations(joints=target_position),
            )
            res = client.movement.position.set_arm_position(body=target_position_body)
            assert res.isNotOk()
            assert res.status == 500
            assert res.data.error == models.ErrorEnum.BrakesMustBeDisengaged

            # unbrake robot
            res = client.movement.brakes.set_brakes_state(
                models.BrakesState(state=models.BrakesStateEnum.Disengaged)
            )

    def test_robot_movement_to_unreachable_position(
        self, client_live: StandardBotsRobot
    ) -> None:
        """Test move robot movement to unreachable position"""
        client = client_live

        with client.connection():
            brakes_res = client.movement.brakes.get_brakes_state()
            # make sure to unbrake robot
            if brakes_res.data.state == models.BrakesStateEnum.Engaged:
                res = client.movement.brakes.set_brakes_state(
                    body=models.BrakesState(state=models.BrakesStateEnum.Disengaged)
                )
            # expecting error here
            target_position = (100, 100, 100, 100, 100, 100)
            target_position_body = models.ArmPositionUpdateRequest(
                kind=models.ArmPositionUpdateRequestKindEnum.JointRotation,
                joint_rotation=models.ArmJointRotations(joints=target_position),
            )
            res = client.movement.position.set_arm_position(body=target_position_body)
            assert res.data.kind == models.ArmPositionUpdateKindEnum.Failure
            assert (
                res.data.failure.kind
                == models.ArmPositionUpdateFailureEventKind.MotionFailedUnknownReason
            )

            # recover from failed position update
            res_recover = client.recovery.recover.recover()
            assert not res_recover.isNotOk()

    def test_invalid_joint_and_tooltip_request(
        self, client_live: StandardBotsRobot
    ) -> None:
        """Test joint movement without joint_rotation"""
        client = client_live

        with client.connection():
            brakes_res = client.movement.brakes.get_brakes_state()
            # make sure to unbrake robot
            if brakes_res.data.state == models.BrakesStateEnum.Engaged:
                res = client.movement.brakes.set_brakes_state(
                    body=models.BrakesState(state=models.BrakesStateEnum.Disengaged)
                )
            # expecting error here
            target_position_body = models.ArmPositionUpdateRequest(
                kind=models.ArmPositionUpdateRequestKindEnum.JointRotation,
            )
            res = client.movement.position.set_arm_position(body=target_position_body)
            assert res.isNotOk()
            assert res.status == 400
            assert res.data.error == models.ErrorEnum.RequestFailedValidation

            target_position_body = models.ArmPositionUpdateRequest(
                kind=models.ArmPositionUpdateRequestKindEnum.TooltipPosition,
            )
            res = client.movement.position.set_arm_position(body=target_position_body)
            assert res.isNotOk()
            assert res.status == 400
            assert res.data.error == models.ErrorEnum.RequestFailedValidation

    def test_invalid_local_accuracy_calibration(
        self, client_live: StandardBotsRobot
    ) -> None:
        """Test invalid local accuracy calibration"""
        client = client_live
        with client.connection():
            brakes_res = client.movement.brakes.get_brakes_state()
            # make sure to unbrake robot
            if brakes_res.data.state == models.BrakesStateEnum.Engaged:
                res = client.movement.brakes.set_brakes_state(
                    body=models.BrakesState(state=models.BrakesStateEnum.Disengaged)
                )
            quartenion = models.Quaternion(
                x=9.135034599492311e-06,
                y=9.136842411048252e-06,
                z=0.7071444639790607,
                w=0.70706909626771,
            )
            target_tooltip_position = models.Position(x=0.1, y=0.4, z=1.3)
            pose_body = models.ArmPositionUpdateRequest(
                kind=models.ArmPositionUpdateRequestKindEnum.TooltipPosition,
                tooltip_position=models.PositionAndOrientation(
                    position=target_tooltip_position,
                    local_accuracy_calibration="invalid",
                    orientation=models.Orientation(
                        kind=models.OrientationKindEnum.Quaternion,
                        quaternion=quartenion,
                    ),
                ),
                movement_kind=models.MovementKindEnum.Line,
            )
            res = client.movement.position.set_arm_position(body=pose_body)
            assert res.isNotOk()
            assert res.status == 400
            assert res.data.error == models.ErrorEnum.InvalidSpaceSpecified

    def test_joint_rotation_to_target_and_back(
        self, client_live: StandardBotsRobot
    ) -> None:
        """Test joint_rotation to target and back"""
        client = client_live
        with client.connection():
            brakes_res = client.movement.brakes.get_brakes_state()
            # make sure to unbrake robot
            if brakes_res.data.state == models.BrakesStateEnum.Engaged:
                res = client.movement.brakes.set_brakes_state(
                    body=models.BrakesState(state=models.BrakesStateEnum.Disengaged)
                )

            initial_position = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
            target_position = (0.01, 0.01, 0.01, 0.01, 0.01, 0.01)
            initial_position_body = models.ArmPositionUpdateRequest(
                kind=models.ArmPositionUpdateRequestKindEnum.JointRotation,
                joint_rotation=models.ArmJointRotations(joints=initial_position),
                speed_profile=models.SpeedProfile(
                    max_joint_speeds=(0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
                ),
            )
            target_position_body = models.ArmPositionUpdateRequest(
                kind=models.ArmPositionUpdateRequestKindEnum.JointRotation,
                joint_rotation=models.ArmJointRotations(joints=target_position),
                speed_profile=models.SpeedProfile(max_joint_speeds=(1, 1, 1, 1, 1, 1)),
            )

            #  move robot to target position
            res = client.movement.position.set_arm_position(body=target_position_body)
            assert not res.isNotOk()
            assert res.status == 200
            assert res.data.kind == models.ArmPositionUpdateKindEnum.Success

            target_position_res = client.movement.position.get_arm_position()
            target_joint_pose_rounded = tuple(
                round(val, 2) for val in target_position_res.data.joint_rotations
            )

            # check if robot successfully moved to target pose
            assert target_joint_pose_rounded == target_position

            # move robot back to initial position
            res = client.movement.position.set_arm_position(body=initial_position_body)
            assert not res.isNotOk()
            assert res.status == 200
            assert res.data.kind == models.ArmPositionUpdateKindEnum.Success

            initial_position_res = client.movement.position.get_arm_position()

            initial_joint_pose_rounded = tuple(
                round(val, 2) for val in initial_position_res.data.joint_rotations
            )
            # check if pose correctly moved to initial pose
            assert initial_joint_pose_rounded == initial_position

    def test_joint_rotations_to_target_and_back(
        self, client_live: StandardBotsRobot
    ) -> None:
        """Test joint_rotations to target and back"""
        client = client_live
        with client.connection():
            brakes_res = client.movement.brakes.get_brakes_state()
            # make sure to unbrake robot
            if brakes_res.data.state == models.BrakesStateEnum.Engaged:
                res = client.movement.brakes.set_brakes_state(
                    body=models.BrakesState(state=models.BrakesStateEnum.Disengaged)
                )
            initial_position = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
            pose_res = client.movement.position.get_arm_position()
            initial_joint_pose_rounded = tuple(
                round(val, 2) for val in pose_res.data.joint_rotations
            )

            #  if robot is not in initial position, move it to initial position
            if initial_joint_pose_rounded != initial_position:
                pose_body = models.ArmPositionUpdateRequest(
                    kind=models.ArmPositionUpdateRequestKindEnum.JointRotation,
                    joint_rotation=models.ArmJointRotations(joints=initial_position),
                )

                res = client.movement.position.set_arm_position(body=pose_body)
                assert not res.isNotOk()
                assert res.status == 200
                assert res.data.kind == models.ArmPositionUpdateKindEnum.Success

            # move every joint by 0.01 radian
            target_position = (0.01, 0.01, 0.01, 0.01, 0.01, 0.01)
            pose_body = models.ArmPositionUpdateRequest(
                kind=models.ArmPositionUpdateRequestKindEnum.JointRotations,
                joint_rotations=[
                    models.ArmJointRotations(joints=target_position),
                    models.ArmJointRotations(joints=initial_position),
                ],
            )

            res = client.movement.position.set_arm_position(body=pose_body)
            assert not res.isNotOk()
            assert res.status == 200
            assert res.data.kind == models.ArmPositionUpdateKindEnum.Success

            pose_res = client.movement.position.get_arm_position()
            joint_pose_rounded = tuple(
                round(val, 2) for val in pose_res.data.joint_rotations
            )

            # check if robot successfully moved into initial pose
            assert joint_pose_rounded == initial_position

    def test_tooltip_position_to_target_and_back(
        self, client_live: StandardBotsRobot
    ) -> None:
        """Test tooltip_position to target and back"""
        client = client_live
        with client.connection():
            brakes_res = client.movement.brakes.get_brakes_state()
            # make sure to unbrake robot
            if brakes_res.data.state == models.BrakesStateEnum.Engaged:
                res = client.movement.brakes.set_brakes_state(
                    body=models.BrakesState(state=models.BrakesStateEnum.Disengaged)
                )
            pose_res = client.movement.position.get_arm_position()

            quartenion = models.Quaternion(
                x=0.0,
                y=0.0,
                z=0.707,
                w=0.707,
            )
            initial_tooltip_position = models.Position(x=0.0, y=0.3687, z=1.3618)
            target_tooltip_position = models.Position(x=0.1, y=0.4, z=1.3)
            pose_body = models.ArmPositionUpdateRequest(
                kind=models.ArmPositionUpdateRequestKindEnum.TooltipPosition,
                tooltip_position=models.PositionAndOrientation(
                    position=target_tooltip_position,
                    orientation=models.Orientation(
                        kind=models.OrientationKindEnum.Quaternion,
                        quaternion=quartenion,
                    ),
                ),
            )
            res = client.movement.position.set_arm_position(body=pose_body)

            assert not res.isNotOk()
            assert res.status == 200
            assert res.data.kind == models.ArmPositionUpdateKindEnum.Success

            # check if robot moved into initial pose
            pose_res = client.movement.position.get_arm_position()
            target_tooltip = pose_res.data.tooltip_position.position

            assert approx_equal(target_tooltip.x, target_tooltip_position.x, 2)
            assert approx_equal(target_tooltip.y, target_tooltip_position.y, 2)
            assert approx_equal(target_tooltip.z, target_tooltip_position.z, 2)

            pose_body = models.ArmPositionUpdateRequest(
                kind=models.ArmPositionUpdateRequestKindEnum.TooltipPosition,
                tooltip_position=models.PositionAndOrientation(
                    position=initial_tooltip_position,
                    orientation=models.Orientation(
                        kind=models.OrientationKindEnum.Quaternion,
                        quaternion=quartenion,
                    ),
                ),
            )
            res = client.movement.position.set_arm_position(body=pose_body)
            assert not res.isNotOk()
            assert res.status == 200
            assert res.data.kind == models.ArmPositionUpdateKindEnum.Success

            # check if robot moved into initial pose
            pose_res = client.movement.position.get_arm_position()
            tooltip_position = pose_res.data.tooltip_position.position

            assert approx_equal(tooltip_position.x, initial_tooltip_position.x, 2)
            assert approx_equal(tooltip_position.y, initial_tooltip_position.y, 2)
            assert approx_equal(tooltip_position.z, initial_tooltip_position.z, 2)

    def test_tooltip_positions_to_target_and_back(
        self, client_live: StandardBotsRobot
    ) -> None:
        """Test tooltip_positions to target and back"""
        client = client_live
        with client.connection():
            brakes_res = client.movement.brakes.get_brakes_state()
            # make sure to unbrake robot
            if brakes_res.data.state == models.BrakesStateEnum.Engaged:
                res = client.movement.brakes.set_brakes_state(
                    body=models.BrakesState(state=models.BrakesStateEnum.Disengaged)
                )
            initial_tooltip_position = models.Position(x=0.1, y=0.35, z=1.18)
            target_tooltip_position = models.Position(x=0.1, y=0.4, z=1.3)
            quartenion = models.Quaternion(
                x=0.0,
                y=0.0,
                z=0.707,
                w=0.707,
            )
            pose_res = client.movement.position.get_arm_position()
            tooltip_position = pose_res.data.tooltip_position.position

            if not (
                approx_equal(tooltip_position.x, initial_tooltip_position.x)
                and approx_equal(tooltip_position.y, initial_tooltip_position.y)
                and approx_equal(tooltip_position.z, initial_tooltip_position.z)
            ):
                pose_body = models.ArmPositionUpdateRequest(
                    kind=models.ArmPositionUpdateRequestKindEnum.TooltipPosition,
                    tooltip_position=models.PositionAndOrientation(
                        position=initial_tooltip_position,
                        orientation=models.Orientation(
                            kind=models.OrientationKindEnum.Quaternion,
                            quaternion=quartenion,
                        ),
                    ),
                )
                res = client.movement.position.set_arm_position(body=pose_body)
                assert not res.isNotOk()
                assert res.status == 200
                assert res.data.kind == models.ArmPositionUpdateKindEnum.Success

            pose_body = models.ArmPositionUpdateRequest(
                kind=models.ArmPositionUpdateRequestKindEnum.TooltipPositions,
                tooltip_positions=[
                    models.PositionAndOrientation(
                        position=target_tooltip_position,
                        orientation=models.Orientation(
                            kind=models.OrientationKindEnum.Quaternion,
                            quaternion=quartenion,
                        ),
                    ),
                    models.PositionAndOrientation(
                        position=initial_tooltip_position,
                        orientation=models.Orientation(
                            kind=models.OrientationKindEnum.Quaternion,
                            quaternion=quartenion,
                        ),
                    ),
                ],
                movement_kind=models.MovementKindEnum.Joint,
            )
            res = client.movement.position.set_arm_position(body=pose_body)

            assert not res.isNotOk()
            assert res.status == 200
            assert res.data.kind == models.ArmPositionUpdateKindEnum.Success

            # check if robot moved successfully moved to initial position
            pose_res = client.movement.position.get_arm_position()
            tooltip_position = pose_res.data.tooltip_position.position

            assert approx_equal(tooltip_position.x, initial_tooltip_position.x)
            assert approx_equal(tooltip_position.y, initial_tooltip_position.y)
            assert approx_equal(tooltip_position.z, initial_tooltip_position.z)


class TestGetMovementROSState:
    """Tests: [GET] `/api/v1/movement/ros/state`"""

    def test_basic(self, client_live: StandardBotsRobot) -> None:
        client = client_live

        res = client.ros.status.get_ros_control_state()

        assert not res.isNotOk()
        assert isinstance(res.data, models.ROSControlStateResponse)
        assert isinstance(res.data.state, models.ROSControlStateEnum)


class TestPostMovementROSState:
    """Tests: [POST] `/api/v1/movement/ros/state`"""

    def test_basic(
        self, unbrake_robot_fixt: None, client_live: StandardBotsRobot
    ) -> None:
        """Basic test"""
        client = client_live

        res = client.ros.status.get_ros_control_state()
        initial_state = res.data.state
        action = (
            models.ROSControlStateEnum.Enabled
            if initial_state == models.ROSControlStateEnum.Disabled
            else models.ROSControlStateEnum.Disabled
        )
        body = models.ROSControlUpdateRequest(action=action)

        final_res = client.ros.control.update_ros_control_state(body=body)

        updated_state = client.ros.status.get_ros_control_state()

        assert not final_res.isNotOk()
        assert final_res.data.state == updated_state.data.state

        # if initial_state == models.ROSControlStateEnum.Disabled:
        client.ros.control.update_ros_control_state(
            models.ROSControlUpdateRequest(action=initial_state)
        )


class TestPostRecoveryRecover:
    """Tests: [POST] `/api/v1/recovery/recover`"""

    def test_not_need_to_recover(
        self, routine_running_live_fixt: None, client_live: StandardBotsRobot
    ) -> None:
        """Bot not in need of recovery/not in fault"""
        client = client_live

        with client.connection():
            res_status = client.recovery.recover.get_status()
            assert not res_status.isNotOk()
            data = res_status.data
            assert isinstance(data, models.FailureStateResponse)

            # Check if robot is failed, if yes then recover
            if data.failed:
                res_recover = client.recovery.recover.recover()
                assert not res_recover.isNotOk()
                recover_data = res_recover.data
                assert not recover_data.failed

            # check response when bot does not need recovery
            res_recover = client.recovery.recover.recover()
            assert not res_recover.isNotOk()
            recover_data = res_recover.data
            assert not recover_data.failed

    def test_recoverable_flow_basic(
        self, routine_running_live_fixt: None, client_live: StandardBotsRobot
    ) -> None:
        """Basic test: Ensures recovery works when robot is in a fault state."""
        client = client_live

        time.sleep(3)  # wait for routine to start

        with client.connection():
            res_status = client.recovery.recover.get_status()
            assert not res_status.isNotOk()
            data = res_status.data
            assert isinstance(data, models.FailureStateResponse)

            # Check if robot is already in a failed state, if not trigger user fault
            if not data.failed:
                body = models.TriggerFaultRequest(
                    message="Make user fault to test recovery", isRecoverable=True
                )

                res = client.faults.user_faults.trigger_user_fault(body)
                assert res.status == 200
                assert not res.isNotOk()

                res_status_before = client.recovery.recover.get_status()
                assert not res_status_before.isNotOk()
                data_after = res_status_before.data
                assert isinstance(data_after, models.FailureStateResponse)
                assert data_after.failed

            res_recover = client.recovery.recover.recover()
            assert not res_recover.isNotOk()
            recover_data = res_recover.data
            assert not recover_data.failed

            # Make sure data returned from recovery call is same as from get status call
            res_status_after = client.recovery.recover.get_status()
            assert not res_status_after.isNotOk()
            status_data_after = res_status_after.data
            assert isinstance(status_data_after, models.FailureStateResponse)
            assert status_data_after.failed == recover_data.failed
            assert status_data_after.status == recover_data.status

    # need to figure out how to run non recoverable tests
    @pytest.mark.skip(reason="Aborts entire routine")
    def test_not_recoverable_flow_basic(self, client_live: StandardBotsRobot) -> None:
        """Basic test: Ensures recovery works when robot is in a fault state."""
        client = client_live

        with client.connection():
            res_status = client.recovery.recover.get_status()
            assert not res_status.isNotOk()
            data = res_status.data
            assert isinstance(data, models.FailureStateResponse)

            # Check if robot is already in a failed state, if not trigger user fault
            if not data.failed:
                body = models.TriggerFaultRequest(
                    message="Make user fault to test recovery", isRecoverable=False
                )

                res = client.faults.user_faults.trigger_user_fault(body)
                assert res.status == 200
                assert not res.isNotOk()

                res_status_before = client.recovery.recover.get_status()
                assert not res_status_before.isNotOk()
                data_after = res_status_before.data
                assert isinstance(data_after, models.FailureStateResponse)
                assert data_after.failed

                res_recover = client.recovery.recover.recover()
                assert not res_recover.isNotOk()
                recover_data = res_recover.data
                assert recover_data.failed

        # TODO: Add following tests
        # 1. Fault that is recoverable but not trigger-fault (these are handled separate)


class TestGetRecoveryStatus:
    """Tests: [GET] `/api/v1/recovery/status`"""

    def test_basic(self, client_live: StandardBotsRobot) -> None:
        """Basic test"""
        client = client_live

        with client.connection():
            res = client.recovery.recover.get_status()

        assert not res.isNotOk()
        data = res.data
        assert isinstance(data, models.FailureStateResponse)
        assert data.failed in [True, False]
        assert isinstance(data.status, models.RobotStatusEnum)

        # TODO: Add following tests
        # 1. Non-trigger fault failure
        # 2. Trigger fault failure (different kind of failure under the hood)


class TestGetCameraStreamRGB:
    """Tests: [GET] `/api/v1/camera/stream/rgb`"""

    def test_camera_stream_rgb_camera_disconnected(
        self, client_live: StandardBotsRobot
    ) -> None:
        """Test case when camera is disconnected"""
        client = client_live

        res = client.camera.data.get_camera_stream()

        assert res.isNotOk()
        assert res.status == 503

    @pytest.mark.camera_connected
    def test_basic(self, client_live: StandardBotsRobot) -> None:
        """Basic test to get camera steam RGB"""
        client = client_live
        res = client.camera.data.get_camera_stream()

        assert not res.isNotOk()
        assert res.status == 200

        MAX_ITER = 1000
        MAX_FRAMES = 3

        try:
            res.ok()

            n_frames = 0
            buffer = b""
            for i, chunk in enumerate(res.response.stream(1024)):
                buffer += chunk
                # Search for the start (0xffd8) and end (0xffd9) of the JPEG frame
                a = buffer.find(b"\xff\xd8")
                b = buffer.find(b"\xff\xd9")
                if a != -1 and b != -1:
                    n_frames += 1

                if i > MAX_ITER or n_frames + 1 > MAX_FRAMES:
                    break
        finally:
            # Always close the connection
            res.response.release_conn()
            assert n_frames > 0


class TestPostCameraSettings:
    """Tests: [POST] `/api/v1/camera/settings`"""

    def test_post_camera_settings_camera_disconnected(
        self, client_live: StandardBotsRobot
    ) -> None:
        """Test case when camera is disconnected"""
        client = client_live
        camera_settings = models.CameraSettings(
            brightness=10,
            contrast=10,
            exposure=300,
            sharpness=40,
            hue=10,
            whiteBalance=4500,
            autoWhiteBalance=True,
        )
        res = client.camera.settings.set_camera_settings(camera_settings)

        assert res.isNotOk()
        assert res.status == 503

    @pytest.mark.camera_connected
    def test_post_camera_settings(self, client_live: StandardBotsRobot) -> None:
        """Basic test to update settings"""
        client = client_live
        camera_settings = models.CameraSettings(
            brightness=10,
            contrast=10,
            exposure=300,
            sharpness=40,
            hue=10,
            whiteBalance=4500,
            autoWhiteBalance=True,
        )
        res = client.camera.settings.set_camera_settings(camera_settings)

        assert not res.isNotOk()
        assert res.status == 200


class TestGetCameraFrameRGB:
    """Tests: [GET] `/api/v1/camera/frame/rgb`"""

    def test_strem_rgb_camera_disconnected(
        self, client_live: StandardBotsRobot
    ) -> None:
        """Test case when camera is disconnected"""
        body = models.CameraFrameRequest(
            camera_settings=models.CameraSettings(
                brightness=0,
                contrast=50,
                exposure=350,
                sharpness=50,
                hue=0,
                whiteBalance=4600,
                autoWhiteBalance=True,
            )
        )

        client = client_live
        res = client.camera.data.get_color_frame(body)
        assert res.isNotOk()
        assert res.status == 503

    @pytest.mark.camera_connected
    def test_get_color_frame_invalid_payload(
        self, client_live: StandardBotsRobot
    ) -> None:
        """Test get color frame invalid payload"""
        client = client_live
        body = models.CameraFrameRequest()

        res = client.camera.data.get_color_frame(body)
        assert res.isNotOk()
        assert res.status == 400
        assert res.data.error == models.ErrorEnum.RequestFailedValidation

    @pytest.mark.camera_connected
    def test_get_color_frame(self, client_live: StandardBotsRobot) -> None:
        """Test get color frame"""
        client = client_live
        body = models.CameraFrameRequest(
            camera_settings=models.CameraSettings(
                brightness=0,
                contrast=50,
                exposure=350,
                sharpness=50,
                hue=0,
                whiteBalance=4600,
                autoWhiteBalance=True,
            )
        )

        res = client.camera.data.get_color_frame(body)
        assert not res.isNotOk()
        assert res.status == 200

        raw_data = res.response.data

        base64_data = raw_data.decode().split(",")[1]

        assert isinstance(base64_data, str)


class TestGetCameraIntrinsicsRGB:
    """Tests: [GET] `/api/v1/camera/intrinsics/rgb`"""

    def test_get_camera_intrinsics_camera_disconnected(
        self, client_live: StandardBotsRobot
    ) -> None:
        """Test case when camera is disconnected"""

        client = client_live
        res = client.camera.data.get_camera_intrinsics_color()
        assert res.isNotOk()
        assert res.status == 503

    @pytest.mark.camera_connected
    def test_get_camera_intrinsics(self, client_live: StandardBotsRobot) -> None:
        """Test to get camera intrinsics"""

        client = client_live
        res = client.camera.data.get_camera_intrinsics_color()
        assert not res.isNotOk()
        assert res.status == 200
        assert isinstance(res.data, models.CameraIntrinsics)

    # TODO might need to add tests for not found camera intrinsics


class TestGetCameraStatus:
    """Tests: [GET] `/api/v1/camera/status`"""

    def test_get_camera_status_camera_disconnected(
        self, client_live: StandardBotsRobot
    ) -> None:
        """Test case when camera is disconnected"""

        client = client_live
        res = client.camera.status.get_camera_status()
        assert not res.isNotOk()
        assert res.status == 200
        assert isinstance(res.data, models.CameraStatus)
        assert not res.data.connected

    @pytest.mark.camera_connected
    def test_get_camera_status(self, client_live: StandardBotsRobot) -> None:
        """Test to get camera status"""

        client = client_live
        res = client.camera.status.get_camera_status()
        assert not res.isNotOk()
        assert res.status == 200
        assert isinstance(res.data, models.CameraStatus)
        assert res.data.connected
        assert res.data.message is not None


class TestGetConnectedCameras:
    """Tests: [GET] `/api/v1/cameras/connected`"""

    @pytest.mark.camera_connected
    def test_get_connected_cameras(self, client_live: StandardBotsRobot) -> None:
        """Test case when camera is disconnected"""

        client = client_live
        res = client.camera.bot.get_connected_cameras()
        assert res.status == 200
        assert isinstance(res.data, models.CameraDeviceList)


class TestGetRoutineEditorRoutines:
    """Tests: [GET] `/api/v1/routine-editor/routines`"""

    def test_basic(self, client_live: StandardBotsRobot) -> None:
        """Basic test"""
        client = client_live
        limit = 10
        offset = 0
        with client.connection():
            res = client.routine_editor.routines.list(limit=limit, offset=offset)

        assert not res.isNotOk()
        data = res.ok()

        assert isinstance(data, models.RoutinesPaginatedResponse)
        assert len(data.items) <= limit
        assert data.pagination.total == len(data.items)
        assert data.pagination.limit == limit
        assert data.pagination.offset == offset

    def test_pagination(self, client_live: StandardBotsRobot) -> None:
        """Pagination test"""
        client = client_live
        limit = 10
        offset = 0
        with client.connection():
            res = client.routine_editor.routines.list(limit=limit, offset=offset)

        assert not res.isNotOk()
        data = res.ok()

        assert isinstance(data, models.RoutinesPaginatedResponse)
        assert len(data.items) > 2, "Expected >2 routines (necessary for other tests)"

        # #################################
        # Lower limit
        # #################################
        limit = len(data.items) - 2
        offset = 0
        with client.connection():
            res = client.routine_editor.routines.list(limit=limit, offset=offset)

        assert not res.isNotOk()
        data = res.ok()
        assert isinstance(data, models.RoutinesPaginatedResponse)
        assert data.pagination.total == len(data.items)
        assert len(data.items) <= limit
        assert data.pagination.limit == limit
        assert data.pagination.offset == offset

        # #################################
        # Higher offset
        # #################################
        limit = 10
        offset = 1
        with client.connection():
            res = client.routine_editor.routines.list(limit=limit, offset=offset)

        assert not res.isNotOk()
        data2 = res.ok()
        assert data2.pagination.total == len(data2.items)
        assert len(data2.items) <= limit
        assert data2.pagination.limit == limit
        assert data2.pagination.offset == offset
        assert data.items[0].id not in set(r.id for r in data2.items), (
            "Offset not working"
        )

    @pytest.mark.parametrize(
        ["limit"],
        [
            (0,),
            (-1,),
        ],
    )
    def test_bad_limit(self, limit: int, client_live: StandardBotsRobot) -> None:
        """Bad limit test"""
        client = client_live
        offset = 0
        with client.connection():
            res_raw = client.routine_editor.routines.list(limit=limit, offset=offset)

        assert res_raw.isNotOk()
        assert res_raw.status == 400
        assert isinstance(res_raw.data, models.ErrorResponse)
        assert res_raw.data.error == models.ErrorEnum.InvalidParameters
        assert res_raw.data.message == "Limit must be greater than 0."

    @pytest.mark.parametrize(
        ["offset"],
        [
            (-100,),
            (-1,),
        ],
    )
    def test_bad_offset(self, offset: int, client_live: StandardBotsRobot) -> None:
        """Bad limit test"""
        client = client_live
        limit = 10
        with client.connection():
            res_raw = client.routine_editor.routines.list(limit=limit, offset=offset)

        assert res_raw.isNotOk()
        assert res_raw.status == 400
        assert isinstance(res_raw.data, models.ErrorResponse)
        assert res_raw.data.error == models.ErrorEnum.InvalidParameters
        assert res_raw.data.message == "Offset must be greater than or equal to 0."


class TestGetRoutineEditorRoutineById:
    """Tests: [GET] `/api/v1/routine-editor/routines/:routineId`"""

    def test_basic(
        self, client_live: StandardBotsRobot, routine_sample: models.Routine
    ) -> None:
        """Basic test"""
        client = client_live
        routine_id = routine_sample.id
        with client.connection():
            res_raw = client.routine_editor.routines.load(routine_id=routine_id)

        assert not res_raw.isNotOk()
        assert res_raw.status == 200
        data = res_raw.ok()
        assert isinstance(data, models.Routine)
        assert data.id == routine_id
        assert data.name == routine_sample.name

        assert len(data.environment_variables) > 0
        assert any(
            ev.name == "my_local_variable" for ev in data.environment_variables
        ), "Failed to find expected environment variable"

    def test_invalid_id(self, client_live: StandardBotsRobot) -> None:
        """Invalid ID returns 404"""
        client = client_live
        routine_id = "invalid"
        with client.connection():
            res_raw = client.routine_editor.routines.load(routine_id=routine_id)

        assert res_raw.isNotOk()
        assert res_raw.status == 404
        assert isinstance(res_raw.data, models.ErrorResponse)
        assert res_raw.data.error == models.ErrorEnum.NotFound


class TestGetRoutineEditorRoutineSpaces:
    """Tests: [GET] `/api/v1/routine-editor/routines/:routineId/spaces`"""

    def test_basic(
        self, client_live: StandardBotsRobot, routine_sample_id: str
    ) -> None:
        """Basic test: No globals"""
        client = client_live
        exclude_global_spaces = True

        with client.connection():
            res = client.routine_editor.routines.list_spaces(
                routine_id=routine_sample_id,
                exclude_global_spaces=exclude_global_spaces,
            )

        assert not res.isNotOk()
        data = res.data
        assert isinstance(data, models.SpacesPaginatedResponse)
        assert len(data.items) > 0

        # Routine should have good representation of space kinds: validate (de)serialization
        assert set(s.kind for s in data.items) == {
            "freeformPositionList",
            "plane",
            "singlePosition",
            "gridPositionList",
        }
        assert not any(True for s in data.items if s.is_global), "No globals expected"

    def test_include_globals(
        self, client_live: StandardBotsRobot, routine_sample_id: str
    ) -> None:
        """Include global spaces"""
        client = client_live
        exclude_global_spaces = False

        with client.connection():
            res = client.routine_editor.routines.list_spaces(
                routine_id=routine_sample_id,
                exclude_global_spaces=exclude_global_spaces,
            )

        assert not res.isNotOk()
        data = res.data
        assert isinstance(data, models.SpacesPaginatedResponse)
        assert len(data.items) > 0

        assert any(True for s in data.items if s.is_global), (
            "Globals not found but were expected"
        )
        assert any(True for s in data.items if not s.is_global), "No non-globals found"

    def test_bad_routine_id(self, client_live: StandardBotsRobot) -> None:
        """Bad routine ID"""
        client = client_live
        routine_id = "invalid"
        exclude_global_spaces = True

        with client.connection():
            res = client.routine_editor.routines.list_spaces(
                routine_id=routine_id,
                exclude_global_spaces=exclude_global_spaces,
            )

        assert res.isNotOk()
        assert res.status == 404
        assert isinstance(res.data, models.ErrorResponse)
        assert res.data.error == models.ErrorEnum.NotFound


class TestGetRoutineEditorRoutineStepVariables:
    """Tests: [GET] `/api/v1/routine-editor/routines/:routineId/step-variables`

    NOTE Tested best via code blocks.
    """

    @pytest.mark.parametrize(["step_id_map"], [(True,), (False,)])
    def test_routine_running(
        self,
        step_id_map: bool,
        routine_running_live_fixt: None,
        client_live: StandardBotsRobot,
        routine_sample_id: str,
    ) -> None:
        """Routine loaded should generate state.

        NOTE Only runs when routine is running
        """
        client = client_live
        routine_id = routine_sample_id

        with client.connection():
            res = client.routine_editor.routines.get_step_variables(
                routine_id=routine_id,
                step_id_map=step_id_map,
            )

        assert not res.isNotOk()
        data = res.data
        assert isinstance(data, models.RoutineStepVariablesResponse)

        assert data.variables is not None
        assert isinstance(data.variables, dict)
        assert len(data.variables) > 0

        if step_id_map:
            assert data.step_id_map is not None
            assert isinstance(data.step_id_map, dict)
            assert len(data.step_id_map) > 0
        else:
            assert data.step_id_map is None

    def test_routine_not_running(
        self,
        client_live: StandardBotsRobot,
        routine_sample_id: str,
    ) -> None:
        """400 when not running"""
        client = client_live
        step_id_map = True  # Does not matter here.

        with client.connection():
            res = client.routine_editor.routines.get_step_variables(
                routine_id=routine_sample_id,
                step_id_map=step_id_map,
            )

        assert res.isNotOk()
        data = res.data
        assert isinstance(data, models.ErrorResponse)
        assert res.status == 400
        assert res.data.error == models.ErrorEnum.RoutineMustBeRunning


class TestGetRoutineEditorRoutineState:
    """Tests: [GET] `/api/v1/routine-editor/routines/:routineId/state`"""

    def test_routine_running(
        self,
        routine_running_live_fixt: None,
        client_live: StandardBotsRobot,
        routine_sample_id: str,
    ) -> None:
        """Routine loaded should generate state.

        NOTE Only runs when routine is running
        """
        client = client_live
        routine_id = routine_sample_id

        with client.connection():
            res = client.routine_editor.routines.get_state(routine_id=routine_id)

        assert not res.isNotOk()
        data = res.data
        assert isinstance(data, models.RoutineStateResponse)

    def test_routine_not_loaded(self, client_live: StandardBotsRobot) -> None:
        """Routine is not loaded should fail"""
        client = client_live
        routine_id = "invalid"

        with client.connection():
            res = client.routine_editor.routines.get_state(routine_id=routine_id)

        assert res.isNotOk()
        data = res.data
        assert isinstance(data, models.ErrorResponse)
        assert res.status == 400
        assert res.data.error == models.ErrorEnum.RoutineMustBeRunning


class TestPostRoutineEditorRoutinePause:
    """Tests: [POST] `/api/v1/routine-editor/routines/:routineId/pause`"""

    def test_pause_not_existing_routine(self, client_live: StandardBotsRobot) -> None:
        """Trigger pause not existing routine"""
        client = client_live

        with client.connection():
            not_existing_routine_id = "not_existing_id"
            res = client.routine_editor.routines.pause(
                routine_id=not_existing_routine_id
            )

            assert res.isNotOk()
            assert res.status == 404
            assert res.data.error == models.ErrorEnum.RoutineDoesNotExist

    def test_pause_routine_which_is_not_running(
        self, routine_sample_id: str, client_live: StandardBotsRobot
    ) -> None:
        """Trigger pause routine that is not running"""
        client = client_live

        with client.connection():
            client.routine_editor.routines.stop()

            res = client.routine_editor.routines.pause(routine_id=routine_sample_id)

            assert res.isNotOk()
            assert res.status == 400
            assert res.data.error == models.ErrorEnum.RoutineMustBePlaying

    def test_pause_routine_which_is_running(
        self, routine_sample_id: str, client_live: StandardBotsRobot
    ) -> None:
        """Trigger pause routine that is running"""
        client = client_live

        with client.connection():
            # make sure to unbreak robot
            brakes_res = client.movement.brakes.get_brakes_state()
            if brakes_res.data.state == models.BrakesStateEnum.Engaged:
                res = client.movement.brakes.set_brakes_state(
                    models.BrakesState(state=models.BrakesStateEnum.Disengaged)
                )
                assert not res.isNotOk()
            body = models.PlayRoutineRequest(variables={})

            client.routine_editor.routines.play(routine_id=routine_sample_id, body=body)

            pause_res = client.routine_editor.routines.pause(
                routine_id=routine_sample_id
            )

            assert not pause_res.isNotOk()
            assert pause_res.status == 200

            play_res = client.routine_editor.routines.play(
                routine_id=routine_sample_id, body=body
            )
            assert not play_res.isNotOk()
            assert play_res.status == 200

            client.routine_editor.routines.stop()


class TestPostRoutineEditorStop:
    """Tests: [POST] `/api/v1/routine-editor/stop`"""

    def test_stop_routine_which_is_not_running(
        self, client_live: StandardBotsRobot
    ) -> None:
        """Trigger stop routine that is not running"""
        client = client_live

        with client.connection():
            # stop routine should throw an error
            res = client.routine_editor.routines.stop()

            assert res.isNotOk()
            assert res.status == 500
            assert res.data.error == models.ErrorEnum.RoutineMustBeRunning

    def test_stop_routine_which_is_running(
        self, routine_sample_id: str, client_live: StandardBotsRobot
    ) -> None:
        """Trigger stop routine that is not running"""
        client = client_live

        with client.connection():
            #  stop routine which is playing
            body = models.PlayRoutineRequest(variables={})
            play_res = client.routine_editor.routines.play(
                routine_id=routine_sample_id, body=body
            )

            res = client.routine_editor.routines.stop()

            assert not res.isNotOk()
            assert res.status == 200

            #  stop routine which is paused
            play_res = client.routine_editor.routines.play(
                routine_id=routine_sample_id, body=body
            )

            assert not play_res.isNotOk()
            assert play_res.status == 200

            pause_res = client.routine_editor.routines.pause(
                routine_id=routine_sample_id
            )

            assert not pause_res.isNotOk()
            assert pause_res.status == 200

            res = client.routine_editor.routines.stop()

            assert not res.isNotOk()
            assert res.status == 200


class TestGetRoutineEditorVariable:
    """Tests: [GET] `/api/v1/routine-editor/variables/:variableName`"""

    def test_basic(
        self, routine_running_live_fixt: None, client_live: StandardBotsRobot
    ) -> None:
        """Basic test"""
        client = client_live

        time.sleep(3)  # give robot time to start routine
        with client.connection():
            not_existing_variable = "not_existing_name"
            response = client.routine_editor.variables.load(not_existing_variable)

            assert response.isNotOk()
            assert response.status == 400
            assert isinstance(response.data, models.ErrorResponse)
            assert response.data.error.value == "request_failed_validation"

            existing_variable = "test_public_api_global"
            response = client.routine_editor.variables.load(existing_variable)

            assert not response.isNotOk()
            assert response.status == 200
            assert isinstance(response.data, models.RuntimeVariable)
            assert response.data.value is not None


class TestPostRoutineEditorVariable:
    """Tests: [POST] `/api/v1/routine-editor/variables/:variableName`"""

    def test_basic(
        self, routine_running_live_fixt: None, client_live: StandardBotsRobot
    ) -> None:
        """Basic test"""
        client = client_live

        time.sleep(3)  # give robot time to start routine
        with client.connection():
            variable_value = models.RuntimeVariable("5")
            variable_name = "my_local_variable"
            res = client.routine_editor.variables.update(variable_value, variable_name)

            assert not res.isNotOk()
            assert res.status == 200

            var_response = client.routine_editor.variables.load(variable_name)
            assert not var_response.isNotOk()
            assert var_response.status == 200
            assert isinstance(var_response.data, models.RuntimeVariable)
            assert var_response.data.value == variable_value.value


class TestGetStatusControlMode:
    """Tests: [GET] `/api/v1/status/control-mode`

    Dependencies:
    - [x] DB
    - [ ] Robot context
    - [ ] Routine context
    """

    def test_basic(self, client_live: StandardBotsRobot) -> None:
        """Basic test"""
        client = client_live

        with client.connection():
            res_raw = client.status.control.get_configuration_state_control()
        assert not res_raw.isNotOk()
        res = res_raw.ok()

        assert res.kind in {
            RobotControlModeEnum.RoutineEditor,
            RobotControlModeEnum.Api,
        }

    def test_basic_sim(self, client_sim: StandardBotsRobot) -> None:
        """Basic test: sim mode"""
        client = client_sim

        with client.connection():
            res_raw = client.status.control.get_configuration_state_control()
        assert not res_raw.isNotOk()
        res = res_raw.ok()

        assert res.kind in {
            RobotControlModeEnum.RoutineEditor,
            RobotControlModeEnum.Api,
        }


@pytest.mark.skip("Control mode POST test does change the database")
class TestPostStatusControlMode:
    """Tests: [POST] `/api/v1/status/control-mode`"""

    """test_basic and test_basic_sim should be the same"""

    def test_basic(self, client_live: StandardBotsRobot) -> None:
        """Basic test"""
        client = client_live

        with client.connection():
            control_mode_api = RobotControlMode(kind=RobotControlModeEnum.Api)
            client.status.control.set_configuration_control_state(control_mode_api)
            res_raw_api = client.status.control.get_configuration_state_control()
            res_api = res_raw_api.ok()
            assert res_api.kind == RobotControlModeEnum.Api

            control_mode_routine_editor = RobotControlMode(
                kind=RobotControlModeEnum.RoutineEditor
            )
            client.status.control.set_configuration_control_state(
                control_mode_routine_editor
            )
            res_raw_routine_editor = (
                client.status.control.get_configuration_state_control()
            )
            res_routine_editor = res_raw_routine_editor.ok()
            assert res_routine_editor.kind == RobotControlModeEnum.RoutineEditor


class TestGetStatusHealthHealth:
    """Tests: [GET] `/api/v1/status/health`

    Dependencies:
    - [x] DB
    - [ ] Robot context
    - [ ] Routine context
    """

    def test_basic(self, client_live: StandardBotsRobot) -> None:
        """Basic test"""
        client = client_live
        with client.connection():
            res_raw = client.status.health.get_health()
        assert not res_raw.isNotOk()
        res = res_raw.ok()

        assert isinstance(res, models.StatusHealthResponse)
        assert res.health == models.StatusHealthEnum.Ok

        # TODO How to test build ID + Name better?
        # (On dev machine is always None. On others it will always change.
        # Could do via a fixture?)
        # assert ok_res.build.id == None

    def test_basic_sim(self, client_sim: StandardBotsRobot) -> None:
        """Basic test: sim mode"""
        client = client_sim
        with client.connection():
            res_raw = client.status.health.get_health()
        assert not res_raw.isNotOk()
        res = res_raw.ok()

        assert isinstance(res, models.StatusHealthResponse)
        assert res.health == models.StatusHealthEnum.Ok


class TestGetSpaceGlobalSpaces:
    """Tests: [GET] `/api/v1/space/globals`"""

    def test_basic(self, client_live: StandardBotsRobot) -> None:
        """Basic test"""
        client = client_live
        with client.connection():
            res = client.space.list_global_spaces()
            assert not res.isNotOk()
            data = res.data
            assert isinstance(data, models.SpacesPaginatedResponse)
            # Implied by test bed requirements
            assert len(data.items) >= 0


class TestGetSpacePlanes:
    """Tests: [GET] `/api/v1/space/planes`"""

    def test_basic(self, client_live: StandardBotsRobot) -> None:
        """Basic test"""
        client = client_live
        limit, offset = 10, 0

        with client.connection():
            res = client.space.list_planes(limit=limit, offset=offset)

            assert not res.isNotOk()
            data = res.data
            assert isinstance(data, models.PlanesPaginatedResponse)
            assert len(data.items) <= limit
            assert data.pagination.limit == limit
            assert data.pagination.offset == offset
            assert data.pagination.total is not None

    def test_pagination(self, client_live: StandardBotsRobot) -> None:
        """Pagination test to check offset is working"""
        client = client_live
        limit, offset = 1, 0

        with client.connection():
            res = client.space.list_planes(limit=limit, offset=offset)

            assert not res.isNotOk()
            data1 = res.data

            res2 = client.space.list_planes(limit=limit, offset=offset + limit)

            assert not res2.isNotOk()
            data2 = res2.data
            assert isinstance(data1, models.PlanesPaginatedResponse)
            assert isinstance(data2, models.PlanesPaginatedResponse)
            if len(data2.items) > 0:
                assert data1.items[0].id != data2.items[0].id

    @pytest.mark.parametrize("limit", [0, -1])
    def test_bad_limit(self, limit: int, client_live: StandardBotsRobot) -> None:
        """Bad limit test"""
        client = client_live
        offset = 0

        with client.connection():
            res = client.space.list_planes(limit=limit, offset=offset)

            assert res.isNotOk()
            assert res.status == 400
            assert isinstance(res.data, models.ErrorResponse)
            assert res.data.error == models.ErrorEnum.InvalidParameters
            assert res.data.message == "Limit must be greater than 0."

    @pytest.mark.parametrize("offset", [-1, -10])
    def test_bad_offset(self, offset: int, client_live: StandardBotsRobot) -> None:
        """Bad offset test"""
        client = client_live
        limit = 10

        with client.connection():
            res = client.space.list_planes(limit=limit, offset=offset)

            assert res.isNotOk()
            assert res.status == 400
            assert isinstance(res.data, models.ErrorResponse)
            assert res.data.error == models.ErrorEnum.InvalidParameters
            assert res.data.message == "Offset must be greater than or equal to 0."


class TestGetIO:
    """Tests: [GET] `/api/v1/io`"""

    def test_basic(self, client_live: StandardBotsRobot) -> None:
        """Basic test"""
        client = client_live
        with client.connection():
            res = client.io.status.get_io_state()
        assert not res.isNotOk()
        data = res.data
        assert isinstance(data, models.IOStateResponse)
        assert data.state is not None

    def test_basic_sim(self, client_sim: StandardBotsRobot) -> None:
        """Basic test: sim mode"""
        client = client_sim
        with client.connection():
            res = client.io.status.get_io_state()
        assert not res.isNotOk()
        data = res.data
        assert isinstance(data, models.IOStateResponse)
        assert data.state is not None


class TestPostIO:
    """Tests: [POST] `/api/v1/io`"""

    def test_change_io_state_level_validation(
        self, client_live: StandardBotsRobot
    ) -> None:
        """Test change output state - level validation"""
        client = client_live

        state_key = "Output 1"

        invalid_level_payload = models.IOStateUpdateRequest(state={state_key: "medium"})

        response = client.io.control.update_io_state(invalid_level_payload)

        assert response.isNotOk()
        assert response.status == 400
        assert response.data.error == models.ErrorEnum.RequestFailedValidation

    def test_change_io_state_port_validation(
        self, client_live: StandardBotsRobot
    ) -> None:
        """Test change output state - port validation"""
        client = client_live

        state_key = "Input 1"

        invalid_level_payload = models.IOStateUpdateRequest(state={state_key: "low"})

        response = client.io.control.update_io_state(invalid_level_payload)

        assert response.isNotOk()
        assert response.status == 400
        assert response.data.error == models.ErrorEnum.RequestFailedValidation

    def test_change_io_state(self, client_live: StandardBotsRobot) -> None:
        """Test change output state(accounting for safety settings): live mode"""
        client = client_live

        state_key = "Output 16"

        initial_state = models.IOStateUpdateRequest(state={state_key: "high"})
        final_state = models.IOStateUpdateRequest(state={state_key: "low"})

        with client.connection():
            # Set initial state and validate
            response = client.io.control.update_io_state(initial_state)

            if response.isNotOk():
                assert response.status == 403
                assert response.data.error == models.ErrorEnum.IoSafeguardError
            else:
                data = response.ok()
                assert isinstance(data, models.IOStateResponse)
                res = client.io.status.get_io_state().ok()

                assert data.state[state_key] == "high"
                assert data.state[state_key] == res.state[state_key]

            response = client.io.control.update_io_state(final_state)
            if response.isNotOk():
                assert response.status == 403
                assert response.data.error == models.ErrorEnum.IoSafeguardError
            else:
                data = response.ok()
                assert isinstance(data, models.IOStateResponse)
                res = client.io.status.get_io_state().ok()

                assert data.state[state_key] == "low"
                assert data.state[state_key] == res.state[state_key]

    def test_basic_sim(self, client_sim: StandardBotsRobot) -> None:
        """Test change output state(accounting for safety settings): sim mode"""
        client = client_sim
        initial_state = models.IOStateUpdateRequest(state={"Output 16": "high"})
        final_state = models.IOStateUpdateRequest(state={"Output 16": "low"})

        with client.connection():
            response = client.io.control.update_io_state(body=initial_state)

            if response.isNotOk():
                assert response.status == 403
                assert response.data.error == models.ErrorEnum.IoSafeguardError
            else:
                data = response.ok()

            response = client.io.control.update_io_state(body=final_state)

            if response.isNotOk():
                assert response.status == 403
                assert response.data.error == models.ErrorEnum.IoSafeguardError
            else:
                data = response.ok()

                assert isinstance(data, models.IOStateResponse)
                assert data.state["Output 16"] == "low"


class TestGetJoints:
    """Tests: [GET] `/api/v1/joints`"""

    @pytest.mark.parametrize("joint_name", ["J0", "J1", "J2", "J3", "J4", "J5"])
    def test_joint_states(
        self, joint_name: str, client_live: StandardBotsRobot
    ) -> None:
        """Basic test that each joint returns expected states."""
        client = client_live

        with client.connection():
            res = client.general.joints.get_joints_state()

        assert not res.isNotOk()
        data = res.data
        assert isinstance(data, models.JointsStateResponse)
        assert hasattr(data, joint_name), f"Joint {joint_name} not found in response"

        joint_state = getattr(data, joint_name)
        assert isinstance(joint_state.connectionStatus, models.ConnectionStatus)
        assert isinstance(joint_state.braked, bool)
        assert isinstance(joint_state.inCollision, bool)
        assert isinstance(joint_state.disturbance, models.JointStateDisturbance)


class TestPostPosesCartesianPose:
    """Tests: [POST] `/api/v1/poses/cartesian-pose`"""

    def test_cartesian_pose_construction(self, client_live: StandardBotsRobot) -> None:
        """Test cartesian pose construction"""
        client = client_live
        with client.connection():
            body = models.CartesianPoseRequest(
                pose=models.EulerPose(
                    x=500.0, y=200.0, z=300.0, rx=30.0, ry=45.0, rz=60.0
                )
            )
            res = client.poses.construct_pose.cartesian_pose(body)
            assert not res.isNotOk()
            assert res.status == 200
            assert isinstance(res.data, models.CartesianPoseResponse)
            assert isinstance(res.data.pose, models.CartesianPose)


class TestPostPosesJointPose:
    """Tests: [POST] `/api/v1/poses/joint-pose`"""

    def test_joint_pose_construction(self, client_live: StandardBotsRobot) -> None:
        """Test joint pose construction"""
        client = client_live
        with client.connection():
            body = models.JointPoseRequest(
                pose=models.JointAngles(j0=1.0, j1=-1.0, j2=1.0, j3=1.0, j4=1.0, j5=1.0)
            )
            res = client.poses.construct_pose.joint_pose(body)
            assert not res.isNotOk()
            assert res.status == 200
            assert isinstance(res.data, models.JointPoseResponse)
            assert isinstance(res.data.pose, models.CartesianPose)


class TestPostPosesPoseDistance:
    """Tests: [POST] `/api/v1/poses/pose-distance`"""

    def test_pose_zero_distance(self, client_live: StandardBotsRobot) -> None:
        """Test pose zero distance"""
        client = client_live
        with client.connection():
            cartesian_res = client.poses.construct_pose.cartesian_pose(
                models.CartesianPoseRequest(
                    pose=models.EulerPose(
                        x=500.0, y=200.0, z=300.0, rx=30.0, ry=45.0, rz=60.0
                    )
                )
            )
            cartesian_pose = cartesian_res.data.pose
            body = models.PoseDistanceRequest(
                pose1=cartesian_pose, pose2=cartesian_pose
            )
            res = client.poses.cartesian_distance.pose_distance(body)
            assert not res.isNotOk()
            assert res.status == 200
            assert isinstance(res.data, models.PoseDistanceResponse)
            assert res.data.distance == 0

    def test_pose_not_zero_distance(self, client_live: StandardBotsRobot) -> None:
        """Test pose zero distance"""
        client = client_live
        with client.connection():
            cartesian_res1 = client.poses.construct_pose.cartesian_pose(
                models.CartesianPoseRequest(
                    pose=models.EulerPose(
                        x=500.0, y=200.0, z=300.0, rx=30.0, ry=45.0, rz=60.0
                    )
                )
            )
            cartesian_res2 = client.poses.construct_pose.cartesian_pose(
                models.CartesianPoseRequest(
                    pose=models.EulerPose(
                        x=200.0, y=100.0, z=100.0, rx=20.0, ry=15.0, rz=40.0
                    )
                )
            )
            cartesian_pose1 = cartesian_res1.data.pose
            cartesian_pose2 = cartesian_res2.data.pose
            body = models.PoseDistanceRequest(
                pose1=cartesian_pose1, pose2=cartesian_pose2
            )
            res = client.poses.cartesian_distance.pose_distance(body)
            assert not res.isNotOk()
            assert res.status == 200
            assert isinstance(res.data, models.PoseDistanceResponse)
            assert res.data.distance != 0


class TestPostPosesAdd:
    """Tests: [POST] `/api/v1/poses/add`"""

    def test_poses_addition(self, client_live: StandardBotsRobot) -> None:
        """Poses addition test"""
        client = client_live
        with client.connection():
            cartesian_res1 = client.poses.construct_pose.cartesian_pose(
                models.CartesianPoseRequest(
                    pose=models.EulerPose(
                        x=500.0, y=200.0, z=300.0, rx=30.0, ry=45.0, rz=60.0
                    )
                )
            )
            cartesian_res2 = client.poses.construct_pose.cartesian_pose(
                models.CartesianPoseRequest(
                    pose=models.EulerPose(
                        x=200.0, y=100.0, z=100.0, rx=20.0, ry=15.0, rz=40.0
                    )
                )
            )
            cartesian_pose1 = cartesian_res1.data.pose
            cartesian_pose2 = cartesian_res2.data.pose
            body = models.PoseOperationsRequest(
                pose1=cartesian_pose1, pose2=cartesian_pose2
            )
            res = client.poses.pose_operations.poses_addition(body)
            assert not res.isNotOk()
            assert res.status == 200
            assert isinstance(res.data, models.PoseOperationsResponse)
            assert isinstance(res.data.pose, models.CartesianPose)


class TestPostPosesSubtract:
    """Tests: [POST] `/api/v1/poses/subtract`"""

    def test_poses_subtraction(self, client_live: StandardBotsRobot) -> None:
        """Poses subtraction test"""
        client = client_live
        with client.connection():
            cartesian_res1 = client.poses.construct_pose.cartesian_pose(
                models.CartesianPoseRequest(
                    pose=models.EulerPose(
                        x=500.0, y=200.0, z=300.0, rx=30.0, ry=45.0, rz=60.0
                    )
                )
            )
            cartesian_res2 = client.poses.construct_pose.cartesian_pose(
                models.CartesianPoseRequest(
                    pose=models.EulerPose(
                        x=200.0, y=100.0, z=100.0, rx=20.0, ry=15.0, rz=40.0
                    )
                )
            )
            cartesian_pose1 = cartesian_res1.data.pose
            cartesian_pose2 = cartesian_res2.data.pose
            body = models.PoseOperationsRequest(
                pose1=cartesian_pose1, pose2=cartesian_pose2
            )
            res = client.poses.pose_operations.poses_subtraction(body)
            assert not res.isNotOk()
            assert res.status == 200
            assert isinstance(res.data, models.PoseOperationsResponse)
            assert isinstance(res.data.pose, models.CartesianPose)


class TestGetPosesJointsPosition:
    """Tests: [GET] `/api/v1/poses/joints-position`"""

    def test_basic(self, client_live: StandardBotsRobot) -> None:
        """Basic test to retrieve joint positions"""
        client = client_live

        with client.connection():
            res = client.poses.pose_retrieval.get_joints_position()

        assert not res.isNotOk()
        data = res.data
        assert isinstance(data, models.JointsPositionResponse)
        assert isinstance(data.pose, models.JointAngles)


class TestGetPosesTooltipPosition:
    """Tests: [GET] `/api/v1/poses/tooltip-position`"""

    def test_basic(self, client_live: StandardBotsRobot) -> None:
        """Basic test to retrieve tooltip position"""
        client = client_live

        with client.connection():
            res = client.poses.pose_retrieval.get_tooltip_position()

        assert not res.isNotOk()
        data = res.data
        assert isinstance(data, models.TooltipPositionResponse)
        assert isinstance(data.pose, models.CartesianPose)


class TestGetPosesFlangePosition:
    """Tests: [GET] `/api/v1/poses/flange-position`"""

    def test_basic(self, client_live: StandardBotsRobot) -> None:
        """Basic test to retrieve flange position"""
        client = client_live

        with client.connection():
            res = client.poses.pose_retrieval.get_flange_position()

        assert not res.isNotOk()
        data = res.data
        assert isinstance(data, models.FlangePositionResponse)
        assert isinstance(data.pose, models.CartesianPose)


class TestPostPosesCartesianOffset:
    """Tests: [POST] `/api/v1/poses/cartesian-offset`"""

    def test_cartesian_offset(self, client_live: StandardBotsRobot) -> None:
        """Cartesian offset test"""
        client = client_live
        with client.connection():
            pose = models.EulerPose(
                x=500.0, y=200.0, z=300.0, rx=30.0, ry=45.0, rz=60.0
            )
            body = models.CartesianOffsetRequest(pose)
            res = client.poses.pose_operations.cartesian_offset(body)
            assert not res.isNotOk()
            assert res.status == 200
            assert isinstance(res.data, models.CartesianOffsetResponse)
            assert isinstance(res.data.pose, models.CartesianPose)


@pytest.mark.skip("Not implemented")
class TestPostInternalOnlyCreateRemoteControlAuthToken:
    """Tests: [POST] `/api/v1/internal-only/create-remote-control-auth-token`"""

    def test_basic(self, client_live: StandardBotsRobot) -> None:
        """Basic test"""
        pass

    def test_basic_sim(self, client_sim: StandardBotsRobot) -> None:
        """Basic test: sim mode"""
        pass


class TestPostInternalOnlySpeechToText:
    """Tests: [POST] `/api/v1/internal-only/speech-to-text`"""

    def test_basic_chatgpt_speech_to_text_validation(
        self, client_live: StandardBotsRobot
    ) -> None:
        """Basic test speech-to-text chatgpt validation"""
        client = client_live

        with client.connection():
            body = models.SpeechToTextRequest()
            res = client.chat_gpt.data.speech_to_text(body)

            assert res.isNotOk()
            assert res.status == 400
            assert isinstance(res.data, models.ErrorResponse)
            assert res.data.error == models.ErrorEnum.RequestFailedValidation


class TestPostInternalOnlyTextToSkill:
    """Tests: [POST] `/api/v1/internal-only/text-to-skill`"""

    def test_basic_chatgpt_text_to_skill_validation(
        self, client_live: StandardBotsRobot
    ) -> None:
        """Basic test text-to-skill chatgpt validation"""
        client = client_live

        with client.connection():
            body = models.TextToSkillRequest()
            res = client.chat_gpt.data.text_to_skill(body)

            assert res.isNotOk()
            assert res.status == 400
            assert isinstance(res.data, models.ErrorResponse)
            assert res.data.error == models.ErrorEnum.RequestFailedValidation


class TestGetIdentityBotIdentity:
    """Tests: [GET] `/api/v1/identity/bot_identity`"""

    def test_bot_identity_basic(self, client_live: StandardBotsRobot) -> None:
        """Basic bot identity test"""
        client = client_live

        with client.connection():
            res = client.general.bot_identity.bot_identity()

        assert not res.isNotOk()
        data = res.data
        assert isinstance(data, models.BotIdentityData)


@pytest.mark.skip("Not implemented")
class TestPostApiSrvGraphQL:
    """Tests: [POST] `/api/v1/api-srv/graphql`"""

    def test_basic(self, client_live: StandardBotsRobot) -> None:
        """Basic test"""
        pass

    def test_basic_sim(self, client_sim: StandardBotsRobot) -> None:
        """Basic test: sim mode"""
        pass


#  added as last test to check not recoverable routine
class TestPostFaultsUserFault:
    """Tests: [POST] `/api/v1/faults/user-fault`"""

    def test_user_fault_when_routine_not_running(
        self, client_live: StandardBotsRobot, routine_sample_id: str
    ) -> None:
        """Test when routine is not running"""

        client = client_live

        with client.connection():
            body = models.TriggerFaultRequest(
                message="Recoverable error during test run", isRecoverable=True
            )

            res = client.faults.user_faults.trigger_user_fault(body)
            assert res.status == 409
            assert isinstance(res.data, models.ErrorResponse)
            assert res.data.error == models.ErrorEnum.RoutineMustBeRunning

    def test_recoverable_routine(
        self,
        routine_running_live_fixt: None,
        client_live: StandardBotsRobot,
        routine_sample_id: str,
    ) -> None:
        """Test recoverable user faults"""

        client = client_live

        time.sleep(3)  # wait for routine to start

        with client.connection():
            body = models.TriggerFaultRequest(
                message="Recoverable error during test run", isRecoverable=True
            )

            res = client.faults.user_faults.trigger_user_fault(body)

            assert res.status == 200
            assert not res.isNotOk()

            routine_res = client.routine_editor.routines.get_state(
                routine_id=routine_sample_id
            )

            assert not routine_res.isNotOk()
            data = routine_res.data
            assert isinstance(data, models.RoutineStateResponse)
            assert routine_res.status == 200
            assert data.is_paused

            res_status = client.recovery.recover.recover()

            assert not res_status.isNotOk()

    @pytest.mark.skip(reason="Aborts entire routine")
    def test_not_recoverable_routine(
        self,
        routine_running_live_fixt: None,
        client_live: StandardBotsRobot,
        routine_sample_id: str,
    ) -> None:
        """Test not recoverable user faults"""

        client = client_live

        with client.connection():
            body = models.TriggerFaultRequest(
                message="Not recoverable error during test run", isRecoverable=False
            )

            res = client.faults.user_faults.trigger_user_fault(body)

            assert res.status == 200
            assert not res.isNotOk()

            routine_res = client.routine_editor.routines.get_state(
                routine_id=routine_sample_id
            )

            assert routine_res.isNotOk()
            assert isinstance(routine_res.data, models.ErrorResponse)
            assert routine_res.status == 400

            res_status = client.recovery.recover.recover()

            assert not res_status.isNotOk()
            assert isinstance(res_status.data, models.FailureStateResponse)
            assert res_status.data.status == models.RobotStatusEnum.Failure


class TestGetPayload:
    """Tests: [GET] `/api/v1/payload`"""

    def test_basic(self, client_live: StandardBotsRobot) -> None:
        """Basic test to get payload"""
        client = client_live

        with client.connection():
            res = client.payload.get_payload()

        assert not res.isNotOk()
        assert res.status == 200
        assert isinstance(res.data, models.PayloadStateResponse)
        assert isinstance(res.data.mass, int | float)
        assert res.data.mass >= 0


class TestPostPayload:
    """Tests: [POST] `/api/v1/payload`"""

    def test_basic(self, client_live: StandardBotsRobot) -> None:
        """Basic test to set payload"""
        client = client_live
        test_mass = 1.5

        with client.connection():
            # Set new payload
            post_res = client.payload.set_payload(
                models.PayloadStateRequest(mass=test_mass)
            )
            get_res = client.payload.get_payload()

        assert not post_res.isNotOk()
        assert post_res.status == 200
        assert not get_res.isNotOk()
        assert get_res.status == 200
        assert isinstance(get_res.data, models.PayloadStateResponse)
        assert get_res.data.mass == test_mass

    def test_invalid_payload(self, client_live: StandardBotsRobot) -> None:
        """Test setting invalid payload mass"""
        client = client_live
        invalid_mass = -20.0

        with client.connection():
            res = client.payload.set_payload(
                models.PayloadStateRequest(mass=invalid_mass)
            )

        assert res.isNotOk()
        assert res.status == 400
        assert isinstance(res.data, models.ErrorResponse)
        assert res.data.error == models.ErrorEnum.RequestFailedValidation
        assert "Payload mass cannot be less than" in res.data.message

    def test_zero_payload(self, client_live: StandardBotsRobot) -> None:
        """Test setting zero payload mass"""
        client = client_live
        zero_mass = 0.0

        with client.connection():
            post_res = client.payload.set_payload(
                models.PayloadStateRequest(mass=zero_mass)
            )
            get_res = client.payload.get_payload()

        assert not post_res.isNotOk()
        assert post_res.status == 200

        assert not get_res.isNotOk()
        assert get_res.status == 200
        assert isinstance(get_res.data, models.PayloadStateResponse)
        assert get_res.data.mass == zero_mass


class TestPostMovementPositionArmControlledHeartbeat:
    """Tests: [POST] `/api/v1/movement/position/arm/controlled/:commandId/heartbeat`

    NOTE Must be used in conjunction with an active movement.
    """

    def test_non_existent_command_id(self, client_live: StandardBotsRobot) -> None:
        """Test non-existent command ID"""
        client = client_live

        with client.connection():
            res = client.movement.position_controlled.send_heartbeat(
                command_id="non_existent_command_id"
            )

        assert res.isNotOk()
        assert res.status == 404
        assert isinstance(res.data, models.ErrorResponse)
        assert res.data.error == models.ErrorEnum.NotFound
        assert res.data.message == "Invalid command ID"


class TestPostMovementPositionArmControlled:
    """Tests: [POST] `/api/v1/movement/position/arm/controlled`"""

    def test_basic(
        self,
        client_live: StandardBotsRobot,
        unbrake_robot_fixt: None,
        move_robot_to_home_fixt: None,
    ) -> None:
        """Send a movement command with heartbeats until completion"""
        client = client_live

        with client.connection():
            # Now send a movement command
            target_position = (0.5, 0.5, 0.5, 0.5, 0.5, 0.5)
            target_position_body = models.ArmPositionUpdateControlledRequest(
                heartbeat_interval=300,
                kind=models.ArmPositionUpdateRequestKindEnum.JointRotation,
                joint_rotation=models.ArmJointRotations(joints=target_position),
            )
            res = client.movement.position_controlled.set_arm_position_controlled(
                body=target_position_body
            )
            assert not res.isNotOk()
            assert isinstance(res.data, models.SetArmPositionControlledResponse)
            command_id = res.data.id
            assert command_id is not None

            is_active = res.data.is_active
            assert is_active is not None

            i = 0
            max_iter = 10_000
            while is_active:
                res = client.movement.position_controlled.send_heartbeat(
                    command_id=command_id
                )
                assert not res.isNotOk()
                data = res.data
                assert isinstance(data, models.SetArmPositionControlledResponse)
                is_active = data.is_active
                assert is_active is not None

                i += 1
                assert i < max_iter, (
                    "Maximum iterations reached. The movement is not updating correctly."
                )

            # Get current position
            current_position = client.movement.position.get_arm_position()
            assert not current_position.isNotOk()
            assert current_position.status == 200
            data = current_position.data
            assert isinstance(data, models.CombinedArmPosition)
            current_joints = data.joint_rotations
            assert current_joints is not None

            for i, joint in enumerate(current_joints):
                assert approx_equal(joint, target_position[i], 2), (
                    f"Joint {i} is not approximately equal to target position (actual={joint}, expected={target_position[i]})"
                )

    def test_does_not_move_when_no_heartbeat_sent(
        self,
        client_live: StandardBotsRobot,
        unbrake_robot_fixt: None,
        move_robot_to_home_fixt: None,
    ) -> None:
        """Send a movement command but don't send a heartbeat. Robot should not move (much)."""
        client = client_live

        with client.connection():
            # Get current position
            initil_pos_res = client.movement.position.get_arm_position()
            assert not initil_pos_res.isNotOk()
            assert initil_pos_res.status == 200
            data = initil_pos_res.data
            assert isinstance(data, models.CombinedArmPosition)
            initial_joints = data.joint_rotations
            assert initial_joints is not None

            # Now send a movement command
            target_position = (0.5, 0.5, 0.5, 0.5, 0.5, 0.5)
            target_position_body = models.ArmPositionUpdateControlledRequest(
                heartbeat_interval=1,  # Small so it really can't move
                kind=models.ArmPositionUpdateRequestKindEnum.JointRotation,
                joint_rotation=models.ArmJointRotations(joints=target_position),
            )
            res = client.movement.position_controlled.set_arm_position_controlled(
                body=target_position_body
            )
            assert not res.isNotOk()

            time.sleep(0.1)

            # Get current position (again)
            current_position = client.movement.position.get_arm_position()
            assert not current_position.isNotOk()
            assert current_position.status == 200
            data = current_position.data
            assert isinstance(data, models.CombinedArmPosition)
            current_joints = data.joint_rotations
            assert current_joints is not None

            for i, joint in enumerate(current_joints):
                assert approx_equal(joint, initial_joints[i]), (
                    f"Joint {i} is not approximately equal to initial position (actual={joint}, expected={initial_joints[i]})"
                )

    def test_motion_planning_failure(
        self,
        client_live: StandardBotsRobot,
        unbrake_robot_fixt: None,
        move_robot_to_home_fixt: None,
    ) -> None:
        """Generate a motion planning failure. Should come up in heartbeat."""
        client = client_live

        with client.connection():
            # Now send a movement command
            target_position = (100, 100, 100, 100, 100, 100)
            target_position_body = models.ArmPositionUpdateControlledRequest(
                heartbeat_interval=300,
                kind=models.ArmPositionUpdateRequestKindEnum.JointRotation,
                joint_rotation=models.ArmJointRotations(joints=target_position),
            )
            res = client.movement.position_controlled.set_arm_position_controlled(
                body=target_position_body
            )
            assert not res.isNotOk()
            assert isinstance(res.data, models.SetArmPositionControlledResponse)
            command_id = res.data.id
            assert command_id is not None

            is_active = res.data.is_active
            assert is_active is not None

            i = 0
            max_iter = 10_000
            while is_active:
                res = client.movement.position_controlled.send_heartbeat(
                    command_id=command_id
                )
                assert not res.isNotOk()
                heartbeat_data = res.data
                assert isinstance(
                    heartbeat_data, models.SetArmPositionControlledResponse
                )
                is_active = heartbeat_data.is_active
                assert is_active is not None

                i += 1
                assert i < max_iter, (
                    "Maximum iterations reached. The movement is not updating correctly."
                )

            # Get current position: We didn't reach the target position
            current_position = client.movement.position.get_arm_position()
            assert not current_position.isNotOk()
            data = current_position.data
            assert isinstance(data, models.CombinedArmPosition)
            current_joints = data.joint_rotations
            assert current_joints is not None
            for i, joint in enumerate(current_joints):
                assert not approx_equal(joint, target_position[i], 2), (
                    f"Joint {i} is approximately equal to target position (should not reach goal) (actual={joint}, expected={target_position[i]})"
                )
            time.sleep(2)

            # Now retrieve the failure
            assert heartbeat_data.event is not None
            assert heartbeat_data.event.kind == models.ArmPositionUpdateKindEnum.Failure
            assert heartbeat_data.event.failure is not None
            assert (
                heartbeat_data.event.failure.reason
                == "Failed to generate a motion plan"
            )

    def test_move_then_stop_heartbeat(
        self,
        client_live: StandardBotsRobot,
        unbrake_robot_fixt: None,
        move_robot_to_home_fixt: None,
    ) -> None:
        """Send a movement command and stop sending heartbeats. Robot should stop moving. But we should have moved a bit."""
        client = client_live

        movement_started = 0

        with client.connection():
            # Get initial position
            initial_position = client.movement.position.get_arm_position()
            assert not initial_position.isNotOk()
            assert initial_position.status == 200
            data = initial_position.data
            assert isinstance(data, models.CombinedArmPosition)
            initial_joints = data.joint_rotations
            assert initial_joints is not None

            # Now send a movement command
            target_position = (0.5, 0.5, 0.5, 0.5, 0.5, 0.5)
            target_position_body = models.ArmPositionUpdateControlledRequest(
                heartbeat_interval=100,
                kind=models.ArmPositionUpdateRequestKindEnum.JointRotation,
                joint_rotation=models.ArmJointRotations(joints=target_position),
            )
            res = client.movement.position_controlled.set_arm_position_controlled(
                body=target_position_body
            )
            assert not res.isNotOk()
            assert isinstance(res.data, models.SetArmPositionControlledResponse)
            command_id = res.data.id
            assert command_id is not None

            is_active = res.data.is_active
            assert is_active is not None

            i = 0
            max_iter = 10_000
            while is_active:
                res = client.movement.position_controlled.send_heartbeat(
                    command_id=command_id
                )
                assert not res.isNotOk()
                data = res.data
                assert isinstance(data, models.SetArmPositionControlledResponse)
                is_active = data.is_active
                assert is_active is not None

                assert data.event is not None

                # Stop sending heartbeats once the movement has started
                if data.event.kind == models.ArmPositionUpdateKindEnum.BeginMotion:
                    movement_started += 1

                if movement_started > 5:
                    break

                i += 1
                assert i < max_iter, (
                    "Maximum iterations reached. The movement is not updating correctly."
                )

            assert movement_started > 0, "Movement never started"
            time.sleep(3)

            # Check that the arm has stopped
            res = client.recovery.recover.get_status()
            assert not res.isNotOk()
            assert res.status == 200
            status = res.data
            assert isinstance(status, models.FailureStateResponse)
            assert status.status == models.RobotStatusEnum.Idle

            # Get current position: We didn't reach the target position
            current_position = client.movement.position.get_arm_position()
            assert not current_position.isNotOk()
            data = current_position.data
            assert isinstance(data, models.CombinedArmPosition)
            current_joints = data.joint_rotations
            assert current_joints is not None

        # Arm should move a bit away from the initial position
        for i, joint in enumerate(current_joints):
            assert not approx_equal(joint, initial_joints[i], 2), (
                f"Joint {i} is approx. equal to initial joints (should move a bit) (actual={joint}, expected={initial_joints[i]})"
            )

        # Arm should not reach target position
        for i, joint in enumerate(current_joints):
            assert not approx_equal(joint, target_position[i], 2), (
                f"Joint {i} is approximately equal to target position (should not reach goal) (actual={joint}, expected={target_position[i]})"
            )
