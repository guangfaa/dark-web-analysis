import re

# 用有序字典和列表保持节点顺序
nodes = {}      # 格式：{节点ID: {0:数量, 1:数量, ..., 6:数量}}
node_ids = []   # 记录节点出现顺序

with open('Sttepd.out', 'r', encoding='utf-8') as f:
    current_node_id = None
    for line in f:
        stripped_line = line.strip()
        
        # 匹配新节点块开始
        if re.fullmatch(r'=== 节点 \d+/\d+ ===', stripped_line):
            node_id_line = next(f).strip()
            node_id_match = re.match(r'节点ID: (\d+)', node_id_line)
            if node_id_match:
                current_node_id = node_id_match.group(1)
                if current_node_id not in nodes:  # 新节点初始化
                    node_ids.append(current_node_id)
                    nodes[current_node_id] = {step: 0 for step in range(7)}
                    
        # 匹配数据行
        elif current_node_id:
            data_match = re.fullmatch(r'\|\s*(\d+)\s*\|\s*(\d+)\s*\|', stripped_line)
            if data_match:
                step, count = map(int, data_match.groups())
                if 0 <= step <= 6:  # 只处理0-6步
                    nodes[current_node_id][step] = count

# 生成表格输出
header = "节点ID\t" + "\t".join(map(str, range(7)))
print(header)
for node_id in node_ids:
    counts = [str(nodes[node_id][step]) for step in range(7)]
    print(f"{node_id}\t" + "\t".join(counts))