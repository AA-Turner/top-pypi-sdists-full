import ast
import importlib.util
import os
import sys
import textwrap
from collections import OrderedDict
from types import SimpleNamespace, ModuleType
from unittest.mock import call, patch, MagicMock
from hashlib import sha1

import Ice

from django.test import SimpleTestCase, TestCase
from passlib.handlers.bcrypt import bcrypt_sha256

from allianceauth.services.modules.mumble import authenticator
from allianceauth.services.modules.mumble.authenticator import (
    _load_slice_compat,
    main,
    _run_ice_app_compat,
)


class LoadSliceCompatTests(SimpleTestCase):
    def test_uses_ice_38_list_signature(self) -> None:
        slice_args = ["-I/usr/share/Ice/slice", "-I/tmp", "/tmp/MumbleServer.ice"]

        fakeIce = SimpleNamespace()
        fakeIce.loadSlice = MagicMock()

        with patch.object(authenticator, "Ice", fakeIce):
            _load_slice_compat(slice_args)

        fakeIce.loadSlice.assert_called_once_with(slice_args)

    def test_falls_back_to_legacy_string_signature(self) -> None:
        slice_args = ["-I/usr/share/Ice/slice", "-I/tmp", "/tmp/MumbleServer.ice"]

        fakeIce = SimpleNamespace()
        fakeIce.loadSlice = MagicMock(
            side_effect=[TypeError("new signature only"), None]
        )

        with patch.object(authenticator, "Ice", fakeIce):
            _load_slice_compat(slice_args)

        fakeIce.loadSlice.assert_has_calls(
            [
                call(slice_args),
                call("-I/usr/share/Ice/slice -I/tmp /tmp/MumbleServer.ice"),
            ]
        )

    def test_falls_back_to_legacy_two_argument_signature(self) -> None:
        slice_args = ["-I/usr/share/Ice/slice", "-I/tmp", "/tmp/MumbleServer.ice"]

        fakeIce = SimpleNamespace()
        fakeIce.loadSlice = MagicMock(
            side_effect=[
                TypeError("new signature only"),
                TypeError("string signature unavailable"),
                None,
            ]
        )

        with patch.object(authenticator, "Ice", fakeIce):
            _load_slice_compat(slice_args)

        fakeIce.loadSlice.assert_has_calls(
            [
                call(slice_args),
                call("-I/usr/share/Ice/slice -I/tmp /tmp/MumbleServer.ice"),
                call("", slice_args),
            ]
        )

    def test_raises_when_all_signatures_unavailable(self) -> None:
        slice_args = ["-I/usr/share/Ice/slice", "-I/tmp", "/tmp/MumbleServer.ice"]

        fakeIce = SimpleNamespace()
        fakeIce.loadSlice = MagicMock(side_effect=TypeError("no supported signature"))

        with patch.object(authenticator, "Ice", fakeIce):
            with self.assertRaises(TypeError):
                _load_slice_compat(slice_args)

    def test_propagates_non_typeerror_exceptions_from_loadSlice(self) -> None:
        slice_args = ["-I/usr/share/Ice/slice", "-I/tmp", "/tmp/MumbleServer.ice"]

        fakeIce = SimpleNamespace()
        fakeIce.loadSlice = MagicMock(side_effect=ValueError("unexpected"))

        with patch.object(authenticator, "Ice", fakeIce):
            with self.assertRaises(ValueError):
                _load_slice_compat(slice_args)


# class LoadSliceSmokeTests(SimpleTestCase):
#     def test_bundled_slice_file_preprocesses(self) -> None:
#         package_spec = importlib.util.find_spec("allianceauth.services.modules.mumble")
#         self.assertIsNotNone(package_spec)
#         self.assertTrue(package_spec.submodule_search_locations)
#
#         package_dir = next(iter(package_spec.submodule_search_locations))
#         slice_file = os.path.join(package_dir, "MumbleServer_1_6_870.ice")
#
#         slice_args = []
#         ice_slice_dir = Ice.getSliceDir()
#         if ice_slice_dir:
#             slice_args.append(f"-I{ice_slice_dir}")
#         else:
#             slice_args.extend(["-I/usr/share/Ice/slice", "-I/usr/share/slice"])
#
#         slice_args.extend([f"-I{package_dir}", slice_file])
#
#         _load_slice_compat(slice_args)


class MainSliceSetupTests(TestCase):
    def test_main_includes_ice_slice_dir_when_available(self) -> None:
        fake_server = SimpleNamespace(
            slice="MumbleServer_1_6_870.ice",
            watchdog=0,
            secret="",
            virtual_servers_list=lambda: [1],
            offset=1000000000,
            avatar_enable=True,
            reject_on_error=False,
            idler_handler=None,
        )
        fake_spec = SimpleNamespace(
            submodule_search_locations=[
                "/fake/pkg/allianceauth/services/modules/mumble"
            ]
        )

        fake_murmur = ModuleType("MumbleServer")
        fake_murmur.MetaCallback = type("MetaCallback", (), {})
        fake_murmur.ServerCallback = type("ServerCallback", (), {})
        fake_murmur.ServerUpdatingAuthenticator = type(
            "ServerUpdatingAuthenticator", (), {}
        )

        with (
            patch.dict(sys.modules, {"MumbleServer": fake_murmur}),
            patch(
                "allianceauth.services.modules.mumble.authenticator.MumbleServerServer"
            ) as model_mock,
            patch(
                "allianceauth.services.modules.mumble.authenticator.importlib.util.find_spec",
                return_value=fake_spec,
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator.Ice.getSliceDir",
                return_value="/opt/ice/slice",
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator._load_slice_compat"
            ) as load_compat_mock,
            patch(
                "allianceauth.services.modules.mumble.authenticator.Ice.InitializationData"
            ) as init_data_mock,
            patch(
                "allianceauth.services.modules.mumble.authenticator.Ice.createProperties"
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator._run_ice_app_compat",
                return_value=0,
            ),
        ):
            model_mock.objects.get.return_value = fake_server
            init_data_mock.return_value = SimpleNamespace(properties=None)
            main(server_id=1)

        load_compat_mock.assert_called_once_with(
            [
                "-I/opt/ice/slice",
                "-I/fake/pkg/allianceauth/services/modules/mumble",
                "/fake/pkg/allianceauth/services/modules/mumble/MumbleServer_1_6_870.ice",
            ]
        )

    def test_main_uses_default_slice_dirs_when_no_ice_slice_dir(self) -> None:
        fake_server = SimpleNamespace(
            slice="MumbleServer_1_6_870.ice",
            watchdog=0,
            secret="",
            virtual_servers_list=lambda: [1],
            offset=1000000000,
            avatar_enable=True,
            reject_on_error=False,
            idler_handler=None,
        )
        fake_spec = SimpleNamespace(
            submodule_search_locations=[
                "/fake/pkg/allianceauth/services/modules/mumble"
            ]
        )

        fake_murmur = ModuleType("MumbleServer")
        fake_murmur.MetaCallback = type("MetaCallback", (), {})
        fake_murmur.ServerCallback = type("ServerCallback", (), {})
        fake_murmur.ServerUpdatingAuthenticator = type(
            "ServerUpdatingAuthenticator", (), {}
        )

        with (
            patch.dict(sys.modules, {"MumbleServer": fake_murmur}),
            patch(
                "allianceauth.services.modules.mumble.authenticator.MumbleServerServer"
            ) as model_mock,
            patch(
                "allianceauth.services.modules.mumble.authenticator.importlib.util.find_spec",
                return_value=fake_spec,
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator.Ice.getSliceDir",
                return_value=None,
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator._load_slice_compat"
            ) as load_compat_mock,
            patch(
                "allianceauth.services.modules.mumble.authenticator.Ice.InitializationData"
            ) as init_data_mock,
            patch(
                "allianceauth.services.modules.mumble.authenticator.Ice.createProperties"
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator._run_ice_app_compat",
                return_value=0,
            ),
        ):
            model_mock.objects.get.return_value = fake_server
            init_data_mock.return_value = SimpleNamespace(properties=None)
            main(server_id=1)

        load_compat_mock.assert_called_once_with(
            [
                "-I/usr/share/Ice/slice",
                "-I/usr/share/slice",
                "-I/fake/pkg/allianceauth/services/modules/mumble",
                "/fake/pkg/allianceauth/services/modules/mumble/MumbleServer_1_6_870.ice",
            ]
        )


class RunIceAppCompatTests(SimpleTestCase):
    def test_run_returns_app_run_result_and_calls_destroy_on_success(self) -> None:
        app = SimpleNamespace()
        calls = []

        def set_communicator(comm):
            calls.append(("set", comm))

        def run(args):
            # communicator should have been passed in before run
            self.assertTrue(calls and calls[-1][0] == "set")

            return 42

        app.set_communicator = set_communicator
        app.run = run

        communicator = MagicMock()
        communicator.destroy = MagicMock()

        with patch.object(
            authenticator, "Ice", MagicMock(initialize=lambda *a, **k: communicator)
        ):
            result = _run_ice_app_compat(app, [], object())

        self.assertEqual(result, 42)
        # ensure communicator was cleared
        self.assertEqual(calls[-1], ("set", None))
        communicator.destroy.assert_called_once()

    def test_run_propagates_initialize_exception(self) -> None:
        app = SimpleNamespace()
        app.set_communicator = lambda c: None
        app.run = lambda args: 0

        with patch.object(
            authenticator,
            "Ice",
            MagicMock(
                initialize=lambda *a, **k: (_ for _ in ()).throw(
                    RuntimeError("init-fail")
                )
            ),
        ):
            with self.assertRaises(RuntimeError):
                _run_ice_app_compat(app, [], object())

    def test_run_cleans_up_and_propagates_when_app_run_raises(self) -> None:
        app = SimpleNamespace()
        calls = []

        def set_communicator(comm):
            calls.append(comm)

        def run(args):
            raise ValueError("run-failed")

        app.set_communicator = set_communicator
        app.run = run

        communicator = MagicMock()
        communicator.destroy = MagicMock()

        with patch.object(
            authenticator, "Ice", MagicMock(initialize=lambda *a, **k: communicator)
        ):
            with self.assertRaises(ValueError):
                _run_ice_app_compat(app, [], object())

        # ensure communicator was set then cleared and destroy was called
        self.assertTrue(calls and calls[0] is communicator and calls[-1] is None)
        communicator.destroy.assert_called_once()

    def test_run_ignores_destroy_exception_and_returns_result(self) -> None:
        app = SimpleNamespace()
        calls = []

        def set_communicator(comm):
            calls.append(comm)

        def run(args):
            return 7

        app.set_communicator = set_communicator
        app.run = run

        communicator = MagicMock()
        communicator.destroy.side_effect = Exception("destroy-bad")

        with patch.object(
            authenticator, "Ice", MagicMock(initialize=lambda *a, **k: communicator)
        ):
            result = _run_ice_app_compat(app, [], object())

        self.assertEqual(result, 7)
        # communicator.clear should have been called in finally despite destroy raising
        self.assertTrue(calls and calls[0] is communicator and calls[-1] is None)
        communicator.destroy.assert_called_once()


class TestAllianceauthCheckHash(TestCase):
    def test_allianceauth_check_hash_accepts_valid_sha1_bytes(self):
        password = b"hello"
        h = sha1(password).hexdigest()

        self.assertTrue(authenticator.allianceauth_check_hash(password, h, "sha1"))

    def test_allianceauth_check_hash_rejects_invalid_sha1(self):
        password = b"wrong"
        h = sha1(b"hello").hexdigest()

        self.assertFalse(authenticator.allianceauth_check_hash(password, h, "sha1"))

    def test_allianceauth_check_hash_bcrypt_sha256_verifies_password(self):
        password = "s3cr3t-pass"
        h = bcrypt_sha256.hash(password)

        self.assertTrue(
            authenticator.allianceauth_check_hash(password, h, "bcrypt-sha256")
        )

    def test_allianceauth_check_hash_unknown_hash_type_returns_false(self):
        self.assertFalse(
            authenticator.allianceauth_check_hash(b"pw", "hash", "unsupported")
        )


class TestIdlerHandler(TestCase):
    def test_idler_handler_returns_when_allowlist_excludes_channel(self):
        class DummyTimer:
            def __init__(self, interval, func, args):
                pass

            def start(self):
                pass

        with patch.object(authenticator, "Timer", DummyTimer):
            user = SimpleNamespace(name="tester", session=42, idlesecs=500, userid=100)
            state = SimpleNamespace(channel=5, selfMute=False, selfDeaf=False)
            server = MagicMock()
            server.getUsers.return_value = {user.session: user}
            server.getState.return_value = state

            # allowlist does NOT include current channel -> handler should return early
            idler_cfg = SimpleNamespace(
                seconds=300, denylist=False, list=[1, 2, 3], channel=99, interval=1
            )
            server_config_obj = SimpleNamespace(idler_handler=idler_cfg)

            authenticator.idler_handler(server, server_config_obj)

            self.assertEqual(state.channel, 5)
            self.assertFalse(state.selfMute)
            self.assertFalse(state.selfDeaf)
            server.setState.assert_not_called()

    def test_idler_handler_returns_when_denylist_includes_channel(self):
        class DummyTimer:
            def __init__(self, interval, func, args):
                pass

            def start(self):
                pass

        with patch.object(authenticator, "Timer", DummyTimer):
            user = SimpleNamespace(
                name="denytest", session=10, idlesecs=400, userid=200
            )
            state = SimpleNamespace(channel=7, selfMute=False, selfDeaf=False)
            server = MagicMock()
            server.getUsers.return_value = {user.session: user}
            server.getState.return_value = state

            # denylist True and includes channel 7 -> should return early
            idler_cfg = SimpleNamespace(
                seconds=300, denylist=True, list=[7, 8], channel=99, interval=1
            )
            server_config_obj = SimpleNamespace(idler_handler=idler_cfg)

            authenticator.idler_handler(server, server_config_obj)

            self.assertEqual(state.channel, 7)
            server.setState.assert_not_called()

    def test_idler_handler_skips_int_user_and_processes_afk_user_after(self):
        timers = []

        class DummyTimer:
            def __init__(self, interval, func, args):
                self.interval = interval
                self.func = func
                self.args = args

                timers.append(self)

            def start(self):
                pass

        with patch.object(authenticator, "Timer", DummyTimer):
            # Use an int subclass that also exposes a .name attribute so logging
            # (which accesses user.name) does not raise while isinstance(..., int)
            # still returns True and the handler will skip it.
            class IntWithName(int):
                def __new__(cls, value, name):
                    obj = int.__new__(cls, value)
                    obj.name = name
                    return obj

            int_user = IntWithName(123, "int-placeholder")
            afk_user = SimpleNamespace(name="afk", session=2, idlesecs=500, userid=201)
            state = SimpleNamespace(channel=1, selfMute=False, selfDeaf=False)
            server = MagicMock()
            # Ensure afk_user appears before the int entry so the handler sees a user object first
            server.getUsers.return_value = OrderedDict(
                [("b", afk_user), ("a", int_user)]
            )
            server.getState.return_value = state

            idler_cfg = SimpleNamespace(
                seconds=300, denylist=False, list=[1], channel=50, interval=7
            )
            server_config_obj = SimpleNamespace(idler_handler=idler_cfg)

            authenticator.idler_handler(server, server_config_obj)

            self.assertEqual(state.channel, 50)
            self.assertTrue(state.selfMute)
            self.assertTrue(state.selfDeaf)
            server.setState.assert_called_once_with(state)
            self.assertTrue(timers)
            self.assertEqual(timers[0].interval, 7)
            self.assertIs(timers[0].func, authenticator.idler_handler)
            self.assertEqual(timers[0].args, (server, server_config_obj))

    def test_idler_handler_does_not_move_if_already_in_target_channel(self):
        class DummyTimer:
            def __init__(self, interval, func, args):
                pass

            def start(self):
                pass

        with patch.object(authenticator, "Timer", DummyTimer):
            user = SimpleNamespace(name="already", session=8, idlesecs=600, userid=300)
            state = SimpleNamespace(channel=99, selfMute=False, selfDeaf=False)
            server = MagicMock()
            server.getUsers.return_value = {user.session: user}
            server.getState.return_value = state

            idler_cfg = SimpleNamespace(
                seconds=300, denylist=False, list=[99], channel=99, interval=1
            )
            server_config_obj = SimpleNamespace(idler_handler=idler_cfg)

            authenticator.idler_handler(server, server_config_obj)

            # No change because user is already in target channel
            self.assertEqual(state.channel, 99)
            server.setState.assert_not_called()


class TestMainClassAllianceAuthAuthenticatorApp(TestCase):
    # AllianceAuthAuthenticatorApp.set_communicator
    def test_set_communicator_assigns_given_object(self):
        murmur_mod = ModuleType("MumbleServer")

        class MetaCallback:
            pass

        class ServerCallback:
            pass

        class ServerUpdatingAuthenticator:
            pass

        class MetaPrx:
            @staticmethod
            def uncheckedCast(x):
                return x

        class ServerUpdatingAuthenticatorPrx:
            @staticmethod
            def uncheckedCast(x):
                return x

        class MetaCallbackPrx:
            @staticmethod
            def uncheckedCast(x):
                return x

        class ServerCallbackPrx:
            @staticmethod
            def uncheckedCast(x):
                return x

        murmur_mod.MetaCallback = MetaCallback
        murmur_mod.ServerCallback = ServerCallback
        murmur_mod.ServerUpdatingAuthenticator = ServerUpdatingAuthenticator
        murmur_mod.MetaPrx = MetaPrx
        murmur_mod.ServerUpdatingAuthenticatorPrx = ServerUpdatingAuthenticatorPrx
        murmur_mod.MetaCallbackPrx = MetaCallbackPrx
        murmur_mod.ServerCallbackPrx = ServerCallbackPrx

        sys.modules["MumbleServer"] = murmur_mod
        sys.modules["Murmur"] = murmur_mod

        # If the class is available at module level use it; otherwise extract the
        # nested class definition from the source and exec it into a minimal
        # namespace so we can instantiate and exercise set_communicator without
        # invoking main() (which loads Ice slice files).
        AppClass = getattr(authenticator, "AllianceAuthAuthenticatorApp", None)

        if AppClass is None:
            src = open(authenticator.__file__, encoding="utf-8").read()
            module_ast = ast.parse(src)
            class_node = None

            for node in module_ast.body:
                if isinstance(node, ast.FunctionDef) and node.name == "main":
                    for inner in node.body:
                        if (
                            isinstance(inner, ast.ClassDef)
                            and inner.name == "AllianceAuthAuthenticatorApp"
                        ):
                            class_node = inner
                            break

                    if class_node:
                        break

            self.assertIsNotNone(
                class_node, "Could not locate AllianceAuthAuthenticatorApp in source"
            )

            # extract source lines for the class and dedent
            lines = src.splitlines()
            class_src = "\n".join(lines[class_node.lineno - 1 : class_node.end_lineno])
            class_src = textwrap.dedent(class_src)

            ns = {}
            # provide minimal globals expected by the class definition
            ns["Murmur"] = ModuleType("Murmur")
            ns["Ice"] = ModuleType("Ice")
            ns["Timer"] = lambda *a, **k: MagicMock()
            exec(class_src, ns)
            AppClass = ns["AllianceAuthAuthenticatorApp"]

        app = AppClass()
        comm = object()
        app.set_communicator(comm)
        self.assertIs(app._communicator, comm)

    def test_set_communicator_clears_when_none_passed(self):
        # Try to obtain the class directly; if it's not available (it may be
        # defined inside main in some versions), create an app instance via
        # running main with a patched runner that captures the app object.
        AppClass = getattr(authenticator, "AllianceAuthAuthenticatorApp", None)

        if AppClass is None:
            src = open(authenticator.__file__, encoding="utf-8").read()
            module_ast = ast.parse(src)
            class_node = None

            for node in module_ast.body:
                if isinstance(node, ast.FunctionDef) and node.name == "main":
                    for inner in node.body:
                        if (
                            isinstance(inner, ast.ClassDef)
                            and inner.name == "AllianceAuthAuthenticatorApp"
                        ):
                            class_node = inner
                            break

                    if class_node:
                        break

            self.assertIsNotNone(
                class_node, "Could not locate AllianceAuthAuthenticatorApp in source"
            )

            lines = src.splitlines()
            class_src = "\n".join(lines[class_node.lineno - 1 : class_node.end_lineno])
            class_src = textwrap.dedent(class_src)

            ns = {}
            ns["Murmur"] = ModuleType("Murmur")
            ns["Ice"] = ModuleType("Ice")
            ns["Timer"] = lambda *a, **k: MagicMock()
            exec(class_src, ns)
            AppClass = ns["AllianceAuthAuthenticatorApp"]

        app = AppClass()
        dummy = object()

        app.set_communicator(dummy)
        self.assertIs(app._communicator, dummy)

        app.set_communicator(None)
        self.assertIsNone(app._communicator)

    # AllianceAuthAuthenticatorApp.run
    def test_run_returns_1_when_initializeIceConnection_returns_false(self):
        StopRun = type("StopRun", (Exception,), {})
        captured = {}

        dummy_murmur = ModuleType("MumbleServer")

        class DummyBase:
            pass

        dummy_murmur.MetaCallback = DummyBase
        dummy_murmur.ServerCallback = DummyBase
        dummy_murmur.ServerUpdatingAuthenticator = DummyBase
        dummy_murmur.MetaPrx = SimpleNamespace(uncheckedCast=lambda x: x)
        dummy_murmur.ServerUpdatingAuthenticatorPrx = SimpleNamespace(
            uncheckedCast=lambda x: x
        )
        dummy_murmur.ServerCallbackPrx = SimpleNamespace(uncheckedCast=lambda x: x)

        sys.modules["MumbleServer"] = dummy_murmur
        sys.modules["Murmur"] = dummy_murmur

        server_config = SimpleNamespace(
            slice="dummy.ice",
            ip="127.0.0.1",
            port=6502,
            endpoint="127.0.0.1:0",
            secret="s",
            watchdog=0,
            virtual_servers_list=lambda: [],
            idler_handler=None,
            offset=1000,
            avatar_enable=False,
            reject_on_error=False,
        )

        with patch(
            "allianceauth.services.modules.mumble.authenticator.MumbleServerServer.objects.get",
            return_value=server_config,
        ):
            with patch(
                "allianceauth.services.modules.mumble.authenticator.Ice.loadSlice",
                return_value=None,
            ):
                with patch(
                    "allianceauth.services.modules.mumble.authenticator._run_ice_app_compat"
                ) as mock_run:

                    def fake_run(app, args, initdata):
                        app.initializeIceConnection = lambda: False
                        result = app.run([])
                        captured["result"] = result
                        raise StopRun()

                    mock_run.side_effect = fake_run

                    with self.assertRaises(SystemExit):
                        authenticator.main(1)

        self.assertEqual(captured.get("result"), 1)

    def test_run_returns_1_when_initialized_but_communicator_is_none(self):
        class StopRun(Exception):
            pass

        fake_server_config = SimpleNamespace(
            slice="dummy.ice",
            secret="",
            ip="127.0.0.1",
            port=6502,
            endpoint="127.0.0.1:6502",
            virtual_servers_list=lambda: [],
            watchdog=0,
            offset=1000000000,
            avatar_enable=True,
            reject_on_error=False,
            idler_handler=None,
        )

        def fake_run(app, args, initdata):
            app.initializeIceConnection = lambda *a, **k: True
            app._communicator = None
            result = app.run([])
            self.assertEqual(result, 1)
            raise StopRun

        with (
            patch(
                "allianceauth.services.modules.mumble.authenticator.MumbleServerServer"
            ) as MockMgr,
            patch("importlib.util.find_spec") as mock_find_spec,
            patch(
                "allianceauth.services.modules.mumble.authenticator._load_slice_compat",
                lambda x: None,
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator._run_ice_app_compat",
                side_effect=fake_run,
            ),
        ):
            MockMgr.objects.get.return_value = fake_server_config
            mock_find_spec.return_value = SimpleNamespace(
                submodule_search_locations=[os.getcwd()]
            )

            with self.assertRaises(SystemExit):
                authenticator.main(1)

    def test_run_returns_zero_and_cancels_watchdog_when_wait_for_shutdown_succeeds(
        self,
    ):
        # Ensure a fresh import of the module and inject fake dependencies before import
        mod_name = "allianceauth.services.modules.mumble.authenticator"

        if mod_name in sys.modules:
            del sys.modules[mod_name]

        # Minimal fake Ice module used during import and by main()
        fakeIce = SimpleNamespace()
        fakeIce.Exception = Exception

        class FakeProperties:
            def setProperty(self, k, v):
                pass

        def createProperties():
            return FakeProperties()

        class InitData:
            pass

        fakeIce.createProperties = createProperties
        fakeIce.InitializationData = InitData
        fakeIce.getSliceDir = lambda: None
        fakeIce.loadSlice = lambda *args, **kwargs: None
        sys.modules["Ice"] = fakeIce

        # Minimal fake Murmur/MumbleServer module for imports inside main()
        fakeMurmur = SimpleNamespace()

        class BaseCallback:
            pass

        fakeMurmur.MetaCallback = BaseCallback
        fakeMurmur.ServerCallback = BaseCallback
        fakeMurmur.ServerUpdatingAuthenticator = BaseCallback
        fakeMurmur.MetaPrx = SimpleNamespace(
            uncheckedCast=lambda x: MagicMock(
                addCallback=MagicMock(), getBootedServers=lambda: []
            )
        )
        fakeMurmur.ServerCallbackPrx = SimpleNamespace(uncheckedCast=lambda x: x)
        fakeMurmur.ServerUpdatingAuthenticatorPrx = SimpleNamespace(
            uncheckedCast=lambda x: x
        )
        sys.modules["MumbleServer"] = fakeMurmur
        sys.modules["Murmur"] = fakeMurmur

        module = importlib.import_module(mod_name)

        # Fake server config returned by MumbleServerServer.objects.get
        mock_server_config = SimpleNamespace(
            slice="dummy.ice",
            watchdog=10,
            secret="secret",
            ip="127.0.0.1",
            port=6502,
            endpoint="127.0.0.1:6503",
            virtual_servers_list=lambda: [],
            idler_handler=None,
            offset=1000,
            avatar_enable=False,
            reject_on_error=False,
            id=1,
        )

        with patch(
            f"{mod_name}.MumbleServerServer.objects.get",
            return_value=mock_server_config,
        ):

            def fake_run(app, args, initdata):
                # Provide a communicator whose waitForShutdown succeeds (no exception)
                communicator = SimpleNamespace(waitForShutdown=lambda: None)
                app.set_communicator(communicator)

                # Short-circuit initialization and set checkConnection to attach a mock watchdog
                app.initializeIceConnection = lambda: True
                mock_watchdog = MagicMock()

                def checkConn():
                    app.watchdog = mock_watchdog

                app.checkConnection = checkConn

                # Execute the real run() and capture results on the module for assertions
                result = app.run(args)
                module._last_app = app
                module._last_run_result = result
                return result

            with patch(f"{mod_name}._run_ice_app_compat", new=fake_run):
                module.main(server_id=1)

        # Assert run returned success (0) and that watchdog.cancel was called in finally
        self.assertEqual(getattr(module, "_last_run_result", None), 0)
        self.assertTrue(hasattr(module, "_last_app"))
        self.assertTrue(hasattr(module._last_app, "watchdog"))
        module._last_app.watchdog.cancel.assert_called_once()

    def test_run_returns_one_and_cancels_watchdog_when_wait_for_shutdown_raises(self):
        mod_name = "allianceauth.services.modules.mumble.authenticator"

        if mod_name in sys.modules:
            del sys.modules[mod_name]

        fakeIce = SimpleNamespace()
        fakeIce.Exception = Exception

        class FakeProperties:
            def setProperty(self, k, v):
                pass

        def createProperties():
            return FakeProperties()

        class InitData:
            pass

        fakeIce.createProperties = createProperties
        fakeIce.InitializationData = InitData
        fakeIce.getSliceDir = lambda: None
        fakeIce.loadSlice = lambda *args, **kwargs: None
        sys.modules["Ice"] = fakeIce

        fakeMurmur = SimpleNamespace()

        class BaseCallback:
            pass

        fakeMurmur.MetaCallback = BaseCallback
        fakeMurmur.ServerCallback = BaseCallback
        fakeMurmur.ServerUpdatingAuthenticator = BaseCallback
        fakeMurmur.MetaPrx = SimpleNamespace(
            uncheckedCast=lambda x: MagicMock(
                addCallback=MagicMock(), getBootedServers=lambda: []
            )
        )
        fakeMurmur.ServerCallbackPrx = SimpleNamespace(uncheckedCast=lambda x: x)
        fakeMurmur.ServerUpdatingAuthenticatorPrx = SimpleNamespace(
            uncheckedCast=lambda x: x
        )
        sys.modules["MumbleServer"] = fakeMurmur
        sys.modules["Murmur"] = fakeMurmur

        module = importlib.import_module(mod_name)

        mock_server_config = SimpleNamespace(
            slice="dummy.ice",
            watchdog=10,
            secret="secret",
            ip="127.0.0.1",
            port=6502,
            endpoint="127.0.0.1:6503",
            virtual_servers_list=lambda: [],
            idler_handler=None,
            offset=1000,
            avatar_enable=False,
            reject_on_error=False,
            id=1,
        )

        with patch(
            f"{mod_name}.MumbleServerServer.objects.get",
            return_value=mock_server_config,
        ):

            def fake_run(app, args, initdata):
                # Communicator whose waitForShutdown raises an exception
                def raise_exc():
                    raise Exception("shutdown failure")

                communicator = SimpleNamespace(waitForShutdown=raise_exc)
                app.set_communicator(communicator)

                app.initializeIceConnection = lambda: True
                mock_watchdog = MagicMock()

                def checkConn():
                    app.watchdog = mock_watchdog

                app.checkConnection = checkConn

                result = app.run(args)
                module._last_app = app
                module._last_run_result = result
                return result

            with patch(f"{mod_name}._run_ice_app_compat", new=fake_run):
                module.main(server_id=1)

        # Run should have returned 1 on exception and watchdog.cancel must have been called
        self.assertEqual(getattr(module, "_last_run_result", None), 1)
        self.assertTrue(hasattr(module, "_last_app"))
        self.assertTrue(hasattr(module._last_app, "watchdog"))
        module._last_app.watchdog.cancel.assert_called_once()

    def test_run_returns_one_and_does_not_set_watchdog_when_initialize_fails(self):
        mod_name = "allianceauth.services.modules.mumble.authenticator"

        if mod_name in sys.modules:
            del sys.modules[mod_name]

        fakeIce = SimpleNamespace()
        fakeIce.Exception = Exception

        class FakeProperties:
            def setProperty(self, k, v):
                pass

        def createProperties():
            return FakeProperties()

        class InitData:
            pass

        fakeIce.createProperties = createProperties
        fakeIce.InitializationData = InitData
        fakeIce.getSliceDir = lambda: None
        fakeIce.loadSlice = lambda *args, **kwargs: None
        sys.modules["Ice"] = fakeIce

        fakeMurmur = SimpleNamespace()

        class BaseCallback:
            pass

        fakeMurmur.MetaCallback = BaseCallback
        fakeMurmur.ServerCallback = BaseCallback
        fakeMurmur.ServerUpdatingAuthenticator = BaseCallback
        fakeMurmur.MetaPrx = SimpleNamespace(
            uncheckedCast=lambda x: MagicMock(
                addCallback=MagicMock(), getBootedServers=lambda: []
            )
        )
        fakeMurmur.ServerCallbackPrx = SimpleNamespace(uncheckedCast=lambda x: x)
        fakeMurmur.ServerUpdatingAuthenticatorPrx = SimpleNamespace(
            uncheckedCast=lambda x: x
        )
        sys.modules["MumbleServer"] = fakeMurmur
        sys.modules["Murmur"] = fakeMurmur

        module = importlib.import_module(mod_name)

        mock_server_config = SimpleNamespace(
            slice="dummy.ice",
            watchdog=10,
            secret="secret",
            ip="127.0.0.1",
            port=6502,
            endpoint="127.0.0.1:6503",
            virtual_servers_list=lambda: [],
            idler_handler=None,
            offset=1000,
            avatar_enable=False,
            reject_on_error=False,
            id=1,
        )

        with patch(
            f"{mod_name}.MumbleServerServer.objects.get",
            return_value=mock_server_config,
        ):

            def fake_run(app, args, initdata):
                # Provide communicator but have initializeIceConnection fail so run returns early
                communicator = SimpleNamespace(waitForShutdown=lambda: None)
                app.set_communicator(communicator)

                # Force initialization to fail
                app.initializeIceConnection = lambda: False

                result = app.run(args)
                module._last_app = app
                module._last_run_result = result
                return result

            with patch(f"{mod_name}._run_ice_app_compat", new=fake_run):
                module.main(server_id=1)

        # initializeIceConnection False -> run returns 1, and watchdog should not be set
        self.assertEqual(getattr(module, "_last_run_result", None), 1)
        self.assertTrue(hasattr(module, "_last_app"))
        self.assertFalse(hasattr(module._last_app, "watchdog"))

    # AllianceAuthAuthenticatorApp.initializeIceConnection
    def test_initializeIceConnection_returns_false_when_communicator_is_none(self):
        fake_server = SimpleNamespace(
            slice="dummy.ice",
            watchdog=0,
            secret="",
            virtual_servers_list=lambda: [],
            offset=1000,
            avatar_enable=False,
            reject_on_error=False,
            idler_handler=None,
            ip="127.0.0.1",
            port=6502,
            endpoint="127.0.0.1:6502",
        )
        fake_spec = SimpleNamespace(submodule_search_locations=[os.getcwd()])

        fake_murmur = ModuleType("MumbleServer")
        fake_murmur.MetaCallback = type("MetaCallback", (), {})
        fake_murmur.ServerCallback = type("ServerCallback", (), {})
        fake_murmur.ServerUpdatingAuthenticator = type(
            "ServerUpdatingAuthenticator", (), {}
        )
        # Provide minimal Prx objects used during initialization
        fake_murmur.MetaPrx = SimpleNamespace(
            uncheckedCast=lambda x: SimpleNamespace(
                ice_context=lambda ctx: SimpleNamespace()
            )
        )
        fake_murmur.MetaCallbackPrx = SimpleNamespace(uncheckedCast=lambda x: x)
        fake_murmur.ServerUpdatingAuthenticatorPrx = SimpleNamespace(
            uncheckedCast=lambda x: x
        )
        fake_murmur.ServerCallbackPrx = SimpleNamespace(uncheckedCast=lambda x: x)

        captured = {}

        def fake_run(app, args, initdata):
            captured["app"] = app
            return 0

        with (
            patch.dict(sys.modules, {"MumbleServer": fake_murmur}),
            patch(
                "allianceauth.services.modules.mumble.authenticator.MumbleServerServer"
            ) as model_mock,
            patch(
                "allianceauth.services.modules.mumble.authenticator.importlib.util.find_spec",
                return_value=fake_spec,
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator._load_slice_compat",
                lambda x: None,
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator.Ice.InitializationData"
            ) as init_data_mock,
            patch(
                "allianceauth.services.modules.mumble.authenticator.Ice.createProperties"
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator._run_ice_app_compat",
                side_effect=fake_run,
            ),
        ):
            model_mock.objects.get.return_value = fake_server
            init_data_mock.return_value = SimpleNamespace(properties=None)
            authenticator.main(1)

        app = captured.get("app")
        self.assertIsNotNone(app)
        self.assertFalse(app.initializeIceConnection())

    def test_initializeIceConnection_returns_false_when_attachCallbacks_fails(self):
        fake_server = SimpleNamespace(
            slice="dummy.ice",
            watchdog=0,
            secret="sekrit",
            virtual_servers_list=lambda: [],
            offset=1000,
            avatar_enable=False,
            reject_on_error=False,
            idler_handler=None,
            ip="127.0.0.1",
            port=6502,
            endpoint="127.0.0.1:6502",
        )
        fake_spec = SimpleNamespace(submodule_search_locations=[os.getcwd()])

        fake_murmur = ModuleType("MumbleServer")
        fake_murmur.MetaCallback = type("MetaCallback", (), {})
        fake_murmur.ServerCallback = type("ServerCallback", (), {})
        fake_murmur.ServerUpdatingAuthenticator = type(
            "ServerUpdatingAuthenticator", (), {}
        )
        fake_murmur.MetaPrx = SimpleNamespace(
            uncheckedCast=lambda x: SimpleNamespace(
                ice_context=lambda ctx: SimpleNamespace()
            )
        )
        fake_murmur.MetaCallbackPrx = SimpleNamespace(uncheckedCast=lambda x: x)
        fake_murmur.ServerUpdatingAuthenticatorPrx = SimpleNamespace(
            uncheckedCast=lambda x: x
        )
        fake_murmur.ServerCallbackPrx = SimpleNamespace(uncheckedCast=lambda x: x)

        captured = {}

        def fake_run(app, args, initdata):
            captured["app"] = app
            return 0

        with (
            patch.dict(sys.modules, {"MumbleServer": fake_murmur}),
            patch(
                "allianceauth.services.modules.mumble.authenticator.MumbleServerServer"
            ) as model_mock,
            patch(
                "allianceauth.services.modules.mumble.authenticator.importlib.util.find_spec",
                return_value=fake_spec,
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator._load_slice_compat",
                lambda x: None,
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator.Ice.InitializationData"
            ) as init_data_mock,
            patch(
                "allianceauth.services.modules.mumble.authenticator.Ice.createProperties"
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator._run_ice_app_compat",
                side_effect=fake_run,
            ),
        ):
            model_mock.objects.get.return_value = fake_server
            init_data_mock.return_value = SimpleNamespace(properties=None)
            authenticator.main(1)

        app = captured.get("app")
        self.assertIsNotNone(app)

        comm = SimpleNamespace(
            getImplicitContext=lambda: None,
            stringToProxy=lambda s: object(),
            createObjectAdapterWithEndpoints=lambda name, endpoints: SimpleNamespace(
                activate=lambda: None, addWithUUID=lambda obj: obj
            ),
        )
        app.set_communicator(comm)
        app.attachCallbacks = lambda quiet=False: False

        self.assertFalse(app.initializeIceConnection())

    def test_initializeIceConnection_calls_implicit_context_put_and_returns_true_when_available(
        self,
    ):
        fake_server = SimpleNamespace(
            slice="dummy.ice",
            watchdog=0,
            secret="sekrit",
            virtual_servers_list=lambda: [],
            offset=1000,
            avatar_enable=False,
            reject_on_error=False,
            idler_handler=None,
            ip="127.0.0.1",
            port=6502,
            endpoint="127.0.0.1:6502",
        )
        fake_spec = SimpleNamespace(submodule_search_locations=[os.getcwd()])

        fake_murmur = ModuleType("MumbleServer")
        fake_murmur.MetaCallback = type("MetaCallback", (), {})
        fake_murmur.ServerCallback = type("ServerCallback", (), {})
        fake_murmur.ServerUpdatingAuthenticator = type(
            "ServerUpdatingAuthenticator", (), {}
        )

        meta_obj = SimpleNamespace()
        meta_obj.ice_context = lambda ctx, m=meta_obj: m
        meta_obj.addCallback = lambda cb: None
        meta_obj.getBootedServers = lambda: []

        fake_murmur.MetaPrx = SimpleNamespace(uncheckedCast=lambda x, m=meta_obj: m)
        fake_murmur.MetaCallbackPrx = SimpleNamespace(uncheckedCast=lambda x: x)
        fake_murmur.ServerUpdatingAuthenticatorPrx = SimpleNamespace(
            uncheckedCast=lambda x: x
        )
        fake_murmur.ServerCallbackPrx = SimpleNamespace(uncheckedCast=lambda x: x)

        captured = {}

        def fake_run(app, args, initdata):
            captured["app"] = app
            return 0

        with (
            patch.dict(sys.modules, {"MumbleServer": fake_murmur}),
            patch(
                "allianceauth.services.modules.mumble.authenticator.MumbleServerServer"
            ) as model_mock,
            patch(
                "allianceauth.services.modules.mumble.authenticator.importlib.util.find_spec",
                return_value=fake_spec,
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator._load_slice_compat",
                lambda x: None,
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator.Ice.InitializationData"
            ) as init_data_mock,
            patch(
                "allianceauth.services.modules.mumble.authenticator.Ice.createProperties"
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator._run_ice_app_compat",
                side_effect=fake_run,
            ),
        ):
            model_mock.objects.get.return_value = fake_server
            init_data_mock.return_value = SimpleNamespace(properties=None)
            authenticator.main(1)

        app = captured.get("app")
        self.assertIsNotNone(app)

        put_calls = []

        class ImplicitContext:
            def put(self, k, v):
                put_calls.append((k, v))

        comm = SimpleNamespace(
            getImplicitContext=lambda: ImplicitContext(),
            stringToProxy=lambda s: object(),
            createObjectAdapterWithEndpoints=lambda name, endpoints: SimpleNamespace(
                activate=lambda: None, addWithUUID=lambda obj: obj
            ),
        )
        app.set_communicator(comm)
        app.attachCallbacks = MagicMock(return_value=True)

        self.assertTrue(app.initializeIceConnection())
        self.assertEqual(app.request_context, {"secret": fake_server.secret})
        self.assertIn(("secret", fake_server.secret), put_calls)

    def test_initializeIceConnection_handles_missing_getImplicitContext_and_returns_true(
        self,
    ):
        fake_server = SimpleNamespace(
            slice="dummy.ice",
            watchdog=0,
            secret="sekrit",
            virtual_servers_list=lambda: [],
            offset=1000,
            avatar_enable=False,
            reject_on_error=False,
            idler_handler=None,
            ip="127.0.0.1",
            port=6502,
            endpoint="127.0.0.1:6502",
        )
        fake_spec = SimpleNamespace(submodule_search_locations=[os.getcwd()])

        fake_murmur = ModuleType("MumbleServer")
        fake_murmur.MetaCallback = type("MetaCallback", (), {})
        fake_murmur.ServerCallback = type("ServerCallback", (), {})
        fake_murmur.ServerUpdatingAuthenticator = type(
            "ServerUpdatingAuthenticator", (), {}
        )

        meta_obj = SimpleNamespace()
        meta_obj.ice_context = lambda ctx, m=meta_obj: m
        meta_obj.addCallback = lambda cb: None
        meta_obj.getBootedServers = lambda: []

        fake_murmur.MetaPrx = SimpleNamespace(uncheckedCast=lambda x, m=meta_obj: m)
        fake_murmur.MetaCallbackPrx = SimpleNamespace(uncheckedCast=lambda x: x)
        fake_murmur.ServerUpdatingAuthenticatorPrx = SimpleNamespace(
            uncheckedCast=lambda x: x
        )
        fake_murmur.ServerCallbackPrx = SimpleNamespace(uncheckedCast=lambda x: x)

        captured = {}

        def fake_run(app, args, initdata):
            captured["app"] = app
            return 0

        with (
            patch.dict(sys.modules, {"MumbleServer": fake_murmur}),
            patch(
                "allianceauth.services.modules.mumble.authenticator.MumbleServerServer"
            ) as model_mock,
            patch(
                "allianceauth.services.modules.mumble.authenticator.importlib.util.find_spec",
                return_value=fake_spec,
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator._load_slice_compat",
                lambda x: None,
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator.Ice.InitializationData"
            ) as init_data_mock,
            patch(
                "allianceauth.services.modules.mumble.authenticator.Ice.createProperties"
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator._run_ice_app_compat",
                side_effect=fake_run,
            ),
        ):
            model_mock.objects.get.return_value = fake_server
            init_data_mock.return_value = SimpleNamespace(properties=None)
            authenticator.main(1)

        app = captured.get("app")
        self.assertIsNotNone(app)

        class CommNoImplicit:
            def getImplicitContext(self):
                raise AttributeError()

            def stringToProxy(self, s):
                return object()

            def createObjectAdapterWithEndpoints(self, name, endpoints):
                return SimpleNamespace(
                    activate=lambda: None, addWithUUID=lambda obj: obj
                )

        comm = CommNoImplicit()
        app.set_communicator(comm)
        app.attachCallbacks = MagicMock(return_value=True)

        self.assertTrue(app.initializeIceConnection())

    # AllianceAuthAuthenticatorApp.attachCallbacks
    def test_attachCallbacks_attaches_callbacks_for_configured_virtual_server(self):
        fake_server = SimpleNamespace(
            slice="dummy.ice",
            watchdog=0,
            secret="",
            virtual_servers_list=lambda: [42],
            offset=1000,
            avatar_enable=False,
            reject_on_error=False,
            idler_handler=None,
            ip="127.0.0.1",
            port=6502,
            endpoint="127.0.0.1:6502",
        )

        fake_spec = SimpleNamespace(submodule_search_locations=[os.getcwd()])

        fake_murmur = ModuleType("MumbleServer")
        fake_murmur.MetaCallback = type("MetaCallback", (), {})
        fake_murmur.ServerCallback = type("ServerCallback", (), {})
        fake_murmur.ServerUpdatingAuthenticator = type(
            "ServerUpdatingAuthenticator", (), {}
        )
        fake_murmur.MetaPrx = SimpleNamespace(uncheckedCast=lambda x: x)
        fake_murmur.MetaCallbackPrx = SimpleNamespace(uncheckedCast=lambda x: x)
        fake_murmur.ServerUpdatingAuthenticatorPrx = SimpleNamespace(
            uncheckedCast=lambda x: x
        )
        fake_murmur.ServerCallbackPrx = SimpleNamespace(uncheckedCast=lambda x: x)

        captured = {}

        def fake_run(app, args, initdata):
            captured["app"] = app
            return 0

        with (
            patch.dict(sys.modules, {"MumbleServer": fake_murmur}),
            patch(
                "allianceauth.services.modules.mumble.authenticator.MumbleServerServer"
            ) as model_mock,
            patch(
                "allianceauth.services.modules.mumble.authenticator.importlib.util.find_spec",
                return_value=fake_spec,
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator._load_slice_compat",
                lambda x: None,
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator.Ice.InitializationData"
            ) as init_data_mock,
            patch(
                "allianceauth.services.modules.mumble.authenticator.Ice.createProperties"
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator._run_ice_app_compat",
                side_effect=fake_run,
            ),
        ):
            model_mock.objects.get.return_value = fake_server
            init_data_mock.return_value = SimpleNamespace(properties=None)
            authenticator.main(1)

        app = captured.get("app")
        self.assertIsNotNone(app)

        # Build fake server proxy returned by meta.getBootedServers()
        server_proxy = SimpleNamespace()
        server_proxy.id = lambda: 42
        server_proxy.ice_getIdentity = lambda: "identity-1"
        server_proxy.ice_context = lambda ctx: server_proxy
        server_proxy.setAuthenticator = MagicMock()
        server_proxy.addCallback = MagicMock()

        # Callback proxy object that adapter.addWithUUID will return
        cb_obj = SimpleNamespace(ice_getIdentity=lambda: "cb-ident")
        adapter = SimpleNamespace(
            addWithUUID=lambda obj: cb_obj,
            remove=MagicMock(),
            activate=lambda: None,
        )

        meta = SimpleNamespace(
            getBootedServers=lambda: [server_proxy], addCallback=MagicMock()
        )

        app.meta = meta
        app.metacb = object()
        app.adapter = adapter
        app.auth = object()

        result = app.attachCallbacks()
        self.assertTrue(result)
        server_proxy.setAuthenticator.assert_called_once_with(app.auth)
        server_proxy.addCallback.assert_called()
        self.assertIn(42, app.server_callbacks)
        entry = app.server_callbacks[42]
        self.assertIs(entry["server_proxy"], server_proxy)
        self.assertIs(entry["cb_prx"], cb_obj)

    def test_attachCallbacks_reuses_existing_callback_when_identities_match(self):
        fake_server = SimpleNamespace(
            slice="dummy.ice",
            watchdog=0,
            secret="",
            virtual_servers_list=lambda: [7],
            offset=1000,
            avatar_enable=False,
            reject_on_error=False,
            idler_handler=None,
            ip="127.0.0.1",
            port=6502,
            endpoint="127.0.0.1:6502",
        )

        fake_spec = SimpleNamespace(submodule_search_locations=[os.getcwd()])

        fake_murmur = ModuleType("MumbleServer")
        fake_murmur.MetaCallback = type("MetaCallback", (), {})
        fake_murmur.ServerCallback = type("ServerCallback", (), {})
        fake_murmur.ServerUpdatingAuthenticator = type(
            "ServerUpdatingAuthenticator", (), {}
        )
        fake_murmur.MetaPrx = SimpleNamespace(uncheckedCast=lambda x: x)
        fake_murmur.MetaCallbackPrx = SimpleNamespace(uncheckedCast=lambda x: x)
        fake_murmur.ServerUpdatingAuthenticatorPrx = SimpleNamespace(
            uncheckedCast=lambda x: x
        )
        fake_murmur.ServerCallbackPrx = SimpleNamespace(uncheckedCast=lambda x: x)

        captured = {}

        def fake_run(app, args, initdata):
            captured["app"] = app
            return 0

        with (
            patch.dict(sys.modules, {"MumbleServer": fake_murmur}),
            patch(
                "allianceauth.services.modules.mumble.authenticator.MumbleServerServer"
            ) as model_mock,
            patch(
                "allianceauth.services.modules.mumble.authenticator.importlib.util.find_spec",
                return_value=fake_spec,
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator._load_slice_compat",
                lambda x: None,
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator.Ice.InitializationData"
            ) as init_data_mock,
            patch(
                "allianceauth.services.modules.mumble.authenticator.Ice.createProperties"
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator._run_ice_app_compat",
                side_effect=fake_run,
            ),
        ):
            model_mock.objects.get.return_value = fake_server
            init_data_mock.return_value = SimpleNamespace(properties=None)
            authenticator.main(1)

        app = captured.get("app")
        self.assertIsNotNone(app)

        server_proxy = SimpleNamespace()
        server_proxy.id = lambda: 7
        server_proxy.ice_getIdentity = lambda: "same-id"
        server_proxy.ice_context = lambda ctx: server_proxy
        server_proxy.setAuthenticator = MagicMock()
        server_proxy.addCallback = MagicMock()

        cb_existing = SimpleNamespace(ice_getIdentity=lambda: "same-id")
        app.server_callbacks = {
            7: {
                "server_proxy": server_proxy,
                "cb_prx": cb_existing,
                "cb_identity": "ident-object",
            },
        }

        meta = SimpleNamespace(
            getBootedServers=lambda: [server_proxy], addCallback=MagicMock()
        )
        app.meta = meta
        app.metacb = object()
        # adapter that would create a new callback if reuse=False; track calls
        adapter = SimpleNamespace(
            addWithUUID=MagicMock(side_effect=lambda x: SimpleNamespace()),
            remove=MagicMock(),
            activate=lambda: None,
        )
        app.adapter = adapter
        app.auth = object()

        result = app.attachCallbacks()
        self.assertTrue(result)
        # since identities match, adapter.addWithUUID should not be used to create duplicate callback
        adapter.addWithUUID.assert_not_called()

    def test_attachCallbacks_removes_stale_callback_and_attaches_new_when_identity_changes(
        self,
    ):
        fake_server = SimpleNamespace(
            slice="dummy.ice",
            watchdog=0,
            secret="",
            virtual_servers_list=lambda: [99],
            offset=1000,
            avatar_enable=False,
            reject_on_error=False,
            idler_handler=None,
            ip="127.0.0.1",
            port=6502,
            endpoint="127.0.0.1:6502",
        )

        fake_spec = SimpleNamespace(submodule_search_locations=[os.getcwd()])

        fake_murmur = ModuleType("MumbleServer")
        fake_murmur.MetaCallback = type("MetaCallback", (), {})
        fake_murmur.ServerCallback = type("ServerCallback", (), {})
        fake_murmur.ServerUpdatingAuthenticator = type(
            "ServerUpdatingAuthenticator", (), {}
        )
        fake_murmur.MetaPrx = SimpleNamespace(uncheckedCast=lambda x: x)
        fake_murmur.MetaCallbackPrx = SimpleNamespace(uncheckedCast=lambda x: x)
        fake_murmur.ServerUpdatingAuthenticatorPrx = SimpleNamespace(
            uncheckedCast=lambda x: x
        )
        fake_murmur.ServerCallbackPrx = SimpleNamespace(uncheckedCast=lambda x: x)

        captured = {}

        def fake_run(app, args, initdata):
            captured["app"] = app
            return 0

        with (
            patch.dict(sys.modules, {"MumbleServer": fake_murmur}),
            patch(
                "allianceauth.services.modules.mumble.authenticator.MumbleServerServer"
            ) as model_mock,
            patch(
                "allianceauth.services.modules.mumble.authenticator.importlib.util.find_spec",
                return_value=fake_spec,
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator._load_slice_compat",
                lambda x: None,
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator.Ice.InitializationData"
            ) as init_data_mock,
            patch(
                "allianceauth.services.modules.mumble.authenticator.Ice.createProperties"
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator._run_ice_app_compat",
                side_effect=fake_run,
            ),
        ):
            model_mock.objects.get.return_value = fake_server
            init_data_mock.return_value = SimpleNamespace(properties=None)
            authenticator.main(1)

        app = captured.get("app")
        self.assertIsNotNone(app)

        server_proxy = SimpleNamespace()
        server_proxy.id = lambda: 99
        server_proxy.ice_getIdentity = lambda: "new-id"
        server_proxy.ice_context = lambda ctx: server_proxy
        server_proxy.setAuthenticator = MagicMock()
        server_proxy.addCallback = MagicMock()

        # existing stored server that returns different identity
        stored_server = SimpleNamespace(ice_getIdentity=lambda: "old-id")
        existing_entry = {
            "server_proxy": stored_server,
            "cb_prx": SimpleNamespace(),
            "cb_identity": "old-identity-obj",
        }
        app.server_callbacks = {99: existing_entry}

        cb_new = SimpleNamespace(ice_getIdentity=lambda: "cb-new-ident")
        adapter = SimpleNamespace(
            addWithUUID=lambda obj: cb_new, remove=MagicMock(), activate=lambda: None
        )
        meta = SimpleNamespace(
            getBootedServers=lambda: [server_proxy], addCallback=MagicMock()
        )

        app.meta = meta
        app.metacb = object()
        app.adapter = adapter
        app.auth = object()

        result = app.attachCallbacks()
        self.assertTrue(result)
        # adapter.remove should have been called for the old identity
        adapter.remove.assert_called()
        # a new callback should have been added and stored
        self.assertIn(99, app.server_callbacks)
        self.assertIs(app.server_callbacks[99]["cb_prx"], cb_new)

    # AllianceAuthAuthenticatorApp.checkConnection
    def test_checkConnection_sets_failedWatch_true_and_schedules_watchdog_when_attachCallbacks_returns_false(
        self,
    ):
        fake_server = SimpleNamespace(
            slice="dummy.ice",
            watchdog=3,
            secret="",
            virtual_servers_list=lambda: [],
            offset=1000,
            avatar_enable=False,
            reject_on_error=False,
            idler_handler=None,
            ip="127.0.0.1",
            port=6502,
            endpoint="127.0.0.1:6502",
        )

        fake_spec = SimpleNamespace(submodule_search_locations=[os.getcwd()])

        fake_murmur = ModuleType("MumbleServer")
        fake_murmur.MetaCallback = type("MetaCallback", (), {})
        fake_murmur.ServerCallback = type("ServerCallback", (), {})
        fake_murmur.ServerUpdatingAuthenticator = type(
            "ServerUpdatingAuthenticator", (), {}
        )
        fake_murmur.MetaPrx = SimpleNamespace(uncheckedCast=lambda x: x)
        fake_murmur.MetaCallbackPrx = SimpleNamespace(uncheckedCast=lambda x: x)
        fake_murmur.ServerUpdatingAuthenticatorPrx = SimpleNamespace(
            uncheckedCast=lambda x: x
        )
        fake_murmur.ServerCallbackPrx = SimpleNamespace(uncheckedCast=lambda x: x)

        captured = {}

        def fake_run(app, args, initdata):
            captured["app"] = app
            return 0

        with (
            patch.dict(sys.modules, {"MumbleServer": fake_murmur}),
            patch(
                "allianceauth.services.modules.mumble.authenticator.MumbleServerServer"
            ) as model_mock,
            patch(
                "allianceauth.services.modules.mumble.authenticator.importlib.util.find_spec",
                return_value=fake_spec,
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator._load_slice_compat",
                lambda x: None,
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator.Ice.InitializationData"
            ) as init_data_mock,
            patch(
                "allianceauth.services.modules.mumble.authenticator.Ice.createProperties"
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator._run_ice_app_compat",
                side_effect=fake_run,
            ),
        ):
            model_mock.objects.get.return_value = fake_server
            init_data_mock.return_value = SimpleNamespace(properties=None)
            authenticator.main(1)

        app = captured.get("app")
        self.assertIsNotNone(app)

        app.attachCallbacks = MagicMock(return_value=False)
        app.failedWatch = False

        timer_mock = MagicMock()
        with patch.object(
            authenticator, "Timer", MagicMock(return_value=timer_mock)
        ) as TimerCtor:
            app.checkConnection()

        self.assertTrue(app.failedWatch)
        TimerCtor.assert_called_once_with(fake_server.watchdog, app.checkConnection)
        timer_mock.start.assert_called_once()

    def test_checkConnection_sets_failedWatch_false_and_schedules_watchdog_when_attachCallbacks_returns_true(
        self,
    ):
        fake_server = SimpleNamespace(
            slice="dummy.ice",
            watchdog=4,
            secret="",
            virtual_servers_list=lambda: [],
            offset=1000,
            avatar_enable=False,
            reject_on_error=False,
            idler_handler=None,
            ip="127.0.0.1",
            port=6502,
            endpoint="127.0.0.1:6502",
        )

        fake_spec = SimpleNamespace(submodule_search_locations=[os.getcwd()])

        fake_murmur = ModuleType("MumbleServer")
        fake_murmur.MetaCallback = type("MetaCallback", (), {})
        fake_murmur.ServerCallback = type("ServerCallback", (), {})
        fake_murmur.ServerUpdatingAuthenticator = type(
            "ServerUpdatingAuthenticator", (), {}
        )
        fake_murmur.MetaPrx = SimpleNamespace(uncheckedCast=lambda x: x)
        fake_murmur.MetaCallbackPrx = SimpleNamespace(uncheckedCast=lambda x: x)
        fake_murmur.ServerUpdatingAuthenticatorPrx = SimpleNamespace(
            uncheckedCast=lambda x: x
        )
        fake_murmur.ServerCallbackPrx = SimpleNamespace(uncheckedCast=lambda x: x)

        captured = {}

        def fake_run(app, args, initdata):
            captured["app"] = app
            return 0

        with (
            patch.dict(sys.modules, {"MumbleServer": fake_murmur}),
            patch(
                "allianceauth.services.modules.mumble.authenticator.MumbleServerServer"
            ) as model_mock,
            patch(
                "allianceauth.services.modules.mumble.authenticator.importlib.util.find_spec",
                return_value=fake_spec,
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator._load_slice_compat",
                lambda x: None,
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator.Ice.InitializationData"
            ) as init_data_mock,
            patch(
                "allianceauth.services.modules.mumble.authenticator.Ice.createProperties"
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator._run_ice_app_compat",
                side_effect=fake_run,
            ),
        ):
            model_mock.objects.get.return_value = fake_server
            init_data_mock.return_value = SimpleNamespace(properties=None)
            authenticator.main(1)

        app = captured.get("app")
        self.assertIsNotNone(app)

        app.attachCallbacks = MagicMock(return_value=True)
        app.failedWatch = True

        timer_mock = MagicMock()
        with patch.object(
            authenticator, "Timer", MagicMock(return_value=timer_mock)
        ) as TimerCtor:
            app.checkConnection()

        self.assertFalse(app.failedWatch)
        TimerCtor.assert_called_once_with(fake_server.watchdog, app.checkConnection)
        timer_mock.start.assert_called_once()

    def test_checkConnection_handles_ice_exception_and_marks_failedWatch_true(self):
        fake_server = SimpleNamespace(
            slice="dummy.ice",
            watchdog=2,
            secret="",
            virtual_servers_list=lambda: [],
            offset=1000,
            avatar_enable=False,
            reject_on_error=False,
            idler_handler=None,
            ip="127.0.0.1",
            port=6502,
            endpoint="127.0.0.1:6502",
        )

        fake_spec = SimpleNamespace(submodule_search_locations=[os.getcwd()])

        fake_murmur = ModuleType("MumbleServer")
        fake_murmur.MetaCallback = type("MetaCallback", (), {})
        fake_murmur.ServerCallback = type("ServerCallback", (), {})
        fake_murmur.ServerUpdatingAuthenticator = type(
            "ServerUpdatingAuthenticator", (), {}
        )
        fake_murmur.MetaPrx = SimpleNamespace(uncheckedCast=lambda x: x)
        fake_murmur.MetaCallbackPrx = SimpleNamespace(uncheckedCast=lambda x: x)
        fake_murmur.ServerUpdatingAuthenticatorPrx = SimpleNamespace(
            uncheckedCast=lambda x: x
        )
        fake_murmur.ServerCallbackPrx = SimpleNamespace(uncheckedCast=lambda x: x)

        captured = {}

        def fake_run(app, args, initdata):
            captured["app"] = app
            return 0

        with (
            patch.dict(sys.modules, {"MumbleServer": fake_murmur}),
            patch(
                "allianceauth.services.modules.mumble.authenticator.MumbleServerServer"
            ) as model_mock,
            patch(
                "allianceauth.services.modules.mumble.authenticator.importlib.util.find_spec",
                return_value=fake_spec,
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator._load_slice_compat",
                lambda x: None,
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator.Ice.InitializationData"
            ) as init_data_mock,
            patch(
                "allianceauth.services.modules.mumble.authenticator.Ice.createProperties"
            ),
            patch(
                "allianceauth.services.modules.mumble.authenticator._run_ice_app_compat",
                side_effect=fake_run,
            ),
        ):
            model_mock.objects.get.return_value = fake_server
            init_data_mock.return_value = SimpleNamespace(properties=None)
            authenticator.main(1)

        app = captured.get("app")
        self.assertIsNotNone(app)

        # Patch module Ice to have Exception refer to built-in Exception so our raised exception matches except Ice.Exception
        with patch.object(authenticator, "Ice", SimpleNamespace(Exception=Exception)):

            def raise_ice_exc(*a, **k):
                raise Exception("boom")

            app.attachCallbacks = raise_ice_exc
            app.failedWatch = False

            timer_mock = MagicMock()
            with patch.object(
                authenticator, "Timer", MagicMock(return_value=timer_mock)
            ) as TimerCtor:
                app.checkConnection()

            self.assertTrue(app.failedWatch)
            TimerCtor.assert_called_once_with(fake_server.watchdog, app.checkConnection)
            timer_mock.start.assert_called_once()


class TestMainCheckSecret(TestCase):
    def test_checkSecret_returns_original_when_no_secret_configured(self):
        src = open(authenticator.__file__, encoding="utf-8").read()
        module_ast = ast.parse(src)
        func_node = None

        for node in module_ast.body:
            if isinstance(node, ast.FunctionDef) and node.name == "main":
                for inner in node.body:
                    if (
                        isinstance(inner, ast.FunctionDef)
                        and inner.name == "checkSecret"
                    ):
                        func_node = inner
                        break

                if func_node:
                    break

        self.assertIsNotNone(func_node, "Could not locate checkSecret in source")

        lines = src.splitlines()
        func_src = "\n".join(lines[func_node.lineno - 1 : func_node.end_lineno])
        func_src = textwrap.dedent(func_src)

        ns = {}
        # Provide minimal globals used by checkSecret
        ns["Murmur"] = ModuleType("Murmur")
        ns["logger"] = authenticator.logger
        ns["server_config_obj"] = SimpleNamespace(secret="")

        exec(func_src, ns)
        checkSecret = ns["checkSecret"]

        def original(*a, **k):
            return "called"

        decorated = checkSecret(original)
        # When no secret is configured the decorator should return the original
        self.assertIs(decorated, original)

    def test_checkSecret_allows_call_when_secret_matches_and_current_passed_as_kwarg(
        self,
    ):
        src = open(authenticator.__file__, encoding="utf-8").read()
        module_ast = ast.parse(src)
        func_node = None

        for node in module_ast.body:
            if isinstance(node, ast.FunctionDef) and node.name == "main":
                for inner in node.body:
                    if (
                        isinstance(inner, ast.FunctionDef)
                        and inner.name == "checkSecret"
                    ):
                        func_node = inner
                        break

                if func_node:
                    break

        lines = src.splitlines()
        func_src = "\n".join(lines[func_node.lineno - 1 : func_node.end_lineno])
        func_src = textwrap.dedent(func_src)

        ns = {}
        # Provide minimal globals used by checkSecret
        ns["Murmur"] = ModuleType("Murmur")
        # Provide an exception type the decorator will raise on invalid secret
        ns["Murmur"].InvalidSecretException = type(
            "InvalidSecretException", (Exception,), {}
        )
        ns["logger"] = authenticator.logger
        ns["server_config_obj"] = SimpleNamespace(secret="sekrit")

        exec(func_src, ns)
        checkSecret = ns["checkSecret"]

        called = {}

        def original(*a, **k):
            called["ok"] = True
            return "ok"

        decorated = checkSecret(original)
        current = SimpleNamespace(ctx={"secret": "sekrit"})
        result = decorated(current=current)
        self.assertEqual(result, "ok")
        self.assertTrue(called.get("ok"))

    def test_checkSecret_allows_call_when_secret_matches_and_current_passed_positionally(
        self,
    ):
        src = open(authenticator.__file__, encoding="utf-8").read()
        module_ast = ast.parse(src)
        func_node = None

        for node in module_ast.body:
            if isinstance(node, ast.FunctionDef) and node.name == "main":
                for inner in node.body:
                    if (
                        isinstance(inner, ast.FunctionDef)
                        and inner.name == "checkSecret"
                    ):
                        func_node = inner
                        break

                if func_node:
                    break

        lines = src.splitlines()
        func_src = "\n".join(lines[func_node.lineno - 1 : func_node.end_lineno])
        func_src = textwrap.dedent(func_src)

        ns = {}
        ns["Murmur"] = ModuleType("Murmur")
        ns["Murmur"].InvalidSecretException = type(
            "InvalidSecretException", (Exception,), {}
        )
        ns["logger"] = authenticator.logger
        ns["server_config_obj"] = SimpleNamespace(secret="sekrit")

        exec(func_src, ns)
        checkSecret = ns["checkSecret"]

        def original(*a, **k):
            return a, k

        decorated = checkSecret(original)
        current = SimpleNamespace(ctx={"secret": "sekrit"})
        # pass current positionally as the last arg
        args, kws = decorated(1, current)
        self.assertEqual(args[-1], current)

    def test_checkSecret_raises_when_secret_missing_or_mismatch(self):
        src = open(authenticator.__file__, encoding="utf-8").read()
        module_ast = ast.parse(src)
        func_node = None

        for node in module_ast.body:
            if isinstance(node, ast.FunctionDef) and node.name == "main":
                for inner in node.body:
                    if (
                        isinstance(inner, ast.FunctionDef)
                        and inner.name == "checkSecret"
                    ):
                        func_node = inner
                        break

                if func_node:
                    break

        lines = src.splitlines()
        func_src = "\n".join(lines[func_node.lineno - 1 : func_node.end_lineno])
        func_src = textwrap.dedent(func_src)

        ns = {}
        ns["Murmur"] = ModuleType("Murmur")
        ns["Murmur"].InvalidSecretException = type(
            "InvalidSecretException", (Exception,), {}
        )
        ns["logger"] = authenticator.logger
        ns["server_config_obj"] = SimpleNamespace(secret="sekrit")

        exec(func_src, ns)
        checkSecret = ns["checkSecret"]

        def original(*a, **k):
            return "ok"

        decorated = checkSecret(original)

        # missing ctx (present but empty to exercise decorator branch that checks for 'secret')
        bad_current = SimpleNamespace(ctx={})
        with self.assertRaises(ns["Murmur"].InvalidSecretException):
            decorated(current=bad_current)

        # wrong secret
        wrong_current = SimpleNamespace(ctx={"secret": "nope"})
        with self.assertRaises(ns["Murmur"].InvalidSecretException):
            decorated(current=wrong_current)

    def test_checkSecret_raises_when_current_is_none(self):
        src = open(authenticator.__file__, encoding="utf-8").read()
        module_ast = ast.parse(src)
        func_node = None

        for node in module_ast.body:
            if isinstance(node, ast.FunctionDef) and node.name == "main":
                for inner in node.body:
                    if (
                        isinstance(inner, ast.FunctionDef)
                        and inner.name == "checkSecret"
                    ):
                        func_node = inner
                        break

                if func_node:
                    break

        lines = src.splitlines()
        func_src = "\n".join(lines[func_node.lineno - 1 : func_node.end_lineno])
        func_src = textwrap.dedent(func_src)

        ns = {}
        ns["Murmur"] = ModuleType("Murmur")
        ns["Murmur"].InvalidSecretException = type(
            "InvalidSecretException", (Exception,), {}
        )
        ns["logger"] = authenticator.logger
        ns["server_config_obj"] = SimpleNamespace(secret="sekrit")

        exec(func_src, ns)
        checkSecret = ns["checkSecret"]

        def original(*a, **k):
            return "ok"

        decorated = checkSecret(original)

        with self.assertRaises(ns["Murmur"].InvalidSecretException):
            decorated(current=None)
