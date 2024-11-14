from sqlalchemy import BigInteger, Boolean
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from decouple import config

engine = create_async_engine(config('POSTGRESQL'), echo=False)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Statistics(Base):
    __tablename__ = 'statistics'
    id: Mapped[int] = mapped_column(primary_key=True)
    count_comments: Mapped[int] = mapped_column()
    count_error: Mapped[int] = mapped_column()