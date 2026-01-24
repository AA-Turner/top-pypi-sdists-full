import chalk


class MissingDependencyException(ImportError):
    ...


def missing_dependency_exception(name: str, original_error: Exception | None = None):
    msg = f"Missing pip dependency '{name}' for chalkpy=={chalk.__version__}. Please add this to your requirements.txt file and pip install."
    if original_error:
        msg += f"\n\n{original_error}"
    return MissingDependencyException(msg)
