from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Central place for all environment-driven config.
    Values are read from a .env file (see .env.example) or real
    environment variables — never hardcode secrets here.
    """

    # MySQL connection
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_NAME: str = "school_db"

    # JWT auth
    JWT_SECRET_KEY: str = "change-me-in-.env"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    @property
    def DATABASE_URL(self) -> str:
        # mysqlconnector is the driver; PyMySQL also works if you prefer
        return (
            f"mysql+mysqlconnector://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    class Config:
        env_file = ".env"


settings = Settings()
