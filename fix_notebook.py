import json, re

path = 'railway_accidents_analysis.ipynb'
nb = json.load(open(path, encoding='utf-8'))

# Все emoji-символы которые встречаются в ноутбуке
EMOJI_RE = re.compile(
    '['
    '\U0001F300-\U0001F9FF'   # Misc symbols, emoticons, transport, etc.
    '\U00002600-\U000027BF'   # Misc symbols (✓ ✗ ★ etc.)
    '\U0001FA00-\U0001FFFF'   # Extended symbols
    '\U00002702-\U000027B0'
    '\U000024C2-\U0001F251'
    ']+',
    flags=re.UNICODE
)

fixed_code = 0
fixed_inline = 0

for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        src = ''.join(cell['source'])
        new_src = EMOJI_RE.sub('', src)
        # Убираем лишние пробелы после удаления emoji в начале строк
        new_src = re.sub(r'(?m)^(\s*print\(["\'])(\s+)', r'\1', new_src)
        if new_src != src:
            cell['source'] = new_src
            fixed_code += 1

print(f"Cleaned emojis from {fixed_code} code cells")

# ── Добавляем %matplotlib inline в ячейку с импортами ──────
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'code':
        src = ''.join(cell['source'])
        if 'import matplotlib' in src and '%matplotlib' not in src:
            cell['source'] = '%matplotlib inline\n' + src
            print(f"Added %matplotlib inline to cell {i}")
            break

json.dump(nb, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print("Done.")
