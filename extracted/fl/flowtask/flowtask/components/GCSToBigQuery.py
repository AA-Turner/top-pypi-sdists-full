import asyncio
from typing import Callable, Tuple, List
from asyncdb import AsyncDB
from querysource.datasources.drivers.bigquery import bigquery_default
from .flow import FlowComponent
from ..exceptions import ComponentError


class GCSToBigQuery(FlowComponent):
    """
    GCSToBigQuery.

    Este componente carga un archivo CSV desde un bucket específico de GCS a una tabla de BigQuery.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          GCSToBigQuery:
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
        self.bucket_uri: str = kwargs.pop('bucket_uri', None)       # Recibe el object_uri de CSVToGCS
        self.table_id: str = kwargs.pop('table_id')
        self.dataset_id: str = kwargs.pop('dataset_id')
        self.schema: List[dict] = kwargs.pop('schema', None)
        self.overwrite: bool = kwargs.pop('overwrite', False)
        self.delete_gcs: bool = kwargs.pop('delete_gcs', False)
        self.bq = None  # Instancia de AsyncDB
        super(GCSToBigQuery, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """Inicializa el componente configurando la conexión AsyncDB."""
        # Obtener bucket_uri del componente anterior si no se proporciona directamente
        if not self.bucket_uri:
            self.bucket_uri = self.getTaskVar('object_uri')  # Get object_uri set by CSVToGCS

        # Validar parámetros requeridos
        if not self.bucket_uri or not self.table_id or not self.dataset_id:
            raise ComponentError("GCSToBigQuery: 'bucket_uri', 'table_id' y 'dataset_id' son parámetros requeridos.")

        if not bigquery_default:
            raise ComponentError("GCSToBigQuery: 'bigquery_default' no está configurado correctamente.")

        # Obtener credenciales y parámetros del driver
        credentials = bigquery_default.get_credentials()

        # Inicializar AsyncDB con el driver de BigQuery
        try:
            self.bq = AsyncDB("bigquery", params=credentials)
            self._logger.info("GCSToBigQuery: Instancia de AsyncDB creada exitosamente.")
        except Exception as e:
            raise ComponentError(f"GCSToBigQuery: Error al inicializar AsyncDB: {e}") from e

    async def run(self) -> Tuple[str, str]:
        """Ejecuta la carga del CSV desde GCS a BigQuery."""
        if not self.bq:
            raise ComponentError("GCSToBigQuery: AsyncDB no está inicializado. Asegúrate de ejecutar 'start' antes de 'run'.")

        try:
            async with await self.bq.connection() as conn:
                # Truncar la tabla si overwrite=True
                if self.overwrite:
                    truncated = await conn.truncate_table(
                        dataset_id=self.dataset_id,
                        table_id=self.table_id
                    )
                    self._logger.info(f"GCSToBigQuery: Tabla '{self.dataset_id}.{self.table_id}' truncada exitosamente.")

                # Cargar el CSV desde GCS a BigQuery
                load_result = await conn.read_csv_from_gcs(
                    bucket_uri=self.bucket_uri,
                    table_id=self.table_id,
                    dataset_id=self.dataset_id,
                    schema=self.schema  # Puede ser None para autodetectar
                )
                self._logger.info(f"GCSToBigQuery: {load_result}")

                # Guardar el resultado para el siguiente componente (si es necesario)
                self.setTaskVar('bigquery_load_result', load_result)

                # Opcionalmente eliminar el objeto de GCS
                if self.delete_gcs:
                    await conn.delete_gcs_object(
                        bucket_uri=self.bucket_uri
                    )
                    self._logger.info(f"GCSToBigQuery: Objeto GCS '{self.bucket_uri}' eliminado exitosamente.")

                return self.bucket_uri, "Carga exitosa en BigQuery."

        except ComponentError as ce:
            raise ce  # Re-lanzar errores específicos de componentes
        except Exception as e:
            raise ComponentError(f"GCSToBigQuery: Error durante la carga a BigQuery: {e}") from e

    async def close(self):
        """Cierra la conexión AsyncDB."""
        try:
            if self.bq:
                await self.bq.close()
                self._logger.info("GCSToBigQuery: AsyncDB cerrado exitosamente.")
        except Exception as e:
            self._logger.error(f"GCSToBigQuery: Error al cerrar AsyncDB: {e}")
