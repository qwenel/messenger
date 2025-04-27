from sqlalchemy import (
    Column,
    String,
    Float,
    DateTime,
    Integer,
)

from datetime import datetime
from sqlalchemy.orm import Mapped

from sqlalchemy import ForeignKey

from app.database.db import BASE


class Chat(BASE):
    __tablename__ = "chat"

    id: Mapped[int] = Column(Integer, primary_key=True, unique=True, index=True)

    chat_type: Mapped[str] = Column(String(20), nullable=False)
    chat_name: Mapped[str] = Column(String(45), nullable=False)

    created_at: Mapped[datetime] = Column(DateTime, nullable=False)

    async def create(self, session):
        session.add(self)
        await session.commit()
        await session.refresh(self)
        return self

    # @staticmethod
    # async def get_by_hash(session, declaration_hash: str) -> "Declaration":
    #     query = select(Declaration).where(Declaration.declaration_hash == declaration_hash)
    #     result = await session.scalar(query)
    #     return result
    #
    # @staticmethod
    # async def get_by_id(session, declaration_id: uuid.UUID) -> "Declaration":
    #     query = select(Declaration).where(Declaration.id == declaration_id)
    #     result = await session.scalar(query)
    #     return result


class User(BASE):
    __tablename__ = "user"

    id: Mapped[str] = Column(String, primary_key=True, unique=True, index=True)

    username: Mapped[str] = Column(String(50), nullable=False)
    email: Mapped[str] = Column(String(320), nullable=True)
    password: Mapped[str] = Column(String(20), nullable=False)
    avatar_url: Mapped[str] = Column(String(45), nullable=True)

    created_at: Mapped[datetime] = Column(DateTime, nullable=False)

    async def create(self, session):
        session.add(self)
        await session.commit()
        await session.refresh(self)
        return self


class ChatToUser(BASE):
    __tablename__ = "chat_to_user"

    id: Mapped[int] = Column(Integer, primary_key=True, unique=True, index=True)

    fk_user_id: Mapped[str] = Column(String, ForeignKey("user.id"))
    fk_chat_id: Mapped[int] = Column(Integer, ForeignKey("chat.id"))
    fk_role_id: Mapped[int] = Column(Integer, ForeignKey("role.id"))

    created_at: Mapped[datetime] = Column(DateTime, nullable=False)

    async def create(self, session):
        session.add(self)
        await session.commit()
        await session.refresh(self)
        return self


class Message(BASE):
    __tablename__ = "message"

    id: Mapped[int] = Column(Integer, primary_key=True, unique=True, index=True)

    content: Mapped[str] = Column(String, nullable=False)
    status: Mapped[str] = Column(String(20), nullable=False)
    sender_user_id: Mapped[str] = Column(String, nullable=False)

    created_at: Mapped[datetime] = Column(DateTime, nullable=False)

    fk_chat_id: Mapped[int] = Column(Integer, ForeignKey("chat.id"))

    async def create(self, session):
        session.add(self)
        await session.commit()
        await session.refresh(self)
        return self


class Role(BASE):
    __tablename__ = "role"

    id: Mapped[int] = Column(Integer, primary_key=True, unique=True, index=True)

    name: Mapped[str] = Column(String(45), nullable=False)

    created_at: Mapped[datetime] = Column(DateTime, nullable=False)

    async def create(self, session):
        session.add(self)
        await session.commit()
        await session.refresh(self)
        return self


class Attachment(BASE):
    __tablename__ = "attachment"

    id: Mapped[int] = Column(Integer, primary_key=True, unique=True, index=True)

    file_name: Mapped[str] = Column(String(45), nullable=False)
    file_type: Mapped[str] = Column(String(10), nullable=False)
    file_size: Mapped[float] = Column(Float, nullable=True)
    file_url: Mapped[str] = Column(String(200), nullable=True)

    fk_message_id: Mapped[int] = Column(Integer, ForeignKey("message.id"))

    async def create(self, session):
        session.add(self)
        await session.commit()
        await session.refresh(self)
        return self
