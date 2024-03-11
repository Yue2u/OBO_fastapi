from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from app.db import LocalAsyncSession, get_session
from .utils import get_current_user_id
from app.models.user import (
    User,
    UserRead,
    UserCreate,
    UserUpdate,
    UserSideBarRead,
    AvatarUpload,
    AvatarDownload,
)
from app.cruds.user import (
    get_user_by_id,
    get_user_by_email,
    get_users,
    get_or_create_user_by_email,
    create_user,
    update_user,
    delete_user,
    update_user_kwargs,
    get_users_deals,
    is_user_superuser
)
from app.models.deal import DealRead

router = APIRouter()


@router.get("/users", tags=["users"], response_model=list[UserRead])
async def get_users_list(
    db: Annotated[LocalAsyncSession, Depends(get_session)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Not not found")

    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough privileges to perform requested action")

    return await get_users(db)


@router.get(
    "/users/me",
    tags=["users"],
    response_model=UserRead,
)
async def get_user(
    db: Annotated[LocalAsyncSession, Depends(get_session)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    user = await get_user_by_id(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user)


@router.get(
    "/users/me/deals",
    tags=["users"],
    response_model=list[DealRead],
)
async def get_user_deals(
    db: Annotated[LocalAsyncSession, Depends(get_session)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    user = await get_user_by_id(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    deals = await get_users_deals(db, user_id)
    return deals


@router.post(
    "/users/me",
    tags=["users"],
    response_model=UserRead,
)
async def create_new_user(
    db: Annotated[LocalAsyncSession, Depends(get_session)],
    user_id: Annotated[int, Depends(get_current_user_id)],
    user: UserCreate,
):
    if not is_user_superuser(db, user_id):
        raise HTTPException(status_code=403, detail="Not enough privileges to perform requested action")
    return await create_user(db, user)


@router.put(
    "/users/me",
    tags=["users"],
    response_model=UserRead,
)
async def update_existing_user(
    db: Annotated[LocalAsyncSession, Depends(get_session)],
    user_id: Annotated[int, Depends(get_current_user_id)],
    user: UserUpdate,
):
    updated = await update_user(db, user_id, user)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.delete(
    "/users/me",
    tags=["users"],
    response_model=UserRead,
)
async def delete_existing_user(
    db: Annotated[LocalAsyncSession, Depends(get_session)],
    user_id: Annotated[int, Depends(get_current_user_id)],
):
    deleted = await delete_user(db, user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted
