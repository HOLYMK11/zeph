def box(title, text):
    lines = ['╭─ ' + title + ' ─╮']
    lines += text.splitlines()
    lines.append('╰' + '─' * (len(title) + 2) + '╯')
    return '```' + '\n'.join(lines) + '```'
