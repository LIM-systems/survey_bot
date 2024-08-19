from aiogram import types
from aiogram.dispatcher import FSMContext

import bot1.CRUD.survey as db
from bot1.loader import dp, rate_buttons, yon
from bot1.state import QuestionsState


@dp.message_handler(commands=['start'])
@dp.message_handler(commands=['start'], state=QuestionsState.questions)
async def start(msg: types.Message, state: FSMContext):
    '''Старт'''
    # приветствуем и записываем
    await state.finish()
    greeting = await db.get_greeting()
    button = types.InlineKeyboardButton(
        text='Начать', callback_data='start_button')
    markup = types.InlineKeyboardMarkup().add(button)
    await msg.answer(greeting, reply_markup=markup)
    await db.add_user(msg.from_user.id, msg.from_user.full_name)


async def gen_question_msg(question, state):
    '''Генерация сообщения с вопросом'''
    text = question['name']
    id = question['id']
    await state.update_data(question_id=id)
    if question['answer_view'] == 2:
        keyboard = types.InlineKeyboardMarkup().row(
            types.InlineKeyboardButton(
                text='Да', callback_data='yes_yon_button'),
            types.InlineKeyboardButton(
                text='Нет', callback_data='no_yon_button')
        )
    elif question['answer_view'] == 0:
        keyboard = types.InlineKeyboardMarkup().row(
            types.InlineKeyboardButton(
                text=rate_buttons[0], callback_data='1_rate_button'),
            types.InlineKeyboardButton(
                text=rate_buttons[1], callback_data='2_rate_button'),
            types.InlineKeyboardButton(
                text=rate_buttons[2], callback_data='3_rate_button'),
            types.InlineKeyboardButton(
                text=rate_buttons[3], callback_data='4_rate_button'),
            types.InlineKeyboardButton(
                text=rate_buttons[4], callback_data='5_rate_button'),
        )
    elif question['answer_view'] == 1:
        keyboard = None

    return text, keyboard


async def set_question(text, keyboard, msg, state, add_question=None):
    await msg.answer(text, reply_markup=keyboard)
    if not keyboard:
        await QuestionsState.questions.set()
    await state.update_data(add_question=add_question)


async def get_new_question(msg, tg_id, state):
    '''Получение нового вопроса'''

    # получаем вопросы из бд
    data = await state.get_data()

    add_question = data.get('add_question')
    if add_question:
        text, keyboard = await gen_question_msg(add_question, state)
        await set_question(text, keyboard, msg, state)
        await state.update_data(add_question=None)
        return

    questions = data.get('questions')
    swap_questions_ids = data.get('swap_questions_ids')
    for question in questions:
        if not question['answered'] and question['id'] not in swap_questions_ids:
            text, keyboard = await gen_question_msg(question, state)
            add_question = None
            if question['add_question_id']:
                add_question = await db.get_question(question['add_question_id'])
                add_question = {**add_question.__dict__, 'answered': False}
            await set_question(text, keyboard, msg, state, add_question)
            return

    parting_msg = await db.get_parting()
    answers = []
    for question in questions:
        question.pop('answered')
        answers.append(question)
    await db.save_result(tg_id, answers)
    await msg.answer(parting_msg)


@dp.callback_query_handler(lambda c: c.data == 'start_button')
async def start_button(call: types.CallbackQuery, state: FSMContext):
    '''Кнопка "Начать"'''
    await call.message.delete()
    questions = await db.get_questions()
    swap_questions_ids = []
    for question in questions:
        if question['add_question_id']:
            swap_questions_ids.append(question['add_question_id'])
    await state.update_data(questions=questions)
    await state.update_data(swap_questions_ids=swap_questions_ids)
    await get_new_question(call.message, call.from_user.id, state)


@dp.callback_query_handler(lambda c: c.data.endswith('rate_button'))
@dp.callback_query_handler(lambda c: c.data.endswith('rate_button'), state=QuestionsState.questions)
async def rate_button(call: types.CallbackQuery, state: FSMContext):
    '''Кнопка "Оценить"'''
    # получаем данные из callback_data
    await call.message.delete()
    rate = int(call.data.split('_')[0])

    data = await state.get_data()
    id = data.get('question_id')
    questions = data.get('questions')
    for question in questions:
        if question['id'] == id:
            if str(rate) not in question['trigger']:
                await state.update_data(add_question=None)
            question['rate'] = rate
            question['answered'] = True
            await state.update_data(questions=questions)
            await get_new_question(call.message, call.from_user.id, state)
            break


@dp.message_handler(state=QuestionsState.questions)
async def comment(msg: types.Message, state: FSMContext):
    '''Комментарий'''
    data = await state.get_data()
    id = data.get('question_id')
    questions = data.get('questions')
    for i, question in enumerate(questions):
        if question['id'] == id:
            question['comment'] = msg.text
            question['answered'] = True
            await state.update_data(questions=questions)
            await get_new_question(msg, msg.from_user.id, state)
            return


@dp.callback_query_handler(lambda c: c.data.endswith('yon_button'))
@dp.callback_query_handler(lambda c: c.data.endswith('yon_button'), state=QuestionsState.questions)
async def yon_button(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    answer = call.data.split('_')[0]
    data = await state.get_data()
    id = data.get('question_id')
    questions = data.get('questions')
    for question in questions:
        if question['id'] == id:
            trigger_answer = 'Да' if answer == 'yes' else 'Нет'
            if str(trigger_answer) not in question['trigger']:
                await state.update_data(add_question=None)
            question['yon'] = True if answer == 'yes' else False
            question['answered'] = True
            await state.update_data(questions=questions)
            await get_new_question(call.message, call.from_user.id, state)
            break
