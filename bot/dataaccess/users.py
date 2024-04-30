from typing import Sequence

from sqlmodel import Session, select

from bot.models import get_engine, User


def create_or_update_user(user: User) -> User:
    engine = get_engine()
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
    return user


def get_user(id: int) -> User | None:
    engine = get_engine()
    with Session(engine) as session:
        user = session.get(User, id)
    return user


def get_all_users() -> Sequence[User]:
    engine = get_engine()
    with Session(engine) as session:
        statement = select(User).where()
        users = session.exec(statement).all()
    return users


def delete_user(user_id: int) -> None:
    engine = get_engine()
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise ValueError("User not found")
        session.delete(user)
        session.commit()
