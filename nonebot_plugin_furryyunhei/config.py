from pydantic import BaseModel, field_validator

class Config(BaseModel):
    yunhei_api_key: str
