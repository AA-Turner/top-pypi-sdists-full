import os
import logging
import datetime
from marshmallow import Schema, fields, post_load, validates, ValidationError
import pandas as pd
from .utilities import s3_utils, spark_utils, general_utils
from .assets import BaseDatasetSchema, BaseDataset

S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY")


class TimeDeltaSchema(Schema):
    """
    Schema for specifying the time delta.
    """
    days = fields.Integer()
    hours = fields.Integer()
    weeks = fields.Integer()


class DtDeltaSchema(TimeDeltaSchema):
    """
    Schema for specifying the dt rolling or latest time delta.
    """
    delta_type = fields.String()

    @validates("delta_type")
    def validate_delta_type(self, delta_type, **kwargs):
        valid_args = ["latest", "rolling"]
        if delta_type not in valid_args:
            raise ValidationError(
                f"Invalid delta_type '{delta_type}' provided, "
                "please choose among the list: [{}]".format(
                    ", ".join(valid_args)))


class TimestampConversionSchema(Schema):
    """
    Schema for specifying timestamp conversion parameters.
    """
    column_header = fields.String(required=True)
    # Will default to UTC if not provided
    timezone = fields.String()
    # Will default to column_header
    new_column_header = fields.String()


class DatasetSchema(BaseDatasetSchema):
    """
        Dataset marshmallow validation schema.
    """
    # TODO: Phase out required fields
    spark = fields.Raw(required=True)
    dt = fields.DateTime(required=True)
    hour = fields.String(required=True)
    bucket = fields.String(required=True)
    format_args = fields.Dict()
    time_delta = fields.Nested(TimeDeltaSchema)
    timestamp_conversion = fields.List(
        fields.Nested(TimestampConversionSchema))
    dt_delta = fields.Nested(DtDeltaSchema)
    exclude_hours = fields.List(fields.String())
    rename = fields.Dict()
    check_path = fields.Boolean(load_default=True)

    @post_load
    def make_dataset(self, data, **kwargs):
        return Dataset(**data)


class Dataset(BaseDataset):
    """
    Dataset class.
    """

    def __init__(
            self,
            # BaseDataset fields
            asset_name, dirname, file_path, file_format="csv", separator=",",
            location="local", bucket_asset_name=None, header=True,
            schema=None, options={},
            # Additional Dataset specific fields
            spark=None, dt=datetime.datetime.utcnow(), hour="*",
            bucket=None, format_args={},
            time_delta={"days": 0, "hours": 0, "weeks": 0},
            timestamp_conversion=[], dt_delta={}, exclude_hours=[],
            rename={}, check_path=True, **kwargs
        ):
        """
        Dataset constructor.
        """
        # Setup BaseDataset arguments
        super().__init__(
            asset_name, dirname, file_path, file_format, separator, location,
            bucket_asset_name, header, schema, options)
        # Setup additional Dataset arguments
        self.spark = spark
        # Extract string formatting variables from file path
        string_formatting_vars = set.union(*map(set, [
            general_utils.extract_formatting_variables(path)
            for path in self.file_path_list]))
        # Update format args with missing string formatting variables
        for variable in string_formatting_vars:
            if (
                (variable not in format_args) and
                (variable not in (
                    "dt", "date_str", "dt_m1", "dt_p1", "hour", "lz_hour",
                    "bucket"
                ))
            ):
                format_args[variable] = "*"
        # Get all unique permutations of the format arguments
        format_args_permutations = general_utils.get_dict_permutations(
            format_args)
        # Load data from s3 if that is what the location is set to
        if location == "s3":
            self.file_path_list = self._setup_s3_path(
                self.file_path_list, dt, hour, time_delta, bucket, 
                format_args_permutations, dt_delta, exclude_hours,
                check_path)
            # If basePath option is provided add bucket to string formatting
            if "basePath" in options:
                options["basePath"] = options["basePath"].format(
                    bucket=bucket)
            # Load data into a pyspark DataFrame
            self.df = self._load_data_from_s3(
                schema, file_format, separator, header, rename=rename,
                options=options)
            # Convert timestamp if applicable
            if timestamp_conversion:
                for params in timestamp_conversion:
                    self.df = spark_utils.convert_timestamp(self.df, **params)
        # Otherwise assume the data is a local csv file
        else:
            self.df = spark_utils.pandas_to_spark(
                spark, pd.concat(
                    [pd.read_csv(path) for path in self.file_path_list],
                    ignore_index=True))
    
    @classmethod
    def from_base_dataset(cls, base_dataset, **additional_fields):
        # Create a new Dataset instance using attributes from base_dataset
        # and any additional fields specific to Dataset
        return cls(
            base_dataset.asset_name, base_dataset.dirname,
            base_dataset.file_path_list, base_dataset.file_format,
            base_dataset.separator, base_dataset.location,
            base_dataset.bucket_asset_name, base_dataset.header,
            base_dataset.schema, base_dataset.options, **additional_fields)

    def _setup_s3_path(
            self, s3_path, dt, hour, time_delta, bucket, format_args,
            dt_delta, exclude_hours, check_path):
        """
        This method will setup the s3 path for the dataset.

        Args:
            s3_path (str): input s3 path
            dt (datetime.datetime): datetime object
            hour (int|str): input hour
            bucket (str): bucket name
            format_args (list): list of unique format argument dicts
            dt_delta (dict): either rolling or latest day / hour range

        Returns:
            final dataset s3 path
        """
        dataset_s3_path_list = []
        # Apply time delta and modify dt and hour
        dt, hour = general_utils.apply_time_delta(dt, hour, time_delta)
        # Iterate over each path and format accordingly
        for path in s3_path:
            # Iterate over each unique set of format arguments
            for unique_format_args in format_args:
                if (
                    not dt_delta or
                    (dt_delta and dt_delta["delta_type"] == "rolling")
                ):
                    # Default input days to 0
                    input_days = 0
                    input_weeks = 0
                    # Setup input hour based on hour variable
                    if hour == "*":
                        input_hours = hour
                    else:
                        input_hours = 1
                    # Override values depending on dt_delta
                    if dt_delta and (dt_delta["delta_type"] == "rolling"):
                        if "days" in dt_delta:
                            input_days = dt_delta["days"]
                        if "hours" in dt_delta:
                            input_hours = dt_delta["hours"]
                        if "weeks" in dt_delta:
                            input_weeks = dt_delta["weeks"]
                    # Get dt range given assembled arguments
                    if hour == "*":
                        dt_range = general_utils.get_dt_range(
                            dt, days=input_days, hours=input_hours,
                            weeks=input_weeks)
                    else:
                        dt_range = general_utils.get_dt_range(
                            datetime.datetime(
                                dt.year, dt.month, dt.day, hour=int(hour)),
                            days=input_days, hours=input_hours,
                            weeks=input_weeks)
                    # Exclude hours
                    if exclude_hours:
                        dt_range = general_utils.exclude_hours_from_range(
                            dt_range, exclude_hours)
                    # Assemble list of valid s3 paths
                    for dt_object in dt_range:
                        dt_path = path.format(
                            date_str=dt.date(), dt=dt_object,
                            dt_m1=dt_object - datetime.timedelta(days=1),
                            dt_p1=dt_object + datetime.timedelta(days=1),
                            hour=dt_object.hour,
                            lz_hour=general_utils.leading_zero(dt_object.hour),
                            bucket=bucket, **unique_format_args)
                        # If the check_path field is True then make sure the
                        # path exists before attempting to load it.
                        # Note: this is optional in case keys or iam role
                        # don't have read access to the bucket for any reason
                        exist_status = True
                        if check_path:
                            # TODO: Update this once bucket asset is setup properly
                            if bucket in dt_path:
                                exist_status = s3_utils.check_s3_path(
                                    S3_ACCESS_KEY, S3_SECRET_KEY, dt_path, bucket)
                            else:
                                # Assume we are using IAM role to read
                                exist_status = s3_utils.check_s3_path(
                                    None, None, *s3_utils.parse_url(dt_path))
                        # Verify whether path exists if bucket matches and is
                        # new then append
                        if (
                            exist_status and
                            (dt_path not in dataset_s3_path_list)
                        ):
                            dataset_s3_path_list.append(dt_path)
                # Otherwise, get latest valid path
                elif dt_delta["delta_type"] == "latest":
                    dataset_s3_path_list += s3_utils.find_latest_s3_path(
                        path, dt, hour, format_args=unique_format_args,
                        bucket=bucket if "{bucket}" in path else None,
                        **{
                            key: value for key, value in dt_delta.items()
                            if key in ["days", "hours"]},
                        aws_access_key=S3_ACCESS_KEY, aws_secret_key=S3_SECRET_KEY)
                else:
                    logging.error("Invalid dt_delta arguments provided.\n")

        return dataset_s3_path_list


    def _load_data_from_s3(
            self, schema, file_format, separator, header, rename={},
            options={}):
        """
        This method will load the dataset into a pyspark DataFrame object
        and set corresponding meta data.

        Returns:
            pyspark DataFrame
        """
        # Explicitely raise exception if no valid files were found
        if not self.file_path_list:
            logging.error("No valid data located.\n")
            raise Exception
        # Otherwise attempt to load data
        if file_format == "csv":
            df = self.spark.read.load(
                self.file_path_list, format=file_format, sep=separator,
                header=header, schema=spark_utils.create_spark_schema(
                    schema.keys(), schema.values()))
        elif file_format in ("parquet", "delta", "avro"):
            # TODO: Remove this once the datasets that need it have it added
            # to their definition
            # Add merge schema as default value
            if "mergeSchema" not in options:
                options["mergeSchema"] = True
            # Load data provided options dict
            df = self.spark.read.format(file_format).options(
                **options).load(self.file_path_list)
        elif file_format == "json":
            df = self.spark.read.json(self.file_path_list)
        # Rename columns if applicable
        if rename:
            df = spark_utils.rename_cols(self.df, rename)

        return df
