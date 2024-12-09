import sys
import yaml
import json
import os

# 设置标准输出为 UTF-8 编码
sys.stdout.reconfigure(encoding='utf-8')

input_file = r'D:\eve\coding\evedata\blueprints.yaml'
output_file = r'D:\eve\coding\evedata\blueprints1.json'

try:
    # 读取 YAML 文件
    with open(input_file, 'r', encoding='utf-8') as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)

    # 转换为 JSON
    json_data = json.dumps(yaml_data, indent=4, ensure_ascii=False)

    # 打印 JSON 数据
    print(json_data)

    # 确保目标文件夹存在
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 写入到文件
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json_file.write(json_data)
    print(f"JSON file saved to {output_file}")

except Exception as e:
    print(f"Error: {e}")
