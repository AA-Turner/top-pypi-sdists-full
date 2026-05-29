import asyncio
import glob as _glob_stdlib
import importlib
import inspect
import json
import logging
import pkgutil
from typing import Any, List, Optional, Union
from collections.abc import Callable
from pathlib import Path
import pandas as pd
from tqdm import tqdm
from parrot.loaders import AbstractLoader, Document
from parrot_loaders.factory import get_loader_class, LOADER_MAPPING

try:
    from parrot_loaders import LOADER_REGISTRY  # name -> "module.Class"
except ImportError:
    LOADER_REGISTRY = {}

logging.getLogger("pdfminer").setLevel(logging.WARNING)
from ...interfaces.flow import FlowComponent
from ...conf import BASE_DIR
from ...exceptions import ConfigError, ComponentError


DEFAULT_SCRAPING_PLANS_DIR = BASE_DIR.joinpath("artifacts", "scraping_plans")


def _has_glob(pattern: str) -> bool:
    """Return True if the string contains shell-style wildcard characters."""
    return any(ch in pattern for ch in "*?[")


_LLM_CLIENT_MAP = {
    "google": ("parrot.clients.google", "GoogleGenAIClient"),
    "gemini": ("parrot.clients.google", "GoogleGenAIClient"),
    "googlegenai": ("parrot.clients.google", "GoogleGenAIClient"),
    "anthropic": ("parrot.clients.claude", "AnthropicClient"),
    "claude": ("parrot.clients.claude", "AnthropicClient"),
    "openai": ("parrot.clients.gpt", "OpenAIClient"),
    "gpt": ("parrot.clients.gpt", "OpenAIClient"),
    "groq": ("parrot.clients.groq", "GroqClient"),
    "grok": ("parrot.clients.grok", "GrokClient"),
}


class ParrotLoader(FlowComponent):
    """
    ParrotLoader.

    Overview:

    Getting a list of documents and convert them using Parrot Loaders.


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          ParrotLoader:
          path: /home/ubuntu/symbits/lg/bot/products_positive
          source_type: Product-Top-Reviews
          loader: HTMLLoader
          chunk_size: 2048
        ```

        LLM-backed loader (e.g. WebScrapingLoader) — pick the provider via
        the ``llm`` key. Falls back to ``google`` when omitted and relies on
        the provider's standard environment variables for credentials.
        Scraping plans are persisted under
        ``BASE_DIR/artifacts/scraping_plans`` by default; override via
        ``plans_dir`` and toggle persistence with ``save_plan``:

        ```yaml
          ParrotLoader:
            path: "https://www.att.com/prepaid/plans/"
            loader: WebScrapingLoader
            source_type: att-prepaid-plans
            llm: anthropic          # google | anthropic | openai | groq | grok
            llm_model: claude-sonnet-4-5
            objective: "Extract prepaid plan cards..."
            save_plan: true         # enable to persist generated plans
        ```

        Multi-source mode — iterate over many URLs, files, or directories
        in a single run. Three entry points, resolved with this priority:

        1. ``path_list``: either an inline YAML list or a filename pointing
           to a ``.txt`` / ``.json`` / ``.csv`` file. Supported formats via
           ``path_list_format``: ``auto`` (default), ``txt``, ``json``,
           ``csv``. The ``txt`` reader also accepts files whose content is
           a JSON array. For ``csv`` the column is ``path_column``
           (default ``url``).
        2. ``path_column`` + upstream DataFrame: when a previous component
           passes a DataFrame and ``path_column`` is configured, values
           from that column are used as the list of sources.
        3. ``path`` with wildcards (``*``, ``?``, ``[...]``): expanded via
           glob and iterated.

        Per-entry failures log a warning and continue.

        ```yaml
          ParrotLoader:
            path_list: /path/to/yt_links.txt
            loader: YoutubeLoader
            source_type: youtube-videos
            chunk_size: 2048
        ```

        ```yaml
          ParrotLoader:
            path_list:
              - https://youtu.be/xxx
              - https://youtu.be/yyy
            loader: YoutubeLoader
            source_type: youtube-videos
        ```

        ```yaml
          # Upstream component returns a DataFrame with a "video_url" column
          ParrotLoader:
            path_column: video_url
            loader: YoutubeLoader
            source_type: youtube-videos
        ```

        ```yaml
          # Wildcard on path — expanded via pathlib glob
          ParrotLoader:
            path: /home/*/myfiles/*.pdf
            source_type: product-manuals
            chunk_size: 2048
        ```
    """
    _version = "1.0.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.extensions: list = kwargs.pop('extensions', [])
        self.encoding: str = kwargs.get('encoding', 'utf-8')
        self.path: str = kwargs.pop('path', None)
        self.skip_directories: List[str] = kwargs.pop('skip_directories', [])
        self._chunk_size = kwargs.get('chunk_size', 8000)
        self.source_type: str = kwargs.pop('source_type', 'document')
        self.doctype: str = kwargs.pop('doctype', 'document')
        self.category: str = kwargs.pop('category', 'document')
        # LLM provider name (string) or pre-built client instance.
        self._llm = kwargs.pop('llm', None)
        self._llm_model = kwargs.pop('llm_model', None)
        # Table settings for PDFTablesLoader
        self.table_settings = kwargs.pop('table_settings', {})
        # Multi-source inputs: inline list, list file, or DataFrame column.
        self._path_list: Optional[Any] = kwargs.pop('path_list', None)
        self._path_list_format: str = str(
            kwargs.pop('path_list_format', 'auto') or 'auto'
        ).lower()
        self._path_column: Optional[str] = kwargs.pop('path_column', None)
        super().__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )
        self._device: str = kwargs.get('device', 'cpu')
        self._cuda_number: int = kwargs.get('cuda_number', 0)

    def _build_llm_client(self):
        """Instantiate an LLM client based on ``self._llm``.

        Accepts either a provider name (string key from ``_LLM_CLIENT_MAP``)
        or an already-built client instance. Credentials are resolved from
        the provider's standard environment variables.
        """
        if self._llm is not None and not isinstance(self._llm, str):
            return self._llm

        provider = (self._llm or "google").lower()
        if provider not in _LLM_CLIENT_MAP:
            raise ConfigError(
                f"ParrotLoader: unknown llm provider '{self._llm}'. "
                f"Known providers: {sorted(_LLM_CLIENT_MAP)}"
            )

        module_path, class_name = _LLM_CLIENT_MAP[provider]
        module = importlib.import_module(module_path)
        cls = getattr(module, class_name)

        init_kwargs = {}
        if self._llm_model:
            init_kwargs["model"] = self._llm_model

        client = cls(**init_kwargs)
        self._logger.info(
            "ParrotLoader: injected %s as llm_client (provider=%s)",
            class_name, provider,
        )
        return client

    async def close(self):
        # Destroy effectively all Models.
        pass

    async def start(self, **kwargs):
        await super().start(**kwargs)

        upstream_df = isinstance(getattr(self, 'data', None), pd.DataFrame)
        has_multi_source = (
            self._path_list is not None
            or (self._path_column and upstream_df)
        )

        # Check if path comes from previous component (like FileList)
        if not self.path and self.previous and self.input:
            filename = kwargs.get('filename')
            if filename:
                self.path = filename
                print(f"ParrotLoader: Received file from previous component: {self.path}")
            elif not has_multi_source:
                # Fallback: try to use input directly. Skipped when a multi-
                # source mode (path_list / path_column) is already active.
                self.path = self.input

        # Normalize a string path_list (treated as a filename) via mask replacement.
        if isinstance(self._path_list, str):
            self._path_list = self.mask_replacement_recursively(self._path_list)

        if self.path:
            if isinstance(self.path, str):
                self.path = self.mask_replacement_recursively(self.path)
                if self.path.startswith(('http://', 'https://', 'ftp://')):
                    # URLs are kept as-is — no filesystem checks.
                    print(f"Loading from URL: {self.path}")
                elif _has_glob(self.path):
                    # Keep as a string pattern; expansion happens in run().
                    print(f"Loading with glob pattern: {self.path}")
                else:
                    self.path = Path(self.path).resolve()
                    if not self.path.exists():
                        raise ComponentError(
                            f"ParrotLoader: {self.path} doesn't exist."
                        )
            elif isinstance(self.path, Path):
                if not self.path.exists():
                    raise ComponentError(
                        f"ParrotLoader: {self.path} doesn't exist."
                    )
        elif has_multi_source:
            # path is optional when path_list or DataFrame-column mode is active.
            pass
        else:
            raise ConfigError(
                "Provide at least one directory or filename in *path* "
                "attribute, a *path_list*, or ensure previous component "
                "provides input."
            )

    def _get_loader_by_extension(self, suffix: str, source_path: Union[Path, List] = None) -> AbstractLoader:
        """Get a Document Loader based on file extension."""
        suffix = suffix.lower()
        if suffix not in LOADER_MAPPING:
            raise ComponentError(
                f"ParrotLoader: No loader available for extension '{suffix}'. "
                f"Available extensions: {list(LOADER_MAPPING.keys())}"
            )

        loader_class = get_loader_class(suffix)

        doctype = f"{self.source_type}-{suffix.lstrip('.')}"

        # Common Arguments for Parrot loaders
        args = {
            "source": source_path or self.path,
            "chunk_size": self._chunk_size,
            "encoding": self.encoding,
            "source_type": self.source_type,
            "doctype": doctype,
            "category": self.category,
            "device": self._device,
            "cuda_number": self._cuda_number,
        }

        return loader_class(**args)

    def _resolve_loader_class(self, name: str) -> Optional[type]:
        """Find a Parrot loader class by name across known locations.

        Resolution order:
        1. ``parrot_loaders.LOADER_REGISTRY`` (canonical registry, values
           are ``"module.ClassName"`` strings).
        2. Direct attribute on ``parrot_loaders`` / ``parrot.loaders``.
        3. Walk first-level submodules of ``parrot_loaders`` (e.g. the
           ``webscraping`` module exposes ``WebScrapingLoader`` without
           being re-exported at package root).
        """
        spec = LOADER_REGISTRY.get(name)
        if isinstance(spec, str) and "." in spec:
            module_path, class_name = spec.rsplit(".", 1)
            try:
                return getattr(importlib.import_module(module_path), class_name)
            except (ImportError, AttributeError):
                pass
        elif inspect.isclass(spec):
            return spec

        for module_path in ("parrot_loaders", "parrot.loaders"):
            try:
                module = importlib.import_module(module_path)
            except (ImportError, ModuleNotFoundError):
                continue
            try:
                candidate = getattr(module, name, None)
            except ImportError:
                # parrot.loaders.__getattr__ raises ImportError for
                # unknown/unavailable names; treat as "not here".
                candidate = None
            if inspect.isclass(candidate):
                return candidate

        try:
            pkg = importlib.import_module("parrot_loaders")
        except (ImportError, ModuleNotFoundError):
            return None
        for sub in pkgutil.iter_modules(pkg.__path__):
            try:
                submod = importlib.import_module(f"parrot_loaders.{sub.name}")
            except Exception:  # noqa: BLE001
                continue
            candidate = getattr(submod, name, None)
            if inspect.isclass(candidate):
                return candidate
        return None

    def _load_loader_by_name(self, name: str) -> AbstractLoader:
        """Dynamically imports a loader class from parrot_loaders or parrot.loaders."""
        cls = self._resolve_loader_class(name)

        if cls is None:
            raise ImportError(
                f"Unable to load the Parrot loader '{name}': not found in "
                f"LOADER_REGISTRY, 'parrot_loaders', or 'parrot.loaders'."
            )

        try:
            sig = inspect.signature(cls.__init__)
            params = sig.parameters
            has_var_kw = any(
                p.kind == inspect.Parameter.VAR_KEYWORD for p in params.values()
            )

            def _accepts(key: str) -> bool:
                """Loader can receive this kwarg (named or via **kwargs)."""
                return key in params or has_var_kw

            def _explicit(key: str) -> bool:
                """Loader declares this kwarg explicitly in its signature."""
                param = params.get(key)
                return param is not None and param.kind not in (
                    inspect.Parameter.VAR_POSITIONAL,
                    inspect.Parameter.VAR_KEYWORD,
                )

            # Parrot loaders require 'source' as first positional argument
            args = {"source": self.path}

            if _accepts("chunk_size"):
                args["chunk_size"] = self._chunk_size
            if _accepts("encoding"):
                args["encoding"] = self.encoding

            # source_type/doctype/category: only pass when the loader names
            # them explicitly. Loaders like WebScrapingLoader hardcode their
            # own source_type when calling super(), so passing these via
            # **kwargs raises TypeError. The user's values are still applied
            # post-load via _stamp_metadata().
            if _explicit("source_type"):
                args["source_type"] = self.source_type
            if _explicit("doctype"):
                args["doctype"] = self.doctype
            if _explicit("category"):
                args["category"] = self.category

            # Only add device parameters for loaders that support them
            if name not in ("YoutubeLoader", "VideoLoader"):
                if _accepts("device"):
                    args["device"] = self._device
                if _accepts("cuda_number"):
                    args["cuda_number"] = self._cuda_number

            # Pass through any additional parameters from the component
            # configuration, filtered by the target loader's signature.
            skip_attrs = {
                "loader", "path", "extensions", "skip_directories",
                "llm", "llm_model", "source_type", "doctype", "category",
                "chunk_size", "encoding", "device", "cuda_number",
                "table_settings",
                "path_list", "path_list_format", "path_column",
            }
            for key, value in self._attrs.items():
                if key in skip_attrs or key in args:
                    continue
                if _accepts(key):
                    args[key] = value

            # Handle table_settings specifically for PDFTablesLoader
            if hasattr(self, 'table_settings') and isinstance(self.table_settings, dict):
                for key, value in self.table_settings.items():
                    if _accepts(key):
                        args[key] = value

            # Auto-inject an LLM client when the loader declares `llm_client`.
            if 'llm_client' in params and args.get('llm_client') is None:
                args['llm_client'] = self._build_llm_client()

            # Default plans_dir to a flowtask-wide location so scraping plans
            # land under BASE_DIR/artifacts/scraping_plans instead of the
            # toolkit's CWD-relative default.
            if 'plans_dir' in params and not args.get('plans_dir'):
                DEFAULT_SCRAPING_PLANS_DIR.mkdir(parents=True, exist_ok=True)
                args['plans_dir'] = str(DEFAULT_SCRAPING_PLANS_DIR)

            loader = cls(**args)
            self._logger.info("ParrotLoader: instantiated %s", name)
            return loader
        except Exception as e:
            raise ImportError(
                f"Unable to instantiate the Parrot loader '{name}': {e}"
            ) from e

    def _extract_paths_from_dataframe(self, df: pd.DataFrame) -> List[str]:
        """Pull source paths/URLs from the configured column of a DataFrame."""
        col = self._path_column or "url"
        if col not in df.columns:
            raise ComponentError(
                f"ParrotLoader: DataFrame has no column '{col}'. "
                f"Available columns: {list(df.columns)}"
            )
        return [
            str(u).strip()
            for u in df[col].tolist()
            if pd.notna(u) and str(u).strip()
        ]

    def _read_path_list_file(self, file_path: Path) -> List[str]:
        """Parse a file containing a list of paths/URLs.

        Supported formats via ``path_list_format``: ``auto`` (default),
        ``txt``, ``json``, ``csv``. The ``txt`` reader transparently
        handles files whose content is a JSON array, covering the common
        case of ``*.txt`` files that actually hold JSON.
        """
        fmt = self._path_list_format or "auto"

        if fmt == "auto":
            suffix = file_path.suffix.lower()
            if suffix == ".json":
                fmt = "json"
            elif suffix == ".csv":
                fmt = "csv"
            else:
                fmt = "txt"

        if fmt == "csv":
            df = pd.read_csv(file_path, encoding=self.encoding)
            return self._extract_paths_from_dataframe(df)

        text = file_path.read_text(encoding=self.encoding)

        if fmt == "json":
            data = json.loads(text)
            if not isinstance(data, list):
                raise ComponentError(
                    f"ParrotLoader: expected JSON array in {file_path}, "
                    f"got {type(data).__name__}."
                )
            return [str(u).strip() for u in data if isinstance(u, str) and u.strip()]

        if fmt == "txt":
            stripped = text.strip()
            if stripped.startswith("["):
                try:
                    data = json.loads(stripped)
                    if isinstance(data, list):
                        return [
                            str(u).strip()
                            for u in data
                            if isinstance(u, str) and u.strip()
                        ]
                except json.JSONDecodeError:
                    pass
            entries: List[str] = []
            for line in text.splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                entries.append(line)
            return entries

        raise ConfigError(
            f"ParrotLoader: unknown path_list_format '{fmt}'. "
            "Expected one of: auto, txt, json, csv."
        )

    def _resolve_sources(self) -> Optional[List[Union[str, Path]]]:
        """Collect multi-source entries, or ``None`` to fall back to single-source.

        Resolution priority:
          1. ``path_list`` set (inline list or filename).
          2. ``path_column`` set and upstream DataFrame present.
          3. ``path`` with glob wildcards — expanded via ``glob.glob``.
        """
        if self._path_list is not None:
            if isinstance(self._path_list, (list, tuple)):
                return [
                    str(x).strip()
                    for x in self._path_list
                    if x is not None and str(x).strip()
                ]
            if isinstance(self._path_list, (str, Path)):
                file_path = Path(self._path_list).resolve()
                if not file_path.is_file():
                    raise ComponentError(
                        f"ParrotLoader: path_list file not found: {file_path}"
                    )
                return self._read_path_list_file(file_path)
            raise ConfigError(
                f"ParrotLoader: unsupported path_list type "
                f"{type(self._path_list).__name__}; expected list, str, or Path."
            )

        if self._path_column and isinstance(getattr(self, 'data', None), pd.DataFrame):
            return self._extract_paths_from_dataframe(self.data)

        if isinstance(self.path, str) and _has_glob(self.path):
            matches = sorted(_glob_stdlib.glob(self.path, recursive=True))
            return [Path(p).resolve() for p in matches]

        return None

    def _loader_for_url(self, url: str) -> Optional[AbstractLoader]:
        """Resolve the loader to use for a given URL.

        Returns ``None`` when no loader is configured and the URL pattern
        is not auto-recognized; callers should skip and log a warning.
        """
        if hasattr(self, "loader"):
            return self._load_loader_by_name(self.loader)
        if "youtube.com" in url or "youtu.be" in url:
            return self._load_loader_by_name("YoutubeLoader")
        return None

    async def _load_one_source(self, source: Union[str, Path]) -> List[Document]:
        """Load documents from a single source (URL, file, or directory)."""
        if isinstance(source, str) and source.startswith(
            ('http://', 'https://', 'ftp://')
        ):
            # URL dispatch (sets self.path so ``source`` arg in loader
            # constructors matches the per-entry URL).
            self.path = source
            loader = self._loader_for_url(source)
            if loader is None:
                raise ComponentError(
                    f"ParrotLoader: no loader mapping for URL {source}"
                )
            return await loader.load(source)

        path = Path(source).resolve()
        if not path.exists():
            raise ComponentError(f"ParrotLoader: path does not exist: {path}")

        self.path = path
        if path.is_dir():
            return await self._load_directory(path)
        if path.is_file():
            if hasattr(self, 'loader'):
                loader = self._load_loader_by_name(self.loader)
                return await loader.load(path)
            ext = path.suffix.lower()
            if self.extensions and ext not in self.extensions:
                return []
            loader = self._get_loader_by_extension(ext, source_path=path)
            return await loader.load()
        raise ComponentError(f"ParrotLoader: invalid source: {source}")

    async def _load_directory(self, directory: Path) -> List[Document]:
        """Iterate files in ``directory`` using per-extension loaders."""
        _file_buckets: dict = {}
        if self.extensions:
            for ext in self.extensions:
                for item in directory.glob(f'*{ext}'):
                    if item.is_file() and set(item.parts).isdisjoint(
                        self.skip_directories
                    ):
                        _file_buckets.setdefault(item.suffix.lower(), []).append(item)
        else:
            for item in directory.glob('*.*'):
                if item.is_file() and set(item.parts).isdisjoint(
                    self.skip_directories
                ):
                    _file_buckets.setdefault(item.suffix.lower(), []).append(item)

        documents: List[Document] = []
        for ext, files in _file_buckets.items():
            for file in files:
                try:
                    loader = self._get_loader_by_extension(ext, source_path=file)
                    docs = await loader.load()
                    documents.extend(docs)
                except ComponentError as ce:
                    self._logger.warning("ParrotLoader: %s", ce)
        return documents

    def _stamp_metadata(self, documents: List[Document]) -> None:
        """Apply user-configured source_type/doctype/category to docs.

        Loaders that hardcode these fields (e.g. WebScrapingLoader pins
        ``source_type="webpage"``) would otherwise discard the values set
        in the component YAML. Stamp them onto the resulting documents so
        downstream components (indexers, routers) see the intended tags.
        """
        for doc in documents:
            if doc.metadata is None:
                doc.metadata = {}
            doc.metadata["source_type"] = self.source_type
            doc.metadata["doctype"] = self.doctype
            doc.metadata["category"] = self.category

    async def run(self):
        documents: List[Document] = []

        sources = self._resolve_sources()

        if sources is not None:
            if not sources:
                raise ComponentError(
                    "ParrotLoader: multi-source mode produced no entries."
                )
            self._logger.info(
                "ParrotLoader: processing %d source(s).", len(sources)
            )
            original_path = self.path
            try:
                with tqdm(total=len(sources), desc="ParrotLoader", unit="src") as pbar:
                    for src in sources:
                        try:
                            docs = await self._load_one_source(src)
                            documents.extend(docs)
                        except Exception as exc:  # noqa: BLE001
                            self._logger.warning(
                                "ParrotLoader: failed to load %s: %s", src, exc
                            )
                        finally:
                            pbar.update(1)
            finally:
                self.path = original_path
        elif hasattr(self, 'loader'):
            loader = self._load_loader_by_name(self.loader)
            documents = await loader.load(self.path)
        else:
            if isinstance(self.path, str) and self.path.startswith(
                ('http://', 'https://', 'ftp://')
            ):
                if 'youtube.com' in self.path or 'youtu.be' in self.path:
                    loader = self._load_loader_by_name('YoutubeLoader')
                    documents = await loader.load(self.path)
                else:
                    raise ComponentError(
                        f"ParrotLoader: URL type not supported: {self.path}"
                    )
            else:
                if self.path.is_dir():
                    documents = await self._load_directory(self.path)
                    if not documents:
                        raise FileNotFoundError(
                            f"ParrotLoader: No files found in {self.path}"
                        )
                elif self.path.is_file():
                    ext = self.path.suffix.lower()
                    if self.extensions and ext not in self.extensions:
                        raise FileNotFoundError(
                            f"ParrotLoader: {self.path} filtered out by extensions={self.extensions}"
                        )
                    if not set(self.path.parts).isdisjoint(self.skip_directories):
                        raise FileNotFoundError(
                            f"ParrotLoader: {self.path} in skip_directories"
                        )
                    loader = self._get_loader_by_extension(ext, source_path=self.path)
                    documents = await loader.load()
                else:
                    raise ValueError(
                        f"ParrotLoader: Invalid path: {self.path}"
                    )

        if documents:
            self._stamp_metadata(documents)
            doc = documents[0]
            print(
                f":: First Document ::\n  type: {type(doc).__name__}\n"
                f"  metadata: {doc.metadata}\n"
                f"  content: {doc.page_content[:200]}..."
            )

        self._result = documents
        self.add_metric('NUM_DOCUMENTS', len(documents))
        return True
