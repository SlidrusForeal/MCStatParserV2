import json
import pandas as pd
import os
import requests

# Указываем директорию с файлами JSON
DIRECTORY = "а"
FILES = sorted(os.listdir(DIRECTORY))

# Определяем список метрик
COLUMNS = [
    'UUID', 'Время в игре', 'Кол-во смертей', 'Выброшено предметов',
    'Выведено животных', 'Зачаровано предметов', 'Крался', 'Нанесено урона',
    'Поймано рыбы', 'Получено урона', 'Преодолено бегом',
    'Преодолено в полёте', 'Преодолено вплавь', 'Преодолено на элитрах',
    'Прыжков', 'Съедено кусков торта', 'Убито игроков', 'Убито существ'
]

# Функция для извлечения данных из JSON
def extract_stat(stats, category, key):
    return stats.get(category, {}).get(key, 'None')

# Создаем DataFrame
df = pd.DataFrame(columns=COLUMNS)

# Обрабатываем файлы
for file in FILES:
    file_path = os.path.join(DIRECTORY, file)
    with open(file_path, encoding='utf-8') as f:
        data = json.load(f)
    
    uuid = file[:-5]  # Убираем ".json"
    response = requests.get(f'https://api.mojang.com/user/profile/{uuid}')
    username = response.json().get('name', 'Unknown')
    
    stats = data.get('stats', {}).get('minecraft:custom', {})
    
    row = [
        username,
        extract_stat(stats, 'minecraft:custom', 'minecraft:play_one_minute') / 20 / 60 / 60,
        extract_stat(stats, 'minecraft:custom', 'minecraft:deaths'),
        extract_stat(stats, 'minecraft:custom', 'minecraft:drop'),
        extract_stat(stats, 'minecraft:custom', 'minecraft:animals_bred'),
        extract_stat(stats, 'minecraft:custom', 'minecraft:enchant_item'),
        extract_stat(stats, 'minecraft:custom', 'minecraft:sneak_time'),
        extract_stat(stats, 'minecraft:custom', 'minecraft:damage_dealt'),
        extract_stat(stats, 'minecraft:custom', 'minecraft:fish_caught'),
        extract_stat(stats, 'minecraft:custom', 'minecraft:damage_taken'),
        extract_stat(stats, 'minecraft:custom', 'minecraft:sprint_one_cm'),
        extract_stat(stats, 'minecraft:custom', 'minecraft:fly_one_cm'),
        extract_stat(stats, 'minecraft:custom', 'minecraft:swim_one_cm'),
        extract_stat(stats, 'minecraft:custom', 'minecraft:aviate_one_cm'),
        extract_stat(stats, 'minecraft:custom', 'minecraft:jump'),
        extract_stat(stats, 'minecraft:custom', 'minecraft:eat_cake_slice'),
        extract_stat(stats, 'minecraft:custom', 'minecraft:player_kills'),
        extract_stat(stats, 'minecraft:custom', 'minecraft:mob_kills')
    ]
    
    df.loc[len(df)] = row
    print(f"Обработан файл: {file}")

# Сохранение результата
output_file = 'minecraft_stats.csv'
df.to_csv(output_file, index=False)
print(f"Данные сохранены в {output_file}")
