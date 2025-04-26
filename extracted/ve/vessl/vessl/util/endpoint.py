from vessl.util.constant import WEB_HOST


class Endpoint:
    cluster = WEB_HOST + "/{}/clusters/{}"  # Orgainzation name, cluster ID
    dataset = WEB_HOST + "/{}/datasets/{}"  # Organization name, dataset name
    experiment = (
        WEB_HOST + "/{}/{}/experiments/{}"
    )  # Organization name, project name, experiment number
    experiment_logs = (
        WEB_HOST + "/{}/{}/experiments/{}/logs"
    )  # Organization name, project name, experiment number
    run = WEB_HOST + "/{}/runs/{}/{}"
    model_repository = WEB_HOST + "/{}/models/{}"  # Organization name, repository name
    model = WEB_HOST + "/{}/models/{}/{}"  # Organization name, repository name, number
    organization = WEB_HOST + "/{}"  # Organization name
    project = WEB_HOST + "/{}/{}"  # Organization name, project name
    sweep = WEB_HOST + "/{}/{}/sweeps/{}"  # Organization name, project name, sweep name
    sweep_logs = WEB_HOST + "/{}/{}/sweeps/{}/logs"  # Organization name, project name, sweep name
    workspace = WEB_HOST + "/{}/workspaces/{}"  # Organization name, workspace id
    service = WEB_HOST + "/{}/services/{}"  # Organization name, service name
