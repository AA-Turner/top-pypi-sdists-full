import unittest
from adam.repl_state import ReplState
from adam.utils_k8s import get_host_id, is_pod_name, is_sts_name, strip, to_tabular
from kubernetes import config as kconfig
import requests
import portforward

class TestReaper(unittest.TestCase):
    def _test_get_host_id(self):
        kconfig.load_kube_config(config_file='gkeops845-sa')

        # cmd = Status()
        state = ReplState(sts='cs-d0767a536f-cs-d0767a536f-default-sts',
                          pod = 'cs-d0767a536f-cs-d0767a536f-default-sts-0',
                          namespace = 'gkeops845'
        )
        user, pw = state.user_pass('reaper-ui')
        # cmd.run('status', state)

    def test_port_forward(self):
        namespace = "gkeops845"  # Replace with your namespace
        pod_name = "cs-d0767a536f-cs-d0767a536f-reaper-946969766-rws92"  # Replace with your pod name or service name
        local_port = 9000
        target_port = 8080

        with portforward.forward(namespace, pod_name, local_port, target_port):
            # Now you can access the service/pod via http://localhost:9000
            response = requests.post("http://localhost:9000/login", headers={
                'Accept': '*'
            },data={
                'username':'cs-d0767a536f-reaper-ui',
                'password':'1d1J00-aj4QohJ07D7G7',
                'rememberMe': 'true'})
            print(f"Status Code: {response.status_code}")
            # print(len(response.content))
            print(response.headers)
            cookie = response.headers['Set-Cookie']



            token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjcy1kMDc2N2E1MzZmLXJlYXBlci11aSIsImV4cCI6MTc1MDk2OTIyN30.La4vlaFjtVONZdWB_1Lt-S16R0xNR1Rqi5Ok4VEZx-I'
            response = requests.get("http://localhost:9000/cluster", headers={
                'Cookie': cookie
            })
            print(f"Status Code: {response.status_code}")
            print(response.headers)
            print(f"Response Text: {response.text[:100]}...")

            response = requests.get("http://localhost:9000/repair_schedule", headers={
                'Cookie': cookie
            }, params={
                'clusterName': 'cs-d0767a536f'
            })
            print(f"Status Code: {response.status_code}")
            print(response.headers)
            print(f"Response Text: {response.text}")


            # If the response is JSON:
            # try:
            #     data = response.json()
            #     print(f"JSON Data: {data}")
            # except ValueError:
            #     print("Response is not valid JSON.")
            #     print(f"Text Content: {response.text}")

            # response = requests.get("http://localhost:9000/jwt", headers={
            #     'Accept': '*'
            # })
            # print(f"Status Code: {response.status_code}")
            # print(response.headers)
            # print(f"Response Text: {response.text[:100]}...")

    def _test_port_forward(self):
        namespace = "gkeops845"  # Replace with your namespace
        pod_name = "cs-d0767a536f-cs-d0767a536f-reaper-946969766-rws92"  # Replace with your pod name or service name
        local_port = 9000
        target_port = 8080

        with portforward.forward(namespace, pod_name, local_port, target_port):
            # Now you can access the service/pod via http://localhost:9000
            # token = 'a95kPZEI3g+GxuGkTdwK1ES7WjGvZhYK0iEMnkPiMGQpTmyRs9GgEtwWPO1YTyRVPjAswIXB6kzhVTs3nncGqdkFdPDMUTc0kf+SJ9Afa9K4TuGHOZFCmrj/W6ZPv7btsJBL/rIfMYNvmZBA16OBUTfT55fBAGYztpcDdM/ynoCZsacmHdIiQLOAjIxSzkuUo7w/vW/gXRbDdXcp+zPMB26y6Yp17dZNE1DLox/rj7tVgXwlLYafoAdxzoO0JBCDQ4Wu4pu4N1ZmLeOQiRCDWtmAyzXCeiRdZNZMu6HfspODhDc+K7DiOCI2d/27KFyTmsEqvGkJ9/zZbM7U2KWqpOti9JuRALK1JMdeI8/GvmX1R2lvdR8uuhRR8qfQTWvxOB+rvNRIHXztkudDZA1fzW6ailAi8eEKXc5A5mx4SRBuJX9czJiBV7/Tt0S55laMMVD3KUhtLPT7EMxXk3Oj7kDYhr+VuhjUkvt0eOf+jC0OW7ilGsvMwrs9DJaUNjBD2Sc7CrlkPxxDEY6DpEV/J0MAiw=='
            token = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJjcy1kMDc2N2E1MzZmLXJlYXBlci11aSIsImV4cCI6MTc1MDk2OTIyN30.La4vlaFjtVONZdWB_1Lt-S16R0xNR1Rqi5Ok4VEZx-I'
            response = requests.get("http://localhost:9000/cluster", headers={
                'Authorization': f'Bearer {token}'
            })
            print(f"Status Code: {response.status_code}")
            print(response.headers)
            print(f"Response Text: {response.text[:100]}...")

if __name__ == '__main__':
    unittest.main()