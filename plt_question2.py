import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# 数据准备
data = {
    'Pattern': ['P117', 'P210', 'P221', 'P305', 'P354', 'P405', 'P435', 'P461', 'P481', 'P511', 'P564'],
    'Usage': [10, 6, 1, 1, 13, 14, 2, 10, 6, 12, 5],
    'Material_5.5m': [10, 0, 0, 0, 13, 0, 0, 0, 0, 0, 5],
    'Material_6.2m': [0, 6, 1, 1, 0, 14, 2, 10, 6, 12, 0],
    'Material_7.8m': [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
}
df = pd.DataFrame(data)

# 智能颜色映射配置
cmap = sns.diverging_palette(220, 20, as_cmap=True)
norm = plt.Normalize(vmin=df[['Material_5.5m', 'Material_6.2m', 'Material_7.8m']].values.min(),
                     vmax=df[['Material_5.5m', 'Material_6.2m', 'Material_7.8m']].values.max())

# 创建专业画布
plt.figure(figsize=(14, 8))
ax = sns.heatmap(
    df.set_index('Pattern'),
    annot=True,
    fmt="d",
    cmap=cmap,
    norm=norm,
    linewidths=0.5,
    annot_kws={"size": 12},
    cbar_kws={
        "shrink": 0.8,
        "label": "Usage Frequency",
        "orientation": "vertical"
    }
)

# 高级样式配置
ax.set_title(
    "Cutting Pattern Material Usage Analysis",
    fontsize=18,
    pad=20,
    fontweight='bold',
    color='#2c3e50'
)
plt.xlabel("Material Type", fontsize=14, labelpad=15)
plt.ylabel("Cutting Pattern", fontsize=14, labelpad=15)
plt.xticks(rotation=45, ha='right', fontsize=12)
plt.yticks(fontsize=12)

# 智能零值处理
for text in ax.texts:
    if text.get_text() == '0':
        text.set_text('')
        text.set_visible(False)

# 添加数据标签格式
for _, spine in ax.spines.items():
    spine.set_visible(True)
    spine.set_color('#bdc3c7')
    spine.set_linewidth(0.8)

# 添加颜色条注释
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=12)
cbar.set_label('Usage Frequency', rotation=270, labelpad=20)

# # 添加辅助装饰线
# plt.annotate(
#     '* High-frequency patterns indicate optimal material utilization',
#     xy=(0.5, -0.15),
#     xycoords='axes fraction',
#     ha='center',
#     fontsize=10,
#     alpha=0.7,
#     color='#2c3e50'
# )

plt.tight_layout()
plt.show()

"""
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.patheffects import withStroke

# 数据准备
labels = ['Material Utilization', 'Material Loss']
sizes = [82.20, 18.01]
explode = (0.1, 0)  # 反向突出显示利用率

# 创建专业渐变色
gradient = np.linspace(0, 1, 256).reshape(1, -1)
cmap = plt.get_cmap('viridis')
colors = [cmap(0.2), cmap(0.8)]  # 蓝绿渐变

# 创建画布
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, aspect='equal')

# 绘制渐变环形图
wedges, texts, autotexts = ax.pie(
    sizes,
    explode=explode,
    labels=labels,
    autopct='%1.1f%%',
    startangle=90,
    colors=colors,
    wedgeprops={
        'edgecolor': 'black',
        'linewidth': 2,
        'linestyle': '-.',
        'hatch': '//'
    },
    pctdistance=0.8
)

# 添加3D投影效果
for w in wedges:
    w.set_zorder(1)
    w.set_edgecolor('white')
    w.set_linewidth(2)
    w.set_path_effects([
        withStroke(linewidth=4, foreground='white', alpha=0.8)
    ])

# 智能标签系统
ax.set_title(
    "Material Efficiency Analysis",
    fontsize=18,
    pad=20,
    fontweight='bold',
    color='#2c3e50'
)

# 动态注释框
bbox_props = dict(boxstyle="round,pad=0.8", fc="white", ec="#34495e", lw=2)
ax.text(0.75, 0.2,
        'Key Insight: Exceptional material utilization rate\nof 82.20% with minimal loss',
        ha='center', va='center',
        fontsize=12,
        bbox=bbox_props,
        transform=ax.transAxes)

# 高级坐标轴设置
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_linewidth(1.5)
ax.spines['left'].set_linewidth(1.5)

# 添加数据标签格式
for autotext in autotexts:
    autotext.set_size(14)
    autotext.set_color('white')
    autotext.set_path_effects([
        withStroke(linewidth=3, foreground='black', alpha=0.9)
    ])

# 添加价值线
ax.plot([0, 0.5], [0.5, 0.5], color='#e74c3c',
        linestyle='--', linewidth=2, alpha=0.7)

plt.tight_layout()
plt.show()
"""

"""
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import numpy as np

# ----- Global Configuration -----
plt.rcParams.update({
    'font.sans-serif': 'Arial',    # Universal font setting
    'axes.edgecolor': '#34495e',   # Axis line color
    'axes.linewidth': 1.5,         # Axis line width
    'grid.alpha': 0.4             # Grid transparency
})

# ----- Data Preparation -----
categories = ['Total Cost', 'Total Revenue', 'Net Profit']
values = [2240.0, 35700.0, 33460.0]  # Unit: CNY
colors = ['#2ecc71', '#3498db', '#e74c3c']  # Green-Blue-Red gradient

# ----- Visualization Engine -----
fig, ax = plt.subplots(figsize=(12, 7))

# Core bar plot (error-proof implementation)
bars = ax.bar(
    range(len(categories)),  # Numeric indexing for stability
    values,
    width=0.6,
    color=colors,
    edgecolor='black',
    linewidth=1.2,
    zorder=3
)

# ----- Annotation System -----
# Dynamic data labels
for i, (bar, val) in enumerate(zip(bars, values)):
    y_offset = val * 0.03  # 3% offset from top
    ax.text(
        bar.get_x() + bar.get_width()/2,
        val + y_offset,
        f'¥{val:,.2f}',
        ha='center',
        va='bottom',
        fontsize=13,
        color=colors[i],
        weight='bold',
        bbox=dict(
            boxstyle='round',
            facecolor='white',
            edgecolor=colors[i],
            alpha=0.9
        )
)

# Axis configuration
ax.set_xticks(range(len(categories)))
ax.set_xticklabels(categories, fontsize=14)
ax.set_ylim(0, max(values)*1.25)
ax.yaxis.set_visible(False)  # Hide Y-axis ticks

# Grid system
ax.grid(axis='y', linestyle='--', linewidth=1, zorder=0)

# Title system
ax.set_title(
    " Payments Analysis ",
    fontsize=18,
    pad=20,
    fontweight='bold',
    color='#2c3e50'
)

# Key metric annotation
profit_margin = (values[2]/values[1])*100
ax.annotate(
    f'Profit Margin: {profit_margin:.1f}%',
    xy=(2, values[2]),
    xytext=(2.3, values[2]*1.15),
    arrowprops=dict(
        arrowstyle='->',
        color='#e74c3c',
        linewidth=1.5,
        connectionstyle='arc3,rad=0.3'
    ),
    fontsize=12,
    color='#2c3e50',
    bbox=dict(boxstyle='round', facecolor='white', alpha=0.9)
)

# ----- Output Guarantee -----
plt.tight_layout()
plt.savefig('financial_analysis.png', dpi=300, bbox_inches='tight')
plt.show()
"""

"""
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import numpy as np

# ---------- 数据准备 ----------
orders = ['Order1', 'Order2', 'Order3', 'Order4']
dimensions = ['Width', 'Height']
requirements = np.array([[20, 40, 40, 30], [20, 40, 40, 30]])  # 需求值矩阵
actuals = np.array([[20.0, 40.0, 40.0, 30.0], [20.0, 40.0, 40.0, 30.0]])  # 实际值矩阵

# ---------- 可视化配置 ----------
plt.rcParams.update({
    'font.family': 'Arial',        # 全局字体
    'axes.edgecolor': '#34495e',   # 坐标轴颜色
    'axes.linewidth': 1.5,         # 坐标轴线宽
    'grid.color': '#bdc3c7',       # 网格颜色
    'grid.alpha': 0.4             # 网格透明度
})

# ---------- 创建画布 ----------
fig, ax = plt.subplots(figsize=(14, 8))

# ---------- 核心绘图逻辑 ----------
bar_width = 0.35  # 柱宽
index = np.arange(len(orders))  # 订单索引

# 绘制需求柱状图
rects1 = ax.bar(index - bar_width/2, requirements[0], bar_width,
               label='Requirement (Width)', color='#3498db', edgecolor='black')
rects2 = ax.bar(index - bar_width/2, requirements[1], bar_width,
               label='Requirement (Height)', color='#2ecc71', edgecolor='black', bottom=requirements[0])

# 绘制实际柱状图
rects3 = ax.bar(index + bar_width/2, actuals[0], bar_width,
               label='Actual (Width)', color='#2980b9', edgecolor='black')
rects4 = ax.bar(index + bar_width/2, actuals[1], bar_width,
               label='Actual (Height)', color='#27ae60', edgecolor='black', bottom=actuals[0])

# ---------- 自动标注系统 ----------
def safe_annotate(rects):
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2.,
                height + 1,
                f'{height:.0f}',
                ha='center', va='bottom',
                fontsize=10)

safe_annotate(rects1)
safe_annotate(rects2)
safe_annotate(rects3)
safe_annotate(rects4)

# ---------- 样式增强 ----------
ax.set_title('Order Specification Compliance Analysis', fontsize=16, pad=20)
ax.set_xlabel('Order Categories', fontsize=12, labelpad=15)
ax.set_ylabel('Measurement Values', fontsize=12, labelpad=15)
ax.set_xticks(index)
ax.set_xticklabels(orders, fontsize=12)
ax.legend(loc='upper left', frameon=True, framealpha=0.9)

# 网格系统
ax.grid(axis='y', linestyle='--', linewidth=0.7)

# 边框优化
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_color('#34495e')

# ---------- 输出保障 ----------
plt.tight_layout()
plt.savefig('order_compliance.png', dpi=300, bbox_inches='tight')
plt.show()
"""








