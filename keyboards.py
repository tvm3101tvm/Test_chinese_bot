from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton('🇨🇳 Начать новый квест', callback_data='new_game'))
    return kb

def day_menu(day_num, has_unstudied, has_day_graphemes, final_test_available=False):
    kb = InlineKeyboardMarkup(row_width=1)
    if has_unstudied:
        kb.add(InlineKeyboardButton(f'📚 День {day_num} – учить новые иероглифы', callback_data=f'study_day_{day_num}'))
    if has_day_graphemes:
        kb.add(InlineKeyboardButton(f'📝 Тест дня (только день {day_num})', callback_data=f'test_day_{day_num}'))
    kb.add(InlineKeyboardButton('❌ Закончить день', callback_data=f'end_day_{day_num}'))
    if final_test_available:
        kb.add(InlineKeyboardButton('🎓 Финальный тест (все 71 иероглиф)', callback_data='final_test'))
    return kb

def finish_study_keyboard(day_num, total_new):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton(f'📝 Пройти тест дня ({total_new} вопросов)', callback_data=f'test_day_{day_num}'),
        InlineKeyboardButton('➡️ Перейти к следующему дню', callback_data=f'next_day_{day_num+1}')
    )
    return kb

def grapheme_card_keyboard(grapheme_id, day_num):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton('🔊 Озвучить', callback_data=f'voice_{grapheme_id}'),
        InlineKeyboardButton('➡️ Следующий', callback_data=f'next_grapheme_{day_num}_{grapheme_id}')
    )
    kb.add(InlineKeyboardButton('❌ Закончить день', callback_data=f'end_day_{day_num}'))
    return kb

def test_keyboard(question_id, options):
    kb = InlineKeyboardMarkup(row_width=1)
    for i, opt in enumerate(options):
        kb.add(InlineKeyboardButton(opt, callback_data=f'test_ans_{question_id}_{i}'))
    kb.add(InlineKeyboardButton('❌ Прервать тест', callback_data='cancel_test'))
    return kb

def end_game_keyboard():
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(InlineKeyboardButton('🎮 Начать заново', callback_data='new_game'))
    return kb