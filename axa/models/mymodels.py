import re

from pydantic import BaseModel, Field, field_validator, computed_field
from typing import Optional, Dict, Any

class ResponseModel(BaseModel):
  data: Any

class NotFoundModel(BaseModel):
  message: str = "Customer or policy not found"


class NoAccess(BaseModel):
  message: str = "Sorry but your user is not an admin"


class ApiNotValid(BaseModel):
  error: str = "This method is not valid"


class Client(BaseModel):
    id: str
    name: str
    email: str
    role: str


class Policies(BaseModel):
    id: str
    amountInsured: float
    email: str
    inceptionDate: str
    installmentPayment: bool
    clientId: str

class ClientsBase(BaseModel):
    clients: Dict[str, Client]

    def __iter__(self):
        return iter(self.clients)

    def __getitem__(self, item):
        try:
            return self.clients[item]
        except:
            return NotFoundModel()
    
class PolicyBase(BaseModel):
    policies: Dict[str, Policies]

    def __iter__(self):
        return iter(self.policies)

    def __getitem__(self, item):
        try:
            return self.policies[item]
        except:
            return NotFoundModel()


class ValidateMode(BaseModel):
    mode: str
    
    @computed_field
    @property
    def valid(self) -> bool:
        if self.mode in ["id", "name"]:
            return True
        else:
            return False
        

"""    
    @field_validator("cf_driver426551")
    def check_fleet(cls, value):
        if value is None:
            return "NO DRIVER"
        else:
            return value
        
    @computed_field
    @property
    def cf_category_cs_escalations(self) -> bool:
        return map_categories(categories, self.cf_contact_reason, self.cf_reason_details, self.cf_outcome)
"""