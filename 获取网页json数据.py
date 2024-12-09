import requests
import sqlite3
from datetime import datetime
import sys
sys.stdout.reconfigure(encoding='utf-8')
# 请求获取 JSON 数据
url = "https://esi.evetech.net/latest/markets/10000002/orders/?datasource=tranquility&order_type=all"
response = requests.get(url)
data = response.json()

# 连接到 SQLite 数据库
db = sqlite3.connect(r'D:\eve\coding\database\items.db')  # 连接到 items.db
cursor = db.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# 获取并打印所有表的名称
tables = cursor.fetchall()
print("Tables in the database:")
for table in tables:
    print(table[0])


for order in data:
    # 处理每个订单
    order_id = order['order_id']
    duration = order['duration']
    is_buy_order = order['is_buy_order']
    issued = order['issued']
    location_id = order['location_id']
    min_volume = order['min_volume']
    price = order['price']
    range_ = order['range']
    system_id = order['system_id']
    type_id = order['type_id']
    volume_remain = order['volume_remain']
    volume_total = order['volume_total']

    # 插入到数据库
    cursor.execute("""
        INSERT INTO market_orders (
            order_id, duration, is_buy_order, issued, location_id, min_volume, 
            price, range, system_id, type_id, volume_remain, volume_total
        ) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (order_id, duration, is_buy_order, issued, location_id, min_volume,
          price, range_, system_id, type_id, volume_remain, volume_total))

# 提交事务并关闭连接
db.commit()
cursor.close()
db.close()
