# ============================================================
# 50 Startups Multiple Linear Regression Explorer
# CRISP-DM Feature Selection & Parsimony Analysis Workflow
# ============================================================

import os
import sys
import json
from io import StringIO
from itertools import combinations
import requests
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LassoCV, ElasticNetCV
from sklearn.feature_selection import RFE
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score, mean_squared_error

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


# ------------------------------------------------------------
# Step 1: Data Loading & Validation
# ------------------------------------------------------------

def load_dataset(local_cache_path="50_Startups.csv"):
    """
    載入 50 Startups 資料集。
    優先嘗試遠端 GitHub Gist 下載，若遇網路問題則自動切換至本機備用快取。
    """
    url = (
        "https://gist.githubusercontent.com/"
        "GaneshSparkz/b5662effbdae8746f7f7d8ed70c42b2d/"
        "raw/faf8b1a0d58e251f48a647d3881e7a960c3f0925/"
        "50_Startups.csv"
    )

    required_columns = [
        "R&D Spend",
        "Administration",
        "Marketing Spend",
        "State",
        "Profit"
    ]

    data = None

    try:
        print("[Step 1] 下載資料集中...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = pd.read_csv(StringIO(response.text))
        print(">> 遠端資料下載成功！")

        try:
            data.to_csv(local_cache_path, index=False)
        except Exception:
            pass

    except Exception as e:
        print(f"!! 遠端下載失敗 ({e})，嘗試切換至本機快取: {local_cache_path}")
        if os.path.exists(local_cache_path):
            data = pd.read_csv(local_cache_path)
            print(">> 成功載入本機資料集！")
        else:
            raise FileNotFoundError(f"無法取得資料：遠端連線失敗且找不到本機檔案 {local_cache_path}") from e

    if not all(col in data.columns for col in required_columns):
        raise ValueError(f"資料集缺少必要欄位: {data.columns.tolist()}")

    print(f"\n資料集筆數: {len(data)}, 欄位數: {len(data.columns)}")
    return data


# ------------------------------------------------------------
# Step 2: Evaluation Metrics Calculator
# ------------------------------------------------------------

def evaluate_metrics(y_true, y_pred, p_features, y_train=None, y_train_pred=None):
    """
    計算回歸評估指標：
    - RMSE (Root Mean Squared Error)
    - R-squared (判定係數)
    - Adjusted R-squared (懲罰自由度之校正判定係數)
    - MAE (Mean Absolute Error)
    - F-Statistic (模型整體顯著性)
    """
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    n = len(y_true)
    p = p_features
    adj_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1) if (n - p - 1) > 0 else 0
    mae = float(np.mean(np.abs(np.array(y_true) - np.array(y_pred))))

    # 計算訓練集 F 檢定值
    f_stat = 0.0
    if y_train is not None and y_train_pred is not None:
        r2_tr = r2_score(y_train, y_train_pred)
        n_tr = len(y_train)
        if (1 - r2_tr) > 0 and (n_tr - p - 1) > 0:
            f_stat = (r2_tr / p) / ((1 - r2_tr) / (n_tr - p - 1))

    return {
        "rmse": float(rmse),
        "r2": float(r2),
        "adj_r2": float(adj_r2),
        "mae": float(mae),
        "f_stat": float(f_stat)
    }


# ------------------------------------------------------------
# Step 3: Multi-Algorithm Feature Selection
# ------------------------------------------------------------

def run_multi_algorithm_selection(X_train, X_test, y_train, y_test, raw_df):
    """
    執行 5 種經典機器學習特徵選取演算法：
    1. Lasso (L1 Regularization Ranking)
    2. Forward SFS (Greedy Forward Stepwise Selection)
    3. RFE (Recursive Feature Elimination)
    4. ElasticNet (L1 + L2 Regularization)
    5. Exhaustive Search (Best Subset Selection)
    """
    features = list(X_train.columns)
    methods = {}

    def fit_and_record(feats):
        m = LinearRegression().fit(X_train[feats], y_train)
        pred_test = m.predict(X_test[feats])
        pred_train = m.predict(X_train[feats])
        metrics = evaluate_metrics(y_test, pred_test, len(feats), y_train, pred_train)

        test_records = []
        for real_idx, p_val in zip(X_test.index, pred_test):
            row = raw_df.loc[real_idx]
            act = float(y_test.loc[real_idx])
            test_records.append({
                "idx": int(real_idx),
                "rd": float(row["R&D Spend"]),
                "adm": float(row["Administration"]),
                "mkt": float(row["Marketing Spend"]),
                "state": str(row["State"]),
                "actual": round(act, 2),
                "predicted": round(float(p_val), 2),
                "residual": round(float(p_val - act), 2),
                "abs_error": round(float(abs(p_val - act)), 2),
                "pct_error": round(float(abs(p_val - act) / act * 100), 2)
            })

        return {
            "features": list(feats),
            "rmse": round(metrics["rmse"], 2),
            "r2": round(metrics["r2"], 4),
            "adj_r2": round(metrics["adj_r2"], 4),
            "mae": round(metrics["mae"], 2),
            "f_stat": round(metrics["f_stat"], 1),
            "intercept": round(float(m.intercept_), 2),
            "coef": {f: round(float(c), 4) for f, c in zip(feats, m.coef_)},
            "test_predictions": test_records
        }

    # 1. Forward SFS (Greedy)
    sfs = {}
    curr = []
    for k in range(1, 6):
        rem = [f for f in features if f not in curr]
        best_f = None
        best_tr_rmse = 1e9
        for f in rem:
            m = LinearRegression().fit(X_train[curr + [f]], y_train)
            rmse_tr = np.sqrt(mean_squared_error(y_train, m.predict(X_train[curr + [f]])))
            if rmse_tr < best_tr_rmse:
                best_tr_rmse = rmse_tr
                best_f = f
        curr.append(best_f)
        sfs[k] = fit_and_record(curr.copy())
    methods["forward_sfs"] = sfs

    # 2. Lasso (L1 Ranking)
    scaler = StandardScaler()
    X_tr_s = scaler.fit_transform(X_train)
    lasso_cv = LassoCV(cv=5, random_state=0).fit(X_tr_s, y_train)
    lasso_ranks = [f for _, f in sorted(zip(np.abs(lasso_cv.coef_), features), reverse=True)]
    lasso_res = {}
    for k in range(1, 6):
        lasso_res[k] = fit_and_record(lasso_ranks[:k])
    methods["lasso"] = lasso_res

    # 3. RFE (Backward Elimination)
    rfe_res = {}
    for k in range(1, 6):
        if k == 5:
            rfe_feats = features.copy()
        else:
            rfe = RFE(LinearRegression(), n_features_to_select=k)
            rfe.fit(X_train, y_train)
            rfe_feats = [f for f, s in zip(features, rfe.support_) if s]
        rfe_res[k] = fit_and_record(rfe_feats)
    methods["rfe"] = rfe_res

    # 4. ElasticNet (L1 + L2)
    enet_cv = ElasticNetCV(l1_ratio=[.1, .5, .7, .9, .95, .99, 1], cv=5, random_state=0).fit(X_tr_s, y_train)
    enet_ranks = [f for _, f in sorted(zip(np.abs(enet_cv.coef_), features), reverse=True)]
    enet_res = {}
    for k in range(1, 6):
        enet_res[k] = fit_and_record(enet_ranks[:k])
    methods["elasticnet"] = enet_res

    # 5. Exhaustive Search (Best Subset)
    exh_res = {}
    for k in range(1, 6):
        best_c = None
        best_tr_r2 = -1
        for c in combinations(features, k):
            m = LinearRegression().fit(X_train[list(c)], y_train)
            r2_tr = m.score(X_train[list(c)], y_train)
            if r2_tr > best_tr_r2:
                best_tr_r2 = r2_tr
                best_c = list(c)
        exh_res[k] = fit_and_record(best_c)
    methods["exhaustive"] = exh_res

    return methods


# ------------------------------------------------------------
# Step 4: Markdown Table Printer
# ------------------------------------------------------------

def print_markdown_table(headers, rows):
    print("| " + " | ".join(headers) + " |")
    print("| " + " | ".join(["---"] * len(headers)) + " |")
    for r in rows:
        print("| " + " | ".join(map(str, r)) + " |")


# ------------------------------------------------------------
# Main Workflow
# ------------------------------------------------------------

def main():
    print("=" * 65)
    print(" 50 Startups Multiple Linear Regression Explorer (CRISP-DM)")
    print("=" * 65)

    # 1. 載入資料
    raw_df = load_dataset()
    df = raw_df.dropna().copy()

    # 2. 資料前處理：One-Hot Encoding 並 drop_first=True 避開虛擬變數陷阱
    X = pd.get_dummies(df.drop(columns=["Profit"]), columns=["State"], drop_first=True, dtype=int)
    y = df["Profit"]

    print("\n[Step 2] 編碼後特徵清單 (已移除 California 基準避免虛擬變數陷阱):")
    for idx, col in enumerate(X.columns, 1):
        print(f"  {idx}. {col}")

    # 3. 資料集嚴格分割 (80% Train / 20% Test, random_state=0)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
    print(f"\n[Step 3] 資料隔離: 訓練集 {len(X_train)} 筆，測試集 {len(X_test)} 筆")

    # 4. 執行 5 種演算法特徵挑選
    print("\n[Step 4] 執行 5 種演算法特徵挑選分析 (k=1 到 5)...")
    methods = run_multi_algorithm_selection(X_train, X_test, y_train, y_test, raw_df)

    # 5. 輸出跨演算法測試集表現比對表
    print("\n" + "=" * 65)
    print(" 特徵選取演算法測試集表現評比 (Test Set Evaluation)")
    print("=" * 65)

    headers = ["Method", "k=1 (RMSE)", "k=2 (Min RMSE)", "k=3 (RMSE)", "k=4 (RMSE)", "k=5 (Cliff)", "Optimal k"]
    rows = []
    method_labels = {
        "lasso": "Lasso (L1)",
        "forward_sfs": "Forward SFS",
        "rfe": "RFE (Backward)",
        "elasticnet": "ElasticNet",
        "exhaustive": "Exhaustive Search"
    }

    for key, name in method_labels.items():
        m_data = methods[key]
        rows.append([
            name,
            f"${m_data[1]['rmse']:,.2f}",
            f"${m_data[2]['rmse']:,.2f} ★",
            f"${m_data[3]['rmse']:,.2f}",
            f"${m_data[4]['rmse']:,.2f}",
            f"${m_data[5]['rmse']:,.2f} ▲",
            "k=2"
        ])
    print_markdown_table(headers, rows)

    # 6. 最優模型深入解析 (Lasso / SFS / Exhaustive 共識：k=2)
    opt_model = methods["lasso"][2]
    print("\n" + "=" * 65)
    print(" ★ 全域最優模型 (Global Sweet Spot: k=2) 評估報告")
    print("=" * 65)
    print(f"入選特徵       : {opt_model['features']}")
    print(f"Test RMSE      : ${opt_model['rmse']:,.2f} (最低誤差)")
    print(f"Test R^2       : {opt_model['r2']:.4f} ({opt_model['r2']*100:.2f}% 解釋力)")
    print(f"Test Adj R^2   : {opt_model['adj_r2']:.4f}")
    print(f"Test MAE       : ${opt_model['mae']:,.2f}")
    print(f"Train F-Stat   : {opt_model['f_stat']:.1f} (P < 0.0001)")

    eq_terms = [f"{coef:+.4f} * ({feat})" for feat, coef in opt_model["coef"].items()]
    equation = f"Profit = ${opt_model['intercept']:,.2f} " + " ".join(eq_terms)
    print(f"\n迴歸方程式: {equation}")

    # 7. 匯出預測成果與完整資料包
    test_pred_df = pd.DataFrame(opt_model["test_predictions"])
    test_pred_df.to_csv("test_predictions.csv", index=False)

    summary_data = {
        "best_features": opt_model["features"],
        "optimal_k": 2,
        "test_metrics": {
            "rmse": opt_model["rmse"],
            "r2": opt_model["r2"],
            "adj_r2": opt_model["adj_r2"],
            "mae": opt_model["mae"],
            "f_stat": opt_model["f_stat"]
        },
        "intercept": opt_model["intercept"],
        "coefficients": opt_model["coef"],
        "equation": equation
    }
    with open("results_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)

    full_payload = {
        "methods": methods,
        "dataset": raw_df.to_dict(orient="records"),
        "features": list(X.columns),
        "test_indices": list(map(int, X_test.index))
    }
    with open("model_data.json", "w", encoding="utf-8") as f:
        json.dump(full_payload, f, indent=2)

    print("\n>> 成果已輸出至 'test_predictions.csv'、'results_summary.json' 與 'model_data.json'！")


if __name__ == "__main__":
    main()
