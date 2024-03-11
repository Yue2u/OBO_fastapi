from sqlmodel import SQLModel, Field, Relationship


class Message(SQLModel, table=True):
    id: int
    text: str
    sender_id: int

    chat_id: int = Field(foreign_key="chatroom.id")
    chat = Relationship(back_populates="messages")


class Chatroom(SQLModel, table=True):
    id: int
    deal_id: int = Field(foreign_key="deal.id")

    messages: list[Message] = Relationship(back_populates="chat")
    deal: "Deal" = Relationship(back_populates="chat")
