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
    repeat_grapheme_card_keyboard, test_keyboard, end_game_keyboard
)

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# ======================= БАЗА ГРАФЕМ (71 иероглиф) =======================
# Все file_id реальные (часть получена, остальные будут заменены по мере получения)
graphemes = {
    1: {'char': '人', 'pinyin': 'rén', 'meaning': 'человек', 'gif': 'CgACAgIAAyEFAATUCKVhAANNahcBZ9qEao7mbO2hwxYc5JszZkAAAoGdAAIEQLhI1OsNgdeZp-o7BA', 'voice': 'CQACAgIAAyEFAATUCKVhAANrahczev-uCAo8Q5l02mjOmT_mFowAAqmnAAKPt7hIoqyCsgABcUqGOwQ'},
    2: {'char': '大', 'pinyin': 'dà', 'meaning': 'большой', 'gif': 'CgACAgIAAyEFAATUCKVhAANOahcCF1X17Sdi-XmQ8k2Zb_6kjjgAAoadAAIEQLhIf34J0DpiPXA7BA', 'voice': 'CQACAgIAAyEFAATUCKVhAANsahczeqfnNDXqcTBWa6PVrM31F30AApunAAKPt7hIM3MLp5yn6Yc7BA'},
    3: {'char': '天', 'pinyin': 'tiān', 'meaning': 'небо', 'gif': 'CgACAgIAAyEFAATUCKVhAANRahcDXgayrUDkAWQ8_m6HTuZXtpYAApmdAAIEQLhI1bqaBiYj0_87BA', 'voice': 'CQACAgIAAyEFAATUCKVhAANuahczerxQfK7cdOPsRzu0P6mOp2YAApanAAKPt7hIEN5OnCf6-RQ7BA'},
    4: {'char': '口', 'pinyin': 'kǒu', 'meaning': 'рот', 'gif': 'CgACAgIAAyEFAATUCKVhAANSahcDbQi16L7wi-xgOr1kmHnbdQ8AApudAAIEQLhIryPPeQLjEK87BA', 'voice': 'CQACAgIAAyEFAATUCKVhAANtahczeoEm8DzqY7oF5PeKMbEQuoUAApinAAKPt7hI582PqtVHR2E7BA'},
    5: {'char': '日', 'pinyin': 'rì', 'meaning': 'солнце', 'gif': 'CgACAgIAAyEFAATUCKVhAANTahcEDSijDpO40AWeJpOFYEX1rlgAAqCdAAIEQLhIIzo7XbEQlM47BA', 'voice': 'CQACAgIAAyEFAATUCKVhAANwahczeqQNy8LoKmc8JwSd_RCGmqEAAqCnAAKPt7hIAtpL8OAQ_Tg7BA'},
    6: {'char': '目', 'pinyin': 'mù', 'meaning': 'глаз', 'gif': 'CgACAgIAAyEFAATUCKVhAANWahcUGSPg94WNQehWDrRIeRrU3ToAAnKeAAIEQLhIXbA4U-uQQT47BA', 'voice': 'CQACAgIAAyEFAATUCKVhAANvahczenHFEvRCZsYX99JDZlpPVXgAAqKnAAKPt7hImHz1EKlqOnw7BA'},
    7: {'char': '田', 'pinyin': 'tián', 'meaning': 'поле', 'gif': 'CgACAgIAAyEFAATUCKVhAANXahcUxzv19ylLg3malDyZlIAieVgAAn6eAAIEQLhIXCBqRPjFAAGUOwQ', 'voice': 'CQACAgIAAyEFAATUCKVhAANyahczelUjrvpPYl_wrWAr8rXXgRoAAqOnAAKPt7hIo2rKpK4L8VI7BA'},
    8: {'char': '月', 'pinyin': 'yuè', 'meaning': 'месяц', 'gif': 'CgACAgIAAyEFAATUCKVhAANYahcVgKm8QMXYOYNsOasOqr75XRoAAo-eAAIEQLhI_VMjboJ7uBs7BA', 'voice': 'CQACAgIAAyEFAATUCKVhAANxahczehtm9vOlC0lyV8yBqRwOzdMAAqGnAAKPt7hIcGgu6wUtbYY7BA'},
    9: {'char': '木', 'pinyin': 'mù', 'meaning': 'дерево', 'gif': 'CgACAgIAAyEFAATUCKVhAANZahcWIZ8Gm6AcVBQQxwfd3ehBUCEAApaeAAIEQLhIPSEtBtQWH3c7BA', 'voice': 'CQACAgIAAyEFAATUCKVhAANzahczegJuTIWQVbdlAAGeKzQPPpO1AAKXpwACj7e4SMFNf8Q1Wl0pOwQ'},
    10: {'char': '女', 'pinyin': 'nǚ', 'meaning': 'женщина', 'gif': 'CgACAgIAAyEFAATUCKVhAANaahcW0gyxrpTKevp7M0xb4Tto6iYAAp2eAAIEQLhI89yUy1YpYf07BA', 'voice': 'CQACAgIAAyEFAATUCKVhAAN0ahczejDiSQfEDg7CLqcHDfmmQTgAAqenAAKPt7hIhwABSWycsIl0OwQ'},
    11: {'char': '马', 'pinyin': 'mǎ', 'meaning': 'лошадь', 'gif': 'CgACAgIAAyEFAATUCKVhAANbahcXh6ZEUiZsG9GMXuFssSkED8sAAqOeAAIEQLhIPkoqVT1cO-Y7BA', 'voice': 'CQACAgIAAyEFAATUCKVhAAN2ahczegg3xLcIBW5xCe4QS8DSmI4AAqqnAAKPt7hI5NZ97EtKCrA7BA'},
    12: {'char': '儿', 'pinyin': 'ér', 'meaning': 'идущий человек', 'gif': 'CgACAgIAAyEFAATUCKVhAANiahcezepUk5cOg5QTDKu8V2KohNIAAvWeAAIEQLhI-rLSBwW_aew7BA', 'voice': 'CQACAgIAAyEFAATUCKVhAAN1ahczeiM6tCNZe4xamKTPEnvAE9UAApynAAKPt7hIJwFdbodh9xI7BA'},
    13: {'char': '父', 'pinyin': 'fù', 'meaning': 'отец', 'gif': 'CgACAgIAAyEFAATUCKVhAANgahcdShgxCh_d5TCxqt19YbsWUjEAAuWeAAIEQLhInkMrr_pt0fw7BA', 'voice': 'CQACAgIAAyEFAATUCKVhAAN5ahczevRJZvD4XWUIWplYVp5ZIS8AAp-nAAKPt7hIBrZ-6sH7tEM7BA'},
    14: {'char': '母', 'pinyin': 'mǔ', 'meaning': 'мать', 'gif': 'CgACAgIAAyEFAATUCKVhAANdahcbTBYSZXrCbMojoT82Wy1RPqkAAsmeAAIEQLhI8YjVg58yN0w7BA', 'voice': 'CQACAgIAAyEFAATUCKVhAAN7ahczeiVQviMWO0oMzJMmO3srUpwAAqWnAAKPt7hIEFpswz-Z8bE7BA'},
    15: {'char': '门', 'pinyin': 'mén', 'meaning': 'дверь', 'gif': 'CgACAgIAAyEFAATUCKVhAANeahccRznbErEhHMBi9mWk5TvAaKMAAs2eAAIEQLhIkFASeWvtbr07BA', 'voice': 'CQACAgIAAyEFAATUCKVhAAN3ahczekoEvu4ypmAYpW8egdUT2eoAAqSnAAKPt7hIt35W_KOUv2w7BA'},
    16: {'char': '刀', 'pinyin': 'dāo', 'meaning': 'нож', 'gif': 'CgACAgIAAyEFAATUCKVhAANfahcc4IJZ0n0XxeTbxk79QNNmINIAAtqeAAIEQLhImf1e-lYYGg07BA', 'voice': 'voice_16'},
    17: {'char': 'ヒ', 'pinyin': 'bǐ', 'meaning': 'черпак, кинжал', 'gif': 'CgACAgIAAyEFAATUCKVhAANhahceQVSCZCdjEjPOcbeYXU2YixgAAvKeAAIEQLhIZeJjnF-Mbpk7BA', 'voice': 'CQACAgIAAyEFAATUCKVhAAN4ahczemr1VdyyAnNV5cBwvEb8w0YAAqanAAKPt7hI7oZrMcl7F9A7BA'},
    18: {'char': '米', 'pinyin': 'mǐ', 'meaning': 'рис', 'gif': 'CgACAgIAAyEFAATUCKVhAANjahcf2-N6mA1Bzyjll-gOdLkkTdYAAv6eAAIEQLhIej0zwBQjbwo7BA', 'voice': 'CQACAgIAAyEFAATUCKVhAAN6ahczehUlv7fh_2XUGCvubb-GxqMAAqinAAKPt7hIlp8DwGQil4A7BA'},
    19: {'char': '水', 'pinyin': 'shuǐ', 'meaning': 'вода', 'gif': 'CgACAgIAAyEFAATUCKVhAANkahcgjZjXyQcx3Y1TmJl9eegAAYzQAAIInwACBEC4SALiJnzkLQ6vOwQ', 'voice': 'CQACAgIAAyEFAATUCKVhAAN9ahczettiJjAND1vrtYv-JGHmpBwAApmnAAKPt7hIiSEXNMG_Ntw7BA'},
    20: {'char': '火', 'pinyin': 'huǒ', 'meaning': 'огонь', 'gif': 'CgACAgIAAyEFAATUCKVhAANlahchPpSYlBrLT2J54TKFNf8f57cAAhGfAAIEQLhI0RJKW-dZpH07BA', 'voice': 'CQACAgIAAyEFAATUCKVhAAN-ahczehjqUofMnU7cdeAf4katqSgAAp2nAAKPt7hIZEQClT4Twnc7BA'},
    21: {'char': '毛', 'pinyin': 'máo', 'meaning': 'шерсть', 'gif': 'CgACAgIAAyEFAATUCKVhAANmahciGcsnhLicu1YCkJTPxaTSvLgAAiWfAAIEQLhIlYSSAljrT-87BA', 'voice': 'CQACAgIAAyEFAATUCKVhAAN8ahczevC7lqwypM93nkOr5D2kINMAAp6nAAKPt7hISaQD-G-mkpk7BA'},
    22: {'char': '手', 'pinyin': 'shǒu', 'meaning': 'рука', 'gif': 'CgACAgIAAyEFAATUCKVhAANnahcil1ofSeDhHw5OcWUbVyn5fd4AAi6fAAIEQLhIbshVLgj0jXo7BA', 'voice': 'voice_22'},
    23: {'char': '又', 'pinyin': 'yòu', 'meaning': 'ладонь правой руки', 'gif': 'CgACAgIAAyEFAATUCKVhAANoahcj29hb8NZth9fCAAFR6WFbX2BAAAJBnwACBEC4SCe1NQxAnlopOwQ', 'voice': 'voice_23'},
    24: {'char': '足', 'pinyin': 'zú', 'meaning': 'нога, ступня', 'gif': 'gif_24', 'voice': 'CgACAgIAAyEFAATUCKVhAANpahckYbSgNM4qlfysZ8YKkc0L5PUAAkifAAIEQLhI0sDGnRNXFNQ7BA'},
    25: {'char': '走', 'pinyin': 'zǒu', 'meaning': 'идти', 'gif': 'CgACAgIAAyEFAATUCKVhAANqahcloJnJPdYtzCuRyCw3aRp5DhIAAl6fAAIEQLhIghJ7e7p_x_w7BA', 'voice': 'voice_25'},
    26: {'char': '行', 'pinyin': 'xíng', 'meaning': 'движение', 'gif': 'gif_26', 'voice': 'voice_26'},
    27: {'char': '舌', 'pinyin': 'shé', 'meaning': 'язык', 'gif': 'gif_27', 'voice': 'voice_27'},
    28: {'char': '言', 'pinyin': 'yán', 'meaning': 'речь', 'gif': 'gif_28', 'voice': 'voice_28'},
    29: {'char': '立', 'pinyin': 'lì', 'meaning': 'стоять', 'gif': 'gif_29', 'voice': 'voice_29'},
    30: {'char': '音', 'pinyin': 'yīn', 'meaning': 'звук', 'gif': 'gif_30', 'voice': 'voice_30'},
    31: {'char': '面', 'pinyin': 'miàn', 'meaning': 'лицо, мука', 'gif': 'gif_31', 'voice': 'voice_31'},
    32: {'char': '见', 'pinyin': 'jiàn', 'meaning': 'видеться', 'gif': 'gif_32', 'voice': 'voice_32'},
    33: {'char': '耳', 'pinyin': 'ěr', 'meaning': 'ухо', 'gif': 'gif_33', 'voice': 'voice_33'},
    34: {'char': '页', 'pinyin': 'yè', 'meaning': 'страница', 'gif': 'gif_34', 'voice': 'voice_34'},
    35: {'char': '牙', 'pinyin': 'yá', 'meaning': 'зуб', 'gif': 'gif_35', 'voice': 'voice_35'},
    36: {'char': '文', 'pinyin': 'wén', 'meaning': 'письмена', 'gif': 'gif_36', 'voice': 'voice_36'},
    37: {'char': '比', 'pinyin': 'bǐ', 'meaning': 'сравнивать', 'gif': 'gif_37', 'voice': 'voice_37'},
    38: {'char': '长', 'pinyin': 'cháng/zhǎng', 'meaning': 'длинный / расти', 'gif': 'gif_38', 'voice': 'voice_38'},
    39: {'char': '身', 'pinyin': 'shēn', 'meaning': 'тело', 'gif': 'gif_39', 'voice': 'voice_39'},
    40: {'char': '西', 'pinyin': 'xī', 'meaning': 'запад', 'gif': 'gif_40', 'voice': 'voice_40'},
    41: {'char': '东', 'pinyin': 'dōng', 'meaning': 'восток', 'gif': 'gif_41', 'voice': 'voice_41'},
    42: {'char': '雨', 'pinyin': 'yǔ', 'meaning': 'дождь', 'gif': 'gif_42', 'voice': 'voice_42'},
    43: {'char': '气', 'pinyin': 'qì', 'meaning': 'воздух', 'gif': 'gif_43', 'voice': 'voice_43'},
    44: {'char': '山', 'pinyin': 'shān', 'meaning': 'гора', 'gif': 'gif_44', 'voice': 'voice_44'},
    45: {'char': '士', 'pinyin': 'shì', 'meaning': 'воин', 'gif': 'gif_45', 'voice': 'voice_45'},
    46: {'char': '川', 'pinyin': 'chuān', 'meaning': 'поток', 'gif': 'gif_46', 'voice': 'voice_46'},
    47: {'char': '生', 'pinyin': 'shēng', 'meaning': 'рождаться', 'gif': 'gif_47', 'voice': 'voice_47'},
    48: {'char': '禾', 'pinyin': 'hé', 'meaning': 'злак', 'gif': 'gif_48', 'voice': 'voice_48'},
    49: {'char': '贝', 'pinyin': 'bèi', 'meaning': 'раковина, деньги', 'gif': 'gif_49', 'voice': 'voice_49'},
    50: {'char': '玉', 'pinyin': 'yù', 'meaning': 'яшма', 'gif': 'gif_50', 'voice': 'voice_50'},
    51: {'char': '金', 'pinyin': 'jīn', 'meaning': 'золото, металл', 'gif': 'gif_51', 'voice': 'voice_51'},
    52: {'char': '皮', 'pinyin': 'pí', 'meaning': 'кожа', 'gif': 'gif_52', 'voice': 'voice_52'},
    53: {'char': '风', 'pinyin': 'fēng', 'meaning': 'ветер', 'gif': 'gif_53', 'voice': 'voice_53'},
    54: {'char': '牛', 'pinyin': 'niú', 'meaning': 'корова', 'gif': 'gif_54', 'voice': 'voice_54'},
    55: {'char': '羊', 'pinyin': 'yáng', 'meaning': 'баран', 'gif': 'gif_55', 'voice': 'voice_55'},
    56: {'char': '鱼', 'pinyin': 'yú', 'meaning': 'рыба', 'gif': 'gif_56', 'voice': 'voice_56'},
    57: {'char': '肉', 'pinyin': 'ròu', 'meaning': 'мясо', 'gif': 'gif_57', 'voice': 'voice_57'},
    58: {'char': '白', 'pinyin': 'bái', 'meaning': 'белый', 'gif': 'gif_58', 'voice': 'voice_58'},
    59: {'char': '黑', 'pinyin': 'hēi', 'meaning': 'чёрный', 'gif': 'gif_59', 'voice': 'voice_59'},
    60: {'char': '黄', 'pinyin': 'huáng', 'meaning': 'жёлтый', 'gif': 'gif_60', 'voice': 'voice_60'},
    61: {'char': '小', 'pinyin': 'xiǎo', 'meaning': 'маленький', 'gif': 'gif_61', 'voice': 'voice_61'},
    62: {'char': '高', 'pinyin': 'gāo', 'meaning': 'высокий', 'gif': 'gif_62', 'voice': 'voice_62'},
    63: {'char': '户', 'pinyin': 'hù', 'meaning': 'двор', 'gif': 'gif_63', 'voice': 'voice_63'},
    64: {'char': '食', 'pinyin': 'shí', 'meaning': 'еда', 'gif': 'gif_64', 'voice': 'voice_64'},
    65: {'char': '衣', 'pinyin': 'yī', 'meaning': 'одежда', 'gif': 'gif_65', 'voice': 'voice_65'},
    66: {'char': '工', 'pinyin': 'gōng', 'meaning': 'работа', 'gif': 'gif_66', 'voice': 'voice_66'},
    67: {'char': '片', 'pinyin': 'piàn', 'meaning': 'доска', 'gif': 'gif_67', 'voice': 'voice_67'},
    68: {'char': '方', 'pinyin': 'fāng', 'meaning': 'квадрат', 'gif': 'gif_68', 'voice': 'voice_68'},
    69: {'char': '网', 'pinyin': 'wǎng', 'meaning': 'сеть', 'gif': 'gif_69', 'voice': 'voice_69'},
    70: {'char': '飞', 'pinyin': 'fēi', 'meaning': 'летать', 'gif': 'gif_70', 'voice': 'voice_70'},
    71: {'char': '车', 'pinyin': 'chē', 'meaning': 'машина', 'gif': 'gif_71', 'voice': 'voice_71'},
}

# Распределение по дням (1-10, 11-20, ...)
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
        'last_test_result': None,
        'current_new_graphemes': [],
        'current_new_index': 0,
        'repeat_graphemes': [],
        'repeat_index': 0,
        'test_questions': [],
        'test_index': 0,
        'test_correct': 0,
        'test_wrong': [],
        'test_options': [],
        'test_correct_option': '',
        'waiting_test': False,
        'current_test_is_final': False
    }

def get_grapheme(gid):
    return graphemes.get(gid)

# ======================= УСТАНОВКА КОМАНД =======================
async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command="start", description="Начать игру"),
        types.BotCommand(command="help", description="Помощь и инструкция")
    ]
    await bot.set_my_commands(commands)

# ======================= ОБРАБОТЧИКИ =======================
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(
        "🇨🇳 Добро пожаловать в «Китайский квест»!\n"
        "Вы студент, готовитесь к HSK. У вас 7 дней.\n"
        "Каждый день изучайте 10–11 новых иероглифов.\n"
        "После изучения дня можно пройти тест или повторить иероглифы.\n"
        "Тесты можно проходить сколько угодно раз – результаты суммируются.\n"
        "Используйте /help для инструкции.\n\n"
        "Нажмите кнопку, чтобы начать!",
        reply_markup=main_menu()
    )

@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    help_text = (
        "📚 *Инструкция по использованию бота «Китайский квест»*\n\n"
        "1️⃣ *Начало игры*: нажмите «Начать новый квест» или введите /start.\n"
        "2️⃣ *Изучение*: в каждый из 7 дней вы будете учить 10-11 новых иероглифов.\n"
        "   После каждого иероглифа нажмите «Следующий».\n"
        "3️⃣ *Повторение*: после изучения всех иероглифов дня вы можете повторно просмотреть их,\n"
        "   нажав «Повторить иероглифы дня».\n"
        "4️⃣ *Тесты*:\n"
        "   - Тест дня можно проходить в любой момент (кнопка в меню дня).\n"
        "   - Финальный тест (71 иероглиф) доступен на 7-й день.\n"
        "   - Результаты тестов суммируются, а последний результат сохраняется.\n"
        "5️⃣ *Последний тест*: нажмите «📊 Последний тест» в главном меню,\n"
        "   чтобы увидеть результат самого свежего теста.\n"
        "6️⃣ *Завершение*: после 7-го дня завершите игру кнопкой «Завершить игру».\n\n"
        "Удачи в изучении китайского! 🇨🇳"
    )
    await message.reply(help_text, parse_mode="Markdown")

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
        state['last_test_result'] = saved.get('last_test_result', None)
    user_states[user_id] = state
    await show_day_menu(user_id, callback_query.message)
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data == 'last_test')
async def show_last_test(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    state = user_states.get(user_id)
    if not state:
        await bot.answer_callback_query(callback_query.id, "Сначала начните игру (/start)")
        return
    if state['last_test_result']:
        correct, total = state['last_test_result']
        percent = (correct / total * 100) if total > 0 else 0
        await bot.send_message(user_id,
                               f"📊 *Ваш последний тест:* {correct} из {total} правильных ({percent:.1f}%).\n"
                               "Результаты предыдущих тестов суммируются в общую статистику.\n"
                               "Сыграйте ещё, чтобы улучшить результат!",
                               parse_mode="Markdown")
    else:
        await bot.send_message(user_id, "Вы ещё не проходили ни одного теста. Пройдите тест дня или финальный тест!")
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
    kb = day_menu(day, has_unstudied, has_day_graphemes)
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
    await send_next_grapheme(user_id, day_num, callback_query.message, mode='study')
    await bot.answer_callback_query(callback_query.id)

async def send_next_grapheme(user_id, day_num, msg_to_del=None, mode='study'):
    state = user_states.get(user_id)
    if not state:
        return
    if mode == 'study':
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
    else:  # repeat
        if state['repeat_index'] >= len(state['repeat_graphemes']):
            await bot.send_message(user_id, "Повторение завершено. Возвращаемся в меню дня.")
            await show_day_menu(user_id, None)
            if msg_to_del:
                await bot.delete_message(user_id, msg_to_del.message_id)
            return
        gid = state['repeat_graphemes'][state['repeat_index']]

    g = get_grapheme(gid)
    text = f"Иероглиф: {g['char']}\nПиньинь: {g['pinyin']}\nЗначение: {g['meaning']}"
    if mode == 'study':
        kb = grapheme_card_keyboard(gid, day_num, mode='study')
    else:
        kb = repeat_grapheme_card_keyboard(gid, day_num)
    if g['gif']:
        await bot.send_animation(user_id, g['gif'], caption=text, reply_markup=kb)
    else:
        await bot.send_message(user_id, text, reply_markup=kb)
    if msg_to_del:
        try:
            await bot.delete_message(user_id, msg_to_del.message_id)
        except:
            pass

@dp.callback_query_handler(lambda c: c.data.startswith('study_next_'))
async def study_next_grapheme(callback_query: types.CallbackQuery):
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
            'last_test_result': state['last_test_result']
        }
        save_progress(all_prog)
    state['current_new_index'] += 1
    await send_next_grapheme(user_id, day_num, callback_query.message, mode='study')
    await bot.answer_callback_query(callback_query.id)

# ---------- ПОВТОРЕНИЕ ИЕРОГЛИФОВ ДНЯ ----------
@dp.callback_query_handler(lambda c: c.data.startswith('repeat_day_'))
async def repeat_day(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    day_num = int(callback_query.data.split('_')[2])
    state = user_states.get(user_id)
    if not state or state['day'] != day_num:
        await bot.answer_callback_query(callback_query.id, "Ошибка")
        return
    day_ids = day_to_ids[day_num]
    state['repeat_graphemes'] = day_ids.copy()
    state['repeat_index'] = 0
    await send_next_grapheme(user_id, day_num, callback_query.message, mode='repeat')
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data.startswith('repeat_next_'))
async def repeat_next_grapheme(callback_query: types.CallbackQuery):
    parts = callback_query.data.split('_')
    day_num = int(parts[2])
    user_id = callback_query.from_user.id
    state = user_states.get(user_id)
    if not state or state['day'] != day_num:
        return
    state['repeat_index'] += 1
    await send_next_grapheme(user_id, day_num, callback_query.message, mode='repeat')
    await bot.answer_callback_query(callback_query.id)

@dp.callback_query_handler(lambda c: c.data.startswith('end_repeat_'))
async def end_repeat(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    day_num = int(callback_query.data.split('_')[2])
    state = user_states.get(user_id)
    if state:
        state['repeat_graphemes'] = []
        state['repeat_index'] = 0
    await show_day_menu(user_id, callback_query.message)
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
        'last_test_result': state['last_test_result']
    }
    save_progress(all_prog)
    await show_day_menu(user_id, callback_query.message)
    await bot.answer_callback_query(callback_query.id)

# ---------- ТЕСТ ДНЯ ----------
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

# ---------- ФИНАЛЬНЫЙ ТЕСТ ----------
@dp.callback_query_handler(lambda c: c.data == 'final_test')
async def final_test(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    state = user_states.get(user_id)
    if not state:
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
        state['last_test_result'] = (correct, total)
        state['total_tested'] += total
        state['score'] += correct
        all_prog = load_progress()
        all_prog[str(user_id)] = {
            'day': state['day'],
            'studied': state['studied'],
            'score': state['score'],
            'total_tested': state['total_tested'],
            'last_test_result': state['last_test_result']
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
    other_meanings = [v['meaning'] for k, v in graphemes.items() if k != gid]
    random.shuffle(other_meanings)
    options = [correct_meaning] + other_meanings[:2]
    random.shuffle(options)
    state['test_options'] = options
    state['test_correct_option'] = correct_meaning
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
    if not g:
        await bot.answer_callback_query(callback_query.id, "Иероглиф не найден")
        return
    file_id = g.get('voice') or g.get('audio')
    if not file_id:
        await bot.answer_callback_query(callback_query.id, "Аудио для этого иероглифа ещё не добавлено")
        return
    voice_state = load_voice_state()
    old_msg_id = voice_state.get(str(user_id))
    if old_msg_id:
        try:
            await bot.delete_message(user_id, int(old_msg_id))
        except:
            pass
    msg = await bot.send_voice(user_id, file_id)
    voice_state[str(user_id)] = msg.message_id
    save_voice_state(voice_state)
    await bot.answer_callback_query(callback_query.id)

# ---------- ВРЕМЕННЫЙ ОБРАБОТЧИК ДЛЯ ПОЛУЧЕНИЯ FILE_ID (всегда активен) ----------
@dp.message_handler(content_types=['animation', 'voice', 'audio'])
async def get_file_id_handler(message: types.Message):
    if message.animation:
        file_id = message.animation.file_id
        await message.reply(f"GIF file_id:\n`{file_id}`")
    elif message.voice:
        file_id = message.voice.file_id
        await message.reply(f"Voice file_id:\n`{file_id}`")
    elif message.audio:
        file_id = message.audio.file_id
        await message.reply(f"Audio file_id:\n`{file_id}`")

# ---------- ЗАПУСК ----------
async def on_startup(dp):
    await bot.delete_webhook(drop_pending_updates=True)
    await set_commands(bot)
    logging.info("Бот запущен")

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)