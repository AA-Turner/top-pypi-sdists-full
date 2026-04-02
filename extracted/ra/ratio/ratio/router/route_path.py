from ratio.router.route_type import RouteType
from ratio.router.exceptions import InvalidRouteError
import re
import pathlib

ROUTE_ALLOWED_CHARACTERS = r"^[A-Za-z0-9_\/\[\]]+$"
DIRECT_ROUTE_ALLOWED_CHARACTERS = r"^[A-Za-z0-9_\/]+$"
DYNAMIC_ROUTE_KEY_ALLOWED_CHARACTERS = r"[A-Za-z0-9_]+"
DYNAMIC_PATH_PARAMETER_REGEX = r"\[([A-Za-z0-9_]+?)]"
INVALID_DYNAMIC_PARAMETER_REGEX = r"(.*?)\[([^A-Za-z0-9_]+)](.*?)$"

# The minimum amount of slashes needed for a nested route
# e.g. /test/ is not nested, while /test/something/ is
MINIMUM_SEPARATORS_FOR_NESTED_ROUTE = 3


class RoutePath:
    __path: str

    def __init__(self, path: str):
        if path == "/":
            path = "/index"
        self.__path = path
        self.assert_is_valid()

    def __str__(self) -> str:
        return self.__path

    @classmethod
    def from_path(cls, path: pathlib.Path) -> "RoutePath":
        return cls("/" + str(path))

    @property
    def route_type(self) -> RouteType:
        if len(self.parameter_keys) == 0:
            return RouteType.DIRECT

        return RouteType.DYNAMIC

    def assert_is_valid(self) -> None:
        if not self.__path.startswith("/"):
            raise InvalidRouteError(
                "A route path should start with `/`, indicating the project root."
            )

        if self.__path.endswith("/"):
            raise InvalidRouteError(
                "A route path must refer to a file, not a directory. It may not end with `/`."
            )

        if not re.match(ROUTE_ALLOWED_CHARACTERS, self.__path):
            raise InvalidRouteError(
                "Routes may only contain underscores, alphanumerical characters and `/`."
            )

        if self.route_type == RouteType.DIRECT:
            if not re.match(DIRECT_ROUTE_ALLOWED_CHARACTERS, self.__path):
                raise InvalidRouteError("Your route contains invalid characters")

            return

        # If a dynamic parameter key appears twice, a route is invalid
        if len(set(self.parameter_keys)) != len(self.parameter_keys):
            raise InvalidRouteError(
                "A dynamic route should contain unique parameter keys."
            )

        # If a route is not matched against a direct route after removing all dynamic parameter keys
        # it is invalid, because it contains invalid characters after removing parameters.
        route_without_dynamic_parameters = re.sub(
            DYNAMIC_PATH_PARAMETER_REGEX, "", self.__path
        )

        if (
            re.match(DIRECT_ROUTE_ALLOWED_CHARACTERS, route_without_dynamic_parameters)
            is None
        ):
            raise InvalidRouteError(
                "Some parameters are specified incorrectly. Make sure you close your brackets appropriately."
            )

        # For intuitive custom error routes to work, we cannot have `/[id]` as route.
        if (
            len(self.parameter_keys) == 1
            and len(self.__path.split("/")) < MINIMUM_SEPARATORS_FOR_NESTED_ROUTE
        ):
            raise InvalidRouteError("Top-level dynamic routes are not allowed.")

    @property
    def parameter_keys(self) -> list[str]:
        return re.findall(DYNAMIC_PATH_PARAMETER_REGEX, self.__path)

    def as_simple_regex(self) -> str:
        if self.route_type == RouteType.DIRECT:
            return self.__path

        regex = self.__path

        for parameter in self.parameter_keys:
            regex = re.sub(
                rf"/\[{parameter}\]",
                f"/({DYNAMIC_ROUTE_KEY_ALLOWED_CHARACTERS})",
                regex,
            )

        return regex

    def as_regex(self) -> str:
        if self.route_type == RouteType.DIRECT:
            return self.__path

        regex = self.__path

        for parameter in self.parameter_keys:
            regex = re.sub(
                rf"/\[{parameter}\]",
                f"/(?P<{parameter}>{DYNAMIC_ROUTE_KEY_ALLOWED_CHARACTERS})",
                regex,
            )

        return regex

    def as_uri_path(self) -> str:
        return self.__path.replace("_", "-")
