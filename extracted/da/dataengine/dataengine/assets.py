import os
from typing import List, Optional, Dict, Union
from marshmallow import Schema, fields, validates, post_load, ValidationError
from .utilities import general_utils


class AssetSchema(Schema):
    """
    Base Asset Schema.
    """
    asset_name = fields.Str(required=True)
    dirname = fields.Str(required=True)
    description = fields.Str()


class BaseDatasetSchema(AssetSchema):
    """
    Schema for BaseDataset class.
    """
    file_path = general_utils.StringOrListField(required=True)
    file_format = fields.Str(load_default="csv")
    separator = fields.String(load_default=",")
    location = fields.Str(load_default="local")
    bucket_asset_name = fields.Str()
    header = fields.Bool(load_default=True)
    schema = fields.Dict()
    options = fields.Dict()
    
    @validates("file_format")
    def validate_file_format(self, file_format, **kwargs):
        """
        Validate the input file format.
        """
        valid_args = ["csv", "parquet", "delta", "avro", "json"]
        if file_format not in valid_args:
            raise ValidationError(
                f"Invalid file_format '{file_format}' provided, "
                "please choose among the list: [{}]".format(
                    ", ".join(valid_args)))

    @validates("schema")
    def validate_schema(self, schema, **kwargs):
        """
        Validate the 'schema' field to ensure it's a dictionary of key-value
        pairs where both keys and values are strings.
        """
        if not isinstance(schema, dict):
            raise ValidationError("Schema must be a dictionary.")

        for key, value in schema.items():
            if not isinstance(key, str) or not isinstance(value, str):
                raise ValidationError(
                    "Schema keys and values must be strings.")
    
    @post_load
    def make_base_dataset(self, data, **kwargs):
        return BaseDataset(**data)


class BucketSchema(AssetSchema):
    """
    Schema for Bucket class.
    """
    bucket_name = fields.Str(required=True)
    access_key = fields.Str()
    secret_key = fields.Str()
    datasets = fields.List(fields.Nested(BaseDatasetSchema))
    
    @post_load
    def make_bucket(self, data, **kwargs):
        return Bucket(**data)
    
class Asset:
    """
    The Asset class will function as our parent class for all different types
    of assets.
    """
    def __init__(self, asset_name: str, dirname: str, description: str = None):
        self.asset_name = asset_name
        self.dirname = dirname
        self.description = description


# Forward declaration for type hinting
class Bucket(Asset):
    pass


class BaseDataset(Asset):
    """
    Base Dataset class.
    """
    def __init__(
            self,
            asset_name: str,
            dirname: str,
            file_path: Union[str, List[str]],
            file_format: str = "csv",
            separator: str = ",",
            location: str = "local",
            bucket_asset_name: str = None,
            header: bool = True,
            schema: Optional[Dict[str, str]] = None,
            options: Optional[Dict[str, str]] = {},
            **kwargs
    ):
        # Setup generic asset variables
        super().__init__(asset_name, dirname, description=kwargs.get("description"))
        # Setup filepath
        if isinstance(file_path, str):
            file_path = [file_path]
        self.file_path_list = file_path
        # Set base dataset parameters
        self.separator = separator
        self.file_format = file_format
        self.header = header
        self.schema = schema
        self.options = options
        # Override location to s3 if bucket name is provided
        self.bucket_asset_name = bucket_asset_name
        if self.bucket_asset_name:
            self.location = "s3"
        else:
            self.location = location
        # Get the relative normal path of for the local files
        if self.location == "local":
            self.file_path_list = [
                os.path.normpath(os.path.join(dirname, i))
                for i in self.file_path_list]
        # Initially, the dataset is not in any bucket
        self.bucket: Optional[Bucket] = None

    def set_bucket(self, bucket: Bucket):
        self.bucket = bucket

    def get_bucket_name(self):
        return self.bucket.bucket_name if self.bucket else "Unassigned"


class Bucket(Asset):
    """
    S3 Bucket class.
    """
    def __init__(
            self,
            asset_name: str,
            bucket_name: str,
            access_key: Optional[str] = None,
            secret_key: Optional[str] = None
    ):
        super().__init__(asset_name)
        self.bucket_name = bucket_name
        self.access_key = access_key
        self.secret_key = secret_key
        self.datasets: List[BaseDataset] = []

    def add_dataset(self, dataset: BaseDataset):
        self.datasets.append(dataset)
        dataset.set_bucket(self)  # Set the parent bucket of the dataset

    def get_dataset(self, s3_prefix: str):
        for dataset in self.datasets:
            if dataset.s3_prefix == s3_prefix:
                return dataset
        return None
