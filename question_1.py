import pulp
from pulp import LpProblem, LpMinimize, LpVariable, LpInteger, lpSum, LpStatus, value

# segments = [
#     {'name': 'order1_width', 'length': 1.61, 'demand': 20},
#     {'name': 'order1_height', 'length': 2.21, 'demand': 20},
#     {'name': 'order2_width', 'length': 1.81, 'demand': 40},
#     {'name': 'order2_height', 'length': 2.41, 'demand': 40},
#     {'name': 'order3_width', 'length': 1.71, 'demand': 40},
#     {'name': 'order3_height', 'length': 2.31, 'demand': 40},
#     {'name': 'order4_width', 'length': 1.51, 'demand': 30},
#     {'name': 'order4_height', 'length': 2.01, 'demand': 30},
# ]

segments = [
    {'name': 'order1_width', 'length': 1.59, 'demand': 20},
    {'name': 'order1_height', 'length': 2.19, 'demand': 20},
    {'name': 'order2_width', 'length': 1.79, 'demand': 40},
    {'name': 'order2_height', 'length': 2.39, 'demand': 40},
    {'name': 'order3_width', 'length': 1.69, 'demand': 40},
    {'name': 'order3_height', 'length': 2.29, 'demand': 40},
    {'name': 'order4_width', 'length': 1.49, 'demand': 30},
    {'name': 'order4_height', 'length': 1.99, 'demand': 30},
]

materials = [
    {'length': 5.5, 'cost': 18},
    {'length': 6.2, 'cost': 22},
    {'length': 7.8, 'cost': 28},
]

"""dfs算法生成3种原料的所有切割方式"""


def generate_patterns(material_length, material_cost):
    patterns = []
    seg_list = [s for s in segments]

    def dfs(start, current_length, current_kerf, pattern):
        for i in range(start, len(seg_list)):
            seg = seg_list[i]
            new_length = current_length + seg['length']
            """边界条件判断"""
            judge_length = new_length + current_kerf
            new_kerf = current_kerf
            if judge_length < material_length:
                new_kerf = current_kerf + 0.005

            total_used = new_length + new_kerf
            if total_used > material_length:
                continue

            new_pattern = pattern.copy()
            new_pattern[seg['name']] = new_pattern.get(seg['name'], 0) + 1

            patterns.append({
                'material_length': material_length,
                'cost': material_cost,
                'pattern': new_pattern,
                'total_used': total_used,
                'waste': material_length - total_used,
                'kerf_loss': new_kerf
            })

            dfs(i, new_length, new_kerf, new_pattern)

    dfs(0, 0.0, 0.0, {})
    return patterns


all_patterns = []
for mat in materials:
    patterns = generate_patterns(mat['length'], mat['cost'])
    all_patterns.extend(patterns)

# for i in all_patterns:
#     print(i)
"""使用线性规划模型"""
prob = LpProblem("Optimal_Cutting", LpMinimize)

pattern_vars = [
    LpVariable(f"Pattern_{i}", lowBound=0, cat=LpInteger)
    for i in range(len(all_patterns))
]

# 目标函数
prob += lpSum([var * all_patterns[i]['cost'] for i, var in enumerate(pattern_vars)])

# 约束条件
for seg in segments:
    seg_total = lpSum([
        var * all_patterns[i]['pattern'].get(seg['name'], 0)
        for i, var in enumerate(pattern_vars)
    ])
    prob += seg_total >= seg['demand']

prob.solve()

"""结果验证"""
if prob.status == pulp.LpStatusOptimal:
    total_cost = value(prob.objective)
    total_revenue = sum(seg['demand'] // 2 * price for seg, price in [
        (segments[0], 480), (segments[1], 480),
        (segments[2], 680), (segments[3], 680),
        (segments[4], 550), (segments[5], 550),
        (segments[6], 420), (segments[7], 420)
    ]) / 2

    total_material = sum(
        var.value() * p['material_length']
        for var, p in zip(pattern_vars, all_patterns)
    )
    total_waste = sum(
        var.value() * p['waste']
        for var, p in zip(pattern_vars, all_patterns)
    )
    total_kerf = sum(
        var.value() * p['kerf_loss']
        for var, p in zip(pattern_vars, all_patterns)
    )

    utilization = (total_material - total_waste) / total_material
    loss_rate = (total_waste + total_kerf) / total_material

    print(f"最优总成本: {total_cost}元")
    print(f"总销售额: {total_revenue}元")
    print(f"材料利用率: {utilization * 100:.2f}%")
    print(f"综合损耗率: {loss_rate * 100:.2f}%")

    print("\n详细切割方案：")
    for i, var in enumerate(pattern_vars):
        if var.value() > 0:
            details = ", ".join(
                f"{k}:{v}" for k, v in all_patterns[i]['pattern'].items()
            )
            print(f"模式{i + 1}: 使用{var.value()}次, 包含[{details}]")
else:
    print("未找到可行解")

print("\n需求满足验证：")
for seg in segments:
    actual = sum(
        var.value() * all_patterns[i]['pattern'].get(seg['name'], 0)
        for i, var in enumerate(pattern_vars)
    )
    print(f"{seg['name']}: 需要{seg['demand']} 实际{actual}")
