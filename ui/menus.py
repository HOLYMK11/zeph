from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
def compact_buttons(items, per_row=1):
    rows = []
    row = []
    for i, it in enumerate(items):
        row.append(InlineKeyboardButton(it[0], callback_data=it[1]))
        if len(row) == per_row:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return InlineKeyboardMarkup(inline_keyboard=rows)
