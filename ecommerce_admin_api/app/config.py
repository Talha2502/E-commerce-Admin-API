from pydantic import BaseSettings


class Settings(BaseSettings):
    # db stuff - change these with your local setup
    DB_HOST: str = "localhost"
    DB_PORT: str = "3306"
    DB_USER: str = "root" 
    DB_PASSWORD: str = "password"  # remember to change this!
    DB_NAME: str = "ecommerce_admin"
    
    # api config - might tweak this later
    API_PREFIX: str = "/api"
    APP_NAME: str = "E-commerce Admin API"
    
    class Config:
        env_file = ".env"


# just create once
settings = Settings()