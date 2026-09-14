from ...imports import (
    imports,
    os,
    logging,
    get_args,
    load_dotenv,
    jsonify,
    secure_filename,
    read_from_file,
    write_to_file,
    get_text_or_read,
    eatAll,
    eatInner,
    eatElse,
    clean_line,
    if_none_change,
    if_none_default,
    get_true_globals,
    get_initial_caller_dir,
    get_caller_path,
    get_caller_dir,
    make_list,
    get_file_parts,
    is_number,
    collect_filepaths,
    collect_globs,
    get_shortest_path,
    get_common_root,
    get_logFile,
    IMPORT_TAG,
    FROM_TAG,
    is_line_import,
    is_line_group_import,
    is_from_line_group,
    get_unique_name,
)
nullProxy_logger = logging.getLogger("abstract.lazy_import")


class nullProxy:
    """
    Safe, chainable, callable placeholder for missing modules/attributes.
    """

    def __init__(self, name, path=(),fallback=None):
        self._name = name
        self._path = path
        self.fallback=fallback
    def __getattr__(self, attr):
        return nullProxy(self._name, self._path + (attr,))

    def __call__(self, *args, **kwargs):
        if self.fallback is not None:
            try:
                return self.fallback(*args, **kwargs)
            except Exception as e:
                logger.info(f"{e}")
        nullProxy_logger.warning(
            "[lazy_import] Call to missing module/attr: %s.%s args=%s kwargs=%s",
            self._name,
            ".".join(self._path),
            args,
            kwargs,
        )
        return None

    def __repr__(self):
        full = ".".join((self._name, *self._path))
        return f"<nullProxy {full}>"

    def __bool__(self):
        return False  # safe in conditionals
