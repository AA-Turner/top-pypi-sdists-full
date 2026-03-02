@transformation_group(name="{{ project_name }}")
def transformations() -> List[Any]:
    #  Transformations will be executed in order
    return [prepare_active_load_ids, {{ transformations }}, update_processed_load_ids]
