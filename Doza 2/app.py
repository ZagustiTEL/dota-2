from flask import Flask, render_template, request, jsonify
import random
import sqlite3
import os

app = Flask(__name__)

# Имя базы данных
DB_NAME = 'Doza.db'

def init_db():
    """Инициализация базы данных и создание таблиц"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Таблица героев
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS heroes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')
    
    # Таблица предметов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL
        )
    ''')
    
    # Таблица стратегий прокачки
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS skill_builds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            description TEXT NOT NULL
        )
    ''')
    
    # Таблица линий
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lanes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')

    # В файл app.py, в функцию init_db(), добавить:
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS generation_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hero TEXT NOT NULL,
        lane TEXT NOT NULL,
        skill_build TEXT NOT NULL,
        starting_items TEXT NOT NULL,
        early_game TEXT NOT NULL,
        core_items TEXT NOT NULL,
        late_game TEXT NOT NULL,
        neutral_items TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
         )
    ''')
    
    conn.commit()
    conn.close()

def populate_db():
    """Заполнение базы данных начальными данными"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Герои
    heroes = [
        "Anti-Mage", "Axe", "Bane", "Bloodseeker", "Crystal Maiden", "Drow Ranger",
        "Earthshaker", "Juggernaut", "Mirana", "Morphling", "Shadow Fiend", "Phantom Lancer",
        "Puck", "Pudge", "Razor", "Sand King", "Storm Spirit", "Sven", "Tiny", "Vengeful Spirit",
        "Windranger", "Zeus", "Kunkka", "Lina", "Lion", "Shadow Shaman", "Slardar", "Tidehunter",
        "Witch Doctor", "Riki", "Enigma", "Tinker", "Sniper", "Necrophos", "Warlock", "Beastmaster",
        "Queen of Pain", "Venomancer", "Faceless Void", "Wraith King", "Death Prophet", "Phantom Assassin",
        "Pugna", "Templar Assassin", "Viper", "Luna", "Dragon Knight", "Dazzle", "Clockwerk",
        "Leshrac", "Nature's Prophet", "Lifestealer", "Dark Seer", "Clinkz", "Omniknight", "Enchantress",
        "Huskar", "Night Stalker", "Broodmother", "Bounty Hunter", "Weaver", "Jakiro", "Batrider",
        "Chen", "Spectre", "Ancient Apparition", "Doom", "Ursa", "Spirit Breaker", "Gyrocopter",
        "Alchemist", "Invoker", "Silencer", "Outworld Destroyer", "Lycan", "Brewmaster", "Shadow Demon",
        "Lone Druid", "Chaos Knight", "Meepo", "Treant Protector", "Ogre Magi", "Undying", "Rubick",
        "Disruptor", "Nyx Assassin", "Naga Siren", "Keeper of the Light", "Io", "Visage", "Slark",
        "Medusa", "Troll Warlord", "Centaur Warrunner", "Magnus", "Timbersaw", "Bristleback",
        "Tusk", "Skywrath Mage", "Abaddon", "Elder Titan", "Legion Commander", "Techies", "Ember Spirit",
        "Earth Spirit", "Underlord", "Terrorblade", "Phoenix", "Oracle", "Winter Wyvern", "Arc Warden",
        "Monkey King", "Dark Willow", "Pangolier", "Grimstroke", "Hoodwink", "Void Spirit", "Snapfire",
        "Mars", "Dawnbreaker", "Marci", "Primal Beast", "Muerta"
    ]
    
    for hero in heroes:
        cursor.execute('INSERT OR IGNORE INTO heroes (name) VALUES (?)', (hero,))
    
    # Предметы
    items_data = {
        "starting": [
            "Tango", "Healing Salve", "Clarity", "Iron Branch", "Gauntlets of Strength", 
            "Slippers of Agility", "Mantle of Intelligence", "Circlet", "Magic Stick",
            "Enchanted Mango", "Faerie Fire"
        ],
        "early": [
            "Magic Wand", "Boots of Speed", "Bracer", "Wraith Band", "Null Talisman",
            "Soul Ring", "Power Treads", "Phase Boots", "Arcane Boots", "Hand of Midas"
        ],
        "core": [
            "Black King Bar", "Blink Dagger", "Force Staff", "Aghanim's Scepter",
            "Shadow Blade", "Desolator", "Maelstrom", "Battle Fury", "Radiance",
            "Armlet of Mordiggian", "Crystalys", "Echo Sabre", "Dragon Lance"
        ],
        "late": [
            "Abyssal Blade", "Butterfly", "Daedalus", "Divine Rapier", "Eye of Skadi",
            "Heart of Tarrasque", "Monkey King Bar", "Mjollnir", "Nullifier",
            "Satanic", "Skull Basher", "Silver Edge", "Bloodthorn", "Assault Cuirass",
            "Shiva's Guard", "Scythe of Vyse", "Linken's Sphere", "Lotus Orb",
            "Refresher Orb", "Aghanim's Blessing", "Octarine Core"
        ],
        "neutral": [
            "Faded Broach", "Ocean Heart", "Iron Talon", "Royal Jelly", "Pupil's Gift",
            "Trusty Shovel", "Quickening Charm", "Philosopher's Stone", "Essence Ring",
            "Grove Bow", "Elven Tunic", "Cloak of Flames", "Titan Sliver", "Mind Breaker",
            "Spell Prism", "Ninja Gear", "Illusionist's Cape", "Timeless Relic",
            "Fusion Rune", "Mirror Shield", "Apex", "Ballista", "Book of the Dead",
            "Ex Machina", "Fallen Sky", "Seer Stone", "Stygian Desolator", "The Leveller",
            "Pirate Hat", "Witless Shako", "Magic Lamp", "Giant's Ring"
        ]
    }
    
    for category, items in items_data.items():
        for item in items:
            cursor.execute('INSERT OR IGNORE INTO items (name, category) VALUES (?, ?)', (item, category))
    
    # Стратегии прокачки
    skill_builds = {
        "aggressive": ["Maximize damage skills first", "Focus on early game dominance"],
        "defensive": ["Maximize survival skills", "Focus on sustain and escape"],
        "farming": ["Maximize farming abilities", "Focus on late game scaling"],
        "utility": ["Maximize crowd control", "Focus on team support"],
        "hybrid": ["Balanced skill build", "Adapt to game situation"]
    }
    
    for build_type, descriptions in skill_builds.items():
        for desc in descriptions:
            cursor.execute('INSERT OR IGNORE INTO skill_builds (type, description) VALUES (?, ?)', (build_type, desc))
    
    # Линии
    lanes = ["Safe Lane", "Mid Lane", "Off Lane", "Soft Support", "Hard Support"]
    for lane in lanes:
        cursor.execute('INSERT OR IGNORE INTO lanes (name) VALUES (?)', (lane,))
    
    conn.commit()
    conn.close()

def get_random_hero():
    """Получить случайного героя из базы данных"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM heroes ORDER BY RANDOM() LIMIT 1')
    hero = cursor.fetchone()[0]
    conn.close()
    return hero

def get_random_lane():
    """Получить случайную линию из базы данных"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM lanes ORDER BY RANDOM() LIMIT 1')
    lane = cursor.fetchone()[0]
    conn.close()
    return lane

def get_random_skill_build():
    """Получить случайную стратегию прокачки из базы данных"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT type, description FROM skill_builds ORDER BY RANDOM() LIMIT 1')
    result = cursor.fetchone()
    conn.close()
    return result[1]  # Возвращаем описание

def get_random_items(category, limit):
    """Получить случайные предметы определенной категории"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM items WHERE category = ? ORDER BY RANDOM() LIMIT ?', (category, limit))
    items = [row[0] for row in cursor.fetchall()]
    conn.close()
    return items

# В файле app.py, заменить функцию generate_random_build():
def generate_random_build():
    """Генерация случайного билда с использованием данных из базы данных"""
    hero = get_random_hero()
    lane = get_random_lane()
    skill_build = get_random_skill_build()
    
    # Генерация предметов
    starting_items = get_random_items("starting", 6)
    early_items = get_random_items("early", 3)
    core_items = get_random_items("core", 3)
    late_items = get_random_items("late", 2)
    neutral_items = get_random_items("neutral", 2)
    
    build = {
        "hero": hero,
        "lane": lane,
        "skill_build": skill_build,
        "starting_items": starting_items,
        "early_game": early_items,
        "core_items": core_items,
        "late_game": late_items,
        "neutral_items": neutral_items
    }
    
    # Сохраняем в историю
    save_to_history(build)
    
    return build

# В файл app.py, добавить после других функций
def save_to_history(build):
    """Сохранить билд в историю"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO generation_history 
        (hero, lane, skill_build, starting_items, early_game, core_items, late_game, neutral_items)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        build['hero'],
        build['lane'],
        build['skill_build'],
        ','.join(build['starting_items']),
        ','.join(build['early_game']),
        ','.join(build['core_items']),
        ','.join(build['late_game']),
        ','.join(build['neutral_items'])
    ))
    
    conn.commit()
    conn.close()

def get_generation_history(limit=10):
    """Получить историю генераций"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT hero, lane, skill_build, starting_items, early_game, core_items, late_game, neutral_items, created_at
        FROM generation_history 
        ORDER BY created_at DESC 
        LIMIT ?
    ''', (limit,))
    
    history = []
    for row in cursor.fetchall():
        history.append({
            'hero': row[0],
            'lane': row[1],
            'skill_build': row[2],
            'starting_items': row[3].split(','),
            'early_game': row[4].split(','),
            'core_items': row[5].split(','),
            'late_game': row[6].split(','),
            'neutral_items': row[7].split(','),
            'created_at': row[8]
        })
    
    conn.close()
    return history

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate')
def generate_build():
    build = generate_random_build()
    return render_template('build.html', build=build)

@app.route('/api/generate')
def api_generate_build():
    build = generate_random_build()
    return jsonify(build)

@app.route('/api/heroes')
def api_get_heroes():
    """API endpoint для получения списка героев"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM heroes ORDER BY name')
    heroes = [row[0] for row in cursor.fetchall()]
    conn.close()
    return jsonify(heroes)

@app.route('/api/items/<category>')
def api_get_items(category):
    """API endpoint для получения предметов по категории"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM items WHERE category = ? ORDER BY name', (category,))
    items = [row[0] for row in cursor.fetchall()]
    conn.close()
    return jsonify(items)

if __name__ == '__main__':
    # Инициализация базы данных при первом запуске
    if not os.path.exists(DB_NAME):
        init_db()
        populate_db()
        print("База данных Doza.db создана и заполнена данными!")

# В файл app.py, добавить после других маршрутов:
@app.route('/history')
def history():
    history_data = get_generation_history(20)  # Последние 20 записей
    return render_template('history.html', history=history_data)
    
if __name__ == '__main__':
    app.run(debug=True)