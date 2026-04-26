import os
import pickle

import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

MODEL_PATH = "models/churn_model.pkl"
DATA_PATH = "data/WA_Fn-UseC_-Telco-Customer-Churn.csv"

DEFAULT_THRESHOLD = 0.5
LOWERED_THRESHOLD = 0.35


@pytest.fixture(scope="module")
def artifacts():
    assert os.path.exists(MODEL_PATH), f"Модель не найдена: {MODEL_PATH}"
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


@pytest.fixture(scope="module")
def test_split(artifacts):
    """Воспроизводит тот же train/test split что и при обучении."""
    assert os.path.exists(DATA_PATH), f"Данные не найдены: {DATA_PATH}"

    df = pd.read_csv(DATA_PATH)
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
    df.loc[df["tenure"] == 0, "TotalCharges"] = 0
    df = df.dropna(subset=["TotalCharges"])
    df = df.drop("customerID", axis=1)

    le_target = LabelEncoder()
    df["Churn"] = le_target.fit_transform(df["Churn"])

    cat_cols = df.select_dtypes(include=["object"]).columns.tolist()
    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))

    X = df.drop("Churn", axis=1)
    y = df["Churn"]

    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    return X_test, y_test


def predict_scenario(artifacts, raw_dict):
    """Кодирует сырой словарь через сохранённые энкодеры и возвращает вероятность оттока."""
    df = pd.DataFrame([raw_dict])
    for col, le in artifacts["encoders"].items():
        if col in df.columns:
            df[col] = le.transform(df[col])
    prob = artifacts["model"].predict_proba(df)[0][1]
    return prob


SCENARIOS = {
    "loyal_low_risk": {
        "label": "Лояльный клиент",
        "data": {
            "gender": "Male",
            "SeniorCitizen": 0,
            "Partner": "Yes",
            "Dependents": "Yes",
            "tenure": 60,
            "PhoneService": "Yes",
            "MultipleLines": "Yes",
            "InternetService": "DSL",
            "OnlineSecurity": "Yes",
            "OnlineBackup": "Yes",
            "DeviceProtection": "Yes",
            "TechSupport": "Yes",
            "StreamingTV": "No",
            "StreamingMovies": "No",
            "Contract": "Two year",
            "PaperlessBilling": "No",
            "PaymentMethod": "Bank transfer (automatic)",
            "MonthlyCharges": 55.0,
            "TotalCharges": 3300.0,
        },
        # Двухлетний контракт, стаж 60 мес, все защитные услуги, автоплатёж
        "expected_prob_max_default": 0.20,
        "expected_pred_default": 0, 
        "expected_pred_lowered": 0, 
    },
    "high_churn_risk": {
        "label": "Высокий риск оттока",
        "data": {
            "gender": "Female",
            "SeniorCitizen": 0,
            "Partner": "No",
            "Dependents": "No",
            "tenure": 2,
            "PhoneService": "Yes",
            "MultipleLines": "No",
            "InternetService": "Fiber optic",
            "OnlineSecurity": "No",
            "OnlineBackup": "No",
            "DeviceProtection": "No",
            "TechSupport": "No",
            "StreamingTV": "Yes",
            "StreamingMovies": "Yes",
            "Contract": "Month-to-month",
            "PaperlessBilling": "Yes",
            "PaymentMethod": "Electronic check",
            "MonthlyCharges": 95.0,
            "TotalCharges": 190.0,
        },
        # Стаж 2 мес, Fiber optic без защиты, месячный контракт, electronic check
        "expected_prob_min_default": 0.60,
        "expected_pred_default": 1,
        "expected_pred_lowered": 1, 
    },
    "medium_risk_senior": {
        "label": "Средний риск (пожилой, краткосрочный)",
        "data": {
            "gender": "Male",
            "SeniorCitizen": 1,
            "Partner": "No",
            "Dependents": "No",
            "tenure": 12,
            "PhoneService": "Yes",
            "MultipleLines": "No",
            "InternetService": "Fiber optic",
            "OnlineSecurity": "No",
            "OnlineBackup": "Yes",
            "DeviceProtection": "No",
            "TechSupport": "No",
            "StreamingTV": "No",
            "StreamingMovies": "No",
            "Contract": "Month-to-month",
            "PaperlessBilling": "Yes",
            "PaymentMethod": "Electronic check",
            "MonthlyCharges": 75.0,
            "TotalCharges": 900.0,
        },
        # Стаж 12 мес, Fiber optic, нет OnlineSecurity/TechSupport, пожилой
        "expected_prob_range": (0.40, 0.80),
        "expected_pred_default": 1, 
        "expected_pred_lowered": 1,
    },
    "moderate_loyal_one_year": {
        "label": "Умеренно лояльный (One year, DSL)",
        "data": {
            "gender": "Female",
            "SeniorCitizen": 0,
            "Partner": "Yes",
            "Dependents": "No",
            "tenure": 24,
            "PhoneService": "Yes",
            "MultipleLines": "No",
            "InternetService": "DSL",
            "OnlineSecurity": "Yes",
            "OnlineBackup": "No",
            "DeviceProtection": "Yes",
            "TechSupport": "No",
            "StreamingTV": "No",
            "StreamingMovies": "Yes",
            "Contract": "One year",
            "PaperlessBilling": "Yes",
            "PaymentMethod": "Credit card (automatic)",
            "MonthlyCharges": 60.0,
            "TotalCharges": 1440.0,
        },
        # Стаж 24 мес, годовой контракт, DSL, OnlineSecurity, кредитка
        "expected_prob_max_default": 0.30,
        "expected_pred_default": 0,  
        "expected_pred_lowered": 0,  
    },
    "phone_only_no_internet": {
        "label": "Только телефон, без интернета",
        "data": {
            "gender": "Male",
            "SeniorCitizen": 0,
            "Partner": "No",
            "Dependents": "No",
            "tenure": 5,
            "PhoneService": "Yes",
            "MultipleLines": "No",
            "InternetService": "No",
            "OnlineSecurity": "No internet service",
            "OnlineBackup": "No internet service",
            "DeviceProtection": "No internet service",
            "TechSupport": "No internet service",
            "StreamingTV": "No internet service",
            "StreamingMovies": "No internet service",
            "Contract": "Month-to-month",
            "PaperlessBilling": "No",
            "PaymentMethod": "Mailed check",
            "MonthlyCharges": 20.0,
            "TotalCharges": 100.0,
        },
        # Низкий платёж, нет интернета — нет главного источника неудовлетворённости
        "expected_prob_max_default": 0.30,
        "expected_pred_default": 0,  
        "expected_pred_lowered": 0,   
    },
}



def test_loyal_low_risk_probability(artifacts):
    prob = predict_scenario(artifacts, SCENARIOS["loyal_low_risk"]["data"])
    max_prob = SCENARIOS["loyal_low_risk"]["expected_prob_max_default"]
    assert prob < max_prob, (
        f"Лояльный клиент: ожидаем prob < {max_prob:.0%}, получено {prob:.1%}"
    )


def test_high_churn_risk_probability(artifacts):
    prob = predict_scenario(artifacts, SCENARIOS["high_churn_risk"]["data"])
    min_prob = SCENARIOS["high_churn_risk"]["expected_prob_min_default"]
    assert prob > min_prob, (
        f"Высокий риск: ожидаем prob > {min_prob:.0%}, получено {prob:.1%}"
    )


def test_medium_risk_probability_in_range(artifacts):
    prob = predict_scenario(artifacts, SCENARIOS["medium_risk_senior"]["data"])
    lo, hi = SCENARIOS["medium_risk_senior"]["expected_prob_range"]
    assert lo <= prob <= hi, (
        f"Средний риск: ожидаем prob в [{lo:.0%}, {hi:.0%}], получено {prob:.1%}"
    )


def test_moderate_loyal_low_probability(artifacts):
    prob = predict_scenario(artifacts, SCENARIOS["moderate_loyal_one_year"]["data"])
    max_prob = SCENARIOS["moderate_loyal_one_year"]["expected_prob_max_default"]
    assert prob < max_prob, (
        f"Умеренно лояльный: ожидаем prob < {max_prob:.0%}, получено {prob:.1%}"
    )


def test_phone_only_low_probability(artifacts):
    prob = predict_scenario(artifacts, SCENARIOS["phone_only_no_internet"]["data"])
    max_prob = SCENARIOS["phone_only_no_internet"]["expected_prob_max_default"]
    assert prob < max_prob, (
        f"Только телефон: ожидаем prob < {max_prob:.0%}, получено {prob:.1%}"
    )



@pytest.mark.parametrize("scenario_key", SCENARIOS.keys())
def test_prediction_default_threshold(artifacts, scenario_key):
    scenario = SCENARIOS[scenario_key]
    prob = predict_scenario(artifacts, scenario["data"])
    pred = int(prob >= DEFAULT_THRESHOLD)
    expected = scenario["expected_pred_default"]
    assert pred == expected, (
        f"[threshold={DEFAULT_THRESHOLD}] {scenario['label']}: "
        f"prob={prob:.1%}, ожидали pred={expected}, получили pred={pred}"
    )

@pytest.mark.parametrize("scenario_key", SCENARIOS.keys())
def test_prediction_lowered_threshold(artifacts, scenario_key):
    scenario = SCENARIOS[scenario_key]
    prob = predict_scenario(artifacts, scenario["data"])
    pred = int(prob >= LOWERED_THRESHOLD)
    expected = scenario["expected_pred_lowered"]
    assert pred == expected, (
        f"[threshold={LOWERED_THRESHOLD}] {scenario['label']}: "
        f"prob={prob:.1%}, ожидали pred={expected}, получили pred={pred}"
    )


def test_lowered_threshold_improves_recall(artifacts, test_split):
    """Пониженный порог должен значительно увеличить Recall по классу Churn."""
    X_test, y_test = test_split
    model = artifacts["model"]
    y_prob = model.predict_proba(X_test)[:, 1]

    y_pred_default = (y_prob >= DEFAULT_THRESHOLD).astype(int)
    y_pred_lowered = (y_prob >= LOWERED_THRESHOLD).astype(int)

    recall_default = recall_score(y_test, y_pred_default)
    recall_lowered = recall_score(y_test, y_pred_lowered)

    print(f"\nRecall @0.50: {recall_default:.4f}")
    print(f"Recall @0.35: {recall_lowered:.4f}")
    print(f"Прирост Recall: +{recall_lowered - recall_default:.4f}")

    assert recall_lowered > recall_default, (
        f"Пониженный порог должен увеличить Recall: "
        f"{recall_lowered:.4f} <= {recall_default:.4f}"
    )
    assert recall_lowered >= 0.70, (
        f"Recall при пороге 0.35 должен быть >= 70%, получено {recall_lowered:.1%}"
    )


def test_lowered_threshold_precision_tradeoff(artifacts, test_split):
    """При пониженном пороге Precision падает — ожидаемый компромисс."""
    X_test, y_test = test_split
    model = artifacts["model"]
    y_prob = model.predict_proba(X_test)[:, 1]

    y_pred_default = (y_prob >= DEFAULT_THRESHOLD).astype(int)
    y_pred_lowered = (y_prob >= LOWERED_THRESHOLD).astype(int)

    prec_default = precision_score(y_test, y_pred_default)
    prec_lowered = precision_score(y_test, y_pred_lowered)

    print(f"\nPrecision @0.50: {prec_default:.4f}")
    print(f"Precision @0.35: {prec_lowered:.4f}")

    assert prec_lowered < prec_default, (
        "При пониженном пороге Precision должен снижаться"
    )
    assert prec_lowered >= 0.45, (
        f"Precision при 0.35 не должен падать ниже 45%, получено {prec_lowered:.1%}"
    )


def test_roc_auc_unchanged_by_threshold(artifacts, test_split):
    """ROC-AUC не зависит от порога — должен оставаться выше 0.83."""
    X_test, y_test = test_split
    y_prob = artifacts["model"].predict_proba(X_test)[:, 1]
    auc = roc_auc_score(y_test, y_prob)

    print(f"\nROC-AUC: {auc:.4f}")
    assert auc >= 0.83, f"ROC-AUC должен быть >= 0.83, получено {auc:.4f}"


def test_full_metrics_report(artifacts, test_split, capsys):
    """Выводит сводную таблицу метрик для обоих порогов."""
    X_test, y_test = test_split
    model = artifacts["model"]
    y_prob = model.predict_proba(X_test)[:, 1]

    for threshold in (DEFAULT_THRESHOLD, LOWERED_THRESHOLD):
        y_pred = (y_prob >= threshold).astype(int)
        print(f"\n{'='*40}")
        print(f"  Порог: {threshold}")
        print(f"{'='*40}")
        print(f"  Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
        print(f"  Precision: {precision_score(y_test, y_pred):.4f}")
        print(f"  Recall:    {recall_score(y_test, y_pred):.4f}")
        print(f"  F1-score:  {f1_score(y_test, y_pred):.4f}")
        print(f"  ROC-AUC:   {roc_auc_score(y_test, y_prob):.4f}")

    assert True
