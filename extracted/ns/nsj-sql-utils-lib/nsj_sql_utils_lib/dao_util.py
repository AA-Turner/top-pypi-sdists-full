def make_sql_fields(fields: list[str], alias: str = None) -> str:
    """
    Returns a list of fields to build select queries (in string, with comma separator)
    """

    # Building SQL fields
    if alias is not None:
        fields = [f"{alias}.{k}" for k in fields]
    else:
        fields = [f"{k}" for k in fields]

    return ", ".join(fields)

  

def make_sql_insert_fields_values(fields: list[str], psycopg2: bool = False) -> str:
    """
    Retorna uma tupla com duas partes: (sql_fields, sql_ref_values), onde:
    - sql_fields: Lista de campos a inserir no insert
    - sql_ref_values: Lista das referências aos campos, a inserir no insert (parte values)
    """

    # Building SQL fields
    fields = [f"{k}" for k in fields]
    if psycopg2:
        ref_values = [f"%({k})s" for k in fields]
    else:
        ref_values = [f":{k}" for k in fields]

    return (", ".join(fields), ", ".join(ref_values))
