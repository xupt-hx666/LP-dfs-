import pulp
from pulp import LpProblem, LpMinimize, LpVariable, LpInteger, lpSum, LpStatus, value

segments = [
    {'name': 'order1_width', 'length': 1.61, 'demand': 20},
    {'name': 'order1_height', 'length': 2.21, 'demand': 20},
    {'name': 'order2_width', 'length': 1.81, 'demand': 40},
    {'name': 'order2_height', 'length': 2.41, 'demand': 40},
    {'name': 'order3_width', 'length': 1.71, 'demand': 40},
    {'name': 'order3_height', 'length': 2.31, 'demand': 40},
    {'name': 'order4_width', 'length': 1.51, 'demand': 30},
    {'name': 'order4_height', 'length': 2.01, 'demand': 30},
]

# segments = [
#     {'name': 'order1_width', 'length': 1.59, 'demand': 20},
#     {'name': 'order1_height', 'length': 2.19, 'demand': 20},
#     {'name': 'order2_width', 'length': 1.79, 'demand': 40},
#     {'name': 'order2_height', 'length': 2.39, 'demand': 40},
#     {'name': 'order3_width', 'length': 1.69, 'demand': 40},
#     {'name': 'order3_height', 'length': 2.29, 'demand': 40},
#     {'name': 'order4_width', 'length': 1.49, 'demand': 30},
#     {'name': 'order4_height', 'length': 1.99, 'demand': 30},
# ]

materials = [
    {
        'length': 5.5,
        'cost': 18,
        'defects': [
            {'start': 1.0, 'length': 0.03},
            {'start': 2.5, 'length': 0.04},
        ]
    },
    {
        'length': 6.2,
        'cost': 22,
        'defects': [
            {'start': 0.5, 'length': 0.02},
            {'start': 1.8, 'length': 0.05},
        ]
    },
    {
        'length': 7.8,
        'cost': 28,
        'defects': [
            {'start': 3.0, 'length': 0.03},
        ]
    },
]


def get_available_intervals(material_length, defects):
    sorted_defects = sorted(defects, key=lambda x: x['start'])
    available_intervals = []
    current_start = 0.0
    for defect in sorted_defects:
        defect_start = defect['start']
        defect_end = defect_start + defect['length']
        if current_start < defect_start:
            available_intervals.append({'start': current_start, 'end': defect_start})
        current_start = defect_end
    if current_start < material_length:
        available_intervals.append({'start': current_start, 'end': material_length})
    return available_intervals


def generate_patterns(material_length, material_cost, defects):
    available_intervals = get_available_intervals(material_length, defects)
    interval_lengths = [interval['end'] - interval['start'] for interval in available_intervals]
    patterns = []
    seg_list = segments

    def dfs(start, remaining_intervals, current_pattern, total_used, total_kerf):
        patterns.append({
            'material_length': material_length,
            'cost': material_cost,
            'pattern': current_pattern.copy(),
            'total_used': total_used + total_kerf,
            'waste': material_length - (total_used + total_kerf),
            'kerf_loss': total_kerf
        })

        for i in range(start, len(seg_list)):
            seg = seg_list[i]
            for interval_idx in range(len(remaining_intervals)):
                interval_remaining = remaining_intervals[interval_idx]
                required = seg['length'] + 0.005
                if required <= interval_remaining:
                    new_remaining = remaining_intervals.copy()
                    new_remaining[interval_idx] -= required
                    new_pattern = current_pattern.copy()
                    new_pattern[seg['name']] = new_pattern.get(seg['name'], 0) + 1
                    new_total_used = total_used + seg['length']
                    new_total_kerf = total_kerf + 0.005
                    dfs(i, new_remaining, new_pattern, new_total_used, new_total_kerf)

    initial_remaining = interval_lengths.copy()
    dfs(0, initial_remaining, {}, 0.0, 0.0)
    return patterns


all_patterns = []
for mat in materials:
    patterns = generate_patterns(mat['length'], mat['cost'], mat['defects'])
    all_patterns.extend(patterns)

# for i in all_patterns:
#     print(i)

prob = LpProblem("Optimal_Cutting_Defects", LpMinimize)

pattern_vars = [
    LpVariable(f"Pattern_{i}", lowBound=0, cat=LpInteger)
    for i in range(len(all_patterns))
]

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
    total_revenue = sum(seg['demand'] // 2 * price for seg, price in [
        (segments[0], 480), (segments[1], 480),
        (segments[2], 680), (segments[3], 680),
        (segments[4], 550), (segments[5], 550),
        (segments[6], 420), (segments[7], 420)
    ]) / 2

    total_material = sum(var.value() * p['material_length'] for var, p in zip(pattern_vars, all_patterns))
    total_waste = sum(var.value() * p['waste'] for var, p in zip(pattern_vars, all_patterns))
    total_kerf = sum(var.value() * p['kerf_loss'] for var, p in zip(pattern_vars, all_patterns))

    utilization = (total_material - total_waste) / total_material if total_material != 0 else 0
    loss_rate = (total_waste + total_kerf) / total_material if total_material != 0 else 0

    print(f"最优总成本: {total_cost}元")
    print(f"总销售额: {total_revenue}元")
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
