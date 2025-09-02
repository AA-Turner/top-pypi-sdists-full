class CheckContext:
    def __init__(self, statefulset: str = None, host_id: str = None, pod: str = None, namespace: str = None, user: str = None, pw: str = None, show_output: bool = True):
        self.statefulset = statefulset
        self.host_id = host_id
        self.pod = pod
        self.namespace = namespace
        self.user = user
        self.pw = pw
        self.show_output = show_output