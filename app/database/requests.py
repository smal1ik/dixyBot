from app.database.models import Statistics, async_session
from sqlalchemy import select, BigInteger, update, delete, func

async def add_error():
    async with async_session() as session:
        result = await session.scalar(select(Statistics).where(Statistics.id == 1))
        await session.execute(update(Statistics).where(Statistics.id == 1).values(
            count_error=result.count_error+1)
        )
        await session.commit()

async def add_comments():
    async with async_session() as session:
        result = await session.scalar(select(Statistics).where(Statistics.id == 1))
        await session.execute(update(Statistics).where(Statistics.id == 1).values(
            count_comments=result.count_comments+1)
        )
        await session.commit()

async def get_statistics():
    async with async_session() as session:
        result = await session.scalar(select(Statistics).where(Statistics.id == 1))
        return result