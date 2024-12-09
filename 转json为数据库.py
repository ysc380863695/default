import json
import sqlite3
import os
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 读取 JSON 数据
with open(r'D:\eve\coding\evedata\types2.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# 确保数据库存储路径存在
db_path = r'D:\eve\coding\database\items.db'
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# 连接到 SQLite 数据库（如果文件不存在，会自动创建）
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 创建表
cursor.execute('''
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY,
    groupID INTEGER,
    iconID INTEGER,
    marketGroupID INTEGER,
    mass REAL,
    metaGroupID INTEGER,
    portionSize INTEGER,
    published BOOLEAN,
    variationParentTypeID INTEGER,
    volume REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS item_descriptions (
    id INTEGER PRIMARY KEY,
    item_id INTEGER,
    de TEXT,
    en TEXT,
    es TEXT,
    fr TEXT,
    ja TEXT,
    ko TEXT,
    ru TEXT,
    zh TEXT,
    FOREIGN KEY(item_id) REFERENCES items(id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS item_names (
    id INTEGER PRIMARY KEY,
    item_id INTEGER,
    de TEXT,
    en TEXT,
    es TEXT,
    fr TEXT,
    ja TEXT,
    ko TEXT,
    ru TEXT,
    zh TEXT,
    FOREIGN KEY(item_id) REFERENCES items(id)
)
''')

# 插入数据
for item_id, item_data in data.items():
    # 插入 items 表
    cursor.execute('''
    INSERT INTO items (id, groupID, iconID, marketGroupID, mass, metaGroupID, portionSize, published, variationParentTypeID, volume)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        item_id,
        item_data.get('groupID'),  # 如果没有这个键，返回 None
        item_data.get('iconID'),  # 如果没有这个键，返回 None
        item_data.get('marketGroupID'),
        item_data.get('mass'),
        item_data.get('metaGroupID'),
        item_data.get('portionSize'),
        item_data.get('published'),
        item_data.get('variationParentTypeID'),
        item_data.get('volume')
    ))

    # 获取插入的 item_id
    item_id_db = cursor.lastrowid

    # 使用 get() 方法来避免 KeyError
    descriptions = item_data.get('description', {})
    cursor.execute('''
    INSERT INTO item_descriptions (item_id, de, en, es, fr, ja, ko, ru, zh)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        item_id_db,
        descriptions.get('de', ''),
        descriptions.get('en', ''),
        descriptions.get('es', ''),
        descriptions.get('fr', ''),
        descriptions.get('ja', ''),
        descriptions.get('ko', ''),
        descriptions.get('ru', ''),
        descriptions.get('zh', '')
    ))

    # 使用 get() 方法来避免 KeyError
    names = item_data.get('name', {})
    cursor.execute('''
    INSERT INTO item_names (item_id, de, en, es, fr, ja, ko, ru, zh)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        item_id_db,
        names.get('de', ''),
        names.get('en', ''),
        names.get('es', ''),
        names.get('fr', ''),
        names.get('ja', ''),
        names.get('ko', ''),
        names.get('ru', ''),
        names.get('zh', '')
    ))

# 提交事务并关闭连接
conn.commit()
conn.close()

print(f"Data has been successfully saved to {db_path}")
