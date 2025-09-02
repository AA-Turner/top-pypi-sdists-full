class Issue:
    def __init__(self, category: str, statefulset: str = None, namespace: str = None, pod: str = None, host: str = None, desc: str = None, details: str = None, suggestion: str = None):
        self.statefulset = statefulset
        self.namespace = namespace
        self.pod = pod
        self.host = host
        self.category = category
        self.desc = desc
        self.details = details
        self.suggestion = suggestion

    def to_dict(self):
        return self.__dict__