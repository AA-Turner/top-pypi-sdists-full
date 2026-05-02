import asyncio
from typing import Callable, Tuple
from asyncdb import AsyncDB
from querysource.datasources.drivers.bigquery import bigquery_default
from .flow import FlowComponent
from ..exceptions import ComponentError


class CreateGCSBucket(FlowComponent):
    """
    CreateGCSBucket.

    Este componente crea un bucket en Google Cloud Storage (GCS).

    Properties:

    - bucket_name: Nombre único para el bucket de GCS. (Requerido)
    - location: Región geográfica donde se creará el bucket. (Opcional, por defecto 'US')
    - storage_class: Clase de almacenamiento del bucket. (Opcional, por defecto 'STANDARD')
    - overwrite: Permite proceder si el bucket ya existe. (Opcional, por defecto 'False')

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          CreateGCSBucket:
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
        self.bucket_name: str = kwargs.pop('bucket_name')
        self.location: str = kwargs.pop('location', 'US')
        self.storage_class: str = kwargs.pop('storage_class', 'STANDARD')
        self.overwrite: bool = kwargs.pop('overwrite', False)
        self.bq = None  # Instancia de AsyncDB
        super(CreateGCSBucket, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """Inicializa el componente configurando la conexión AsyncDB."""
        # Validar parámetro requerido
        if not self.bucket_name:
            raise ComponentError("CreateGCSBucket: 'bucket_name' es un parámetro requerido.")

        if not bigquery_default:
            raise ComponentError("CreateGCSBucket: 'bigquery_default' no está configurado correctamente.")

        # Obtener credenciales y parámetros del driver
        credentials = bigquery_default.get_credentials()

        # Inicializar AsyncDB con el driver de BigQuery
        try:
            self.bq = AsyncDB("bigquery", params=credentials)
            self._logger.info("CreateGCSBucket: Instancia de AsyncDB creada exitosamente.")
        except Exception as e:
            raise ComponentError(f"CreateGCSBucket: Error al inicializar AsyncDB: {e}") from e

    async def run(self) -> Tuple[str, str]:
        """Ejecuta la creación del bucket en GCS."""
        if not self.bq:
            raise ComponentError("CreateGCSBucket: AsyncDB no está inicializado. Asegúrate de ejecutar 'start' antes de 'run'.")

        try:
            async with await self.bq.connection() as conn:
                # Verificar si el bucket existe
                bucket_exists = await conn.bucket_exists(self.bucket_name)
                if not bucket_exists:
                    # Crear el bucket
                    await conn.create_bucket(
                        bucket_name=self.bucket_name,
                        location=self.location,
                        storage_class=self.storage_class
                    )
                    message = f"Bucket '{self.bucket_name}' creado exitosamente en la región '{self.location}' con clase de almacenamiento '{self.storage_class}'."
                    self._logger.info(message)
                else:
                    if self.overwrite:
                        message = f"CreateGCSBucket: El bucket '{self.bucket_name}' ya existe."
                        self._logger.warning(message)
                    else:
                        raise ComponentError(f"CreateGCSBucket: El bucket '{self.bucket_name}' ya existe y 'overwrite' está establecido en False.")

                # Generar bucket_uri
                bucket_uri = f"gs://{self.bucket_name}"

                # Guardar bucket_name y bucket_uri en las variables de la tarea
                self.setTaskVar("bucket_name", self.bucket_name)
                self.setTaskVar("bucket_uri", bucket_uri)

                return bucket_uri, message

        except ComponentError as ce:
            raise ce  # Re-lanzar errores específicos de componentes
        except Exception as e:
            raise ComponentError(f"CreateGCSBucket: Error durante la creación del bucket: {e}") from e

    async def close(self):
        """Cierra la conexión AsyncDB."""
        try:
            if self.bq:
                await self.bq.close()
                self._logger.info("CreateGCSBucket: AsyncDB cerrado exitosamente.")
        except Exception as e:
            self._logger.error(f"CreateGCSBucket: Error al cerrar AsyncDB: {e}")
