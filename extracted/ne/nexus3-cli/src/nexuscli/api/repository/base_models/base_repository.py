import nexuscli  # noqa: F401; for mypy
from nexuscli.api.base_model import BaseModel

DEFAULT_BLOB_STORE_NAME = 'default'
DEFAULT_STRICT_CONTENT = False


class BaseRepository(BaseModel):
    """
    The base class for Nexus repositories.

    :param name: name of the repository.
    :param recipe: format (recipe) of the new repository. Must be one of
        :py:attr:`RECIPES`. See Nexus documentation for details.
    :type recipe: str
    :param blob_store_name: name of an existing blob store; 'default'
        should work on most installations.
    :type blob_store_name: str
    :param strict_content_type_validation: Whether to validate file
        extension against its content type.
    :type strict_content_type_validation: bool
    """
    TYPE = None
    """The repository type supported by this class"""
    RECIPE_NAME = None
    """If a recipe is not given during initialisation, use this one as the default"""

    def __init__(self, *args, **kwargs):
        self.blob_store_name: str = kwargs.get('blob_store_name', DEFAULT_BLOB_STORE_NAME)
        self.strict_content: bool = kwargs.get(
            'strict_content_type_validation', DEFAULT_STRICT_CONTENT)

        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f'{self.__class__.__name__}-{self.name}'

    def _validate_params(self) -> None:
        super()._validate_params()

    @property
    def recipe_name(self):
        """
        The nexus3-cli name for this repository's recipe (format). This is almost
        always the same as :attr:`RECIPE_NAME` with ``maven`` being the notable
        exception.
        """
        return self.RECIPE_NAME
