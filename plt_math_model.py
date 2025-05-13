"""
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np  # 添加缺失的numpy导入

# 输入数据（修正了字符串中的引号问题）
materials = [
    {"id": 1, "length": 5.5,
     "defects": [{"start": 1.0, "length": 0.03},
                 {"start": 2.5, "length": 0.04}]},
    {"id": 3, "length": 7.8,
     "defects": [{"start": 3.0, "length": 0.03}]}
]


def plot_material_defects(mat, figsize=(8, 2)):
    fig = plt.figure(figsize=figsize, dpi=120)
    ax = fig.add_subplot(111)

    # 修改为当前支持的样式
    plt.style.use('seaborn-v0_8-whitegrid')  # 使用seaborn白底网格样式

    # 绘制材料主体
    ax.broken_barh([(0, mat["length"])], (-0.4, 0.8),
                   facecolors='#E8E8E8', edgecolor='#4A4A4A',
                   linewidth=1, zorder=1)

    # 绘制缺陷区域（修正了字符串引号问题）
    for i, defect in enumerate(mat["defects"]):
        ax.broken_barh([(defect["start"], defect["length"])], (-0.4, 0.8),
                       facecolors='#FF4B4B', edgecolor='#C70039',
                       linewidth=0.8, hatch='///', zorder=2)

        defect_center = defect["start"] + defect["length"] / 2
        ax.text(defect_center, 0.05, f"D{i + 1}\n({defect['length']}m)",  # 修正引号使用
                ha='center', va='bottom', color='black',
                fontsize=8, fontweight='bold', zorder=3)

    # 设置刻度
    ax.set_xticks(np.arange(0, mat["length"] + 0.5, 0.5))
    ax.set_xticks(np.arange(0, mat["length"] + 0.1, 0.1), minor=True)
    ax.set_xlim(0, mat["length"] * 1.05)
    ax.set_yticks([])

    # 设置网格
    ax.grid(which='major', axis='x', linestyle='--', alpha=0.7)
    ax.grid(which='minor', axis='x', linestyle=':', alpha=0.4)

    ax.set_title(f"Material {mat['id']} Defect Visualization (Total Length: {mat['length']}m)",
                 pad=12, fontsize=10, fontweight='bold')

    # 添加图例
    legend_elements = [
        Patch(facecolor='#E8E8E8', edgecolor='#4A4A4A', label='Intact Material'),
        Patch(facecolor='#FF4B4B', edgecolor='#C70039', hatch='///', label='Defect Area')
    ]
    ax.legend(handles=legend_elements, loc='upper right',
              frameon=True, framealpha=0.9)

    plt.tight_layout()
    return fig


# 生成示意图
plot_material_defects(materials[0], figsize=(8, 1.5))
plt.show()

plot_material_defects(materials[1], figsize=(8, 1.5))
plt.show()
"""

"""
import matplotlib

matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np  # 添加缺失的numpy导入

# 输入数据（修正了字符串中的引号问题）
materials = [
    {"id": 1, "length": 5.5,
     "defects": [{"start": 1.0, "length": 0.03},
                 {"start": 2.5, "length": 0.04}]},
    {"id": 3, "length": 7.8,
     "defects": [{"start": 3.0, "length": 0.03}]}
]


def plot_material_defects(mat, figsize=(8, 2)):
    fig = plt.figure(figsize=figsize, dpi=120)
    ax = fig.add_subplot(111)

    # 修改为当前支持的样式
    plt.style.use('seaborn-v0_8-whitegrid')  # 使用seaborn白底网格样式

    # 绘制材料主体
    ax.broken_barh([(0, mat["length"])], (-0.4, 0.8),
                   facecolors='#E8E8E8', edgecolor='#4A4A4A',
                   linewidth=1, zorder=1)

    # 绘制缺陷区域（修正了字符串引号问题）
    for i, defect in enumerate(mat["defects"]):
        ax.broken_barh([(defect["start"], defect["length"])], (-0.4, 0.8),
                       facecolors='#FF4B4B', edgecolor='#C70039',
                       linewidth=0.8, hatch='///', zorder=2)

        defect_center = defect["start"] + defect["length"] / 2
        ax.text(defect_center, 0.05, f"D{i + 1}\n({defect['length']}m)",  # 修正引号使用
                ha='center', va='bottom', color='black',
                fontsize=8, fontweight='bold', zorder=3)

    # 设置刻度
    ax.set_xticks(np.arange(0, mat["length"] + 0.5, 0.5))
    ax.set_xticks(np.arange(0, mat["length"] + 0.1, 0.1), minor=True)
    ax.set_xlim(0, mat["length"] * 1.05)
    ax.set_yticks([])

    # 设置网格
    ax.grid(which='major', axis='x', linestyle='--', alpha=0.7)
    ax.grid(which='minor', axis='x', linestyle=':', alpha=0.4)

    ax.set_title(f"Material {mat['id']} Defect Visualization (Total Length: {mat['length']}m)",
                 pad=12, fontsize=10, fontweight='bold')

    # 添加图例
    legend_elements = [
        Patch(facecolor='#E8E8E8', edgecolor='#4A4A4A', label='Intact Material'),
        Patch(facecolor='#FF4B4B', edgecolor='#C70039', hatch='///', label='Defect Area')
    ]
    ax.legend(handles=legend_elements, loc='upper right',
              frameon=True, framealpha=0.9)

    plt.tight_layout()
    return fig


plot_material_defects(materials[1], figsize=(8, 1.5))
plt.show()
"""


