from kubernetes import client, config

from adam.config import Config

# utility collection on service accounts; methods are all static
class ServiceAccounts:
    def delete(namespace: str, label_selector: str):
        ServiceAccounts.delete_cluster_role_bindings(label_selector)
        ServiceAccounts.delete_role_bindings(namespace, label_selector)
        ServiceAccounts.delete_service_account(namespace, label_selector)

    def replicate(to_sa: str, namespace: str, from_sa: str, labels: dict[str, str] = {}, add_cluster_roles: list[str] = []):
        ServiceAccounts.create_service_account(to_sa, namespace, labels=labels)
        for b in ServiceAccounts.get_role_bindings(from_sa, namespace):
            n = f'{to_sa}-{b.role_ref.name}'
            ServiceAccounts.create_role_binding(n, namespace, to_sa, b.role_ref.name, labels=labels)

        for b in ServiceAccounts.get_cluster_role_bindings(from_sa):
            n = f'{to_sa}-{b.role_ref.name}'
            ServiceAccounts.create_cluster_role_binding(n, namespace, to_sa, b.role_ref.name, labels=labels)

        for cr in add_cluster_roles:
            n = f'{to_sa}-{cr}'
            ServiceAccounts.create_cluster_role_binding(n, namespace, to_sa, cr, labels=labels)

    def create_service_account(name: str, namespace: str, labels: dict[str, str] = {}):
        config.load_kube_config()

        v1 = client.CoreV1Api()

        service_account = client.V1ServiceAccount(
            metadata=client.V1ObjectMeta(
                name=name,
                labels=labels)
        )
        api_response = v1.create_namespaced_service_account(
            namespace=namespace,
            body=service_account
        )
        Config().debug(f"Service Account '{api_response.metadata.name}' created in namespace '{namespace}'.")

    def delete_service_account(namespace: str, label_selector: str) -> list:
        refs = []

        v1 = client.CoreV1Api()
        sas = v1.list_namespaced_service_account(namespace=namespace, label_selector=label_selector).items
        for sa in sas:
            Config().debug(f'delete {sa.metadata.name}')
            v1.delete_namespaced_service_account(name=sa.metadata.name, namespace=namespace)
            refs.append(sa)

        return refs

    def create_role_binding(name: str, namespace: str, sa_name: str, role_name: str, labels: dict[str, str] = {}):
        api = client.RbacAuthorizationV1Api()

        metadata = client.V1ObjectMeta(
            name=name,
            namespace=namespace,
            labels=labels
        )
        role_ref = client.V1RoleRef(
            api_group="rbac.authorization.k8s.io",
            kind="Role",
            name=role_name
        )

        subjects = [
            client.RbacV1Subject(
                kind="ServiceAccount",
                name=sa_name, # Name of the service account
                namespace=namespace # Namespace of the service account
            )
        ]

        role_binding = client.V1RoleBinding(
            api_version="rbac.authorization.k8s.io/v1",
            kind="RoleBinding",
            metadata=metadata,
            role_ref=role_ref,
            subjects=subjects
        )

        api.create_namespaced_role_binding(namespace=namespace, body=role_binding)

    def get_role_bindings(service_account_name: str, namespace: str) -> list:
        refs = []

        rbac_api = client.RbacAuthorizationV1Api()
        role_bindings = rbac_api.list_namespaced_role_binding(namespace=namespace)
        for binding in role_bindings.items:
            if binding.subjects:
                for subject in binding.subjects:
                    if subject.kind == "ServiceAccount" and subject.name == service_account_name:
                        refs.append(binding)

        return refs

    def delete_role_bindings(namespace: str, label_selector: str) -> list:
        refs = []

        v1_rbac = client.RbacAuthorizationV1Api()
        cluster_role_bindings = v1_rbac.list_namespaced_role_binding(namespace=namespace, label_selector=label_selector).items
        for binding in cluster_role_bindings:
            Config().debug(f'delete {binding.metadata.name}')
            v1_rbac.delete_namespaced_role_binding(name=binding.metadata.name, namespace=namespace)
            refs.append(binding)

        return refs

    def create_cluster_role_binding(name: str, namespace: str, sa_name: str, role_name: str, labels: dict[str, str] = {}):
        api = client.RbacAuthorizationV1Api()

        metadata = client.V1ObjectMeta(
            name=name,
            namespace=namespace,
            labels=labels
        )
        role_ref = client.V1RoleRef(
            api_group="rbac.authorization.k8s.io",
            kind="ClusterRole",
            name=role_name
        )

        subjects = [
            client.RbacV1Subject(
                kind="ServiceAccount",
                name=sa_name,
                namespace=namespace
            )
        ]

        role_binding = client.V1ClusterRoleBinding(
            api_version="rbac.authorization.k8s.io/v1",
            metadata=metadata,
            role_ref=role_ref,
            subjects=subjects
        )

        try:
            api.create_cluster_role_binding(body=role_binding)
        except client.ApiException as e:
            print(f"Error creating ClusterRoleBinding: {e}")

    def get_cluster_role_bindings(service_account_name: str) -> list:
        refs = []

        v1_rbac = client.RbacAuthorizationV1Api()
        cluster_role_bindings = v1_rbac.list_cluster_role_binding().items
        for binding in cluster_role_bindings:
            if binding.subjects:
                for subject in binding.subjects:
                    if subject.kind == "ServiceAccount" and subject.name == service_account_name:
                        refs.append(binding)

        return refs


    def delete_cluster_role_bindings(label_selector: str) -> list:
        refs = []

        v1_rbac = client.RbacAuthorizationV1Api()
        cluster_role_bindings = v1_rbac.list_cluster_role_binding(label_selector=label_selector).items
        for binding in cluster_role_bindings:
            Config().debug(f'delete {binding.metadata.name}')
            v1_rbac.delete_cluster_role_binding(binding.metadata.name)
            refs.append(binding)

        return refs