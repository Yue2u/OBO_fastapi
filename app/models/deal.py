from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

from app.models.user import User, UserRead


class DealBase(SQLModel):
    title: str
    description: Optional[str] = None
    value: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    creator_id: int
    status: str = Field(default="active")  # One of active, successful, denied


class Deal(DealBase, table=True):
    id: int = Field(default=None, primary_key=True)
    chat_id: Optional[int] = Field(default=None, foreign_key="chatroom.id")

    chat: "Chatroom" = Relationship(back_populates="deal")
    users: list[User] = Relationship(back_populates="deals")


class DealRead(DealBase):
    id: int
    users: list[UserRead] = []


class DealCreate(SQLModel):
    title: str
    description: Optional[str] = None
    value: Optional[float] = None


class DealUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    value: Optional[float] = None
    created_at: Optional[datetime] = None
    users: Optional[list[User]] = None
