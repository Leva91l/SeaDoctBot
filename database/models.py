from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine('sqlite+aiosqlite:///SDB.db', echo=False)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Wickdays(Base):
    __tablename__ = 'wickdays'
    id = Column(Integer, primary_key=True, autoincrement=True)
    wickday = Column(String, unique=True)
    date = Column(String)


class Time(Base):
    __tablename__ = 'time'
    id = Column(Integer, primary_key=True, autoincrement=True)
    time = Column(String, unique=True)


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer)
    name = Column(String)
    date_of_birth = Column(String)
    phone = Column(String)
    consult_type = Column(String)
    wickday_id = Column(Integer, ForeignKey('wickdays.id'))
    time_id = Column(Integer, ForeignKey('time.id'))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
