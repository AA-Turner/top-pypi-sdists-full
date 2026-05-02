import asyncio
import importlib
import inspect
import logging
import pkgutil
from typing import List, Optional, Union
from collections.abc import Callable
from pathlib import Path
from tqdm import tqdm
from parrot.loaders import AbstractLoader, Document
from parrot_loaders.factory import get_loader_class, LOADER_MAPPING

try:
    from parrot_loaders import LOADER_REGISTRY  # name -> "module.Class"
except ImportError:
    LOADER_REGISTRY = {}

logging.getLogger("pdfminer").setLevel(logging.WARNING)
from ..flow import FlowComponent
from ...conf import BASE_DIR
from ...exceptions import ConfigError, ComponentError


DEFAULT_SCRAPING_PLANS_DIR = BASE_DIR.joinpath("artifacts", "scraping_plans")


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
        self._chunk_size = kwargs.get('chunk_size', 2048)
        self.source_type: str = kwargs.pop('source_type', 'document')
        self.doctype: str = kwargs.pop('doctype', 'document')
        self.category: str = kwargs.pop('category', 'document')
        # LLM provider name (string) or pre-built client instance.
        self._llm = kwargs.pop('llm', None)
        self._llm_model = kwargs.pop('llm_model', None)
        # Table settings for PDFTablesLoader
        self.table_settings = kwargs.pop('table_settings', {})
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
        
        # Check if path comes from previous component (like FileList)
        if not self.path and self.previous and self.input:
            # Handle input from previous component (FileList passes filename in kwargs)
            filename = kwargs.get('filename')
            if filename:
                self.path = filename
                print(f"ParrotLoader: Received file from previous component: {self.path}")
            else:
                # Fallback: try to use input directly
                self.path = self.input
                print(f"ParrotLoader: Using input as path: {self.path}")
        
        if self.path:
            if isinstance(self.path, str):
                self.path = self.mask_replacement_recursively(self.path)
                # Check if it's a URL (for video loaders like YouTube)
                if self.path.startswith(('http://', 'https://', 'ftp://')):
                    # For URLs, keep as string - don't convert to Path
                    print(f"Loading from URL: {self.path}")
                else:
                    # For local files, convert to Path and validate existence
                    self.path = Path(self.path).resolve()
                    if not self.path.exists():
                        raise ComponentError(
                            f"ParrotLoader: {self.path} doesn't exist."
                        )
            elif isinstance(self.path, Path):
                # Already a Path object (from FileList)
                if not self.path.exists():
                    raise ComponentError(
                        f"ParrotLoader: {self.path} doesn't exist."
                    )
        else:
            raise ConfigError(
                "Provide at least one directory or filename in *path* attribute or ensure previous component provides input."
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
        documents = []

        if hasattr(self, 'loader'):
            # Use specific loader by name
            loader = self._load_loader_by_name(self.loader)
            documents = await loader.load(self.path)
        else:
            # Check if path is a URL or file/directory
            if isinstance(self.path, str) and self.path.startswith(('http://', 'https://', 'ftp://')):
                # For URLs, we need to determine the appropriate loader
                # For now, assume YouTube for youtube.com URLs
                if 'youtube.com' in self.path or 'youtu.be' in self.path:
                    loader = self._load_loader_by_name('YoutubeLoader')
                    documents = await loader.load(self.path)
                else:
                    raise ComponentError(
                        f"ParrotLoader: URL type not supported: {self.path}"
                    )
            else:
                # Use automatic loader detection by file extension for local files
                _file_buckets = {}
                if self.path.is_dir():
                    # Process directory
                    if self.extensions:
                        # Process specific extensions
                        for ext in self.extensions:
                            for item in self.path.glob(f'*{ext}'):
                                if item.is_file() and set(item.parts).isdisjoint(self.skip_directories):
                                    ext = item.suffix.lower()
                                    _file_buckets.setdefault(ext, []).append(item)
                    else:
                        # Process all files
                        for item in self.path.glob('*.*'):
                            if item.is_file() and set(item.parts).isdisjoint(self.skip_directories):
                                ext = item.suffix.lower()
                                _file_buckets.setdefault(ext, []).append(item)
                elif self.path.is_file():
                    # Process single file
                    ext = self.path.suffix.lower()
                    if not self.extensions or ext in self.extensions:
                        if set(self.path.parts).isdisjoint(self.skip_directories):
                            _file_buckets.setdefault(ext, []).append(self.path)
                else:
                    raise ValueError(
                        f"ParrotLoader: Invalid path: {self.path}"
                    )
                if not _file_buckets:
                    raise FileNotFoundError(
                        f"ParrotLoader: No files found in {self.path}"
                    )
                total_files = sum(len(f) for f in _file_buckets.values())
                with tqdm(total=total_files, desc="ParrotLoader", unit="file") as pbar:
                    for ext, files in _file_buckets.items():
                        for file in files:
                            try:
                                loader = self._get_loader_by_extension(ext, source_path=file)
                                docs = await loader.load()
                                documents.extend(docs)
                            except ComponentError as ce:
                                print(f"Warning: {ce}")
                            pbar.update(1)

        if documents:
            self._stamp_metadata(documents)
            doc = documents[0]
            print(f":: First Document ::\n  type: {type(doc).__name__}\n  metadata: {doc.metadata}\n  content: {doc.page_content[:200]}...")

        self._result = documents
        self.add_metric('NUM_DOCUMENTS', len(documents))
        return True
