from sqlalchemy.orm import selectinload
from sqlmodel import select
from fastapi import HTTPException

from app.models.user import User, UserCreate, UserUpdate
from app.db import LocalAsyncSession


async def get_users(db: LocalAsyncSession):
    users = await db.execute(select(User))
    return users.scalars().all()


async def get_user_by_id(db: LocalAsyncSession, id: ImportWarning):
    stmt = select(User).where(User.id == id)
    users = await db.execute(stmt)
    result = users.scalars().first()
    return result


async def get_users_deals(db: LocalAsyncSession, user_id: int):
    stmt = (
        select(User.deals)
        .options(selectinload(User.deals))
        .where(User.id == user_id)
    )
    deals = await db.execute(stmt)
    return deals.scalars().all()


async def get_user_by_email(db: LocalAsyncSession, email: str):
    stmt = select(User).where(User.email == email)
    users = await db.execute(stmt)
    result = users.scalars().first()
    return result


async def get_or_create_user_by_email(db: LocalAsyncSession, email: str):
    user = await get_user_by_email(db, email)
    if not user:
        user = User(email=email)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    return user


async def is_user_superuser(db: LocalAsyncSession, user_id: int):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Admin not found")
    return user.is_superuser


async def create_user(db: LocalAsyncSession, user: UserCreate):
    user_data = user.model_dump(exclude_unset=True)
    password = user_data.pop("password")
    user_data["hashed_password"] = User.hash_password(password)
    new_user = User(**user_data)
    db.add(new_user)
    await db.commit()
    return new_user


async def update_user(db: LocalAsyncSession, user_id: int, user: UserUpdate):
    db_user = await get_user_by_id(db, id=user_id)
    if not db_user:
        return None
    user_data = user.model_dump(exclude_unset=True)

    for key, value in user_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    await db.commit()
    return db_user


async def update_user_kwargs(db: LocalAsyncSession, user_id: int, **kwargs):
    db_user = await get_user_by_id(db, id=user_id)
    if not db_user:
        return None
    user_data = kwargs
    for key, value in user_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def delete_user(db: LocalAsyncSession, user_id: int):
    db_user = await get_user_by_id(db, id=user_id)
    if not db_user:
        return None
    db.delete(db_user)
    await db.commit()
    return db_user
