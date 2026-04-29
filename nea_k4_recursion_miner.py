import numpy as np
import networkx as nx
import scipy.linalg as la
import matplotlib.pyplot as plt

def calculate_nea_rent(matrix):
    """计算矩阵的 N.E.A. 租金：特征根之和"""
    eigenvals = la.eigvalsh(matrix)
    # 过滤微小负值
    eigenvals = np.maximum(eigenvals, 1e-10)
    return np.sum(np.sqrt(eigenvals))

def simulate_k4_nesting(max_gen=4):
    """
    模拟 K4 结构的递归嵌套。
    第一代：标准 K4
    第二代：K4 的每个节点内部再次进行 K4 锁定（Kronecker 积或权重叠加）
    """
    print(f"--- OP-5: K4 递归租金动力学审计 (深度: {max_gen}) ---")
    
    # 1. 定义基础单元：K4 的拉普拉斯矩阵
    K4 = nx.complete_graph(4)
    L_k4 = nx.laplacian_matrix(K4).toarray()
    
    results = []
    
    # 模拟“带宽挤压”下的非线性叠加
    # 在 N.E.A. 逻辑中，更高代的锁定是在同一个“物理节点”的内部位宽里进行的
    for gen in range(1, max_gen + 1):
        # 使用 Kronecker 和来模拟多维相位的递归锁定
        # 这代表了每一代在逻辑空间中增加的自由度
        if gen == 1:
            L_gen = L_k4
        else:
            # 递归构造：L_n = L_{n-1} ⊕ L_k4
            # 这模拟了在原有锁定基础上增加新的独立相位循环
            I_prev = np.eye(L_gen.shape[0])
            I_k4 = np.eye(4)
            L_gen = np.kron(L_gen, I_k4) + np.kron(I_prev, L_k4)
        
        # 计算总租金
        total_rent = calculate_nea_rent(L_gen)
        # 归一化到单位物理节点（第一代的4个节点）
        unit_rent = total_rent / (4**gen)
        
        results.append(unit_rent)
        print(f"第 {gen} 代单位租金: {unit_rent:.4f} ZY")

    # 2. 计算边际租金衰减（折射率）
    print("\n--- 边际租金分析 (f_K4 压缩函数) ---")
    diffs = []
    for i in range(1, len(results)):
        ratio = results[i] / results[i-1]
        # 计算“谱压缩比”
        # 这个比值应该对应 CKM 矩阵的层级系数 lambda (约 0.22)
        print(f"代际压缩比 (Gen{i+1}/Gen{i}): {ratio:.4f}")
        diffs.append(ratio)
        
    return results, diffs

def analyze_ckm_link(ratios):
    """
    尝试将压缩比与 CKM 矩阵元素 V_cb, V_ub 挂钩
    """
    print("\n--- CKM 路径锁定审计 ---")
    # 实验观测：V_us ~ 0.22, V_cb ~ 0.04, V_ub ~ 0.003
    # 对应的层级关系是 lambda, lambda^2, lambda^3
    if len(ratios) >= 1:
        derived_lambda = ratios[0] - 1.0 # 提取增量部分的缩放
        print(f"推导的拓扑扰动因子 (lambda_derived): {abs(derived_lambda):.4f}")
        print(f"预期 lambda (Wolfenstein 参数): 0.225")

if __name__ == "__main__":
    rents, ratios = simulate_k4_nesting(3)
    analyze_ckm_link(ratios)
    
    # 可视化非线性压缩
    plt.figure(figsize=(8, 5))
    plt.plot(range(1, len(rents)+1), rents, 'ro-', label='Unit Rent (Stiffness)')
    plt.title("Non-linear Rent Compression in K4 Stacking")
    plt.xlabel("Generation (Generation Layer)")
    plt.ylabel("Rent per Physical Node (ZY)")
    plt.grid(True, alpha=0.3)
    plt.show()