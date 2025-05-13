"""
import matplotlib

matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import numpy as np


def create_cutting_demo(material_length, cuts, title):
    plt.style.use('ggplot')

    fig, ax = plt.subplots(figsize=(10, 2), dpi=120)

    # 绘制完整材料
    ax.broken_barh([(0, material_length)], (-0.4, 0.8),
                   facecolors='#E8E8E8', edgecolor='#4A4A4A', linewidth=1)

    # 生成切割分段
    segments = []
    prev = 0.0
    for cut in sorted(cuts):
        segments.append((prev, cut - prev))
        prev = cut
    segments.append((prev, material_length - prev))

    # 添加分段标签（仅标注前两段）
    labels = ['a', 'b']
    for i, (start, width) in enumerate(segments[:2]):
        center = start + width / 2
        ax.text(center, 0.4, labels[i],  # y=0.4位于材料条中心
                ha='center', va='center',
                fontsize=14, color='#2E75B6',  # 使用与切割线相同的蓝色
                fontweight='bold')

    # 添加切割线
    for cut_position in cuts:
        ax.axvline(x=cut_position, color='#2E75B6', linewidth=2, linestyle='--')

    # 设置刻度
    ax.set_xticks(np.arange(0, material_length + 0.5, 0.5))
    ax.set_xticks(np.arange(0, material_length + 0.1, 0.1), minor=True)
    ax.set_xlim(0, material_length)
    ax.set_yticks([])

    # 设置网格和标题
    ax.grid(axis='x', which='major', linestyle='--', alpha=0.7)
    ax.grid(axis='x', which='minor', linestyle=':', alpha=0.4)
    ax.set_title(f"{title} (Length: {material_length}m)", pad=12, fontsize=12, fontweight='bold')

    plt.tight_layout()
    return fig


# 生成两刀切割示意图（5.5米材料）
# create_cutting_demo(material_length=5.5,
#                     cuts=[1.8, 3.6],
#                     title="Cutting Pattern 1")
# plt.show()
"""

"""
import matplotlib

matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import numpy as np


def create_cutting_demo(material_length, cuts, title):
    plt.style.use('ggplot')

    fig, ax = plt.subplots(figsize=(10, 2), dpi=120)

    # 绘制完整材料
    ax.broken_barh([(0, material_length)], (-0.4, 0.8),
                   facecolors='#E8E8E8', edgecolor='#4A4A4A', linewidth=1)

    # 生成切割分段
    sorted_cuts = sorted(cuts)
    segments = []
    prev = 0.0
    for cut in sorted_cuts + [material_length]:  # 添加材料末端
        segments.append((prev, cut - prev))
        prev = cut

    # 确定中间两段（总段数-2）
    mid_segments = segments[1:-1]  # 排除首尾段

    # 添加中间段标签
    labels = ['a', 'b']
    for i, (start, width) in enumerate(mid_segments[:2]):  # 只取前两个中间段
        center = start + width / 2
        ax.text(center, 0.4, labels[i],
                ha='center', va='center',
                fontsize=14, color='#2E75B6',
                fontweight='bold',
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))  # 添加白色背景

    # 添加切割线
    for cut_position in sorted_cuts:
        ax.axvline(x=cut_position, color='#2E75B6', linewidth=2, linestyle='--')

    # 设置刻度
    ax.set_xticks(np.arange(0, material_length + 0.5, 0.5))
    ax.set_xticks(np.arange(0, material_length + 0.1, 0.1), minor=True)
    ax.set_xlim(0, material_length)
    ax.set_yticks([])

    # 设置网格和标题
    ax.grid(axis='x', which='major', linestyle='--', alpha=0.7)
    ax.grid(axis='x', which='minor', linestyle=':', alpha=0.4)
    ax.set_title(f"{title} (Length: {material_length}m)", pad=12, fontsize=12, fontweight='bold')

    plt.tight_layout()
    return fig


# 生成三刀切割示意图（6.2米材料）
create_cutting_demo(material_length=6.2,
                    cuts=[0.5, 2.0, 5.2],
                    title="Cutting Pattern 2")
plt.show()
"""