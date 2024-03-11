from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.models.deal import Deal, DealCreate, DealRead, DealUpdate
from app.db import LocalAsyncSession


async def get_deal_by_id(db: LocalAsyncSession, id: int):
    stmt = (
        select(Deal)
        .options(selectinload(Deal.users))
        .where(Deal.id == id)
    )
    results = await db.execute(stmt)
    return results.scalars().first()


async def get_deal_users(db: LocalAsyncSession, deal_id: int):
    stmt = (
        select(Deal.users)
        .options(selectinload(Deal.users))
        .where(Deal.id == deal_id)
    )
    results = await db.execute(stmt)
    return results.scalars().all()


async def create_deal(db: LocalAsyncSession, deal: DealCreate, creator_id: int):
    db_deal = Deal.model_validate(deal)
    db_deal.creator_id = creator_id
    db.add(db_deal)
    await db.commit()
    await db.refresh(db_deal)
    return db_deal


async def update_deal(db: LocalAsyncSession, deal_id: int, deal: DealUpdate):
    db_deal = await get_deal_by_id(db, deal_id)
    if not db_deal:
        return None

    deal_data = deal.model_dump(exclude_unset=True)

    for key, value in deal_data.items():
        setattr(db_deal, key, value)

    db.add(db_deal)
    await db.commit()
    await db.refresh(db_deal)
    return db_deal


async def delete_deal(db: LocalAsyncSession, deal_id: int):
    db_deal = await get_deal_by_id(db, deal_id)
    if not db_deal:
        return None
    await db.delete(db_deal)
    await db.commit()
    return db_deal
