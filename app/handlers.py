from aiogram import Router, F, Bot
from aiogram.enums import ContentType
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile, CallbackQuery, LabeledPrice, PreCheckoutQuery

from app.keyboards import type_consult, first_or_second, accept_agreement, get_all_days, order_keyboard, get_all_times, \
    maintenance_keyboard
from config import HELLO_MESSAGE, YOOTOKEN, ADMIN_ID
from database.requests import what_a_day, what_a_time, new_user
from long_answers import reception_info

router = Router()


class Reg(StatesGroup):
    name = State()
    phone = State()
    birthday = State()
    consult_type = State()
    appointment = State()
    selected_day = State()
    selected_time = State()


@router.message(CommandStart())
async def welcome(message: Message, state: FSMContext):
    await message.answer_photo(photo='https://i10.fotocdn.net/s214/fab8c913b608e654/public_pin_l/2890742493.jpg')
    await message.answer(
        'Вас приветсвует бот Левченко Екатерины Андреевны. Пожалуйста, ознакомьтесь с форматами работы доктора, и выберите подходящий вариант:')
    await message.answer(HELLO_MESSAGE, reply_markup=type_consult)
    await state.set_state(Reg.consult_type)


@router.message(F.text == 'Очный прием')
@router.message(F.text == Reg.consult_type)
async def reception(message: Message, state: FSMContext):
    await state.update_data(consult_type=message.text)
    await message.answer(reception_info)
    await state.set_state(None)


@router.message(F.text == 'Видео-консультация')
@router.message(F.text == Reg.consult_type)
async def video_consultation(message: Message, state: FSMContext):
    await state.update_data(consult_type=message.text)
    await state.set_state(None)
    await message.answer('Какой у вас прием? Первичный или вторичный?', reply_markup=first_or_second)
    await state.set_state(Reg.appointment)


@router.message(F.text == 'Сопровождение "Оптимальный"')
@router.message(F.text == 'Сопровождение "Макси"')
@router.message(F.text == Reg.consult_type)
async def maintenance(message: Message, state: FSMContext):
    await state.update_data(consult_type=message.text)
    await state.set_state(None)
    await message.answer_document(FSInputFile('docs/Oferta'))
    await message.answer_document(FSInputFile('docs/Konfidenc'))
    await message.answer(
        'Бот пишет инфу по сопровождению подробно и говорит что сперва будет онлайн консультация и скидывает оферту и политику',
        reply_markup=maintenance_keyboard)


@router.message(Reg.appointment)
async def video_consultation(message: Message, state: FSMContext):
    await state.update_data(appointment=message.text)
    await state.set_state(None)
    await message.answer_document(FSInputFile('docs/Oferta'))
    await message.answer_document(FSInputFile('docs/Konfidenc'))
    await message.answer('Пожалуйста, ознакомьтесь с документами и нажмите принять',
                         reply_markup=accept_agreement)


@router.message(F.text == 'Принимаю')
@router.message(F.text == 'Да, продолжим!')
async def get_name(message: Message, state: FSMContext):
    await message.answer('Отлично. Теперь напишите ФИО полностью:')
    await state.set_state(Reg.name)


@router.message(Reg.name)
async def get_birthday(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Спасибо! Теперь напишите дату рождения в формате дд.мм.гггг:')
    await state.set_state(Reg.birthday)


@router.message(Reg.birthday)
async def get_phone(message: Message, state: FSMContext):
    await state.update_data(birthday=message.text)
    await message.answer('Отлично, теперь напишите свой номер телефона:')
    await state.set_state(Reg.phone)


@router.message(Reg.phone)
async def get_schedule_wickday(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer(
        'Спасибо. Теперь нужно выбрать дату и время консультации. Давайте выберем день из предложенных:',
        reply_markup=await get_all_days())
    await state.set_state(Reg.selected_day)


@router.callback_query(Reg.selected_day)
async def get_schedule_time(callback: CallbackQuery, state: FSMContext):
    day = callback.data
    await state.update_data(selected_day=callback.data)
    await callback.message.edit_text('Теперь время', reply_markup=await get_all_times(day))
    await state.set_state(Reg.selected_time)


@router.callback_query(Reg.selected_time)
async def order(callback: CallbackQuery, state: FSMContext):
    print(callback.data)
    await state.update_data(selected_time=callback.data)
    data = await state.get_data()
    print(data)
    await state.set_state(None)
    await callback.message.edit_text('Теперь нужно произвести оплату!', reply_markup=order_keyboard)


@router.callback_query(F.data == 'Приступить к оплате')
async def start_payment(callback: CallbackQuery, bot: Bot, ):
    await bot.send_invoice(
        chat_id=callback.message.chat.id,
        title='Консультация',
        description='Консультация у Левченко Е.А.',
        payload=f'Платеж за консультацию',
        provider_token=YOOTOKEN,
        currency='RUB',
        prices=[LabeledPrice(
            label='Цена',
            amount=10000
        )]
    )


@router.pre_checkout_query()
async def pre_checkout_query(pre_check: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_check.id, ok=True)


@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    print(data)
    wickday = await what_a_day(data['selected_day'])
    time = await what_a_time(data['selected_time'])
    msg = f'Спасибо за оплату!\n{data['name']}, Вы записались на консультацию к Левченко Е.А. на {wickday} в {time}.'
    await new_user(name=data['name'], date_of_birth=data['birthday'], phone=data['phone'], tg_id=message.chat.id,
                   wickday_id=data['selected_day'], time_id=data['selected_time'], consult_type=data['consult_type'])
    await message.answer_document(FSInputFile('docs/Anketa'))
    await bot.send_message(ADMIN_ID,
                           f'Муська, к тебе записались на {data['consult_type']}!\nПациент - {data['name']}, на {wickday}, {time}\nТы можешь посмотреть подробную информацию у себя в админ панели выбрав день и время записи.')
    return await message.answer(msg)
