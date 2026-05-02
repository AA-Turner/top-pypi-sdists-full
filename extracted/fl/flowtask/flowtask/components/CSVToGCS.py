import asyncio
from pathlib import Path
from typing import Callable, Tuple
from asyncdb import AsyncDB
from querysource.datasources.drivers.bigquery import bigquery_default
from .flow import FlowComponent
from ..exceptions import ComponentError

class CSVToGCS(FlowComponent):
    """
    CSVToGCS.

    Este componente sube un archivo CSV desde el sistema local a un bucket específico de Google Cloud Storage (GCS).
    Opcionalmente, puede crear el bucket si no existe.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          CSVToGCS:
          # attributes here
        ```
    """
    _version = "1.0.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.csv_path: Path = Path(kwargs.pop('csv_path'))
        self.bucket_uri: str = kwargs.pop('bucket_uri', None)  # Puede ser proporcionado directamente o generado
        self.object_name: str = kwargs.pop('object_name', self.csv_path.name)
        self.overwrite: bool = kwargs.pop('overwrite', False)
        self.create_bucket: bool = kwargs.pop('create_bucket', False)
        self.storage_class: str = kwargs.pop('storage_class', 'STANDARD')
        self.location: str = kwargs.pop('location', 'US')
        self.delete_local: bool = kwargs.pop('delete_local', False)
        self.bq = None  # Instancia de AsyncDB
        self.bucket_name: str = kwargs.pop('bucket_name', None)  # Necesario si bucket_uri no se proporciona
        super(CSVToGCS, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """Inicializa el componente configurando la conexión AsyncDB."""
        # Validar parámetros requeridos
        if not self.csv_path.exists():
            raise ComponentError(f"CSVToGCS: El archivo CSV '{self.csv_path}' no existe.")

        if not bigquery_default:
            raise ComponentError("CSVToGCS: 'bigquery_default' no está configurado correctamente.")

        # Obtener credenciales y parámetros del driver
        credentials = bigquery_default.get_credentials()

        # Inicializar AsyncDB con el driver de BigQuery
        try:
            self.bq = AsyncDB("bigquery", params=credentials)
            self._logger.info("CSVToGCS: Instancia de AsyncDB creada exitosamente.")
        except Exception as e:
            raise ComponentError(f"CSVToGCS: Error al inicializar AsyncDB: {e}") from e

    async def run(self) -> Tuple[str, str]:
        """Ejecuta la carga del archivo CSV a GCS y retorna bucket_uri y object_uri."""
        if not self.bq:
            raise ComponentError("CSVToGCS: AsyncDB no está inicializado. Asegúrate de ejecutar 'start' antes de 'run'.")

        try:
            async with await self.bq.connection() as conn:
                # Obtener bucket_uri y bucket_name del componente anterior si no se proporcionan
                if not self.bucket_uri:
                    self.bucket_uri = self.getTaskVar('bucket_uri')
                if not self.bucket_name:
                    self.bucket_name = self.getTaskVar('bucket_name')

                if not self.bucket_uri:
                    if not self.bucket_name:
                        raise ComponentError("CSVToGCS: 'bucket_uri' o 'bucket_name' deben ser proporcionados.")
                    self.bucket_uri = f"gs://{self.bucket_name}"

                # Verificar si el bucket existe
                bucket_exists = await conn.bucket_exists(self.bucket_name)
                if not bucket_exists:
                    if self.create_bucket:
                        await conn.create_bucket(
                            bucket_name=self.bucket_name,
                            location=self.location,
                            storage_class=self.storage_class
                        )
                        self._logger.info(f"CSVToGCS: Bucket '{self.bucket_name}' creado exitosamente en la región '{self.location}' con clase de almacenamiento '{self.storage_class}'.")
                    else:
                        raise ComponentError(f"CSVToGCS: El bucket '{self.bucket_name}' no existe y 'create_bucket' está establecido en False.")
                else:
                    self._logger.info(f"CSVToGCS: Bucket '{self.bucket_name}' ya existe.")

                # Subir el archivo CSV a GCS
                object_uri, message = await conn.create_gcs_from_csv(
                    bucket_uri=self.bucket_uri,
                    object_name=self.object_name,
                    csv_data=self.csv_path,
                    overwrite=self.overwrite
                )
                self._logger.info(f"CSVToGCS: {message}")

                # Guardar bucket_uri y object_uri para el siguiente componente
                self.setTaskVar('bucket_uri', self.bucket_uri)
                self.setTaskVar('object_uri', object_uri)

                # Opcionalmente eliminar el archivo local
                if self.delete_local and object_uri:
                    self.csv_path.unlink()
                    self._logger.info(f"CSVToGCS: Archivo local '{self.csv_path}' eliminado exitosamente después de la carga.")

                return self.bucket_uri, object_uri

        except ComponentError as ce:
            raise ce  # Re-lanzar errores específicos de componentes
        except Exception as e:
            raise ComponentError(f"CSVToGCS: Error durante la carga a GCS: {e}") from e

    async def close(self):
        """Cierra la conexión AsyncDB."""
        try:
            if self.bq:
                await self.bq.close()
                self._logger.info("CSVToGCS: AsyncDB cerrado exitosamente.")
        except Exception as e:
            self._logger.error(f"CSVToGCS: Error al cerrar AsyncDB: {e}")
