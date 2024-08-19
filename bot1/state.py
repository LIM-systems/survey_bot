from aiogram.dispatcher.filters.state import State, StatesGroup


class QuestionsState(StatesGroup):
    questions = State()
    swap_questions_ids = State()
    add_question = State()
    question_id = State()
