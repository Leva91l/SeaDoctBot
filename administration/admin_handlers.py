from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from administration.admin_keyboards import admin_keyboard, get_admin_schedule, admin_choose_day_keyboard
from config import ADMIN_ID
from database.admin_requests import admin_get_busy_time, close_day
from database.requests import what_a_time

admin_router = Router()


@admin_router.message(Command('admin'))
async def admin(message: Message):
    if str(message.from_user.id) == ADMIN_ID:
        await message.answer('Вас приветствует личный бот Муськи. Что вы хотите сделать?', reply_markup=admin_keyboard)
    else:
        await message.answer('Админ-панель только для администратора!\nНажмите "Запустить бот заново"')


@admin_router.callback_query(F.data == 'Расписание')
async def detailed_information_wickday(callback: CallbackQuery):
    await callback.message.edit_text('Все дни с записями. Выберите какой день посмотреть:',
                                     reply_markup=await get_admin_schedule())


@admin_router.callback_query(F.data.startswith('день'))
async def detailed_information_time(callback: CallbackQuery):
    day = callback.data[4:5]
    wickday = callback.data[5:8]
    actual_users = await admin_get_busy_time(day)
    await callback.message.answer(f'На {wickday} у Вас записаны:')
    for user in actual_users:
        busy_time = await what_a_time(user.time_id)
        await callback.message.answer(
            f'{user.name}, {user.date_of_birth} г.р, {user.phone} - {user.consult_type} на {busy_time}')


@admin_router.callback_query(F.data == 'Закрыть')
async def admin_choose_day_to_close(callback: CallbackQuery):
    print(callback.data)
    await callback.message.edit_text('Выберите день для закрытия:', reply_markup=await admin_choose_day_keyboard())


@admin_router.callback_query(F.data.startswith('ЗД'))
async def admin_close_day(callback: CallbackQuery):
    day = callback.data[2:]
    await close_day(day)
