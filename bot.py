```python
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

from config import *
from database import *
from keyboards import *
from states import *

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(F.text == "/start")
async def start(msg: Message):
    add_user(msg.from_user.id, msg.from_user.username)
    await msg.answer("Главное меню 👇", reply_markup=main_menu())


@dp.callback_query(F.data == "menu")
async def back_to_menu(call: CallbackQuery):
    await call.message.edit_text("Главное меню 👇", reply_markup=main_menu())


@dp.callback_query(F.data == "suggest")
async def suggest(call: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Комфортный", callback_data="track_comfort")],
        [InlineKeyboardButton(text="Для игр", callback_data="track_games")],
        [InlineKeyboardButton(text="Рандом", callback_data="track_random")],
        [InlineKeyboardButton(text="⬅️ В меню", callback_data="menu")]
    ])
    await call.message.edit_text("Выбери плейлист:", reply_markup=kb)


@dp.callback_query(F.data.startswith("track_"))
async def choose_track(call: CallbackQuery, state: FSMContext):
    await state.set_state(TrackState.waiting_track)
    await state.update_data(playlist=call.data.replace("track_", ""))
    await call.message.answer("Напишите трек и артиста или ссылку Spotify")


@dp.message(TrackState.waiting_track)
async def save_track_handler(msg: Message, state: FSMContext):
    data = await state.get_data()
    add_track(msg.from_user.id, data["playlist"], msg.text)

    for admin in ADMIN_IDS:
        await bot.send_message(
            admin,
            f"🎵 Новый трек\nПлейлист: {data['playlist']}\n"
            f"От: @{msg.from_user.username}\n\n{msg.text}"
        )

    await msg.answer("✅ Успешно отправлено", reply_markup=main_menu())
    await state.clear()


@dp.callback_query(F.data == "playlists")
async def playlists(call: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Комфортный", callback_data="pl_comfort")],
        [InlineKeyboardButton(text="Для игр", callback_data="pl_games")],
        [InlineKeyboardButton(text="Рандом", callback_data="pl_random")],
        [InlineKeyboardButton(text="⬅️ В меню", callback_data="menu")]
    ])
    await call.message.edit_text("Плейлисты:", reply_markup=kb)


@dp.callback_query(F.data.startswith("pl_"))
async def playlist_link(call: CallbackQuery):
    key = call.data.replace("pl_", "")
    await call.message.edit_text(
        "Готово 👇",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="▶️ Открыть", url=PLAYLIST_LINKS[key])],
            [InlineKeyboardButton(text="⬅️ В меню", callback_data="menu")]
        ])
    )


@dp.callback_query(F.data == "vpn")
async def vpn(call: CallbackQuery):
    await call.message.edit_text(
        "Хороший VPN для YouTube, Discord, TikTok, Spotify.\n30 дней бесплатно",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Подключить VPN", url=VPN_LINK)],
            [InlineKeyboardButton(text="⬅️ В меню", callback_data="menu")]
        ])
    )


@dp.callback_query(F.data == "help")
async def help_start(call: CallbackQuery, state: FSMContext):
    await state.set_state(HelpState.waiting_question)
    await call.message.answer("Напишите свой вопрос")


@dp.message(HelpState.waiting_question)
async def help_send(msg: Message, state: FSMContext):
    add_question(msg.from_user.id, msg.text)

    for admin in ADMIN_IDS:
        await bot.send_message(
            admin,
            f"❓ Вопрос от @{msg.from_user.username}\n\n{msg.text}",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="✉️ Ответить",
                    callback_data=f"reply_{msg.from_user.id}"
                )]
            ])
        )

    await msg.answer("📨 Вопрос отправлен", reply_markup=main_menu())
    await state.clear()


@dp.callback_query(F.data.startswith("reply_"))
async def reply_start(call: CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.reply_user)
    await state.update_data(user_id=int(call.data.split("_")[1]))
    await call.message.answer("Введите ответ пользователю")


@dp.message(AdminState.reply_user)
async def reply_send(msg: Message, state: FSMContext):
    data = await state.get_data()
    await bot.send_message(
        data["user_id"],
        f"💬 Ответ поддержки:\n{msg.text}"
    )
    await msg.answer("✅ Ответ отправлен")
    await state.clear()


@dp.message(F.text == "/admin88")
async def admin_login(msg: Message, state: FSMContext):
    await state.set_state(AdminState.waiting_password)
    await msg.answer("Введите пароль")


@dp.message(AdminState.waiting_password)
async def admin_check(msg: Message, state: FSMContext):
    if msg.text == ADMIN_PASSWORD and msg.from_user.id in ADMIN_IDS:
        await msg.answer("👑 Админ-панель", reply_markup=admin_panel())
    else:
        await msg.answer("❌ Нет доступа")
    await state.clear()


@dp.callback_query(F.data == "admin_tracks")
async def admin_tracks(call: CallbackQuery):
    rows = get_tracks()
    if not rows:
        await call.message.answer("Треков нет")
        return

    text = "🎵 Треки:\n\n"
    for r in rows:
        text += f"{r[0]}:\n{r[1]}\n\n"

    await call.message.answer(text)


@dp.callback_query(F.data == "admin_questions")
async def admin_questions(call: CallbackQuery):
    rows = get_questions()
    if not rows:
        await call.message.answer("Вопросов нет")
        return

    for r in rows:
        await call.message.answer(
            f"❓ Вопрос:\n{r[1]}",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="✉️ Ответить",
                    callback_data=f"reply_{r[0]}"
                )]
            ])
        )


@dp.callback_query(F.data == "admin_users")
async def admin_users(call: CallbackQuery):
    await call.message.answer(
        f"👥 Пользователей: {get_users_count()}"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
```
