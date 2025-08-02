from swimlane_connector_exceptions import InvalidInput
from .asset_debugger import AssetDebugger

import base64

from datetime_parser import is_datetime


def create_attachment(filename, raw_data):
    """Easy way to create a single attachment. To create multiple attachments under a single key, use SwimlaneAttachment()
    
    Args:
        filename: filname of the attachment
        raw_data: raw data of the file (pre-base64)
    
    Returns:
        JSON data suitable for a key output in Swimlane

    """
    swa = SwimlaneAttachments()
    swa.add_attachment(filename, raw_data)
    return swa.get_attachments()


class SwimlaneAttachments(object):
    """Swimlane Attachment Manager Class"""
    
    def __init__(self):
        self.attachments = []

    def add_attachment(self, filename, raw_data):
        """Add an attachment to 

        Args:
            filename: Name of the file
            raw_data: Raw, pre-base64 data to encode

        """
        if isinstance(raw_data, str) and not isinstance(raw_data, bytes):  # Needed for python3 support
            raw_data = raw_data.encode()

        file_data = base64.b64encode(raw_data)
        if isinstance(file_data, bytes):
            # In python3, b64encode returns a bytes object.  Platform cant handle this because it isn't JSON
            #  serializable, so we convert it to a string.
            file_data = file_data.decode("ascii")

        self.attachments.append({
            "filename": filename,
            "base64": file_data
        })
        
    def get_attachments(self):
        """Get attachments fit for a key output in Swimlane

        Examples:
            All files to key "output_files"::
            
                >>>swa = SwimlaneAttachments()
                >>>swa.add_attachment("myfile.txt", "asdf")
                >>>output["output_files"] = swa.get_attachments()

        Returns:
            Attachments for output in a key in Swimlane

        """
        return self.attachments


def create_test_conn(base_cls, execute_func=None, custom_test_funcs=[]):
    """Create a test connection base class

    Examples:
        Create a basic integration for MyIntegration::
            >>>SwMain = create_test_conn(MyIntegration)
        Create a basic integration for MyIntegration with auth function name "auth"
            >>>SwMain = create_test_conn(MyIntegration, "auth")
        Create a basic integration for MyIntegration with custom test functions
            >>>SwMain = create_test_conn(MyIntegration, custom_test_funcs=[custom_func_1, custom_func_2])
            see quickstart for appropriate test function signatures

    Args:
        base_cls: a Classtype of the ABCIntegration
        execute_func: the name of the function to call during execute, such as 'login'

    Returns:
        TestConnection class

    """

    class SwMain(object):
        def __init__(self, context):
            self.context = context

        def execute(self):
            try:
                c = base_cls(self.context)
                if execute_func:
                    getattr(c, execute_func)()
                return {"successful": True}
            except Exception as e:
                message = e
                try:
                    message = AssetDebugger(asset=self.context.asset,
                                            test_conn_exception=e,
                                            custom_tests=custom_test_funcs).results
                except Exception as ex:
                    pass
                return {"successful": False, "errorMessage": str(message)}
    return SwMain


def parse_datetime(param_name, param_value):
    """
    :param val: A string representing a datetime.
    This can be any standard datetime format supported by pendulum or a relative datetime.
    Relative datetime format:
        For the current time:
            now
        Any other time:
            (+/-)(integer) (milliseconds|seconds|minutes|days|weeks|months|years)
    examples:
        now
        -1 months
        +3 days
        -123 seconds

    :return: a pendulum object for the datetime
    """
    datetime = is_datetime(param_value)
    if datetime is None:
        raise InvalidInput("Unknown datetime format",
                           input_name=param_name,
                           input_value=param_value)
    return datetime
