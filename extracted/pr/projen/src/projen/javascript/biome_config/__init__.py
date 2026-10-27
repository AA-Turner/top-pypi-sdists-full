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

from jsii._type_checking import cached_type_hints, check_type


from ..._jsii import *


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.Actions",
    jsii_struct_bases=[],
    name_mapping={
        "preset": "preset",
        "recommended": "recommended",
        "source": "source",
    },
)
class Actions:
    def __init__(
        self,
        *,
        preset: typing.Optional["PresetConfig"] = None,
        recommended: typing.Optional[builtins.bool] = None,
        source: typing.Optional[typing.Union["Source", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param preset: (experimental) Selects the baseline set of assist actions. ``recommended`` enables Biome's recommended actions, ``all`` enables all actions, and ``none`` starts with no actions enabled. Group presets and explicit action settings override this preset. Defaults to ``recommended``. Default: recommended`.
        :param recommended: (experimental) Enables or disables Biome's recommended assist actions across all action groups. Defaults to ``true``. Default: true`.
        :param source: (experimental) Configures source-level actions such as organizing imports and sorting declarations. These actions are exposed through editor source actions and through CLI checking and application.

        :stability: experimental
        :schema: Actions
        '''
        if isinstance(source, dict):
            source = Source(**source)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__6366c915d5edbe08a6c33dee8fe8422a0286f131b30d1697e72b9e5e37127dcc)
            check_type(argname="argument preset", value=preset, expected_type=type_hints["preset"])
            check_type(argname="argument recommended", value=recommended, expected_type=type_hints["recommended"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if preset is not None:
            self._values["preset"] = preset
        if recommended is not None:
            self._values["recommended"] = recommended
        if source is not None:
            self._values["source"] = source

    @builtins.property
    def preset(self) -> typing.Optional["PresetConfig"]:
        '''(experimental) Selects the baseline set of assist actions.

        ``recommended`` enables Biome's
        recommended actions, ``all`` enables all actions, and ``none`` starts with no actions
        enabled. Group presets and explicit action settings override this preset.
        Defaults to ``recommended``.

        :default: recommended`.

        :stability: experimental
        :schema: Actions#preset
        '''
        result = self._values.get("preset")
        return typing.cast(typing.Optional["PresetConfig"], result)

    @builtins.property
    def recommended(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables Biome's recommended assist actions across all action groups.

        Defaults to ``true``.

        :default: true`.

        :stability: experimental
        :schema: Actions#recommended
        '''
        result = self._values.get("recommended")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def source(self) -> typing.Optional["Source"]:
        '''(experimental) Configures source-level actions such as organizing imports and sorting declarations.

        These actions are exposed through editor source actions and through CLI checking and application.

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
    '''(experimental) Always prints parentheses around arrow-function parameters.

    (always)

    :stability: experimental
    '''
    AS_NEEDED = "AS_NEEDED"
    '''(experimental) Omits parentheses when an arrow function has one parameter and the syntax permits it.

    (asNeeded)

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
        actions: typing.Optional[typing.Union["Actions", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[builtins.bool] = None,
        includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param actions: (experimental) The assist-action configuration.
        :param enabled: (experimental) Enables configured assist actions in the CLI and editor integrations. Defaults to ``true``. Default: true`.
        :param includes: (experimental) A list of glob patterns selecting files on which assist actions can run. If omitted, all files selected by ``files.includes`` remain eligible for assist actions. An empty list selects no files. This option can only narrow the files selected by ``files.includes``.

        :stability: experimental
        :schema: AssistConfiguration
        '''
        if isinstance(actions, dict):
            actions = Actions(**actions)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__653e8f7779876f355ba04bd69945d4c60ef342663eb94ddff052064ccd3fe707)
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
    def actions(self) -> typing.Optional["Actions"]:
        '''(experimental) The assist-action configuration.

        :stability: experimental
        :schema: AssistConfiguration#actions
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional["Actions"], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables configured assist actions in the CLI and editor integrations.

        Defaults to ``true``.

        :default: true`.

        :stability: experimental
        :schema: AssistConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def includes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of glob patterns selecting files on which assist actions can run.

        If omitted, all files
        selected by ``files.includes`` remain eligible for assist actions. An empty list selects no
        files. This option can only narrow the files selected by ``files.includes``.

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
    '''(experimental) Controls attribute placement in HTML-like languages.

    :stability: experimental
    :schema: AttributePosition
    '''

    AUTO = "AUTO"
    '''(experimental) Places attributes automatically and wraps them when needed.

    (auto)

    :stability: experimental
    '''
    MULTILINE = "MULTILINE"
    '''(experimental) Places each attribute on its own line when an element has multiple attributes.

    (multiline)

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
        "markdown": "markdown",
        "overrides": "overrides",
        "plugins": "plugins",
        "root": "root",
        "schema": "schema",
        "tailwind": "tailwind",
        "vcs": "vcs",
        "yaml": "yaml",
    },
)
class BiomeConfiguration:
    def __init__(
        self,
        *,
        assist: typing.Optional[typing.Union["AssistConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        css: typing.Optional[typing.Union["CssConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        extends: typing.Any = None,
        files: typing.Optional[typing.Union["FilesConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        formatter: typing.Optional[typing.Union["FormatterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        graphql: typing.Optional[typing.Union["GraphqlConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        grit: typing.Optional[typing.Union["GritConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        html: typing.Optional[typing.Union["HtmlConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        javascript: typing.Optional[typing.Union["JsConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        json: typing.Optional[typing.Union["JsonConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        linter: typing.Optional[typing.Union["LinterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        markdown: typing.Optional[typing.Union["MarkdownConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        overrides: typing.Optional[typing.Sequence[typing.Union["OverridePattern", typing.Dict[builtins.str, typing.Any]]]] = None,
        plugins: typing.Optional[typing.Sequence[typing.Any]] = None,
        root: typing.Optional[builtins.bool] = None,
        schema: typing.Optional[builtins.str] = None,
        tailwind: typing.Optional[typing.Union["TailwindConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        vcs: typing.Optional[typing.Union["VcsConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        yaml: typing.Optional[typing.Union["YamlConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) The configuration contained in ``biome.json`` or ``biome.jsonc``.

        :param assist: (experimental) The assist configuration.
        :param css: (experimental) Configuration specific to CSS.
        :param extends: (experimental) Extends the current configuration with settings from one or more other Biome configurations. Use ``"//"`` in a nested configuration to extend the root configuration at any nesting depth. Use an array to extend configurations by relative path or installed package specifier. Biome merges configurations from left to right. Later configurations take precedence for single-value options, list entries are combined, and the current file is applied last.
        :param files: (experimental) Configures which files Biome can discover and process.
        :param formatter: (experimental) Configures formatting for selected files.
        :param graphql: (experimental) Configuration specific to GraphQL.
        :param grit: (experimental) Configuration specific to GritQL.
        :param html: (experimental) Configuration specific to HTML.
        :param javascript: (experimental) Configuration specific to JavaScript.
        :param json: (experimental) Configuration specific to JSON.
        :param linter: (experimental) The linter configuration.
        :param markdown: (experimental) Configuration specific to Markdown.
        :param overrides: (experimental) Configures settings for files selected by each override. When multiple overrides configure the same single-value setting, the last matching override takes precedence.
        :param plugins: (experimental) A list of GritQL plugins to load.
        :param root: (experimental) Marks whether this file is the root configuration for a Biome project. The root configuration establishes the project's base settings, while ``false`` marks a configuration found inside the project as nested rather than a second project root. Defaults to ``true``. Biome implicitly treats ``root`` as ``false`` when a nested configuration uses ``"extends": "//"``. All other nested configurations must explicitly set ``root`` to ``false``. Default: true``. Biome implicitly treats ``root``as``false` when a nested configuration uses
        :param schema: (experimental) The JSON Schema used to validate the configuration and provide editor completion. Biome emits a diagnostic when a ``biomejs.dev`` schema URL specifies a version that differs from the running CLI version.
        :param tailwind: (experimental) Configures how Biome recognizes Tailwind class strings.
        :param vcs: (experimental) The version control integration configuration.
        :param yaml: (experimental) Configuration specific to YAML.

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
        if isinstance(markdown, dict):
            markdown = MarkdownConfiguration(**markdown)
        if isinstance(tailwind, dict):
            tailwind = TailwindConfiguration(**tailwind)
        if isinstance(vcs, dict):
            vcs = VcsConfiguration(**vcs)
        if isinstance(yaml, dict):
            yaml = YamlConfiguration(**yaml)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__5d80cddd85ec22ae5e9ee130a7150db72ca1333e6e292553494d0e61d7b92e10)
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
            check_type(argname="argument markdown", value=markdown, expected_type=type_hints["markdown"])
            check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
            check_type(argname="argument plugins", value=plugins, expected_type=type_hints["plugins"])
            check_type(argname="argument root", value=root, expected_type=type_hints["root"])
            check_type(argname="argument schema", value=schema, expected_type=type_hints["schema"])
            check_type(argname="argument tailwind", value=tailwind, expected_type=type_hints["tailwind"])
            check_type(argname="argument vcs", value=vcs, expected_type=type_hints["vcs"])
            check_type(argname="argument yaml", value=yaml, expected_type=type_hints["yaml"])
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
        if markdown is not None:
            self._values["markdown"] = markdown
        if overrides is not None:
            self._values["overrides"] = overrides
        if plugins is not None:
            self._values["plugins"] = plugins
        if root is not None:
            self._values["root"] = root
        if schema is not None:
            self._values["schema"] = schema
        if tailwind is not None:
            self._values["tailwind"] = tailwind
        if vcs is not None:
            self._values["vcs"] = vcs
        if yaml is not None:
            self._values["yaml"] = yaml

    @builtins.property
    def assist(self) -> typing.Optional["AssistConfiguration"]:
        '''(experimental) The assist configuration.

        :stability: experimental
        :schema: BiomeConfiguration#assist
        '''
        result = self._values.get("assist")
        return typing.cast(typing.Optional["AssistConfiguration"], result)

    @builtins.property
    def css(self) -> typing.Optional["CssConfiguration"]:
        '''(experimental) Configuration specific to CSS.

        :stability: experimental
        :schema: BiomeConfiguration#css
        '''
        result = self._values.get("css")
        return typing.cast(typing.Optional["CssConfiguration"], result)

    @builtins.property
    def extends(self) -> typing.Any:
        '''(experimental) Extends the current configuration with settings from one or more other Biome configurations.

        Use ``"//"`` in a nested configuration to extend the root configuration at any nesting depth.
        Use an array to extend configurations by relative path or installed package specifier.

        Biome merges configurations from left to right. Later configurations take precedence for
        single-value options, list entries are combined, and the current file is applied last.

        :stability: experimental
        :schema: BiomeConfiguration#extends
        '''
        result = self._values.get("extends")
        return typing.cast(typing.Any, result)

    @builtins.property
    def files(self) -> typing.Optional["FilesConfiguration"]:
        '''(experimental) Configures which files Biome can discover and process.

        :stability: experimental
        :schema: BiomeConfiguration#files
        '''
        result = self._values.get("files")
        return typing.cast(typing.Optional["FilesConfiguration"], result)

    @builtins.property
    def formatter(self) -> typing.Optional["FormatterConfiguration"]:
        '''(experimental) Configures formatting for selected files.

        :stability: experimental
        :schema: BiomeConfiguration#formatter
        '''
        result = self._values.get("formatter")
        return typing.cast(typing.Optional["FormatterConfiguration"], result)

    @builtins.property
    def graphql(self) -> typing.Optional["GraphqlConfiguration"]:
        '''(experimental) Configuration specific to GraphQL.

        :stability: experimental
        :schema: BiomeConfiguration#graphql
        '''
        result = self._values.get("graphql")
        return typing.cast(typing.Optional["GraphqlConfiguration"], result)

    @builtins.property
    def grit(self) -> typing.Optional["GritConfiguration"]:
        '''(experimental) Configuration specific to GritQL.

        :stability: experimental
        :schema: BiomeConfiguration#grit
        '''
        result = self._values.get("grit")
        return typing.cast(typing.Optional["GritConfiguration"], result)

    @builtins.property
    def html(self) -> typing.Optional["HtmlConfiguration"]:
        '''(experimental) Configuration specific to HTML.

        :stability: experimental
        :schema: BiomeConfiguration#html
        '''
        result = self._values.get("html")
        return typing.cast(typing.Optional["HtmlConfiguration"], result)

    @builtins.property
    def javascript(self) -> typing.Optional["JsConfiguration"]:
        '''(experimental) Configuration specific to JavaScript.

        :stability: experimental
        :schema: BiomeConfiguration#javascript
        '''
        result = self._values.get("javascript")
        return typing.cast(typing.Optional["JsConfiguration"], result)

    @builtins.property
    def json(self) -> typing.Optional["JsonConfiguration"]:
        '''(experimental) Configuration specific to JSON.

        :stability: experimental
        :schema: BiomeConfiguration#json
        '''
        result = self._values.get("json")
        return typing.cast(typing.Optional["JsonConfiguration"], result)

    @builtins.property
    def linter(self) -> typing.Optional["LinterConfiguration"]:
        '''(experimental) The linter configuration.

        :stability: experimental
        :schema: BiomeConfiguration#linter
        '''
        result = self._values.get("linter")
        return typing.cast(typing.Optional["LinterConfiguration"], result)

    @builtins.property
    def markdown(self) -> typing.Optional["MarkdownConfiguration"]:
        '''(experimental) Configuration specific to Markdown.

        :stability: experimental
        :schema: BiomeConfiguration#markdown
        '''
        result = self._values.get("markdown")
        return typing.cast(typing.Optional["MarkdownConfiguration"], result)

    @builtins.property
    def overrides(self) -> typing.Optional[typing.List["OverridePattern"]]:
        '''(experimental) Configures settings for files selected by each override.

        When multiple overrides configure
        the same single-value setting, the last matching override takes precedence.

        :stability: experimental
        :schema: BiomeConfiguration#overrides
        '''
        result = self._values.get("overrides")
        return typing.cast(typing.Optional[typing.List["OverridePattern"]], result)

    @builtins.property
    def plugins(self) -> typing.Optional[typing.List[typing.Any]]:
        '''(experimental) A list of GritQL plugins to load.

        :stability: experimental
        :schema: BiomeConfiguration#plugins
        '''
        result = self._values.get("plugins")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    @builtins.property
    def root(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Marks whether this file is the root configuration for a Biome project.

        The root configuration
        establishes the project's base settings, while ``false`` marks a configuration found inside the
        project as nested rather than a second project root.

        Defaults to ``true``. Biome implicitly treats ``root`` as ``false`` when a nested configuration uses
        ``"extends": "//"``. All other nested configurations must explicitly set ``root`` to ``false``.

        :default: true``. Biome implicitly treats ``root``as``false` when a nested configuration uses

        :stability: experimental
        :schema: BiomeConfiguration#root
        '''
        result = self._values.get("root")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def schema(self) -> typing.Optional[builtins.str]:
        '''(experimental) The JSON Schema used to validate the configuration and provide editor completion.

        Biome
        emits a diagnostic when a ``biomejs.dev`` schema URL specifies a version that differs from the
        running CLI version.

        :stability: experimental
        :schema: BiomeConfiguration#$schema
        '''
        result = self._values.get("schema")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tailwind(self) -> typing.Optional["TailwindConfiguration"]:
        '''(experimental) Configures how Biome recognizes Tailwind class strings.

        :stability: experimental
        :schema: BiomeConfiguration#tailwind
        '''
        result = self._values.get("tailwind")
        return typing.cast(typing.Optional["TailwindConfiguration"], result)

    @builtins.property
    def vcs(self) -> typing.Optional["VcsConfiguration"]:
        '''(experimental) The version control integration configuration.

        :stability: experimental
        :schema: BiomeConfiguration#vcs
        '''
        result = self._values.get("vcs")
        return typing.cast(typing.Optional["VcsConfiguration"], result)

    @builtins.property
    def yaml(self) -> typing.Optional["YamlConfiguration"]:
        '''(experimental) Configuration specific to YAML.

        :stability: experimental
        :schema: BiomeConfiguration#yaml
        '''
        result = self._values.get("yaml")
        return typing.cast(typing.Optional["YamlConfiguration"], result)

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
        '''(experimental) Options that change how CSS assist behaves.

        :param enabled: (experimental) Enables or disables assist actions for CSS.

        :stability: experimental
        :schema: CssAssistConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__2d79ee25821f244538ee0bcf57d1ff302007d2643512718410c33310d05b8dc4)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables assist actions for CSS.

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
        assist: typing.Optional[typing.Union["CssAssistConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        formatter: typing.Optional[typing.Union["CssFormatterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        globals: typing.Optional[typing.Sequence[builtins.str]] = None,
        linter: typing.Optional[typing.Union["CssLinterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        parser: typing.Optional[typing.Union["CssParserConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options applied to CSS and languages that extend it.

        Language-specific settings take precedence over corresponding global settings. Global settings
        apply when their language-specific counterparts are omitted, unless stated otherwise.

        :param assist: (experimental) CSS assist options.
        :param formatter: (experimental) CSS formatter options.
        :param globals: (experimental) Reserved for future CSS analyzer support. This option currently has no effect.
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
            type_hints = cached_type_hints(_typecheckingstub__546cd91eebef3c3c3a2ec7242b79be8e1e49bbd4e237eea9e2543e548c089bea)
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
    def assist(self) -> typing.Optional["CssAssistConfiguration"]:
        '''(experimental) CSS assist options.

        :stability: experimental
        :schema: CssConfiguration#assist
        '''
        result = self._values.get("assist")
        return typing.cast(typing.Optional["CssAssistConfiguration"], result)

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
        '''(experimental) Reserved for future CSS analyzer support.

        This option currently has no effect.

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
        "delimiter_spacing": "delimiterSpacing",
        "enabled": "enabled",
        "indent_style": "indentStyle",
        "indent_width": "indentWidth",
        "line_ending": "lineEnding",
        "line_width": "lineWidth",
        "quote_style": "quoteStyle",
        "trailing_newline": "trailingNewline",
    },
)
class CssFormatterConfiguration:
    def __init__(
        self,
        *,
        delimiter_spacing: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        indent_style: typing.Optional["IndentStyle"] = None,
        indent_width: typing.Optional[jsii.Number] = None,
        line_ending: typing.Optional["LineEnding"] = None,
        line_width: typing.Optional[jsii.Number] = None,
        quote_style: typing.Optional["QuoteStyle"] = None,
        trailing_newline: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options that change how the CSS formatter behaves.

        :param delimiter_spacing: (experimental) Controls spaces inside CSS parentheses and square brackets when their content fits on one line. When enabled, ``rgb(0, 0, 0)`` becomes ``rgb( 0, 0, 0 )`` and ``[data-attr]`` becomes ``[ data-attr ]``. Empty delimiters are unchanged. If unset, inherits the global delimiter spacing setting.
        :param enabled: (experimental) Enables or disables the formatter for CSS and languages that extend it.
        :param indent_style: (experimental) The indent style applied to CSS and languages that extend it. If unset, inherits the global indentation style.
        :param indent_width: (experimental) The indentation width applied to CSS and languages that extend it. If unset, inherits the global indentation width.
        :param line_ending: (experimental) The line ending applied to CSS and languages that extend it. If unset, inherits the global line ending.
        :param line_width: (experimental) The preferred maximum line width for CSS and languages that extend it. If unset, inherits the global line width.
        :param quote_style: (experimental) Selects the preferred quote style for CSS strings. Biome may use the alternate quote when that avoids additional escaping. Quotes in ``@charset`` rules are currently preserved. Defaults to ``double``. Default: double`.
        :param trailing_newline: (experimental) Whether to add a trailing newline at the end of the file. If unset, inherits the global trailing newline setting.

        :stability: experimental
        :schema: CssFormatterConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e1fb0cc7e8e9a8ff6796060277e93271c00edf3f8878cd107fe3a211c7aa58ca)
            check_type(argname="argument delimiter_spacing", value=delimiter_spacing, expected_type=type_hints["delimiter_spacing"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument indent_style", value=indent_style, expected_type=type_hints["indent_style"])
            check_type(argname="argument indent_width", value=indent_width, expected_type=type_hints["indent_width"])
            check_type(argname="argument line_ending", value=line_ending, expected_type=type_hints["line_ending"])
            check_type(argname="argument line_width", value=line_width, expected_type=type_hints["line_width"])
            check_type(argname="argument quote_style", value=quote_style, expected_type=type_hints["quote_style"])
            check_type(argname="argument trailing_newline", value=trailing_newline, expected_type=type_hints["trailing_newline"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delimiter_spacing is not None:
            self._values["delimiter_spacing"] = delimiter_spacing
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
        if trailing_newline is not None:
            self._values["trailing_newline"] = trailing_newline

    @builtins.property
    def delimiter_spacing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Controls spaces inside CSS parentheses and square brackets when their content fits on one line.

        When enabled, ``rgb(0, 0, 0)`` becomes ``rgb( 0, 0, 0 )`` and ``[data-attr]`` becomes
        ``[ data-attr ]``. Empty delimiters are unchanged.

        If unset, inherits the global delimiter spacing setting.

        :stability: experimental
        :schema: CssFormatterConfiguration#delimiterSpacing
        '''
        result = self._values.get("delimiter_spacing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables the formatter for CSS and languages that extend it.

        :stability: experimental
        :schema: CssFormatterConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def indent_style(self) -> typing.Optional["IndentStyle"]:
        '''(experimental) The indent style applied to CSS and languages that extend it.

        If unset, inherits the global
        indentation style.

        :stability: experimental
        :schema: CssFormatterConfiguration#indentStyle
        '''
        result = self._values.get("indent_style")
        return typing.cast(typing.Optional["IndentStyle"], result)

    @builtins.property
    def indent_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The indentation width applied to CSS and languages that extend it.

        If unset, inherits the
        global indentation width.

        :stability: experimental
        :schema: CssFormatterConfiguration#indentWidth
        '''
        result = self._values.get("indent_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def line_ending(self) -> typing.Optional["LineEnding"]:
        '''(experimental) The line ending applied to CSS and languages that extend it.

        If unset, inherits the global
        line ending.

        :stability: experimental
        :schema: CssFormatterConfiguration#lineEnding
        '''
        result = self._values.get("line_ending")
        return typing.cast(typing.Optional["LineEnding"], result)

    @builtins.property
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The preferred maximum line width for CSS and languages that extend it.

        If unset, inherits
        the global line width.

        :stability: experimental
        :schema: CssFormatterConfiguration#lineWidth
        '''
        result = self._values.get("line_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def quote_style(self) -> typing.Optional["QuoteStyle"]:
        '''(experimental) Selects the preferred quote style for CSS strings.

        Biome may use the alternate quote when
        that avoids additional escaping. Quotes in ``@charset`` rules are currently preserved.
        Defaults to ``double``.

        :default: double`.

        :stability: experimental
        :schema: CssFormatterConfiguration#quoteStyle
        '''
        result = self._values.get("quote_style")
        return typing.cast(typing.Optional["QuoteStyle"], result)

    @builtins.property
    def trailing_newline(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to add a trailing newline at the end of the file.

        If unset, inherits the global
        trailing newline setting.

        :stability: experimental
        :schema: CssFormatterConfiguration#trailingNewline
        '''
        result = self._values.get("trailing_newline")
        return typing.cast(typing.Optional[builtins.bool], result)

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
        '''(experimental) Options that change how the CSS linter behaves.

        :param enabled: (experimental) Enables or disables the linter for CSS.

        :stability: experimental
        :schema: CssLinterConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__66bcb81b30852efd84c1040b1c15bea9669396c926d4f016dc8c65523fc5d8c0)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables the linter for CSS.

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
        "tailwind_directives": "tailwindDirectives",
    },
)
class CssParserConfiguration:
    def __init__(
        self,
        *,
        allow_wrong_line_comments: typing.Optional[builtins.bool] = None,
        css_modules: typing.Optional[builtins.bool] = None,
        tailwind_directives: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options that change how the CSS parser behaves.

        :param allow_wrong_line_comments: (experimental) Enables ``//`` line comments in plain CSS. Standard CSS treats ``//`` as delimiter characters rather than as a comment, and SCSS accepts ``//`` comments independently of this option. Defaults to ``false``. Default: false`.
        :param css_modules: (experimental) Enables CSS Modules-specific syntax such as ``:local``, ``:global``, ``composes``, and ``@value``. When unset, Biome enables this syntax automatically for files whose names end in ``.module.css`` or ``.module.scss; otherwise, it defaults to ``false`. Enable it explicitly when CSS Module files use another naming convention.
        :param tailwind_directives: (experimental) Enables parsing Tailwind CSS 4.0 directives and functions, including ``@theme``, ``@utility``, ``@variant``, ``@source``, and ``@apply``. Defaults to ``false``. Default: false`.

        :stability: experimental
        :schema: CssParserConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__8529582f37794a4d2a6c31671f27c3add8085e862adbf314c4f633b00295f518)
            check_type(argname="argument allow_wrong_line_comments", value=allow_wrong_line_comments, expected_type=type_hints["allow_wrong_line_comments"])
            check_type(argname="argument css_modules", value=css_modules, expected_type=type_hints["css_modules"])
            check_type(argname="argument tailwind_directives", value=tailwind_directives, expected_type=type_hints["tailwind_directives"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_wrong_line_comments is not None:
            self._values["allow_wrong_line_comments"] = allow_wrong_line_comments
        if css_modules is not None:
            self._values["css_modules"] = css_modules
        if tailwind_directives is not None:
            self._values["tailwind_directives"] = tailwind_directives

    @builtins.property
    def allow_wrong_line_comments(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables ``//`` line comments in plain CSS.

        Standard CSS treats ``//`` as delimiter characters
        rather than as a comment, and SCSS accepts ``//`` comments independently of this option.
        Defaults to ``false``.

        :default: false`.

        :stability: experimental
        :schema: CssParserConfiguration#allowWrongLineComments
        '''
        result = self._values.get("allow_wrong_line_comments")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def css_modules(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables CSS Modules-specific syntax such as ``:local``, ``:global``, ``composes``, and ``@value``.

        When unset, Biome enables this syntax automatically for files whose names end in
        ``.module.css`` or ``.module.scss; otherwise, it defaults to ``false`. Enable it explicitly when CSS Module files
        use another naming convention.

        :stability: experimental
        :schema: CssParserConfiguration#cssModules
        '''
        result = self._values.get("css_modules")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def tailwind_directives(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables parsing Tailwind CSS 4.0 directives and functions, including ``@theme``, ``@utility``, ``@variant``, ``@source``, and ``@apply``. Defaults to ``false``.

        :default: false`.

        :stability: experimental
        :schema: CssParserConfiguration#tailwindDirectives
        '''
        result = self._values.get("tailwind_directives")
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
    '''(experimental) Objects are expanded when the first property has a leading newline.

    Arrays remain on one
    line if they fit. (auto)

    :stability: experimental
    '''
    ALWAYS = "ALWAYS"
    '''(experimental) Objects and arrays are always expanded.

    (always)

    :stability: experimental
    '''
    NEVER = "NEVER"
    '''(experimental) Objects and arrays remain on one line if they fit.

    (never)

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
        '''(experimental) The file handling configuration.

        :param experimental_scanner_ignores: (experimental) **Deprecated:** Please use *force-ignore syntax* in ``files.includes`` instead: `https://biomejs.dev/reference/configuration/#filesincludes <https://biomejs.dev/reference/configuration/#filesincludes>`_. File or directory names that the scanner ignores unconditionally while crawling. Each value matches a complete path component, not a glob. Ignored files are not added to the module graph, so types are not inferred from them.
        :param ignore_unknown: (experimental) Prevents Biome from emitting diagnostics for unrecognized file types. Defaults to ``false``. Default: false`.
        :param includes: (experimental) A list of glob patterns selecting which files and directories Biome can process. If omitted, this option does not further restrict the supported files Biome can process. An empty list selects no files. Biome ignores files under ``node_modules`` even when they match a pattern. The scanner uses these patterns and, when enabled, VCS ignore files while discovering nested configuration and ignore files. When enabled rules use the ``project`` or ``types`` domains, it also indexes source files and project dependencies. It may still discover required metadata or index excluded source files needed for analysis. A pattern beginning with ``!!`` prevents the scanner from indexing matching paths. Patterns are evaluated in order, and a pattern beginning with ``!`` excludes matches.
        :param max_size: (experimental) The maximum source-file size in bytes. Biome skips larger files and emits a warning diagnostic. Defaults to ``1 MiB``. Default: 1 MiB`.

        :stability: experimental
        :schema: FilesConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f06e077779a89de8924deeb042aada1ebd486faca5b2fad3aabff17e1eaaa2e4)
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
        '''(experimental) **Deprecated:** Please use *force-ignore syntax* in ``files.includes`` instead: `https://biomejs.dev/reference/configuration/#filesincludes <https://biomejs.dev/reference/configuration/#filesincludes>`_.

        File or directory names that the scanner ignores unconditionally while crawling. Each value
        matches a complete path component, not a glob. Ignored files are not added to the module graph,
        so types are not inferred from them.

        :stability: experimental
        :schema: FilesConfiguration#experimentalScannerIgnores
        '''
        result = self._values.get("experimental_scanner_ignores")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ignore_unknown(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Prevents Biome from emitting diagnostics for unrecognized file types.

        Defaults to ``false``.

        :default: false`.

        :stability: experimental
        :schema: FilesConfiguration#ignoreUnknown
        '''
        result = self._values.get("ignore_unknown")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def includes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of glob patterns selecting which files and directories Biome can process.

        If omitted,
        this option does not further restrict the supported files Biome can process. An empty list
        selects no files. Biome ignores files under ``node_modules`` even when they match a pattern.

        The scanner uses these patterns and, when enabled, VCS ignore files while discovering nested
        configuration and ignore files. When enabled rules use the ``project`` or ``types`` domains, it
        also indexes source files and project dependencies. It may still discover required metadata or
        index excluded source files needed for analysis. A pattern beginning with ``!!`` prevents the
        scanner from indexing matching paths. Patterns are evaluated in order, and a pattern beginning
        with ``!`` excludes matches.

        :stability: experimental
        :schema: FilesConfiguration#includes
        '''
        result = self._values.get("includes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def max_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum source-file size in bytes.

        Biome skips larger files and emits a warning
        diagnostic. Defaults to ``1 MiB``.

        :default: 1 MiB`.

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
        "delimiter_spacing": "delimiterSpacing",
        "enabled": "enabled",
        "expand": "expand",
        "format_with_errors": "formatWithErrors",
        "includes": "includes",
        "indent_style": "indentStyle",
        "indent_width": "indentWidth",
        "line_ending": "lineEnding",
        "line_width": "lineWidth",
        "trailing_newline": "trailingNewline",
        "use_editorconfig": "useEditorconfig",
    },
)
class FormatterConfiguration:
    def __init__(
        self,
        *,
        attribute_position: typing.Optional["AttributePosition"] = None,
        bracket_same_line: typing.Optional[builtins.bool] = None,
        bracket_spacing: typing.Optional[builtins.bool] = None,
        delimiter_spacing: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        expand: typing.Optional["Expand"] = None,
        format_with_errors: typing.Optional[builtins.bool] = None,
        includes: typing.Optional[typing.Sequence[builtins.str]] = None,
        indent_style: typing.Optional["IndentStyle"] = None,
        indent_width: typing.Optional[jsii.Number] = None,
        line_ending: typing.Optional["LineEnding"] = None,
        line_width: typing.Optional[jsii.Number] = None,
        trailing_newline: typing.Optional[builtins.bool] = None,
        use_editorconfig: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Configures formatting for selected files.

        :param attribute_position: (experimental) The attribute position style in HTML-like languages. Defaults to ``auto``. Default: auto`.
        :param bracket_same_line: (experimental) Controls the placement of the closing bracket for multiline HTML and JSX opening tags. Biome places the bracket at the end of the last attribute line when enabled and on its own line when disabled. This also affects self-closing HTML elements, but self-closing JSX elements are unaffected. Defaults to ``false``. Default: false`.
        :param bracket_spacing: (experimental) Controls spaces inside braces in supported single-line structures. The affected structures vary by language. Defaults to ``true``. Default: true`.
        :param delimiter_spacing: (experimental) Controls spaces immediately inside supported delimiters when their content fits on one line. It doesn't add spaces before opening delimiters or inside empty delimiters. The affected delimiters vary by language. Defaults to ``false``. Default: false`.
        :param enabled: (experimental) Enables or disables the formatter. Defaults to ``true``. Default: true`.
        :param expand: (experimental) Controls whether arrays and objects are formatted on one line or multiple lines. ``auto`` formats objects on multiple lines if the first property has a newline, and arrays on one line if they fit. ``always`` formats arrays and objects on multiple lines. ``never`` formats arrays and objects on one line if they fit. Defaults to ``auto``. When formatting ``package.json``, Biome uses ``always`` unless configured otherwise. Default: auto`.
        :param format_with_errors: (experimental) Allows formatting files that contain syntax errors when set to ``true``. Defaults to ``false``. Default: false`.
        :param includes: (experimental) A list of glob patterns selecting files to format. If omitted, all files selected by ``files.includes`` remain eligible for formatting. An empty list selects no files. This option can only narrow the files selected by ``files.includes``.
        :param indent_style: (experimental) Uses tabs or spaces for indentation. Defaults to ``tab``. Default: tab`.
        :param indent_width: (experimental) Sets the indentation width. With space indentation, this is the number of spaces emitted per indentation level. With tab indentation, Biome emits one tab per level and uses this value as the tab's display width when calculating line length. Accepted values are ``0`` through ``24``. Defaults to ``2``. Default: 2`.
        :param line_ending: (experimental) Selects the line ending. ``auto`` uses the platform convention. Defaults to ``lf``. Default: lf`.
        :param line_width: (experimental) Sets the preferred maximum line width used when deciding where to wrap code. Some content, such as long unbreakable strings, may still exceed this width. Accepted values are ``1`` through ``320``. Defaults to ``80``. Default: 80`.
        :param trailing_newline: (experimental) Whether to add a trailing newline at the end of the file. Defaults to ``true``. Disabling this option can cause compatibility problems with other tools. Default: true`. Disabling
        :param use_editorconfig: (experimental) Controls whether Biome loads formatter settings from an ``.editorconfig`` file. Biome reads ``indent_style``, ``indent_size``, ``end_of_line``, and ``insert_final_newline``. Settings in ``biome.json`` or ``biome.jsonc`` take precedence. Biome loads only one ``.editorconfig``. Nested cascading configurations and the EditorConfig ``root`` property are not supported. Defaults to ``false``. Default: false`.

        :stability: experimental
        :schema: FormatterConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d250053b03cd738e71599a16d0b903766c0befb7557dadc7ffee799234532c78)
            check_type(argname="argument attribute_position", value=attribute_position, expected_type=type_hints["attribute_position"])
            check_type(argname="argument bracket_same_line", value=bracket_same_line, expected_type=type_hints["bracket_same_line"])
            check_type(argname="argument bracket_spacing", value=bracket_spacing, expected_type=type_hints["bracket_spacing"])
            check_type(argname="argument delimiter_spacing", value=delimiter_spacing, expected_type=type_hints["delimiter_spacing"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument expand", value=expand, expected_type=type_hints["expand"])
            check_type(argname="argument format_with_errors", value=format_with_errors, expected_type=type_hints["format_with_errors"])
            check_type(argname="argument includes", value=includes, expected_type=type_hints["includes"])
            check_type(argname="argument indent_style", value=indent_style, expected_type=type_hints["indent_style"])
            check_type(argname="argument indent_width", value=indent_width, expected_type=type_hints["indent_width"])
            check_type(argname="argument line_ending", value=line_ending, expected_type=type_hints["line_ending"])
            check_type(argname="argument line_width", value=line_width, expected_type=type_hints["line_width"])
            check_type(argname="argument trailing_newline", value=trailing_newline, expected_type=type_hints["trailing_newline"])
            check_type(argname="argument use_editorconfig", value=use_editorconfig, expected_type=type_hints["use_editorconfig"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attribute_position is not None:
            self._values["attribute_position"] = attribute_position
        if bracket_same_line is not None:
            self._values["bracket_same_line"] = bracket_same_line
        if bracket_spacing is not None:
            self._values["bracket_spacing"] = bracket_spacing
        if delimiter_spacing is not None:
            self._values["delimiter_spacing"] = delimiter_spacing
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
        if trailing_newline is not None:
            self._values["trailing_newline"] = trailing_newline
        if use_editorconfig is not None:
            self._values["use_editorconfig"] = use_editorconfig

    @builtins.property
    def attribute_position(self) -> typing.Optional["AttributePosition"]:
        '''(experimental) The attribute position style in HTML-like languages.

        Defaults to ``auto``.

        :default: auto`.

        :stability: experimental
        :schema: FormatterConfiguration#attributePosition
        '''
        result = self._values.get("attribute_position")
        return typing.cast(typing.Optional["AttributePosition"], result)

    @builtins.property
    def bracket_same_line(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Controls the placement of the closing bracket for multiline HTML and JSX opening tags.

        Biome
        places the bracket at the end of the last attribute line when enabled and on its own line when
        disabled. This also affects self-closing HTML elements, but self-closing JSX elements are
        unaffected. Defaults to ``false``.

        :default: false`.

        :stability: experimental
        :schema: FormatterConfiguration#bracketSameLine
        '''
        result = self._values.get("bracket_same_line")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def bracket_spacing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Controls spaces inside braces in supported single-line structures.

        The affected structures
        vary by language. Defaults to ``true``.

        :default: true`.

        :stability: experimental
        :schema: FormatterConfiguration#bracketSpacing
        '''
        result = self._values.get("bracket_spacing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def delimiter_spacing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Controls spaces immediately inside supported delimiters when their content fits on one line.

        It doesn't add spaces before opening delimiters or inside empty delimiters.

        The affected delimiters vary by language. Defaults to ``false``.

        :default: false`.

        :stability: experimental
        :schema: FormatterConfiguration#delimiterSpacing
        '''
        result = self._values.get("delimiter_spacing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables the formatter.

        Defaults to ``true``.

        :default: true`.

        :stability: experimental
        :schema: FormatterConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def expand(self) -> typing.Optional["Expand"]:
        '''(experimental) Controls whether arrays and objects are formatted on one line or multiple lines.

        ``auto`` formats objects on multiple lines if the first property has a newline, and arrays on
        one line if they fit.

        ``always`` formats arrays and objects on multiple lines.

        ``never`` formats arrays and objects on one line if they fit.

        Defaults to ``auto``.

        When formatting ``package.json``, Biome uses ``always`` unless configured otherwise.

        :default: auto`.

        :stability: experimental
        :schema: FormatterConfiguration#expand
        '''
        result = self._values.get("expand")
        return typing.cast(typing.Optional["Expand"], result)

    @builtins.property
    def format_with_errors(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allows formatting files that contain syntax errors when set to ``true``.

        Defaults to ``false``.

        :default: false`.

        :stability: experimental
        :schema: FormatterConfiguration#formatWithErrors
        '''
        result = self._values.get("format_with_errors")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def includes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of glob patterns selecting files to format.

        If omitted, all files selected by
        ``files.includes`` remain eligible for formatting. An empty list selects no files. This option
        can only narrow the files selected by ``files.includes``.

        :stability: experimental
        :schema: FormatterConfiguration#includes
        '''
        result = self._values.get("includes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def indent_style(self) -> typing.Optional["IndentStyle"]:
        '''(experimental) Uses tabs or spaces for indentation.

        Defaults to ``tab``.

        :default: tab`.

        :stability: experimental
        :schema: FormatterConfiguration#indentStyle
        '''
        result = self._values.get("indent_style")
        return typing.cast(typing.Optional["IndentStyle"], result)

    @builtins.property
    def indent_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Sets the indentation width.

        With space indentation, this is the number of spaces emitted per
        indentation level. With tab indentation, Biome emits one tab per level and uses this value as
        the tab's display width when calculating line length. Accepted values are ``0`` through ``24``.
        Defaults to ``2``.

        :default: 2`.

        :stability: experimental
        :schema: FormatterConfiguration#indentWidth
        '''
        result = self._values.get("indent_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def line_ending(self) -> typing.Optional["LineEnding"]:
        '''(experimental) Selects the line ending.

        ``auto`` uses the platform convention. Defaults to ``lf``.

        :default: lf`.

        :stability: experimental
        :schema: FormatterConfiguration#lineEnding
        '''
        result = self._values.get("line_ending")
        return typing.cast(typing.Optional["LineEnding"], result)

    @builtins.property
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Sets the preferred maximum line width used when deciding where to wrap code.

        Some content,
        such as long unbreakable strings, may still exceed this width. Accepted values are ``1`` through
        ``320``. Defaults to ``80``.

        :default: 80`.

        :stability: experimental
        :schema: FormatterConfiguration#lineWidth
        '''
        result = self._values.get("line_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def trailing_newline(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to add a trailing newline at the end of the file.

        Defaults to ``true``. Disabling
        this option can cause compatibility problems with other tools.

        :default: true`. Disabling

        :stability: experimental
        :schema: FormatterConfiguration#trailingNewline
        '''
        result = self._values.get("trailing_newline")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def use_editorconfig(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Controls whether Biome loads formatter settings from an ``.editorconfig`` file. Biome reads ``indent_style``, ``indent_size``, ``end_of_line``, and ``insert_final_newline``. Settings in ``biome.json`` or ``biome.jsonc`` take precedence. Biome loads only one ``.editorconfig``. Nested cascading configurations and the EditorConfig ``root`` property are not supported. Defaults to ``false``.

        :default: false`.

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
        '''(experimental) Options that change how GraphQL assist behaves.

        :param enabled: (experimental) Enables or disables assist actions for GraphQL. Defaults to ``false``. Default: false`.

        :stability: experimental
        :schema: GraphqlAssistConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0dbfc7c635234e8ca5c531a8c27d60cc9eb836491490660da8418fad825b69a2)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables assist actions for GraphQL.

        Defaults to ``false``.

        :default: false`.

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
        assist: typing.Optional[typing.Union["GraphqlAssistConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        formatter: typing.Optional[typing.Union["GraphqlFormatterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        linter: typing.Optional[typing.Union["GraphqlLinterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options applied to GraphQL files.

        Language-specific settings take precedence over corresponding global settings. Global settings
        apply when their language-specific counterparts are omitted, unless stated otherwise.

        :param assist: (experimental) GraphQL assist options.
        :param formatter: (experimental) GraphQL formatter options.
        :param linter: (experimental) GraphQL linter options.

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
            type_hints = cached_type_hints(_typecheckingstub__2155336ae80236225feccaa799a660386650fec7a49468bef45ab34ed6677842)
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
    def assist(self) -> typing.Optional["GraphqlAssistConfiguration"]:
        '''(experimental) GraphQL assist options.

        :stability: experimental
        :schema: GraphqlConfiguration#assist
        '''
        result = self._values.get("assist")
        return typing.cast(typing.Optional["GraphqlAssistConfiguration"], result)

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
        '''(experimental) GraphQL linter options.

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
        "trailing_newline": "trailingNewline",
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
        trailing_newline: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options that change how the GraphQL formatter behaves.

        :param bracket_spacing: (experimental) Controls spaces inside the braces of single-line GraphQL object values. Biome formats ``{name: "Biome"}`` when disabled and ``{ name: "Biome" }`` when enabled. If unset, inherits the global bracket spacing setting.
        :param enabled: (experimental) Enables or disables the formatter for GraphQL.
        :param indent_style: (experimental) The indent style applied to GraphQL files. If unset, inherits the global indentation style.
        :param indent_width: (experimental) The indentation width applied to GraphQL files. If unset, inherits the global indentation width.
        :param line_ending: (experimental) The line ending applied to GraphQL files. If unset, inherits the global line ending.
        :param line_width: (experimental) The preferred maximum line width for GraphQL files. If unset, inherits the global line width.
        :param quote_style: (experimental) Reserved for future formatter support. The current formatter preserves standard double-quoted GraphQL strings and does not use this setting.
        :param trailing_newline: (experimental) Whether to add a trailing newline at the end of the file. If unset, inherits the global trailing newline setting.

        :stability: experimental
        :schema: GraphqlFormatterConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__dc9ad6152bf4d6cec4d40f5bfd9a8d0247f6c53cda4876e24cc83741fac1ae9f)
            check_type(argname="argument bracket_spacing", value=bracket_spacing, expected_type=type_hints["bracket_spacing"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument indent_style", value=indent_style, expected_type=type_hints["indent_style"])
            check_type(argname="argument indent_width", value=indent_width, expected_type=type_hints["indent_width"])
            check_type(argname="argument line_ending", value=line_ending, expected_type=type_hints["line_ending"])
            check_type(argname="argument line_width", value=line_width, expected_type=type_hints["line_width"])
            check_type(argname="argument quote_style", value=quote_style, expected_type=type_hints["quote_style"])
            check_type(argname="argument trailing_newline", value=trailing_newline, expected_type=type_hints["trailing_newline"])
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
        if trailing_newline is not None:
            self._values["trailing_newline"] = trailing_newline

    @builtins.property
    def bracket_spacing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Controls spaces inside the braces of single-line GraphQL object values.

        Biome formats
        ``{name: "Biome"}`` when disabled and ``{ name: "Biome" }`` when enabled. If unset, inherits the
        global bracket spacing setting.

        :stability: experimental
        :schema: GraphqlFormatterConfiguration#bracketSpacing
        '''
        result = self._values.get("bracket_spacing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables the formatter for GraphQL.

        :stability: experimental
        :schema: GraphqlFormatterConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def indent_style(self) -> typing.Optional["IndentStyle"]:
        '''(experimental) The indent style applied to GraphQL files.

        If unset, inherits the global indentation style.

        :stability: experimental
        :schema: GraphqlFormatterConfiguration#indentStyle
        '''
        result = self._values.get("indent_style")
        return typing.cast(typing.Optional["IndentStyle"], result)

    @builtins.property
    def indent_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The indentation width applied to GraphQL files.

        If unset, inherits the global indentation
        width.

        :stability: experimental
        :schema: GraphqlFormatterConfiguration#indentWidth
        '''
        result = self._values.get("indent_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def line_ending(self) -> typing.Optional["LineEnding"]:
        '''(experimental) The line ending applied to GraphQL files.

        If unset, inherits the global line ending.

        :stability: experimental
        :schema: GraphqlFormatterConfiguration#lineEnding
        '''
        result = self._values.get("line_ending")
        return typing.cast(typing.Optional["LineEnding"], result)

    @builtins.property
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The preferred maximum line width for GraphQL files.

        If unset, inherits the global line
        width.

        :stability: experimental
        :schema: GraphqlFormatterConfiguration#lineWidth
        '''
        result = self._values.get("line_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def quote_style(self) -> typing.Optional["QuoteStyle"]:
        '''(experimental) Reserved for future formatter support.

        The current formatter preserves standard
        double-quoted GraphQL strings and does not use this setting.

        :stability: experimental
        :schema: GraphqlFormatterConfiguration#quoteStyle
        '''
        result = self._values.get("quote_style")
        return typing.cast(typing.Optional["QuoteStyle"], result)

    @builtins.property
    def trailing_newline(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to add a trailing newline at the end of the file.

        If unset, inherits the global
        trailing newline setting.

        :stability: experimental
        :schema: GraphqlFormatterConfiguration#trailingNewline
        '''
        result = self._values.get("trailing_newline")
        return typing.cast(typing.Optional[builtins.bool], result)

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

        :param enabled: (experimental) Enables or disables the linter for GraphQL.

        :stability: experimental
        :schema: GraphqlLinterConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0d2f81257796562c5e318e2c7b1278da3b88a7b868379f34ecb8d427734ba141)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables the linter for GraphQL.

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
        '''(experimental) Options that change how GritQL assist behaves.

        :param enabled: (experimental) Enables or disables assist actions for GritQL.

        :stability: experimental
        :schema: GritAssistConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__59f4559ad93f10b7671f2d81b54798d511d54078f14b37594d40617170bd4645)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables assist actions for GritQL.

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
        assist: typing.Optional[typing.Union["GritAssistConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        formatter: typing.Optional[typing.Union["GritFormatterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        linter: typing.Optional[typing.Union["GritLinterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options applied to GritQL files.

        Language-specific settings take precedence over corresponding global settings. Global settings
        apply when their language-specific counterparts are omitted, unless stated otherwise.

        :param assist: (experimental) GritQL assist options.
        :param formatter: (experimental) GritQL formatter options.
        :param linter: (experimental) GritQL linter options.

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
            type_hints = cached_type_hints(_typecheckingstub__6767810d80e7477e7c2f6a26f7c7f238a608f28412191ad4e6ab8504edd02a88)
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
    def assist(self) -> typing.Optional["GritAssistConfiguration"]:
        '''(experimental) GritQL assist options.

        :stability: experimental
        :schema: GritConfiguration#assist
        '''
        result = self._values.get("assist")
        return typing.cast(typing.Optional["GritAssistConfiguration"], result)

    @builtins.property
    def formatter(self) -> typing.Optional["GritFormatterConfiguration"]:
        '''(experimental) GritQL formatter options.

        :stability: experimental
        :schema: GritConfiguration#formatter
        '''
        result = self._values.get("formatter")
        return typing.cast(typing.Optional["GritFormatterConfiguration"], result)

    @builtins.property
    def linter(self) -> typing.Optional["GritLinterConfiguration"]:
        '''(experimental) GritQL linter options.

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
        "trailing_newline": "trailingNewline",
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
        trailing_newline: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options that change how the GritQL formatter behaves.

        :param enabled: (experimental) Enables or disables the formatter for GritQL.
        :param indent_style: (experimental) The indent style applied to GritQL files. If unset, inherits the global indentation style.
        :param indent_width: (experimental) The indentation width applied to GritQL files. If unset, inherits the global indentation width.
        :param line_ending: (experimental) The line ending applied to GritQL files. If unset, inherits the global line ending.
        :param line_width: (experimental) The preferred maximum line width for GritQL files. If unset, inherits the global line width.
        :param trailing_newline: (experimental) Whether to add a trailing newline at the end of the file. If unset, inherits the global trailing newline setting.

        :stability: experimental
        :schema: GritFormatterConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__7eb20c598594405c2626c0973407324d66863625354188a196be6d25686d44e8)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument indent_style", value=indent_style, expected_type=type_hints["indent_style"])
            check_type(argname="argument indent_width", value=indent_width, expected_type=type_hints["indent_width"])
            check_type(argname="argument line_ending", value=line_ending, expected_type=type_hints["line_ending"])
            check_type(argname="argument line_width", value=line_width, expected_type=type_hints["line_width"])
            check_type(argname="argument trailing_newline", value=trailing_newline, expected_type=type_hints["trailing_newline"])
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
        if trailing_newline is not None:
            self._values["trailing_newline"] = trailing_newline

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables the formatter for GritQL.

        :stability: experimental
        :schema: GritFormatterConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def indent_style(self) -> typing.Optional["IndentStyle"]:
        '''(experimental) The indent style applied to GritQL files.

        If unset, inherits the global indentation style.

        :stability: experimental
        :schema: GritFormatterConfiguration#indentStyle
        '''
        result = self._values.get("indent_style")
        return typing.cast(typing.Optional["IndentStyle"], result)

    @builtins.property
    def indent_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The indentation width applied to GritQL files.

        If unset, inherits the global indentation
        width.

        :stability: experimental
        :schema: GritFormatterConfiguration#indentWidth
        '''
        result = self._values.get("indent_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def line_ending(self) -> typing.Optional["LineEnding"]:
        '''(experimental) The line ending applied to GritQL files.

        If unset, inherits the global line ending.

        :stability: experimental
        :schema: GritFormatterConfiguration#lineEnding
        '''
        result = self._values.get("line_ending")
        return typing.cast(typing.Optional["LineEnding"], result)

    @builtins.property
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The preferred maximum line width for GritQL files.

        If unset, inherits the global line width.

        :stability: experimental
        :schema: GritFormatterConfiguration#lineWidth
        '''
        result = self._values.get("line_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def trailing_newline(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to add a trailing newline at the end of the file.

        If unset, inherits the global
        trailing newline setting.

        :stability: experimental
        :schema: GritFormatterConfiguration#trailingNewline
        '''
        result = self._values.get("trailing_newline")
        return typing.cast(typing.Optional[builtins.bool], result)

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
        '''(experimental) Options that change how the GritQL linter behaves.

        :param enabled: (experimental) Enables or disables the linter for GritQL.

        :stability: experimental
        :schema: GritLinterConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4f328d623f0baa93f52695005ba45f28881c95ae610fde354116a44bc8b01c30)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables the linter for GritQL.

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
    jsii_type="projen.javascript.biome_config.HtmlAssistConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class HtmlAssistConfiguration:
    def __init__(self, *, enabled: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Options that change how HTML assist behaves.

        :param enabled: (experimental) Enables or disables assist actions for HTML and languages that extend it.

        :stability: experimental
        :schema: HtmlAssistConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4f12d37d14edd5b34740aa842931963f60cd55f179c839350e2c9eb8d0ce519a)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables assist actions for HTML and languages that extend it.

        :stability: experimental
        :schema: HtmlAssistConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HtmlAssistConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.HtmlConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "assist": "assist",
        "experimental_full_support_enabled": "experimentalFullSupportEnabled",
        "formatter": "formatter",
        "linter": "linter",
        "parser": "parser",
    },
)
class HtmlConfiguration:
    def __init__(
        self,
        *,
        assist: typing.Optional[typing.Union["HtmlAssistConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        experimental_full_support_enabled: typing.Optional[builtins.bool] = None,
        formatter: typing.Optional[typing.Union["HtmlFormatterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        linter: typing.Optional[typing.Union["HtmlLinterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        parser: typing.Optional[typing.Union["HtmlParserConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options applied to HTML and languages that extend it.

        Full HTML support and the HTML formatter are experimental. Biome aims to minimize breaking
        changes, but bug fixes and new features may change formatting output or diagnostics.

        Language-specific settings take precedence over corresponding global settings. Global settings
        apply when their language-specific counterparts are omitted, unless stated otherwise.

        :param assist: (experimental) HTML assist options.
        :param experimental_full_support_enabled: (experimental) Enables Biome's experimental full support for ``.html``, ``.vue``, ``.svelte``, and ``.astro`` files. In this mode, Biome parses the complete document and can analyze or format its markup and supported embedded languages. When disabled, ``.vue``, ``.svelte``, and ``.astro`` files use legacy handling, which extracts their JavaScript or TypeScript portions and leaves the rest unchanged. This option selects how these files are processed. It does not enable the HTML formatter. Set ``html.formatter.enabled`` to ``true`` to format complete HTML, Vue, Svelte, and Astro files. Defaults to ``false``. Default: false`.
        :param formatter: (experimental) HTML formatter options.
        :param linter: (experimental) HTML linter options.
        :param parser: (experimental) HTML parsing options.

        :stability: experimental
        :schema: HtmlConfiguration
        '''
        if isinstance(assist, dict):
            assist = HtmlAssistConfiguration(**assist)
        if isinstance(formatter, dict):
            formatter = HtmlFormatterConfiguration(**formatter)
        if isinstance(linter, dict):
            linter = HtmlLinterConfiguration(**linter)
        if isinstance(parser, dict):
            parser = HtmlParserConfiguration(**parser)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__048266f3b4e4769e6485570d4954197f51204fc6e607e2ffe5267f80089b5ded)
            check_type(argname="argument assist", value=assist, expected_type=type_hints["assist"])
            check_type(argname="argument experimental_full_support_enabled", value=experimental_full_support_enabled, expected_type=type_hints["experimental_full_support_enabled"])
            check_type(argname="argument formatter", value=formatter, expected_type=type_hints["formatter"])
            check_type(argname="argument linter", value=linter, expected_type=type_hints["linter"])
            check_type(argname="argument parser", value=parser, expected_type=type_hints["parser"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assist is not None:
            self._values["assist"] = assist
        if experimental_full_support_enabled is not None:
            self._values["experimental_full_support_enabled"] = experimental_full_support_enabled
        if formatter is not None:
            self._values["formatter"] = formatter
        if linter is not None:
            self._values["linter"] = linter
        if parser is not None:
            self._values["parser"] = parser

    @builtins.property
    def assist(self) -> typing.Optional["HtmlAssistConfiguration"]:
        '''(experimental) HTML assist options.

        :stability: experimental
        :schema: HtmlConfiguration#assist
        '''
        result = self._values.get("assist")
        return typing.cast(typing.Optional["HtmlAssistConfiguration"], result)

    @builtins.property
    def experimental_full_support_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables Biome's experimental full support for ``.html``, ``.vue``, ``.svelte``, and ``.astro`` files. In this mode, Biome parses the complete document and can analyze or format its markup and supported embedded languages.

        When disabled, ``.vue``, ``.svelte``, and ``.astro`` files use legacy handling, which extracts their
        JavaScript or TypeScript portions and leaves the rest unchanged. This option selects how
        these files are processed. It does not enable the HTML formatter. Set
        ``html.formatter.enabled`` to ``true`` to format complete HTML, Vue, Svelte, and Astro files.
        Defaults to ``false``.

        :default: false`.

        :stability: experimental
        :schema: HtmlConfiguration#experimentalFullSupportEnabled
        '''
        result = self._values.get("experimental_full_support_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def formatter(self) -> typing.Optional["HtmlFormatterConfiguration"]:
        '''(experimental) HTML formatter options.

        :stability: experimental
        :schema: HtmlConfiguration#formatter
        '''
        result = self._values.get("formatter")
        return typing.cast(typing.Optional["HtmlFormatterConfiguration"], result)

    @builtins.property
    def linter(self) -> typing.Optional["HtmlLinterConfiguration"]:
        '''(experimental) HTML linter options.

        :stability: experimental
        :schema: HtmlConfiguration#linter
        '''
        result = self._values.get("linter")
        return typing.cast(typing.Optional["HtmlLinterConfiguration"], result)

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
        "trailing_newline": "trailingNewline",
        "whitespace_sensitivity": "whitespaceSensitivity",
    },
)
class HtmlFormatterConfiguration:
    def __init__(
        self,
        *,
        attribute_position: typing.Optional["AttributePosition"] = None,
        bracket_same_line: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        indent_script_and_style: typing.Optional[builtins.bool] = None,
        indent_style: typing.Optional["IndentStyle"] = None,
        indent_width: typing.Optional[jsii.Number] = None,
        line_ending: typing.Optional["LineEnding"] = None,
        line_width: typing.Optional[jsii.Number] = None,
        self_close_void_elements: typing.Optional["SelfCloseVoidElements"] = None,
        trailing_newline: typing.Optional[builtins.bool] = None,
        whitespace_sensitivity: typing.Optional["WhitespaceSensitivity"] = None,
    ) -> None:
        '''(experimental) Options that change how the HTML formatter behaves.

        :param attribute_position: (experimental) The attribute position style in HTML elements. If unset, inherits the global attribute position setting.
        :param bracket_same_line: (experimental) Controls the placement of the closing bracket for multiline HTML opening tags. Biome places the bracket at the end of the last attribute line when enabled and on its own line after the last attribute when disabled. This option also affects self-closing HTML elements. If unset, inherits the global ``bracketSameLine`` setting.
        :param enabled: (experimental) Enables or disables the formatter for HTML and languages that extend it. The formatter is experimental and disabled by default. Formatting complete HTML, Vue, Svelte, and Astro files requires ``html.experimentalFullSupportEnabled`` to be ``true``.
        :param indent_script_and_style: (experimental) Controls whether the content of ``<script>`` and ``<style>`` tags is indented by one level in HTML, Vue, Svelte, and Astro files. Defaults to ``false``. Default: false`.
        :param indent_style: (experimental) The indent style applied to HTML and languages that extend it. If unset, inherits the global indentation style.
        :param indent_width: (experimental) The indentation width applied to HTML and languages that extend it. If unset, inherits the global indentation width.
        :param line_ending: (experimental) The line ending applied to HTML and languages that extend it. If unset, inherits the global line ending.
        :param line_width: (experimental) The preferred maximum line width for HTML and languages that extend it. If unset, inherits the global line width.
        :param self_close_void_elements: (experimental) Controls whether void elements are self-closed. Defaults to ``never``. Default: never`.
        :param trailing_newline: (experimental) Whether to add a trailing newline at the end of the file. Unlike other language-specific trailing newline settings, this option defaults to ``true`` instead of inheriting the global setting.
        :param whitespace_sensitivity: (experimental) Controls how the formatter treats whitespace around text and child elements in HTML, Vue, Svelte, and Astro markup. The ``ignore`` setting should be used only when whitespace cannot affect rendered output. Defaults to ``css``. Default: css`.

        :stability: experimental
        :schema: HtmlFormatterConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__bcbf243ebdc0f288a10a4e6b68dc5a1ff88f4d8abe5566f57f212bf101440a69)
            check_type(argname="argument attribute_position", value=attribute_position, expected_type=type_hints["attribute_position"])
            check_type(argname="argument bracket_same_line", value=bracket_same_line, expected_type=type_hints["bracket_same_line"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument indent_script_and_style", value=indent_script_and_style, expected_type=type_hints["indent_script_and_style"])
            check_type(argname="argument indent_style", value=indent_style, expected_type=type_hints["indent_style"])
            check_type(argname="argument indent_width", value=indent_width, expected_type=type_hints["indent_width"])
            check_type(argname="argument line_ending", value=line_ending, expected_type=type_hints["line_ending"])
            check_type(argname="argument line_width", value=line_width, expected_type=type_hints["line_width"])
            check_type(argname="argument self_close_void_elements", value=self_close_void_elements, expected_type=type_hints["self_close_void_elements"])
            check_type(argname="argument trailing_newline", value=trailing_newline, expected_type=type_hints["trailing_newline"])
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
        if trailing_newline is not None:
            self._values["trailing_newline"] = trailing_newline
        if whitespace_sensitivity is not None:
            self._values["whitespace_sensitivity"] = whitespace_sensitivity

    @builtins.property
    def attribute_position(self) -> typing.Optional["AttributePosition"]:
        '''(experimental) The attribute position style in HTML elements.

        If unset, inherits the global attribute
        position setting.

        :stability: experimental
        :schema: HtmlFormatterConfiguration#attributePosition
        '''
        result = self._values.get("attribute_position")
        return typing.cast(typing.Optional["AttributePosition"], result)

    @builtins.property
    def bracket_same_line(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Controls the placement of the closing bracket for multiline HTML opening tags.

        Biome places
        the bracket at the end of the last attribute line when enabled and on its own line after the
        last attribute when disabled. This option also affects self-closing HTML elements. If unset,
        inherits the global ``bracketSameLine`` setting.

        :stability: experimental
        :schema: HtmlFormatterConfiguration#bracketSameLine
        '''
        result = self._values.get("bracket_same_line")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables the formatter for HTML and languages that extend it.

        The formatter is
        experimental and disabled by default. Formatting complete HTML, Vue, Svelte, and Astro files
        requires ``html.experimentalFullSupportEnabled`` to be ``true``.

        :stability: experimental
        :schema: HtmlFormatterConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def indent_script_and_style(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Controls whether the content of ``<script>`` and ``<style>`` tags is indented by one level in HTML, Vue, Svelte, and Astro files.

        Defaults to ``false``.

        :default: false`.

        :stability: experimental
        :schema: HtmlFormatterConfiguration#indentScriptAndStyle
        '''
        result = self._values.get("indent_script_and_style")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def indent_style(self) -> typing.Optional["IndentStyle"]:
        '''(experimental) The indent style applied to HTML and languages that extend it.

        If unset, inherits the global
        indentation style.

        :stability: experimental
        :schema: HtmlFormatterConfiguration#indentStyle
        '''
        result = self._values.get("indent_style")
        return typing.cast(typing.Optional["IndentStyle"], result)

    @builtins.property
    def indent_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The indentation width applied to HTML and languages that extend it.

        If unset, inherits the
        global indentation width.

        :stability: experimental
        :schema: HtmlFormatterConfiguration#indentWidth
        '''
        result = self._values.get("indent_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def line_ending(self) -> typing.Optional["LineEnding"]:
        '''(experimental) The line ending applied to HTML and languages that extend it.

        If unset, inherits the global
        line ending.

        :stability: experimental
        :schema: HtmlFormatterConfiguration#lineEnding
        '''
        result = self._values.get("line_ending")
        return typing.cast(typing.Optional["LineEnding"], result)

    @builtins.property
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The preferred maximum line width for HTML and languages that extend it.

        If unset, inherits
        the global line width.

        :stability: experimental
        :schema: HtmlFormatterConfiguration#lineWidth
        '''
        result = self._values.get("line_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def self_close_void_elements(self) -> typing.Optional["SelfCloseVoidElements"]:
        '''(experimental) Controls whether void elements are self-closed.

        Defaults to ``never``.

        :default: never`.

        :stability: experimental
        :schema: HtmlFormatterConfiguration#selfCloseVoidElements
        '''
        result = self._values.get("self_close_void_elements")
        return typing.cast(typing.Optional["SelfCloseVoidElements"], result)

    @builtins.property
    def trailing_newline(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to add a trailing newline at the end of the file.

        Unlike other language-specific
        trailing newline settings, this option defaults to ``true`` instead of inheriting the global
        setting.

        :stability: experimental
        :schema: HtmlFormatterConfiguration#trailingNewline
        '''
        result = self._values.get("trailing_newline")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def whitespace_sensitivity(self) -> typing.Optional["WhitespaceSensitivity"]:
        '''(experimental) Controls how the formatter treats whitespace around text and child elements in HTML, Vue, Svelte, and Astro markup.

        The ``ignore`` setting should be used only when whitespace cannot
        affect rendered output. Defaults to ``css``.

        :default: css`.

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
    jsii_type="projen.javascript.biome_config.HtmlLinterConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class HtmlLinterConfiguration:
    def __init__(self, *, enabled: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Options that change how the HTML linter behaves.

        :param enabled: (experimental) Enables or disables the linter for HTML and languages that extend it.

        :stability: experimental
        :schema: HtmlLinterConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__271da6fb8e26ef7e9c2ec0ea9fc3487d2975824399c15a87994edbcfcdd37131)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables the linter for HTML and languages that extend it.

        :stability: experimental
        :schema: HtmlLinterConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HtmlLinterConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.HtmlParserConfiguration",
    jsii_struct_bases=[],
    name_mapping={"interpolation": "interpolation", "vue": "vue"},
)
class HtmlParserConfiguration:
    def __init__(
        self,
        *,
        interpolation: typing.Optional[builtins.bool] = None,
        vue: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options that change how the HTML parser behaves.

        :param interpolation: (experimental) Enables double-curly interpolation expressions such as ``{{ expression }}`` in ``.html`` files. Defaults to ``false``. Default: false`.
        :param vue: (experimental) Enables parsing Vue syntax (``v-if``, ``v-bind``, etc.) in ``.html`` files. Enabling this option also enables ``interpolation`` implicitly. Biome will already automatically enable Vue parsing in ``.vue`` files, so you probably don't need to enable this option. This only affects ``.html`` files, and does not change how ``.vue``, ``.svelte``, or ``.astro`` files are parsed. Defaults to ``false``. Default: false`.

        :stability: experimental
        :schema: HtmlParserConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1b3cfca5c3ad8f608b86ade05d476530f16da0ba23410a7613236950da38ff37)
            check_type(argname="argument interpolation", value=interpolation, expected_type=type_hints["interpolation"])
            check_type(argname="argument vue", value=vue, expected_type=type_hints["vue"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if interpolation is not None:
            self._values["interpolation"] = interpolation
        if vue is not None:
            self._values["vue"] = vue

    @builtins.property
    def interpolation(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables double-curly interpolation expressions such as ``{{ expression }}`` in ``.html`` files. Defaults to ``false``.

        :default: false`.

        :stability: experimental
        :schema: HtmlParserConfiguration#interpolation
        '''
        result = self._values.get("interpolation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vue(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables parsing Vue syntax (``v-if``, ``v-bind``, etc.) in ``.html`` files. Enabling this option also enables ``interpolation`` implicitly.

        Biome will already automatically enable Vue parsing in ``.vue`` files, so you probably don't need
        to enable this option. This only affects ``.html`` files, and does not change how ``.vue``, ``.svelte``,
        or ``.astro`` files are parsed. Defaults to ``false``.

        :default: false`.

        :stability: experimental
        :schema: HtmlParserConfiguration#vue
        '''
        result = self._values.get("vue")
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
    '''(experimental) Uses tabs for indentation.

    (tab)

    :stability: experimental
    '''
    SPACE = "SPACE"
    '''(experimental) Uses spaces for indentation.

    (space)

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

        :param enabled: (experimental) Enables or disables assist actions for JavaScript and languages that extend it.

        :stability: experimental
        :schema: JsAssistConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__a425594ed8c46868c14fe924e8346d0d10c110ecabdc7f0d160d30bb06cf91ea)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables assist actions for JavaScript and languages that extend it.

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
        "experimental_embedded_snippets_enabled": "experimentalEmbeddedSnippetsEnabled",
        "formatter": "formatter",
        "globals": "globals",
        "jsx_runtime": "jsxRuntime",
        "linter": "linter",
        "parser": "parser",
        "resolver": "resolver",
    },
)
class JsConfiguration:
    def __init__(
        self,
        *,
        assist: typing.Optional[typing.Union["JsAssistConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        experimental_embedded_snippets_enabled: typing.Optional[builtins.bool] = None,
        formatter: typing.Optional[typing.Union["JsFormatterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        globals: typing.Optional[typing.Sequence[builtins.str]] = None,
        jsx_runtime: typing.Optional["JsxRuntime"] = None,
        linter: typing.Optional[typing.Union["JsLinterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        parser: typing.Optional[typing.Union["JsParserConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        resolver: typing.Optional[typing.Union["JsResolverConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options applied to JavaScript, TypeScript, JSX, TSX, and supported languages that embed JavaScript.

        Language-specific settings take precedence over corresponding global settings. Global settings
        apply when their language-specific counterparts are omitted, unless stated otherwise.

        :param assist: (experimental) JavaScript assist options.
        :param experimental_embedded_snippets_enabled: (experimental) Enables experimental parsing, formatting, linting, diagnostics, and fixes for CSS and GraphQL snippets embedded in JavaScript and TypeScript template literals. Biome recognizes CSS in ``css`` and ``styled`` templates and GraphQL in ``gql`` and ``graphql`` templates or calls. Templates containing interpolations are not currently supported. Defaults to ``false``. Default: false`.
        :param formatter: (experimental) JavaScript formatter options.
        :param globals: (experimental) A list of additional names that Biome's JavaScript linter treats as predefined global bindings. Use this for globals supplied by a runtime, framework, or external script that are not declared in the source file.
        :param jsx_runtime: (experimental) Configures how the analyzer accounts for imports used by JSX. This option does not transform JSX or select a runtime for a build tool. Defaults to ``transparent``. Default: transparent`.
        :param linter: (experimental) JavaScript linter options.
        :param parser: (experimental) JavaScript parser options.
        :param resolver: (experimental) JavaScript module and dependency resolver options.

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
        if isinstance(resolver, dict):
            resolver = JsResolverConfiguration(**resolver)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__57972f7094bf127a9fb1918efc38b7f9fd8b7e2a28387b1d59645ced7024c16b)
            check_type(argname="argument assist", value=assist, expected_type=type_hints["assist"])
            check_type(argname="argument experimental_embedded_snippets_enabled", value=experimental_embedded_snippets_enabled, expected_type=type_hints["experimental_embedded_snippets_enabled"])
            check_type(argname="argument formatter", value=formatter, expected_type=type_hints["formatter"])
            check_type(argname="argument globals", value=globals, expected_type=type_hints["globals"])
            check_type(argname="argument jsx_runtime", value=jsx_runtime, expected_type=type_hints["jsx_runtime"])
            check_type(argname="argument linter", value=linter, expected_type=type_hints["linter"])
            check_type(argname="argument parser", value=parser, expected_type=type_hints["parser"])
            check_type(argname="argument resolver", value=resolver, expected_type=type_hints["resolver"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assist is not None:
            self._values["assist"] = assist
        if experimental_embedded_snippets_enabled is not None:
            self._values["experimental_embedded_snippets_enabled"] = experimental_embedded_snippets_enabled
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
        if resolver is not None:
            self._values["resolver"] = resolver

    @builtins.property
    def assist(self) -> typing.Optional["JsAssistConfiguration"]:
        '''(experimental) JavaScript assist options.

        :stability: experimental
        :schema: JsConfiguration#assist
        '''
        result = self._values.get("assist")
        return typing.cast(typing.Optional["JsAssistConfiguration"], result)

    @builtins.property
    def experimental_embedded_snippets_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables experimental parsing, formatting, linting, diagnostics, and fixes for CSS and GraphQL snippets embedded in JavaScript and TypeScript template literals.

        Biome recognizes CSS in ``css`` and ``styled`` templates and GraphQL in ``gql`` and ``graphql``
        templates or calls. Templates containing interpolations are not currently supported.
        Defaults to ``false``.

        :default: false`.

        :stability: experimental
        :schema: JsConfiguration#experimentalEmbeddedSnippetsEnabled
        '''
        result = self._values.get("experimental_embedded_snippets_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def formatter(self) -> typing.Optional["JsFormatterConfiguration"]:
        '''(experimental) JavaScript formatter options.

        :stability: experimental
        :schema: JsConfiguration#formatter
        '''
        result = self._values.get("formatter")
        return typing.cast(typing.Optional["JsFormatterConfiguration"], result)

    @builtins.property
    def globals(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of additional names that Biome's JavaScript linter treats as predefined global bindings.

        Use this for globals supplied by a runtime, framework, or external script that are not
        declared in the source file.

        :stability: experimental
        :schema: JsConfiguration#globals
        '''
        result = self._values.get("globals")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def jsx_runtime(self) -> typing.Optional["JsxRuntime"]:
        '''(experimental) Configures how the analyzer accounts for imports used by JSX.

        This option does not transform
        JSX or select a runtime for a build tool. Defaults to ``transparent``.

        :default: transparent`.

        :stability: experimental
        :schema: JsConfiguration#jsxRuntime
        '''
        result = self._values.get("jsx_runtime")
        return typing.cast(typing.Optional["JsxRuntime"], result)

    @builtins.property
    def linter(self) -> typing.Optional["JsLinterConfiguration"]:
        '''(experimental) JavaScript linter options.

        :stability: experimental
        :schema: JsConfiguration#linter
        '''
        result = self._values.get("linter")
        return typing.cast(typing.Optional["JsLinterConfiguration"], result)

    @builtins.property
    def parser(self) -> typing.Optional["JsParserConfiguration"]:
        '''(experimental) JavaScript parser options.

        :stability: experimental
        :schema: JsConfiguration#parser
        '''
        result = self._values.get("parser")
        return typing.cast(typing.Optional["JsParserConfiguration"], result)

    @builtins.property
    def resolver(self) -> typing.Optional["JsResolverConfiguration"]:
        '''(experimental) JavaScript module and dependency resolver options.

        :stability: experimental
        :schema: JsConfiguration#resolver
        '''
        result = self._values.get("resolver")
        return typing.cast(typing.Optional["JsResolverConfiguration"], result)

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
        "delimiter_spacing": "delimiterSpacing",
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
        "trailing_newline": "trailingNewline",
    },
)
class JsFormatterConfiguration:
    def __init__(
        self,
        *,
        arrow_parentheses: typing.Optional["ArrowParentheses"] = None,
        attribute_position: typing.Optional["AttributePosition"] = None,
        bracket_same_line: typing.Optional[builtins.bool] = None,
        bracket_spacing: typing.Optional[builtins.bool] = None,
        delimiter_spacing: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        expand: typing.Optional["Expand"] = None,
        indent_style: typing.Optional["IndentStyle"] = None,
        indent_width: typing.Optional[jsii.Number] = None,
        jsx_quote_style: typing.Optional["QuoteStyle"] = None,
        line_ending: typing.Optional["LineEnding"] = None,
        line_width: typing.Optional[jsii.Number] = None,
        operator_linebreak: typing.Optional["OperatorLinebreak"] = None,
        quote_properties: typing.Optional["QuoteProperties"] = None,
        quote_style: typing.Optional["QuoteStyle"] = None,
        semicolons: typing.Optional["Semicolons"] = None,
        trailing_commas: typing.Optional["JsTrailingCommas"] = None,
        trailing_newline: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Formatting options specific to JavaScript and languages that extend it.

        :param arrow_parentheses: (experimental) Controls parentheses around arrow-function parameters. ``always`` always prints parentheses, while ``asNeeded`` omits them when an arrow function has one parameter and the syntax permits it. Defaults to ``always``. Default: always`.
        :param attribute_position: (experimental) The attribute position style in JSX elements. If unset, inherits the global attribute position setting.
        :param bracket_same_line: (experimental) Controls the placement of the closing bracket for multiline JSX opening tags. Biome places the bracket at the end of the last attribute line when enabled and on its own line after the last attribute when disabled. Self-closing JSX elements are unaffected. If unset, inherits the global bracket placement setting.
        :param bracket_spacing: (experimental) Controls spaces inside the braces of single-line object literals. Biome formats ``{value: 1}`` when disabled and ``{ value: 1 }`` when enabled. If unset, inherits the global bracket spacing setting.
        :param delimiter_spacing: (experimental) Controls spaces immediately inside supported JavaScript and TypeScript delimiters when their content fits on one line. This affects parentheses, square brackets, template interpolations, TypeScript angle brackets, and JSX expression braces. Empty delimiters are unchanged. It also controls spacing after logical NOT operators. In a chain of logical NOT operators, only the final operator receives a following space. Biome doesn't add spaces before opening delimiters. If unset, inherits the global delimiter spacing setting.
        :param enabled: (experimental) Enables or disables the formatter for JavaScript and languages that extend it.
        :param expand: (experimental) Uses the same ``auto``, ``always``, and ``never`` behavior as the global expansion setting. If unset, inherits the global expansion setting.
        :param indent_style: (experimental) The indent style applied to JavaScript and languages that extend it. If unset, inherits the global indentation style.
        :param indent_width: (experimental) The indentation width applied to JavaScript and languages that extend it. If unset, inherits the global indentation width.
        :param jsx_quote_style: (experimental) Selects the preferred quote style for JSX attribute values. Defaults to ``double``. Default: double`.
        :param line_ending: (experimental) The line ending applied to JavaScript and languages that extend it. If unset, inherits the global line ending.
        :param line_width: (experimental) The preferred maximum line width applied to JavaScript and languages that extend it. If unset, inherits the global line width.
        :param operator_linebreak: (experimental) When breaking binary expressions into multiple lines, whether to break them before or after the binary operator. Defaults to ``after``. Default: after`.
        :param quote_properties: (experimental) Controls whether quotes around object property names are preserved. ``asNeeded`` removes quotes when the property name is valid without them, while ``preserve`` keeps quotes around property names that were quoted in the input. Defaults to ``asNeeded`` in configuration (``as-needed`` on the CLI). Default: asNeeded` in configuration
        :param quote_style: (experimental) Selects the preferred quote style for JavaScript and TypeScript string literals. Biome may use the alternate quote when that avoids additional escaping. Defaults to ``double``. Default: double`.
        :param semicolons: (experimental) Prints semicolons after every statement or only where needed to avoid automatic semicolon insertion hazards. Defaults to ``always``. Default: always`.
        :param trailing_commas: (experimental) Controls trailing commas in multiline comma-separated structures. ``all`` adds trailing commas wherever syntax permits, including function parameters and calls. ``es5`` adds them only in constructs supported by ES5, such as array and object literals, and excludes function parameters, function calls, and TypeScript type parameters. ``none`` removes trailing commas. Defaults to ``all``. Default: all`.
        :param trailing_newline: (experimental) Whether to add a trailing newline at the end of the file. If unset, inherits the global trailing newline setting.

        :stability: experimental
        :schema: JsFormatterConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__83d4960ad9dc84017b237fabc105d7837e8a3ec56d19b1de7e01183651d05de1)
            check_type(argname="argument arrow_parentheses", value=arrow_parentheses, expected_type=type_hints["arrow_parentheses"])
            check_type(argname="argument attribute_position", value=attribute_position, expected_type=type_hints["attribute_position"])
            check_type(argname="argument bracket_same_line", value=bracket_same_line, expected_type=type_hints["bracket_same_line"])
            check_type(argname="argument bracket_spacing", value=bracket_spacing, expected_type=type_hints["bracket_spacing"])
            check_type(argname="argument delimiter_spacing", value=delimiter_spacing, expected_type=type_hints["delimiter_spacing"])
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
            check_type(argname="argument trailing_newline", value=trailing_newline, expected_type=type_hints["trailing_newline"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if arrow_parentheses is not None:
            self._values["arrow_parentheses"] = arrow_parentheses
        if attribute_position is not None:
            self._values["attribute_position"] = attribute_position
        if bracket_same_line is not None:
            self._values["bracket_same_line"] = bracket_same_line
        if bracket_spacing is not None:
            self._values["bracket_spacing"] = bracket_spacing
        if delimiter_spacing is not None:
            self._values["delimiter_spacing"] = delimiter_spacing
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
        if trailing_newline is not None:
            self._values["trailing_newline"] = trailing_newline

    @builtins.property
    def arrow_parentheses(self) -> typing.Optional["ArrowParentheses"]:
        '''(experimental) Controls parentheses around arrow-function parameters.

        ``always`` always prints parentheses,
        while ``asNeeded`` omits them when an arrow function has one parameter and the syntax permits
        it. Defaults to ``always``.

        :default: always`.

        :stability: experimental
        :schema: JsFormatterConfiguration#arrowParentheses
        '''
        result = self._values.get("arrow_parentheses")
        return typing.cast(typing.Optional["ArrowParentheses"], result)

    @builtins.property
    def attribute_position(self) -> typing.Optional["AttributePosition"]:
        '''(experimental) The attribute position style in JSX elements.

        If unset, inherits the global attribute
        position setting.

        :stability: experimental
        :schema: JsFormatterConfiguration#attributePosition
        '''
        result = self._values.get("attribute_position")
        return typing.cast(typing.Optional["AttributePosition"], result)

    @builtins.property
    def bracket_same_line(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Controls the placement of the closing bracket for multiline JSX opening tags.

        Biome places
        the bracket at the end of the last attribute line when enabled and on its own line after the
        last attribute when disabled. Self-closing JSX elements are unaffected. If unset, inherits
        the global bracket placement setting.

        :stability: experimental
        :schema: JsFormatterConfiguration#bracketSameLine
        '''
        result = self._values.get("bracket_same_line")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def bracket_spacing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Controls spaces inside the braces of single-line object literals.

        Biome formats ``{value: 1}``
        when disabled and ``{ value: 1 }`` when enabled. If unset, inherits the global bracket spacing
        setting.

        :stability: experimental
        :schema: JsFormatterConfiguration#bracketSpacing
        '''
        result = self._values.get("bracket_spacing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def delimiter_spacing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Controls spaces immediately inside supported JavaScript and TypeScript delimiters when their content fits on one line.

        This affects parentheses, square brackets, template
        interpolations, TypeScript angle brackets, and JSX expression braces. Empty delimiters are
        unchanged.

        It also controls spacing after logical NOT operators. In a chain of logical NOT operators,
        only the final operator receives a following space. Biome doesn't add spaces before opening
        delimiters.

        If unset, inherits the global delimiter spacing setting.

        :stability: experimental
        :schema: JsFormatterConfiguration#delimiterSpacing
        '''
        result = self._values.get("delimiter_spacing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables the formatter for JavaScript and languages that extend it.

        :stability: experimental
        :schema: JsFormatterConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def expand(self) -> typing.Optional["Expand"]:
        '''(experimental) Uses the same ``auto``, ``always``, and ``never`` behavior as the global expansion setting.

        If unset, inherits the global expansion setting.

        :stability: experimental
        :schema: JsFormatterConfiguration#expand
        '''
        result = self._values.get("expand")
        return typing.cast(typing.Optional["Expand"], result)

    @builtins.property
    def indent_style(self) -> typing.Optional["IndentStyle"]:
        '''(experimental) The indent style applied to JavaScript and languages that extend it.

        If unset, inherits the
        global indentation style.

        :stability: experimental
        :schema: JsFormatterConfiguration#indentStyle
        '''
        result = self._values.get("indent_style")
        return typing.cast(typing.Optional["IndentStyle"], result)

    @builtins.property
    def indent_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The indentation width applied to JavaScript and languages that extend it.

        If unset,
        inherits the global indentation width.

        :stability: experimental
        :schema: JsFormatterConfiguration#indentWidth
        '''
        result = self._values.get("indent_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def jsx_quote_style(self) -> typing.Optional["QuoteStyle"]:
        '''(experimental) Selects the preferred quote style for JSX attribute values.

        Defaults to ``double``.

        :default: double`.

        :stability: experimental
        :schema: JsFormatterConfiguration#jsxQuoteStyle
        '''
        result = self._values.get("jsx_quote_style")
        return typing.cast(typing.Optional["QuoteStyle"], result)

    @builtins.property
    def line_ending(self) -> typing.Optional["LineEnding"]:
        '''(experimental) The line ending applied to JavaScript and languages that extend it.

        If unset, inherits the
        global line ending.

        :stability: experimental
        :schema: JsFormatterConfiguration#lineEnding
        '''
        result = self._values.get("line_ending")
        return typing.cast(typing.Optional["LineEnding"], result)

    @builtins.property
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The preferred maximum line width applied to JavaScript and languages that extend it.

        If
        unset, inherits the global line width.

        :stability: experimental
        :schema: JsFormatterConfiguration#lineWidth
        '''
        result = self._values.get("line_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def operator_linebreak(self) -> typing.Optional["OperatorLinebreak"]:
        '''(experimental) When breaking binary expressions into multiple lines, whether to break them before or after the binary operator.

        Defaults to ``after``.

        :default: after`.

        :stability: experimental
        :schema: JsFormatterConfiguration#operatorLinebreak
        '''
        result = self._values.get("operator_linebreak")
        return typing.cast(typing.Optional["OperatorLinebreak"], result)

    @builtins.property
    def quote_properties(self) -> typing.Optional["QuoteProperties"]:
        '''(experimental) Controls whether quotes around object property names are preserved.

        ``asNeeded`` removes
        quotes when the property name is valid without them, while ``preserve`` keeps quotes around
        property names that were quoted in the input. Defaults to ``asNeeded`` in configuration
        (``as-needed`` on the CLI).

        :default: asNeeded` in configuration

        :stability: experimental
        :schema: JsFormatterConfiguration#quoteProperties
        '''
        result = self._values.get("quote_properties")
        return typing.cast(typing.Optional["QuoteProperties"], result)

    @builtins.property
    def quote_style(self) -> typing.Optional["QuoteStyle"]:
        '''(experimental) Selects the preferred quote style for JavaScript and TypeScript string literals.

        Biome may
        use the alternate quote when that avoids additional escaping. Defaults to ``double``.

        :default: double`.

        :stability: experimental
        :schema: JsFormatterConfiguration#quoteStyle
        '''
        result = self._values.get("quote_style")
        return typing.cast(typing.Optional["QuoteStyle"], result)

    @builtins.property
    def semicolons(self) -> typing.Optional["Semicolons"]:
        '''(experimental) Prints semicolons after every statement or only where needed to avoid automatic semicolon insertion hazards.

        Defaults to ``always``.

        :default: always`.

        :stability: experimental
        :schema: JsFormatterConfiguration#semicolons
        '''
        result = self._values.get("semicolons")
        return typing.cast(typing.Optional["Semicolons"], result)

    @builtins.property
    def trailing_commas(self) -> typing.Optional["JsTrailingCommas"]:
        '''(experimental) Controls trailing commas in multiline comma-separated structures.

        ``all`` adds trailing commas
        wherever syntax permits, including function parameters and calls. ``es5`` adds them only in
        constructs supported by ES5, such as array and object literals, and excludes function
        parameters, function calls, and TypeScript type parameters. ``none`` removes trailing commas.
        Defaults to ``all``.

        :default: all`.

        :stability: experimental
        :schema: JsFormatterConfiguration#trailingCommas
        '''
        result = self._values.get("trailing_commas")
        return typing.cast(typing.Optional["JsTrailingCommas"], result)

    @builtins.property
    def trailing_newline(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to add a trailing newline at the end of the file.

        If unset, inherits the global
        trailing newline setting.

        :stability: experimental
        :schema: JsFormatterConfiguration#trailingNewline
        '''
        result = self._values.get("trailing_newline")
        return typing.cast(typing.Optional[builtins.bool], result)

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

        :param enabled: (experimental) Enables or disables the linter for JavaScript and languages that extend it.

        :stability: experimental
        :schema: JsLinterConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f73a12c3631a151ee57c8ecf68020468207f1fa3a6b5c91890a93814a4119533)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables the linter for JavaScript and languages that extend it.

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
        "jsx_everywhere": "jsxEverywhere",
        "unsafe_parameter_decorators_enabled": "unsafeParameterDecoratorsEnabled",
    },
)
class JsParserConfiguration:
    def __init__(
        self,
        *,
        jsx_everywhere: typing.Optional[builtins.bool] = None,
        unsafe_parameter_decorators_enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options that change how the JavaScript parser behaves.

        :param jsx_everywhere: (experimental) Controls whether ``.js``, ``.mjs``, and ``.cjs`` files may contain JSX syntax. Disabling this option causes JSX in those files to raise a diagnostic. Defaults to ``true``. Default: true`.
        :param unsafe_parameter_decorators_enabled: (experimental) Enables parsing decorators on class parameters. This syntax belongs to an old experimental proposal and may change. Defaults to ``false``. Default: false`.

        :stability: experimental
        :schema: JsParserConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c08c2e4162829556526f51e35e2cd7194c2c8bab38e0d01775d808ad7d573450)
            check_type(argname="argument jsx_everywhere", value=jsx_everywhere, expected_type=type_hints["jsx_everywhere"])
            check_type(argname="argument unsafe_parameter_decorators_enabled", value=unsafe_parameter_decorators_enabled, expected_type=type_hints["unsafe_parameter_decorators_enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if jsx_everywhere is not None:
            self._values["jsx_everywhere"] = jsx_everywhere
        if unsafe_parameter_decorators_enabled is not None:
            self._values["unsafe_parameter_decorators_enabled"] = unsafe_parameter_decorators_enabled

    @builtins.property
    def jsx_everywhere(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Controls whether ``.js``, ``.mjs``, and ``.cjs`` files may contain JSX syntax. Disabling this option causes JSX in those files to raise a diagnostic. Defaults to ``true``.

        :default: true`.

        :stability: experimental
        :schema: JsParserConfiguration#jsxEverywhere
        '''
        result = self._values.get("jsx_everywhere")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def unsafe_parameter_decorators_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables parsing decorators on class parameters.

        This syntax belongs to an old experimental
        proposal and may change. Defaults to ``false``.

        :default: false`.

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
    jsii_type="projen.javascript.biome_config.JsResolverConfiguration",
    jsii_struct_bases=[],
    name_mapping={"experimental_pnpm_catalogs": "experimentalPnpmCatalogs"},
)
class JsResolverConfiguration:
    def __init__(
        self,
        *,
        experimental_pnpm_catalogs: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Resolver options specific to JavaScript files.

        :param experimental_pnpm_catalogs: (experimental) Enables pnpm workspace catalog resolution for JavaScript package manifests. Opt-in: - Set ``javascript.resolver.experimentalPnpmCatalogs`` to ``true``. Scope: - Resolves ``catalog:`` and ``catalog:<name>`` dependency versions from ``package.json``. - Applies to ``dependencies``, ``devDependencies``, and ``peerDependencies``. Fail-safe behavior: - If ``pnpm-workspace.yaml`` is missing, unreadable, or cannot be parsed, Biome silently falls back to the default behavior (as if this option were disabled). - Unknown keys and unsupported value shapes in ``pnpm-workspace.yaml`` are ignored. Limitations: - Only ``pnpm-workspace.yaml`` is read. - Biome only reads top-level ``catalog`` / ``catalogs`` mappings and scalar string entries. Defaults to ``false``. Default: false`.

        :stability: experimental
        :schema: JsResolverConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__1e0ae3402dedb6e0fd3dbd8c7871dc3e24d95f19bd630a3675b446eeff16b76d)
            check_type(argname="argument experimental_pnpm_catalogs", value=experimental_pnpm_catalogs, expected_type=type_hints["experimental_pnpm_catalogs"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if experimental_pnpm_catalogs is not None:
            self._values["experimental_pnpm_catalogs"] = experimental_pnpm_catalogs

    @builtins.property
    def experimental_pnpm_catalogs(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables pnpm workspace catalog resolution for JavaScript package manifests.

        Opt-in:

        - Set ``javascript.resolver.experimentalPnpmCatalogs`` to ``true``.

        Scope:

        - Resolves ``catalog:`` and ``catalog:<name>`` dependency versions from
          ``package.json``.
        - Applies to ``dependencies``, ``devDependencies``, and ``peerDependencies``.

        Fail-safe behavior:

        - If ``pnpm-workspace.yaml`` is missing, unreadable, or cannot be parsed,
          Biome silently falls back to the default behavior (as if this option
          were disabled).
        - Unknown keys and unsupported value shapes in ``pnpm-workspace.yaml`` are
          ignored.

        Limitations:

        - Only ``pnpm-workspace.yaml`` is read.
        - Biome only reads top-level ``catalog`` / ``catalogs`` mappings and scalar
          string entries.

        Defaults to ``false``.

        :default: false`.

        :stability: experimental
        :schema: JsResolverConfiguration#experimentalPnpmCatalogs
        '''
        result = self._values.get("experimental_pnpm_catalogs")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JsResolverConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.javascript.biome_config.JsTrailingCommas")
class JsTrailingCommas(enum.Enum):
    '''(experimental) Print trailing commas wherever possible in multi-line comma-separated syntactic structures for JavaScript/TypeScript files.

    :stability: experimental
    :schema: JsTrailingCommas
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


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.JsonAssistConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class JsonAssistConfiguration:
    def __init__(self, *, enabled: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Assist options specific to the JSON linter.

        :param enabled: (experimental) Enables or disables assist actions for JSON and languages that extend it.

        :stability: experimental
        :schema: JsonAssistConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f1fb6aa8858788da93c40533dca490e5cba8b040cbde40fcc78bbd02d8efd181)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables assist actions for JSON and languages that extend it.

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
        assist: typing.Optional[typing.Union["JsonAssistConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        formatter: typing.Optional[typing.Union["JsonFormatterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        linter: typing.Optional[typing.Union["JsonLinterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        parser: typing.Optional[typing.Union["JsonParserConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options applied to JSON, JSONC, and recognized JSON-based configuration files.

        Language-specific settings take precedence over corresponding global settings. Global settings
        apply when their language-specific counterparts are omitted, unless stated otherwise.

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
            type_hints = cached_type_hints(_typecheckingstub__67ca83a8b26135c2a9bc9fcca08d39f860187439c18546ca3bb66035d3ec1146)
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
    def assist(self) -> typing.Optional["JsonAssistConfiguration"]:
        '''(experimental) Assist options.

        :stability: experimental
        :schema: JsonConfiguration#assist
        '''
        result = self._values.get("assist")
        return typing.cast(typing.Optional["JsonAssistConfiguration"], result)

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
        "delimiter_spacing": "delimiterSpacing",
        "enabled": "enabled",
        "expand": "expand",
        "indent_style": "indentStyle",
        "indent_width": "indentWidth",
        "line_ending": "lineEnding",
        "line_width": "lineWidth",
        "trailing_commas": "trailingCommas",
        "trailing_newline": "trailingNewline",
    },
)
class JsonFormatterConfiguration:
    def __init__(
        self,
        *,
        bracket_spacing: typing.Optional[builtins.bool] = None,
        delimiter_spacing: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        expand: typing.Optional["Expand"] = None,
        indent_style: typing.Optional["IndentStyle"] = None,
        indent_width: typing.Optional[jsii.Number] = None,
        line_ending: typing.Optional["LineEnding"] = None,
        line_width: typing.Optional[jsii.Number] = None,
        trailing_commas: typing.Optional["JsonTrailingCommas"] = None,
        trailing_newline: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param bracket_spacing: (experimental) Whether to insert spaces inside braces in object literals. If unset, inherits the global bracket spacing setting.
        :param delimiter_spacing: (experimental) Controls spaces inside JSON square brackets when their content fits on one line. When enabled, ``[1, 2, 3]`` becomes ``[ 1, 2, 3 ]``. Empty brackets are unchanged. If unset, inherits the global delimiter spacing setting.
        :param enabled: (experimental) Enables or disables the formatter for JSON and languages that extend it.
        :param expand: (experimental) Uses the same ``auto``, ``always``, and ``never`` behavior as the global expansion setting. If unset, inherits the global expansion setting. When formatting ``package.json``, Biome uses ``always`` unless configured otherwise.
        :param indent_style: (experimental) The indent style applied to JSON and languages that extend it. If unset, inherits the global indentation style.
        :param indent_width: (experimental) The indentation width applied to JSON and languages that extend it. If unset, inherits the global indentation width.
        :param line_ending: (experimental) The line ending applied to JSON and languages that extend it. If unset, inherits the global line ending.
        :param line_width: (experimental) The preferred maximum line width applied to JSON and languages that extend it. If unset, inherits the global line width.
        :param trailing_commas: (experimental) Controls trailing commas in multiline JSON arrays and objects. ``none`` removes trailing commas, while ``all`` adds them wherever the JSON formatter supports them. Use ``all`` only for JSON variants that allow trailing commas, and ensure ``json.parser.allowTrailingCommas`` is enabled or automatically detected for those files. Defaults to ``none``. Default: none`.
        :param trailing_newline: (experimental) Whether to add a trailing newline at the end of the file. If unset, inherits the global trailing newline setting.

        :stability: experimental
        :schema: JsonFormatterConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4a0473ff26e9f0e1a38d7055c4e466dc2b2b92f24abfce11672601c5a1f6f4a2)
            check_type(argname="argument bracket_spacing", value=bracket_spacing, expected_type=type_hints["bracket_spacing"])
            check_type(argname="argument delimiter_spacing", value=delimiter_spacing, expected_type=type_hints["delimiter_spacing"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument expand", value=expand, expected_type=type_hints["expand"])
            check_type(argname="argument indent_style", value=indent_style, expected_type=type_hints["indent_style"])
            check_type(argname="argument indent_width", value=indent_width, expected_type=type_hints["indent_width"])
            check_type(argname="argument line_ending", value=line_ending, expected_type=type_hints["line_ending"])
            check_type(argname="argument line_width", value=line_width, expected_type=type_hints["line_width"])
            check_type(argname="argument trailing_commas", value=trailing_commas, expected_type=type_hints["trailing_commas"])
            check_type(argname="argument trailing_newline", value=trailing_newline, expected_type=type_hints["trailing_newline"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bracket_spacing is not None:
            self._values["bracket_spacing"] = bracket_spacing
        if delimiter_spacing is not None:
            self._values["delimiter_spacing"] = delimiter_spacing
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
        if trailing_newline is not None:
            self._values["trailing_newline"] = trailing_newline

    @builtins.property
    def bracket_spacing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to insert spaces inside braces in object literals.

        If unset, inherits the global
        bracket spacing setting.

        :stability: experimental
        :schema: JsonFormatterConfiguration#bracketSpacing
        '''
        result = self._values.get("bracket_spacing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def delimiter_spacing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Controls spaces inside JSON square brackets when their content fits on one line.

        When
        enabled, ``[1, 2, 3]`` becomes ``[ 1, 2, 3 ]``. Empty brackets are unchanged.

        If unset, inherits the global delimiter spacing setting.

        :stability: experimental
        :schema: JsonFormatterConfiguration#delimiterSpacing
        '''
        result = self._values.get("delimiter_spacing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables the formatter for JSON and languages that extend it.

        :stability: experimental
        :schema: JsonFormatterConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def expand(self) -> typing.Optional["Expand"]:
        '''(experimental) Uses the same ``auto``, ``always``, and ``never`` behavior as the global expansion setting.

        If unset, inherits the global expansion setting.

        When formatting ``package.json``, Biome uses ``always`` unless configured otherwise.

        :stability: experimental
        :schema: JsonFormatterConfiguration#expand
        '''
        result = self._values.get("expand")
        return typing.cast(typing.Optional["Expand"], result)

    @builtins.property
    def indent_style(self) -> typing.Optional["IndentStyle"]:
        '''(experimental) The indent style applied to JSON and languages that extend it.

        If unset, inherits the global
        indentation style.

        :stability: experimental
        :schema: JsonFormatterConfiguration#indentStyle
        '''
        result = self._values.get("indent_style")
        return typing.cast(typing.Optional["IndentStyle"], result)

    @builtins.property
    def indent_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The indentation width applied to JSON and languages that extend it.

        If unset, inherits the
        global indentation width.

        :stability: experimental
        :schema: JsonFormatterConfiguration#indentWidth
        '''
        result = self._values.get("indent_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def line_ending(self) -> typing.Optional["LineEnding"]:
        '''(experimental) The line ending applied to JSON and languages that extend it.

        If unset, inherits the global
        line ending.

        :stability: experimental
        :schema: JsonFormatterConfiguration#lineEnding
        '''
        result = self._values.get("line_ending")
        return typing.cast(typing.Optional["LineEnding"], result)

    @builtins.property
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The preferred maximum line width applied to JSON and languages that extend it.

        If unset,
        inherits the global line width.

        :stability: experimental
        :schema: JsonFormatterConfiguration#lineWidth
        '''
        result = self._values.get("line_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def trailing_commas(self) -> typing.Optional["JsonTrailingCommas"]:
        '''(experimental) Controls trailing commas in multiline JSON arrays and objects.

        ``none`` removes trailing
        commas, while ``all`` adds them wherever the JSON formatter supports them. Use ``all`` only for
        JSON variants that allow trailing commas, and ensure ``json.parser.allowTrailingCommas`` is
        enabled or automatically detected for those files. Defaults to ``none``.

        :default: none`.

        :stability: experimental
        :schema: JsonFormatterConfiguration#trailingCommas
        '''
        result = self._values.get("trailing_commas")
        return typing.cast(typing.Optional["JsonTrailingCommas"], result)

    @builtins.property
    def trailing_newline(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to add a trailing newline at the end of the file.

        If unset, inherits the global
        trailing newline setting.

        :stability: experimental
        :schema: JsonFormatterConfiguration#trailingNewline
        '''
        result = self._values.get("trailing_newline")
        return typing.cast(typing.Optional[builtins.bool], result)

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

        :param enabled: (experimental) Enables or disables the linter for JSON and languages that extend it.

        :stability: experimental
        :schema: JsonLinterConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__850ce6cbde62685594cc979eca53b2938f923a2a6a9d3168729c891046c7be59)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables the linter for JSON and languages that extend it.

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
        '''(experimental) Options that change how the JSON parser behaves.

        :param allow_comments: (experimental) Controls whether comments are allowed in files parsed as JSON. When unset, Biome follows the file type's default behavior. An explicit value overrides that behavior, except that ``biome.jsonc`` always allows comments.
        :param allow_trailing_commas: (experimental) Controls whether trailing commas are allowed in files parsed as JSON. When unset, Biome follows the file type's default behavior. An explicit value overrides that behavior, except that ``biome.jsonc`` always allows trailing commas.

        :stability: experimental
        :schema: JsonParserConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0ced0fa0672bed168a8348653ba985dd1a20d26c25f814d1492bdc2bb5b05233)
            check_type(argname="argument allow_comments", value=allow_comments, expected_type=type_hints["allow_comments"])
            check_type(argname="argument allow_trailing_commas", value=allow_trailing_commas, expected_type=type_hints["allow_trailing_commas"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_comments is not None:
            self._values["allow_comments"] = allow_comments
        if allow_trailing_commas is not None:
            self._values["allow_trailing_commas"] = allow_trailing_commas

    @builtins.property
    def allow_comments(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Controls whether comments are allowed in files parsed as JSON.

        When unset, Biome follows the
        file type's default behavior. An explicit value overrides that behavior, except that
        ``biome.jsonc`` always allows comments.

        :stability: experimental
        :schema: JsonParserConfiguration#allowComments
        '''
        result = self._values.get("allow_comments")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def allow_trailing_commas(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Controls whether trailing commas are allowed in files parsed as JSON.

        When unset, Biome
        follows the file type's default behavior. An explicit value overrides that behavior, except
        that ``biome.jsonc`` always allows trailing commas.

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


@jsii.enum(jsii_type="projen.javascript.biome_config.JsonTrailingCommas")
class JsonTrailingCommas(enum.Enum):
    '''(experimental) Controls trailing commas in multiline JSON arrays and objects.

    Use ``all`` only for JSON variants that allow trailing commas, and ensure ``json.parser.allowTrailingCommas`` is enabled or automatically detected for those files.

    :stability: experimental
    :schema: JsonTrailingCommas
    '''

    NONE = "NONE"
    '''(experimental) none.

    :stability: experimental
    '''
    ALL = "ALL"
    '''(experimental) all.

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.javascript.biome_config.JsxRuntime")
class JsxRuntime(enum.Enum):
    '''(experimental) How Biome's analyzer accounts for imports used by JSX.

    :stability: experimental
    :schema: JsxRuntime
    '''

    TRANSPARENT = "TRANSPARENT"
    '''(experimental) An automatic or native JSX environment that doesn't require an in-scope factory import.

    (transparent)

    :stability: experimental
    '''
    REACT_CLASSIC = "REACT_CLASSIC"
    '''(experimental) A classic React environment that requires the React import, or custom JSX factory imports configured in ``tsconfig.json``.

    Corresponds to the ``react`` value for the ``jsx`` option in TypeScript's
    ``tsconfig.json``.

    This option should only be necessary if you cannot upgrade to a React
    version that supports the new JSX runtime. For more information about
    the old vs. new JSX runtime, please see:
    `https://legacy.reactjs.org/blog/2020/09/22/introducing-the-new-jsx-transform.html <https://legacy.reactjs.org/blog/2020/09/22/introducing-the-new-jsx-transform.html>`_ (reactClassic)

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.javascript.biome_config.LineEnding")
class LineEnding(enum.Enum):
    '''
    :stability: experimental
    :schema: LineEnding
    '''

    LF = "LF"
    '''(experimental) Line Feed only (\\n), common on Linux and macOS as well as inside git repos (lf).

    :stability: experimental
    '''
    CRLF = "CRLF"
    '''(experimental) Carriage Return + Line Feed characters (\\r\\n), common on Windows (crlf).

    :stability: experimental
    '''
    CR = "CR"
    '''(experimental) Carriage Return character only (\\r), used very rarely (cr).

    :stability: experimental
    '''
    AUTO = "AUTO"
    '''(experimental) Automatically use CRLF on Windows and LF on other platforms (auto).

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
        domains: typing.Optional[typing.Union["RuleDomains", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[builtins.bool] = None,
        includes: typing.Optional[typing.Sequence[builtins.str]] = None,
        rules: typing.Optional[typing.Union["Rules", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param domains: (experimental) Configures rules associated with a framework, library, project-wide analysis, or type analysis. Keys are domain names and values are ``all``, ``recommended``, or ``none``. Enabling rules from the ``project`` or ``types`` domains activates project and dependency scanning. The ``types`` domain also enables type-aware resolution.
        :param enabled: (experimental) Enables or disables the linter. Defaults to ``true``. Default: true`.
        :param includes: (experimental) A list of glob patterns selecting files to lint. If omitted, all files selected by ``files.includes`` remain eligible for linting. An empty list selects no files. This option can only narrow the files selected by ``files.includes``.
        :param rules: (experimental) The lint-rule configuration.

        :stability: experimental
        :schema: LinterConfiguration
        '''
        if isinstance(domains, dict):
            domains = RuleDomains(**domains)
        if isinstance(rules, dict):
            rules = Rules(**rules)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__65dab822a12255f6f845b9299f073f8d1333a90456c41e244f29210e8ad1de68)
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
    def domains(self) -> typing.Optional["RuleDomains"]:
        '''(experimental) Configures rules associated with a framework, library, project-wide analysis, or type analysis.

        Keys are domain names and values are ``all``, ``recommended``, or ``none``.
        Enabling rules from the ``project`` or ``types`` domains activates project and dependency
        scanning. The ``types`` domain also enables type-aware resolution.

        :stability: experimental
        :schema: LinterConfiguration#domains
        '''
        result = self._values.get("domains")
        return typing.cast(typing.Optional["RuleDomains"], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables the linter.

        Defaults to ``true``.

        :default: true`.

        :stability: experimental
        :schema: LinterConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def includes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of glob patterns selecting files to lint.

        If omitted, all files selected by
        ``files.includes`` remain eligible for linting. An empty list selects no files. This option can
        only narrow the files selected by ``files.includes``.

        :stability: experimental
        :schema: LinterConfiguration#includes
        '''
        result = self._values.get("includes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def rules(self) -> typing.Optional["Rules"]:
        '''(experimental) The lint-rule configuration.

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


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.MarkdownConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "analyze_embeds": "analyzeEmbeds",
        "formatter": "formatter",
        "linter": "linter",
        "parser": "parser",
    },
)
class MarkdownConfiguration:
    def __init__(
        self,
        *,
        analyze_embeds: typing.Optional[builtins.bool] = None,
        formatter: typing.Optional[typing.Union["MarkdownFormatterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        linter: typing.Optional[typing.Union["MarkdownLinterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        parser: typing.Optional[typing.Union["MarkdownParserConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options applied to Markdown files.

        :param analyze_embeds: (experimental) Runs the linter and assist actions on the code inside fenced code blocks, frontmatter, and HTML blocks, with the rules and actions of the code's language. Defaults to ``false``. Default: false`.
        :param formatter: (experimental) Formatter options.
        :param linter: (experimental) Linter options.
        :param parser: (experimental) Parsing options.

        :stability: experimental
        :schema: MarkdownConfiguration
        '''
        if isinstance(formatter, dict):
            formatter = MarkdownFormatterConfiguration(**formatter)
        if isinstance(linter, dict):
            linter = MarkdownLinterConfiguration(**linter)
        if isinstance(parser, dict):
            parser = MarkdownParserConfiguration(**parser)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__9c0f77fe366fbbfddda5ede857901f0002d502c1e847f7998e0ef60a07b15ee5)
            check_type(argname="argument analyze_embeds", value=analyze_embeds, expected_type=type_hints["analyze_embeds"])
            check_type(argname="argument formatter", value=formatter, expected_type=type_hints["formatter"])
            check_type(argname="argument linter", value=linter, expected_type=type_hints["linter"])
            check_type(argname="argument parser", value=parser, expected_type=type_hints["parser"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if analyze_embeds is not None:
            self._values["analyze_embeds"] = analyze_embeds
        if formatter is not None:
            self._values["formatter"] = formatter
        if linter is not None:
            self._values["linter"] = linter
        if parser is not None:
            self._values["parser"] = parser

    @builtins.property
    def analyze_embeds(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Runs the linter and assist actions on the code inside fenced code blocks, frontmatter, and HTML blocks, with the rules and actions of the code's language.

        Defaults to ``false``.

        :default: false`.

        :stability: experimental
        :schema: MarkdownConfiguration#analyzeEmbeds
        '''
        result = self._values.get("analyze_embeds")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def formatter(self) -> typing.Optional["MarkdownFormatterConfiguration"]:
        '''(experimental) Formatter options.

        :stability: experimental
        :schema: MarkdownConfiguration#formatter
        '''
        result = self._values.get("formatter")
        return typing.cast(typing.Optional["MarkdownFormatterConfiguration"], result)

    @builtins.property
    def linter(self) -> typing.Optional["MarkdownLinterConfiguration"]:
        '''(experimental) Linter options.

        :stability: experimental
        :schema: MarkdownConfiguration#linter
        '''
        result = self._values.get("linter")
        return typing.cast(typing.Optional["MarkdownLinterConfiguration"], result)

    @builtins.property
    def parser(self) -> typing.Optional["MarkdownParserConfiguration"]:
        '''(experimental) Parsing options.

        :stability: experimental
        :schema: MarkdownConfiguration#parser
        '''
        result = self._values.get("parser")
        return typing.cast(typing.Optional["MarkdownParserConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MarkdownConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.MarkdownFormatterConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "format_embeds": "formatEmbeds",
        "indent_style": "indentStyle",
        "indent_width": "indentWidth",
        "line_ending": "lineEnding",
        "line_width": "lineWidth",
        "prose_wrap": "proseWrap",
        "trailing_newline": "trailingNewline",
    },
)
class MarkdownFormatterConfiguration:
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        format_embeds: typing.Optional[builtins.bool] = None,
        indent_style: typing.Optional["IndentStyle"] = None,
        indent_width: typing.Optional[jsii.Number] = None,
        line_ending: typing.Optional["LineEnding"] = None,
        line_width: typing.Optional[jsii.Number] = None,
        prose_wrap: typing.Optional["ProseWrap"] = None,
        trailing_newline: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options that change how the Markdown formatter behaves.

        :param enabled: (experimental) Control the formatter for Markdown (and its super languages) files.
        :param format_embeds: (experimental) Formats the code inside fenced code blocks, frontmatter, and HTML blocks with the formatter of the code's language. Defaults to ``true``. A block with a syntax error stays as written, and Biome still formats the rest of the file. When this option is ``false``, Biome keeps every block as written. Default: true`.
        :param indent_style: (experimental) The indent style applied to Markdown files.
        :param indent_width: (experimental) The size of the indentation applied to Markdown files. Defaults to 2. Default: 2.
        :param line_ending: (experimental) The type of line ending applied to Markdown (and its super languages) files. ``auto`` uses CRLF on Windows and LF on other platforms.
        :param line_width: (experimental) What's the max width of a line applied to Markdown files. Defaults to 80. Default: 80.
        :param prose_wrap: (experimental) Controls whether Biome keeps, adds, or removes line breaks in Markdown paragraphs. Manual line breaks are always kept. In Markdown, a manual line break is created by ending a line with two spaces or a backslash.
        :param trailing_newline: (experimental) Whether to add a trailing newline at the end of the file. Setting this option to ``false`` is **highly discouraged** because it could cause many problems with other tools: - https://thoughtbot.com/blog/no-newline-at-end-of-file - https://callmeryan.medium.com/no-newline-at-end-of-file-navigating-gits-warning-for-android-developers-af14e73dd804 - https://unix.stackexchange.com/questions/345548/how-to-cat-files-together-adding-missing-newlines-at-end-of-some-files Disable the option at your own risk. Defaults to true. Default: true.

        :stability: experimental
        :schema: MarkdownFormatterConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4ee25d4f71c40309136ce3dadf5413566922dcca0df3b908293e084a82af789a)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument format_embeds", value=format_embeds, expected_type=type_hints["format_embeds"])
            check_type(argname="argument indent_style", value=indent_style, expected_type=type_hints["indent_style"])
            check_type(argname="argument indent_width", value=indent_width, expected_type=type_hints["indent_width"])
            check_type(argname="argument line_ending", value=line_ending, expected_type=type_hints["line_ending"])
            check_type(argname="argument line_width", value=line_width, expected_type=type_hints["line_width"])
            check_type(argname="argument prose_wrap", value=prose_wrap, expected_type=type_hints["prose_wrap"])
            check_type(argname="argument trailing_newline", value=trailing_newline, expected_type=type_hints["trailing_newline"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if format_embeds is not None:
            self._values["format_embeds"] = format_embeds
        if indent_style is not None:
            self._values["indent_style"] = indent_style
        if indent_width is not None:
            self._values["indent_width"] = indent_width
        if line_ending is not None:
            self._values["line_ending"] = line_ending
        if line_width is not None:
            self._values["line_width"] = line_width
        if prose_wrap is not None:
            self._values["prose_wrap"] = prose_wrap
        if trailing_newline is not None:
            self._values["trailing_newline"] = trailing_newline

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the formatter for Markdown (and its super languages) files.

        :stability: experimental
        :schema: MarkdownFormatterConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def format_embeds(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Formats the code inside fenced code blocks, frontmatter, and HTML blocks with the formatter of the code's language.

        Defaults to ``true``.

        A block with a syntax error stays as written, and Biome still formats the rest of the file.

        When this option is ``false``, Biome keeps every block as written.

        :default: true`.

        :stability: experimental
        :schema: MarkdownFormatterConfiguration#formatEmbeds
        '''
        result = self._values.get("format_embeds")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def indent_style(self) -> typing.Optional["IndentStyle"]:
        '''(experimental) The indent style applied to Markdown files.

        :stability: experimental
        :schema: MarkdownFormatterConfiguration#indentStyle
        '''
        result = self._values.get("indent_style")
        return typing.cast(typing.Optional["IndentStyle"], result)

    @builtins.property
    def indent_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation applied to Markdown files.

        Defaults to 2.

        :default: 2.

        :stability: experimental
        :schema: MarkdownFormatterConfiguration#indentWidth
        '''
        result = self._values.get("indent_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def line_ending(self) -> typing.Optional["LineEnding"]:
        '''(experimental) The type of line ending applied to Markdown (and its super languages) files.

        ``auto`` uses CRLF on Windows and LF on other platforms.

        :stability: experimental
        :schema: MarkdownFormatterConfiguration#lineEnding
        '''
        result = self._values.get("line_ending")
        return typing.cast(typing.Optional["LineEnding"], result)

    @builtins.property
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) What's the max width of a line applied to Markdown files.

        Defaults to 80.

        :default: 80.

        :stability: experimental
        :schema: MarkdownFormatterConfiguration#lineWidth
        '''
        result = self._values.get("line_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def prose_wrap(self) -> typing.Optional["ProseWrap"]:
        '''(experimental) Controls whether Biome keeps, adds, or removes line breaks in Markdown paragraphs.

        Manual line breaks are always kept. In Markdown, a manual line break is created by ending a
        line with two spaces or a backslash.

        :stability: experimental
        :schema: MarkdownFormatterConfiguration#proseWrap
        '''
        result = self._values.get("prose_wrap")
        return typing.cast(typing.Optional["ProseWrap"], result)

    @builtins.property
    def trailing_newline(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to add a trailing newline at the end of the file.

        Setting this option to ``false`` is **highly discouraged** because it could cause many problems with other tools:

        - https://thoughtbot.com/blog/no-newline-at-end-of-file
        - https://callmeryan.medium.com/no-newline-at-end-of-file-navigating-gits-warning-for-android-developers-af14e73dd804
        - https://unix.stackexchange.com/questions/345548/how-to-cat-files-together-adding-missing-newlines-at-end-of-some-files

        Disable the option at your own risk.

        Defaults to true.

        :default: true.

        :stability: experimental
        :schema: MarkdownFormatterConfiguration#trailingNewline
        '''
        result = self._values.get("trailing_newline")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MarkdownFormatterConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.MarkdownLinterConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class MarkdownLinterConfiguration:
    def __init__(self, *, enabled: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Options that change how the Markdown linter behaves.

        :param enabled: (experimental) Control the linter for Markdown files.

        :stability: experimental
        :schema: MarkdownLinterConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__0e95f8e46a79bb691a2ac81ce7797be7d5c153005b278d27315908fdc06c7648)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the linter for Markdown files.

        :stability: experimental
        :schema: MarkdownLinterConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MarkdownLinterConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.MarkdownParserConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "cjk_friendly_emphasis": "cjkFriendlyEmphasis",
        "frontmatter": "frontmatter",
        "gfm": "gfm",
    },
)
class MarkdownParserConfiguration:
    def __init__(
        self,
        *,
        cjk_friendly_emphasis: typing.Optional[builtins.bool] = None,
        frontmatter: typing.Optional[builtins.bool] = None,
        gfm: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options that change how the Markdown parser behaves.

        :param cjk_friendly_emphasis: (experimental) Recognizes bold, italic, and strikethrough markers placed directly next to Chinese, Japanese, or Korean text. Defaults to ``false``. Standard Markdown doesn't treat ``**テスト。**テスト`` as bold text, because the closing ``**`` is between a punctuation mark and a letter with no space around it. Languages that don't put spaces between words run into this often. When enabled, Biome follows the `CommonMark CJK-friendly amendments <https://github.com/tats-u/markdown-cjk-friendly/blob/main/specification.md>`_ and treats such text as bold or italic. The option applies to ``*``, ``_``, and ``~~`` markers. After a variation selector (an invisible character that picks a glyph style for the character before it), Biome classifies a marker by the character before the selector. The option can also change markers that aren't next to Chinese, Japanese, or Korean text, because a marker that can now open or close formatting can take another marker's partner in the same paragraph, heading, or table cell. For example, standard Markdown shows ``**テスト。**テスト a**`` with ``テスト a`` in bold. With the option enabled, ``テスト。`` is bold and the last ``**`` is shown as written. The formatter and the linter both use this reading of the document. Enable the option only when the tool that renders your Markdown also supports these amendments. Otherwise, Biome treats as bold some text that your renderer shows with literal ``**``, and formatting can change what your renderer shows. For example, the option makes ``__`` after a variation selector a bold marker, and the formatter rewrites it as ``**``, which standard Markdown shows as bold even where it showed the original ``__`` as written. Default: false`.
        :param frontmatter: (experimental) Enables parsing frontmatter at the start of the file. Defaults to ``false``. Default: false`.
        :param gfm: (experimental) Enables GitHub Flavored Markdown extensions. Defaults to ``true``. Default: true`.

        :stability: experimental
        :schema: MarkdownParserConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__75b32c24508369083846bdfa68209b976e9a847dc2157991a7a479e27f8f4874)
            check_type(argname="argument cjk_friendly_emphasis", value=cjk_friendly_emphasis, expected_type=type_hints["cjk_friendly_emphasis"])
            check_type(argname="argument frontmatter", value=frontmatter, expected_type=type_hints["frontmatter"])
            check_type(argname="argument gfm", value=gfm, expected_type=type_hints["gfm"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if cjk_friendly_emphasis is not None:
            self._values["cjk_friendly_emphasis"] = cjk_friendly_emphasis
        if frontmatter is not None:
            self._values["frontmatter"] = frontmatter
        if gfm is not None:
            self._values["gfm"] = gfm

    @builtins.property
    def cjk_friendly_emphasis(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Recognizes bold, italic, and strikethrough markers placed directly next to Chinese, Japanese, or Korean text. Defaults to ``false``.

        Standard Markdown doesn't treat ``**テスト。**テスト`` as bold text, because the closing ``**``
        is between a punctuation mark and a letter with no space around it. Languages that don't
        put spaces between words run into this often. When enabled, Biome follows the
        `CommonMark CJK-friendly amendments <https://github.com/tats-u/markdown-cjk-friendly/blob/main/specification.md>`_
        and treats such text as bold or italic. The option applies to ``*``, ``_``, and ``~~`` markers.
        After a variation selector (an invisible character that picks a glyph style for the
        character before it), Biome classifies a marker by the character before the selector.

        The option can also change markers that aren't next to Chinese, Japanese, or Korean text,
        because a marker that can now open or close formatting can take another marker's partner
        in the same paragraph, heading, or table cell. For example, standard Markdown shows
        ``**テスト。**テスト a**`` with ``テスト a`` in bold. With the option enabled, ``テスト。`` is bold
        and the last ``**`` is shown as written.

        The formatter and the linter both use this reading of the document. Enable the option only
        when the tool that renders your Markdown also supports these amendments. Otherwise, Biome
        treats as bold some text that your renderer shows with literal ``**``, and formatting can
        change what your renderer shows. For example, the option makes ``__`` after a variation
        selector a bold marker, and the formatter rewrites it as ``**``, which standard Markdown
        shows as bold even where it showed the original ``__`` as written.

        :default: false`.

        :stability: experimental
        :schema: MarkdownParserConfiguration#cjkFriendlyEmphasis
        '''
        result = self._values.get("cjk_friendly_emphasis")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def frontmatter(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables parsing frontmatter at the start of the file.

        Defaults to ``false``.

        :default: false`.

        :stability: experimental
        :schema: MarkdownParserConfiguration#frontmatter
        '''
        result = self._values.get("frontmatter")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def gfm(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables GitHub Flavored Markdown extensions.

        Defaults to ``true``.

        :default: true`.

        :stability: experimental
        :schema: MarkdownParserConfiguration#gfm
        '''
        result = self._values.get("gfm")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MarkdownParserConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.javascript.biome_config.OperatorLinebreak")
class OperatorLinebreak(enum.Enum):
    '''
    :stability: experimental
    :schema: OperatorLinebreak
    '''

    AFTER = "AFTER"
    '''(experimental) The operator is placed after the expression (after).

    :stability: experimental
    '''
    BEFORE = "BEFORE"
    '''(experimental) The operator is placed before the expression (before).

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
        actions: typing.Optional[typing.Union["Actions", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param actions: (experimental) The assist-action configuration for matched files.
        :param enabled: (experimental) Enables or disables assist actions for matched files.

        :stability: experimental
        :schema: OverrideAssistConfiguration
        '''
        if isinstance(actions, dict):
            actions = Actions(**actions)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__56dc91405fb970d58320a5a0025d8bde646c1421e2210fdd1d1f303623e06ef1)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def actions(self) -> typing.Optional["Actions"]:
        '''(experimental) The assist-action configuration for matched files.

        :stability: experimental
        :schema: OverrideAssistConfiguration#actions
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional["Actions"], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables assist actions for matched files.

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
        :param max_size: (experimental) The maximum source-file size in bytes for matched files.

        :stability: experimental
        :schema: OverrideFilesConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__26fa6398c015df15db0e8378e7692ad89fd6e1addf1ee19d970d8cd2eb5e64f3)
            check_type(argname="argument max_size", value=max_size, expected_type=type_hints["max_size"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if max_size is not None:
            self._values["max_size"] = max_size

    @builtins.property
    def max_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum source-file size in bytes for matched files.

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
        "delimiter_spacing": "delimiterSpacing",
        "enabled": "enabled",
        "expand": "expand",
        "format_with_errors": "formatWithErrors",
        "indent_size": "indentSize",
        "indent_style": "indentStyle",
        "indent_width": "indentWidth",
        "line_ending": "lineEnding",
        "line_width": "lineWidth",
        "trailing_commas": "trailingCommas",
        "trailing_newline": "trailingNewline",
    },
)
class OverrideFormatterConfiguration:
    def __init__(
        self,
        *,
        attribute_position: typing.Optional["AttributePosition"] = None,
        bracket_same_line: typing.Optional[builtins.bool] = None,
        bracket_spacing: typing.Optional[builtins.bool] = None,
        delimiter_spacing: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        expand: typing.Optional["Expand"] = None,
        format_with_errors: typing.Optional[builtins.bool] = None,
        indent_size: typing.Optional[jsii.Number] = None,
        indent_style: typing.Optional["IndentStyle"] = None,
        indent_width: typing.Optional[jsii.Number] = None,
        line_ending: typing.Optional["LineEnding"] = None,
        line_width: typing.Optional[jsii.Number] = None,
        trailing_commas: typing.Optional["JsTrailingCommas"] = None,
        trailing_newline: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param attribute_position: (experimental) The attribute position style in HTML-like languages.
        :param bracket_same_line: (experimental) Controls the placement of the closing bracket for multiline HTML and JSX opening tags. Biome places the bracket at the end of the last attribute line when enabled and on its own line when disabled. This also affects self-closing HTML elements, but self-closing JSX elements are unaffected.
        :param bracket_spacing: (experimental) Controls spaces inside braces in supported single-line structures. The affected structures vary by language.
        :param delimiter_spacing: (experimental) Controls spaces immediately inside supported delimiters when their content fits on one line. It doesn't add spaces before opening delimiters or inside empty delimiters. The affected delimiters vary by language. If unset, uses the configured formatter setting.
        :param enabled: (experimental) Enables or disables the formatter for matched files.
        :param expand: (experimental) Controls whether arrays and objects are formatted on one line or multiple lines. ``auto`` formats objects on multiple lines if the first property has a newline, and arrays on one line if they fit. ``always`` formats arrays and objects on multiple lines. ``never`` formats arrays and objects on one line if they fit. If unset, uses the configured formatter setting. When formatting ``package.json``, Biome uses ``always`` unless configured otherwise.
        :param format_with_errors: (experimental) Allows formatting matched files that contain syntax errors.
        :param indent_size: (experimental) The indentation width. Deprecated, use ``indentWidth`` instead.
        :param indent_style: (experimental) Uses tabs or spaces for indentation.
        :param indent_width: (experimental) Sets the indentation width. With space indentation, this is the number of spaces emitted per indentation level. With tab indentation, Biome emits one tab per level and uses this value as the tab's display width when calculating line length. Accepted values are ``0`` through ``24``.
        :param line_ending: (experimental) The line ending.
        :param line_width: (experimental) Sets the preferred maximum line width used when deciding where to wrap code. Some content, such as long unbreakable strings, may still exceed this width. Accepted values are ``1`` through ``320``.
        :param trailing_commas: (experimental) Prints trailing commas wherever possible in multiline comma-separated structures. This is a legacy override option. Prefer ``javascript.formatter.trailingCommas``.
        :param trailing_newline: (experimental) Whether to add a trailing newline at the end of matched files. Disabling this option can cause compatibility problems with other tools.

        :stability: experimental
        :schema: OverrideFormatterConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__3602eb22e2d33d64a65f4ebb15f534391f93d1e72546965c7be88c0c1e391655)
            check_type(argname="argument attribute_position", value=attribute_position, expected_type=type_hints["attribute_position"])
            check_type(argname="argument bracket_same_line", value=bracket_same_line, expected_type=type_hints["bracket_same_line"])
            check_type(argname="argument bracket_spacing", value=bracket_spacing, expected_type=type_hints["bracket_spacing"])
            check_type(argname="argument delimiter_spacing", value=delimiter_spacing, expected_type=type_hints["delimiter_spacing"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument expand", value=expand, expected_type=type_hints["expand"])
            check_type(argname="argument format_with_errors", value=format_with_errors, expected_type=type_hints["format_with_errors"])
            check_type(argname="argument indent_size", value=indent_size, expected_type=type_hints["indent_size"])
            check_type(argname="argument indent_style", value=indent_style, expected_type=type_hints["indent_style"])
            check_type(argname="argument indent_width", value=indent_width, expected_type=type_hints["indent_width"])
            check_type(argname="argument line_ending", value=line_ending, expected_type=type_hints["line_ending"])
            check_type(argname="argument line_width", value=line_width, expected_type=type_hints["line_width"])
            check_type(argname="argument trailing_commas", value=trailing_commas, expected_type=type_hints["trailing_commas"])
            check_type(argname="argument trailing_newline", value=trailing_newline, expected_type=type_hints["trailing_newline"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attribute_position is not None:
            self._values["attribute_position"] = attribute_position
        if bracket_same_line is not None:
            self._values["bracket_same_line"] = bracket_same_line
        if bracket_spacing is not None:
            self._values["bracket_spacing"] = bracket_spacing
        if delimiter_spacing is not None:
            self._values["delimiter_spacing"] = delimiter_spacing
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
        if trailing_commas is not None:
            self._values["trailing_commas"] = trailing_commas
        if trailing_newline is not None:
            self._values["trailing_newline"] = trailing_newline

    @builtins.property
    def attribute_position(self) -> typing.Optional["AttributePosition"]:
        '''(experimental) The attribute position style in HTML-like languages.

        :stability: experimental
        :schema: OverrideFormatterConfiguration#attributePosition
        '''
        result = self._values.get("attribute_position")
        return typing.cast(typing.Optional["AttributePosition"], result)

    @builtins.property
    def bracket_same_line(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Controls the placement of the closing bracket for multiline HTML and JSX opening tags.

        Biome
        places the bracket at the end of the last attribute line when enabled and on its own line when
        disabled. This also affects self-closing HTML elements, but self-closing JSX elements are
        unaffected.

        :stability: experimental
        :schema: OverrideFormatterConfiguration#bracketSameLine
        '''
        result = self._values.get("bracket_same_line")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def bracket_spacing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Controls spaces inside braces in supported single-line structures.

        The affected structures
        vary by language.

        :stability: experimental
        :schema: OverrideFormatterConfiguration#bracketSpacing
        '''
        result = self._values.get("bracket_spacing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def delimiter_spacing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Controls spaces immediately inside supported delimiters when their content fits on one line.

        It doesn't add spaces before opening delimiters or inside empty delimiters.

        The affected delimiters vary by language. If unset, uses the configured formatter setting.

        :stability: experimental
        :schema: OverrideFormatterConfiguration#delimiterSpacing
        '''
        result = self._values.get("delimiter_spacing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables the formatter for matched files.

        :stability: experimental
        :schema: OverrideFormatterConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def expand(self) -> typing.Optional["Expand"]:
        '''(experimental) Controls whether arrays and objects are formatted on one line or multiple lines.

        ``auto`` formats objects on multiple lines if the first property has a newline, and arrays on
        one line if they fit.

        ``always`` formats arrays and objects on multiple lines.

        ``never`` formats arrays and objects on one line if they fit.

        If unset, uses the configured formatter setting.

        When formatting ``package.json``, Biome uses ``always`` unless configured otherwise.

        :stability: experimental
        :schema: OverrideFormatterConfiguration#expand
        '''
        result = self._values.get("expand")
        return typing.cast(typing.Optional["Expand"], result)

    @builtins.property
    def format_with_errors(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Allows formatting matched files that contain syntax errors.

        :stability: experimental
        :schema: OverrideFormatterConfiguration#formatWithErrors
        '''
        result = self._values.get("format_with_errors")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def indent_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The indentation width.

        Deprecated, use ``indentWidth`` instead.

        :stability: experimental
        :schema: OverrideFormatterConfiguration#indentSize
        '''
        result = self._values.get("indent_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def indent_style(self) -> typing.Optional["IndentStyle"]:
        '''(experimental) Uses tabs or spaces for indentation.

        :stability: experimental
        :schema: OverrideFormatterConfiguration#indentStyle
        '''
        result = self._values.get("indent_style")
        return typing.cast(typing.Optional["IndentStyle"], result)

    @builtins.property
    def indent_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Sets the indentation width.

        With space indentation, this is the number of spaces emitted per
        indentation level. With tab indentation, Biome emits one tab per level and uses this value as
        the tab's display width when calculating line length. Accepted values are ``0`` through ``24``.

        :stability: experimental
        :schema: OverrideFormatterConfiguration#indentWidth
        '''
        result = self._values.get("indent_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def line_ending(self) -> typing.Optional["LineEnding"]:
        '''(experimental) The line ending.

        :stability: experimental
        :schema: OverrideFormatterConfiguration#lineEnding
        '''
        result = self._values.get("line_ending")
        return typing.cast(typing.Optional["LineEnding"], result)

    @builtins.property
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Sets the preferred maximum line width used when deciding where to wrap code.

        Some content,
        such as long unbreakable strings, may still exceed this width. Accepted values are ``1`` through
        ``320``.

        :stability: experimental
        :schema: OverrideFormatterConfiguration#lineWidth
        '''
        result = self._values.get("line_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def trailing_commas(self) -> typing.Optional["JsTrailingCommas"]:
        '''(experimental) Prints trailing commas wherever possible in multiline comma-separated structures.

        This is a
        legacy override option. Prefer ``javascript.formatter.trailingCommas``.

        :stability: experimental
        :schema: OverrideFormatterConfiguration#trailingCommas
        '''
        result = self._values.get("trailing_commas")
        return typing.cast(typing.Optional["JsTrailingCommas"], result)

    @builtins.property
    def trailing_newline(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to add a trailing newline at the end of matched files.

        Disabling this option can
        cause compatibility problems with other tools.

        :stability: experimental
        :schema: OverrideFormatterConfiguration#trailingNewline
        '''
        result = self._values.get("trailing_newline")
        return typing.cast(typing.Optional[builtins.bool], result)

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
        domains: typing.Optional[typing.Union["RuleDomains", typing.Dict[builtins.str, typing.Any]]] = None,
        enabled: typing.Optional[builtins.bool] = None,
        rules: typing.Optional[typing.Union["Rules", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param domains: (experimental) The lint-domain configuration for matched files.
        :param enabled: (experimental) Enables or disables the linter for matched files.
        :param rules: (experimental) The lint-rule configuration for matched files.

        :stability: experimental
        :schema: OverrideLinterConfiguration
        '''
        if isinstance(domains, dict):
            domains = RuleDomains(**domains)
        if isinstance(rules, dict):
            rules = Rules(**rules)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__4b923acd3721838353ddf97d9a992327d3607a622afc36e911bc3eb842adb709)
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
    def domains(self) -> typing.Optional["RuleDomains"]:
        '''(experimental) The lint-domain configuration for matched files.

        :stability: experimental
        :schema: OverrideLinterConfiguration#domains
        '''
        result = self._values.get("domains")
        return typing.cast(typing.Optional["RuleDomains"], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables the linter for matched files.

        :stability: experimental
        :schema: OverrideLinterConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def rules(self) -> typing.Optional["Rules"]:
        '''(experimental) The lint-rule configuration for matched files.

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
        "markdown": "markdown",
        "plugins": "plugins",
        "yaml": "yaml",
    },
)
class OverridePattern:
    def __init__(
        self,
        *,
        assist: typing.Optional[typing.Union["OverrideAssistConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        css: typing.Optional[typing.Union["CssConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        files: typing.Optional[typing.Union["OverrideFilesConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        formatter: typing.Optional[typing.Union["OverrideFormatterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        graphql: typing.Optional[typing.Union["GraphqlConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        grit: typing.Optional[typing.Union["GritConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        html: typing.Optional[typing.Union["HtmlConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        includes: typing.Optional[typing.Sequence[builtins.str]] = None,
        javascript: typing.Optional[typing.Union["JsConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        json: typing.Optional[typing.Union["JsonConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        linter: typing.Optional[typing.Union["OverrideLinterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        markdown: typing.Optional[typing.Union["MarkdownConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        plugins: typing.Optional[typing.Sequence[typing.Any]] = None,
        yaml: typing.Optional[typing.Union["YamlConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param assist: (experimental) Assist settings for matched files.
        :param css: (experimental) CSS-specific settings for matched files.
        :param files: (experimental) File-handling settings for matched files.
        :param formatter: (experimental) Formatter settings for matched files.
        :param graphql: (experimental) GraphQL-specific settings for matched files.
        :param grit: (experimental) GritQL-specific settings for matched files.
        :param html: (experimental) HTML-specific settings for matched files.
        :param includes: (experimental) A list of glob patterns selecting the files to which this override applies. If omitted, the override applies to every file. An empty list applies to no files.
        :param javascript: (experimental) JavaScript-specific settings for matched files.
        :param json: (experimental) JSON-specific settings for matched files.
        :param linter: (experimental) Linter settings for matched files.
        :param markdown: (experimental) Specific configuration for the Markdown language.
        :param plugins: (experimental) Additional plugins for matched files.
        :param yaml: (experimental) Specific configuration for the YAML language.

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
        if isinstance(markdown, dict):
            markdown = MarkdownConfiguration(**markdown)
        if isinstance(yaml, dict):
            yaml = YamlConfiguration(**yaml)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__15d4ec259e2481f14109da78900e918d2d10bde9b57b737b5c0ac7d4d415d889)
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
            check_type(argname="argument markdown", value=markdown, expected_type=type_hints["markdown"])
            check_type(argname="argument plugins", value=plugins, expected_type=type_hints["plugins"])
            check_type(argname="argument yaml", value=yaml, expected_type=type_hints["yaml"])
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
        if markdown is not None:
            self._values["markdown"] = markdown
        if plugins is not None:
            self._values["plugins"] = plugins
        if yaml is not None:
            self._values["yaml"] = yaml

    @builtins.property
    def assist(self) -> typing.Optional["OverrideAssistConfiguration"]:
        '''(experimental) Assist settings for matched files.

        :stability: experimental
        :schema: OverridePattern#assist
        '''
        result = self._values.get("assist")
        return typing.cast(typing.Optional["OverrideAssistConfiguration"], result)

    @builtins.property
    def css(self) -> typing.Optional["CssConfiguration"]:
        '''(experimental) CSS-specific settings for matched files.

        :stability: experimental
        :schema: OverridePattern#css
        '''
        result = self._values.get("css")
        return typing.cast(typing.Optional["CssConfiguration"], result)

    @builtins.property
    def files(self) -> typing.Optional["OverrideFilesConfiguration"]:
        '''(experimental) File-handling settings for matched files.

        :stability: experimental
        :schema: OverridePattern#files
        '''
        result = self._values.get("files")
        return typing.cast(typing.Optional["OverrideFilesConfiguration"], result)

    @builtins.property
    def formatter(self) -> typing.Optional["OverrideFormatterConfiguration"]:
        '''(experimental) Formatter settings for matched files.

        :stability: experimental
        :schema: OverridePattern#formatter
        '''
        result = self._values.get("formatter")
        return typing.cast(typing.Optional["OverrideFormatterConfiguration"], result)

    @builtins.property
    def graphql(self) -> typing.Optional["GraphqlConfiguration"]:
        '''(experimental) GraphQL-specific settings for matched files.

        :stability: experimental
        :schema: OverridePattern#graphql
        '''
        result = self._values.get("graphql")
        return typing.cast(typing.Optional["GraphqlConfiguration"], result)

    @builtins.property
    def grit(self) -> typing.Optional["GritConfiguration"]:
        '''(experimental) GritQL-specific settings for matched files.

        :stability: experimental
        :schema: OverridePattern#grit
        '''
        result = self._values.get("grit")
        return typing.cast(typing.Optional["GritConfiguration"], result)

    @builtins.property
    def html(self) -> typing.Optional["HtmlConfiguration"]:
        '''(experimental) HTML-specific settings for matched files.

        :stability: experimental
        :schema: OverridePattern#html
        '''
        result = self._values.get("html")
        return typing.cast(typing.Optional["HtmlConfiguration"], result)

    @builtins.property
    def includes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of glob patterns selecting the files to which this override applies.

        If omitted, the
        override applies to every file. An empty list applies to no files.

        :stability: experimental
        :schema: OverridePattern#includes
        '''
        result = self._values.get("includes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def javascript(self) -> typing.Optional["JsConfiguration"]:
        '''(experimental) JavaScript-specific settings for matched files.

        :stability: experimental
        :schema: OverridePattern#javascript
        '''
        result = self._values.get("javascript")
        return typing.cast(typing.Optional["JsConfiguration"], result)

    @builtins.property
    def json(self) -> typing.Optional["JsonConfiguration"]:
        '''(experimental) JSON-specific settings for matched files.

        :stability: experimental
        :schema: OverridePattern#json
        '''
        result = self._values.get("json")
        return typing.cast(typing.Optional["JsonConfiguration"], result)

    @builtins.property
    def linter(self) -> typing.Optional["OverrideLinterConfiguration"]:
        '''(experimental) Linter settings for matched files.

        :stability: experimental
        :schema: OverridePattern#linter
        '''
        result = self._values.get("linter")
        return typing.cast(typing.Optional["OverrideLinterConfiguration"], result)

    @builtins.property
    def markdown(self) -> typing.Optional["MarkdownConfiguration"]:
        '''(experimental) Specific configuration for the Markdown language.

        :stability: experimental
        :schema: OverridePattern#markdown
        '''
        result = self._values.get("markdown")
        return typing.cast(typing.Optional["MarkdownConfiguration"], result)

    @builtins.property
    def plugins(self) -> typing.Optional[typing.List[typing.Any]]:
        '''(experimental) Additional plugins for matched files.

        :stability: experimental
        :schema: OverridePattern#plugins
        '''
        result = self._values.get("plugins")
        return typing.cast(typing.Optional[typing.List[typing.Any]], result)

    @builtins.property
    def yaml(self) -> typing.Optional["YamlConfiguration"]:
        '''(experimental) Specific configuration for the YAML language.

        :stability: experimental
        :schema: OverridePattern#yaml
        '''
        result = self._values.get("yaml")
        return typing.cast(typing.Optional["YamlConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OverridePattern(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.javascript.biome_config.PresetConfig")
class PresetConfig(enum.Enum):
    '''(experimental) A preset configuration for enabling a set of rules.

    :stability: experimental
    :schema: PresetConfig
    '''

    RECOMMENDED = "RECOMMENDED"
    '''(experimental) recommended.

    :stability: experimental
    '''
    ALL = "ALL"
    '''(experimental) all.

    :stability: experimental
    '''
    NONE = "NONE"
    '''(experimental) none.

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.javascript.biome_config.ProseWrap")
class ProseWrap(enum.Enum):
    '''(experimental) Controls whether Biome keeps, adds, or removes line breaks in Markdown paragraphs.

    Manual line breaks are always kept. In Markdown, a manual line break is created by ending a
    line with two spaces or a backslash.

    :stability: experimental
    :schema: ProseWrap
    '''

    PRESERVE = "PRESERVE"
    '''(experimental) Keep line breaks as written in the source file.

    This is the default. (preserve)

    :stability: experimental
    '''
    ALWAYS = "ALWAYS"
    '''(experimental) Wrap paragraphs to fit the configured ``lineWidth``.

    (always)

    :stability: experimental
    '''
    NEVER = "NEVER"
    '''(experimental) Remove line breaks from paragraphs so that each paragraph is on one line.

    (never)

    :stability: experimental
    '''


@jsii.enum(jsii_type="projen.javascript.biome_config.QuoteProperties")
class QuoteProperties(enum.Enum):
    '''
    :stability: experimental
    :schema: QuoteProperties
    '''

    AS_NEEDED = "AS_NEEDED"
    '''(experimental) Removes quotes when the property name is valid without them.

    (asNeeded)

    :stability: experimental
    '''
    PRESERVE = "PRESERVE"
    '''(experimental) Preserves quotes around property names that were quoted in the input.

    (preserve)

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
    '''(experimental) Enables all rules in the domain.

    (all)

    :stability: experimental
    '''
    NONE = "NONE"
    '''(experimental) Disables the domain.

    (none)

    :stability: experimental
    '''
    RECOMMENDED = "RECOMMENDED"
    '''(experimental) Enables the domain's recommended non-nursery rules.

    (recommended)

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.RuleDomains",
    jsii_struct_bases=[],
    name_mapping={
        "astro": "astro",
        "drizzle": "drizzle",
        "next": "next",
        "playwright": "playwright",
        "project": "project",
        "qwik": "qwik",
        "react": "react",
        "react_native": "reactNative",
        "solid": "solid",
        "svelte": "svelte",
        "tailwind": "tailwind",
        "test": "test",
        "turborepo": "turborepo",
        "types": "types",
        "vue": "vue",
    },
)
class RuleDomains:
    def __init__(
        self,
        *,
        astro: typing.Optional["RuleDomainValue"] = None,
        drizzle: typing.Optional["RuleDomainValue"] = None,
        next: typing.Optional["RuleDomainValue"] = None,
        playwright: typing.Optional["RuleDomainValue"] = None,
        project: typing.Optional["RuleDomainValue"] = None,
        qwik: typing.Optional["RuleDomainValue"] = None,
        react: typing.Optional["RuleDomainValue"] = None,
        react_native: typing.Optional["RuleDomainValue"] = None,
        solid: typing.Optional["RuleDomainValue"] = None,
        svelte: typing.Optional["RuleDomainValue"] = None,
        tailwind: typing.Optional["RuleDomainValue"] = None,
        test: typing.Optional["RuleDomainValue"] = None,
        turborepo: typing.Optional["RuleDomainValue"] = None,
        types: typing.Optional["RuleDomainValue"] = None,
        vue: typing.Optional["RuleDomainValue"] = None,
    ) -> None:
        '''
        :param astro: 
        :param drizzle: 
        :param next: 
        :param playwright: 
        :param project: 
        :param qwik: 
        :param react: 
        :param react_native: 
        :param solid: 
        :param svelte: 
        :param tailwind: 
        :param test: 
        :param turborepo: 
        :param types: 
        :param vue: 

        :stability: experimental
        :schema: RuleDomains
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d48381bffa9c2b0ef8e9116898fdc56e984cd30d1a51b6e379dc5c999a8b5336)
            check_type(argname="argument astro", value=astro, expected_type=type_hints["astro"])
            check_type(argname="argument drizzle", value=drizzle, expected_type=type_hints["drizzle"])
            check_type(argname="argument next", value=next, expected_type=type_hints["next"])
            check_type(argname="argument playwright", value=playwright, expected_type=type_hints["playwright"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument qwik", value=qwik, expected_type=type_hints["qwik"])
            check_type(argname="argument react", value=react, expected_type=type_hints["react"])
            check_type(argname="argument react_native", value=react_native, expected_type=type_hints["react_native"])
            check_type(argname="argument solid", value=solid, expected_type=type_hints["solid"])
            check_type(argname="argument svelte", value=svelte, expected_type=type_hints["svelte"])
            check_type(argname="argument tailwind", value=tailwind, expected_type=type_hints["tailwind"])
            check_type(argname="argument test", value=test, expected_type=type_hints["test"])
            check_type(argname="argument turborepo", value=turborepo, expected_type=type_hints["turborepo"])
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
            check_type(argname="argument vue", value=vue, expected_type=type_hints["vue"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if astro is not None:
            self._values["astro"] = astro
        if drizzle is not None:
            self._values["drizzle"] = drizzle
        if next is not None:
            self._values["next"] = next
        if playwright is not None:
            self._values["playwright"] = playwright
        if project is not None:
            self._values["project"] = project
        if qwik is not None:
            self._values["qwik"] = qwik
        if react is not None:
            self._values["react"] = react
        if react_native is not None:
            self._values["react_native"] = react_native
        if solid is not None:
            self._values["solid"] = solid
        if svelte is not None:
            self._values["svelte"] = svelte
        if tailwind is not None:
            self._values["tailwind"] = tailwind
        if test is not None:
            self._values["test"] = test
        if turborepo is not None:
            self._values["turborepo"] = turborepo
        if types is not None:
            self._values["types"] = types
        if vue is not None:
            self._values["vue"] = vue

    @builtins.property
    def astro(self) -> typing.Optional["RuleDomainValue"]:
        '''
        :stability: experimental
        :schema: RuleDomains#astro
        '''
        result = self._values.get("astro")
        return typing.cast(typing.Optional["RuleDomainValue"], result)

    @builtins.property
    def drizzle(self) -> typing.Optional["RuleDomainValue"]:
        '''
        :stability: experimental
        :schema: RuleDomains#drizzle
        '''
        result = self._values.get("drizzle")
        return typing.cast(typing.Optional["RuleDomainValue"], result)

    @builtins.property
    def next(self) -> typing.Optional["RuleDomainValue"]:
        '''
        :stability: experimental
        :schema: RuleDomains#next
        '''
        result = self._values.get("next")
        return typing.cast(typing.Optional["RuleDomainValue"], result)

    @builtins.property
    def playwright(self) -> typing.Optional["RuleDomainValue"]:
        '''
        :stability: experimental
        :schema: RuleDomains#playwright
        '''
        result = self._values.get("playwright")
        return typing.cast(typing.Optional["RuleDomainValue"], result)

    @builtins.property
    def project(self) -> typing.Optional["RuleDomainValue"]:
        '''
        :stability: experimental
        :schema: RuleDomains#project
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional["RuleDomainValue"], result)

    @builtins.property
    def qwik(self) -> typing.Optional["RuleDomainValue"]:
        '''
        :stability: experimental
        :schema: RuleDomains#qwik
        '''
        result = self._values.get("qwik")
        return typing.cast(typing.Optional["RuleDomainValue"], result)

    @builtins.property
    def react(self) -> typing.Optional["RuleDomainValue"]:
        '''
        :stability: experimental
        :schema: RuleDomains#react
        '''
        result = self._values.get("react")
        return typing.cast(typing.Optional["RuleDomainValue"], result)

    @builtins.property
    def react_native(self) -> typing.Optional["RuleDomainValue"]:
        '''
        :stability: experimental
        :schema: RuleDomains#reactNative
        '''
        result = self._values.get("react_native")
        return typing.cast(typing.Optional["RuleDomainValue"], result)

    @builtins.property
    def solid(self) -> typing.Optional["RuleDomainValue"]:
        '''
        :stability: experimental
        :schema: RuleDomains#solid
        '''
        result = self._values.get("solid")
        return typing.cast(typing.Optional["RuleDomainValue"], result)

    @builtins.property
    def svelte(self) -> typing.Optional["RuleDomainValue"]:
        '''
        :stability: experimental
        :schema: RuleDomains#svelte
        '''
        result = self._values.get("svelte")
        return typing.cast(typing.Optional["RuleDomainValue"], result)

    @builtins.property
    def tailwind(self) -> typing.Optional["RuleDomainValue"]:
        '''
        :stability: experimental
        :schema: RuleDomains#tailwind
        '''
        result = self._values.get("tailwind")
        return typing.cast(typing.Optional["RuleDomainValue"], result)

    @builtins.property
    def test(self) -> typing.Optional["RuleDomainValue"]:
        '''
        :stability: experimental
        :schema: RuleDomains#test
        '''
        result = self._values.get("test")
        return typing.cast(typing.Optional["RuleDomainValue"], result)

    @builtins.property
    def turborepo(self) -> typing.Optional["RuleDomainValue"]:
        '''
        :stability: experimental
        :schema: RuleDomains#turborepo
        '''
        result = self._values.get("turborepo")
        return typing.cast(typing.Optional["RuleDomainValue"], result)

    @builtins.property
    def types(self) -> typing.Optional["RuleDomainValue"]:
        '''
        :stability: experimental
        :schema: RuleDomains#types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional["RuleDomainValue"], result)

    @builtins.property
    def vue(self) -> typing.Optional["RuleDomainValue"]:
        '''
        :stability: experimental
        :schema: RuleDomains#vue
        '''
        result = self._values.get("vue")
        return typing.cast(typing.Optional["RuleDomainValue"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RuleDomains(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.Rules",
    jsii_struct_bases=[],
    name_mapping={
        "a11_y": "a11Y",
        "complexity": "complexity",
        "correctness": "correctness",
        "nursery": "nursery",
        "performance": "performance",
        "preset": "preset",
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
        preset: typing.Optional["PresetConfig"] = None,
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
        :param preset: (experimental) Selects the baseline set of lint rules. ``recommended`` enables Biome's recommended non-nursery rules, ``all`` enables all non-nursery rules, and ``none`` starts with no rules enabled. Group-level settings and explicit rule settings override this preset. Defaults to ``recommended``. Default: recommended`.
        :param recommended: (experimental) Enables or disables Biome's recommended non-nursery rules. Defaults to ``true``. **Deprecated:** This option will be removed in the next major version. Use ``linter.rules.preset`` instead, or run ``biome migrate`` to update the configuration. Default: true`.
        :param security: 
        :param style: 
        :param suspicious: 

        :stability: experimental
        :schema: Rules
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d509a5cc6f981426e8c0771a7bcfe4b66092b008a57a49a58a2d172ec95c48bd)
            check_type(argname="argument a11_y", value=a11_y, expected_type=type_hints["a11_y"])
            check_type(argname="argument complexity", value=complexity, expected_type=type_hints["complexity"])
            check_type(argname="argument correctness", value=correctness, expected_type=type_hints["correctness"])
            check_type(argname="argument nursery", value=nursery, expected_type=type_hints["nursery"])
            check_type(argname="argument performance", value=performance, expected_type=type_hints["performance"])
            check_type(argname="argument preset", value=preset, expected_type=type_hints["preset"])
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
        if preset is not None:
            self._values["preset"] = preset
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
    def preset(self) -> typing.Optional["PresetConfig"]:
        '''(experimental) Selects the baseline set of lint rules.

        ``recommended`` enables Biome's recommended
        non-nursery rules, ``all`` enables all non-nursery rules, and ``none`` starts with no
        rules enabled. Group-level settings and explicit rule settings override this
        preset. Defaults to ``recommended``.

        :default: recommended`.

        :stability: experimental
        :schema: Rules#preset
        '''
        result = self._values.get("preset")
        return typing.cast(typing.Optional["PresetConfig"], result)

    @builtins.property
    def recommended(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables Biome's recommended non-nursery rules. Defaults to ``true``.

        **Deprecated:** This option will be removed in the next major version. Use
        ``linter.rules.preset`` instead, or run ``biome migrate`` to update the configuration.

        :default: true`.

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
    '''(experimental) Controls whether HTML void elements such as ``<img>`` and ``<input>`` include a slash before ``>``.

    :stability: experimental
    :schema: SelfCloseVoidElements
    '''

    NEVER = "NEVER"
    '''(experimental) Removes the slash, for example ``<img src="image.png">``. (never).

    :stability: experimental
    '''
    ALWAYS = "ALWAYS"
    '''(experimental) Adds the slash, for example ``<img src="image.png" />``. (always).

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
        "no_duplicate_classes": "noDuplicateClasses",
        "organize_imports": "organizeImports",
        "preset": "preset",
        "recommended": "recommended",
        "use_graphql_sorted_arguments": "useGraphqlSortedArguments",
        "use_graphql_sorted_definitions": "useGraphqlSortedDefinitions",
        "use_graphql_sorted_variables": "useGraphqlSortedVariables",
        "use_sorted_attributes": "useSortedAttributes",
        "use_sorted_enum_members": "useSortedEnumMembers",
        "use_sorted_interface_members": "useSortedInterfaceMembers",
        "use_sorted_keys": "useSortedKeys",
        "use_sorted_package_json": "useSortedPackageJson",
        "use_sorted_properties": "useSortedProperties",
        "use_sorted_selection_set": "useSortedSelectionSet",
        "use_sorted_type_fields": "useSortedTypeFields",
    },
)
class Source:
    def __init__(
        self,
        *,
        no_duplicate_classes: typing.Any = None,
        organize_imports: typing.Any = None,
        preset: typing.Optional["PresetConfig"] = None,
        recommended: typing.Optional[builtins.bool] = None,
        use_graphql_sorted_arguments: typing.Any = None,
        use_graphql_sorted_definitions: typing.Any = None,
        use_graphql_sorted_variables: typing.Any = None,
        use_sorted_attributes: typing.Any = None,
        use_sorted_enum_members: typing.Any = None,
        use_sorted_interface_members: typing.Any = None,
        use_sorted_keys: typing.Any = None,
        use_sorted_package_json: typing.Any = None,
        use_sorted_properties: typing.Any = None,
        use_sorted_selection_set: typing.Any = None,
        use_sorted_type_fields: typing.Any = None,
    ) -> None:
        '''(experimental) Configures one group of assist actions.

        :param no_duplicate_classes: (experimental) Remove repeated CSS class names from HTML class attributes. See https://biomejs.dev/assist/actions/no-duplicate-classes
        :param organize_imports: (experimental) Organize imports and exports in JavaScript and TypeScript files. See https://biomejs.dev/assist/actions/organize-imports
        :param preset: (experimental) Selects the baseline set of assist actions for this group. ``recommended`` enables the group's recommended actions, ``all`` enables all actions in the group, and ``none`` starts with no actions enabled in the group. Explicit action settings override this group preset, which overrides ``assist.actions.preset`` for the group.
        :param recommended: (experimental) Enables or disables the recommended actions in this group. The group's ``preset`` setting takes precedence when both options are set.
        :param use_graphql_sorted_arguments: (experimental) Sort the arguments of GraphQL fields and directives in natural order. See https://biomejs.dev/assist/actions/use-graphql-sorted-arguments
        :param use_graphql_sorted_definitions: (experimental) Sort the named definitions in a GraphQL document. See https://biomejs.dev/assist/actions/use-graphql-sorted-definitions
        :param use_graphql_sorted_variables: (experimental) Sort the variable definitions of GraphQL operations in natural order. See https://biomejs.dev/assist/actions/use-graphql-sorted-variables
        :param use_sorted_attributes: (experimental) Sort HTML attributes and framework directives into a consistent order. See https://biomejs.dev/assist/actions/use-sorted-attributes
        :param use_sorted_enum_members: (experimental) Sort GraphQL enum values in natural order. See https://biomejs.dev/assist/actions/use-sorted-enum-members
        :param use_sorted_interface_members: (experimental) Sort named members of a TypeScript interface. See https://biomejs.dev/assist/actions/use-sorted-interface-members
        :param use_sorted_keys: (experimental) Sort keys in a JSON object. See https://biomejs.dev/assist/actions/use-sorted-keys
        :param use_sorted_package_json: (experimental) Organize package.json fields according to established conventions. See https://biomejs.dev/assist/actions/use-sorted-package-json.
        :param use_sorted_properties: (experimental) Sort CSS properties and nested rules into a consistent order. See https://biomejs.dev/assist/actions/use-sorted-properties
        :param use_sorted_selection_set: (experimental) Sort selections inside GraphQL operations and fragments. See https://biomejs.dev/assist/actions/use-sorted-selection-set
        :param use_sorted_type_fields: (experimental) Sort fields in GraphQL type definitions by name. See https://biomejs.dev/assist/actions/use-sorted-type-fields

        :stability: experimental
        :schema: Source
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f128bc69ea32431a28e9aae09b49905087cb9f2c49176cf906cbd06f3c7237b7)
            check_type(argname="argument no_duplicate_classes", value=no_duplicate_classes, expected_type=type_hints["no_duplicate_classes"])
            check_type(argname="argument organize_imports", value=organize_imports, expected_type=type_hints["organize_imports"])
            check_type(argname="argument preset", value=preset, expected_type=type_hints["preset"])
            check_type(argname="argument recommended", value=recommended, expected_type=type_hints["recommended"])
            check_type(argname="argument use_graphql_sorted_arguments", value=use_graphql_sorted_arguments, expected_type=type_hints["use_graphql_sorted_arguments"])
            check_type(argname="argument use_graphql_sorted_definitions", value=use_graphql_sorted_definitions, expected_type=type_hints["use_graphql_sorted_definitions"])
            check_type(argname="argument use_graphql_sorted_variables", value=use_graphql_sorted_variables, expected_type=type_hints["use_graphql_sorted_variables"])
            check_type(argname="argument use_sorted_attributes", value=use_sorted_attributes, expected_type=type_hints["use_sorted_attributes"])
            check_type(argname="argument use_sorted_enum_members", value=use_sorted_enum_members, expected_type=type_hints["use_sorted_enum_members"])
            check_type(argname="argument use_sorted_interface_members", value=use_sorted_interface_members, expected_type=type_hints["use_sorted_interface_members"])
            check_type(argname="argument use_sorted_keys", value=use_sorted_keys, expected_type=type_hints["use_sorted_keys"])
            check_type(argname="argument use_sorted_package_json", value=use_sorted_package_json, expected_type=type_hints["use_sorted_package_json"])
            check_type(argname="argument use_sorted_properties", value=use_sorted_properties, expected_type=type_hints["use_sorted_properties"])
            check_type(argname="argument use_sorted_selection_set", value=use_sorted_selection_set, expected_type=type_hints["use_sorted_selection_set"])
            check_type(argname="argument use_sorted_type_fields", value=use_sorted_type_fields, expected_type=type_hints["use_sorted_type_fields"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if no_duplicate_classes is not None:
            self._values["no_duplicate_classes"] = no_duplicate_classes
        if organize_imports is not None:
            self._values["organize_imports"] = organize_imports
        if preset is not None:
            self._values["preset"] = preset
        if recommended is not None:
            self._values["recommended"] = recommended
        if use_graphql_sorted_arguments is not None:
            self._values["use_graphql_sorted_arguments"] = use_graphql_sorted_arguments
        if use_graphql_sorted_definitions is not None:
            self._values["use_graphql_sorted_definitions"] = use_graphql_sorted_definitions
        if use_graphql_sorted_variables is not None:
            self._values["use_graphql_sorted_variables"] = use_graphql_sorted_variables
        if use_sorted_attributes is not None:
            self._values["use_sorted_attributes"] = use_sorted_attributes
        if use_sorted_enum_members is not None:
            self._values["use_sorted_enum_members"] = use_sorted_enum_members
        if use_sorted_interface_members is not None:
            self._values["use_sorted_interface_members"] = use_sorted_interface_members
        if use_sorted_keys is not None:
            self._values["use_sorted_keys"] = use_sorted_keys
        if use_sorted_package_json is not None:
            self._values["use_sorted_package_json"] = use_sorted_package_json
        if use_sorted_properties is not None:
            self._values["use_sorted_properties"] = use_sorted_properties
        if use_sorted_selection_set is not None:
            self._values["use_sorted_selection_set"] = use_sorted_selection_set
        if use_sorted_type_fields is not None:
            self._values["use_sorted_type_fields"] = use_sorted_type_fields

    @builtins.property
    def no_duplicate_classes(self) -> typing.Any:
        '''(experimental) Remove repeated CSS class names from HTML class attributes.

        See https://biomejs.dev/assist/actions/no-duplicate-classes

        :stability: experimental
        :schema: Source#noDuplicateClasses
        '''
        result = self._values.get("no_duplicate_classes")
        return typing.cast(typing.Any, result)

    @builtins.property
    def organize_imports(self) -> typing.Any:
        '''(experimental) Organize imports and exports in JavaScript and TypeScript files.

        See https://biomejs.dev/assist/actions/organize-imports

        :stability: experimental
        :schema: Source#organizeImports
        '''
        result = self._values.get("organize_imports")
        return typing.cast(typing.Any, result)

    @builtins.property
    def preset(self) -> typing.Optional["PresetConfig"]:
        '''(experimental) Selects the baseline set of assist actions for this group.

        ``recommended`` enables
        the group's recommended actions, ``all`` enables all actions in the group, and
        ``none`` starts with no actions enabled in the group. Explicit action settings
        override this group preset, which overrides ``assist.actions.preset`` for the group.

        :stability: experimental
        :schema: Source#preset
        '''
        result = self._values.get("preset")
        return typing.cast(typing.Optional["PresetConfig"], result)

    @builtins.property
    def recommended(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables the recommended actions in this group.

        The group's ``preset``
        setting takes precedence when both options are set.

        :stability: experimental
        :schema: Source#recommended
        '''
        result = self._values.get("recommended")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def use_graphql_sorted_arguments(self) -> typing.Any:
        '''(experimental) Sort the arguments of GraphQL fields and directives in natural order.

        See https://biomejs.dev/assist/actions/use-graphql-sorted-arguments

        :stability: experimental
        :schema: Source#useGraphqlSortedArguments
        '''
        result = self._values.get("use_graphql_sorted_arguments")
        return typing.cast(typing.Any, result)

    @builtins.property
    def use_graphql_sorted_definitions(self) -> typing.Any:
        '''(experimental) Sort the named definitions in a GraphQL document.

        See https://biomejs.dev/assist/actions/use-graphql-sorted-definitions

        :stability: experimental
        :schema: Source#useGraphqlSortedDefinitions
        '''
        result = self._values.get("use_graphql_sorted_definitions")
        return typing.cast(typing.Any, result)

    @builtins.property
    def use_graphql_sorted_variables(self) -> typing.Any:
        '''(experimental) Sort the variable definitions of GraphQL operations in natural order.

        See https://biomejs.dev/assist/actions/use-graphql-sorted-variables

        :stability: experimental
        :schema: Source#useGraphqlSortedVariables
        '''
        result = self._values.get("use_graphql_sorted_variables")
        return typing.cast(typing.Any, result)

    @builtins.property
    def use_sorted_attributes(self) -> typing.Any:
        '''(experimental) Sort HTML attributes and framework directives into a consistent order.

        See https://biomejs.dev/assist/actions/use-sorted-attributes

        :stability: experimental
        :schema: Source#useSortedAttributes
        '''
        result = self._values.get("use_sorted_attributes")
        return typing.cast(typing.Any, result)

    @builtins.property
    def use_sorted_enum_members(self) -> typing.Any:
        '''(experimental) Sort GraphQL enum values in natural order.

        See https://biomejs.dev/assist/actions/use-sorted-enum-members

        :stability: experimental
        :schema: Source#useSortedEnumMembers
        '''
        result = self._values.get("use_sorted_enum_members")
        return typing.cast(typing.Any, result)

    @builtins.property
    def use_sorted_interface_members(self) -> typing.Any:
        '''(experimental) Sort named members of a TypeScript interface.

        See https://biomejs.dev/assist/actions/use-sorted-interface-members

        :stability: experimental
        :schema: Source#useSortedInterfaceMembers
        '''
        result = self._values.get("use_sorted_interface_members")
        return typing.cast(typing.Any, result)

    @builtins.property
    def use_sorted_keys(self) -> typing.Any:
        '''(experimental) Sort keys in a JSON object.

        See https://biomejs.dev/assist/actions/use-sorted-keys

        :stability: experimental
        :schema: Source#useSortedKeys
        '''
        result = self._values.get("use_sorted_keys")
        return typing.cast(typing.Any, result)

    @builtins.property
    def use_sorted_package_json(self) -> typing.Any:
        '''(experimental) Organize package.json fields according to established conventions. See https://biomejs.dev/assist/actions/use-sorted-package-json.

        :stability: experimental
        :schema: Source#useSortedPackageJson
        '''
        result = self._values.get("use_sorted_package_json")
        return typing.cast(typing.Any, result)

    @builtins.property
    def use_sorted_properties(self) -> typing.Any:
        '''(experimental) Sort CSS properties and nested rules into a consistent order.

        See https://biomejs.dev/assist/actions/use-sorted-properties

        :stability: experimental
        :schema: Source#useSortedProperties
        '''
        result = self._values.get("use_sorted_properties")
        return typing.cast(typing.Any, result)

    @builtins.property
    def use_sorted_selection_set(self) -> typing.Any:
        '''(experimental) Sort selections inside GraphQL operations and fragments.

        See https://biomejs.dev/assist/actions/use-sorted-selection-set

        :stability: experimental
        :schema: Source#useSortedSelectionSet
        '''
        result = self._values.get("use_sorted_selection_set")
        return typing.cast(typing.Any, result)

    @builtins.property
    def use_sorted_type_fields(self) -> typing.Any:
        '''(experimental) Sort fields in GraphQL type definitions by name.

        See https://biomejs.dev/assist/actions/use-sorted-type-fields

        :stability: experimental
        :schema: Source#useSortedTypeFields
        '''
        result = self._values.get("use_sorted_type_fields")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Source(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.TailwindConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "attributes": "attributes",
        "merge_functions": "mergeFunctions",
        "stylesheet": "stylesheet",
        "variant_functions": "variantFunctions",
    },
)
class TailwindConfiguration:
    def __init__(
        self,
        *,
        attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
        merge_functions: typing.Optional[typing.Sequence[builtins.str]] = None,
        stylesheet: typing.Optional[builtins.str] = None,
        variant_functions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Tells Biome where your code lists Tailwind CSS classes, so the Tailwind lint rules know which strings to check.

        :param attributes: (experimental) Attributes whose values are Tailwind classes, such as ``class`` in ``<div class="px-2 py-2">``. Defaults to ``class`` and ``className``. In HTML, they are case-insensitive. Default: class``and``className`. In HTML, they are case-insensitive.
        :param merge_functions: (experimental) Functions that combine Tailwind classes, such as ``clsx`` and ``cn``. Biome checks every string passed to these functions, like both strings in ``cn("px-2", "py-2")``. When an object is passed, Biome checks its keys: in ``cn({ "px-2": isActive })``, it checks ``"px-2"``. Properties of these functions are checked too, so listing ``tw`` also covers ``tw.div`px-2``` and ``tw.div("px-2")``. Defaults to ``clsx``, ``tw``, ``twMerge``, ``twJoin``, ``cn``, ``cc``, ``cnb``, and ``ctl``. Default: clsx``, ``tw``, ``twMerge``, ``twJoin``, ``cn``, ``cc``, ``cnb`, and
        :param stylesheet: (experimental) The CSS file that holds your Tailwind CSS configuration, such as ``"./src/app.css"``. A relative path starts from the folder of the Biome configuration file. Biome reads the ``@theme``, ``@utility``, and ``@custom-variant`` rules in this file and in the files it imports with ``@import``, so that the Tailwind rules know your theme values, utilities, and variants. To read the file, Biome scans your project when a Tailwind rule is enabled. Setting this option also turns on ``css.parser.tailwindDirectives``, unless you set that option yourself.
        :param variant_functions: (experimental) Functions that describe a component's styles with an object, such as ``cva`` and ``tv``. Biome checks every string passed directly to these functions. In an object passed to them, Biome checks the classes under these properties: - ``base``, ``class``, and ``className``: classes that always apply. - ``variants``: classes for each version of the component, such as each button size. - ``slots``: classes for each part of the component, such as its icon. - ``compoundVariants`` and ``compoundSlots``: only the ``class`` and ``className`` of each entry. Other properties, such as ``defaultVariants``, hold names rather than classes, so Biome skips them. For example, Biome checks ``"rounded"``, ``"px-2"``, and ``"px-4"`` here, but not ``"small"``:: cva("rounded", { variants: { size: { small: "px-2", large: "px-4" }, }, defaultVariants: { size: "small" }, }); Defaults to ``cva`` and ``tv``. Default: cva``and``tv`.

        :stability: experimental
        :schema: TailwindConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__f57cbd515131470edf00afa86518e00838398080de4b1b1f003b94db15f43581)
            check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
            check_type(argname="argument merge_functions", value=merge_functions, expected_type=type_hints["merge_functions"])
            check_type(argname="argument stylesheet", value=stylesheet, expected_type=type_hints["stylesheet"])
            check_type(argname="argument variant_functions", value=variant_functions, expected_type=type_hints["variant_functions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if attributes is not None:
            self._values["attributes"] = attributes
        if merge_functions is not None:
            self._values["merge_functions"] = merge_functions
        if stylesheet is not None:
            self._values["stylesheet"] = stylesheet
        if variant_functions is not None:
            self._values["variant_functions"] = variant_functions

    @builtins.property
    def attributes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Attributes whose values are Tailwind classes, such as ``class`` in ``<div class="px-2 py-2">``.

        Defaults to ``class`` and ``className``. In HTML, they are case-insensitive.

        :default: class``and``className`. In HTML, they are case-insensitive.

        :stability: experimental
        :schema: TailwindConfiguration#attributes
        '''
        result = self._values.get("attributes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def merge_functions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Functions that combine Tailwind classes, such as ``clsx`` and ``cn``.

        Biome checks every string passed to these functions, like both strings
        in ``cn("px-2", "py-2")``. When an object is passed, Biome checks its
        keys: in ``cn({ "px-2": isActive })``, it checks ``"px-2"``.

        Properties of these functions are checked too, so listing ``tw`` also
        covers ``tw.div``px-2`` and ``tw.div("px-2")``.

        Defaults to ``clsx``, ``tw``, ``twMerge``, ``twJoin``, ``cn``, ``cc``, ``cnb``, and
        ``ctl``.

        :default: clsx``, ``tw``, ``twMerge``, ``twJoin``, ``cn``, ``cc``, ``cnb`, and

        :stability: experimental
        :schema: TailwindConfiguration#mergeFunctions
        '''
        result = self._values.get("merge_functions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def stylesheet(self) -> typing.Optional[builtins.str]:
        '''(experimental) The CSS file that holds your Tailwind CSS configuration, such as ``"./src/app.css"``. A relative path starts from the folder of the Biome configuration file.

        Biome reads the ``@theme``, ``@utility``, and ``@custom-variant`` rules in
        this file and in the files it imports with ``@import``, so that the
        Tailwind rules know your theme values, utilities, and variants.

        To read the file, Biome scans your project when a Tailwind rule is
        enabled. Setting this option also turns on ``css.parser.tailwindDirectives``,
        unless you set that option yourself.

        :stability: experimental
        :schema: TailwindConfiguration#stylesheet
        '''
        result = self._values.get("stylesheet")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def variant_functions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Functions that describe a component's styles with an object, such as ``cva`` and ``tv``.

        Biome checks every string passed directly to these functions. In an
        object passed to them, Biome checks the classes under these properties:

        - ``base``, ``class``, and ``className``: classes that always apply.
        - ``variants``: classes for each version of the component, such as each
          button size.
        - ``slots``: classes for each part of the component, such as its icon.
        - ``compoundVariants`` and ``compoundSlots``: only the ``class`` and
          ``className`` of each entry.

        Other properties, such as ``defaultVariants``, hold names rather than
        classes, so Biome skips them. For example, Biome checks ``"rounded"``,
        ``"px-2"``, and ``"px-4"`` here, but not ``"small"``::

           cva("rounded", {
           variants: {
           size: { small: "px-2", large: "px-4" },
           },
           defaultVariants: { size: "small" },
           });

        Defaults to ``cva`` and ``tv``.

        :default: cva``and``tv`.

        :stability: experimental
        :schema: TailwindConfiguration#variantFunctions
        '''
        result = self._values.get("variant_functions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TailwindConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="projen.javascript.biome_config.VcsClientKind")
class VcsClientKind(enum.Enum):
    '''(experimental) Integration with Git as the version control client.

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
        client_kind: typing.Optional["VcsClientKind"] = None,
        default_branch: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        root: typing.Optional[builtins.str] = None,
        use_ignore_file: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Configures how Biome integrates with a version control system.

        :param client_kind: (experimental) Selects the version-control client. Currently, only ``git`` is supported.
        :param default_branch: (experimental) Sets the base branch used by ``--changed`` when ``--since`` is not provided. If neither this option nor ``--since`` is set, commands using ``--changed`` fail because Biome cannot determine the comparison base.
        :param enabled: (experimental) Enables or disables version-control integration. Defaults to ``false``. Enabling integration requires ``vcs.clientKind`` to be set. Default: false`. Enabling integration
        :param root: (experimental) Sets the directory where Biome looks for version-control files. A relative value is resolved from the directory containing the current configuration file, while an absolute path is used directly. Defaults to the directory containing ``biome.json`` or ``biome.jsonc``. If no configuration is found, Biome uses the current working directory. If neither directory is available, Biome disables version control integration and emits a diagnostic. Default: the directory containing ``biome.json`` or ``biome.jsonc``. If no configuration is
        :param use_ignore_file: (experimental) Controls whether Biome applies patterns from ``.gitignore``, Git's local ``.git/info/exclude``, and supported ``.ignore`` files, including nested ignore files. Patterns in the root ignore file are resolved from ``vcs.root``. Patterns in nested ignore files are resolved from the directory containing that file. Defaults to ``false``. Default: false`.

        :stability: experimental
        :schema: VcsConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__d0ca0d2f64e42e40c29e089e5200324b97670a6ebbf0f39b444b15a42a7150b7)
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
    def client_kind(self) -> typing.Optional["VcsClientKind"]:
        '''(experimental) Selects the version-control client.

        Currently, only ``git`` is supported.

        :stability: experimental
        :schema: VcsConfiguration#clientKind
        '''
        result = self._values.get("client_kind")
        return typing.cast(typing.Optional["VcsClientKind"], result)

    @builtins.property
    def default_branch(self) -> typing.Optional[builtins.str]:
        '''(experimental) Sets the base branch used by ``--changed`` when ``--since`` is not provided.

        If neither this option
        nor ``--since`` is set, commands using ``--changed`` fail because Biome cannot determine the
        comparison base.

        :stability: experimental
        :schema: VcsConfiguration#defaultBranch
        '''
        result = self._values.get("default_branch")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables or disables version-control integration.

        Defaults to ``false``. Enabling integration
        requires ``vcs.clientKind`` to be set.

        :default: false`. Enabling integration

        :stability: experimental
        :schema: VcsConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def root(self) -> typing.Optional[builtins.str]:
        '''(experimental) Sets the directory where Biome looks for version-control files.

        A relative value is resolved
        from the directory containing the current configuration file, while an absolute path is used
        directly.

        Defaults to the directory containing ``biome.json`` or ``biome.jsonc``. If no configuration is
        found, Biome uses the current working directory.

        If neither directory is available, Biome disables version control integration and emits a
        diagnostic.

        :default: the directory containing ``biome.json`` or ``biome.jsonc``. If no configuration is

        :stability: experimental
        :schema: VcsConfiguration#root
        '''
        result = self._values.get("root")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_ignore_file(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Controls whether Biome applies patterns from ``.gitignore``, Git's local ``.git/info/exclude``, and supported ``.ignore`` files, including nested ignore files. Patterns in the root ignore file are resolved from ``vcs.root``. Patterns in nested ignore files are resolved from the directory containing that file. Defaults to ``false``.

        :default: false`.

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
    '''(experimental) Controls how the formatter treats whitespace around text and child elements in HTML, Vue, Svelte, and Astro markup.

    The following two cases won't produce the same output:

    |                |      html      |    output    |
    | -------------- | :------------: | :----------: |
    | with spaces    | ``1<b> 2 </b>3`` | 1 2 3 |
    | without spaces |  ``1<b>2</b>3``  |  123  |

    This happens because whitespace is significant in inline elements.

    As a consequence of this, the formatter must format blocks that look like this (assume a small line width, <20)::

       <span>really long content</span>

    as this, where the content hugs the tags::

       <span
       >really long content</span
       >

    Note that this is only necessary for inline elements. Block elements do not have this restriction.

    :stability: experimental
    :schema: WhitespaceSensitivity
    '''

    CSS = "CSS"
    '''(experimental) Treats whitespace as significant for elements that browsers display inline by default.

    (css)

    :stability: experimental
    '''
    STRICT = "STRICT"
    '''(experimental) Treats leading and trailing whitespace as significant for every element.

    Existing whitespace
    is preserved as at least one character and absent whitespace is not added.

    Example of text hugging the tags::

       <b
       >content</b
       >
       ``` (strict)

    :stability: experimental
    '''
    IGNORE = "IGNORE"
    '''(experimental) Treats whitespace as insignificant, allowing the formatter to add or remove it.

    Use this only
    when whitespace cannot affect rendered output. (ignore)

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.YamlConfiguration",
    jsii_struct_bases=[],
    name_mapping={"formatter": "formatter", "linter": "linter"},
)
class YamlConfiguration:
    def __init__(
        self,
        *,
        formatter: typing.Optional[typing.Union["YamlFormatterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        linter: typing.Optional[typing.Union["YamlLinterConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options applied to Yaml files.

        :param formatter: (experimental) Formatter options.
        :param linter: 

        :stability: experimental
        :schema: YamlConfiguration
        '''
        if isinstance(formatter, dict):
            formatter = YamlFormatterConfiguration(**formatter)
        if isinstance(linter, dict):
            linter = YamlLinterConfiguration(**linter)
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__e4be2e84646b4f1e76ed6203c510bd540d723eaa817a823ec387e839e5770734)
            check_type(argname="argument formatter", value=formatter, expected_type=type_hints["formatter"])
            check_type(argname="argument linter", value=linter, expected_type=type_hints["linter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if formatter is not None:
            self._values["formatter"] = formatter
        if linter is not None:
            self._values["linter"] = linter

    @builtins.property
    def formatter(self) -> typing.Optional["YamlFormatterConfiguration"]:
        '''(experimental) Formatter options.

        :stability: experimental
        :schema: YamlConfiguration#formatter
        '''
        result = self._values.get("formatter")
        return typing.cast(typing.Optional["YamlFormatterConfiguration"], result)

    @builtins.property
    def linter(self) -> typing.Optional["YamlLinterConfiguration"]:
        '''
        :stability: experimental
        :schema: YamlConfiguration#linter
        '''
        result = self._values.get("linter")
        return typing.cast(typing.Optional["YamlLinterConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "YamlConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.YamlFormatterConfiguration",
    jsii_struct_bases=[],
    name_mapping={
        "bracket_spacing": "bracketSpacing",
        "enabled": "enabled",
        "indent_width": "indentWidth",
        "line_ending": "lineEnding",
        "line_width": "lineWidth",
        "quote_style": "quoteStyle",
        "trailing_newline": "trailingNewline",
    },
)
class YamlFormatterConfiguration:
    def __init__(
        self,
        *,
        bracket_spacing: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        indent_width: typing.Optional[jsii.Number] = None,
        line_ending: typing.Optional["LineEnding"] = None,
        line_width: typing.Optional[jsii.Number] = None,
        quote_style: typing.Optional["QuoteStyle"] = None,
        trailing_newline: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options that change how the Yaml formatter behaves.

        :param bracket_spacing: (experimental) Whether to insert spaces inside non-empty flow mappings (``{ key: value }``) and sequences (``[ item ]``) that fit on one line. If unset, inherits the global bracket spacing setting. When neither is set, mappings have spaces and sequences do not.
        :param enabled: (experimental) Control the formatter for Yaml (and its super languages) files.
        :param indent_width: (experimental) The size of the indentation applied to Yaml files. Defaults to 2. Default: 2.
        :param line_ending: (experimental) The type of line ending applied to Yaml (and its super languages) files. ``auto`` uses CRLF on Windows and LF on other platforms.
        :param line_width: (experimental) What's the max width of a line applied to Yaml files. Defaults to 80. Default: 80.
        :param quote_style: (experimental) The type of quotes used in YAML code. Defaults to ``double``. Default: double`.
        :param trailing_newline: (experimental) Whether to add a trailing newline at the end of the file. Setting this option to ``false`` is **highly discouraged** because it could cause many problems with other tools: - https://thoughtbot.com/blog/no-newline-at-end-of-file - https://callmeryan.medium.com/no-newline-at-end-of-file-navigating-gits-warning-for-android-developers-af14e73dd804 - https://unix.stackexchange.com/questions/345548/how-to-cat-files-together-adding-missing-newlines-at-end-of-some-files Disable the option at your own risk. Defaults to true. Default: true.

        :stability: experimental
        :schema: YamlFormatterConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__81c4c499f318c8dc484c199cfecf1d58ce9436ca1c3426be083c0dc6eba27680)
            check_type(argname="argument bracket_spacing", value=bracket_spacing, expected_type=type_hints["bracket_spacing"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument indent_width", value=indent_width, expected_type=type_hints["indent_width"])
            check_type(argname="argument line_ending", value=line_ending, expected_type=type_hints["line_ending"])
            check_type(argname="argument line_width", value=line_width, expected_type=type_hints["line_width"])
            check_type(argname="argument quote_style", value=quote_style, expected_type=type_hints["quote_style"])
            check_type(argname="argument trailing_newline", value=trailing_newline, expected_type=type_hints["trailing_newline"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bracket_spacing is not None:
            self._values["bracket_spacing"] = bracket_spacing
        if enabled is not None:
            self._values["enabled"] = enabled
        if indent_width is not None:
            self._values["indent_width"] = indent_width
        if line_ending is not None:
            self._values["line_ending"] = line_ending
        if line_width is not None:
            self._values["line_width"] = line_width
        if quote_style is not None:
            self._values["quote_style"] = quote_style
        if trailing_newline is not None:
            self._values["trailing_newline"] = trailing_newline

    @builtins.property
    def bracket_spacing(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to insert spaces inside non-empty flow mappings (``{ key: value }``) and sequences (``[ item ]``) that fit on one line.

        If unset, inherits the
        global bracket spacing setting. When neither is set, mappings have spaces
        and sequences do not.

        :stability: experimental
        :schema: YamlFormatterConfiguration#bracketSpacing
        '''
        result = self._values.get("bracket_spacing")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the formatter for Yaml (and its super languages) files.

        :stability: experimental
        :schema: YamlFormatterConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def indent_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The size of the indentation applied to Yaml files.

        Defaults to 2.

        :default: 2.

        :stability: experimental
        :schema: YamlFormatterConfiguration#indentWidth
        '''
        result = self._values.get("indent_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def line_ending(self) -> typing.Optional["LineEnding"]:
        '''(experimental) The type of line ending applied to Yaml (and its super languages) files.

        ``auto`` uses CRLF on Windows and LF on other platforms.

        :stability: experimental
        :schema: YamlFormatterConfiguration#lineEnding
        '''
        result = self._values.get("line_ending")
        return typing.cast(typing.Optional["LineEnding"], result)

    @builtins.property
    def line_width(self) -> typing.Optional[jsii.Number]:
        '''(experimental) What's the max width of a line applied to Yaml files.

        Defaults to 80.

        :default: 80.

        :stability: experimental
        :schema: YamlFormatterConfiguration#lineWidth
        '''
        result = self._values.get("line_width")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def quote_style(self) -> typing.Optional["QuoteStyle"]:
        '''(experimental) The type of quotes used in YAML code.

        Defaults to ``double``.

        :default: double`.

        :stability: experimental
        :schema: YamlFormatterConfiguration#quoteStyle
        '''
        result = self._values.get("quote_style")
        return typing.cast(typing.Optional["QuoteStyle"], result)

    @builtins.property
    def trailing_newline(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to add a trailing newline at the end of the file.

        Setting this option to ``false`` is **highly discouraged** because it could cause many problems with other tools:

        - https://thoughtbot.com/blog/no-newline-at-end-of-file
        - https://callmeryan.medium.com/no-newline-at-end-of-file-navigating-gits-warning-for-android-developers-af14e73dd804
        - https://unix.stackexchange.com/questions/345548/how-to-cat-files-together-adding-missing-newlines-at-end-of-some-files

        Disable the option at your own risk.

        Defaults to true.

        :default: true.

        :stability: experimental
        :schema: YamlFormatterConfiguration#trailingNewline
        '''
        result = self._values.get("trailing_newline")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "YamlFormatterConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="projen.javascript.biome_config.YamlLinterConfiguration",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class YamlLinterConfiguration:
    def __init__(self, *, enabled: typing.Optional[builtins.bool] = None) -> None:
        '''(experimental) Options that change how the Yaml linter behaves.

        :param enabled: (experimental) Control the linter for Yaml files.

        :stability: experimental
        :schema: YamlLinterConfiguration
        '''
        if __debug__:
            type_hints = cached_type_hints(_typecheckingstub__c83d03a52addd9222a3003b1f2875dabba0929b35d82eca404422215464f903f)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Control the linter for Yaml files.

        :stability: experimental
        :schema: YamlLinterConfiguration#enabled
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "YamlLinterConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


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
    "HtmlAssistConfiguration",
    "HtmlConfiguration",
    "HtmlFormatterConfiguration",
    "HtmlLinterConfiguration",
    "HtmlParserConfiguration",
    "IndentStyle",
    "JsAssistConfiguration",
    "JsConfiguration",
    "JsFormatterConfiguration",
    "JsLinterConfiguration",
    "JsParserConfiguration",
    "JsResolverConfiguration",
    "JsTrailingCommas",
    "JsonAssistConfiguration",
    "JsonConfiguration",
    "JsonFormatterConfiguration",
    "JsonLinterConfiguration",
    "JsonParserConfiguration",
    "JsonTrailingCommas",
    "JsxRuntime",
    "LineEnding",
    "LinterConfiguration",
    "MarkdownConfiguration",
    "MarkdownFormatterConfiguration",
    "MarkdownLinterConfiguration",
    "MarkdownParserConfiguration",
    "OperatorLinebreak",
    "OverrideAssistConfiguration",
    "OverrideFilesConfiguration",
    "OverrideFormatterConfiguration",
    "OverrideLinterConfiguration",
    "OverridePattern",
    "PresetConfig",
    "ProseWrap",
    "QuoteProperties",
    "QuoteStyle",
    "RuleDomainValue",
    "RuleDomains",
    "Rules",
    "SelfCloseVoidElements",
    "Semicolons",
    "Source",
    "TailwindConfiguration",
    "VcsClientKind",
    "VcsConfiguration",
    "WhitespaceSensitivity",
    "YamlConfiguration",
    "YamlFormatterConfiguration",
    "YamlLinterConfiguration",
]

publication.publish()

def _typecheckingstub__6366c915d5edbe08a6c33dee8fe8422a0286f131b30d1697e72b9e5e37127dcc(
    *,
    preset: typing.Optional[PresetConfig] = None,
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
    extends: typing.Any = None,
    files: typing.Optional[typing.Union[FilesConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    formatter: typing.Optional[typing.Union[FormatterConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    graphql: typing.Optional[typing.Union[GraphqlConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    grit: typing.Optional[typing.Union[GritConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    html: typing.Optional[typing.Union[HtmlConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    javascript: typing.Optional[typing.Union[JsConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    json: typing.Optional[typing.Union[JsonConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    linter: typing.Optional[typing.Union[LinterConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    markdown: typing.Optional[typing.Union[MarkdownConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    overrides: typing.Optional[typing.Sequence[typing.Union[OverridePattern, typing.Dict[builtins.str, typing.Any]]]] = None,
    plugins: typing.Optional[typing.Sequence[typing.Any]] = None,
    root: typing.Optional[builtins.bool] = None,
    schema: typing.Optional[builtins.str] = None,
    tailwind: typing.Optional[typing.Union[TailwindConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    vcs: typing.Optional[typing.Union[VcsConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    yaml: typing.Optional[typing.Union[YamlConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
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
    delimiter_spacing: typing.Optional[builtins.bool] = None,
    enabled: typing.Optional[builtins.bool] = None,
    indent_style: typing.Optional[IndentStyle] = None,
    indent_width: typing.Optional[jsii.Number] = None,
    line_ending: typing.Optional[LineEnding] = None,
    line_width: typing.Optional[jsii.Number] = None,
    quote_style: typing.Optional[QuoteStyle] = None,
    trailing_newline: typing.Optional[builtins.bool] = None,
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
    tailwind_directives: typing.Optional[builtins.bool] = None,
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
    delimiter_spacing: typing.Optional[builtins.bool] = None,
    enabled: typing.Optional[builtins.bool] = None,
    expand: typing.Optional[Expand] = None,
    format_with_errors: typing.Optional[builtins.bool] = None,
    includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    indent_style: typing.Optional[IndentStyle] = None,
    indent_width: typing.Optional[jsii.Number] = None,
    line_ending: typing.Optional[LineEnding] = None,
    line_width: typing.Optional[jsii.Number] = None,
    trailing_newline: typing.Optional[builtins.bool] = None,
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
    trailing_newline: typing.Optional[builtins.bool] = None,
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
    trailing_newline: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f328d623f0baa93f52695005ba45f28881c95ae610fde354116a44bc8b01c30(
    *,
    enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f12d37d14edd5b34740aa842931963f60cd55f179c839350e2c9eb8d0ce519a(
    *,
    enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__048266f3b4e4769e6485570d4954197f51204fc6e607e2ffe5267f80089b5ded(
    *,
    assist: typing.Optional[typing.Union[HtmlAssistConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    experimental_full_support_enabled: typing.Optional[builtins.bool] = None,
    formatter: typing.Optional[typing.Union[HtmlFormatterConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    linter: typing.Optional[typing.Union[HtmlLinterConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
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
    trailing_newline: typing.Optional[builtins.bool] = None,
    whitespace_sensitivity: typing.Optional[WhitespaceSensitivity] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__271da6fb8e26ef7e9c2ec0ea9fc3487d2975824399c15a87994edbcfcdd37131(
    *,
    enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b3cfca5c3ad8f608b86ade05d476530f16da0ba23410a7613236950da38ff37(
    *,
    interpolation: typing.Optional[builtins.bool] = None,
    vue: typing.Optional[builtins.bool] = None,
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
    experimental_embedded_snippets_enabled: typing.Optional[builtins.bool] = None,
    formatter: typing.Optional[typing.Union[JsFormatterConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    globals: typing.Optional[typing.Sequence[builtins.str]] = None,
    jsx_runtime: typing.Optional[JsxRuntime] = None,
    linter: typing.Optional[typing.Union[JsLinterConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    parser: typing.Optional[typing.Union[JsParserConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    resolver: typing.Optional[typing.Union[JsResolverConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83d4960ad9dc84017b237fabc105d7837e8a3ec56d19b1de7e01183651d05de1(
    *,
    arrow_parentheses: typing.Optional[ArrowParentheses] = None,
    attribute_position: typing.Optional[AttributePosition] = None,
    bracket_same_line: typing.Optional[builtins.bool] = None,
    bracket_spacing: typing.Optional[builtins.bool] = None,
    delimiter_spacing: typing.Optional[builtins.bool] = None,
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
    trailing_commas: typing.Optional[JsTrailingCommas] = None,
    trailing_newline: typing.Optional[builtins.bool] = None,
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
    jsx_everywhere: typing.Optional[builtins.bool] = None,
    unsafe_parameter_decorators_enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e0ae3402dedb6e0fd3dbd8c7871dc3e24d95f19bd630a3675b446eeff16b76d(
    *,
    experimental_pnpm_catalogs: typing.Optional[builtins.bool] = None,
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
    delimiter_spacing: typing.Optional[builtins.bool] = None,
    enabled: typing.Optional[builtins.bool] = None,
    expand: typing.Optional[Expand] = None,
    indent_style: typing.Optional[IndentStyle] = None,
    indent_width: typing.Optional[jsii.Number] = None,
    line_ending: typing.Optional[LineEnding] = None,
    line_width: typing.Optional[jsii.Number] = None,
    trailing_commas: typing.Optional[JsonTrailingCommas] = None,
    trailing_newline: typing.Optional[builtins.bool] = None,
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
    domains: typing.Optional[typing.Union[RuleDomains, typing.Dict[builtins.str, typing.Any]]] = None,
    enabled: typing.Optional[builtins.bool] = None,
    includes: typing.Optional[typing.Sequence[builtins.str]] = None,
    rules: typing.Optional[typing.Union[Rules, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c0f77fe366fbbfddda5ede857901f0002d502c1e847f7998e0ef60a07b15ee5(
    *,
    analyze_embeds: typing.Optional[builtins.bool] = None,
    formatter: typing.Optional[typing.Union[MarkdownFormatterConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    linter: typing.Optional[typing.Union[MarkdownLinterConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    parser: typing.Optional[typing.Union[MarkdownParserConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ee25d4f71c40309136ce3dadf5413566922dcca0df3b908293e084a82af789a(
    *,
    enabled: typing.Optional[builtins.bool] = None,
    format_embeds: typing.Optional[builtins.bool] = None,
    indent_style: typing.Optional[IndentStyle] = None,
    indent_width: typing.Optional[jsii.Number] = None,
    line_ending: typing.Optional[LineEnding] = None,
    line_width: typing.Optional[jsii.Number] = None,
    prose_wrap: typing.Optional[ProseWrap] = None,
    trailing_newline: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e95f8e46a79bb691a2ac81ce7797be7d5c153005b278d27315908fdc06c7648(
    *,
    enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75b32c24508369083846bdfa68209b976e9a847dc2157991a7a479e27f8f4874(
    *,
    cjk_friendly_emphasis: typing.Optional[builtins.bool] = None,
    frontmatter: typing.Optional[builtins.bool] = None,
    gfm: typing.Optional[builtins.bool] = None,
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
    delimiter_spacing: typing.Optional[builtins.bool] = None,
    enabled: typing.Optional[builtins.bool] = None,
    expand: typing.Optional[Expand] = None,
    format_with_errors: typing.Optional[builtins.bool] = None,
    indent_size: typing.Optional[jsii.Number] = None,
    indent_style: typing.Optional[IndentStyle] = None,
    indent_width: typing.Optional[jsii.Number] = None,
    line_ending: typing.Optional[LineEnding] = None,
    line_width: typing.Optional[jsii.Number] = None,
    trailing_commas: typing.Optional[JsTrailingCommas] = None,
    trailing_newline: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b923acd3721838353ddf97d9a992327d3607a622afc36e911bc3eb842adb709(
    *,
    domains: typing.Optional[typing.Union[RuleDomains, typing.Dict[builtins.str, typing.Any]]] = None,
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
    markdown: typing.Optional[typing.Union[MarkdownConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    plugins: typing.Optional[typing.Sequence[typing.Any]] = None,
    yaml: typing.Optional[typing.Union[YamlConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d48381bffa9c2b0ef8e9116898fdc56e984cd30d1a51b6e379dc5c999a8b5336(
    *,
    astro: typing.Optional[RuleDomainValue] = None,
    drizzle: typing.Optional[RuleDomainValue] = None,
    next: typing.Optional[RuleDomainValue] = None,
    playwright: typing.Optional[RuleDomainValue] = None,
    project: typing.Optional[RuleDomainValue] = None,
    qwik: typing.Optional[RuleDomainValue] = None,
    react: typing.Optional[RuleDomainValue] = None,
    react_native: typing.Optional[RuleDomainValue] = None,
    solid: typing.Optional[RuleDomainValue] = None,
    svelte: typing.Optional[RuleDomainValue] = None,
    tailwind: typing.Optional[RuleDomainValue] = None,
    test: typing.Optional[RuleDomainValue] = None,
    turborepo: typing.Optional[RuleDomainValue] = None,
    types: typing.Optional[RuleDomainValue] = None,
    vue: typing.Optional[RuleDomainValue] = None,
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
    preset: typing.Optional[PresetConfig] = None,
    recommended: typing.Optional[builtins.bool] = None,
    security: typing.Any = None,
    style: typing.Any = None,
    suspicious: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f128bc69ea32431a28e9aae09b49905087cb9f2c49176cf906cbd06f3c7237b7(
    *,
    no_duplicate_classes: typing.Any = None,
    organize_imports: typing.Any = None,
    preset: typing.Optional[PresetConfig] = None,
    recommended: typing.Optional[builtins.bool] = None,
    use_graphql_sorted_arguments: typing.Any = None,
    use_graphql_sorted_definitions: typing.Any = None,
    use_graphql_sorted_variables: typing.Any = None,
    use_sorted_attributes: typing.Any = None,
    use_sorted_enum_members: typing.Any = None,
    use_sorted_interface_members: typing.Any = None,
    use_sorted_keys: typing.Any = None,
    use_sorted_package_json: typing.Any = None,
    use_sorted_properties: typing.Any = None,
    use_sorted_selection_set: typing.Any = None,
    use_sorted_type_fields: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f57cbd515131470edf00afa86518e00838398080de4b1b1f003b94db15f43581(
    *,
    attributes: typing.Optional[typing.Sequence[builtins.str]] = None,
    merge_functions: typing.Optional[typing.Sequence[builtins.str]] = None,
    stylesheet: typing.Optional[builtins.str] = None,
    variant_functions: typing.Optional[typing.Sequence[builtins.str]] = None,
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

def _typecheckingstub__e4be2e84646b4f1e76ed6203c510bd540d723eaa817a823ec387e839e5770734(
    *,
    formatter: typing.Optional[typing.Union[YamlFormatterConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    linter: typing.Optional[typing.Union[YamlLinterConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81c4c499f318c8dc484c199cfecf1d58ce9436ca1c3426be083c0dc6eba27680(
    *,
    bracket_spacing: typing.Optional[builtins.bool] = None,
    enabled: typing.Optional[builtins.bool] = None,
    indent_width: typing.Optional[jsii.Number] = None,
    line_ending: typing.Optional[LineEnding] = None,
    line_width: typing.Optional[jsii.Number] = None,
    quote_style: typing.Optional[QuoteStyle] = None,
    trailing_newline: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c83d03a52addd9222a3003b1f2875dabba0929b35d82eca404422215464f903f(
    *,
    enabled: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass
