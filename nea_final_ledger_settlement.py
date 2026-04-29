import numpy as np

def settle_ckm_final():
    """
    Vus 结算：回归 v3.0 的几何投影逻辑。
    Vus = sin( theta_K4_C8 * R )
    """
    print("\n--- [参数 1] CKM V_us (卡比博角) 最终清算 ---")
    R = 1.0 / (1.0 + np.pi) 
    # 正四面体面法线与立方体轴的夹角 (arccos(1/sqrt(3)))
    theta = np.arccos(1.0/np.sqrt(3))
    
    # 25位机器的寻址漏损修正
    leakage = (10 * np.sqrt(3)) / (25 * np.log(2)) - 1 # 约 0.0005
    
    v_us_calc = np.sin(theta * R * (1 + leakage))
    v_us_obs = 0.2245
    
    print(f"N.E.A. 几何投影 V_us: {v_us_calc:.5f}")
    print(f"实验观测值: {v_us_obs:.5f}")
    print(f"清算精度: {100*(1-np.abs(v_us_calc-v_us_obs)/v_us_obs):.4f}%")

def settle_quark_ratio_final():
    """
    质量比结算：基于“首位债务”原理。
    m_d / m_u = 2 + R/pi
    """
    print("\n--- [参数 2] 夸克质量比 (m_d/m_u) 最终清算 ---")
    R = 1.0 / (1.0 + np.pi)
    
    # 2 代表 Stride-10 的对称双向性，R/pi 代表投影残差损耗
    ratio_calc = 2.0 + (R / np.pi)
    obs_ratio = 4.7 / 2.2 # 2.1364
    
    print(f"N.E.A. 债务比 (m_d/m_u): {ratio_calc:.5f}")
    print(f"实验观测值: {obs_ratio:.5f}")
    print(f"清算精度: {100*(1-np.abs(ratio_calc-obs_ratio)/obs_ratio):.4f}%")

def settle_alpha_strong_final():
    """
    强力结算：双向寻址占用率。
    alpha_s = 2 / U_weak
    """
    print("\n--- [参数 3] 强力耦合 alpha_s (Mz) 最终清算 ---")
    u_weak = 10 * np.sqrt(3)
    
    # 强力是 2 个 Stride-1 脉冲在 U_weak 寻址深度下的压强
    alpha_s_calc = 2.0 / u_weak
    alpha_s_obs = 0.1180
    
    # 考虑 Mz 能标下的 3D 海绵收缩修正 (1 + R^2)
    R = 1.0 / (1.0 + np.pi)
    alpha_s_corrected = alpha_s_calc * (1 + R**2)
    
    print(f"N.E.A. 基础占用率: {alpha_s_calc:.5f}")
    print(f"Mz 能标修正值: {alpha_s_corrected:.5f}")
    print(f"实验观测值: {alpha_s_obs:.5f}")
    print(f"清算精度: {100*(1-np.abs(alpha_s_corrected-alpha_s_obs)/alpha_s_obs):.4f}%")

if __name__ == "__main__":
    print("==========================================")
    print("   N.E.A. GUT 账本：19 参数最后结算 (v5.0)   ")
    print("==========================================")
    settle_ckm_final()
    settle_quark_ratio_final()
    settle_alpha_strong_final()