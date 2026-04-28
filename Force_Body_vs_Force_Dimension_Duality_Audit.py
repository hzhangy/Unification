import numpy as np
import networkx as nx
from itertools import combinations

def cycle_basis_count(G):
    """
    返回图G的基本圈数量 = 边数 - 顶点数 + 连通分量数
    （对于连通图 = m - n + 1）
    """
    n = G.number_of_nodes()
    m = G.number_of_edges()
    return m - n + 1

def predicted_gauge_dimension(ring_count):
    """
    根据力-体对偶假说，强力的规范群是SU(N)，其中N = 圈数。
    李代数维度 = N^2 - 1
    """
    return ring_count**2 - 1

def test_force_body_duality():
    print("="*70)
    print("  力与体对偶 vs 力与维度对偶：单纯形圈空间测试")
    print("="*70)
    
    # 3D空间最小体积锁定单元：K4 (正四面体)
    K4 = nx.complete_graph(4)
    rings_3d = cycle_basis_count(K4)
    dim_3d = predicted_gauge_dimension(rings_3d)
    
    # 4D空间最小体积锁定单元：K5 (4-单纯形)
    K5 = nx.complete_graph(5)
    rings_4d = cycle_basis_count(K5)
    dim_4d = predicted_gauge_dimension(rings_4d)
    
    print(f"\n3D 最小单纯形 K4:")
    print(f"  顶点数 = 4,  边数 = 6,  圈数 = {rings_3d}")
    print(f"  预测规范群维数 (圈数^2 - 1) = {dim_3d}")
    print(f"  实测强力规范群维数 (SU(3)) = 8")
    
    print(f"\n4D 最小单纯形 K5:")
    print(f"  顶点数 = 5,  边数 = 10, 圈数 = {rings_4d}")
    print(f"  预测规范群维数 (圈数^2 - 1) = {dim_4d}")
    print(f"  (若力与体对偶，4D强力应为 SU({rings_4d})，维数 {dim_4d})")
    
    # 对比两种假说
    print("\n--- 假说对比 ---")
    print("力与维度对偶预测：强力规范群随背景维度变化 (如3D: SU(3), 4D: SU(4) 维数15 或 SO(4) 等)")
    print("力与体对偶预测：强力规范群由单纯形的拓扑不变圈数决定")
    print(f"  3D (K4) 圈数=3 -> SU(3) 维数8  (符合观测)")
    print(f"  4D (K5) 圈数=6 -> SU(6) 维数35 (可检验的理论预言)")
    
    # 也可以展示K4在3D背景和4D背景（若仍用K4）的对比
    print("\n--- 跨维度 K4 测试 (同一个体在不同背景) ---")
    # 如果力与体对偶，K4在任何背景维度下圈数都是3，规范群始终是SU(3)
    print("  K4 固有圈数 = 3，无论嵌入3D或4D，预测规范群维数 = 8 (SU(3))")
    print("  若力与维度对偶，在4D中K4不再是锁定单元，可能不产生强力，或产生不同的群。")
    print("  实验上，若在4D格点中观测到K4激发，其通道数应为8，支撑体对偶。")
    
if __name__ == "__main__":
    test_force_body_duality()