from nhc.const import DEFAULT_PORT
from .errors import UnknownError, ToManyRequestsOrSyntaxError
from .connection import NHCConnection
from .scene import NHCScene
from .light import NHCLight
from .cover import NHCCover
from .fan import NHCFan
from .energy import NHCEnergy
from .thermostat import NHCThermostat
from .events import NHCActionEvent, NHCEnergyEvent, NHCThermostatEvent
import json
import asyncio
from collections.abc import Awaitable, Callable
from typing import Any

class NHCController:
    _actions: list[NHCLight | NHCCover | NHCFan] = []
    _locations: dict[int, str] = {}
    _energy: dict[str, NHCEnergy] = {}
    _thermostats: dict[str, NHCThermostat] = {}
    _system_info: dict[str, Any] = {}
    _callbacks: dict[str, list[Callable[[int], Awaitable[None]]]] = {}
    jobs = []
    jobRunning = False
    
    def __init__(self, host, port=DEFAULT_PORT) -> None:
        self._host: str = host
        self._port: int = port
        self._connection = NHCConnection(host, port)
        
    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def locations(self) -> dict[str, str]:
        return self._locations

    @property
    def system_info(self) -> dict[str, Any]:
        return self._system_info

    @property
    def actions(self) -> list[NHCLight | NHCCover | NHCFan]:
        return self._actions

    def scenes(self) -> list[NHCScene]:
        scenes: list[NHCScene] = []
        for action in self._actions:
            if action.is_scene is True:
                scenes.append(action)
        return scenes
    
    @property
    def lights(self) -> list[NHCLight]:
        lights: list[NHCLight] = []
        for action in self._actions:
            if action.is_light is True or action.is_dimmable is True:
                lights.append(action)
        return lights
    
    @property
    def covers(self) -> list[NHCCover]:
        covers: list[NHCCover] = []
        for action in self._actions:
            if action.is_cover is True:
                covers.append(action)
        return covers
    
    @property
    def fans(self) -> list[NHCFan]:
        fans: list[NHCFan] = []
        for action in self._actions:
            if action.is_fan is True:
                fans.append(action)
        return fans
    
    @property
    def thermostats(self) -> dict[str, Any]:
        return self._thermostats
    
    @property
    def energy(self) -> dict[str, Any]:
        return self._energy

    async def connect(self) -> None:
        await self._connection.connect()

        for location in await self._send('{"cmd": "listlocations"}'):
            self._locations[location["id"]] = location["name"]

        for thermostat in await self._send('{"cmd": "listthermostat"}'):
            entity =  NHCThermostat(self, thermostat)
            self._thermostats[entity.action_id] = entity

        for energy in await self._send('{"cmd": "listenergy"}'):
            entity = NHCEnergy(self, energy)
            self._energy[entity.action_id] = entity

        self._system_info = await self._send('{"cmd": "systeminfo"}')

        for (_action) in await self._send('{"cmd": "listactions"}'):
            entity = None
            if (_action["type"] == 0):
                entity = NHCScene(self, _action)
            elif (_action["type"] == 1 or _action["type"] == 2):
                entity = NHCLight(self, _action)
            elif (_action["type"] == 3):
                entity = NHCFan(self, _action)
            elif (_action["type"] == 4):
                entity = NHCCover(self, _action)
            if (entity is not None):
                self._actions.append(entity)
        
        self._listen_task = asyncio.create_task(self._listen())
        
    async def _send(self, data) -> dict[str, Any] | None:
        response = json.loads(await self._connection.send(data))
        if 'error' in response['data']:
            error = response['data']['error']
            if error:
                if error == 100:
                    raise Exception("NOT_FOUND")
                if error == 200:
                    raise ToManyRequestsOrSyntaxError(error)
                if error == 300:
                    raise Exception("ERROR")
                raise UnknownError(error)
        return response['data']
    
    async def _handle_job(self, job):
        self.jobs.append(job)
        if not self.jobRunning:
            await self.jobHandler()
    
    async def jobHandler(self):
        '''Handle the job queue'''
        if len(self.jobs) > 0 and not self.jobRunning:
            self.jobRunning = True
            job = self.jobs.pop(0)
            await job()
            self.jobRunning = False
            await self.jobHandler()

    async def execute(self, id: int, value: int):
        """Add an action to jobs to make sure only one command happens at a time."""
        async def job():
            await self._connection.write('{"cmd": "%s", "id": %s, "value1": %s}' % ("executeactions", id, value))
        
        await self._handle_job(job)

    async def execute_thermostat_mode(self, id: int, mode: int, overruletime: str, overrule: int) -> None:
        """Add an action to jobs to make sure only one command happens at a time."""
        async def job():
            await self._connection.write('{"cmd": "%s", "id": %s, "mode": %s}' % ("executethermostat", id, mode))
        
        await self._handle_job(job)

    async def execute_thermostat_set_temperature(self, id: int, setpoint: int) -> None:
        """Add an action to jobs to make sure only one command happens at a time."""
        async def job():
            await self._connection.write('{"cmd": "%s", "id": %s, "overrule": %s, "overruletime": "23:59",}' % ("executethermostat", id, setpoint))
        
        await self._handle_job(job)

    def register_callback(
        self, action_id: str, callback: Callable[[int], Awaitable[None]]
    ) -> Callable[[], None]:
        """Register a callback for entity updates."""
        self._callbacks.setdefault(action_id, []).append(callback)

        def remove_callback() -> None:
            self._callbacks[action_id].remove(callback)
            if not self._callbacks[action_id]:
                del self._callbacks[action_id]

        return remove_callback

    async def async_dispatch_update(self, action_id: str, value: int) -> None:
        """Dispatch an update to all registered callbacks."""
        for callback in self._callbacks.get(action_id, []):
            await callback(value)

    async def handle_event(self, event: NHCActionEvent) -> None:
        """Handle an event."""
        for action in self._actions:
            if action.id == event["id"]:
                action.update_state(event["value1"])
      
        await self.async_dispatch_update(event["id"], event["value1"])

    async def handle_energy_event(self, event: NHCEnergyEvent) -> None:
        """Handle an energy event."""
        entity = self._energy[event['channel']]
        entity.update_state(event["v"])
        await self.async_dispatch_update(entity.id, event["v"])

    async def handle_thermostat_event(self, event: NHCThermostatEvent) -> None:
        """Handle an energy event."""
        entity = self._thermostats[event['id']]
        entity.update_state(event)
        await self.async_dispatch_update(entity.id, event)

    async def _listen(self) -> None:
        """
        Listen for events. When an event is received, call callback functions.
        """
        try:
            await self._connection.write('{"cmd":"startevents"}')

            async for line in self._connection.reader:
                message = json.loads(line.decode())
                if "event" in message and message["event"] != "startevents":
                    if message["event"] == "getlive":
                        await self.handle_energy_event(message["data"])
                    elif message["event"] == "listthermostat":
                        for data in message["data"]:
                            await self.handle_thermostat_event(data)
                    else:
                        for data in message["data"]:
                            await self.handle_event(data)
        finally:
            await self._connection.close()
