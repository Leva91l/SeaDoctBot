from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.requests import get_days, get_times

type_consult = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Очный прием'), KeyboardButton(text='Видео-консультация')],
        [KeyboardButton(text='Сопровождение "Лайт"'), KeyboardButton(text='Сопровождение "Оптимальный"')],
            [KeyboardButton(text='Сопровождение "Макси"'), KeyboardButton(text='Расшифровка анализов')],
    ],
    resize_keyboard=True,
    input_field_placeholder='↓Выберите из пунктов ниже↓'
)

first_or_second = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Первичный'), KeyboardButton(text='Вторичный')],
    ],
    resize_keyboard=True,
    input_field_placeholder='↓Выберите из пунктов ниже↓'

)

accept_agreement = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Принимаю')],
    ],
    resize_keyboard=True,
    input_field_placeholder='↓Если вам все понятно, и вы согласны нажмите принять↓'
)

accept_agreement_for_light = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Принять')],
    ],
    resize_keyboard=True,
    input_field_placeholder='↓Если вам все понятно, и вы согласны нажмите принять↓'
)


async def get_all_days():
    days = await get_days()
    keyboard = InlineKeyboardBuilder()
    for day in days:
        keyboard.add(InlineKeyboardButton(text=f'{day.wickday}, {day.date}', callback_data=f'{day.id}'))
    return keyboard.adjust(2).as_markup()


async def get_all_times(day):
    times = await get_times(day)
    keyboard = InlineKeyboardBuilder()
    for time_ in times:
        keyboard.add(InlineKeyboardButton(text=f'{time_.time}', callback_data=f'{time_.id}'))
    return keyboard.adjust(2).as_markup()


order_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Приступить к оплате', callback_data='Приступить к оплате')]
    ]
)

order_keyboard_light = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Оплатить', callback_data='Оплатить')]
    ],
    resize_keyboard=True,
)


observation_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Да'), KeyboardButton(text='Нет')]
    ],
    resize_keyboard=True,
    input_field_placeholder='↓Выберите из пунктов ниже↓'
)

maintenance_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Да, продолжим!')]
    ],
    resize_keyboard=True,
    input_field_placeholder='↓Выберите из пунктов ниже↓'
)

maintenance_light_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Была видео-консультация'), KeyboardButton(text='Наблюдаюсь в клинике')],
        [KeyboardButton(text='Запись на прием в клинику'), KeyboardButton(text='Запись на видео-консультацию')]
    ],
    resize_keyboard=True,
    input_field_placeholder='↓Выберите из пунктов ниже↓'
)

qa_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Меньше 5'), KeyboardButton(text='Больше 5')]
    ],
    resize_keyboard=True,
    input_field_placeholder='↓Выберите из пунктов ниже↓'
)