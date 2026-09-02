from aws_glue_interactive_sessions_kernel.glue_kernel_utils.GlueSessionsConstants import SESSION_TYPE
from ..glue_kernel_base.BaseKernel import BaseKernel
from ..glue_kernel_utils.GlueSessionsConstants import SessionType


class GlueKernel(BaseKernel):
    implementation = "Scala Glue Session"
    implementation_version = "1.0"
    language = "no-op"
    language_version = "0.1"
    language_info = {
        "name": "scala",
        "mimetype": "text/x-scala",
        "codemirror_mode": "text/x-scala",
        "pygments_lexer": "scala",
    }
    session_language = "scala"

    def __init__(self, **kwargs):
        self.request_origin = "GlueSparkKernel"
        super(GlueKernel, self).__init__(**kwargs)

    def _set_default_arguments(self):
        self.default_arguments = {
            "--glue_kernel_version": self._get_current_kernel_version("aws-glue-sessions"),
            "--session-language": "scala",
            "--enable-glue-datacatalog": "true",
        }

    def set_python_version(self, python_version):
        pass

    def set_session_type(self, session_type):
        setattr(self.overrides, SESSION_TYPE, session_type)

if __name__ == "__main__":
    from ipykernel.kernelapp import IPKernelApp

    IPKernelApp.launch_instance(kernel_class=GlueKernel)
