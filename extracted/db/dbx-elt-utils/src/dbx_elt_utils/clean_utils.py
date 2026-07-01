# src/common/clean_utils.py
from pyspark.sql import DataFrame
from pyspark.sql.functions import (
    regexp_replace, col, trim, when, lower, sha2, concat_ws,
    row_number, split, transform, expr
)
from pyspark.sql.window import Window


def extraer_valor_array_string(columna):
    """
    Limpia columnas que vienen con formato de array JSON string.
    Ejemplo: '["12.345.678-9"]' -> '12.345.678-9'
    Ejemplo: '[]' -> NULL
    """
    c = regexp_replace(columna, r'[\["\]]', "")
    return when(trim(c) == "", None).otherwise(trim(c))


def parse_json_array_column(columna):
    """
    Versión mejorada de extraer_valor_array_string.
    Convierte '["a","b","c"]' en un array real de Spark: array('a', 'b', 'c').
    Retorna NULL para arrays vacíos '[]'.
    """
    # Quitar corchetes exteriores
    stripped = regexp_replace(columna, r'^\[|\]$', '')
    # Si queda vacío -> NULL
    cleaned = when(trim(stripped) == "", None).otherwise(stripped)
    # Quitar comillas y separar por coma
    no_quotes = regexp_replace(cleaned, '"', '')
    return when(no_quotes.isNull(), None).otherwise(
        transform(split(no_quotes, ","), lambda x: trim(x))
    )


def normalize_string(columna):
    """
    Normaliza strings: trim + lowercase + remover acentos + colapsar espacios múltiples.
    Ejemplo: '  María  Del   CARMEN  ' -> 'maria del carmen'
    """
    # Trim + lower
    c = lower(trim(columna))
    # Remover acentos comunes (español/portugués)
    accents_from = "áéíóúàèìòùäëïöüâêîôûãõÁÉÍÓÚÀÈÌÒÙÄËÏÖÜÂÊÎÔÛÃÕ"
    accents_to   = "aeiouaeiouaeiouaeiouaoAEIOUAEIOUAEIOUAEIOUAO"
    c = expr(f"translate({c._jc.toString()}, '{accents_from}', '{accents_to}')")
    # Colapsar espacios múltiples
    c = regexp_replace(c, r'\s+', ' ')
    return trim(c)


def safe_cast(columna, target_type: str):
    """
    Cast seguro que retorna NULL en vez de error si la conversión falla.
    Usa try_cast nativo de Spark SQL.
    
    Args:
        columna: Columna de PySpark
        target_type: Tipo destino ('int', 'double', 'date', 'timestamp', 'long', 'float')
    
    Ejemplo: safe_cast(col('precio'), 'double') -> NULL si 'abc', 123.45 si '123.45'
    """
    return expr(f"try_cast({columna._jc.toString()} as {target_type})")


def dedup_by_key(df: DataFrame, key_cols: list, order_col: str, ascending: bool = False) -> DataFrame:
    """
    Deduplica un DataFrame quedando con la fila más reciente (o antigua) por clave.
    Usa Window function con row_number.
    
    Args:
        df: DataFrame de entrada
        key_cols: Lista de columnas que forman la clave única (['id', 'source'])
        order_col: Columna de ordenamiento (ej: 'updated_at', '_ingested_at')
        ascending: True = quedarse con el más antiguo, False = más reciente (default)
    
    Returns:
        DataFrame deduplicado
    """
    order_expr = col(order_col).asc() if ascending else col(order_col).desc()
    window = Window.partitionBy([col(k) for k in key_cols]).orderBy(order_expr)
    return (
        df.withColumn("_row_num", row_number().over(window))
          .filter(col("_row_num") == 1)
          .drop("_row_num")
    )


def add_surrogate_key(df: DataFrame, columns: list, key_name: str = "_surrogate_key") -> DataFrame:
    """
    Genera una clave surrogada SHA-256 a partir de la concatenación de columnas.
    
    Args:
        df: DataFrame de entrada
        columns: Lista de nombres de columna para el hash (['id', 'source', 'version'])
        key_name: Nombre de la columna resultante (default: '_surrogate_key')
    
    Returns:
        DataFrame con columna de clave surrogada agregada
    """
    return df.withColumn(
        key_name,
        sha2(concat_ws("|", *[col(c).cast("string") for c in columns]), 256)
    )
