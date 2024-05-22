from models.mymodels import Client, ClientsBase, PolicyBase, Policies
import requests
import pandas as pd

class DDBB():
    def __init__(self):
        """Initialize a DDBB with the objets from the request"""
        r=requests.get("https://run.mocky.io/v3/532e77dc-2e2d-4a0c-91fd-5ea92ff5d615")
        self.clients = pd.DataFrame(r.json())
        r=requests.get("https://run.mocky.io/v3/289c72a0-8190-4a15-9a15-4118dc2fbde6")
        self.policies = pd.DataFrame(r.json())

    def retrieve_user(self, mode, user) -> Client:
        t = self.clients.set_index(mode).loc[user].to_dict()
        t[mode] = user
        return Client(**t)

    def retrieve_policy_user(self, policynumber) -> Client:
        userid = self.policies.set_index("id").loc[policynumber].clientId
        return self.retrieve_user("id", userid)
    
    def retrieve_user_policies(self, mode, user):
        t = self.clients.set_index(mode).loc[user].to_dict()
        t[mode] = user
        customer = Client(**t)
        return self.policies.set_index("clientId").loc[customer.id]
