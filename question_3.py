import pulp
from pulp import LpProblem, LpMinimize, LpVariable, LpInteger, lpSum, LpStatus, value
import pandas as pd
import plotly.graph_objects as go


# segments = [
#     {'name': 'order1_width', 'length': 1.61, 'demand': 120 * 2},
#     {'name': 'order1_height', 'length': 2.21, 'demand': 120 * 2},
#     {'name': 'order2_width', 'length': 1.81, 'demand': 80 * 2},
#     {'name': 'order2_height', 'length': 2.41, 'demand': 80 * 2},
#     {'name': 'order3_width', 'length': 1.71, 'demand': 60 * 2},
#     {'name': 'order3_height', 'length': 2.31, 'demand': 60 * 2},
#     {'name': 'order4_width', 'length': 1.51, 'demand': 40 * 2},
#     {'name': 'order4_height', 'length': 2.01, 'demand': 40 * 2},
# ]

segments = [
    {'name': 'order1_width', 'length': 1.59, 'demand': 120 * 2},
    {'name': 'order1_height', 'length': 2.19, 'demand': 120 * 2},
    {'name': 'order2_width', 'length': 1.79, 'demand': 80 * 2},
    {'name': 'order2_height', 'length': 2.39, 'demand': 80 * 2},
    {'name': 'order3_width', 'length': 1.69, 'demand': 60 * 2},
    {'name': 'order3_height', 'length': 2.29, 'demand': 60 * 2},
    {'name': 'order4_width', 'length': 1.49, 'demand': 40 * 2},
    {'name': 'order4_height', 'length': 1.99, 'demand': 40 * 2},
]


def load_materials():
    df = pd.read_excel('附件.xlsx', sheet_name='Sheet1')

    materials = []
    for _, row in df.iterrows():
        mat_info = {
            'length': row['原材料长度 (米)'],
            'cost': row['单价（元/根）'],
            'defects': [{
                'start': row['缺陷位置 (米)'],
                'length': row['缺陷长度 (米)']
            }]
        }
        materials.append(mat_info)
    return materials


def get_available_intervals(material_length, defects):
    sorted_defects = sorted(defects, key=lambda x: x['start'])
    available = []
    current_start = 0.0
    for defect in sorted_defects:
        defect_end = defect['start'] + defect['length']
        if current_start < defect['start']:
            available.append({'start': current_start, 'end': defect['start']})
        current_start = max(current_start, defect_end)
    if current_start < material_length:
        available.append({'start': current_start, 'end': material_length})
    return available


def generate_patterns(material_length, material_cost, defects):
    available_intervals = get_available_intervals(material_length, defects)
    interval_lengths = [round(interval['end'] - interval['start'], 6) for interval in available_intervals]
    patterns = []
    KERF = 0.005

    def dfs(seg_idx, remaining_intervals, current_pattern, total_used, total_kerf):
        if current_pattern:
            patterns.append({
                'material_length': material_length,
                'cost': material_cost,
                'pattern': current_pattern.copy(),
                'total_used': total_used + total_kerf,
                'waste': material_length - (total_used + total_kerf),
                'kerf_loss': total_kerf
            })

        for i in range(seg_idx, len(segments)):
            seg = segments[i]
            required_length = round(seg['length'] + KERF, 6)

            for interval_idx in range(len(remaining_intervals)):
                if remaining_intervals[interval_idx] >= required_length:
                    new_remaining = [round(r, 6) for r in remaining_intervals]
                    new_remaining[interval_idx] = round(new_remaining[interval_idx] - required_length, 6)

                    new_pattern = current_pattern.copy()
                    key = seg['name']
                    new_pattern[key] = new_pattern.get(key, 0) + 1

                    dfs(i, new_remaining, new_pattern,
                        round(total_used + seg['length'], 6),
                        round(total_kerf + KERF, 6))

    dfs(0, interval_lengths, {}, 0.0, 0.0)
    return patterns

def visualize_results(patterns, pattern_vars, segments):
    # 数据处理
    active_patterns = [{
        'id': i,
        'vars': int(var.value()),
        'pattern': p['pattern'],
        'material': p['material_length'],
        'cost': p['cost'],
        'waste': p['waste']
    } for i, (var, p) in enumerate(zip(pattern_vars, patterns)) if var.value() > 0]

    # 桑基图数据准备
    labels = []
    source = []
    target = []
    value = []

    # 节点索引
    node_index = {}

    def get_node(name):
        if name not in node_index:
            node_index[name] = len(labels)
            labels.append(name)
        return node_index[name]

    # 构建流量数据
    for p in active_patterns:
        # 原材料到模式
        mat_node = f"Material {p['material']}m"
        source.append(get_node(mat_node))
        target.append(get_node(f"Pattern {p['id']}"))
        value.append(p['vars'])

        # 模式到订单
        for seg, count in p['pattern'].items():
            order = next(s['name'] for s in segments if s['name'] == seg)
            source.append(get_node(f"Pattern {p['id']}"))
            target.append(get_node(order))
            value.append(count * p['vars'])

    # 桑基图绘制
    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            label=labels,
            color="lightblue"
        ),
        link=dict(
            source=source,
            target=target,
            value=value
        )
    ))

    fig.update_layout(title_text="Material Allocation Sankey Diagram", font_size=10)
    fig.show()

    # 平行坐标图数据准备
    para_data = []
    for p in active_patterns:
        entry = {
            'Pattern': p['id'],
            'Usage': p['vars'],
            'Material': p['material'],
            'Cost': p['cost'],
            'Waste': p['waste']
        }
        for seg in segments:
            entry[seg['name']] = p['pattern'].get(seg['name'], 0)
        para_data.append(entry)

    df = pd.DataFrame(para_data)

    # 平行坐标图绘制
    para_fig = go.Figure(data=go.Parcoords(
        line=dict(color=df['Usage'],
                  colorscale='Electric'),
        dimensions=list([
            dict(label='Material', values=df['Material']),
            dict(label='Cost', values=df['Cost']),
            dict(label='Waste', values=df['Waste']),
            dict(label='Usage', values=df['Usage']),
            *[dict(label=seg['name'], values=df[seg['name']])
              for seg in segments]
        ])
    ))

    para_fig.update_layout(title_text="Cutting Pattern Parallel Coordinates")
    para_fig.show()

def main():
    materials = load_materials()

    all_patterns = []
    for mat in materials:
        patterns = generate_patterns(mat['length'], mat['cost'], mat['defects'])
        all_patterns.extend(patterns)

    for i in all_patterns:
        print(i)

    prob = LpProblem("Optimal_Cutting_Defects_Problem3", LpMinimize)

    pattern_vars = [
        LpVariable(f"Pattern_{i}", lowBound=0, cat=LpInteger)
        for i in range(len(all_patterns))
    ]

    revenue = sum(seg['demand'] // 2 * price for seg, price in [
        (segments[0], 480), (segments[1], 480),
        (segments[2], 680), (segments[3], 680),
        (segments[4], 550), (segments[5], 550),
        (segments[6], 420), (segments[7], 420)
    ]) / 2

    prob += lpSum([var * all_patterns[i]['cost'] for i, var in enumerate(pattern_vars)])

    for seg in segments:
        seg_total = lpSum([
            var * all_patterns[i]['pattern'].get(seg['name'], 0)
            for i, var in enumerate(pattern_vars)
        ])
        prob += seg_total >= seg['demand']

    prob.solve()

    if prob.status == pulp.LpStatusOptimal:
        total_cost = value(prob.objective)
        total_material = sum(var.value() * p['material_length'] for var, p in zip(pattern_vars, all_patterns))
        total_waste = sum(var.value() * p['waste'] for var, p in zip(pattern_vars, all_patterns))
        total_kerf = sum(var.value() * p['kerf_loss'] for var, p in zip(pattern_vars, all_patterns))

        utilization = (total_material - total_waste) / total_material if total_material != 0 else 0
        loss_rate = (total_waste + total_kerf) / total_material if total_material != 0 else 0

        print(f"最优总利润: {revenue - total_cost}元")
        print(f"最优总成本: {total_cost.round(2)}元")
        print(f"总销售额: {revenue}元")
        print(f"材料利用率: {utilization * 100:.2f}%")
        print(f"综合损耗率: {loss_rate * 100:.2f}%")

        print("\n详细切割方案：")
        for i, var in enumerate(pattern_vars):
            if var.value() > 0:
                details = ", ".join(f"{k}:{v}" for k, v in all_patterns[i]['pattern'].items())
                print(f"模式{i + 1}: 使用{var.value()}次, 包含[{details}]")
    else:
        print("未找到可行解")

    print("\n需求满足验证：")
    for seg in segments:
        actual = sum(var.value() * all_patterns[i]['pattern'].get(seg['name'], 0) for i, var in enumerate(pattern_vars))
        print(f"{seg['name']}: 需要{seg['demand']} 实际{actual}")

    # visualize_results(all_patterns, pattern_vars, segments)


if __name__ == "__main__":
    main()



