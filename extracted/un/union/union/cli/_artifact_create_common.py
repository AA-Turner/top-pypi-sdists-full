import datetime
import typing
from typing import ClassVar, Tuple

import rich_click as click
from flytekit import BlobType, FlyteContext, Literal, StructuredDataset
from flytekit import LiteralType as lt
from flytekit.extend import TypeEngine
from flytekit.interaction import click_types
from flytekit.models.types import LiteralType, StructuredDatasetType
from flytekit.models.types import SimpleType as st
from flytekit.types.directory import FlyteDirectory
from flytekit.types.file import FlyteFile

from union.cli._common import CommandBase


class ArtifactCreateCommand(CommandBase):
    """
    This is a Command class for creating an artifact. This adds parameters for various artifact types,
    using flytekit's click types.

    TODO we have to add support for collections.
    """

    _ARTIFACT_FOR_TYPES: ClassVar = [
        {
            "param_name": "from_float",
            "description_extra": " (float)",
            "literal_type": lt(simple=st.FLOAT),
            "default_python_type": float,
        },
        {
            "param_name": "from_int",
            "description_extra": " (int)",
            "literal_type": lt(simple=st.INTEGER),
            "default_python_type": int,
        },
        {
            "param_name": "from_str",
            "description_extra": " (str)",
            "literal_type": lt(simple=st.STRING),
            "default_python_type": str,
        },
        {
            "param_name": "from_bool",
            "description_extra": " (bool)",
            "literal_type": lt(simple=st.BOOLEAN),
            "default_python_type": bool,
        },
        {
            "param_name": "from_datetime",
            "description_extra": " (datetime)",
            "literal_type": lt(simple=st.DATETIME),
            "default_python_type": datetime.datetime,
        },
        {
            "param_name": "from_duration",
            "description_extra": " (duration)",
            "literal_type": lt(simple=st.DURATION),
            "default_python_type": datetime.timedelta,
        },
        {
            "param_name": "from_json",
            "description_extra": " (struct)",
            "literal_type": lt(simple=st.STRUCT),
            "default_python_type": dict,
        },
        {
            "param_name": "from_dataframe",
            "description_extra": " (parquet)",
            "literal_type": lt(structured_dataset_type=StructuredDatasetType()),
            "default_python_type": StructuredDataset,
        },
        {
            "param_name": "from_file",
            "description_extra": " (file)",
            "literal_type": lt(blob=BlobType(dimensionality=BlobType.BlobDimensionality.SINGLE, format="")),
            "default_python_type": FlyteFile,
        },
        {
            "param_name": "from_dir",
            "description_extra": " (dir)",
            "literal_type": lt(blob=BlobType(dimensionality=BlobType.BlobDimensionality.MULTIPART, format="")),
            "default_python_type": FlyteDirectory,
        },
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.params.extend(self._create_options())

    @classmethod
    def _create_options(cls) -> typing.List[click.Option]:
        options = []
        for v in cls._ARTIFACT_FOR_TYPES:
            ct = click_types.literal_type_to_click_type(v["literal_type"], v["default_python_type"])
            options.append(
                click.Option(
                    param_decls=[f"--{v['param_name']}"],
                    type=ct,
                    required=False,
                    help=f"Create an artifact of type {v['description_extra']}",
                )
            )
        return options

    @classmethod
    def get_literal_from_args(
        cls, flyte_ctx: FlyteContext, args: typing.Dict[str, typing.Any]
    ) -> Tuple[Literal, LiteralType]:
        for v in cls._ARTIFACT_FOR_TYPES:
            param_name = v["param_name"]
            if param_name in args:
                if args[param_name] is not None:
                    val = args[param_name]
                    lt = v["literal_type"]
                    # TODO this is a hack, need help to set the remote directory to None
                    # I think the click_types has a bug for Directory type
                    if isinstance(val, FlyteDirectory):
                        val._remote_directory = None
                    lit = TypeEngine.to_literal(flyte_ctx, val, v["default_python_type"], lt)
                    return lit.to_flyte_idl(), lt.to_flyte_idl()
        raise click.BadParameter("Artifact should be of one of the supported types, `--from_*`")
