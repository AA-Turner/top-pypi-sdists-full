import os
import datetime
import string
from marshmallow import Schema, fields, post_load, validates, ValidationError
from dataengine import dataset
from .assets import AssetSchema, Asset
from .utilities import general_utils


class SingleOrListField(fields.Field):
    def __init__(self, cls_or_instance, **kwargs):
        super().__init__(**kwargs)
        # Ensure the inner field is always a list of nested fields
        if isinstance(cls_or_instance, fields.Field):
            self.inner_field = fields.List(cls_or_instance)
        else:
            # This assumes cls_or_instance is a Schema class or an instance of a Schema
            self.inner_field = fields.List(fields.Nested(cls_or_instance))

    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, dict):
            value = [value]  # Convert dict to list if not already a list
        return self.inner_field.deserialize(value, attr, data)


class MyFormatter(string.Formatter):
    """
    Custom formatter class from stackoverflow.com/questions/17215400
    """
    def __init__(self, default='{{{0}}}'):
        self.default = default

    def get_value(self, key, args, kwds):
        if isinstance(key, str):
            return kwds.get(key, self.default.format(key))
        else:
            return string.Formatter.get_value(key, args, kwds)


class IntermittentTablesSchema(Schema):
    """
    Schema for specifying the SQL statement information.
    """
    table_name = fields.String(required=True)
    filename = fields.String(required=True)
    format_args = fields.Dict()

    @validates("filename")
    def validate_filename(self, filename, **kwargs):
        """
        Validate the SQL filepath by checking whether it exists.
        """
        if not os.path.exists(filename):
            raise ValidationError(f"Invalid filename provided: {filename}")


class SqlInfoSchema(Schema):
    """
    Schema for specifying the SQL statement information.
    """
    filename = general_utils.StringOrListField(required=True)
    format_args = fields.Dict()
    intermittent_tables = fields.List(fields.Nested(IntermittentTablesSchema))

    @validates("filename")
    def validate_filename(self, filename, **kwargs):
        """
        Validate the SQL filepath by checking whether it exists.
        """
        # Setup file list
        if isinstance(filename, str):
            file_list = [filename]
        else:
            file_list = filename
        # Validate each SQL file provided
        for file_path in file_list:
            if not os.path.exists(file_path):
                raise ValidationError(
                    f"Invalid filename provided: {file_path}")


class DependencySchema(Schema):
    """
    Schema for specifying the dependencies of the Query object.
    """
    table_name = fields.String()
    base_dataset = fields.String(required=True)
    format_args = fields.Dict()
    time_delta = fields.Nested(dataset.TimeDeltaSchema)
    timestamp_conversion = fields.List(
        fields.Nested(dataset.TimestampConversionSchema))
    dt_delta = fields.Nested(dataset.DtDeltaSchema)
    exclude_hours = fields.List(fields.String())
    check_path = fields.Boolean(load_default=True)


class DeleteInfoSchema(Schema):
    """
    Schema for specifying the database table delete parameters.
    """
    delete_all = fields.Boolean()
    days = fields.Integer()
    column_header = fields.String()


class LoadInfoSchema(Schema):
    """
    Schema for specifying the database load information.
    """
    # TODO: Validate load location using assets
    load_location = fields.String(required=True)
    db_arg = fields.String(required=True)
    table_name = fields.String(required=True)
    delete_info = fields.Nested(DeleteInfoSchema)
    replace = fields.Boolean()
    truncate = fields.Boolean(load_default=False)


class DistinctVariableSchema(Schema):
    """
    Distinct Variable marshallow validation schema.
    """
    variable_name = fields.String(required=True)
    table_name = fields.String(required=True)
    column_header = fields.String(required=True)
    lower = fields.Boolean()


class ReplaceWhereSchema(Schema):
    """
    Delta Replace Where arguments for the s3 write.
    """
    column_header = fields.String(required=True)
    column_value = fields.String(required=True)


class Repartition(Schema):
    """
    Spark repartition arguments.
    """
    n_partitions = fields.Integer()
    column_headers = fields.List(fields.String())


class BaseQuerySchema(AssetSchema):
    """
    Query marshmallow validation schema.
    """
    sql_info = SingleOrListField(SqlInfoSchema, required=True)
    # TODO: Move ouput arguments to Nested schema
    output = fields.String(required=True)
    file_format = fields.String()
    separator = fields.String()
    use_pandas = fields.Boolean()
    header = fields.Boolean()
    partition_by = fields.List(fields.String())
    repartition = fields.Nested(Repartition)
    replace_where = fields.List(fields.Nested(ReplaceWhereSchema))
    mode = fields.String()
    max_records_per_file = fields.Integer()
    exact_records_per_file = fields.Integer()
    # Setup nested schemas for dependencies, load, and delete information
    dependencies = fields.List(fields.Nested(DependencySchema), required=True)
    load_info = fields.Nested(LoadInfoSchema)
    # Setup distict column values variables
    distinct_variables = fields.List(fields.Nested(DistinctVariableSchema))
    # Allow the user to specify a AWS Glue Crawler to run after the query
    crawler_name = fields.String()

    @post_load
    def create_query(self, input_data, **kwargs):
        return BaseQuery(**input_data)

    @validates("mode")
    def validate_mode(self, mode, **kwargs):
        valid_args = ["overwrite", "append"]
        if mode not in valid_args:
            raise ValidationError(
                f"Invalid mode '{mode}' provided, "
                "please choose among the list: [{}]".format(
                    ", ".join(valid_args)))


# Query Schema with dt and hour fields
class QuerySchema(BaseQuerySchema):
    dt = fields.DateTime()
    hour = fields.String()

    @post_load
    def create_query(self, input_data, **kwargs):
        return Query(**input_data)


# Base Query Class (simple, only stores fields)
class BaseQuery(Asset):
    def __init__(
        self, asset_name, dirname, sql_info, output, dependencies, load_info={},
        file_format="csv", separator=",", header=True, use_pandas=False,
        partition_by=[], repartition={}, replace_where=[],
        distinct_variables=[], mode="overwrite",
        max_records_per_file=None, exact_records_per_file=None,
        crawler_name=None, **kwargs
    ):
        # Setup generic asset variables
        super().__init__(asset_name, dirname, description=kwargs.get("description"))
        # Setup base query parameters
        self.sql_info = sql_info
        self.output = output
        self.file_format = file_format
        self.separator = separator
        self.use_pandas = use_pandas
        self.header = header
        self.dependencies = dependencies
        self.load_info = load_info
        self.partition_by = partition_by
        self.repartition = repartition
        self.replace_where = replace_where
        self.distinct_variables = distinct_variables
        self.mode = mode
        self.max_records_per_file = max_records_per_file
        self.exact_records_per_file = exact_records_per_file
        self.crawler_name = crawler_name


class Query(BaseQuery):
    """
    Query class.
    """
    def __init__(
            self,
            # BaseQuery fields
            asset_name, dirname, sql_info, output, dependencies, load_info={},
            file_format="csv", separator=",", header=True, use_pandas=False,
            partition_by=[], repartition={}, replace_where=[],
            distinct_variables=[], mode="overwrite",
            max_records_per_file=None, exact_records_per_file=None,
            crawler_name=None,
            # Additional Query specific fields
            dt=datetime.datetime.utcnow(), hour="*",
            **kwargs
        ):
        """
            Query constructor.
        """
        # Format date and hour strings
        date_str = str(dt.date())
        if hour == "*":
            dt_str = str(dt)
        else:
            dt_str = str(datetime.datetime(
                dt.year, dt.month, dt.day, int(hour)))
        # Call the BaseQuery constructor to initialize shared attributes
        super().__init__(
            asset_name=asset_name,
            dirname=dirname,
            sql_info=sql_info,
            output=output,
            dependencies=dependencies,
            load_info=load_info,
            file_format=file_format,
            separator=separator,
            header=header,
            use_pandas=use_pandas,
            partition_by=partition_by,
            repartition=repartition,
            replace_where=replace_where,
            distinct_variables=distinct_variables,
            mode=mode,
            max_records_per_file=max_records_per_file,
            exact_records_per_file=exact_records_per_file,
            crawler_name=crawler_name,
            **kwargs
        )
        # Include timestamp formating information in the output path
        self.output = self.output.format(
            dt=dt, date_str=date_str, hour=hour)
        # Setup replace where
        if self.replace_where:
            self.replace_where = self._setup_replace_where(
                self.replace_where, date_str, dt_str)
        # Setup sql arguments
        self.intermittent_tables = []
        self.sql = self._setup_sql_arguments(
            self.sql_info, dt, date_str, dt_str, hour)

    @classmethod
    def from_base_query(cls, base_query, **additional_fields):
        # Create a new Dataset instance using attributes from base_dataset
        # and any additional fields specific to Dataset
        return cls(
            base_query.asset_name, base_query.dirname,
            base_query.sql_info, base_query.output, base_query.dependencies,
            base_query.load_info, base_query.file_format,
            base_query.separator, base_query.header,
            base_query.use_pandas, base_query.partition_by,
            base_query.repartition, base_query.replace_where,
            base_query.distinct_variables, base_query.mode,
            base_query.max_records_per_file, base_query.exact_records_per_file,
            base_query.crawler_name, **additional_fields)

    def _setup_sql_arguments(self, sql_info, dt, date_str, dt_str, hour):
        """
        This method will setup the primary sql statement for the query.
        """
        self.file_path_list = []
        sql_list = []
        # If sql_info isn't a list make it a list
        if not isinstance(sql_info, list):
            sql_info = [sql_info]
        # Iterate over each set and setup the corresponding information
        sql_list = []
        for values in sql_info:
            # Add formatted sql to sql list
            sql_list.append(self._load_sql(
                dt, date_str, dt_str, hour,
                [values["filename"]] if isinstance(values["filename"], str) else values["filename"],
                values["format_args"] if "format_args" in values else {}))
            # TODO: Update intermittent tables to be outside of sql_info object
            # Setup intermittent tables if provided
            if "intermittent_tables" in values:
                self.intermittent_tables = values["intermittent_tables"]
                for index, value in enumerate(self.intermittent_tables):
                    self.intermittent_tables[index]["sql"] = self._load_sql(
                        dt, date_str, dt_str, hour, [value["filename"]],
                        format_args=value["format_args"] if "format_args" in value else {})

        return "\n\nUNION ALL\n\n".join(sql_list)

    def _load_sql(self, dt, date_str, dt_str, hour, file_path_list, format_args):
        """
        This method will load the query and format all arguments.
        TODO: Remove this once setup function is working as expected

        Args:
            base_dir (str): base file directory
            dt (datetime.datetime): date information
            hour (Union[str|int]): hour information
            file_path_list (list): list of relative file paths
            format_args (dict): extra string formating args for query

        Returns:
            query string
        """
        sql_list = []
        for file_path in file_path_list:
            # Read sql from file and format string
            query = open(file_path, "r").read()
            # Format string using custom formatter
            fmt = MyFormatter()
            query = fmt.format(
                query, dt=dt, date_str=date_str, dt_str=dt_str, hour=hour,
                **format_args)
            # Append to list
            sql_list.append(query)

        return "\n\nUNION ALL\n\n".join(sql_list)

    def _setup_replace_where(self, replace_where, date_str, dt_str):
        """
        This method will setup the delta replace where argument.

        Args:
            replace_where (list): replace where arguments
            date_str (str): date string
            dt_str (str): datetime string

        Returns:
            formatted replace_where arguments
        """
        formatted_replace_where = []
        for key_value_pair in replace_where:
            formatted_replace_where.append(
                "{column_header} == '{column_value}'".format(
                    column_header=key_value_pair["column_header"],
                    column_value=key_value_pair["column_value"].format(
                        date_str=date_str, dt_str=dt_str)))

        return formatted_replace_where
