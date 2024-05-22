import re

from pydantic import BaseModel, Field, field_validator, computed_field
from typing import Optional, Dict

class ResponseModel(BaseModel):
  id: str
  age: int
  name: str
  nickname: Optional[str] = None

class NotFoundModel(BaseModel):
  message: str = "Not found"

class ApiNotValid(BaseModel):
  message: str = "This method is not valid"

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