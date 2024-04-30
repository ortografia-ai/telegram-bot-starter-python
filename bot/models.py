import enum
import datetime
from functools import lru_cache

from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel, Enum, create_engine

from bot.settings import get_settings


class UserRole(int, enum.Enum):
    OWNER = 0
    ADMIN = 1
    USER = 2


class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str | None = None
    user_role: UserRole = Field(
        sa_column_args=[Enum(UserRole)], default=UserRole.USER, nullable=False
    )
    created_at: datetime.datetime = Field(
        default_factory=lambda: datetime.datetime.now(datetime.UTC),
    )
    updated_at: datetime.datetime = Field(
        sa_column=Column(
            DateTime(),
            default=lambda: datetime.datetime.now(datetime.UTC),
            onupdate=lambda: datetime.datetime.now(datetime.UTC),
            nullable=False,
        )
    )


@lru_cache
def get_engine():
    settings = get_settings()
    sqlite_url = f"sqlite:///{settings.db_path}"
    engine = create_engine(sqlite_url)
    return engine
