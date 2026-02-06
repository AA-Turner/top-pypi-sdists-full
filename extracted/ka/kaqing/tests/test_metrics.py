from kubernetes import client, config

# Load the kube config
config.load_kube_config()

# Create an API object for accessing custom objects (like metrics)
api = client.CustomObjectsApi()

# Specify the metrics API group, version, namespace, and plural
group = "metrics.k8s.io"
version = "v1beta1"
namespace = "azops88"  # Replace with your namespace
plural = "pods"

# List namespaced custom objects (pods with metrics)
try:
    resource = api.list_namespaced_custom_object(group=group, version=version, namespace=namespace, plural=plural)

    # Extract and print CPU usage for each container in each pod
    for pod in resource["items"]:
        print(f'Pod name: {pod["metadata"]["name"]}')
        for container in pod["containers"]:
            usage = container["usage"]
            cpu_usage = usage["cpu"]
            print(f'\tContainer name: {container["name"]}, CPU Usage: {cpu_usage}')

            memory_usage = container['usage']['memory']
            print(f"Container: {container['name']}, Memory Usage: {memory_usage}")
            # node_name = container["metadata"]["name"]
            # memory_usage = container["usage"]["memory"]
            # print(f"Node {node_name} has memory usage of {memory_usage}")

    # response = api.list_cluster_custom_object("metrics.k8s.io", "v1beta1", "nodes")
    # for node in response["items"]:
    #     node_name = node["metadata"]["name"]
    #     memory_usage = node["usage"]["memory"]
    #     print(f"Node {node_name} has memory usage of {memory_usage}")

except Exception as e:
    print(f"Error accessing metrics API: {e}")