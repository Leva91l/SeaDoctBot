from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.admin_requests import admin_get_busy_days, admin_get_days

admin_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Посмотреть расписание на определенный день',
                              callback_data='Расписание')],
        [InlineKeyboardButton(text='Открыть расписание на определенный день',
                              callback_data='Открыть')],
        [InlineKeyboardButton(text='Закрыть расписание на определенный день',
                              callback_data='Закрыть')]
    ]
)


async def get_admin_schedule():
    busy_days = await admin_get_busy_days()
    keyboard = InlineKeyboardBuilder()
    for busy_day in busy_days:
        keyboard.add(
            InlineKeyboardButton(text=f'{busy_day.wickday}, {busy_day.date}', callback_data=f'день{busy_day.id}{busy_day.wickday}'))
    return keyboard.adjust(2).as_markup()


async def admin_choose_day_keyboard():
    days = await admin_get_days()
    keyboard = InlineKeyboardBuilder()
    for day in days:
        keyboard.add(
            InlineKeyboardButton(text=f'{day.wickday}, {day.date}', callback_data=f'ЗД{day.id}')
        )
    return keyboard.adjust(2).as_markup()
