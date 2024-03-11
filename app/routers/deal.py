from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from app.db import LocalAsyncSession, get_session
from .utils import get_current_user_id

from app.models.deal import DealCreate, DealUpdate, DealRead
from app.models.user import UserRead
from app.cruds.deal import (
    get_deal_by_id,
    get_deal_users,
    create_deal,
    update_deal,
    delete_deal
)
from app.cruds.user import get_user_by_id


router = APIRouter()


@router.get(
    "/deals/{deal_id}",
    tags=["deals"],
    response_model=DealRead
)
async def get_deal_api(
    db: Annotated[LocalAsyncSession, Depends(get_session)],
    user_id: Annotated[int, Depends(get_current_user_id)],
    deal_id: int
):
    deal = await get_deal_by_id(db, deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_id != deal.creator_id or user not in deal.users:
        raise HTTPException(status_code=403, detail="Not enough privileges to perform requested action")


@router.get(
    "/deals/{deal_id}/users",
    tags=["deals"],
    response_model=list[UserRead]
)
async def get_deal_users_api(
    db: Annotated[LocalAsyncSession, Depends(get_session)],
    user_id: Annotated[int, Depends(get_current_user_id)],
    deal_id: int
):
    deal = await get_deal_by_id(db, deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_id != deal.creator_id or user not in deal.users:
        raise HTTPException(status_code=403, detail="Not enough privileges to perform requested action")
    return await get_deal_users(db, deal_id)


@router.post(
    "/deals/",
    tags=["deals"],
    response_model=DealRead
)
async def create_deal_api(
    db: Annotated[LocalAsyncSession, Depends(get_session)],
    user_id: Annotated[int, Depends(get_current_user_id)],
    deal: DealCreate
):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db_deal = await create_deal(db, deal, creator_id=user_id)
    return db_deal


@router.put(
    "/deals/{deal_id}",
    tags=['deals'],
    response_model=DealRead
)
async def update_deal_api(
    db: Annotated[LocalAsyncSession, Depends(get_session)],
    user_id: Annotated[int, Depends(get_current_user_id)],
    deal_id: int,
    deal: DealUpdate
):
    deal = await get_deal_by_id(db, deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_id != deal.creator_id or user not in deal.users:
        raise HTTPException(status_code=403, detail="Not enough privileges to perform requested action")
    db_deal = await update_deal(db, deal_id, deal)
    return db_deal


@router.delete(
    "/deals/{deal_id}",
    tags=['deals'],
    response_model=DealRead
)
async def delete_deal_api(
    db: Annotated[LocalAsyncSession, Depends(get_session)],
    user_id: Annotated[int, Depends(get_current_user_id)],
    deal_id: int
):
    deal = await get_deal_by_id(db, deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user_id != deal.creator_id:
        raise HTTPException(status_code=403, detail="Not enough privileges to perform requested action")
    db_deal = await delete_deal(db, deal_id)
    return db_deal
