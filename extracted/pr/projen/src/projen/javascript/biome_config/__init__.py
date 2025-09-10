from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ..._jsii import *


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.Actions",
    jsii_struct_bases=[],
    name_mapping={"recommended": "recommended", "source": "source"},
)
class Actions:
    def __init__(
        self,
        *,
        recommended: typing.Optional[builtins.bool] = None,
        source: typing.Optional[typing.Union["Source", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param recommended: (experimental) It enables the assist actions recommended by Biome. ``true`` by default.
        :param source: 

        :stability: experimental
        :schema: Actions
        '''
        if isinstance(source, dict):
            source = Source(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6366c915d5edbe08a6c33dee8fe8422a0286f131b30d1697e72b9e5e37127dcc)
            check_type(argname="argument recommended", value=recommended, expected_type=type_hints["recommended"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if recommended is not None:
            self._values["recommended"] = recommended
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def recommended(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables the assist actions recommended by Biome.

        ``true`` by default.

        :stability: experimental
        :schema: Actions#recommended
        '''
        result = self._values.get("recommended")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def source(self) -> typing.Optional["Source"]:
        '''
        :stability: experimental
        :schema: Actions#source
        '''
        result = self._values.get("source")
        return typing.cast(typing.Optional["Source"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Actions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.javascript.biome_config.ArrowParentheses")
class ArrowParentheses(enum.Enum):
    '''
    :stability: experimental
    :schema: ArrowParentheses
    '''

    ALWAYS = "ALWAYS"
    '''(experimental) always.

    :stability: experimental
    '''
    AS_NEEDED = "AS_NEEDED"
    '''(experimental) asNeeded.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.AssistConfiguration",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions", "enabled": "enabled", "includes": "includes"},
)
class AssistConfiguration:
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Union[Actions, typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[builtins.bool] = None,
        includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param actions: (experimental) Whether Biome should fail in CLI if the assist were not applied to the code.
        :param enabled: (experimental) Whether Biome should enable assist via LSP and CLI.
        :param includes: (experimental) A list of glob patterns. Biome will include files/folders that will match these patterns.

        :stability: experimental
        :schema: AssistConfiguration
        '''
        if isinstance(actions, dict):
            actions = Actions(**actions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__653e8f7779876f355ba04bd69945d4c60ef342663eb94ddff052064ccd3fe707)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument includes", value=includes, expected_type=type_hints["includes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions
        if enabled is not None:
            self._values["enabled"] = enabled
        if includes is not None:
            self._values["includes"] = includes

    @builtins.property
    def actions(self) -> typing.Optional[Actions]:
        '''(experimental) Whether Biome should fail in CLI if the assist were not applied to the code.

        :stability: experimental
        :schema: AssistConfiguration#actions
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[Actions], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether Biome should enable assist via LSP and CLI.

        :stability: experimental
        :schema: AssistConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def includes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of glob patterns.

        Biome will include files/folders that will match these patterns.

        :stability: experimental
        :schema: AssistConfiguration#includes
        '''
        result = self._values.get("includes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssistConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.javascript.biome_config.AttributePosition")
class AttributePosition(enum.Enum):
    '''
    :stability: experimental
    :schema: AttributePosition
    '''

    AUTO = "AUTO"
    '''(experimental) auto.

    :stability: experimental
    '''
    MULTILINE = "MULTILINE"
    '''(experimental) multiline.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.BiomeConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "assist": "assist",
        "css": "css",
        "extends": "extends",
        "files": "files",
        "formatter": "formatter",
        "graphql": "graphql",
        "grit": "grit",
        "html": "html",
        "javascript": "javascript",
        "json": "json",
        "linter": "linter",
        "overrides": "overrides",
        "plugins": "plugins",
        "root": "root",
        "schema": "schema",
        "vcs": "vcs",
    },
)
class BiomeConfiguration:
    def __init__(
        self,
        *,
        assist: typing.Optional[typing.Union[AssistConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        css: typing.Optional[typing.Union["CssConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        extends: typing.Optional[typing.Sequence[builtins.str]] = None,
        files: typing.Optional[typing.Union["FilesConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        formatter: typing.Optional[typing.Union["FormatterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        graphql: typing.Optional[typing.Union["GraphqlConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        grit: typing.Optional[typing.Union["GritConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        html: typing.Optional[typing.Union["HtmlConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        javascript: typing.Optional[typing.Union["JsConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        json: typing.Optional[typing.Union["JsonConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        linter: typing.Optional[typing.Union["LinterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        overrides: typing.Optional[typing.Sequence[typing.Union["OverridePattern", typing.Dict[builtins.str, typing.Any]]]] = None,
        plugins: typing.Optional[typing.Sequence[builtins.str]] = None,
        root: typing.Optional[builtins.bool] = None,
        schema: typing.Optional[builtins.str] = None,
        vcs: typing.Optional[typing.Union["VcsConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) The configuration that is contained inside the file ``biome.json``.

        :param assist: (experimental) Specific configuration for assists.
        :param css: (experimental) Specific configuration for the Css language.
        :param extends: (experimental) A list of paths to other JSON files, used to extends the current configuration.
        :param files: (experimental) The configuration of the filesystem.
        :param formatter: (experimental) The configuration of the formatter.
        :param graphql: (experimental) Specific configuration for the GraphQL language.
        :param grit: (experimental) Specific configuration for the GraphQL language.
        :param html: (experimental) Specific configuration for the HTML language.
        :param javascript: (experimental) Specific configuration for the JavaScript language.
        :param json: (experimental) Specific configuration for the Json language.
        :param linter: (experimental) The configuration for the linter.
        :param overrides: (experimental) A list of granular patterns that should be applied only to a sub set of files.
        :param plugins: (experimental) List of plugins to load.
        :param root: (experimental) Indicates whether this configuration file is at the root of a Biome project. By default, this is ``true``.
        :param schema: (experimental) A field for the `JSON schema <https://json-schema.org/>`_ specification.
        :param vcs: (experimental) The configuration of the VCS integration.

        :stability: experimental
        :schema: BiomeConfiguration
        '''
        if isinstance(assist, dict):
            assist = AssistConfiguration(**assist)
        if isinstance(css, dict):
            css = CssConfiguration(**css)
        if isinstance(files, dict):
            files = FilesConfiguration(**files)
        if isinstance(formatter, dict):
            formatter = FormatterConfiguration(**formatter)
        if isinstance(graphql, dict):
            graphql = GraphqlConfiguration(**graphql)
        if isinstance(grit, dict):
            grit = GritConfiguration(**grit)
        if isinstance(html, dict):
            html = HtmlConfiguration(**html)
        if isinstance(javascript, dict):
            javascript = JsConfiguration(**javascript)
        if isinstance(json, dict):
            json = JsonConfiguration(**json)
        if isinstance(linter, dict):
            linter = LinterConfiguration(**linter)
        if isinstance(vcs, dict):
            vcs = VcsConfiguration(**vcs)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5d80cddd85ec22ae5e9ee130a7150db72ca1333e6e292553494d0e61d7b92e10)
            check_type(argname="argument assist", value=assist, expected_type=type_hints["assist"])
            check_type(argname="argument css", value=css, expected_type=type_hints["css"])
            check_type(argname="argument extends", value=extends, expected_type=type_hints["extends"])
            check_type(argname="argument files", value=files, expected_type=type_hints["files"])
            check_type(argname="argument formatter", value=formatter, expected_type=type_hints["formatter"])
            check_type(argname="argument graphql", value=graphql, expected_type=type_hints["graphql"])
            check_type(argname="argument grit", value=grit, expected_type=type_hints["grit"])
            check_type(argname="argument html", value=html, expected_type=type_hints["html"])
            check_type(argname="argument javascript", value=javascript, expected_type=type_hints["javascript"])
            check_type(argname="argument json", value=json, expected_type=type_hints["json"])
            check_type(argname="argument linter", value=linter, expected_type=type_hints["linter"])
            check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
            check_type(argname="argument plugins", value=plugins, expected_type=type_hints["plugins"])
            check_type(argname="argument root", value=root, expected_type=type_hints["root"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument vcs", value=vcs, expected_type=type_hints["vcs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assist is not None:
            self._values["assist"] = assist
        if css is not None:
            self._values["css"] = css
        if extends is not None:
            self._values["extends"] = extends
        if files is not None:
            self._values["files"] = files
        if formatter is not None:
            self._values["formatter"] = formatter
        if graphql is not None:
            self._values["graphql"] = graphql
        if grit is not None:
            self._values["grit"] = grit
        if html is not None:
            self._values["html"] = html
        if javascript is not None:
            self._values["javascript"] = javascript
        if json is not None:
            self._values["json"] = json
        if linter is not None:
            self._values["linter"] = linter
        if overrides is not None:
            self._values["overrides"] = overrides
        if plugins is not None:
            self._values["plugins"] = plugins
        if root is not None:
            self._values["root"] = root
        if schema is not None:
            self._values["schema"] = schema
        if vcs is not None:
            self._values["vcs"] = vcs

    @builtins.property
    def assist(self) -> typing.Optional[AssistConfiguration]:
        '''(experimental) Specific configuration for assists.

        :stability: experimental
        :schema: BiomeConfiguration#assist
        '''
        result = self._values.get("assist")
        return typing.cast(typing.Optional[AssistConfiguration], result)

    @builtins.property
    def css(self) -> typing.Optional["CssConfiguration"]:
        '''(experimental) Specific configuration for the Css language.

        :stability: experimental
        :schema: BiomeConfiguration#css
        '''
        result = self._values.get("css")
        return typing.cast(typing.Optional["CssConfiguration"], result)

    @builtins.property
    def extends(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of paths to other JSON files, used to extends the current configuration.

        :stability: experimental
        :schema: BiomeConfiguration#extends
        '''
        result = self._values.get("extends")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def files(self) -> typing.Optional["FilesConfiguration"]:
        '''(experimental) The configuration of the filesystem.

        :stability: experimental
        :schema: BiomeConfiguration#files
        '''
        result = self._values.get("files")
        return typing.cast(typing.Optional["FilesConfiguration"], result)

    @builtins.property
    def formatter(self) -> typing.Optional["FormatterConfiguration"]:
        '''(experimental) The configuration of the formatter.

        :stability: experimental
        :schema: BiomeConfiguration#formatter
        '''
        result = self._values.get("formatter")
        return typing.cast(typing.Optional["FormatterConfiguration"], result)

    @builtins.property
    def graphql(self) -> typing.Optional["GraphqlConfiguration"]:
        '''(experimental) Specific configuration for the GraphQL language.

        :stability: experimental
        :schema: BiomeConfiguration#graphql
        '''
        result = self._values.get("graphql")
        return typing.cast(typing.Optional["GraphqlConfiguration"], result)

    @builtins.property
    def grit(self) -> typing.Optional["GritConfiguration"]:
        '''(experimental) Specific configuration for the GraphQL language.

        :stability: experimental
        :schema: BiomeConfiguration#grit
        '''
        result = self._values.get("grit")
        return typing.cast(typing.Optional["GritConfiguration"], result)

    @builtins.property
    def html(self) -> typing.Optional["HtmlConfiguration"]:
        '''(experimental) Specific configuration for the HTML language.

        :stability: experimental
        :schema: BiomeConfiguration#html
        '''
        result = self._values.get("html")
        return typing.cast(typing.Optional["HtmlConfiguration"], result)

    @builtins.property
    def javascript(self) -> typing.Optional["JsConfiguration"]:
        '''(experimental) Specific configuration for the JavaScript language.

        :stability: experimental
        :schema: BiomeConfiguration#javascript
        '''
        result = self._values.get("javascript")
        return typing.cast(typing.Optional["JsConfiguration"], result)

    @builtins.property
    def json(self) -> typing.Optional["JsonConfiguration"]:
        '''(experimental) Specific configuration for the Json language.

        :stability: experimental
        :schema: BiomeConfiguration#json
        '''
        result = self._values.get("json")
        return typing.cast(typing.Optional["JsonConfiguration"], result)

    @builtins.property
    def linter(self) -> typing.Optional["LinterConfiguration"]:
        '''(experimental) The configuration for the linter.

        :stability: experimental
        :schema: BiomeConfiguration#linter
        '''
        result = self._values.get("linter")
        return typing.cast(typing.Optional["LinterConfiguration"], result)

    @builtins.property
    def overrides(self) -> typing.Optional[typing.List["OverridePattern"]]:
        '''(experimental) A list of granular patterns that should be applied only to a sub set of files.

        :stability: experimental
        :schema: BiomeConfiguration#overrides
        '''
        result = self._values.get("overrides")
        return typing.cast(typing.Optional[typing.List["OverridePattern"]], result)

    @builtins.property
    def plugins(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of plugins to load.

        :stability: experimental
        :schema: BiomeConfiguration#plugins
        '''
        result = self._values.get("plugins")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def root(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Indicates whether this configuration file is at the root of a Biome project.

        By default, this is ``true``.

        :stability: experimental
        :schema: BiomeConfiguration#root
        '''
        result = self._values.get("root")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def schema(self) -> typing.Optional[builtins.str]:
        '''(experimental) A field for the `JSON schema <https://json-schema.org/>`_ specification.

        :stability: experimental
        :schema: BiomeConfiguration#$schema
        '''
        result = self._values.get("schema")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vcs(self) -> typing.Optional["VcsConfiguration"]:
        '''(experimental) The configuration of the VCS integration.

        :stability: experimental
        :schema: BiomeConfiguration#vcs
        '''
        result = self._values.get("vcs")
        return typing.cast(typing.Optional["VcsConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BiomeConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.CssAssistConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class CssAssistConfiguration:
    def __init__(self, *, enabled: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Options that changes how the CSS assist behaves.

        :param enabled: (experimental) Control the assist for CSS files.

        :stability: experimental
        :schema: CssAssistConfiguration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d79ee25821f244538ee0bcf57d1ff302007d2643512718410c33310d05b8dc4)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the assist for CSS files.

        :stability: experimental
        :schema: CssAssistConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CssAssistConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.CssConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "assist": "assist",
        "formatter": "formatter",
        "globals": "globals",
        "linter": "linter",
        "parser": "parser",
    },
)
class CssConfiguration:
    def __init__(
        self,
        *,
        assist: typing.Optional[typing.Union[CssAssistConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        formatter: typing.Optional[typing.Union["CssFormatterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        globals: typing.Optional[typing.Sequence[builtins.str]] = None,
        linter: typing.Optional[typing.Union["CssLinterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        parser: typing.Optional[typing.Union["CssParserConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options applied to CSS files.

        :param assist: (experimental) CSS assist options.
        :param formatter: (experimental) CSS formatter options.
        :param globals: (experimental) CSS globals.
        :param linter: (experimental) CSS linter options.
        :param parser: (experimental) CSS parsing options.

        :stability: experimental
        :schema: CssConfiguration
        '''
        if isinstance(assist, dict):
            assist = CssAssistConfiguration(**assist)
        if isinstance(formatter, dict):
            formatter = CssFormatterConfiguration(**formatter)
        if isinstance(linter, dict):
            linter = CssLinterConfiguration(**linter)
        if isinstance(parser, dict):
            parser = CssParserConfiguration(**parser)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__546cd91eebef3c3c3a2ec7242b79be8e1e49bbd4e237eea9e2543e548c089bea)
            check_type(argname="argument assist", value=assist, expected_type=type_hints["assist"])
            check_type(argname="argument formatter", value=formatter, expected_type=type_hints["formatter"])
            check_type(argname="argument globals", value=globals, expected_type=type_hints["globals"])
            check_type(argname="argument linter", value=linter, expected_type=type_hints["linter"])
            check_type(argname="argument parser", value=parser, expected_type=type_hints["parser"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assist is not None:
            self._values["assist"] = assist
        if formatter is not None:
            self._values["formatter"] = formatter
        if globals is not None:
            self._values["globals"] = globals
        if linter is not None:
            self._values["linter"] = linter
        if parser is not None:
            self._values["parser"] = parser

    @builtins.property
    def assist(self) -> typing.Optional[CssAssistConfiguration]:
        '''(experimental) CSS assist options.

        :stability: experimental
        :schema: CssConfiguration#assist
        '''
        result = self._values.get("assist")
        return typing.cast(typing.Optional[CssAssistConfiguration], result)

    @builtins.property
    def formatter(self) -> typing.Optional["CssFormatterConfiguration"]:
        '''(experimental) CSS formatter options.

        :stability: experimental
        :schema: CssConfiguration#formatter
        '''
        result = self._values.get("formatter")
        return typing.cast(typing.Optional["CssFormatterConfiguration"], result)

    @builtins.property
    def globals(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) CSS globals.

        :stability: experimental
        :schema: CssConfiguration#globals
        '''
        result = self._values.get("globals")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def linter(self) -> typing.Optional["CssLinterConfiguration"]:
        '''(experimental) CSS linter options.

        :stability: experimental
        :schema: CssConfiguration#linter
        '''
        result = self._values.get("linter")
        return typing.cast(typing.Optional["CssLinterConfiguration"], result)

    @builtins.property
    def parser(self) -> typing.Optional["CssParserConfiguration"]:
        '''(experimental) CSS parsing options.

        :stability: experimental
        :schema: CssConfiguration#parser
        '''
        result = self._values.get("parser")
        return typing.cast(typing.Optional["CssParserConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CssConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.CssFormatterConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "indent_style": "indentStyle",
        "indent_width": "indentWidth",
        "line_ending": "lineEnding",
        "line_width": "lineWidth",
        "quote_style": "quoteStyle",
    },
)
class CssFormatterConfiguration:
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        indent_style: typing.Optional["IndentStyle"] = None,
        indent_width: typing.Optional[jsii.Number] = None,
        line_ending: typing.Optional["LineEnding"] = None,
        line_width: typing.Optional[jsii.Number] = None,
        quote_style: typing.Optional["QuoteStyle"] = None,
    ) -> None:
        '''(experimental) Options that changes how the CSS formatter behaves.

        :param enabled: (experimental) Control the formatter for CSS (and its super languages) files.
        :param indent_style: (experimental) The indent style applied to CSS (and its super languages) files.
        :param indent_width: (experimental) The size of the indentation applied to CSS (and its super languages) files. Default to 2. Default: 2.
        :param line_ending: (experimental) The type of line ending applied to CSS (and its super languages) files.
        :param line_width: (experimental) What's the max width of a line applied to CSS (and its super languages) files. Defaults to 80. Default: 80.
        :param quote_style: (experimental) The type of quotes used in CSS code. Defaults to double. Default: double.

        :stability: experimental
        :schema: CssFormatterConfiguration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1fb0cc7e8e9a8ff6796060277e93271c00edf3f8878cd107fe3a211c7aa58ca)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument indent_style", value=indent_style, expected_type=type_hints["indent_style"])
            check_type(argname="argument indent_width", value=indent_width, expected_type=type_hints["indent_width"])
            check_type(argname="argument line_ending", value=line_ending, expected_type=type_hints["line_ending"])
            check_type(argname="argument line_width", value=line_width, expected_type=type_hints["line_width"])
            check_type(argname="argument quote_style", value=quote_style, expected_type=type_hints["quote_style"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if indent_style is not None:
            self._values["indent_style"] = indent_style
        if indent_width is not None:
            self._values["indent_width"] = indent_width
        if line_ending is not None:
            self._values["line_ending"] = line_ending
        if line_width is not None:
            self._values["line_width"] = line_width
        if quote_style is not None:
            self._values["quote_style"] = quote_style

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the formatter for CSS (and its super languages) files.

        :stability: experimental
        :schema: CssFormatterConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def indent_style(self) -> typing.Optional["IndentStyle"]:
        '''(experimental) The indent style applied to CSS (and its super languages) files.

        :stability: experimental
        :schema: CssFormatterConfiguration#indentStyle
        '''
        result = self._values.get("indent_style")
        return typing.cast(typing.Optional["IndentStyle"], result)

    @builtins.property
    def indent_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation applied to CSS (and its super languages) files.

        Default to 2.

        :default: 2.

        :stability: experimental
        :schema: CssFormatterConfiguration#indentWidth
        '''
        result = self._values.get("indent_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def line_ending(self) -> typing.Optional["LineEnding"]:
        '''(experimental) The type of line ending applied to CSS (and its super languages) files.

        :stability: experimental
        :schema: CssFormatterConfiguration#lineEnding
        '''
        result = self._values.get("line_ending")
        return typing.cast(typing.Optional["LineEnding"], result)

    @builtins.property
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) What's the max width of a line applied to CSS (and its super languages) files.

        Defaults to 80.

        :default: 80.

        :stability: experimental
        :schema: CssFormatterConfiguration#lineWidth
        '''
        result = self._values.get("line_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def quote_style(self) -> typing.Optional["QuoteStyle"]:
        '''(experimental) The type of quotes used in CSS code.

        Defaults to double.

        :default: double.

        :stability: experimental
        :schema: CssFormatterConfiguration#quoteStyle
        '''
        result = self._values.get("quote_style")
        return typing.cast(typing.Optional["QuoteStyle"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CssFormatterConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.CssLinterConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class CssLinterConfiguration:
    def __init__(self, *, enabled: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Options that changes how the CSS linter behaves.

        :param enabled: (experimental) Control the linter for CSS files.

        :stability: experimental
        :schema: CssLinterConfiguration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66bcb81b30852efd84c1040b1c15bea9669396c926d4f016dc8c65523fc5d8c0)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the linter for CSS files.

        :stability: experimental
        :schema: CssLinterConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CssLinterConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.CssParserConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "allow_wrong_line_comments": "allowWrongLineComments",
        "css_modules": "cssModules",
    },
)
class CssParserConfiguration:
    def __init__(
        self,
        *,
        allow_wrong_line_comments: typing.Optional[builtins.bool] = None,
        css_modules: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options that changes how the CSS parser behaves.

        :param allow_wrong_line_comments: (experimental) Allow comments to appear on incorrect lines in ``.css`` files.
        :param css_modules: (experimental) Enables parsing of CSS Modules specific features.

        :stability: experimental
        :schema: CssParserConfiguration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8529582f37794a4d2a6c31671f27c3add8085e862adbf314c4f633b00295f518)
            check_type(argname="argument allow_wrong_line_comments", value=allow_wrong_line_comments, expected_type=type_hints["allow_wrong_line_comments"])
            check_type(argname="argument css_modules", value=css_modules, expected_type=type_hints["css_modules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_wrong_line_comments is not None:
            self._values["allow_wrong_line_comments"] = allow_wrong_line_comments
        if css_modules is not None:
            self._values["css_modules"] = css_modules

    @builtins.property
    def allow_wrong_line_comments(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allow comments to appear on incorrect lines in ``.css`` files.

        :stability: experimental
        :schema: CssParserConfiguration#allowWrongLineComments
        '''
        result = self._values.get("allow_wrong_line_comments")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def css_modules(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables parsing of CSS Modules specific features.

        :stability: experimental
        :schema: CssParserConfiguration#cssModules
        '''
        result = self._values.get("css_modules")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CssParserConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.javascript.biome_config.Expand")
class Expand(enum.Enum):
    '''
    :stability: experimental
    :schema: Expand
    '''

    AUTO = "AUTO"
    '''(experimental) auto.

    :stability: experimental
    '''
    ALWAYS = "ALWAYS"
    '''(experimental) always.

    :stability: experimental
    '''
    NEVER = "NEVER"
    '''(experimental) never.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.FilesConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "experimental_scanner_ignores": "experimentalScannerIgnores",
        "ignore_unknown": "ignoreUnknown",
        "includes": "includes",
        "max_size": "maxSize",
    },
)
class FilesConfiguration:
    def __init__(
        self,
        *,
        experimental_scanner_ignores: typing.Optional[typing.Sequence[builtins.str]] = None,
        ignore_unknown: typing.Optional[builtins.bool] = None,
        includes: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_size: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) The configuration of the filesystem.

        :param experimental_scanner_ignores: (experimental) Set of file and folder names that should be unconditionally ignored by Biome's scanner. Biome maintains an internal list of default ignore entries, which is based on user feedback and which may change in any release. This setting allows overriding this internal list completely. This is considered an advanced feature that users *should* not need to tweak themselves, but they can as a last resort. This setting can only be configured in root configurations, and is ignored in nested configs. Entries must be file or folder *names*. Specific paths and globs are not supported. Examples where this may be useful: ```jsonc { "files": { "experimentalScannerIgnores": [ // You almost certainly don't want to scan your ``.git`` // folder, which is why it's already ignored by default: ".git", // But the scanner does scan ``node_modules`` by default. If // you *really* don't want this, you can ignore it like // this: "node_modules", // But it's probably better to ignore a specific dependency. // For instance, one that happens to be particularly slow to // scan: "RedisCommander.d.ts", ], } } ``` Please be aware that rules relying on the module graph or type inference information may be negatively affected if dependencies of your project aren't (fully) scanned.
        :param ignore_unknown: (experimental) Tells Biome to not emit diagnostics when handling files that doesn't know.
        :param includes: (experimental) A list of glob patterns. Biome will handle only those files/folders that will match these patterns.
        :param max_size: (experimental) The maximum allowed size for source code files in bytes. Files above this limit will be ignored for performance reasons. Defaults to 1 MiB Default: 1 MiB

        :stability: experimental
        :schema: FilesConfiguration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f06e077779a89de8924deeb042aada1ebd486faca5b2fad3aabff17e1eaaa2e4)
            check_type(argname="argument experimental_scanner_ignores", value=experimental_scanner_ignores, expected_type=type_hints["experimental_scanner_ignores"])
            check_type(argname="argument ignore_unknown", value=ignore_unknown, expected_type=type_hints["ignore_unknown"])
            check_type(argname="argument includes", value=includes, expected_type=type_hints["includes"])
            check_type(argname="argument max_size", value=max_size, expected_type=type_hints["max_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if experimental_scanner_ignores is not None:
            self._values["experimental_scanner_ignores"] = experimental_scanner_ignores
        if ignore_unknown is not None:
            self._values["ignore_unknown"] = ignore_unknown
        if includes is not None:
            self._values["includes"] = includes
        if max_size is not None:
            self._values["max_size"] = max_size

    @builtins.property
    def experimental_scanner_ignores(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Set of file and folder names that should be unconditionally ignored by Biome's scanner.

        Biome maintains an internal list of default ignore entries, which is based on user feedback and which may change in any release. This setting allows overriding this internal list completely.

        This is considered an advanced feature that users *should* not need to tweak themselves, but they can as a last resort. This setting can only be configured in root configurations, and is ignored in nested configs.

        Entries must be file or folder *names*. Specific paths and globs are not supported.

        Examples where this may be useful:

        ```jsonc { "files": { "experimentalScannerIgnores": [ // You almost certainly don't want to scan your ``.git`` // folder, which is why it's already ignored by default: ".git",

        // But the scanner does scan ``node_modules`` by default. If // you *really* don't want this, you can ignore it like // this: "node_modules",

        // But it's probably better to ignore a specific dependency. // For instance, one that happens to be particularly slow to // scan: "RedisCommander.d.ts", ], } } ```

        Please be aware that rules relying on the module graph or type inference information may be negatively affected if dependencies of your project aren't (fully) scanned.

        :stability: experimental
        :schema: FilesConfiguration#experimentalScannerIgnores
        '''
        result = self._values.get("experimental_scanner_ignores")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ignore_unknown(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Tells Biome to not emit diagnostics when handling files that doesn't know.

        :stability: experimental
        :schema: FilesConfiguration#ignoreUnknown
        '''
        result = self._values.get("ignore_unknown")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def includes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of glob patterns.

        Biome will handle only those files/folders that will match these patterns.

        :stability: experimental
        :schema: FilesConfiguration#includes
        '''
        result = self._values.get("includes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def max_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum allowed size for source code files in bytes.

        Files above this limit will be ignored for performance reasons. Defaults to 1 MiB

        :default: 1 MiB

        :stability: experimental
        :schema: FilesConfiguration#maxSize
        '''
        result = self._values.get("max_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FilesConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.FormatterConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "attribute_position": "attributePosition",
        "bracket_same_line": "bracketSameLine",
        "bracket_spacing": "bracketSpacing",
        "enabled": "enabled",
        "expand": "expand",
        "format_with_errors": "formatWithErrors",
        "includes": "includes",
        "indent_style": "indentStyle",
        "indent_width": "indentWidth",
        "line_ending": "lineEnding",
        "line_width": "lineWidth",
        "use_editorconfig": "useEditorconfig",
    },
)
class FormatterConfiguration:
    def __init__(
        self,
        *,
        attribute_position: typing.Optional[AttributePosition] = None,
        bracket_same_line: typing.Optional[builtins.bool] = None,
        bracket_spacing: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        expand: typing.Optional[Expand] = None,
        format_with_errors: typing.Optional[builtins.bool] = None,
        includes: typing.Optional[typing.Sequence[builtins.str]] = None,
        indent_style: typing.Optional["IndentStyle"] = None,
        indent_width: typing.Optional[jsii.Number] = None,
        line_ending: typing.Optional["LineEnding"] = None,
        line_width: typing.Optional[jsii.Number] = None,
        use_editorconfig: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Generic options applied to all files.

        :param attribute_position: (experimental) The attribute position style in HTML-ish languages. Defaults to auto. Default: auto.
        :param bracket_same_line: (experimental) Put the ``>`` of a multi-line HTML or JSX element at the end of the last line instead of being alone on the next line (does not apply to self closing elements).
        :param bracket_spacing: (experimental) Whether to insert spaces around brackets in object literals. Defaults to true. Default: true.
        :param enabled: 
        :param expand: (experimental) Whether to expand arrays and objects on multiple lines. When set to ``auto``, object literals are formatted on multiple lines if the first property has a newline, and array literals are formatted on a single line if it fits in the line. When set to ``always``, these literals are formatted on multiple lines, regardless of length of the list. When set to ``never``, these literals are formatted on a single line if it fits in the line. When formatting ``package.json``, Biome will use ``always`` unless configured otherwise. Defaults to "auto". Default: auto".
        :param format_with_errors: (experimental) Stores whether formatting should be allowed to proceed if a given file has syntax errors.
        :param includes: (experimental) A list of glob patterns. The formatter will include files/folders that will match these patterns.
        :param indent_style: (experimental) The indent style.
        :param indent_width: (experimental) The size of the indentation, 2 by default.
        :param line_ending: (experimental) The type of line ending.
        :param line_width: (experimental) What's the max width of a line. Defaults to 80. Default: 80.
        :param use_editorconfig: (experimental) Use any ``.editorconfig`` files to configure the formatter. Configuration in ``biome.json`` will override ``.editorconfig`` configuration. Default: ``true``.

        :stability: experimental
        :schema: FormatterConfiguration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d250053b03cd738e71599a16d0b903766c0befb7557dadc7ffee799234532c78)
            check_type(argname="argument attribute_position", value=attribute_position, expected_type=type_hints["attribute_position"])
            check_type(argname="argument bracket_same_line", value=bracket_same_line, expected_type=type_hints["bracket_same_line"])
            check_type(argname="argument bracket_spacing", value=bracket_spacing, expected_type=type_hints["bracket_spacing"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument expand", value=expand, expected_type=type_hints["expand"])
            check_type(argname="argument format_with_errors", value=format_with_errors, expected_type=type_hints["format_with_errors"])
            check_type(argname="argument includes", value=includes, expected_type=type_hints["includes"])
            check_type(argname="argument indent_style", value=indent_style, expected_type=type_hints["indent_style"])
            check_type(argname="argument indent_width", value=indent_width, expected_type=type_hints["indent_width"])
            check_type(argname="argument line_ending", value=line_ending, expected_type=type_hints["line_ending"])
            check_type(argname="argument line_width", value=line_width, expected_type=type_hints["line_width"])
            check_type(argname="argument use_editorconfig", value=use_editorconfig, expected_type=type_hints["use_editorconfig"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attribute_position is not None:
            self._values["attribute_position"] = attribute_position
        if bracket_same_line is not None:
            self._values["bracket_same_line"] = bracket_same_line
        if bracket_spacing is not None:
            self._values["bracket_spacing"] = bracket_spacing
        if enabled is not None:
            self._values["enabled"] = enabled
        if expand is not None:
            self._values["expand"] = expand
        if format_with_errors is not None:
            self._values["format_with_errors"] = format_with_errors
        if includes is not None:
            self._values["includes"] = includes
        if indent_style is not None:
            self._values["indent_style"] = indent_style
        if indent_width is not None:
            self._values["indent_width"] = indent_width
        if line_ending is not None:
            self._values["line_ending"] = line_ending
        if line_width is not None:
            self._values["line_width"] = line_width
        if use_editorconfig is not None:
            self._values["use_editorconfig"] = use_editorconfig

    @builtins.property
    def attribute_position(self) -> typing.Optional[AttributePosition]:
        '''(experimental) The attribute position style in HTML-ish languages.

        Defaults to auto.

        :default: auto.

        :stability: experimental
        :schema: FormatterConfiguration#attributePosition
        '''
        result = self._values.get("attribute_position")
        return typing.cast(typing.Optional[AttributePosition], result)

    @builtins.property
    def bracket_same_line(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Put the ``>`` of a multi-line HTML or JSX element at the end of the last line instead of being alone on the next line (does not apply to self closing elements).

        :stability: experimental
        :schema: FormatterConfiguration#bracketSameLine
        '''
        result = self._values.get("bracket_same_line")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def bracket_spacing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to insert spaces around brackets in object literals.

        Defaults to true.

        :default: true.

        :stability: experimental
        :schema: FormatterConfiguration#bracketSpacing
        '''
        result = self._values.get("bracket_spacing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        :schema: FormatterConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def expand(self) -> typing.Optional[Expand]:
        '''(experimental) Whether to expand arrays and objects on multiple lines.

        When set to ``auto``, object literals are formatted on multiple lines if the first property has a newline, and array literals are formatted on a single line if it fits in the line. When set to ``always``, these literals are formatted on multiple lines, regardless of length of the list. When set to ``never``, these literals are formatted on a single line if it fits in the line. When formatting ``package.json``, Biome will use ``always`` unless configured otherwise. Defaults to "auto".

        :default: auto".

        :stability: experimental
        :schema: FormatterConfiguration#expand
        '''
        result = self._values.get("expand")
        return typing.cast(typing.Optional[Expand], result)

    @builtins.property
    def format_with_errors(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Stores whether formatting should be allowed to proceed if a given file has syntax errors.

        :stability: experimental
        :schema: FormatterConfiguration#formatWithErrors
        '''
        result = self._values.get("format_with_errors")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def includes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of glob patterns.

        The formatter will include files/folders that will match these patterns.

        :stability: experimental
        :schema: FormatterConfiguration#includes
        '''
        result = self._values.get("includes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def indent_style(self) -> typing.Optional["IndentStyle"]:
        '''(experimental) The indent style.

        :stability: experimental
        :schema: FormatterConfiguration#indentStyle
        '''
        result = self._values.get("indent_style")
        return typing.cast(typing.Optional["IndentStyle"], result)

    @builtins.property
    def indent_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation, 2 by default.

        :stability: experimental
        :schema: FormatterConfiguration#indentWidth
        '''
        result = self._values.get("indent_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def line_ending(self) -> typing.Optional["LineEnding"]:
        '''(experimental) The type of line ending.

        :stability: experimental
        :schema: FormatterConfiguration#lineEnding
        '''
        result = self._values.get("line_ending")
        return typing.cast(typing.Optional["LineEnding"], result)

    @builtins.property
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) What's the max width of a line.

        Defaults to 80.

        :default: 80.

        :stability: experimental
        :schema: FormatterConfiguration#lineWidth
        '''
        result = self._values.get("line_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def use_editorconfig(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use any ``.editorconfig`` files to configure the formatter. Configuration in ``biome.json`` will override ``.editorconfig`` configuration.

        Default: ``true``.

        :stability: experimental
        :schema: FormatterConfiguration#useEditorconfig
        '''
        result = self._values.get("use_editorconfig")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FormatterConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.GraphqlAssistConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GraphqlAssistConfiguration:
    def __init__(self, *, enabled: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Options that changes how the GraphQL linter behaves.

        :param enabled: (experimental) Control the formatter for GraphQL files.

        :stability: experimental
        :schema: GraphqlAssistConfiguration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0dbfc7c635234e8ca5c531a8c27d60cc9eb836491490660da8418fad825b69a2)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the formatter for GraphQL files.

        :stability: experimental
        :schema: GraphqlAssistConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GraphqlAssistConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.GraphqlConfiguration",
    jsii_struct_bases=[],
    name_mapping={"assist": "assist", "formatter": "formatter", "linter": "linter"},
)
class GraphqlConfiguration:
    def __init__(
        self,
        *,
        assist: typing.Optional[typing.Union[GraphqlAssistConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        formatter: typing.Optional[typing.Union["GraphqlFormatterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        linter: typing.Optional[typing.Union["GraphqlLinterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options applied to GraphQL files.

        :param assist: (experimental) Assist options.
        :param formatter: (experimental) GraphQL formatter options.
        :param linter: 

        :stability: experimental
        :schema: GraphqlConfiguration
        '''
        if isinstance(assist, dict):
            assist = GraphqlAssistConfiguration(**assist)
        if isinstance(formatter, dict):
            formatter = GraphqlFormatterConfiguration(**formatter)
        if isinstance(linter, dict):
            linter = GraphqlLinterConfiguration(**linter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2155336ae80236225feccaa799a660386650fec7a49468bef45ab34ed6677842)
            check_type(argname="argument assist", value=assist, expected_type=type_hints["assist"])
            check_type(argname="argument formatter", value=formatter, expected_type=type_hints["formatter"])
            check_type(argname="argument linter", value=linter, expected_type=type_hints["linter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assist is not None:
            self._values["assist"] = assist
        if formatter is not None:
            self._values["formatter"] = formatter
        if linter is not None:
            self._values["linter"] = linter

    @builtins.property
    def assist(self) -> typing.Optional[GraphqlAssistConfiguration]:
        '''(experimental) Assist options.

        :stability: experimental
        :schema: GraphqlConfiguration#assist
        '''
        result = self._values.get("assist")
        return typing.cast(typing.Optional[GraphqlAssistConfiguration], result)

    @builtins.property
    def formatter(self) -> typing.Optional["GraphqlFormatterConfiguration"]:
        '''(experimental) GraphQL formatter options.

        :stability: experimental
        :schema: GraphqlConfiguration#formatter
        '''
        result = self._values.get("formatter")
        return typing.cast(typing.Optional["GraphqlFormatterConfiguration"], result)

    @builtins.property
    def linter(self) -> typing.Optional["GraphqlLinterConfiguration"]:
        '''
        :stability: experimental
        :schema: GraphqlConfiguration#linter
        '''
        result = self._values.get("linter")
        return typing.cast(typing.Optional["GraphqlLinterConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GraphqlConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.GraphqlFormatterConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "bracket_spacing": "bracketSpacing",
        "enabled": "enabled",
        "indent_style": "indentStyle",
        "indent_width": "indentWidth",
        "line_ending": "lineEnding",
        "line_width": "lineWidth",
        "quote_style": "quoteStyle",
    },
)
class GraphqlFormatterConfiguration:
    def __init__(
        self,
        *,
        bracket_spacing: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        indent_style: typing.Optional["IndentStyle"] = None,
        indent_width: typing.Optional[jsii.Number] = None,
        line_ending: typing.Optional["LineEnding"] = None,
        line_width: typing.Optional[jsii.Number] = None,
        quote_style: typing.Optional["QuoteStyle"] = None,
    ) -> None:
        '''(experimental) Options that changes how the GraphQL formatter behaves.

        :param bracket_spacing: (experimental) Whether to insert spaces around brackets in object literals. Defaults to true. Default: true.
        :param enabled: (experimental) Control the formatter for GraphQL files.
        :param indent_style: (experimental) The indent style applied to GraphQL files.
        :param indent_width: (experimental) The size of the indentation applied to GraphQL files. Default to 2. Default: 2.
        :param line_ending: (experimental) The type of line ending applied to GraphQL files.
        :param line_width: (experimental) What's the max width of a line applied to GraphQL files. Defaults to 80. Default: 80.
        :param quote_style: (experimental) The type of quotes used in GraphQL code. Defaults to double. Default: double.

        :stability: experimental
        :schema: GraphqlFormatterConfiguration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc9ad6152bf4d6cec4d40f5bfd9a8d0247f6c53cda4876e24cc83741fac1ae9f)
            check_type(argname="argument bracket_spacing", value=bracket_spacing, expected_type=type_hints["bracket_spacing"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument indent_style", value=indent_style, expected_type=type_hints["indent_style"])
            check_type(argname="argument indent_width", value=indent_width, expected_type=type_hints["indent_width"])
            check_type(argname="argument line_ending", value=line_ending, expected_type=type_hints["line_ending"])
            check_type(argname="argument line_width", value=line_width, expected_type=type_hints["line_width"])
            check_type(argname="argument quote_style", value=quote_style, expected_type=type_hints["quote_style"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bracket_spacing is not None:
            self._values["bracket_spacing"] = bracket_spacing
        if enabled is not None:
            self._values["enabled"] = enabled
        if indent_style is not None:
            self._values["indent_style"] = indent_style
        if indent_width is not None:
            self._values["indent_width"] = indent_width
        if line_ending is not None:
            self._values["line_ending"] = line_ending
        if line_width is not None:
            self._values["line_width"] = line_width
        if quote_style is not None:
            self._values["quote_style"] = quote_style

    @builtins.property
    def bracket_spacing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to insert spaces around brackets in object literals.

        Defaults to true.

        :default: true.

        :stability: experimental
        :schema: GraphqlFormatterConfiguration#bracketSpacing
        '''
        result = self._values.get("bracket_spacing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the formatter for GraphQL files.

        :stability: experimental
        :schema: GraphqlFormatterConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def indent_style(self) -> typing.Optional["IndentStyle"]:
        '''(experimental) The indent style applied to GraphQL files.

        :stability: experimental
        :schema: GraphqlFormatterConfiguration#indentStyle
        '''
        result = self._values.get("indent_style")
        return typing.cast(typing.Optional["IndentStyle"], result)

    @builtins.property
    def indent_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation applied to GraphQL files.

        Default to 2.

        :default: 2.

        :stability: experimental
        :schema: GraphqlFormatterConfiguration#indentWidth
        '''
        result = self._values.get("indent_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def line_ending(self) -> typing.Optional["LineEnding"]:
        '''(experimental) The type of line ending applied to GraphQL files.

        :stability: experimental
        :schema: GraphqlFormatterConfiguration#lineEnding
        '''
        result = self._values.get("line_ending")
        return typing.cast(typing.Optional["LineEnding"], result)

    @builtins.property
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) What's the max width of a line applied to GraphQL files.

        Defaults to 80.

        :default: 80.

        :stability: experimental
        :schema: GraphqlFormatterConfiguration#lineWidth
        '''
        result = self._values.get("line_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def quote_style(self) -> typing.Optional["QuoteStyle"]:
        '''(experimental) The type of quotes used in GraphQL code.

        Defaults to double.

        :default: double.

        :stability: experimental
        :schema: GraphqlFormatterConfiguration#quoteStyle
        '''
        result = self._values.get("quote_style")
        return typing.cast(typing.Optional["QuoteStyle"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GraphqlFormatterConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.GraphqlLinterConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GraphqlLinterConfiguration:
    def __init__(self, *, enabled: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Options that change how the GraphQL linter behaves.

        :param enabled: (experimental) Control the formatter for GraphQL files.

        :stability: experimental
        :schema: GraphqlLinterConfiguration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d2f81257796562c5e318e2c7b1278da3b88a7b868379f34ecb8d427734ba141)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the formatter for GraphQL files.

        :stability: experimental
        :schema: GraphqlLinterConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GraphqlLinterConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.GritAssistConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GritAssistConfiguration:
    def __init__(self, *, enabled: typing.Optional[builtins.bool] = None) -> None:
        '''
        :param enabled: (experimental) Control the assist functionality for Grit files.

        :stability: experimental
        :schema: GritAssistConfiguration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59f4559ad93f10b7671f2d81b54798d511d54078f14b37594d40617170bd4645)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the assist functionality for Grit files.

        :stability: experimental
        :schema: GritAssistConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GritAssistConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.GritConfiguration",
    jsii_struct_bases=[],
    name_mapping={"assist": "assist", "formatter": "formatter", "linter": "linter"},
)
class GritConfiguration:
    def __init__(
        self,
        *,
        assist: typing.Optional[typing.Union[GritAssistConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        formatter: typing.Optional[typing.Union["GritFormatterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        linter: typing.Optional[typing.Union["GritLinterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options applied to GritQL files.

        :param assist: (experimental) Assist options.
        :param formatter: (experimental) Formatting options.
        :param linter: (experimental) Formatting options.

        :stability: experimental
        :schema: GritConfiguration
        '''
        if isinstance(assist, dict):
            assist = GritAssistConfiguration(**assist)
        if isinstance(formatter, dict):
            formatter = GritFormatterConfiguration(**formatter)
        if isinstance(linter, dict):
            linter = GritLinterConfiguration(**linter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6767810d80e7477e7c2f6a26f7c7f238a608f28412191ad4e6ab8504edd02a88)
            check_type(argname="argument assist", value=assist, expected_type=type_hints["assist"])
            check_type(argname="argument formatter", value=formatter, expected_type=type_hints["formatter"])
            check_type(argname="argument linter", value=linter, expected_type=type_hints["linter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assist is not None:
            self._values["assist"] = assist
        if formatter is not None:
            self._values["formatter"] = formatter
        if linter is not None:
            self._values["linter"] = linter

    @builtins.property
    def assist(self) -> typing.Optional[GritAssistConfiguration]:
        '''(experimental) Assist options.

        :stability: experimental
        :schema: GritConfiguration#assist
        '''
        result = self._values.get("assist")
        return typing.cast(typing.Optional[GritAssistConfiguration], result)

    @builtins.property
    def formatter(self) -> typing.Optional["GritFormatterConfiguration"]:
        '''(experimental) Formatting options.

        :stability: experimental
        :schema: GritConfiguration#formatter
        '''
        result = self._values.get("formatter")
        return typing.cast(typing.Optional["GritFormatterConfiguration"], result)

    @builtins.property
    def linter(self) -> typing.Optional["GritLinterConfiguration"]:
        '''(experimental) Formatting options.

        :stability: experimental
        :schema: GritConfiguration#linter
        '''
        result = self._values.get("linter")
        return typing.cast(typing.Optional["GritLinterConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GritConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.GritFormatterConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "indent_style": "indentStyle",
        "indent_width": "indentWidth",
        "line_ending": "lineEnding",
        "line_width": "lineWidth",
    },
)
class GritFormatterConfiguration:
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        indent_style: typing.Optional["IndentStyle"] = None,
        indent_width: typing.Optional[jsii.Number] = None,
        line_ending: typing.Optional["LineEnding"] = None,
        line_width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: (experimental) Control the formatter for Grit files.
        :param indent_style: (experimental) The indent style applied to Grit files.
        :param indent_width: (experimental) The size of the indentation applied to Grit files. Default to 2. Default: 2.
        :param line_ending: (experimental) The type of line ending applied to Grit files.
        :param line_width: (experimental) What's the max width of a line applied to Grit files. Defaults to 80. Default: 80.

        :stability: experimental
        :schema: GritFormatterConfiguration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7eb20c598594405c2626c0973407324d66863625354188a196be6d25686d44e8)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument indent_style", value=indent_style, expected_type=type_hints["indent_style"])
            check_type(argname="argument indent_width", value=indent_width, expected_type=type_hints["indent_width"])
            check_type(argname="argument line_ending", value=line_ending, expected_type=type_hints["line_ending"])
            check_type(argname="argument line_width", value=line_width, expected_type=type_hints["line_width"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if indent_style is not None:
            self._values["indent_style"] = indent_style
        if indent_width is not None:
            self._values["indent_width"] = indent_width
        if line_ending is not None:
            self._values["line_ending"] = line_ending
        if line_width is not None:
            self._values["line_width"] = line_width

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the formatter for Grit files.

        :stability: experimental
        :schema: GritFormatterConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def indent_style(self) -> typing.Optional["IndentStyle"]:
        '''(experimental) The indent style applied to Grit files.

        :stability: experimental
        :schema: GritFormatterConfiguration#indentStyle
        '''
        result = self._values.get("indent_style")
        return typing.cast(typing.Optional["IndentStyle"], result)

    @builtins.property
    def indent_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation applied to Grit files.

        Default to 2.

        :default: 2.

        :stability: experimental
        :schema: GritFormatterConfiguration#indentWidth
        '''
        result = self._values.get("indent_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def line_ending(self) -> typing.Optional["LineEnding"]:
        '''(experimental) The type of line ending applied to Grit files.

        :stability: experimental
        :schema: GritFormatterConfiguration#lineEnding
        '''
        result = self._values.get("line_ending")
        return typing.cast(typing.Optional["LineEnding"], result)

    @builtins.property
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) What's the max width of a line applied to Grit files.

        Defaults to 80.

        :default: 80.

        :stability: experimental
        :schema: GritFormatterConfiguration#lineWidth
        '''
        result = self._values.get("line_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GritFormatterConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.GritLinterConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class GritLinterConfiguration:
    def __init__(self, *, enabled: typing.Optional[builtins.bool] = None) -> None:
        '''
        :param enabled: (experimental) Control the linter for Grit files.

        :stability: experimental
        :schema: GritLinterConfiguration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f328d623f0baa93f52695005ba45f28881c95ae610fde354116a44bc8b01c30)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the linter for Grit files.

        :stability: experimental
        :schema: GritLinterConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GritLinterConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.HtmlConfiguration",
    jsii_struct_bases=[],
    name_mapping={"formatter": "formatter", "parser": "parser"},
)
class HtmlConfiguration:
    def __init__(
        self,
        *,
        formatter: typing.Optional[typing.Union["HtmlFormatterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        parser: typing.Optional[typing.Union["HtmlParserConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options applied to HTML files.

        :param formatter: (experimental) HTML formatter options.
        :param parser: (experimental) HTML parsing options.

        :stability: experimental
        :schema: HtmlConfiguration
        '''
        if isinstance(formatter, dict):
            formatter = HtmlFormatterConfiguration(**formatter)
        if isinstance(parser, dict):
            parser = HtmlParserConfiguration(**parser)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__048266f3b4e4769e6485570d4954197f51204fc6e607e2ffe5267f80089b5ded)
            check_type(argname="argument formatter", value=formatter, expected_type=type_hints["formatter"])
            check_type(argname="argument parser", value=parser, expected_type=type_hints["parser"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if formatter is not None:
            self._values["formatter"] = formatter
        if parser is not None:
            self._values["parser"] = parser

    @builtins.property
    def formatter(self) -> typing.Optional["HtmlFormatterConfiguration"]:
        '''(experimental) HTML formatter options.

        :stability: experimental
        :schema: HtmlConfiguration#formatter
        '''
        result = self._values.get("formatter")
        return typing.cast(typing.Optional["HtmlFormatterConfiguration"], result)

    @builtins.property
    def parser(self) -> typing.Optional["HtmlParserConfiguration"]:
        '''(experimental) HTML parsing options.

        :stability: experimental
        :schema: HtmlConfiguration#parser
        '''
        result = self._values.get("parser")
        return typing.cast(typing.Optional["HtmlParserConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HtmlConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.HtmlFormatterConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "attribute_position": "attributePosition",
        "bracket_same_line": "bracketSameLine",
        "enabled": "enabled",
        "indent_script_and_style": "indentScriptAndStyle",
        "indent_style": "indentStyle",
        "indent_width": "indentWidth",
        "line_ending": "lineEnding",
        "line_width": "lineWidth",
        "self_close_void_elements": "selfCloseVoidElements",
        "whitespace_sensitivity": "whitespaceSensitivity",
    },
)
class HtmlFormatterConfiguration:
    def __init__(
        self,
        *,
        attribute_position: typing.Optional[AttributePosition] = None,
        bracket_same_line: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        indent_script_and_style: typing.Optional[builtins.bool] = None,
        indent_style: typing.Optional["IndentStyle"] = None,
        indent_width: typing.Optional[jsii.Number] = None,
        line_ending: typing.Optional["LineEnding"] = None,
        line_width: typing.Optional[jsii.Number] = None,
        self_close_void_elements: typing.Optional["SelfCloseVoidElements"] = None,
        whitespace_sensitivity: typing.Optional["WhitespaceSensitivity"] = None,
    ) -> None:
        '''(experimental) Options that changes how the HTML formatter behaves.

        :param attribute_position: (experimental) The attribute position style in HTML elements. Defaults to auto. Default: auto.
        :param bracket_same_line: (experimental) Whether to hug the closing bracket of multiline HTML tags to the end of the last line, rather than being alone on the following line. Defaults to false. Default: false.
        :param enabled: (experimental) Control the formatter for HTML (and its super languages) files.
        :param indent_script_and_style: (experimental) Whether to indent the ``<script>`` and ``<style>`` tags for HTML (and its super languages). Defaults to false. Default: false.
        :param indent_style: (experimental) The indent style applied to HTML (and its super languages) files.
        :param indent_width: (experimental) The size of the indentation applied to HTML (and its super languages) files. Default to 2. Default: 2.
        :param line_ending: (experimental) The type of line ending applied to HTML (and its super languages) files.
        :param line_width: (experimental) What's the max width of a line applied to HTML (and its super languages) files. Defaults to 80. Default: 80.
        :param self_close_void_elements: (experimental) Whether void elements should be self-closed. Defaults to never. Default: never.
        :param whitespace_sensitivity: (experimental) Whether to account for whitespace sensitivity when formatting HTML (and its super languages). Defaults to "css". Default: css".

        :stability: experimental
        :schema: HtmlFormatterConfiguration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcbf243ebdc0f288a10a4e6b68dc5a1ff88f4d8abe5566f57f212bf101440a69)
            check_type(argname="argument attribute_position", value=attribute_position, expected_type=type_hints["attribute_position"])
            check_type(argname="argument bracket_same_line", value=bracket_same_line, expected_type=type_hints["bracket_same_line"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument indent_script_and_style", value=indent_script_and_style, expected_type=type_hints["indent_script_and_style"])
            check_type(argname="argument indent_style", value=indent_style, expected_type=type_hints["indent_style"])
            check_type(argname="argument indent_width", value=indent_width, expected_type=type_hints["indent_width"])
            check_type(argname="argument line_ending", value=line_ending, expected_type=type_hints["line_ending"])
            check_type(argname="argument line_width", value=line_width, expected_type=type_hints["line_width"])
            check_type(argname="argument self_close_void_elements", value=self_close_void_elements, expected_type=type_hints["self_close_void_elements"])
            check_type(argname="argument whitespace_sensitivity", value=whitespace_sensitivity, expected_type=type_hints["whitespace_sensitivity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attribute_position is not None:
            self._values["attribute_position"] = attribute_position
        if bracket_same_line is not None:
            self._values["bracket_same_line"] = bracket_same_line
        if enabled is not None:
            self._values["enabled"] = enabled
        if indent_script_and_style is not None:
            self._values["indent_script_and_style"] = indent_script_and_style
        if indent_style is not None:
            self._values["indent_style"] = indent_style
        if indent_width is not None:
            self._values["indent_width"] = indent_width
        if line_ending is not None:
            self._values["line_ending"] = line_ending
        if line_width is not None:
            self._values["line_width"] = line_width
        if self_close_void_elements is not None:
            self._values["self_close_void_elements"] = self_close_void_elements
        if whitespace_sensitivity is not None:
            self._values["whitespace_sensitivity"] = whitespace_sensitivity

    @builtins.property
    def attribute_position(self) -> typing.Optional[AttributePosition]:
        '''(experimental) The attribute position style in HTML elements.

        Defaults to auto.

        :default: auto.

        :stability: experimental
        :schema: HtmlFormatterConfiguration#attributePosition
        '''
        result = self._values.get("attribute_position")
        return typing.cast(typing.Optional[AttributePosition], result)

    @builtins.property
    def bracket_same_line(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to hug the closing bracket of multiline HTML tags to the end of the last line, rather than being alone on the following line.

        Defaults to false.

        :default: false.

        :stability: experimental
        :schema: HtmlFormatterConfiguration#bracketSameLine
        '''
        result = self._values.get("bracket_same_line")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the formatter for HTML (and its super languages) files.

        :stability: experimental
        :schema: HtmlFormatterConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def indent_script_and_style(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to indent the ``<script>`` and ``<style>`` tags for HTML (and its super languages).

        Defaults to false.

        :default: false.

        :stability: experimental
        :schema: HtmlFormatterConfiguration#indentScriptAndStyle
        '''
        result = self._values.get("indent_script_and_style")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def indent_style(self) -> typing.Optional["IndentStyle"]:
        '''(experimental) The indent style applied to HTML (and its super languages) files.

        :stability: experimental
        :schema: HtmlFormatterConfiguration#indentStyle
        '''
        result = self._values.get("indent_style")
        return typing.cast(typing.Optional["IndentStyle"], result)

    @builtins.property
    def indent_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation applied to HTML (and its super languages) files.

        Default to 2.

        :default: 2.

        :stability: experimental
        :schema: HtmlFormatterConfiguration#indentWidth
        '''
        result = self._values.get("indent_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def line_ending(self) -> typing.Optional["LineEnding"]:
        '''(experimental) The type of line ending applied to HTML (and its super languages) files.

        :stability: experimental
        :schema: HtmlFormatterConfiguration#lineEnding
        '''
        result = self._values.get("line_ending")
        return typing.cast(typing.Optional["LineEnding"], result)

    @builtins.property
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) What's the max width of a line applied to HTML (and its super languages) files.

        Defaults to 80.

        :default: 80.

        :stability: experimental
        :schema: HtmlFormatterConfiguration#lineWidth
        '''
        result = self._values.get("line_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def self_close_void_elements(self) -> typing.Optional["SelfCloseVoidElements"]:
        '''(experimental) Whether void elements should be self-closed.

        Defaults to never.

        :default: never.

        :stability: experimental
        :schema: HtmlFormatterConfiguration#selfCloseVoidElements
        '''
        result = self._values.get("self_close_void_elements")
        return typing.cast(typing.Optional["SelfCloseVoidElements"], result)

    @builtins.property
    def whitespace_sensitivity(self) -> typing.Optional["WhitespaceSensitivity"]:
        '''(experimental) Whether to account for whitespace sensitivity when formatting HTML (and its super languages).

        Defaults to "css".

        :default: css".

        :stability: experimental
        :schema: HtmlFormatterConfiguration#whitespaceSensitivity
        '''
        result = self._values.get("whitespace_sensitivity")
        return typing.cast(typing.Optional["WhitespaceSensitivity"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HtmlFormatterConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.HtmlParserConfiguration",
    jsii_struct_bases=[],
    name_mapping={"interpolation": "interpolation"},
)
class HtmlParserConfiguration:
    def __init__(self, *, interpolation: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Options that changes how the HTML parser behaves.

        :param interpolation: (experimental) Enables the parsing of double text expressions such as ``{{ expression }}`` inside ``.html`` files.

        :stability: experimental
        :schema: HtmlParserConfiguration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b3cfca5c3ad8f608b86ade05d476530f16da0ba23410a7613236950da38ff37)
            check_type(argname="argument interpolation", value=interpolation, expected_type=type_hints["interpolation"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if interpolation is not None:
            self._values["interpolation"] = interpolation

    @builtins.property
    def interpolation(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables the parsing of double text expressions such as ``{{ expression }}`` inside ``.html`` files.

        :stability: experimental
        :schema: HtmlParserConfiguration#interpolation
        '''
        result = self._values.get("interpolation")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HtmlParserConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.javascript.biome_config.IndentStyle")
class IndentStyle(enum.Enum):
    '''
    :stability: experimental
    :schema: IndentStyle
    '''

    TAB = "TAB"
    '''(experimental) tab.

    :stability: experimental
    '''
    SPACE = "SPACE"
    '''(experimental) space.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.JsAssistConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class JsAssistConfiguration:
    def __init__(self, *, enabled: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Assist options specific to the JavaScript assist.

        :param enabled: (experimental) Control the assist for JavaScript (and its super languages) files.

        :stability: experimental
        :schema: JsAssistConfiguration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a425594ed8c46868c14fe924e8346d0d10c110ecabdc7f0d160d30bb06cf91ea)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the assist for JavaScript (and its super languages) files.

        :stability: experimental
        :schema: JsAssistConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JsAssistConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.JsConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "assist": "assist",
        "formatter": "formatter",
        "globals": "globals",
        "jsx_runtime": "jsxRuntime",
        "linter": "linter",
        "parser": "parser",
    },
)
class JsConfiguration:
    def __init__(
        self,
        *,
        assist: typing.Optional[typing.Union[JsAssistConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        formatter: typing.Optional[typing.Union["JsFormatterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        globals: typing.Optional[typing.Sequence[builtins.str]] = None,
        jsx_runtime: typing.Optional["JsxRuntime"] = None,
        linter: typing.Optional[typing.Union["JsLinterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        parser: typing.Optional[typing.Union["JsParserConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) A set of options applied to the JavaScript files.

        :param assist: (experimental) Assist options.
        :param formatter: (experimental) Formatting options.
        :param globals: (experimental) A list of global bindings that should be ignored by the analyzers. If defined here, they should not emit diagnostics.
        :param jsx_runtime: (experimental) Indicates the type of runtime or transformation used for interpreting JSX.
        :param linter: (experimental) Linter options.
        :param parser: (experimental) Parsing options.

        :stability: experimental
        :schema: JsConfiguration
        '''
        if isinstance(assist, dict):
            assist = JsAssistConfiguration(**assist)
        if isinstance(formatter, dict):
            formatter = JsFormatterConfiguration(**formatter)
        if isinstance(linter, dict):
            linter = JsLinterConfiguration(**linter)
        if isinstance(parser, dict):
            parser = JsParserConfiguration(**parser)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57972f7094bf127a9fb1918efc38b7f9fd8b7e2a28387b1d59645ced7024c16b)
            check_type(argname="argument assist", value=assist, expected_type=type_hints["assist"])
            check_type(argname="argument formatter", value=formatter, expected_type=type_hints["formatter"])
            check_type(argname="argument globals", value=globals, expected_type=type_hints["globals"])
            check_type(argname="argument jsx_runtime", value=jsx_runtime, expected_type=type_hints["jsx_runtime"])
            check_type(argname="argument linter", value=linter, expected_type=type_hints["linter"])
            check_type(argname="argument parser", value=parser, expected_type=type_hints["parser"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assist is not None:
            self._values["assist"] = assist
        if formatter is not None:
            self._values["formatter"] = formatter
        if globals is not None:
            self._values["globals"] = globals
        if jsx_runtime is not None:
            self._values["jsx_runtime"] = jsx_runtime
        if linter is not None:
            self._values["linter"] = linter
        if parser is not None:
            self._values["parser"] = parser

    @builtins.property
    def assist(self) -> typing.Optional[JsAssistConfiguration]:
        '''(experimental) Assist options.

        :stability: experimental
        :schema: JsConfiguration#assist
        '''
        result = self._values.get("assist")
        return typing.cast(typing.Optional[JsAssistConfiguration], result)

    @builtins.property
    def formatter(self) -> typing.Optional["JsFormatterConfiguration"]:
        '''(experimental) Formatting options.

        :stability: experimental
        :schema: JsConfiguration#formatter
        '''
        result = self._values.get("formatter")
        return typing.cast(typing.Optional["JsFormatterConfiguration"], result)

    @builtins.property
    def globals(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of global bindings that should be ignored by the analyzers.

        If defined here, they should not emit diagnostics.

        :stability: experimental
        :schema: JsConfiguration#globals
        '''
        result = self._values.get("globals")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def jsx_runtime(self) -> typing.Optional["JsxRuntime"]:
        '''(experimental) Indicates the type of runtime or transformation used for interpreting JSX.

        :stability: experimental
        :schema: JsConfiguration#jsxRuntime
        '''
        result = self._values.get("jsx_runtime")
        return typing.cast(typing.Optional["JsxRuntime"], result)

    @builtins.property
    def linter(self) -> typing.Optional["JsLinterConfiguration"]:
        '''(experimental) Linter options.

        :stability: experimental
        :schema: JsConfiguration#linter
        '''
        result = self._values.get("linter")
        return typing.cast(typing.Optional["JsLinterConfiguration"], result)

    @builtins.property
    def parser(self) -> typing.Optional["JsParserConfiguration"]:
        '''(experimental) Parsing options.

        :stability: experimental
        :schema: JsConfiguration#parser
        '''
        result = self._values.get("parser")
        return typing.cast(typing.Optional["JsParserConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JsConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.JsFormatterConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "arrow_parentheses": "arrowParentheses",
        "attribute_position": "attributePosition",
        "bracket_same_line": "bracketSameLine",
        "bracket_spacing": "bracketSpacing",
        "enabled": "enabled",
        "expand": "expand",
        "indent_style": "indentStyle",
        "indent_width": "indentWidth",
        "jsx_quote_style": "jsxQuoteStyle",
        "line_ending": "lineEnding",
        "line_width": "lineWidth",
        "operator_linebreak": "operatorLinebreak",
        "quote_properties": "quoteProperties",
        "quote_style": "quoteStyle",
        "semicolons": "semicolons",
        "trailing_commas": "trailingCommas",
    },
)
class JsFormatterConfiguration:
    def __init__(
        self,
        *,
        arrow_parentheses: typing.Optional[ArrowParentheses] = None,
        attribute_position: typing.Optional[AttributePosition] = None,
        bracket_same_line: typing.Optional[builtins.bool] = None,
        bracket_spacing: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        expand: typing.Optional[Expand] = None,
        indent_style: typing.Optional[IndentStyle] = None,
        indent_width: typing.Optional[jsii.Number] = None,
        jsx_quote_style: typing.Optional["QuoteStyle"] = None,
        line_ending: typing.Optional["LineEnding"] = None,
        line_width: typing.Optional[jsii.Number] = None,
        operator_linebreak: typing.Optional["OperatorLinebreak"] = None,
        quote_properties: typing.Optional["QuoteProperties"] = None,
        quote_style: typing.Optional["QuoteStyle"] = None,
        semicolons: typing.Optional["Semicolons"] = None,
        trailing_commas: typing.Optional["TrailingCommas"] = None,
    ) -> None:
        '''(experimental) Formatting options specific to the JavaScript files.

        :param arrow_parentheses: (experimental) Whether to add non-necessary parentheses to arrow functions. Defaults to "always". Default: always".
        :param attribute_position: (experimental) The attribute position style in JSX elements. Defaults to auto. Default: auto.
        :param bracket_same_line: (experimental) Whether to hug the closing bracket of multiline HTML/JSX tags to the end of the last line, rather than being alone on the following line. Defaults to false. Default: false.
        :param bracket_spacing: (experimental) Whether to insert spaces around brackets in object literals. Defaults to true. Default: true.
        :param enabled: (experimental) Control the formatter for JavaScript (and its super languages) files.
        :param expand: (experimental) Whether to expand arrays and objects on multiple lines. When set to ``auto``, object literals are formatted on multiple lines if the first property has a newline, and array literals are formatted on a single line if it fits in the line. When set to ``always``, these literals are formatted on multiple lines, regardless of length of the list. When set to ``never``, these literals are formatted on a single line if it fits in the line. When formatting ``package.json``, Biome will use ``always`` unless configured otherwise. Defaults to "auto". Default: auto".
        :param indent_style: (experimental) The indent style applied to JavaScript (and its super languages) files.
        :param indent_width: (experimental) The size of the indentation applied to JavaScript (and its super languages) files. Default to 2. Default: 2.
        :param jsx_quote_style: (experimental) The type of quotes used in JSX. Defaults to double. Default: double.
        :param line_ending: (experimental) The type of line ending applied to JavaScript (and its super languages) files.
        :param line_width: (experimental) What's the max width of a line applied to JavaScript (and its super languages) files. Defaults to 80. Default: 80.
        :param operator_linebreak: (experimental) When breaking binary expressions into multiple lines, whether to break them before or after the binary operator. Defaults to "after". Default: after".
        :param quote_properties: (experimental) When properties in objects are quoted. Defaults to asNeeded. Default: asNeeded.
        :param quote_style: (experimental) The type of quotes used in JavaScript code. Defaults to double. Default: double.
        :param semicolons: (experimental) Whether the formatter prints semicolons for all statements or only in for statements where it is necessary because of ASI.
        :param trailing_commas: (experimental) Print trailing commas wherever possible in multi-line comma-separated syntactic structures. Defaults to "all". Default: all".

        :stability: experimental
        :schema: JsFormatterConfiguration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83d4960ad9dc84017b237fabc105d7837e8a3ec56d19b1de7e01183651d05de1)
            check_type(argname="argument arrow_parentheses", value=arrow_parentheses, expected_type=type_hints["arrow_parentheses"])
            check_type(argname="argument attribute_position", value=attribute_position, expected_type=type_hints["attribute_position"])
            check_type(argname="argument bracket_same_line", value=bracket_same_line, expected_type=type_hints["bracket_same_line"])
            check_type(argname="argument bracket_spacing", value=bracket_spacing, expected_type=type_hints["bracket_spacing"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument expand", value=expand, expected_type=type_hints["expand"])
            check_type(argname="argument indent_style", value=indent_style, expected_type=type_hints["indent_style"])
            check_type(argname="argument indent_width", value=indent_width, expected_type=type_hints["indent_width"])
            check_type(argname="argument jsx_quote_style", value=jsx_quote_style, expected_type=type_hints["jsx_quote_style"])
            check_type(argname="argument line_ending", value=line_ending, expected_type=type_hints["line_ending"])
            check_type(argname="argument line_width", value=line_width, expected_type=type_hints["line_width"])
            check_type(argname="argument operator_linebreak", value=operator_linebreak, expected_type=type_hints["operator_linebreak"])
            check_type(argname="argument quote_properties", value=quote_properties, expected_type=type_hints["quote_properties"])
            check_type(argname="argument quote_style", value=quote_style, expected_type=type_hints["quote_style"])
            check_type(argname="argument semicolons", value=semicolons, expected_type=type_hints["semicolons"])
            check_type(argname="argument trailing_commas", value=trailing_commas, expected_type=type_hints["trailing_commas"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if arrow_parentheses is not None:
            self._values["arrow_parentheses"] = arrow_parentheses
        if attribute_position is not None:
            self._values["attribute_position"] = attribute_position
        if bracket_same_line is not None:
            self._values["bracket_same_line"] = bracket_same_line
        if bracket_spacing is not None:
            self._values["bracket_spacing"] = bracket_spacing
        if enabled is not None:
            self._values["enabled"] = enabled
        if expand is not None:
            self._values["expand"] = expand
        if indent_style is not None:
            self._values["indent_style"] = indent_style
        if indent_width is not None:
            self._values["indent_width"] = indent_width
        if jsx_quote_style is not None:
            self._values["jsx_quote_style"] = jsx_quote_style
        if line_ending is not None:
            self._values["line_ending"] = line_ending
        if line_width is not None:
            self._values["line_width"] = line_width
        if operator_linebreak is not None:
            self._values["operator_linebreak"] = operator_linebreak
        if quote_properties is not None:
            self._values["quote_properties"] = quote_properties
        if quote_style is not None:
            self._values["quote_style"] = quote_style
        if semicolons is not None:
            self._values["semicolons"] = semicolons
        if trailing_commas is not None:
            self._values["trailing_commas"] = trailing_commas

    @builtins.property
    def arrow_parentheses(self) -> typing.Optional[ArrowParentheses]:
        '''(experimental) Whether to add non-necessary parentheses to arrow functions.

        Defaults to "always".

        :default: always".

        :stability: experimental
        :schema: JsFormatterConfiguration#arrowParentheses
        '''
        result = self._values.get("arrow_parentheses")
        return typing.cast(typing.Optional[ArrowParentheses], result)

    @builtins.property
    def attribute_position(self) -> typing.Optional[AttributePosition]:
        '''(experimental) The attribute position style in JSX elements.

        Defaults to auto.

        :default: auto.

        :stability: experimental
        :schema: JsFormatterConfiguration#attributePosition
        '''
        result = self._values.get("attribute_position")
        return typing.cast(typing.Optional[AttributePosition], result)

    @builtins.property
    def bracket_same_line(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to hug the closing bracket of multiline HTML/JSX tags to the end of the last line, rather than being alone on the following line.

        Defaults to false.

        :default: false.

        :stability: experimental
        :schema: JsFormatterConfiguration#bracketSameLine
        '''
        result = self._values.get("bracket_same_line")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def bracket_spacing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to insert spaces around brackets in object literals.

        Defaults to true.

        :default: true.

        :stability: experimental
        :schema: JsFormatterConfiguration#bracketSpacing
        '''
        result = self._values.get("bracket_spacing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the formatter for JavaScript (and its super languages) files.

        :stability: experimental
        :schema: JsFormatterConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def expand(self) -> typing.Optional[Expand]:
        '''(experimental) Whether to expand arrays and objects on multiple lines.

        When set to ``auto``, object literals are formatted on multiple lines if the first property has a newline, and array literals are formatted on a single line if it fits in the line. When set to ``always``, these literals are formatted on multiple lines, regardless of length of the list. When set to ``never``, these literals are formatted on a single line if it fits in the line. When formatting ``package.json``, Biome will use ``always`` unless configured otherwise. Defaults to "auto".

        :default: auto".

        :stability: experimental
        :schema: JsFormatterConfiguration#expand
        '''
        result = self._values.get("expand")
        return typing.cast(typing.Optional[Expand], result)

    @builtins.property
    def indent_style(self) -> typing.Optional[IndentStyle]:
        '''(experimental) The indent style applied to JavaScript (and its super languages) files.

        :stability: experimental
        :schema: JsFormatterConfiguration#indentStyle
        '''
        result = self._values.get("indent_style")
        return typing.cast(typing.Optional[IndentStyle], result)

    @builtins.property
    def indent_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation applied to JavaScript (and its super languages) files.

        Default to 2.

        :default: 2.

        :stability: experimental
        :schema: JsFormatterConfiguration#indentWidth
        '''
        result = self._values.get("indent_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def jsx_quote_style(self) -> typing.Optional["QuoteStyle"]:
        '''(experimental) The type of quotes used in JSX.

        Defaults to double.

        :default: double.

        :stability: experimental
        :schema: JsFormatterConfiguration#jsxQuoteStyle
        '''
        result = self._values.get("jsx_quote_style")
        return typing.cast(typing.Optional["QuoteStyle"], result)

    @builtins.property
    def line_ending(self) -> typing.Optional["LineEnding"]:
        '''(experimental) The type of line ending applied to JavaScript (and its super languages) files.

        :stability: experimental
        :schema: JsFormatterConfiguration#lineEnding
        '''
        result = self._values.get("line_ending")
        return typing.cast(typing.Optional["LineEnding"], result)

    @builtins.property
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) What's the max width of a line applied to JavaScript (and its super languages) files.

        Defaults to 80.

        :default: 80.

        :stability: experimental
        :schema: JsFormatterConfiguration#lineWidth
        '''
        result = self._values.get("line_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def operator_linebreak(self) -> typing.Optional["OperatorLinebreak"]:
        '''(experimental) When breaking binary expressions into multiple lines, whether to break them before or after the binary operator.

        Defaults to "after".

        :default: after".

        :stability: experimental
        :schema: JsFormatterConfiguration#operatorLinebreak
        '''
        result = self._values.get("operator_linebreak")
        return typing.cast(typing.Optional["OperatorLinebreak"], result)

    @builtins.property
    def quote_properties(self) -> typing.Optional["QuoteProperties"]:
        '''(experimental) When properties in objects are quoted.

        Defaults to asNeeded.

        :default: asNeeded.

        :stability: experimental
        :schema: JsFormatterConfiguration#quoteProperties
        '''
        result = self._values.get("quote_properties")
        return typing.cast(typing.Optional["QuoteProperties"], result)

    @builtins.property
    def quote_style(self) -> typing.Optional["QuoteStyle"]:
        '''(experimental) The type of quotes used in JavaScript code.

        Defaults to double.

        :default: double.

        :stability: experimental
        :schema: JsFormatterConfiguration#quoteStyle
        '''
        result = self._values.get("quote_style")
        return typing.cast(typing.Optional["QuoteStyle"], result)

    @builtins.property
    def semicolons(self) -> typing.Optional["Semicolons"]:
        '''(experimental) Whether the formatter prints semicolons for all statements or only in for statements where it is necessary because of ASI.

        :stability: experimental
        :schema: JsFormatterConfiguration#semicolons
        '''
        result = self._values.get("semicolons")
        return typing.cast(typing.Optional["Semicolons"], result)

    @builtins.property
    def trailing_commas(self) -> typing.Optional["TrailingCommas"]:
        '''(experimental) Print trailing commas wherever possible in multi-line comma-separated syntactic structures.

        Defaults to "all".

        :default: all".

        :stability: experimental
        :schema: JsFormatterConfiguration#trailingCommas
        '''
        result = self._values.get("trailing_commas")
        return typing.cast(typing.Optional["TrailingCommas"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JsFormatterConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.JsLinterConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class JsLinterConfiguration:
    def __init__(self, *, enabled: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Linter options specific to the JavaScript linter.

        :param enabled: (experimental) Control the linter for JavaScript (and its super languages) files.

        :stability: experimental
        :schema: JsLinterConfiguration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f73a12c3631a151ee57c8ecf68020468207f1fa3a6b5c91890a93814a4119533)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the linter for JavaScript (and its super languages) files.

        :stability: experimental
        :schema: JsLinterConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JsLinterConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.JsParserConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "grit_metavariables": "gritMetavariables",
        "jsx_everywhere": "jsxEverywhere",
        "unsafe_parameter_decorators_enabled": "unsafeParameterDecoratorsEnabled",
    },
)
class JsParserConfiguration:
    def __init__(
        self,
        *,
        grit_metavariables: typing.Optional[builtins.bool] = None,
        jsx_everywhere: typing.Optional[builtins.bool] = None,
        unsafe_parameter_decorators_enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options that changes how the JavaScript parser behaves.

        :param grit_metavariables: (experimental) Enables parsing of Grit metavariables. Defaults to ``false``. Default: false`.
        :param jsx_everywhere: (experimental) When enabled, files like ``.js``/``.mjs``/``.cjs`` may contain JSX syntax. Defaults to ``true``. Default: true`.
        :param unsafe_parameter_decorators_enabled: (experimental) It enables the experimental and unsafe parsing of parameter decorators. These decorators belong to an old proposal, and they are subject to change.

        :stability: experimental
        :schema: JsParserConfiguration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c08c2e4162829556526f51e35e2cd7194c2c8bab38e0d01775d808ad7d573450)
            check_type(argname="argument grit_metavariables", value=grit_metavariables, expected_type=type_hints["grit_metavariables"])
            check_type(argname="argument jsx_everywhere", value=jsx_everywhere, expected_type=type_hints["jsx_everywhere"])
            check_type(argname="argument unsafe_parameter_decorators_enabled", value=unsafe_parameter_decorators_enabled, expected_type=type_hints["unsafe_parameter_decorators_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if grit_metavariables is not None:
            self._values["grit_metavariables"] = grit_metavariables
        if jsx_everywhere is not None:
            self._values["jsx_everywhere"] = jsx_everywhere
        if unsafe_parameter_decorators_enabled is not None:
            self._values["unsafe_parameter_decorators_enabled"] = unsafe_parameter_decorators_enabled

    @builtins.property
    def grit_metavariables(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables parsing of Grit metavariables.

        Defaults to ``false``.

        :default: false`.

        :stability: experimental
        :schema: JsParserConfiguration#gritMetavariables
        '''
        result = self._values.get("grit_metavariables")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def jsx_everywhere(self) -> typing.Optional[builtins.bool]:
        '''(experimental) When enabled, files like ``.js``/``.mjs``/``.cjs`` may contain JSX syntax.

        Defaults to ``true``.

        :default: true`.

        :stability: experimental
        :schema: JsParserConfiguration#jsxEverywhere
        '''
        result = self._values.get("jsx_everywhere")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def unsafe_parameter_decorators_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables the experimental and unsafe parsing of parameter decorators.

        These decorators belong to an old proposal, and they are subject to change.

        :stability: experimental
        :schema: JsParserConfiguration#unsafeParameterDecoratorsEnabled
        '''
        result = self._values.get("unsafe_parameter_decorators_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JsParserConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.JsonAssistConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class JsonAssistConfiguration:
    def __init__(self, *, enabled: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Linter options specific to the JSON linter.

        :param enabled: (experimental) Control the assist for JSON (and its super languages) files.

        :stability: experimental
        :schema: JsonAssistConfiguration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1fb6aa8858788da93c40533dca490e5cba8b040cbde40fcc78bbd02d8efd181)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the assist for JSON (and its super languages) files.

        :stability: experimental
        :schema: JsonAssistConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JsonAssistConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.JsonConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "assist": "assist",
        "formatter": "formatter",
        "linter": "linter",
        "parser": "parser",
    },
)
class JsonConfiguration:
    def __init__(
        self,
        *,
        assist: typing.Optional[typing.Union[JsonAssistConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        formatter: typing.Optional[typing.Union["JsonFormatterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        linter: typing.Optional[typing.Union["JsonLinterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        parser: typing.Optional[typing.Union["JsonParserConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options applied to JSON files.

        :param assist: (experimental) Assist options.
        :param formatter: (experimental) Formatting options.
        :param linter: (experimental) Linting options.
        :param parser: (experimental) Parsing options.

        :stability: experimental
        :schema: JsonConfiguration
        '''
        if isinstance(assist, dict):
            assist = JsonAssistConfiguration(**assist)
        if isinstance(formatter, dict):
            formatter = JsonFormatterConfiguration(**formatter)
        if isinstance(linter, dict):
            linter = JsonLinterConfiguration(**linter)
        if isinstance(parser, dict):
            parser = JsonParserConfiguration(**parser)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67ca83a8b26135c2a9bc9fcca08d39f860187439c18546ca3bb66035d3ec1146)
            check_type(argname="argument assist", value=assist, expected_type=type_hints["assist"])
            check_type(argname="argument formatter", value=formatter, expected_type=type_hints["formatter"])
            check_type(argname="argument linter", value=linter, expected_type=type_hints["linter"])
            check_type(argname="argument parser", value=parser, expected_type=type_hints["parser"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assist is not None:
            self._values["assist"] = assist
        if formatter is not None:
            self._values["formatter"] = formatter
        if linter is not None:
            self._values["linter"] = linter
        if parser is not None:
            self._values["parser"] = parser

    @builtins.property
    def assist(self) -> typing.Optional[JsonAssistConfiguration]:
        '''(experimental) Assist options.

        :stability: experimental
        :schema: JsonConfiguration#assist
        '''
        result = self._values.get("assist")
        return typing.cast(typing.Optional[JsonAssistConfiguration], result)

    @builtins.property
    def formatter(self) -> typing.Optional["JsonFormatterConfiguration"]:
        '''(experimental) Formatting options.

        :stability: experimental
        :schema: JsonConfiguration#formatter
        '''
        result = self._values.get("formatter")
        return typing.cast(typing.Optional["JsonFormatterConfiguration"], result)

    @builtins.property
    def linter(self) -> typing.Optional["JsonLinterConfiguration"]:
        '''(experimental) Linting options.

        :stability: experimental
        :schema: JsonConfiguration#linter
        '''
        result = self._values.get("linter")
        return typing.cast(typing.Optional["JsonLinterConfiguration"], result)

    @builtins.property
    def parser(self) -> typing.Optional["JsonParserConfiguration"]:
        '''(experimental) Parsing options.

        :stability: experimental
        :schema: JsonConfiguration#parser
        '''
        result = self._values.get("parser")
        return typing.cast(typing.Optional["JsonParserConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JsonConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.JsonFormatterConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "bracket_spacing": "bracketSpacing",
        "enabled": "enabled",
        "expand": "expand",
        "indent_style": "indentStyle",
        "indent_width": "indentWidth",
        "line_ending": "lineEnding",
        "line_width": "lineWidth",
        "trailing_commas": "trailingCommas",
    },
)
class JsonFormatterConfiguration:
    def __init__(
        self,
        *,
        bracket_spacing: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        expand: typing.Optional[Expand] = None,
        indent_style: typing.Optional[IndentStyle] = None,
        indent_width: typing.Optional[jsii.Number] = None,
        line_ending: typing.Optional["LineEnding"] = None,
        line_width: typing.Optional[jsii.Number] = None,
        trailing_commas: typing.Optional["TrailingCommas2"] = None,
    ) -> None:
        '''
        :param bracket_spacing: (experimental) Whether to insert spaces around brackets in object literals. Defaults to true. Default: true.
        :param enabled: (experimental) Control the formatter for JSON (and its super languages) files.
        :param expand: (experimental) Whether to expand arrays and objects on multiple lines. When set to ``auto``, object literals are formatted on multiple lines if the first property has a newline, and array literals are formatted on a single line if it fits in the line. When set to ``always``, these literals are formatted on multiple lines, regardless of length of the list. When set to ``never``, these literals are formatted on a single line if it fits in the line. When formatting ``package.json``, Biome will use ``always`` unless configured otherwise. Defaults to "auto". Default: auto".
        :param indent_style: (experimental) The indent style applied to JSON (and its super languages) files.
        :param indent_width: (experimental) The size of the indentation applied to JSON (and its super languages) files. Default to 2. Default: 2.
        :param line_ending: (experimental) The type of line ending applied to JSON (and its super languages) files.
        :param line_width: (experimental) What's the max width of a line applied to JSON (and its super languages) files. Defaults to 80. Default: 80.
        :param trailing_commas: (experimental) Print trailing commas wherever possible in multi-line comma-separated syntactic structures. Defaults to "none". Default: none".

        :stability: experimental
        :schema: JsonFormatterConfiguration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a0473ff26e9f0e1a38d7055c4e466dc2b2b92f24abfce11672601c5a1f6f4a2)
            check_type(argname="argument bracket_spacing", value=bracket_spacing, expected_type=type_hints["bracket_spacing"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument expand", value=expand, expected_type=type_hints["expand"])
            check_type(argname="argument indent_style", value=indent_style, expected_type=type_hints["indent_style"])
            check_type(argname="argument indent_width", value=indent_width, expected_type=type_hints["indent_width"])
            check_type(argname="argument line_ending", value=line_ending, expected_type=type_hints["line_ending"])
            check_type(argname="argument line_width", value=line_width, expected_type=type_hints["line_width"])
            check_type(argname="argument trailing_commas", value=trailing_commas, expected_type=type_hints["trailing_commas"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bracket_spacing is not None:
            self._values["bracket_spacing"] = bracket_spacing
        if enabled is not None:
            self._values["enabled"] = enabled
        if expand is not None:
            self._values["expand"] = expand
        if indent_style is not None:
            self._values["indent_style"] = indent_style
        if indent_width is not None:
            self._values["indent_width"] = indent_width
        if line_ending is not None:
            self._values["line_ending"] = line_ending
        if line_width is not None:
            self._values["line_width"] = line_width
        if trailing_commas is not None:
            self._values["trailing_commas"] = trailing_commas

    @builtins.property
    def bracket_spacing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to insert spaces around brackets in object literals.

        Defaults to true.

        :default: true.

        :stability: experimental
        :schema: JsonFormatterConfiguration#bracketSpacing
        '''
        result = self._values.get("bracket_spacing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the formatter for JSON (and its super languages) files.

        :stability: experimental
        :schema: JsonFormatterConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def expand(self) -> typing.Optional[Expand]:
        '''(experimental) Whether to expand arrays and objects on multiple lines.

        When set to ``auto``, object literals are formatted on multiple lines if the first property has a newline, and array literals are formatted on a single line if it fits in the line. When set to ``always``, these literals are formatted on multiple lines, regardless of length of the list. When set to ``never``, these literals are formatted on a single line if it fits in the line. When formatting ``package.json``, Biome will use ``always`` unless configured otherwise. Defaults to "auto".

        :default: auto".

        :stability: experimental
        :schema: JsonFormatterConfiguration#expand
        '''
        result = self._values.get("expand")
        return typing.cast(typing.Optional[Expand], result)

    @builtins.property
    def indent_style(self) -> typing.Optional[IndentStyle]:
        '''(experimental) The indent style applied to JSON (and its super languages) files.

        :stability: experimental
        :schema: JsonFormatterConfiguration#indentStyle
        '''
        result = self._values.get("indent_style")
        return typing.cast(typing.Optional[IndentStyle], result)

    @builtins.property
    def indent_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation applied to JSON (and its super languages) files.

        Default to 2.

        :default: 2.

        :stability: experimental
        :schema: JsonFormatterConfiguration#indentWidth
        '''
        result = self._values.get("indent_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def line_ending(self) -> typing.Optional["LineEnding"]:
        '''(experimental) The type of line ending applied to JSON (and its super languages) files.

        :stability: experimental
        :schema: JsonFormatterConfiguration#lineEnding
        '''
        result = self._values.get("line_ending")
        return typing.cast(typing.Optional["LineEnding"], result)

    @builtins.property
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) What's the max width of a line applied to JSON (and its super languages) files.

        Defaults to 80.

        :default: 80.

        :stability: experimental
        :schema: JsonFormatterConfiguration#lineWidth
        '''
        result = self._values.get("line_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def trailing_commas(self) -> typing.Optional["TrailingCommas2"]:
        '''(experimental) Print trailing commas wherever possible in multi-line comma-separated syntactic structures.

        Defaults to "none".

        :default: none".

        :stability: experimental
        :schema: JsonFormatterConfiguration#trailingCommas
        '''
        result = self._values.get("trailing_commas")
        return typing.cast(typing.Optional["TrailingCommas2"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JsonFormatterConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.JsonLinterConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class JsonLinterConfiguration:
    def __init__(self, *, enabled: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Linter options specific to the JSON linter.

        :param enabled: (experimental) Control the linter for JSON (and its super languages) files.

        :stability: experimental
        :schema: JsonLinterConfiguration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__850ce6cbde62685594cc979eca53b2938f923a2a6a9d3168729c891046c7be59)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the linter for JSON (and its super languages) files.

        :stability: experimental
        :schema: JsonLinterConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JsonLinterConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.JsonParserConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "allow_comments": "allowComments",
        "allow_trailing_commas": "allowTrailingCommas",
    },
)
class JsonParserConfiguration:
    def __init__(
        self,
        *,
        allow_comments: typing.Optional[builtins.bool] = None,
        allow_trailing_commas: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options that changes how the JSON parser behaves.

        :param allow_comments: (experimental) Allow parsing comments in ``.json`` files.
        :param allow_trailing_commas: (experimental) Allow parsing trailing commas in ``.json`` files.

        :stability: experimental
        :schema: JsonParserConfiguration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ced0fa0672bed168a8348653ba985dd1a20d26c25f814d1492bdc2bb5b05233)
            check_type(argname="argument allow_comments", value=allow_comments, expected_type=type_hints["allow_comments"])
            check_type(argname="argument allow_trailing_commas", value=allow_trailing_commas, expected_type=type_hints["allow_trailing_commas"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_comments is not None:
            self._values["allow_comments"] = allow_comments
        if allow_trailing_commas is not None:
            self._values["allow_trailing_commas"] = allow_trailing_commas

    @builtins.property
    def allow_comments(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allow parsing comments in ``.json`` files.

        :stability: experimental
        :schema: JsonParserConfiguration#allowComments
        '''
        result = self._values.get("allow_comments")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def allow_trailing_commas(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allow parsing trailing commas in ``.json`` files.

        :stability: experimental
        :schema: JsonParserConfiguration#allowTrailingCommas
        '''
        result = self._values.get("allow_trailing_commas")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JsonParserConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.javascript.biome_config.JsxRuntime")
class JsxRuntime(enum.Enum):
    '''(experimental) Indicates the type of runtime or transformation used for interpreting JSX.

    :stability: experimental
    :schema: JsxRuntime
    '''

    TRANSPARENT = "TRANSPARENT"
    '''(experimental) transparent.

    :stability: experimental
    '''
    REACT_CLASSIC = "REACT_CLASSIC"
    '''(experimental) reactClassic.

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.javascript.biome_config.LineEnding")
class LineEnding(enum.Enum):
    '''
    :stability: experimental
    :schema: LineEnding
    '''

    LF = "LF"
    '''(experimental) lf.

    :stability: experimental
    '''
    CRLF = "CRLF"
    '''(experimental) crlf.

    :stability: experimental
    '''
    CR = "CR"
    '''(experimental) cr.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.LinterConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "domains": "domains",
        "enabled": "enabled",
        "includes": "includes",
        "rules": "rules",
    },
)
class LinterConfiguration:
    def __init__(
        self,
        *,
        domains: typing.Optional[typing.Mapping[builtins.str, "RuleDomainValue"]] = None,
        enabled: typing.Optional[builtins.bool] = None,
        includes: typing.Optional[typing.Sequence[builtins.str]] = None,
        rules: typing.Optional[typing.Union["Rules", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param domains: (experimental) An object where the keys are the names of the domains, and the values are ``all``, ``recommended``, or ``none``.
        :param enabled: (experimental) if ``false``, it disables the feature and the linter won't be executed. ``true`` by default
        :param includes: (experimental) A list of glob patterns. The analyzer will handle only those files/folders that will match these patterns.
        :param rules: (experimental) List of rules.

        :stability: experimental
        :schema: LinterConfiguration
        '''
        if isinstance(rules, dict):
            rules = Rules(**rules)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65dab822a12255f6f845b9299f073f8d1333a90456c41e244f29210e8ad1de68)
            check_type(argname="argument domains", value=domains, expected_type=type_hints["domains"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument includes", value=includes, expected_type=type_hints["includes"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domains is not None:
            self._values["domains"] = domains
        if enabled is not None:
            self._values["enabled"] = enabled
        if includes is not None:
            self._values["includes"] = includes
        if rules is not None:
            self._values["rules"] = rules

    @builtins.property
    def domains(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "RuleDomainValue"]]:
        '''(experimental) An object where the keys are the names of the domains, and the values are ``all``, ``recommended``, or ``none``.

        :stability: experimental
        :schema: LinterConfiguration#domains
        '''
        result = self._values.get("domains")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "RuleDomainValue"]], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) if ``false``, it disables the feature and the linter won't be executed.

        ``true`` by default

        :stability: experimental
        :schema: LinterConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def includes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of glob patterns.

        The analyzer will handle only those files/folders that will match these patterns.

        :stability: experimental
        :schema: LinterConfiguration#includes
        '''
        result = self._values.get("includes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def rules(self) -> typing.Optional["Rules"]:
        '''(experimental) List of rules.

        :stability: experimental
        :schema: LinterConfiguration#rules
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional["Rules"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LinterConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.javascript.biome_config.OperatorLinebreak")
class OperatorLinebreak(enum.Enum):
    '''
    :stability: experimental
    :schema: OperatorLinebreak
    '''

    AFTER = "AFTER"
    '''(experimental) after.

    :stability: experimental
    '''
    BEFORE = "BEFORE"
    '''(experimental) before.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.OverrideAssistConfiguration",
    jsii_struct_bases=[],
    name_mapping={"actions": "actions", "enabled": "enabled"},
)
class OverrideAssistConfiguration:
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Union[Actions, typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param actions: (experimental) List of actions.
        :param enabled: (experimental) if ``false``, it disables the feature and the assist won't be executed. ``true`` by default

        :stability: experimental
        :schema: OverrideAssistConfiguration
        '''
        if isinstance(actions, dict):
            actions = Actions(**actions)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56dc91405fb970d58320a5a0025d8bde646c1421e2210fdd1d1f303623e06ef1)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def actions(self) -> typing.Optional[Actions]:
        '''(experimental) List of actions.

        :stability: experimental
        :schema: OverrideAssistConfiguration#actions
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[Actions], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) if ``false``, it disables the feature and the assist won't be executed.

        ``true`` by default

        :stability: experimental
        :schema: OverrideAssistConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OverrideAssistConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.OverrideFilesConfiguration",
    jsii_struct_bases=[],
    name_mapping={"max_size": "maxSize"},
)
class OverrideFilesConfiguration:
    def __init__(self, *, max_size: typing.Optional[jsii.Number] = None) -> None:
        '''
        :param max_size: (experimental) File size limit in bytes.

        :stability: experimental
        :schema: OverrideFilesConfiguration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26fa6398c015df15db0e8378e7692ad89fd6e1addf1ee19d970d8cd2eb5e64f3)
            check_type(argname="argument max_size", value=max_size, expected_type=type_hints["max_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_size is not None:
            self._values["max_size"] = max_size

    @builtins.property
    def max_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) File size limit in bytes.

        :stability: experimental
        :schema: OverrideFilesConfiguration#maxSize
        '''
        result = self._values.get("max_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OverrideFilesConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.OverrideFormatterConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "attribute_position": "attributePosition",
        "bracket_same_line": "bracketSameLine",
        "bracket_spacing": "bracketSpacing",
        "enabled": "enabled",
        "expand": "expand",
        "format_with_errors": "formatWithErrors",
        "indent_size": "indentSize",
        "indent_style": "indentStyle",
        "indent_width": "indentWidth",
        "line_ending": "lineEnding",
        "line_width": "lineWidth",
    },
)
class OverrideFormatterConfiguration:
    def __init__(
        self,
        *,
        attribute_position: typing.Optional[AttributePosition] = None,
        bracket_same_line: typing.Optional[builtins.bool] = None,
        bracket_spacing: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        expand: typing.Optional[Expand] = None,
        format_with_errors: typing.Optional[builtins.bool] = None,
        indent_size: typing.Optional[jsii.Number] = None,
        indent_style: typing.Optional[IndentStyle] = None,
        indent_width: typing.Optional[jsii.Number] = None,
        line_ending: typing.Optional[LineEnding] = None,
        line_width: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param attribute_position: (experimental) The attribute position style.
        :param bracket_same_line: (experimental) Put the ``>`` of a multi-line HTML or JSX element at the end of the last line instead of being alone on the next line (does not apply to self closing elements).
        :param bracket_spacing: (experimental) Whether to insert spaces around brackets in object literals. Defaults to true. Default: true.
        :param enabled: 
        :param expand: (experimental) Whether to expand arrays and objects on multiple lines. When set to ``auto``, object literals are formatted on multiple lines if the first property has a newline, and array literals are formatted on a single line if it fits in the line. When set to ``always``, these literals are formatted on multiple lines, regardless of length of the list. When set to ``never``, these literals are formatted on a single line if it fits in the line. When formatting ``package.json``, Biome will use ``always`` unless configured otherwise. Defaults to "auto". Default: auto".
        :param format_with_errors: (experimental) Stores whether formatting should be allowed to proceed if a given file has syntax errors.
        :param indent_size: (experimental) The size of the indentation, 2 by default (deprecated, use ``indent-width``).
        :param indent_style: (experimental) The indent style.
        :param indent_width: (experimental) The size of the indentation, 2 by default.
        :param line_ending: (experimental) The type of line ending.
        :param line_width: (experimental) What's the max width of a line. Defaults to 80. Default: 80.

        :stability: experimental
        :schema: OverrideFormatterConfiguration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3602eb22e2d33d64a65f4ebb15f534391f93d1e72546965c7be88c0c1e391655)
            check_type(argname="argument attribute_position", value=attribute_position, expected_type=type_hints["attribute_position"])
            check_type(argname="argument bracket_same_line", value=bracket_same_line, expected_type=type_hints["bracket_same_line"])
            check_type(argname="argument bracket_spacing", value=bracket_spacing, expected_type=type_hints["bracket_spacing"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument expand", value=expand, expected_type=type_hints["expand"])
            check_type(argname="argument format_with_errors", value=format_with_errors, expected_type=type_hints["format_with_errors"])
            check_type(argname="argument indent_size", value=indent_size, expected_type=type_hints["indent_size"])
            check_type(argname="argument indent_style", value=indent_style, expected_type=type_hints["indent_style"])
            check_type(argname="argument indent_width", value=indent_width, expected_type=type_hints["indent_width"])
            check_type(argname="argument line_ending", value=line_ending, expected_type=type_hints["line_ending"])
            check_type(argname="argument line_width", value=line_width, expected_type=type_hints["line_width"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attribute_position is not None:
            self._values["attribute_position"] = attribute_position
        if bracket_same_line is not None:
            self._values["bracket_same_line"] = bracket_same_line
        if bracket_spacing is not None:
            self._values["bracket_spacing"] = bracket_spacing
        if enabled is not None:
            self._values["enabled"] = enabled
        if expand is not None:
            self._values["expand"] = expand
        if format_with_errors is not None:
            self._values["format_with_errors"] = format_with_errors
        if indent_size is not None:
            self._values["indent_size"] = indent_size
        if indent_style is not None:
            self._values["indent_style"] = indent_style
        if indent_width is not None:
            self._values["indent_width"] = indent_width
        if line_ending is not None:
            self._values["line_ending"] = line_ending
        if line_width is not None:
            self._values["line_width"] = line_width

    @builtins.property
    def attribute_position(self) -> typing.Optional[AttributePosition]:
        '''(experimental) The attribute position style.

        :stability: experimental
        :schema: OverrideFormatterConfiguration#attributePosition
        '''
        result = self._values.get("attribute_position")
        return typing.cast(typing.Optional[AttributePosition], result)

    @builtins.property
    def bracket_same_line(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Put the ``>`` of a multi-line HTML or JSX element at the end of the last line instead of being alone on the next line (does not apply to self closing elements).

        :stability: experimental
        :schema: OverrideFormatterConfiguration#bracketSameLine
        '''
        result = self._values.get("bracket_same_line")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def bracket_spacing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to insert spaces around brackets in object literals.

        Defaults to true.

        :default: true.

        :stability: experimental
        :schema: OverrideFormatterConfiguration#bracketSpacing
        '''
        result = self._values.get("bracket_spacing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''
        :stability: experimental
        :schema: OverrideFormatterConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def expand(self) -> typing.Optional[Expand]:
        '''(experimental) Whether to expand arrays and objects on multiple lines.

        When set to ``auto``, object literals are formatted on multiple lines if the first property has a newline, and array literals are formatted on a single line if it fits in the line. When set to ``always``, these literals are formatted on multiple lines, regardless of length of the list. When set to ``never``, these literals are formatted on a single line if it fits in the line. When formatting ``package.json``, Biome will use ``always`` unless configured otherwise. Defaults to "auto".

        :default: auto".

        :stability: experimental
        :schema: OverrideFormatterConfiguration#expand
        '''
        result = self._values.get("expand")
        return typing.cast(typing.Optional[Expand], result)

    @builtins.property
    def format_with_errors(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Stores whether formatting should be allowed to proceed if a given file has syntax errors.

        :stability: experimental
        :schema: OverrideFormatterConfiguration#formatWithErrors
        '''
        result = self._values.get("format_with_errors")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def indent_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation, 2 by default (deprecated, use ``indent-width``).

        :stability: experimental
        :schema: OverrideFormatterConfiguration#indentSize
        '''
        result = self._values.get("indent_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def indent_style(self) -> typing.Optional[IndentStyle]:
        '''(experimental) The indent style.

        :stability: experimental
        :schema: OverrideFormatterConfiguration#indentStyle
        '''
        result = self._values.get("indent_style")
        return typing.cast(typing.Optional[IndentStyle], result)

    @builtins.property
    def indent_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation, 2 by default.

        :stability: experimental
        :schema: OverrideFormatterConfiguration#indentWidth
        '''
        result = self._values.get("indent_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def line_ending(self) -> typing.Optional[LineEnding]:
        '''(experimental) The type of line ending.

        :stability: experimental
        :schema: OverrideFormatterConfiguration#lineEnding
        '''
        result = self._values.get("line_ending")
        return typing.cast(typing.Optional[LineEnding], result)

    @builtins.property
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) What's the max width of a line.

        Defaults to 80.

        :default: 80.

        :stability: experimental
        :schema: OverrideFormatterConfiguration#lineWidth
        '''
        result = self._values.get("line_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OverrideFormatterConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.OverrideLinterConfiguration",
    jsii_struct_bases=[],
    name_mapping={"domains": "domains", "enabled": "enabled", "rules": "rules"},
)
class OverrideLinterConfiguration:
    def __init__(
        self,
        *,
        domains: typing.Optional[typing.Mapping[builtins.str, "RuleDomainValue"]] = None,
        enabled: typing.Optional[builtins.bool] = None,
        rules: typing.Optional[typing.Union["Rules", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param domains: (experimental) List of rules.
        :param enabled: (experimental) if ``false``, it disables the feature and the linter won't be executed. ``true`` by default
        :param rules: (experimental) List of rules.

        :stability: experimental
        :schema: OverrideLinterConfiguration
        '''
        if isinstance(rules, dict):
            rules = Rules(**rules)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b923acd3721838353ddf97d9a992327d3607a622afc36e911bc3eb842adb709)
            check_type(argname="argument domains", value=domains, expected_type=type_hints["domains"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domains is not None:
            self._values["domains"] = domains
        if enabled is not None:
            self._values["enabled"] = enabled
        if rules is not None:
            self._values["rules"] = rules

    @builtins.property
    def domains(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "RuleDomainValue"]]:
        '''(experimental) List of rules.

        :stability: experimental
        :schema: OverrideLinterConfiguration#domains
        '''
        result = self._values.get("domains")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "RuleDomainValue"]], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) if ``false``, it disables the feature and the linter won't be executed.

        ``true`` by default

        :stability: experimental
        :schema: OverrideLinterConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def rules(self) -> typing.Optional["Rules"]:
        '''(experimental) List of rules.

        :stability: experimental
        :schema: OverrideLinterConfiguration#rules
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional["Rules"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OverrideLinterConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.OverridePattern",
    jsii_struct_bases=[],
    name_mapping={
        "assist": "assist",
        "css": "css",
        "files": "files",
        "formatter": "formatter",
        "graphql": "graphql",
        "grit": "grit",
        "html": "html",
        "includes": "includes",
        "javascript": "javascript",
        "json": "json",
        "linter": "linter",
        "plugins": "plugins",
    },
)
class OverridePattern:
    def __init__(
        self,
        *,
        assist: typing.Optional[typing.Union[OverrideAssistConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        css: typing.Optional[typing.Union[CssConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        files: typing.Optional[typing.Union[OverrideFilesConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        formatter: typing.Optional[typing.Union[OverrideFormatterConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        graphql: typing.Optional[typing.Union[GraphqlConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        grit: typing.Optional[typing.Union[GritConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        html: typing.Optional[typing.Union[HtmlConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        includes: typing.Optional[typing.Sequence[builtins.str]] = None,
        javascript: typing.Optional[typing.Union[JsConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        json: typing.Optional[typing.Union[JsonConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        linter: typing.Optional[typing.Union[OverrideLinterConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
        plugins: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param assist: (experimental) Specific configuration for the Json language.
        :param css: (experimental) Specific configuration for the CSS language.
        :param files: (experimental) Specific configuration for the filesystem.
        :param formatter: (experimental) Specific configuration for the Json language.
        :param graphql: (experimental) Specific configuration for the Graphql language.
        :param grit: (experimental) Specific configuration for the GritQL language.
        :param html: (experimental) Specific configuration for the GritQL language.
        :param includes: (experimental) A list of glob patterns. Biome will include files/folders that will match these patterns.
        :param javascript: (experimental) Specific configuration for the JavaScript language.
        :param json: (experimental) Specific configuration for the Json language.
        :param linter: (experimental) Specific configuration for the Json language.
        :param plugins: (experimental) Specific configuration for additional plugins.

        :stability: experimental
        :schema: OverridePattern
        '''
        if isinstance(assist, dict):
            assist = OverrideAssistConfiguration(**assist)
        if isinstance(css, dict):
            css = CssConfiguration(**css)
        if isinstance(files, dict):
            files = OverrideFilesConfiguration(**files)
        if isinstance(formatter, dict):
            formatter = OverrideFormatterConfiguration(**formatter)
        if isinstance(graphql, dict):
            graphql = GraphqlConfiguration(**graphql)
        if isinstance(grit, dict):
            grit = GritConfiguration(**grit)
        if isinstance(html, dict):
            html = HtmlConfiguration(**html)
        if isinstance(javascript, dict):
            javascript = JsConfiguration(**javascript)
        if isinstance(json, dict):
            json = JsonConfiguration(**json)
        if isinstance(linter, dict):
            linter = OverrideLinterConfiguration(**linter)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15d4ec259e2481f14109da78900e918d2d10bde9b57b737b5c0ac7d4d415d889)
            check_type(argname="argument assist", value=assist, expected_type=type_hints["assist"])
            check_type(argname="argument css", value=css, expected_type=type_hints["css"])
            check_type(argname="argument files", value=files, expected_type=type_hints["files"])
            check_type(argname="argument formatter", value=formatter, expected_type=type_hints["formatter"])
            check_type(argname="argument graphql", value=graphql, expected_type=type_hints["graphql"])
            check_type(argname="argument grit", value=grit, expected_type=type_hints["grit"])
            check_type(argname="argument html", value=html, expected_type=type_hints["html"])
            check_type(argname="argument includes", value=includes, expected_type=type_hints["includes"])
            check_type(argname="argument javascript", value=javascript, expected_type=type_hints["javascript"])
            check_type(argname="argument json", value=json, expected_type=type_hints["json"])
            check_type(argname="argument linter", value=linter, expected_type=type_hints["linter"])
            check_type(argname="argument plugins", value=plugins, expected_type=type_hints["plugins"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assist is not None:
            self._values["assist"] = assist
        if css is not None:
            self._values["css"] = css
        if files is not None:
            self._values["files"] = files
        if formatter is not None:
            self._values["formatter"] = formatter
        if graphql is not None:
            self._values["graphql"] = graphql
        if grit is not None:
            self._values["grit"] = grit
        if html is not None:
            self._values["html"] = html
        if includes is not None:
            self._values["includes"] = includes
        if javascript is not None:
            self._values["javascript"] = javascript
        if json is not None:
            self._values["json"] = json
        if linter is not None:
            self._values["linter"] = linter
        if plugins is not None:
            self._values["plugins"] = plugins

    @builtins.property
    def assist(self) -> typing.Optional[OverrideAssistConfiguration]:
        '''(experimental) Specific configuration for the Json language.

        :stability: experimental
        :schema: OverridePattern#assist
        '''
        result = self._values.get("assist")
        return typing.cast(typing.Optional[OverrideAssistConfiguration], result)

    @builtins.property
    def css(self) -> typing.Optional[CssConfiguration]:
        '''(experimental) Specific configuration for the CSS language.

        :stability: experimental
        :schema: OverridePattern#css
        '''
        result = self._values.get("css")
        return typing.cast(typing.Optional[CssConfiguration], result)

    @builtins.property
    def files(self) -> typing.Optional[OverrideFilesConfiguration]:
        '''(experimental) Specific configuration for the filesystem.

        :stability: experimental
        :schema: OverridePattern#files
        '''
        result = self._values.get("files")
        return typing.cast(typing.Optional[OverrideFilesConfiguration], result)

    @builtins.property
    def formatter(self) -> typing.Optional[OverrideFormatterConfiguration]:
        '''(experimental) Specific configuration for the Json language.

        :stability: experimental
        :schema: OverridePattern#formatter
        '''
        result = self._values.get("formatter")
        return typing.cast(typing.Optional[OverrideFormatterConfiguration], result)

    @builtins.property
    def graphql(self) -> typing.Optional[GraphqlConfiguration]:
        '''(experimental) Specific configuration for the Graphql language.

        :stability: experimental
        :schema: OverridePattern#graphql
        '''
        result = self._values.get("graphql")
        return typing.cast(typing.Optional[GraphqlConfiguration], result)

    @builtins.property
    def grit(self) -> typing.Optional[GritConfiguration]:
        '''(experimental) Specific configuration for the GritQL language.

        :stability: experimental
        :schema: OverridePattern#grit
        '''
        result = self._values.get("grit")
        return typing.cast(typing.Optional[GritConfiguration], result)

    @builtins.property
    def html(self) -> typing.Optional[HtmlConfiguration]:
        '''(experimental) Specific configuration for the GritQL language.

        :stability: experimental
        :schema: OverridePattern#html
        '''
        result = self._values.get("html")
        return typing.cast(typing.Optional[HtmlConfiguration], result)

    @builtins.property
    def includes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of glob patterns.

        Biome will include files/folders that will match these patterns.

        :stability: experimental
        :schema: OverridePattern#includes
        '''
        result = self._values.get("includes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def javascript(self) -> typing.Optional[JsConfiguration]:
        '''(experimental) Specific configuration for the JavaScript language.

        :stability: experimental
        :schema: OverridePattern#javascript
        '''
        result = self._values.get("javascript")
        return typing.cast(typing.Optional[JsConfiguration], result)

    @builtins.property
    def json(self) -> typing.Optional[JsonConfiguration]:
        '''(experimental) Specific configuration for the Json language.

        :stability: experimental
        :schema: OverridePattern#json
        '''
        result = self._values.get("json")
        return typing.cast(typing.Optional[JsonConfiguration], result)

    @builtins.property
    def linter(self) -> typing.Optional[OverrideLinterConfiguration]:
        '''(experimental) Specific configuration for the Json language.

        :stability: experimental
        :schema: OverridePattern#linter
        '''
        result = self._values.get("linter")
        return typing.cast(typing.Optional[OverrideLinterConfiguration], result)

    @builtins.property
    def plugins(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Specific configuration for additional plugins.

        :stability: experimental
        :schema: OverridePattern#plugins
        '''
        result = self._values.get("plugins")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OverridePattern(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.javascript.biome_config.QuoteProperties")
class QuoteProperties(enum.Enum):
    '''
    :stability: experimental
    :schema: QuoteProperties
    '''

    AS_NEEDED = "AS_NEEDED"
    '''(experimental) asNeeded.

    :stability: experimental
    '''
    PRESERVE = "PRESERVE"
    '''(experimental) preserve.

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.javascript.biome_config.QuoteStyle")
class QuoteStyle(enum.Enum):
    '''
    :stability: experimental
    :schema: QuoteStyle
    '''

    DOUBLE = "DOUBLE"
    '''(experimental) double.

    :stability: experimental
    '''
    SINGLE = "SINGLE"
    '''(experimental) single.

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.javascript.biome_config.RuleDomainValue")
class RuleDomainValue(enum.Enum):
    '''
    :stability: experimental
    :schema: RuleDomainValue
    '''

    ALL = "ALL"
    '''(experimental) all.

    :stability: experimental
    '''
    NONE = "NONE"
    '''(experimental) none.

    :stability: experimental
    '''
    RECOMMENDED = "RECOMMENDED"
    '''(experimental) recommended.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.Rules",
    jsii_struct_bases=[],
    name_mapping={
        "a11_y": "a11Y",
        "complexity": "complexity",
        "correctness": "correctness",
        "nursery": "nursery",
        "performance": "performance",
        "recommended": "recommended",
        "security": "security",
        "style": "style",
        "suspicious": "suspicious",
    },
)
class Rules:
    def __init__(
        self,
        *,
        a11_y: typing.Any = None,
        complexity: typing.Any = None,
        correctness: typing.Any = None,
        nursery: typing.Any = None,
        performance: typing.Any = None,
        recommended: typing.Optional[builtins.bool] = None,
        security: typing.Any = None,
        style: typing.Any = None,
        suspicious: typing.Any = None,
    ) -> None:
        '''
        :param a11_y: 
        :param complexity: 
        :param correctness: 
        :param nursery: 
        :param performance: 
        :param recommended: (experimental) It enables the lint rules recommended by Biome. ``true`` by default.
        :param security: 
        :param style: 
        :param suspicious: 

        :stability: experimental
        :schema: Rules
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d509a5cc6f981426e8c0771a7bcfe4b66092b008a57a49a58a2d172ec95c48bd)
            check_type(argname="argument a11_y", value=a11_y, expected_type=type_hints["a11_y"])
            check_type(argname="argument complexity", value=complexity, expected_type=type_hints["complexity"])
            check_type(argname="argument correctness", value=correctness, expected_type=type_hints["correctness"])
            check_type(argname="argument nursery", value=nursery, expected_type=type_hints["nursery"])
            check_type(argname="argument performance", value=performance, expected_type=type_hints["performance"])
            check_type(argname="argument recommended", value=recommended, expected_type=type_hints["recommended"])
            check_type(argname="argument security", value=security, expected_type=type_hints["security"])
            check_type(argname="argument style", value=style, expected_type=type_hints["style"])
            check_type(argname="argument suspicious", value=suspicious, expected_type=type_hints["suspicious"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if a11_y is not None:
            self._values["a11_y"] = a11_y
        if complexity is not None:
            self._values["complexity"] = complexity
        if correctness is not None:
            self._values["correctness"] = correctness
        if nursery is not None:
            self._values["nursery"] = nursery
        if performance is not None:
            self._values["performance"] = performance
        if recommended is not None:
            self._values["recommended"] = recommended
        if security is not None:
            self._values["security"] = security
        if style is not None:
            self._values["style"] = style
        if suspicious is not None:
            self._values["suspicious"] = suspicious

    @builtins.property
    def a11_y(self) -> typing.Any:
        '''
        :stability: experimental
        :schema: Rules#a11y
        '''
        result = self._values.get("a11_y")
        return typing.cast(typing.Any, result)

    @builtins.property
    def complexity(self) -> typing.Any:
        '''
        :stability: experimental
        :schema: Rules#complexity
        '''
        result = self._values.get("complexity")
        return typing.cast(typing.Any, result)

    @builtins.property
    def correctness(self) -> typing.Any:
        '''
        :stability: experimental
        :schema: Rules#correctness
        '''
        result = self._values.get("correctness")
        return typing.cast(typing.Any, result)

    @builtins.property
    def nursery(self) -> typing.Any:
        '''
        :stability: experimental
        :schema: Rules#nursery
        '''
        result = self._values.get("nursery")
        return typing.cast(typing.Any, result)

    @builtins.property
    def performance(self) -> typing.Any:
        '''
        :stability: experimental
        :schema: Rules#performance
        '''
        result = self._values.get("performance")
        return typing.cast(typing.Any, result)

    @builtins.property
    def recommended(self) -> typing.Optional[builtins.bool]:
        '''(experimental) It enables the lint rules recommended by Biome.

        ``true`` by default.

        :stability: experimental
        :schema: Rules#recommended
        '''
        result = self._values.get("recommended")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def security(self) -> typing.Any:
        '''
        :stability: experimental
        :schema: Rules#security
        '''
        result = self._values.get("security")
        return typing.cast(typing.Any, result)

    @builtins.property
    def style(self) -> typing.Any:
        '''
        :stability: experimental
        :schema: Rules#style
        '''
        result = self._values.get("style")
        return typing.cast(typing.Any, result)

    @builtins.property
    def suspicious(self) -> typing.Any:
        '''
        :stability: experimental
        :schema: Rules#suspicious
        '''
        result = self._values.get("suspicious")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Rules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.javascript.biome_config.SelfCloseVoidElements")
class SelfCloseVoidElements(enum.Enum):
    '''(experimental) Controls whether void-elements should be self closed.

    :stability: experimental
    :schema: SelfCloseVoidElements
    '''

    NEVER = "NEVER"
    '''(experimental) never.

    :stability: experimental
    '''
    ALWAYS = "ALWAYS"
    '''(experimental) always.

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.javascript.biome_config.Semicolons")
class Semicolons(enum.Enum):
    '''
    :stability: experimental
    :schema: Semicolons
    '''

    ALWAYS = "ALWAYS"
    '''(experimental) always.

    :stability: experimental
    '''
    AS_NEEDED = "AS_NEEDED"
    '''(experimental) asNeeded.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.Source",
    jsii_struct_bases=[],
    name_mapping={
        "organize_imports": "organizeImports",
        "recommended": "recommended",
        "use_sorted_attributes": "useSortedAttributes",
        "use_sorted_keys": "useSortedKeys",
        "use_sorted_properties": "useSortedProperties",
    },
)
class Source:
    def __init__(
        self,
        *,
        organize_imports: typing.Any = None,
        recommended: typing.Optional[builtins.bool] = None,
        use_sorted_attributes: typing.Any = None,
        use_sorted_keys: typing.Any = None,
        use_sorted_properties: typing.Any = None,
    ) -> None:
        '''(experimental) A list of rules that belong to this group.

        :param organize_imports: (experimental) Provides a code action to sort the imports and exports in the file using a built-in or custom order.
        :param recommended: (experimental) Enables the recommended rules for this group.
        :param use_sorted_attributes: (experimental) Enforce attribute sorting in JSX elements.
        :param use_sorted_keys: (experimental) Sort the keys of a JSON object in natural order.
        :param use_sorted_properties: (experimental) Enforce ordering of CSS properties and nested rules.

        :stability: experimental
        :schema: Source
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f128bc69ea32431a28e9aae09b49905087cb9f2c49176cf906cbd06f3c7237b7)
            check_type(argname="argument organize_imports", value=organize_imports, expected_type=type_hints["organize_imports"])
            check_type(argname="argument recommended", value=recommended, expected_type=type_hints["recommended"])
            check_type(argname="argument use_sorted_attributes", value=use_sorted_attributes, expected_type=type_hints["use_sorted_attributes"])
            check_type(argname="argument use_sorted_keys", value=use_sorted_keys, expected_type=type_hints["use_sorted_keys"])
            check_type(argname="argument use_sorted_properties", value=use_sorted_properties, expected_type=type_hints["use_sorted_properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if organize_imports is not None:
            self._values["organize_imports"] = organize_imports
        if recommended is not None:
            self._values["recommended"] = recommended
        if use_sorted_attributes is not None:
            self._values["use_sorted_attributes"] = use_sorted_attributes
        if use_sorted_keys is not None:
            self._values["use_sorted_keys"] = use_sorted_keys
        if use_sorted_properties is not None:
            self._values["use_sorted_properties"] = use_sorted_properties

    @builtins.property
    def organize_imports(self) -> typing.Any:
        '''(experimental) Provides a code action to sort the imports and exports in the file using a built-in or custom order.

        :stability: experimental
        :schema: Source#organizeImports
        '''
        result = self._values.get("organize_imports")
        return typing.cast(typing.Any, result)

    @builtins.property
    def recommended(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables the recommended rules for this group.

        :stability: experimental
        :schema: Source#recommended
        '''
        result = self._values.get("recommended")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def use_sorted_attributes(self) -> typing.Any:
        '''(experimental) Enforce attribute sorting in JSX elements.

        :stability: experimental
        :schema: Source#useSortedAttributes
        '''
        result = self._values.get("use_sorted_attributes")
        return typing.cast(typing.Any, result)

    @builtins.property
    def use_sorted_keys(self) -> typing.Any:
        '''(experimental) Sort the keys of a JSON object in natural order.

        :stability: experimental
        :schema: Source#useSortedKeys
        '''
        result = self._values.get("use_sorted_keys")
        return typing.cast(typing.Any, result)

    @builtins.property
    def use_sorted_properties(self) -> typing.Any:
        '''(experimental) Enforce ordering of CSS properties and nested rules.

        :stability: experimental
        :schema: Source#useSortedProperties
        '''
        result = self._values.get("use_sorted_properties")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Source(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.javascript.biome_config.TrailingCommas")
class TrailingCommas(enum.Enum):
    '''(experimental) Print trailing commas wherever possible in multi-line comma-separated syntactic structures.

    :stability: experimental
    :schema: TrailingCommas
    '''

    ALL = "ALL"
    '''(experimental) all.

    :stability: experimental
    '''
    ES5 = "ES5"
    '''(experimental) es5.

    :stability: experimental
    '''
    NONE = "NONE"
    '''(experimental) none.

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.javascript.biome_config.TrailingCommas2")
class TrailingCommas2(enum.Enum):
    '''
    :stability: experimental
    :schema: TrailingCommas2
    '''

    NONE = "NONE"
    '''(experimental) none.

    :stability: experimental
    '''
    ALL = "ALL"
    '''(experimental) all.

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.javascript.biome_config.VcsClientKind")
class VcsClientKind(enum.Enum):
    '''(experimental) Integration with the git client as VCS.

    :stability: experimental
    :schema: VcsClientKind
    '''

    GIT = "GIT"
    '''(experimental) git.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.VcsConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "client_kind": "clientKind",
        "default_branch": "defaultBranch",
        "enabled": "enabled",
        "root": "root",
        "use_ignore_file": "useIgnoreFile",
    },
)
class VcsConfiguration:
    def __init__(
        self,
        *,
        client_kind: typing.Optional[VcsClientKind] = None,
        default_branch: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        root: typing.Optional[builtins.str] = None,
        use_ignore_file: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Set of properties to integrate Biome with a VCS software.

        :param client_kind: (experimental) The kind of client.
        :param default_branch: (experimental) The main branch of the project.
        :param enabled: (experimental) Whether Biome should integrate itself with the VCS client.
        :param root: (experimental) The folder where Biome should check for VCS files. By default, Biome will use the same folder where ``biome.json`` was found. If Biome can't find the configuration, it will attempt to use the current working directory. If no current working directory can't be found, Biome won't use the VCS integration, and a diagnostic will be emitted
        :param use_ignore_file: (experimental) Whether Biome should use the VCS ignore file. When [true], Biome will ignore the files specified in the ignore file.

        :stability: experimental
        :schema: VcsConfiguration
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0ca0d2f64e42e40c29e089e5200324b97670a6ebbf0f39b444b15a42a7150b7)
            check_type(argname="argument client_kind", value=client_kind, expected_type=type_hints["client_kind"])
            check_type(argname="argument default_branch", value=default_branch, expected_type=type_hints["default_branch"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument root", value=root, expected_type=type_hints["root"])
            check_type(argname="argument use_ignore_file", value=use_ignore_file, expected_type=type_hints["use_ignore_file"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if client_kind is not None:
            self._values["client_kind"] = client_kind
        if default_branch is not None:
            self._values["default_branch"] = default_branch
        if enabled is not None:
            self._values["enabled"] = enabled
        if root is not None:
            self._values["root"] = root
        if use_ignore_file is not None:
            self._values["use_ignore_file"] = use_ignore_file

    @builtins.property
    def client_kind(self) -> typing.Optional[VcsClientKind]:
        '''(experimental) The kind of client.

        :stability: experimental
        :schema: VcsConfiguration#clientKind
        '''
        result = self._values.get("client_kind")
        return typing.cast(typing.Optional[VcsClientKind], result)

    @builtins.property
    def default_branch(self) -> typing.Optional[builtins.str]:
        '''(experimental) The main branch of the project.

        :stability: experimental
        :schema: VcsConfiguration#defaultBranch
        '''
        result = self._values.get("default_branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether Biome should integrate itself with the VCS client.

        :stability: experimental
        :schema: VcsConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def root(self) -> typing.Optional[builtins.str]:
        '''(experimental) The folder where Biome should check for VCS files.

        By default, Biome will use the same folder where ``biome.json`` was found.

        If Biome can't find the configuration, it will attempt to use the current working directory. If no current working directory can't be found, Biome won't use the VCS integration, and a diagnostic will be emitted

        :stability: experimental
        :schema: VcsConfiguration#root
        '''
        result = self._values.get("root")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_ignore_file(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether Biome should use the VCS ignore file.

        When [true], Biome will ignore the files specified in the ignore file.

        :stability: experimental
        :schema: VcsConfiguration#useIgnoreFile
        '''
        result = self._values.get("use_ignore_file")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VcsConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.javascript.biome_config.WhitespaceSensitivity")
class WhitespaceSensitivity(enum.Enum):
    '''(experimental) Whitespace sensitivity for HTML formatting.

    The following two cases won't produce the same output:

    |                |      html      |    output    | | -------------- | :------------: | :----------: | | with spaces    | ``1<b> 2 </b>3`` | 1 2 3 | | without spaces |  ``1<b>2</b>3``  |  123  |

    This happens because whitespace is significant in inline elements.

    As a consequence of this, the formatter must format blocks that look like this (assume a small line width, <20): ``html <span>really long content</span> `` as this, where the content hugs the tags: ``html <span >really long content</span > ``

    Note that this is only necessary for inline elements. Block elements do not have this restriction.

    :stability: experimental
    :schema: WhitespaceSensitivity
    '''

    CSS = "CSS"
    '''(experimental) css.

    :stability: experimental
    '''
    STRICT = "STRICT"
    '''(experimental) strict.

    :stability: experimental
    '''
    IGNORE = "IGNORE"
    '''(experimental) ignore.

    :stability: experimental
    '''


__all__ = [
    "Actions",
    "ArrowParentheses",
    "AssistConfiguration",
    "AttributePosition",
    "BiomeConfiguration",
    "CssAssistConfiguration",
    "CssConfiguration",
    "CssFormatterConfiguration",
    "CssLinterConfiguration",
    "CssParserConfiguration",
    "Expand",
    "FilesConfiguration",
    "FormatterConfiguration",
    "GraphqlAssistConfiguration",
    "GraphqlConfiguration",
    "GraphqlFormatterConfiguration",
    "GraphqlLinterConfiguration",
    "GritAssistConfiguration",
    "GritConfiguration",
    "GritFormatterConfiguration",
    "GritLinterConfiguration",
    "HtmlConfiguration",
    "HtmlFormatterConfiguration",
    "HtmlParserConfiguration",
    "IndentStyle",
    "JsAssistConfiguration",
    "JsConfiguration",
    "JsFormatterConfiguration",
    "JsLinterConfiguration",
    "JsParserConfiguration",
    "JsonAssistConfiguration",
    "JsonConfiguration",
    "JsonFormatterConfiguration",
    "JsonLinterConfiguration",
    "JsonParserConfiguration",
    "JsxRuntime",
    "LineEnding",
    "LinterConfiguration",
    "OperatorLinebreak",
    "OverrideAssistConfiguration",
    "OverrideFilesConfiguration",
    "OverrideFormatterConfiguration",
    "OverrideLinterConfiguration",
    "OverridePattern",
    "QuoteProperties",
    "QuoteStyle",
    "RuleDomainValue",
    "Rules",
    "SelfCloseVoidElements",
    "Semicolons",
    "Source",
    "TrailingCommas",
    "TrailingCommas2",
    "VcsClientKind",
    "VcsConfiguration",
    "WhitespaceSensitivity",
]

publication.publish()

def _typecheckingstub__6366c915d5edbe08a6c33dee8fe8422a0286f131b30d1697e72b9e5e37127dcc(
    *,
    recommended: typing.Optional[builtins.bool] = None,
    source: typing.Optional[typing.Union[Source, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__653e8f7779876f355ba04bd69945d4c60ef342663eb94ddff052064ccd3fe707(
    *,
    actions: typing.Optional[typing.Union[Actions, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled: typing.Optional[builtins.bool] = None,
    includes: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d80cddd85ec22ae5e9ee130a7150db72ca1333e6e292553494d0e61d7b92e10(
    *,
    assist: typing.Optional[typing.Union[AssistConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    css: typing.Optional[typing.Union[CssConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    extends: typing.Optional[typing.Sequence[builtins.str]] = None,
    files: typing.Optional[typing.Union[FilesConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    formatter: typing.Optional[typing.Union[FormatterConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    graphql: typing.Optional[typing.Union[GraphqlConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    grit: typing.Optional[typing.Union[GritConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    html: typing.Optional[typing.Union[HtmlConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    javascript: typing.Optional[typing.Union[JsConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    json: typing.Optional[typing.Union[JsonConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    linter: typing.Optional[typing.Union[LinterConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    overrides: typing.Optional[typing.Sequence[typing.Union[OverridePattern, typing.Dict[builtins.str, typing.Any]]]] = None,
    plugins: typing.Optional[typing.Sequence[builtins.str]] = None,
    root: typing.Optional[builtins.bool] = None,
    schema: typing.Optional[builtins.str] = None,
    vcs: typing.Optional[typing.Union[VcsConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d79ee25821f244538ee0bcf57d1ff302007d2643512718410c33310d05b8dc4(
    *,
    enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__546cd91eebef3c3c3a2ec7242b79be8e1e49bbd4e237eea9e2543e548c089bea(
    *,
    assist: typing.Optional[typing.Union[CssAssistConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    formatter: typing.Optional[typing.Union[CssFormatterConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    globals: typing.Optional[typing.Sequence[builtins.str]] = None,
    linter: typing.Optional[typing.Union[CssLinterConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    parser: typing.Optional[typing.Union[CssParserConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1fb0cc7e8e9a8ff6796060277e93271c00edf3f8878cd107fe3a211c7aa58ca(
    *,
    enabled: typing.Optional[builtins.bool] = None,
    indent_style: typing.Optional[IndentStyle] = None,
    indent_width: typing.Optional[jsii.Number] = None,
    line_ending: typing.Optional[LineEnding] = None,
    line_width: typing.Optional[jsii.Number] = None,
    quote_style: typing.Optional[QuoteStyle] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66bcb81b30852efd84c1040b1c15bea9669396c926d4f016dc8c65523fc5d8c0(
    *,
    enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8529582f37794a4d2a6c31671f27c3add8085e862adbf314c4f633b00295f518(
    *,
    allow_wrong_line_comments: typing.Optional[builtins.bool] = None,
    css_modules: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f06e077779a89de8924deeb042aada1ebd486faca5b2fad3aabff17e1eaaa2e4(
    *,
    experimental_scanner_ignores: typing.Optional[typing.Sequence[builtins.str]] = None,
    ignore_unknown: typing.Optional[builtins.bool] = None,
    includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d250053b03cd738e71599a16d0b903766c0befb7557dadc7ffee799234532c78(
    *,
    attribute_position: typing.Optional[AttributePosition] = None,
    bracket_same_line: typing.Optional[builtins.bool] = None,
    bracket_spacing: typing.Optional[builtins.bool] = None,
    enabled: typing.Optional[builtins.bool] = None,
    expand: typing.Optional[Expand] = None,
    format_with_errors: typing.Optional[builtins.bool] = None,
    includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    indent_style: typing.Optional[IndentStyle] = None,
    indent_width: typing.Optional[jsii.Number] = None,
    line_ending: typing.Optional[LineEnding] = None,
    line_width: typing.Optional[jsii.Number] = None,
    use_editorconfig: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0dbfc7c635234e8ca5c531a8c27d60cc9eb836491490660da8418fad825b69a2(
    *,
    enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2155336ae80236225feccaa799a660386650fec7a49468bef45ab34ed6677842(
    *,
    assist: typing.Optional[typing.Union[GraphqlAssistConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    formatter: typing.Optional[typing.Union[GraphqlFormatterConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    linter: typing.Optional[typing.Union[GraphqlLinterConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc9ad6152bf4d6cec4d40f5bfd9a8d0247f6c53cda4876e24cc83741fac1ae9f(
    *,
    bracket_spacing: typing.Optional[builtins.bool] = None,
    enabled: typing.Optional[builtins.bool] = None,
    indent_style: typing.Optional[IndentStyle] = None,
    indent_width: typing.Optional[jsii.Number] = None,
    line_ending: typing.Optional[LineEnding] = None,
    line_width: typing.Optional[jsii.Number] = None,
    quote_style: typing.Optional[QuoteStyle] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d2f81257796562c5e318e2c7b1278da3b88a7b868379f34ecb8d427734ba141(
    *,
    enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59f4559ad93f10b7671f2d81b54798d511d54078f14b37594d40617170bd4645(
    *,
    enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6767810d80e7477e7c2f6a26f7c7f238a608f28412191ad4e6ab8504edd02a88(
    *,
    assist: typing.Optional[typing.Union[GritAssistConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    formatter: typing.Optional[typing.Union[GritFormatterConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    linter: typing.Optional[typing.Union[GritLinterConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7eb20c598594405c2626c0973407324d66863625354188a196be6d25686d44e8(
    *,
    enabled: typing.Optional[builtins.bool] = None,
    indent_style: typing.Optional[IndentStyle] = None,
    indent_width: typing.Optional[jsii.Number] = None,
    line_ending: typing.Optional[LineEnding] = None,
    line_width: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f328d623f0baa93f52695005ba45f28881c95ae610fde354116a44bc8b01c30(
    *,
    enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__048266f3b4e4769e6485570d4954197f51204fc6e607e2ffe5267f80089b5ded(
    *,
    formatter: typing.Optional[typing.Union[HtmlFormatterConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    parser: typing.Optional[typing.Union[HtmlParserConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcbf243ebdc0f288a10a4e6b68dc5a1ff88f4d8abe5566f57f212bf101440a69(
    *,
    attribute_position: typing.Optional[AttributePosition] = None,
    bracket_same_line: typing.Optional[builtins.bool] = None,
    enabled: typing.Optional[builtins.bool] = None,
    indent_script_and_style: typing.Optional[builtins.bool] = None,
    indent_style: typing.Optional[IndentStyle] = None,
    indent_width: typing.Optional[jsii.Number] = None,
    line_ending: typing.Optional[LineEnding] = None,
    line_width: typing.Optional[jsii.Number] = None,
    self_close_void_elements: typing.Optional[SelfCloseVoidElements] = None,
    whitespace_sensitivity: typing.Optional[WhitespaceSensitivity] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b3cfca5c3ad8f608b86ade05d476530f16da0ba23410a7613236950da38ff37(
    *,
    interpolation: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a425594ed8c46868c14fe924e8346d0d10c110ecabdc7f0d160d30bb06cf91ea(
    *,
    enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57972f7094bf127a9fb1918efc38b7f9fd8b7e2a28387b1d59645ced7024c16b(
    *,
    assist: typing.Optional[typing.Union[JsAssistConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    formatter: typing.Optional[typing.Union[JsFormatterConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    globals: typing.Optional[typing.Sequence[builtins.str]] = None,
    jsx_runtime: typing.Optional[JsxRuntime] = None,
    linter: typing.Optional[typing.Union[JsLinterConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    parser: typing.Optional[typing.Union[JsParserConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83d4960ad9dc84017b237fabc105d7837e8a3ec56d19b1de7e01183651d05de1(
    *,
    arrow_parentheses: typing.Optional[ArrowParentheses] = None,
    attribute_position: typing.Optional[AttributePosition] = None,
    bracket_same_line: typing.Optional[builtins.bool] = None,
    bracket_spacing: typing.Optional[builtins.bool] = None,
    enabled: typing.Optional[builtins.bool] = None,
    expand: typing.Optional[Expand] = None,
    indent_style: typing.Optional[IndentStyle] = None,
    indent_width: typing.Optional[jsii.Number] = None,
    jsx_quote_style: typing.Optional[QuoteStyle] = None,
    line_ending: typing.Optional[LineEnding] = None,
    line_width: typing.Optional[jsii.Number] = None,
    operator_linebreak: typing.Optional[OperatorLinebreak] = None,
    quote_properties: typing.Optional[QuoteProperties] = None,
    quote_style: typing.Optional[QuoteStyle] = None,
    semicolons: typing.Optional[Semicolons] = None,
    trailing_commas: typing.Optional[TrailingCommas] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f73a12c3631a151ee57c8ecf68020468207f1fa3a6b5c91890a93814a4119533(
    *,
    enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c08c2e4162829556526f51e35e2cd7194c2c8bab38e0d01775d808ad7d573450(
    *,
    grit_metavariables: typing.Optional[builtins.bool] = None,
    jsx_everywhere: typing.Optional[builtins.bool] = None,
    unsafe_parameter_decorators_enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1fb6aa8858788da93c40533dca490e5cba8b040cbde40fcc78bbd02d8efd181(
    *,
    enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67ca83a8b26135c2a9bc9fcca08d39f860187439c18546ca3bb66035d3ec1146(
    *,
    assist: typing.Optional[typing.Union[JsonAssistConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    formatter: typing.Optional[typing.Union[JsonFormatterConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    linter: typing.Optional[typing.Union[JsonLinterConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    parser: typing.Optional[typing.Union[JsonParserConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a0473ff26e9f0e1a38d7055c4e466dc2b2b92f24abfce11672601c5a1f6f4a2(
    *,
    bracket_spacing: typing.Optional[builtins.bool] = None,
    enabled: typing.Optional[builtins.bool] = None,
    expand: typing.Optional[Expand] = None,
    indent_style: typing.Optional[IndentStyle] = None,
    indent_width: typing.Optional[jsii.Number] = None,
    line_ending: typing.Optional[LineEnding] = None,
    line_width: typing.Optional[jsii.Number] = None,
    trailing_commas: typing.Optional[TrailingCommas2] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__850ce6cbde62685594cc979eca53b2938f923a2a6a9d3168729c891046c7be59(
    *,
    enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ced0fa0672bed168a8348653ba985dd1a20d26c25f814d1492bdc2bb5b05233(
    *,
    allow_comments: typing.Optional[builtins.bool] = None,
    allow_trailing_commas: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65dab822a12255f6f845b9299f073f8d1333a90456c41e244f29210e8ad1de68(
    *,
    domains: typing.Optional[typing.Mapping[builtins.str, RuleDomainValue]] = None,
    enabled: typing.Optional[builtins.bool] = None,
    includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    rules: typing.Optional[typing.Union[Rules, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56dc91405fb970d58320a5a0025d8bde646c1421e2210fdd1d1f303623e06ef1(
    *,
    actions: typing.Optional[typing.Union[Actions, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26fa6398c015df15db0e8378e7692ad89fd6e1addf1ee19d970d8cd2eb5e64f3(
    *,
    max_size: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3602eb22e2d33d64a65f4ebb15f534391f93d1e72546965c7be88c0c1e391655(
    *,
    attribute_position: typing.Optional[AttributePosition] = None,
    bracket_same_line: typing.Optional[builtins.bool] = None,
    bracket_spacing: typing.Optional[builtins.bool] = None,
    enabled: typing.Optional[builtins.bool] = None,
    expand: typing.Optional[Expand] = None,
    format_with_errors: typing.Optional[builtins.bool] = None,
    indent_size: typing.Optional[jsii.Number] = None,
    indent_style: typing.Optional[IndentStyle] = None,
    indent_width: typing.Optional[jsii.Number] = None,
    line_ending: typing.Optional[LineEnding] = None,
    line_width: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b923acd3721838353ddf97d9a992327d3607a622afc36e911bc3eb842adb709(
    *,
    domains: typing.Optional[typing.Mapping[builtins.str, RuleDomainValue]] = None,
    enabled: typing.Optional[builtins.bool] = None,
    rules: typing.Optional[typing.Union[Rules, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15d4ec259e2481f14109da78900e918d2d10bde9b57b737b5c0ac7d4d415d889(
    *,
    assist: typing.Optional[typing.Union[OverrideAssistConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    css: typing.Optional[typing.Union[CssConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    files: typing.Optional[typing.Union[OverrideFilesConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    formatter: typing.Optional[typing.Union[OverrideFormatterConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    graphql: typing.Optional[typing.Union[GraphqlConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    grit: typing.Optional[typing.Union[GritConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    html: typing.Optional[typing.Union[HtmlConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    javascript: typing.Optional[typing.Union[JsConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    json: typing.Optional[typing.Union[JsonConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    linter: typing.Optional[typing.Union[OverrideLinterConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    plugins: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d509a5cc6f981426e8c0771a7bcfe4b66092b008a57a49a58a2d172ec95c48bd(
    *,
    a11_y: typing.Any = None,
    complexity: typing.Any = None,
    correctness: typing.Any = None,
    nursery: typing.Any = None,
    performance: typing.Any = None,
    recommended: typing.Optional[builtins.bool] = None,
    security: typing.Any = None,
    style: typing.Any = None,
    suspicious: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f128bc69ea32431a28e9aae09b49905087cb9f2c49176cf906cbd06f3c7237b7(
    *,
    organize_imports: typing.Any = None,
    recommended: typing.Optional[builtins.bool] = None,
    use_sorted_attributes: typing.Any = None,
    use_sorted_keys: typing.Any = None,
    use_sorted_properties: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ca0d2f64e42e40c29e089e5200324b97670a6ebbf0f39b444b15a42a7150b7(
    *,
    client_kind: typing.Optional[VcsClientKind] = None,
    default_branch: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    root: typing.Optional[builtins.str] = None,
    use_ignore_file: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass
