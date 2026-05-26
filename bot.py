import logging
import os
import json
import random
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from config import BOT_TOKEN
from keyboards import (
    main_menu, day_menu, finish_study_keyboard, grapheme_card_keyboard,
    test_keyboard, end_game_keyboard
)

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# ======================= БАЗА ГРАФЕМ (71 иероглиф) =======================
# У каждого: char, pinyin, meaning, gif (file_id), audio (file_id)
graphemes = {
    1: {'char': '人', 'pinyin': 'rén', 'meaning': 'человек', 'gif': None, 'audio': None},
    2: {'char': '大', 'pinyin': 'dà', 'meaning': 'большой', 'gif': None, 'audio': None},
    3: {'char': '天', 'pinyin': 'tiān', 'meaning': 'небо', 'gif': None, 'audio': None},
    4: {'char': '口', 'pinyin': 'kǒu', 'meaning': 'рот', 'gif': None, 'audio': None},
    5: {'char': '日', 'pinyin': 'rì', 'meaning': 'солнце', 'gif': None, 'audio': None},
    6: {'char': '目', 'pinyin': 'mù', 'meaning': 'глаз', 'gif': None, 'audio': None},
    7: {'char': '田', 'pinyin': 'tián', 'meaning': 'поле', 'gif': None, 'audio': None},
    8: {'char': '月', 'pinyin': 'yuè', 'meaning': 'месяц', 'gif': None, 'audio': None},
    9: {'char': '木', 'pinyin': 'mù', 'meaning': 'дерево', 'gif': None, 'audio': None},
    10: {'char': '女', 'pinyin': 'nǚ', 'meaning': 'женщина', 'gif': None, 'audio': None},
    11: {'char': '马', 'pinyin': 'mǎ', 'meaning': 'лошадь', 'gif': None, 'audio': None},
    12: {'char': '儿', 'pinyin': 'ér', 'meaning': 'идущий человек', 'gif': None, 'audio': None},
    13: {'char': '父', 'pinyin': 'fù', 'meaning': 'отец', 'gif': None, 'audio': None},
    14: {'char': '母', 'pinyin': 'mǔ', 'meaning': 'мать', 'gif': None, 'audio': None},
    15: {'char': '门', 'pinyin': 'mén', 'meaning': 'дверь', 'gif': None, 'audio': None},
    16: {'char': '刀', 'pinyin': 'dāo', 'meaning': 'нож', 'gif': None, 'audio': None},
    17: {'char': 'ヒ', 'pinyin': 'bǐ', 'meaning': 'черпак, кинжал', 'gif': None, 'audio': None},
    18: {'char': '米', 'pinyin': 'mǐ', 'meaning': 'рис', 'gif': None, 'audio': None},
    19: {'char': '水', 'pinyin': 'shuǐ', 'meaning': 'вода', 'gif': None, 'audio': None},
    20: {'char': '火', 'pinyin': 'huǒ', 'meaning': 'огонь', 'gif': None, 'audio': None},
    21: {'char': '毛', 'pinyin': 'máo', 'meaning': 'шерсть', 'gif': None, 'audio': None},
    22: {'char': '手', 'pinyin': 'shǒu', 'meaning': 'рука', 'gif': None, 'audio': None},
    23: {'char': '又', 'pinyin': 'yòu', 'meaning': 'ладонь правой руки', 'gif': None, 'audio': None},
    24: {'char': '足', 'pinyin': 'zú', 'meaning': 'нога, ступня', 'gif': None, 'audio': None},
    25: {'char': '走', 'pinyin': 'zǒu', 'meaning': 'идти', 'gif': None, 'audio': None},
    26: {'char': '行', 'pinyin': 'xíng', 'meaning': 'движение', 'gif': None, 'audio': None},
    27: {'char': '舌', 'pinyin': 'shé', 'meaning': 'язык', 'gif': None, 'audio': None},
    28: {'char': '言', 'pinyin': 'yán', 'meaning': 'речь', 'gif': None, 'audio': None},
    29: {'char': '立', 'pinyin': 'lì', 'meaning': 'стоять', 'gif': None, 'audio': None},
    30: {'char': '音', 'pinyin': 'yīn', 'meaning': 'звук', 'gif': None, 'audio': None},
    31: {'char': '面', 'pinyin': 'miàn', 'meaning': 'лицо, мука', 'gif': None, 'audio': None},
    32: {'char': '见', 'pinyin': 'jiàn', 'meaning': 'видеться', 'gif': None, 'audio': None},
    33: {'char': '耳', 'pinyin': 'ěr', 'meaning': 'ухо', 'gif': None, 'audio': None},
    34: {'char': '页', 'pinyin': 'yè', 'meaning': 'страница', 'gif': None, 'audio': None},
    35: {'char': '牙', 'pinyin': 'yá', 'meaning': 'зуб', 'gif': None, 'audio': None},
    36: {'char': '文', 'pinyin': 'wén', 'meaning': 'письмена', 'gif': None, 'audio': None},
    37: {'char': '比', 'pinyin': 'bǐ', 'meaning': 'сравнивать', 'gif': None, 'audio': None},
    38: {'char': '长', 'pinyin': 'cháng/zhǎng', 'meaning': 'длинный / расти', 'gif': None, 'audio': None},
    39: {'char': '身', 'pinyin': 'shēn', 'meaning': 'тело', 'gif': None, 'audio': None},
    40: {'char': '西', 'pinyin': 'xī', 'meaning': 'запад', 'gif': None, 'audio': None},
    41: {'char': '东', 'pinyin': 'dōng', 'meaning': 'восток', 'gif': None, 'audio': None},
    42: {'char': '雨', 'pinyin': 'yǔ', 'meaning': 'дождь', 'gif': None, 'audio': None},
    43: {'char': '气', 'pinyin': 'qì', 'meaning': 'воздух', 'gif': None, 'audio': None},
    44: {'char': '山', 'pinyin': 'shān', 'meaning': 'гора', 'gif': None, 'audio': None},
    45: {'char': '士', 'pinyin': 'shì', 'meaning': 'воин', 'gif': None, 'audio': None},
    46: {'char': '川', 'pinyin': 'chuān', 'meaning': 'поток', 'gif': None, 'audio': None},
    47: {'char': '生', 'pinyin': 'shēng', 'meaning': 'рождаться', 'gif': None, 'audio': None},
    48: {'char': '禾', 'pinyin': 'hé', 'meaning': 'злак', 'gif': None, 'audio': None},
    49: {'char': '贝', 'pinyin': 'bèi', 'meaning': 'раковина, деньги', 'gif': None, 'audio': None},
    50: {'char': '玉', 'pinyin': 'yù', 'meaning': 'яшма', 'gif': None, 'audio': None},
    51: {'char': '金', 'pinyin': 'jīn', 'meaning': 'золото, металл', 'gif': None, 'audio': None},
    52: {'char': '皮', 'pinyin': 'pí', 'meaning': 'кожа', 'gif': None, 'audio': None},
    53: {'char': '风', 'pinyin': 'fēng', 'meaning': 'ветер', 'gif': None, 'audio': None},
    54: {'char': '牛', 'pinyin': 'niú', 'meaning': 'корова', 'gif': None, 'audio': None},
    55: {'char': '羊', 'pinyin': 'yáng', 'meaning': 'баран', 'gif': None, 'audio': None},
    56: {'char': '鱼', 'pinyin': 'yú', 'meaning': 'рыба', 'gif': None, 'audio': None},
    57: {'char': '肉', 'pinyin': 'ròu', 'meaning': 'мясо', 'gif': None, 'audio': None},
    58: {'char': '白', 'pinyin': 'bái', 'meaning': 'белый', 'gif': None, 'audio': None},
    59: {'char': '黑', 'pinyin': 'hēi', 'meaning': 'чёрный', 'gif': None, 'audio': None},
    60: {'char': '黄', 'pinyin': 'huáng', 'meaning': 'жёлтый', 'gif': None, 'audio': None},
    61: {'char': '小', 'pinyin': 'xiǎo', 'meaning': 'маленький', 'gif': None, 'audio': None},
    62: {'char': '高', 'pinyin': 'gāo', 'meaning': 'высокий', 'gif': None, 'audio': None},
    63: {'char': '户', 'pinyin': 'hù', 'meaning': 'двор', 'gif': None, 'audio': None},
    64: {'char': '食', 'pinyin': 'shí', 'meaning': 'еда', 'gif': None, 'audio': None},
    65: {'char': '衣', 'pinyin': 'yī', 'meaning': 'одежда', 'gif': None, 'audio': None},
    66: {'char': '工', 'pinyin': 'gōng', 'meaning': 'работа', 'gif': None, 'audio': None},
    67: {'char': '片', 'pinyin': 'piàn', 'meaning': 'доска', 'gif': None, 'audio': None},
    68: {'char': '方', 'pinyin': 'fāng', 'meaning': 'квадрат', 'gif': None, 'audio': None},
    69: {'char': '网', 'pinyin': 'wǎng', 'meaning': 'сеть', 'gif': None, 'audio': None},
    70: {'char': '飞', 'pinyin': 'fēi', 'meaning': 'летать', 'gif': None, 'audio': None},
    71: {'char': '车', 'pinyin': 'chē', 'meaning': 'машина', 'gif': None, 'audio': None},
}

# Распределение по дням: день 1: id 1-10, день 2: 11-20, …, день 7: 61-71
day_to_ids = {1: list(range(1,11)), 2: list(range(11,21)), 3: list(range(21,31)),
              4: list(range(31,41)), 5: list(range(41,51)), 6: list(range(51,61)),
              7: list(range(61,72))}

# ======================= ХРАНЕНИЕ ДАННЫХ =======================
DATA_DIR = '/data' if os.path.exists('/data') else '.'
PROGRESS_FILE = os.path.join(DATA_DIR, 'user_progress.json')
VOICE_FILE = os.path.join(DATA_DIR, 'voice_state.json')
RESULTS_FILE = os.path.join(DATA_DIR, 'game_results.txt')

def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        return {}
    with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_progress(progress):
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)

def load_voice_state():
    if not os.path.exists(VOICE_FILE):
        return {}
    with open(VOICE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_voice_state(state):
    with open(VOICE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f)

def save_result(user_id, score, total, ending):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(RESULTS_FILE, 'a', encoding='utf-8') as f:
        f.write(f"[{timestamp}] {user_id}: {ending} ({score}/{total})\n")

# ======================= СОСТОЯНИЯ ПОЛЬЗОВАТЕЛЯ =======================
user_states = {}

def default_state():
    return {
        'day': 1,
        'studied': [],
        'score': 0,
        'total_tested': 0,
        'current_new_graphemes': [],
        'current_new_index': 0,
        'test_questions': [],          # список (gid, correct_meaning) – только перевод!
        'test_index': 0,
        'test_correct': 0,
        'test_wrong': [],
        'test_options': [],
        'test_correct_option': '',
        'waiting_test': False,
        'final_test_done': False
    }

def get_grapheme(gid):
    return graphemes.get(gid)

# ======================= ОБРАБОТЧИКИ КОМАНД =======================
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(
        "🇨🇳 Добро пожаловать в «Китайский квест»!\n"
        "Вы студент, готовитесь к HSK. У вас 7 дней.\n"
        "Каждый день изучайте 10–11 новых иероглифов (GIF написания + пиньинь + перевод).\n"
        "После изучения дня можно пройти тест только по этим иероглифам.\n"
        "В любой момент доступен финальный тест по всем 71 иероглифу.\n\n"
        "В тесте показывается GIF иероглифа, а варианты ответа — переводы на русский язык.\n\n"
        "Нажмите кнопку, чтобы начать!",
        reply_markup=main_menu()
    )

@dp.callback_query_handler(lambda c: c.data == 'new_game')
async def new_game(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    state = default_state()
    all_prog = load_progress()
    if str(user_id) in all_prog:
        saved = all_prog[str(user_id)]
        state['day'] = saved.get('day', 1)
        state['studied'] = saved.get('studied', [])
        state['score'] = saved.get('score', 0)
        state['total_tested'] = saved.get('total_tested', 0)
        state['final_test_done'] = saved.get('final_test_done', False)
    user_states[user_id] = state
    await show_day_menu(user_id, callback_query.message)
    await bot.answer_callback_query(callback_query.id)

async def show_day_menu(user_id, message_to_edit=None):
    state = user_states.get(user_id)
    if not state:
        return
    day = state['day']
    day_ids = day_to_ids.get(day, [])
    unstudied = [gid for gid in day_ids if gid not in state['studied']]
    has_unstudied = len(unstudied) > 0
    has_day_graphemes = len(day_ids) > 0
    final_test_available = (day == 7 and not state['final_test_done']) or (day > 7)
    kb = day_menu(day, has_unstudied, has_day_graphemes, final_test_available)
    text = f"День {day} из 7. Выберите действие:"
    if message_to_edit:
        await bot.edit_message_text(text, user_id, message_to_edit.message_id, reply_markup=kb)
    else:
        await bot.send_message(user_id, text, reply_markup=kb)

# ---------- ИЗУЧЕНИЕ НОВЫХ ИЕРОГЛИФОВ ----------
@dp.callback_query_handler(lambda c: c.data.startswith('study_day_'))
async def study_day(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    day_num = int(callback_query.data.split('_')[2])
    state = user_states.get(user_id)
    if not state or state['day'] != day_num:
        await bot.answer_callback_query(callback_query.id, "Ошибка: начните игру заново.")
        return
    day_ids = day_to_ids[day_num]
    new_ids = [gid for gid in day_ids if gid not in state['studied']]
    if not new_ids:
        await bot.send_message(user_id, f"Все иероглифы дня {day_num} уже изучены.")
        await bot.delete_message(user_id, callback_query.message.message_id)
        return
    state['current_new_graphemes'] = new_ids
    state['current_new_index'] = 0
    await send_next_grapheme(user_id, day_num, callback_query.message)
    await bot.answer_callback_query(callback_query.id)

async def send_next_grapheme(user_id, day_num, msg_to_del=None):
    state = user_states.get(user_id)
    if not state:
        return
    if state['current_new_index'] >= len(state['current_new_graphemes']):
        total_new = len(state['current_new_graphemes'])
        await bot.send_message(
            user_id,
            f"Вы изучили все новые иероглифы дня {day_num}!",
            reply_markup=finish_study_keyboard(day_num, total_new)
        )
        if msg_to_del:
            try:
                await bot.delete_message(user_id, msg_to_del.message_id)
            except:
                pass
        return
    gid = state['current_new_graphemes'][state['current_new_index']]
    g = get_grapheme(gid)
    # В КАРТОЧКЕ ИЗУЧЕНИЯ ПОКАЗЫВАЕМ ПИНЬИНЬ И ПЕРЕВОД
    text = f"Иероглиф: {g['char']}\nПиньинь: {g['pinyin']}\nЗначение: {g['meaning']}"
    if g['gif']:
        await bot.send_animation(user_id, g['gif'], caption=text,
                                 reply_markup=grapheme_card_keyboard(gid, day_num))
    else:
        await bot.send_message(user_id, text, reply_markup=grapheme_card_keyboard(gid, day_num))
    if msg_to_del:
        try:
            await bot.delete_message(user_id, msg_to_del.message_id)
        except:
            pass

@dp.callback_query_handler(lambda c: c.data.startswith('next_grapheme_'))
async def next_grapheme(callback_query: types.CallbackQuery):
    parts = callback_query.data.split('_')
    day_num = int(parts[2])
    gid = int(parts[3])
    user_id = callback_query.from_user.id
    state = user_states.get(user_id)
    if not state or state['day'] != day_num:
        return
    if gid not in state['studied']:
        state['studied'].append(gid)
        all_prog = load_progress()
        all_prog[str(user_id)] = {
            'day': state['day'],
            'studied': state['studied'],
            'score': state['score'],
            'total_tested': state['total_tested'],
            'final_test_done': state['final_test_done']
        }
        save_progress(all_prog)
    state['current_new_index'] += 1
    await send_next_grapheme(user_id, day_num, callback_query.message)
    await bot.answer_callback_query(callback_query.id)

# ---------- ЗАВЕРШЕНИЕ ДНЯ ----------
@dp.callback_query_handler(lambda c: c.data.startswith('end_day_'))
async def end_day(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    day_num = int(callback_query.data.split('_')[2])
    state = user_states.get(user_id)
    if not state or state['day'] != day_num:
        return
    total_new = len([gid for gid in day_to_ids[day_num] if gid not in state['studied']])
    if total_new == 0:
        total_new = len(day_to_ids[day_num])
    await bot.edit_message_text(
        f"День {day_num} завершён. Что дальше?",
        user_id, callback_query.message.message_id,
        reply_markup=finish_study_keyboard(day_num, total_new)
    )
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data.startswith('next_day_'))
async def next_day(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    next_day_num = int(callback_query.data.split('_')[2])
    state = user_states.get(user_id)
    if not state:
        return
    if next_day_num > 7:
        await show_day_menu(user_id, callback_query.message)
        return
    state['day'] = next_day_num
    all_prog = load_progress()
    all_prog[str(user_id)] = {
        'day': state['day'],
        'studied': state['studied'],
        'score': state['score'],
        'total_tested': state['total_tested'],
        'final_test_done': state['final_test_done']
    }
    save_progress(all_prog)
    await show_day_menu(user_id, callback_query.message)
    await bot.answer_callback_query(callback_query.id)

# ---------- ТЕСТ ДНЯ (только перевод на русском) ----------
@dp.callback_query_handler(lambda c: c.data.startswith('test_day_'))
async def test_day(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    day_num = int(callback_query.data.split('_')[2])
    state = user_states.get(user_id)
    if not state:
        return
    day_ids = day_to_ids[day_num]
    test_ids = [gid for gid in day_ids if gid in state['studied']]
    if not test_ids:
        await bot.answer_callback_query(callback_query.id, "Сначала выучите иероглифы этого дня!")
        return
    # ВОПРОСЫ: (gid, correct_meaning) – только перевод
    questions = [(gid, graphemes[gid]['meaning']) for gid in test_ids]
    random.shuffle(questions)
    state['test_questions'] = questions
    state['test_index'] = 0
    state['test_correct'] = 0
    state['test_wrong'] = []
    state['waiting_test'] = True
    state['current_test_is_final'] = False
    await send_test_question(user_id, callback_query.message)
    await bot.answer_callback_query(callback_query.id)

# ---------- ФИНАЛЬНЫЙ ТЕСТ (все 71, только перевод) ----------
@dp.callback_query_handler(lambda c: c.data == 'final_test')
async def final_test(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    state = user_states.get(user_id)
    if not state:
        return
    if state['final_test_done']:
        await bot.answer_callback_query(callback_query.id, "Финальный тест уже пройден. Завершите игру.")
        return
    questions = [(gid, graphemes[gid]['meaning']) for gid in graphemes.keys()]
    random.shuffle(questions)
    state['test_questions'] = questions
    state['test_index'] = 0
    state['test_correct'] = 0
    state['test_wrong'] = []
    state['waiting_test'] = True
    state['current_test_is_final'] = True
    await send_test_question(user_id, callback_query.message)
    await bot.answer_callback_query(callback_query.id)

async def send_test_question(user_id, msg_to_del=None):
    state = user_states.get(user_id)
    if not state or not state.get('waiting_test'):
        return
    idx = state['test_index']
    total = len(state['test_questions'])
    if idx >= total:
        correct = state['test_correct']
        wrong_ids = state['test_wrong']
        percent = (correct / total * 100) if total > 0 else 0
        out = f"📊 Тест завершён!\nПравильных ответов: {correct} из {total} ({percent:.1f}%).\n"
        if wrong_ids:
            wrong_chars = [graphemes[gid]['char'] for gid in wrong_ids]
            out += f"\n❌ Рекомендуем повторить: {', '.join(wrong_chars)}"
        else:
            out += "\n🎉 Отлично! Ошибок нет!"
        await bot.send_message(user_id, out)
        state['waiting_test'] = False
        state['total_tested'] += total
        state['score'] += correct
        if state.get('current_test_is_final'):
            state['final_test_done'] = True
        all_prog = load_progress()
        all_prog[str(user_id)] = {
            'day': state['day'],
            'studied': state['studied'],
            'score': state['score'],
            'total_tested': state['total_tested'],
            'final_test_done': state['final_test_done']
        }
        save_progress(all_prog)
        await show_day_menu(user_id, None)
        if msg_to_del:
            try:
                await bot.delete_message(user_id, msg_to_del.message_id)
            except:
                pass
        return
    gid, correct_meaning = state['test_questions'][idx]
    g = graphemes[gid]
    # ГЕНЕРИРУЕМ 3 ВАРИАНТА ПЕРЕВОДА (без пиньиня)
    other_meanings = [v['meaning'] for k, v in graphemes.items() if k != gid]
    random.shuffle(other_meanings)
    options = [correct_meaning] + other_meanings[:2]
    random.shuffle(options)
    state['test_options'] = options
    state['test_correct_option'] = correct_meaning
    # ВОПРОС: только GIF иероглифа, без пиньиня и перевода
    caption = f"❓ Вопрос {idx+1} из {total}: Что означает этот иероглиф?"
    if g['gif']:
        await bot.send_animation(user_id, g['gif'], caption=caption,
                                 reply_markup=test_keyboard(idx, options))
    else:
        await bot.send_message(user_id, f"{g['char']}\n{caption}",
                               reply_markup=test_keyboard(idx, options))
    if msg_to_del:
        try:
            await bot.delete_message(user_id, msg_to_del.message_id)
        except:
            pass

@dp.callback_query_handler(lambda c: c.data.startswith('test_ans_'))
async def test_answer(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    state = user_states.get(user_id)
    if not state or not state.get('waiting_test'):
        await bot.answer_callback_query(callback_query.id, "Тест не активен")
        return
    parts = callback_query.data.split('_')
    q_index = int(parts[2])
    opt_index = int(parts[3])
    if q_index != state['test_index']:
        await bot.answer_callback_query(callback_query.id, "Устаревший вопрос")
        return
    correct = state['test_correct_option']
    chosen = state['test_options'][opt_index]
    gid, _ = state['test_questions'][q_index]
    if chosen == correct:
        state['test_correct'] += 1
        feedback = f"✅ Правильно! {correct}"
    else:
        feedback = f"❌ Неправильно. Правильный ответ: {correct}"
        if gid not in state['test_wrong']:
            state['test_wrong'].append(gid)
    await bot.edit_message_text(feedback, user_id, callback_query.message.message_id, reply_markup=None)
    state['test_index'] += 1
    await send_test_question(user_id, None)
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data == 'cancel_test')
async def cancel_test(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    state = user_states.get(user_id)
    if state:
        state['waiting_test'] = False
    await bot.edit_message_text("Тест прерван.", user_id, callback_query.message.message_id)
    await show_day_menu(user_id, None)
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data == 'game_over')
async def game_over(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    state = user_states.get(user_id)
    if not state:
        return
    total = state['total_tested']
    score = state['score']
    percent = (score / total * 100) if total > 0 else 0
    if percent >= 80:
        ending = "Отлично (HSK сдан на высокий балл)"
    elif percent >= 50:
        ending = "Удовлетворительно (HSK сдан)"
    else:
        ending = "Провал (HSK не сдан)"
    if len(state['studied']) == len(graphemes):
        ending += " + Секретная концовка (выучены все иероглифы!)"
    save_result(user_id, score, total, ending)
    await bot.edit_message_text(
        f"🎉 Игра завершена!\nВаш результат: {score} из {total} правильных.\nКонцовка: {ending}\n\n"
        "Нажмите кнопку, чтобы начать новую игру.",
        user_id, callback_query.message.message_id,
        reply_markup=end_game_keyboard()
    )
    await bot.answer_callback_query(callback_query.id)

# ---------- ОЗВУЧИВАНИЕ ----------
@dp.callback_query_handler(lambda c: c.data.startswith('voice_'))
async def voice_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    gid = int(callback_query.data.split('_')[1])
    g = get_grapheme(gid)
    if not g or not g['audio']:
        await bot.answer_callback_query(callback_query.id, "Аудио пока нет")
        return
    voice_state = load_voice_state()
    old_msg_id = voice_state.get(str(user_id))
    if old_msg_id:
        try:
            await bot.delete_message(user_id, int(old_msg_id))
        except:
            pass
    msg = await bot.send_voice(user_id, g['audio'])
    voice_state[str(user_id)] = msg.message_id
    save_voice_state(voice_state)
    await bot.answer_callback_query(callback_query.id)

# ВРЕМЕННЫЙ ОБРАБОТЧИК ДЛЯ ПОЛУЧЕНИЯ FILE_ID
@dp.message_handler(content_types=['animation', 'voice'])
async def get_file_id_handler(message: types.Message):
    if message.animation:
        file_id = message.animation.file_id
        await message.reply(f"GIF file_id:\n`{file_id}`")
    elif message.voice:
        file_id = message.voice.file_id
        await message.reply(f"Audio file_id:\n`{file_id}`")
        
# ---------- ЗАПУСК ----------
async def on_startup(dp):
    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("Бот запущен")

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)