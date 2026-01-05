from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎵 Предложить трек", callback_data="suggest")],
        [InlineKeyboardButton(text="📂 Плейлисты", callback_data="playlists")],
        [InlineKeyboardButton(text="🔒 VPN", callback_data="vpn")],
        [InlineKeyboardButton(text="❓ Помощь", callback_data="help")]
    ])


def admin_panel():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📥 Предложенные треки", callback_data="admin_tracks")],
        [InlineKeyboardButton(text="❓ Вопросы", callback_data="admin_questions")],
        [InlineKeyboardButton(text="👥 Пользователи", callback_data="admin_users")],
        [InlineKeyboardButton(text="⬅️ В меню", callback_data="menu")]
    ])
