from sqlalchemy import select

from database.models import *


async def get_days():
    async with async_session() as session:
        days = await session.scalars(select(Wickdays).filter(Wickdays.status == True))
        return days


async def get_times(day):
    async with async_session() as session:
        actual_users_time_id = []
        actual_users = await session.scalars(select(Users).where(Users.wickday_id == day))
        for user in actual_users:
            actual_users_time_id.append(user.time_id)
        free_times = await session.scalars(select(Time).where(Time.id.notin_(actual_users_time_id)))
        return free_times


async def what_a_day(day):
    async with async_session() as session:
        current_day = await session.scalar(select(Wickdays).where(Wickdays.id == day))
        wickday = current_day.wickday
        return wickday


async def what_a_time(time):
    async with async_session() as session:
        current_time = await session.scalar(select(Time).where(Time.id == time))
        time = current_time.time
        return time


async def new_user(name, date_of_birth, tg_id, phone, wickday_id, time_id, consult_type):
    async with async_session() as session:
        user = await session.scalar(select(Users).where(Users.tg_id == tg_id))
        session.add(
            Users(name=name, date_of_birth=date_of_birth, phone=phone, tg_id=tg_id, wickday_id=wickday_id,
                  time_id=time_id, consult_type=consult_type)
        )
        await session.commit()



