# src/common/expectations_utils.py
"""
Fábrica de Expectations para Lakeflow Spark Declarative Pipelines (SDP).

Genera dicts {nombre: condición_sql} compatibles con:
  - @dp.expect / @dp.expect (warn)
  - @dp.expect_or_drop / @dp.expect_or_drop (drop rows)
  - @dp.expect_or_fail / @dp.expect_or_fail (fail pipeline)
  - Parámetro expectations= en @dp.table / @dp.materialized_view

Uso:
    from dbx_elt_utils.expectations_utils import ExpectationsFactory as EF
    
    rules = EF.combine(
        EF.not_null('id', 'nombre'),
        EF.in_range('edad', 0, 150),
        EF.freshness('fecha_actualizacion', max_hours=48)
    )
    
    @dp.table(name='mi_tabla')
    @dp.expect_all_or_drop(rules)  # O usar individualmente
    def mi_tabla():
        ...
"""


class ExpectationsFactory:
    """Factory para generar expectations compatibles con SDP."""

    @staticmethod
    def not_null(*columns: str) -> dict:
        """Genera expectations de NOT NULL para una o más columnas.
        
        Ejemplo:
            EF.not_null('id', 'nombre') 
            -> {'not_null_id': 'id IS NOT NULL', 'not_null_nombre': 'nombre IS NOT NULL'}
        """
        return {f"not_null_{col}": f"{col} IS NOT NULL" for col in columns}

    @staticmethod
    def unique(column: str) -> dict:
        """Genera expectation de unicidad (count == 1 por valor).
        Nota: Esto es una validación semántica - SDP no soporta expectations de grupo nativamente.
        Se implementa como NOT NULL check + documentación de intención.
        
        Para unicidad real, usar dedup_by_key() de clean_utils antes de la tabla.
        """
        return {f"unique_{column}": f"{column} IS NOT NULL"}

    @staticmethod
    def in_range(column: str, min_val, max_val) -> dict:
        """Genera expectation de rango numérico.
        
        Ejemplo:
            EF.in_range('edad', 0, 150)
            -> {'range_edad': 'edad >= 0 AND edad <= 150'}
        """
        return {f"range_{column}": f"{column} >= {min_val} AND {column} <= {max_val}"}

    @staticmethod
    def in_set(column: str, valid_values: list) -> dict:
        """Genera expectation de pertenencia a un conjunto de valores.
        
        Ejemplo:
            EF.in_set('estado', ['ACTIVO', 'INACTIVO', 'PENDIENTE'])
            -> {'valid_estado': "estado IN ('ACTIVO', 'INACTIVO', 'PENDIENTE')"}
        """
        values_str = ", ".join([f"'{v}'" for v in valid_values])
        return {f"valid_{column}": f"{column} IN ({values_str})"}

    @staticmethod
    def freshness(column: str, max_hours: int = 24) -> dict:
        """Genera expectation de frescura temporal.
        Verifica que los datos no sean más antiguos que max_hours.
        
        Ejemplo:
            EF.freshness('last_updated', max_hours=48)
            -> {'freshness_last_updated': "last_updated >= current_timestamp() - INTERVAL 48 HOURS"}
        """
        return {
            f"freshness_{column}": f"{column} >= current_timestamp() - INTERVAL {max_hours} HOURS"
        }

    @staticmethod
    def regex_match(column: str, pattern: str, rule_name: str = None) -> dict:
        """Genera expectation de coincidencia con expresión regular.
        
        Ejemplo:
            EF.regex_match('email', r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$')
            -> {'regex_email': "email RLIKE '^[a-zA-Z0-9_.+-]+@...'"}
        """
        name = rule_name or f"regex_{column}"
        return {name: f"{column} RLIKE '{pattern}'"}

    @staticmethod
    def not_empty(*columns: str) -> dict:
        """Genera expectations de string no vacío (no null Y no '').
        
        Ejemplo:
            EF.not_empty('nombre', 'apellido')
            -> {'not_empty_nombre': "nombre IS NOT NULL AND trim(nombre) != ''"}
        """
        return {
            f"not_empty_{col}": f"{col} IS NOT NULL AND trim({col}) != ''" 
            for col in columns
        }

    @staticmethod
    def positive(*columns: str) -> dict:
        """Genera expectations de valor positivo (> 0).
        
        Ejemplo:
            EF.positive('monto', 'cantidad')
            -> {'positive_monto': 'monto > 0', 'positive_cantidad': 'cantidad > 0'}
        """
        return {f"positive_{col}": f"{col} > 0" for col in columns}

    @staticmethod
    def combine(*expectation_dicts: dict) -> dict:
        """Combina múltiples diccionarios de expectations en uno solo.
        
        Ejemplo:
            rules = EF.combine(
                EF.not_null('id'),
                EF.in_range('edad', 0, 150),
                EF.freshness('updated_at', 24)
            )
            # -> {'not_null_id': 'id IS NOT NULL', 'range_edad': '...', 'freshness_updated_at': '...'}
        """
        combined = {}
        for d in expectation_dicts:
            combined.update(d)
        return combined
