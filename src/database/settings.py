import os
from typing import AsyncGenerator
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker

from src.utils.singleton import Singleton


load_dotenv()


class PostgresSettings(metaclass=Singleton):
    def __init__(self) -> None:
        self.__user = os.getenv("POSTGRES_USER", "user")
        self.__password = os.getenv("POSTGRES_PASSWORD", "qwerty123")
        self.__host = os.getenv("POSTGRES_HOST", "db")
        self.__port = os.getenv("POSTGRES_PORT", "5432")
        self.__db = os.getenv("POSTGRES_DB", "pgdb")
        self.__url = (
            f"postgresql+asyncpg://{self.__user}:{self.__password}@"
            f"{self.__host}:{self.__port}/{self.__db}"
        )
        self.__engine = create_async_engine(self.__url, echo=False)

    @property
    def url(self) -> str:
        return self.__url

    @property
    def engine(self) -> AsyncEngine:
        return self.__engine


db_settings = PostgresSettings()


AsyncSessionLocal = sessionmaker(  # type: ignore
    bind=db_settings.engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
