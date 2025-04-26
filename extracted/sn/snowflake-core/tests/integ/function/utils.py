from snowflake.core.function import FunctionArgument, ServiceFunction


def create_service_function(
        name,
        arg_types,
        returns,
        endpoint,
        temp_service,
        functions
        ):
    return functions.create(
        ServiceFunction(
            name=name,
            arguments=[
                FunctionArgument(name=f"v_{str(i)}", datatype=v)
                    for i , v in enumerate(arg_types)
            ],
            returns=returns,
            service=temp_service,
            endpoint=endpoint,
            path="/path/to/myapp",
            max_batch_rows=5,
            )
    )
