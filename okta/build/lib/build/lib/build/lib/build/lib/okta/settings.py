from pydantic import BaseModel


class OktaSettings(BaseModel):
    account_id: str
