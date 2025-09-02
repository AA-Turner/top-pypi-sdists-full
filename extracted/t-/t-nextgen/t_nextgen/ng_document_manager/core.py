"""NgDocumentManager module."""

from t_nextgen.ng_app_manager import NGAppManager


class NgDocumentManager(NGAppManager):
    """NgDocumentManager class."""

    def launch_doc_management(self, skip_errors: bool = False) -> None:
        """Launch the Doc Management application."""
        raise NotImplementedError

    def close_document_management_window(self) -> None:
        """This function clears out windows on Document Management."""
        raise NotImplementedError()

    def close_digital_image_function(self) -> None:
        """This function clears out Digital Image windows."""
        raise NotImplementedError()
