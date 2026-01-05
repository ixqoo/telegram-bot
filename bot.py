def admin_panel():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📥 Предложенные треки", callback_data="admin_tracks")],
        [InlineKeyboardButton(text="❓ Вопросы", callback_data="admin_questions")],
        [InlineKeyboardButton(text="👥 Пользователи", callback_data="admin_users")],
        [InlineKeyboardButton(text="🔒 Выйти", callback_data="menu")]
    ])

@dp.message(F.text == "/admin88")
async def admin_login(msg: Message, state: FSMContext):
    await msg.answer("🔐 Укажите пароль")
    await state.set_state(AdminState.waiting_password)

@dp.message(AdminState.waiting_password)
async def check_password(msg: Message, state: FSMContext):
    if msg.text == ADMIN_PASSWORD and msg.from_user.id in ADMIN_IDS:
        await msg.answer("👑 Админ панель", reply_markup=admin_panel())
    else:
        await msg.answer("❌ Нет доступа")
    await state.clear()

@dp.callback_query(F.data == "admin_tracks")
async def show_tracks(call: CallbackQuery):
    tracks = get_tracks()
    if not tracks:
        await call.message.answer("Треков нет")
        return

    text = "🎵 Предложенные треки:\n\n"
    for t in tracks:
        text += f"ID:{t[0]} | {t[2]}\n{t[3]}\n\n"

    await call.message.answer(text)

@dp.callback_query(F.data == "admin_questions")
async def show_questions(call: CallbackQuery):
    questions = get_questions()
    if not questions:
        await call.message.answer("Вопросов нет")
        return

    for q in questions:
        await call.message.answer(
            f"❓ Вопрос:\n{q[2]}",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text="✉️ Ответить",
                    callback_data=f"reply_{q[1]}"
                )]
            ])
        )

  @dp.callback_query(F.data == "admin_users")
async def users(call: CallbackQuery):
    users = get_users()
    await call.message.answer(f"👥 Всего пользователей: {len(users)}")
