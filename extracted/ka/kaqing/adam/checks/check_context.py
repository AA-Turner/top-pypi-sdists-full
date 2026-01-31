from adam.utils_context import Context

class CheckContext(Context):
    def __init__(self, statefulset: str = None, host_id: str = None, pod: str = None, namespace: str = None, user: str = None, pw: str = None, verbose: bool = True):
        super().__init__(None, show_out=verbose)
        self.statefulset = statefulset
        self.host_id = host_id
        self.pod = pod
        self.namespace = namespace
        self.user = user
        self.pw = pw

    def from_exec(ctx: Context, sts: str = None, host_id: str = None, pod: str = None, namespace: str = None, user: str = None, pw: str = None):
        ctx1 = CheckContext(statefulset=sts,
                            host_id=host_id,
                            pod=pod,
                            namespace=namespace,
                            user=user,
                            pw=pw)

        ctx1.cmd=ctx.cmd
        ctx1.background=ctx.background
        ctx1.show_out=ctx.show_out
        ctx1.text_color=ctx.text_color
        ctx1.show_verbose=ctx.show_verbose
        ctx1.history=ctx.history
        ctx1.debug=ctx.debug
        ctx1.log_file=ctx.log_file
        ctx1._histories=ctx._histories
        ctx1.job_id=ctx.job_id
        ctx1._pod_log_file=ctx._pod_log_file

        return ctx1