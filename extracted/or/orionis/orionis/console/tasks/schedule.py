from typing import Any, List, Optional
from apscheduler.schedulers.background import BackgroundScheduler as APSBackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler as APSBlockingScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler as APSAsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.interval import IntervalTrigger
from orionis.console.contracts.reactor import IReactor
from datetime import datetime
import pytz
from orionis.console.exceptions import CLIOrionisRuntimeError
from orionis.foundation.contracts.application import IApplication
from orionis.app import Orionis

class Scheduler:
    """
    Scheduler class to manage scheduled tasks in Orionis.
    This class allows you to define commands, set triggers, and manage the scheduling of tasks.
    """

    def __init__(self) -> None:
        self.__command: str = None
        self.__args: List[str] = None
        self.__type: str = None
        self.__purpose: str = None
        self.__mode: str = None
        self.__start_date: str = None
        self.__end_date: str = None

    def command(self, signature: str, args: Optional[List[str]] = None) -> 'Scheduler':
        """
        Set the command signature and its arguments.
        """
        if not isinstance(signature, str) or not signature.strip():
            raise ValueError("The command signature must be a non-empty string.")

        if args is not None and not isinstance(args, list):
            raise ValueError("Arguments must be a list of strings or None.")

        self.__command = signature
        self.__args = args or []
        return self

    def background(self) -> 'Scheduler':
        self.__type = 'background'
        return self

    def blocking(self) -> 'Scheduler':
        self.__type = 'blocking'
        return self

    def asyncio(self) -> 'Scheduler':
        self.__type = 'asyncio'
        return self

    def porpose(self, purpose: str) -> 'Scheduler':
        if not isinstance(purpose, str) or not purpose.strip():
            raise ValueError("The purpose must be a non-empty string.")
        self.__purpose = purpose
        return self

    def onceAt(self, date: datetime) -> 'Scheduler':

        if not isinstance(date, datetime):
            raise CLIOrionisRuntimeError("The date must be an instance of datetime.")

        if self.__command is None:
            raise CLIOrionisRuntimeError("You must define a command before scheduling it.")

        if self.__type is None:
            self.background()

        if self.__purpose is None:
            self.__purpose = "Scheduled task"

        return self





# class Scheduler2():

#     def __init__(
#         self,
#         app: IApplication,
#         reactor: IReactor
#     ) -> None:
#         self.__app = app or Orionis()
#         self.__jobs: dict = {}
#         self.__command: str = None
#         self.__args: List[str] = None
#         self.__purpose: str = None
#         self.__trigger: Optional[CronTrigger | DateTrigger | IntervalTrigger] = None
#         self.__scheduler: Optional[APSBackgroundScheduler | APSBlockingScheduler | APSAsyncIOScheduler] = None
#         self.__reactor = reactor
#         self.__available_commands = self.__reactor.info()

#     def background(self):
#         self.__scheduler = APSBackgroundScheduler(
#             timezone=self.__app.config('app.timezone', 'UTC')
#         )
#         return self

#     def blocking(self):
#         self.__scheduler = APSBlockingScheduler(
#             timezone=self.__app.config('app.timezone', 'UTC')
#         )
#         return self

#     def asyncio(self):
#         self.__scheduler = APSAsyncIOScheduler(
#             timezone=self.__app.config('app.timezone', 'UTC')
#         )
#         return self

#     def command(self, signature: str, args: Optional[List[str]] = None) -> 'Scheduler':
#         """
#         Set the command signature and its arguments.
#         """
#         if not isinstance(signature, str) or not signature.strip():
#             raise ValueError("The command signature must be a non-empty string.")

#         if args is not None and not isinstance(args, list):
#             raise ValueError("Arguments must be a list of strings or None.")

#         self.__command = signature
#         self.__args = args or []
#         return self

#     def __isAvailable(self, signature: str) -> bool:
#         for command in self.__available_commands:
#             if command['signature'] == signature:
#                 return True
#         return False

#     def __getDescription(self, signature: str) -> Optional[str]:
#         """
#         Get the description of the command by its signature.
#         """
#         for command in self.__available_commands:
#             if command['signature'] == signature:
#                 return command.get('description')
#         return None

#     def command(
#         self,
#         signature: str,
#         args: Optional[List[str]] = None
#     ) -> bool:

#         # Validar que la firma del comando sea una cadena no vacía
#         if not isinstance(signature, str) or not signature.strip():
#             raise ValueError("La firma del comando debe ser una cadena no vacía.")

#         # Garantizar que los argumentos sean una lista de cadenas o None
#         if args is not None and not isinstance(args, list):
#             raise ValueError("Los argumentos deben ser una lista de cadenas o None.")

#         # Verificar si el comando ya está registrado
#         if not self.__isAvailable(signature):
#             raise ValueError(f"El comando '{signature}' no está disponible o no existe.")

#         # Almacenar el trabajo en el diccionario de trabajos
#         self.__jobs[signature] = {
#             "signature": signature,
#             "args": args or [],
            
#         }

#         # Retornar la misma instancia para permitir encadenamiento
#         return self

#     def onceAt(self, date: datetime):
#         """
#         Schedule the defined command to execute every X seconds.
#         """

#         if not isinstance(date, datetime):
#             raise CLIOrionisRuntimeError(
#                 "La fecha debe ser una instancia de datetime."
#             )

#         self.__scheduler.add_job(
#             func=lambda: self.__reactor.run(self.__jobs['signature'], *self.__jobs['args']),
#             trigger=DateTrigger(run_date=date, timezone=self.__timezone),
#             args=[self.__jobs],
#             id=self.__jobs['signature'],
#             replace_existing=True
#         )




#     # def start(self):
#     #     self.__scheduler.start()

#     # def shutdown(self, wait=True):
#     #     self.__scheduler.shutdown(wait=wait)

#     # def remove(self, job_id):
#     #     self.__scheduler.remove_job(job_id)

#     # def jobs(self):
#     #     return self.__scheduler.get_jobs()


