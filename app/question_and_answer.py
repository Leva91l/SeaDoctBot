from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile

from app.handlers import Reg
from app.keyboards import qa_keyboard

qa_router = Router()


@qa_router.message(F.text == 'Расшифровка анализов')
async def question_and_answer(message: Message, state: FSMContext):
    await state.update_data(consult_type=message.text)
    await message.answer('Какое количество анализов нужно обсудить?', reply_markup=qa_keyboard)
    await state.set_state(Reg.count_of_analyses)


@qa_router.message(Reg.count_of_analyses)
async def question_and_answer_info(message: Message, state: FSMContext):
    await state.update_data(count_of_analyses=message.text)
    await message.answer('Бот скидывает  оферту и политику конф данных, и инфу по консультации, что где когда и Просит ввести ФИО')
    await message.answer_document(FSInputFile('docs/Konfidenc'))
    await message.answer_document(FSInputFile('docs/Oferta'))
    await state.set_state(Reg.name)

