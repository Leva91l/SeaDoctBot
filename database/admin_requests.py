from sqlalchemy import select
from sqlalchemy.orm.sync import update

from database.models import *


async def admin_get_days():
    async with async_session() as session:
        days = await session.scalars(select(Wickdays))
        print(days)
        return days



async def admin_get_busy_days():
    async with async_session() as session:

        result = await session.execute(
            select(Users, Wickdays).join(Wickdays, Users.wickday_id == Wickdays.id, isouter=True))
        wickdays_list = []
        for user, wickday in result:
            wickdays_list.append(wickday)
        wickdays_list = set(wickdays_list)
        return wickdays_list


async def admin_get_busy_time(day):
    async with async_session() as session:
        actual_users = await session.scalars(select(Users).where(Users.wickday_id == day))
        return actual_users


async def close_day(day):
    async with async_session() as session:
        day_to_close = await session.scalar(select(Wickdays).filter(Wickdays.id == day))
        day_to_close.status = False
        await session.commit()
