import requests
from requests import auth
from requests.auth import HTTPBasicAuth
import json


class harbor:
    def __init__(self, provider):
        host = provider["host"]
        user = provider["user"]
        pwd = provider["pwd"]

        self.auth = HTTPBasicAuth(user, pwd)
        self.headers = {"content-type": "application/json"}
        self.baseURL = f"https://{host}/api/v2.0"

    def getProjects(self):
        url = f"{self.baseURL}/replication/policies"
        response = requests.request(
            "GET", url, headers=self.headers, auth=self.auth, verify=False
        )
        return json.loads(response.text)

    def getRegistry(self, registry):
        url = f"{self.baseURL}/registries/{registry}"
        response = requests.request(
            "GET", url, headers=self.headers, auth=self.auth, verify=False
        )
        return json.loads(response.text)

    def createReplicationPolicy(self, policy):
        url = f"{self.baseURL}/replication/policies"
        response = requests.request(
            "POST", url, headers=self.headers, auth=self.auth, verify=False, data=json.dumps(policy)
        )
        return json.loads(response.text)

    def executeReplicationPolicy(self, policy_id):
        url = f"{self.baseURL}/replication/executions"
        response = requests.request(
            "POST", url, headers=self.headers, auth=self.auth, verify=False, data=json.dumps(policy_id)
        )
        return json.loads(response.text)