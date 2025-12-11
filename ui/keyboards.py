from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
def main_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('🤖 AI', callback_data='menu_ai')],
        [InlineKeyboardButton('🎵 Downloaders', callback_data='menu_downloaders')],
        [InlineKeyboardButton('🧰 Tools', callback_data='menu_tools')],
        [InlineKeyboardButton('🎮 Games', callback_data='menu_games')],
        [InlineKeyboardButton('⭐ Premium', callback_data='menu_premium')],
        [InlineKeyboardButton('👤 Profile', callback_data='menu_profile')],
        [InlineKeyboardButton('❓ Help', callback_data='menu_help')]
    ])
    return kb

def payment_kb(pid):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Approve', callback_data=f'approve_{pid}'), InlineKeyboardButton('Reject', callback_data=f'reject_{pid}')],
        [InlineKeyboardButton('Back', callback_data='menu_profile')]
    ])
