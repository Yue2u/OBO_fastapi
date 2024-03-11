from typing import Optional

from passlib.context import CryptContext
from sqlmodel import SQLModel, Field, Relationship


class UserBase(SQLModel):
    name: str
    surname: str
    fathers_name: Optional[str]
    email: str = Field(unique=True, index=True, nullable=False)
    avatar_filename: Optional[str] = None
    is_verified: bool = False


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    is_superuser: bool = False
    hashed_password: str = Field(nullable=False)

    deals: list["Deal"] = Relationship(back_populates="users")

    @staticmethod
    def hash_password(password: str):
        """Encrypt password with bcrypt"""
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.hash(password)

    def validate_password(self, password: str):
        """Validate password with existing hash"""
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return pwd_context.verify(password, self.hashed_password)

    @property
    def full_name(self):
        return f"{self.surname} {self.name} {self.fathers_name}"


class UserSideBarRead(SQLModel):
    id: int
    full_name: str
    avatar_b64: Optional[str] = None


class UserCreate(UserBase):
    password: str
    is_superuser: bool = False


class UserRead(UserBase):
    id: int


class UserUpdate(SQLModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    fathers_name: Optional[str] = None
    email: Optional[str] = None
    avatar_filename: Optional[str] = None


class AvatarUpload(SQLModel):
    avatar_b64: Optional[str] = None  # b64encoded avatr image
    avatar_url: Optional[str] = (
        None  # url to the uploaded image TODO: add url validator
    )


class AvatarDownload(SQLModel):
    avatar_b64: str
