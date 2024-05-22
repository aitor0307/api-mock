from models.mymodels import Client, NoAccess
import requests
import pandas as pd

class DDBB():
    def __init__(self):
        """Initialize a DDBB with the objets from the request"""
        r = requests.get("https://run.mocky.io/v3/532e77dc-2e2d-4a0c-91fd-5ea92ff5d615")
        self.clients = pd.DataFrame(r.json())
        r = requests.get("https://run.mocky.io/v3/289c72a0-8190-4a15-9a15-4118dc2fbde6")
        self.policies = pd.DataFrame(r.json())

    def retrieve_user(self, mode, user) -> Client:
        t = self.clients.set_index(mode).loc[user].to_dict()
        t[mode] = user
        return Client(**t)

    def retrieve_policy(self, policynumber) -> Client:
        userid = self.policies.set_index("id").loc[policynumber].clientId
        customer = self.retrieve_user("id", userid)
        if customer.role == "admin":
            return customer
        else:
            return NoAccess()
    
    def retrieve_user_policies(self, mode, user, output = "json"):
        t = self.clients.set_index(mode).loc[user].to_dict()
        t[mode] = user
        customer = Client(**t)
        if customer.role == "admin":
            return (self.policies.set_index("clientId").loc[customer.id].to_json(orient="records"), "application/json") if output == "json" else (self.policies.set_index("clientId").loc[customer.id].to_html(), "text/html")
        else:
            return NoAccess().model_dump_json(), "application/json"
        
