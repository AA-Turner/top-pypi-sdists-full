import z3c.form.converter
import z3c.form.interfaces
import zope.publisher.browser
import ZPublisher.HTTPRequest


class _SimpleFieldStorage:
    """Replacement for cgi.FieldStorage.

    The cgi module is deprecated and will be removed in Python 3.13.
    This simple class implements only what is needed for the converter below.
    """

    def __init__(self, value):
        self.file = value
        self.headers = value.headers
        self.filename = value.filename


class FileUploadDataConverter(z3c.form.converter.FileUploadDataConverter):
    """Although ZPublisher's and zope.publisher's FileUpload
    implementations are almost identical, ``FileUploadDataConverter``
    makes an ``isinstance`` call that breaks duck-typing.

    Therefore, we override the stock ``FileUploadDataConverter`` with
    this little class that will do the right thing when a Zope 2
    FileUpload object is received.
    """

    def toFieldValue(self, value):
        """See interfaces.IDataConverter"""
        if isinstance(value, ZPublisher.HTTPRequest.FileUpload):
            fieldstorage = _SimpleFieldStorage(value)
            value = zope.publisher.browser.FileUpload(fieldstorage)

        return super().toFieldValue(value)
