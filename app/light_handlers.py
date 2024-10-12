from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, LabeledPrice

from app.keyboards import maintenance_light_keyboard, order_keyboard_light
from config import YOOTOKEN
from long_answers import maintanance_light_answer, reception_info

light_router = Router()


class Reg_light(StatesGroup):
    name = State()
    birthday = State()
    phone = State()


@light_router.message(F.text == 'Сопровождение "Лайт"')
async def maintanance_light(message: Message):
    await message.answer(maintanance_light_answer, reply_markup=maintenance_light_keyboard)


@light_router.message(F.text == 'Запись на прием в клинику')
async def make_an_appointment(message: Message):
    await message.answer(reception_info)


@light_router.message(F.text == 'Была видео-консультация')
@light_router.message(F.text == 'Наблюдаюсь в клинике')
async def get_name_light(message: Message, state: FSMContext):
    await message.answer('Отлично, теперь запишем ваши данные. Введите, пожалуйста ФИО')
    await state.set_state(Reg_light.name)


@light_router.message(Reg_light.name)
async def get_birthday_light(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await  message.answer('Теперь введите дату рождения в формате дд.мм.гггг')
    await state.set_state(Reg_light.birthday)


@light_router.message(Reg_light.birthday)
async def get_phone(message: Message, state: FSMContext):
    await state.update_data(birthday=message.text)
    await message.answer('И ваш номер телефона, пожалуйста')
    await state.set_state(Reg_light.phone)


@light_router.message(Reg_light.phone)
async def order_ligth(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(None)
    await message.answer('Теперь нужно оплатить', reply_markup=order_keyboard_light)


@light_router.message(F.text == 'Оплатить')
async def start_payment_light(message: Message, bot: Bot):
    await bot.send_invoice(
        chat_id=message.chat.id,
        title='Оплата',
        description='Сопровождение "Лайт"',
        payload=f'Лайт',
        provider_token=YOOTOKEN,
        currency='RUB',
        prices=[LabeledPrice(
            label='Цена',
            amount=20000
        )]
    )


