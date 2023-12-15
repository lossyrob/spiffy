# spiffy/config.py
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    client_id: str
    client_secret: str
    redirect_uri: str
    user_id: str

    class Config:
        env_file = ".env"
        env_prefix = "SPIFFY_"
