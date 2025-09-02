import click

from adam.utils import log

class ClusterCommandHelper(click.Command):
    def get_help(self, ctx: click.Context):
        log(super().get_help(ctx))
        log()

        ClusterCommandHelper.cluster_help()

    def cluster_help():
        log('Cluster:  Kubernetes statefulset for Cassandra cluster, optionally namespaced with @<namespace>')
        log('          e.g. cs-d0767a536f-cs-d0767a536f-default-sts@gkeops845')

class PodCommandHelper(click.Command):
    def get_help(self, ctx: click.Context):
        log(super().get_help(ctx))
        log()

        PodCommandHelper.pod_help()

    def pod_help():
        log('Pod:      Kubernetes pod for Cassandra node, optionally namespaced with @<namespace>')
        log('          e.g. cs-d0767a536f-cs-d0767a536f-default-sts-0@gkeops845')

class ClusterOrPodCommandHelper(click.Command):
    def get_help(self, ctx: click.Context):
        log(super().get_help(ctx))
        log()

        ClusterOrPodCommandHelper.cluter_or_pod_help()

    def cluter_or_pod_help():
        ClusterCommandHelper.cluster_help()
        log()
        PodCommandHelper.pod_help()