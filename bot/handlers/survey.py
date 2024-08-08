from aiogram import types
from aiogram.dispatcher import FSMContext

import bot.CRUD.survey as db
from bot import loader as ld
from bot.loader import dp, parting, rate_buttons
from bot.state import QuestionsState


@dp.message_handler(commands=['start'])
@dp.message_handler(commands=['start'], state=QuestionsState.questions)
async def start(msg: types.Message, state: FSMContext):
    '''Старт'''
    # приветствуем и записываем
    await state.finish()
    button = types.InlineKeyboardButton(
        text='Начать', callback_data='start_button')
    markup = types.InlineKeyboardMarkup().add(button)
    await msg.answer(ld.greeting, reply_markup=markup)
    await db.add_user(msg.from_user.id, msg.from_user.full_name)


async def get_new_question(msg, state):
    '''Получение нового вопроса'''

    # получаем вопросы из бд
    data = await state.get_data()
    questions = data.get('questions')
    if not questions:
        questions = await db.get_questions()
        await state.update_data(questions=questions)

    # формируем кнопки и ответ
    for question in questions:
        if not question['answered']:
            if question['answer_view'] == 0:
                rates = [types.InlineKeyboardButton(
                    rate, callback_data=f'{rate}_rate_button') for rate in rate_buttons]
                keyboard = types.InlineKeyboardMarkup().row(*rates)
                await msg.answer(question['name'], reply_markup=keyboard)
                return
            else:
                await msg.answer(question['name'])
                return


@dp.callback_query_handler(lambda c: c.data == 'start_button')
async def start_button(call: types.CallbackQuery, state: FSMContext):
    '''Кнопка "Начать"'''
    await call.message.delete()
    yes_button = types.InlineKeyboardButton(
        'Да', callback_data='yes_button_first_question')
    no_button = types.InlineKeyboardButton(
        'Нет', callback_data='no_button_first_question')
    keyboard = types.InlineKeyboardMarkup().row(no_button, yes_button)
    await call.message.answer('Вы были на 19-летии компании?', reply_markup=keyboard)
    await QuestionsState.first_question.set()


@dp.callback_query_handler(lambda c: c.data.endswith('first_question'),
                           state=QuestionsState.first_question)
async def was_in_question(call: types.CallbackQuery, state: FSMContext):
    '''Вопрос "Были ли на дне рождения компании?"'''
    await call.message.delete()
    answer = call.data.split('_')[0] == 'yes'
    await db.set_was_in(call.from_user.id, answer)
    if answer:
        await get_new_question(call.message, state)
        await QuestionsState.questions.set()
    else:
        await call.message.answer('По какой причине не смогли попасть на мероприятие?')
        await QuestionsState.reason.set()


@dp.message_handler(state=QuestionsState.reason)
async def reason_question(msg: types.Message, state: FSMContext):
    '''Вопрос "По какой причине не смогли попасть на мероприятие?"'''
    await db.set_was_in_reason(msg.from_user.id, msg.text)
    await msg.answer('Очень жаль, что Вас не было☹️\nБудем рады увидеться на юбилее компании!')
    await state.finish()


@dp.callback_query_handler(lambda c: c.data.endswith('rate_button'), state=QuestionsState.questions)
async def rate_button(call: types.CallbackQuery, state: FSMContext):
    '''Кнопка "Оценить"'''
    # получаем данные из callback_data
    # original_text = call.message.text
    # await call.message.edit_text(text=original_text)
    await call.message.delete()
    rate = int(call.data.split('_')[0][0])

    data = await state.get_data()
    questions = data.get('questions')
    for question in questions:
        if not question['answered']:
            question['rate'] = rate
            question['answered'] = True
            await state.update_data(questions=questions)
            await get_new_question(call.message, state)
            # await call.message.answer('Ваш комментарий:')
            break


@dp.message_handler(state=QuestionsState.questions)
async def comment(msg: types.Message, state: FSMContext):
    '''Комментарий'''
    data = await state.get_data()
    questions = data.get('questions')
    for i, question in enumerate(questions):
        if not question['answered']:
            question['comment'] = msg.text
            question['answered'] = True
            await state.update_data(questions=questions)
            if i != len(questions) - 1:
                await get_new_question(msg, state)
                return
            else:
                answers = []
                for question in questions:
                    question.pop('answered')
                    answers.append(question)
                await db.save_result(msg.from_user.id, answers)
                await msg.answer(parting)
                await state.finish()
