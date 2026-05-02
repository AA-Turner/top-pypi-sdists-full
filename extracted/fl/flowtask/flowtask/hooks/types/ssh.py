import time
import fnmatch
import threading
import paramiko
from navconfig.logging import logging
from .watch import BaseWatchdog, BaseWatcher
from ...interfaces import CacheSupport

logging.getLogger("paramiko").setLevel(logging.WARNING)

class SFTPWatcher(BaseWatcher):
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        path: str,
        interval: int = 300,  # Intervalo de verificación en segundos
        max_retries: int = 5,  # Número máximo de reintentos
        retry_delay: int = 60,  # Tiempo de espera entre reintentos en segundos
        **kwargs,
    ):
        super(SFTPWatcher, self).__init__(**kwargs)
        self.host = host
        self.port = port
        self.user = username
        self.password = password
        self.interval = interval
        self.path = path
        self._expiration = kwargs.pop("every", None)
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.stop_event = kwargs.get("stop_event", threading.Event())  # Evento para detener el Watchdog

    def close_watcher(self):
        pass

    def run(self, *args, **kwargs):
        retries = 0
        while not self.stop_event.is_set():
            try:
                self._logger.info(f"Intentando conectar a {self.host}:{self.port}")
                # Conectar al servidor SSH
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(
                    hostname=self.host,
                    port=self.port,
                    username=self.user,
                    password=self.password,
                    timeout=10  # Timeout de 10 segundos
                )
                # Conectar al servidor SFTP
                sftp_client = ssh_client.open_sftp()
                self._logger.info(f"Conexión SFTP establecida en {self.host}:{self.port}")

                # Verificar si el archivo o directorio existe
                try:
                    directory, pattern = self.path.rsplit("/", 1)
                    files = sftp_client.listdir(directory)
                    matching_files = fnmatch.filter(files, pattern)

                    found_files = []
                    with CacheSupport(every=self._expiration) as cache:
                        for file in matching_files:
                            filepath = f"{directory}/{file}"
                            if cache.exists(filepath):
                                continue
                            stat = sftp_client.stat(filepath)
                            file_info = {
                                "filename": file,
                                "directory": directory,
                                "path": filepath,
                                "host": self.host,
                                "size": stat.st_size,
                                "perms": oct(stat.st_mode),
                                "modified": time.ctime(stat.st_mtime),
                            }
                            self._logger.notice(f"Encontrado {self.path} en {self.host}: {file_info}")
                            found_files.append(file_info)
                            cache.setexp(filepath, value=filepath)
                        if found_files:
                            args = {"files": found_files, **kwargs}
                            self.parent.call_actions(**args)
                except FileNotFoundError:
                    self._logger.warning(f"Ruta no encontrada: {self.path}")
                finally:
                    sftp_client.close()
                    ssh_client.close()
                    self._logger.info(f"Desconectado de {self.host}:{self.port}")
                    retries = 0  # Reiniciar el contador de reintentos tras una conexión exitosa
            except (paramiko.SSHException, paramiko.AuthenticationException, paramiko.BadHostKeyException) as e:
                self._logger.error(f"Error de conexión SSH/SFTP: {e}")
                retries += 1
                if retries >= self.max_retries:
                    self._logger.error(f"Se alcanzó el máximo de reintentos ({self.max_retries}). Deteniendo Watchdog.")
                    break
                self._logger.info(f"Reintentando en {self.retry_delay} segundos... (Intento {retries}/{self.max_retries})")
                self._sleep_with_stop(self.retry_delay)
                continue
            except Exception as e:
                self._logger.error(f"Se produjo un error al verificar el servidor: {e}")
                retries += 1
                if retries >= self.max_retries:
                    self._logger.error(f"Se alcanzó el máximo de reintentos ({self.max_retries}). Deteniendo Watchdog.")
                    break
                self._logger.info(f"Reintentando en {self.retry_delay} segundos... (Intento {retries}/{self.max_retries})")
                self._sleep_with_stop(self.retry_delay)
                continue

            # Esperar el intervalo antes de la siguiente verificación
            self._sleep_with_stop(self.interval)

    def _sleep_with_stop(self, duration: int):
        """
        Duerme de manera interrumpible, verificando el evento de parada cada segundo.
        """
        for _ in range(duration):
            if self.stop_event and self.stop_event.is_set():
                break
            time.sleep(1)


class SFTPWatchdog(BaseWatchdog):
    def create_watcher(self, *args, **kwargs) -> BaseWatcher:
        credentials = kwargs.pop("credentials", {})
        interval = kwargs.pop("interval", 300)
        self.mask_start(**kwargs)
        self.credentials = self.set_credentials(credentials)
        self.path = self.mask_replacement(kwargs.pop("path", None))
        # Crear un evento de parada para controlar la detención del Watchdog
        stop_event = threading.Event()
        self.stop_event = stop_event
        return SFTPWatcher(
            **self.credentials,
            path=self.path,
            interval=interval,
            stop_event=self.stop_event,
            **kwargs
        )
