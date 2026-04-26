import os
import pickle
import random

import pandas as pd
import streamlit as st

MODEL_PATH = "models/churn_model.pkl"

SCENARIOS = {
    "loyal_low_risk": {
        "label": "Лояльный клиент",
        "data": {
            "gender": "Male", "SeniorCitizen": 0, "Partner": "Yes", "Dependents": "Yes",
            "tenure": 60, "PhoneService": "Yes", "MultipleLines": "Yes",
            "InternetService": "DSL", "OnlineSecurity": "Yes", "OnlineBackup": "Yes",
            "DeviceProtection": "Yes", "TechSupport": "Yes", "StreamingTV": "No",
            "StreamingMovies": "No", "Contract": "Two year", "PaperlessBilling": "No",
            "PaymentMethod": "Bank transfer (automatic)", "MonthlyCharges": 55.0, "TotalCharges": 3300.0,
        },
    },
    "high_churn_risk": {
        "label": "Высокий риск оттока",
        "data": {
            "gender": "Female", "SeniorCitizen": 0, "Partner": "No", "Dependents": "No",
            "tenure": 2, "PhoneService": "Yes", "MultipleLines": "No",
            "InternetService": "Fiber optic", "OnlineSecurity": "No", "OnlineBackup": "No",
            "DeviceProtection": "No", "TechSupport": "No", "StreamingTV": "Yes",
            "StreamingMovies": "Yes", "Contract": "Month-to-month", "PaperlessBilling": "Yes",
            "PaymentMethod": "Electronic check", "MonthlyCharges": 95.0, "TotalCharges": 190.0,
        },
    },
    "medium_risk_senior": {
        "label": "Средний риск (пожилой)",
        "data": {
            "gender": "Male", "SeniorCitizen": 1, "Partner": "No", "Dependents": "No",
            "tenure": 12, "PhoneService": "Yes", "MultipleLines": "No",
            "InternetService": "Fiber optic", "OnlineSecurity": "No", "OnlineBackup": "Yes",
            "DeviceProtection": "No", "TechSupport": "No", "StreamingTV": "No",
            "StreamingMovies": "No", "Contract": "Month-to-month", "PaperlessBilling": "Yes",
            "PaymentMethod": "Electronic check", "MonthlyCharges": 75.0, "TotalCharges": 900.0,
        },
    },
    "moderate_loyal_one_year": {
        "label": "Умеренно лояльный (One year)",
        "data": {
            "gender": "Female", "SeniorCitizen": 0, "Partner": "Yes", "Dependents": "No",
            "tenure": 24, "PhoneService": "Yes", "MultipleLines": "No",
            "InternetService": "DSL", "OnlineSecurity": "Yes", "OnlineBackup": "No",
            "DeviceProtection": "Yes", "TechSupport": "No", "StreamingTV": "No",
            "StreamingMovies": "Yes", "Contract": "One year", "PaperlessBilling": "Yes",
            "PaymentMethod": "Credit card (automatic)", "MonthlyCharges": 60.0, "TotalCharges": 1440.0,
        },
    },
    "phone_only_no_internet": {
        "label": "Только телефон, без интернета",
        "data": {
            "gender": "Male", "SeniorCitizen": 0, "Partner": "No", "Dependents": "No",
            "tenure": 5, "PhoneService": "Yes", "MultipleLines": "No",
            "InternetService": "No", "OnlineSecurity": "No internet service",
            "OnlineBackup": "No internet service", "DeviceProtection": "No internet service",
            "TechSupport": "No internet service", "StreamingTV": "No internet service",
            "StreamingMovies": "No internet service", "Contract": "Month-to-month",
            "PaperlessBilling": "No", "PaymentMethod": "Mailed check",
            "MonthlyCharges": 20.0, "TotalCharges": 100.0,
        },
    },
}

FIELD_OPTIONS = {
    'gender': ["Female", "Male"],
    'SeniorCitizen': [0, 1],
    'Partner': ["Yes", "No"],
    'Dependents': ["Yes", "No"],
    'PhoneService': ["Yes", "No"],
    'MultipleLines': ["No phone service", "No", "Yes"],
    'InternetService': ["DSL", "Fiber optic", "No"],
    'OnlineSecurity': ["No", "Yes", "No internet service"],
    'OnlineBackup': ["No", "Yes", "No internet service"],
    'DeviceProtection': ["No", "Yes", "No internet service"],
    'TechSupport': ["No", "Yes", "No internet service"],
    'StreamingTV': ["No", "Yes", "No internet service"],
    'StreamingMovies': ["No", "Yes", "No internet service"],
    'Contract': ["Month-to-month", "One year", "Two year"],
    'PaperlessBilling': ["Yes", "No"],
    'PaymentMethod': ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"],
}


def load_artifacts():
    if not os.path.exists(MODEL_PATH):
        return None
    with open(MODEL_PATH, 'rb') as f:
        return pickle.load(f)


def apply_scenario(data):
    for key, value in data.items():
        st.session_state[f'f_{key}'] = value


def apply_random():
    tenure = random.randint(0, 72)
    monthly = round(random.uniform(18.0, 120.0), 2)
    for field, options in FIELD_OPTIONS.items():
        st.session_state[f'f_{field}'] = random.choice(options)
    st.session_state['f_tenure'] = tenure
    st.session_state['f_MonthlyCharges'] = monthly
    st.session_state['f_TotalCharges'] = round(tenure * monthly, 2)


def show_ui():
    artifacts = load_artifacts()

    st.set_page_config(page_title="Telecom Churn Prediction", layout="wide")
    st.title("Прогнозирование оттока клиентов (Telecom Churn)")

    if artifacts is None:
        st.error(f"Модель не найдена в {MODEL_PATH}. Сначала запустите `uv run src/train.py`.")
        return

    st.markdown("### Быстрый выбор сценария")
    btn_cols = st.columns(len(SCENARIOS) + 1)
    for i, (key, scenario) in enumerate(SCENARIOS.items()):
        btn_cols[i].button(
            scenario["label"],
            on_click=apply_scenario,
            kwargs={"data": scenario["data"]},
            use_container_width=True,
        )
    btn_cols[-1].button(
        "Случайные данные",
        on_click=apply_random,
        use_container_width=True,
        type="secondary",
    )

    st.divider()
    st.markdown("### Введите данные клиента для прогноза")

    input_data = {}

    tab1, tab2, tab3 = st.tabs(["Демография", "Услуги", "Контракт"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            input_data['gender'] = st.selectbox("Пол", FIELD_OPTIONS['gender'], key='f_gender')
            input_data['SeniorCitizen'] = st.selectbox("Пожилой гражданин", FIELD_OPTIONS['SeniorCitizen'], key='f_SeniorCitizen')
        with col2:
            input_data['Partner'] = st.selectbox("Наличие партнера", FIELD_OPTIONS['Partner'], key='f_Partner')
            input_data['Dependents'] = st.selectbox("Наличие иждивенцев", FIELD_OPTIONS['Dependents'], key='f_Dependents')

    with tab2:
        col1, col2, col3 = st.columns(3)
        with col1:
            input_data['tenure'] = st.slider("Срок обслуживания (мес)", 0, 72, 12, key='f_tenure')
            input_data['PhoneService'] = st.selectbox("Телефонная связь", FIELD_OPTIONS['PhoneService'], key='f_PhoneService')
            input_data['MultipleLines'] = st.selectbox("Несколько линий", FIELD_OPTIONS['MultipleLines'], key='f_MultipleLines')
        with col2:
            input_data['InternetService'] = st.selectbox("Интернет", FIELD_OPTIONS['InternetService'], key='f_InternetService')
            input_data['OnlineSecurity'] = st.selectbox("Онлайн-безопасность", FIELD_OPTIONS['OnlineSecurity'], key='f_OnlineSecurity')
            input_data['OnlineBackup'] = st.selectbox("Облачное хранилище", FIELD_OPTIONS['OnlineBackup'], key='f_OnlineBackup')
        with col3:
            input_data['DeviceProtection'] = st.selectbox("Защита устройств", FIELD_OPTIONS['DeviceProtection'], key='f_DeviceProtection')
            input_data['TechSupport'] = st.selectbox("Техподдержка", FIELD_OPTIONS['TechSupport'], key='f_TechSupport')
            input_data['StreamingTV'] = st.selectbox("Стриминговое ТВ", FIELD_OPTIONS['StreamingTV'], key='f_StreamingTV')
            input_data['StreamingMovies'] = st.selectbox("Стриминговое кино", FIELD_OPTIONS['StreamingMovies'], key='f_StreamingMovies')

    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            input_data['Contract'] = st.selectbox("Тип контракта", FIELD_OPTIONS['Contract'], key='f_Contract')
            input_data['PaperlessBilling'] = st.selectbox("Электронный чек", FIELD_OPTIONS['PaperlessBilling'], key='f_PaperlessBilling')
            input_data['PaymentMethod'] = st.selectbox("Способ оплаты", FIELD_OPTIONS['PaymentMethod'], key='f_PaymentMethod')
        with col2:
            input_data['MonthlyCharges'] = st.number_input("Ежемесячный платеж", 0.0, 200.0, 50.0, key='f_MonthlyCharges')
            input_data['TotalCharges'] = st.number_input("Общая сумма платежей", 0.0, 10000.0, 500.0, key='f_TotalCharges')

    if st.button("Предсказать отток", type="primary"):
        df_input = pd.DataFrame([input_data])

        for col, le in artifacts['encoders'].items():
            df_input[col] = le.transform(df_input[col])

        if artifacts.get('scaler') is not None:
            df_input[artifacts['num_cols']] = artifacts['scaler'].transform(df_input[artifacts['num_cols']])

        THRESHOLD = 0.35
        model = artifacts['model']
        prob = model.predict_proba(df_input)[0][1]
        pred = int(prob >= THRESHOLD)

        st.divider()
        col_res1, col_res2 = st.columns(2)

        with col_res1:
            if pred == 1:
                st.error("Прогноз: КЛИЕНТ УЙДЕТ (Churn)")
            else:
                st.success("Прогноз: КЛИЕНТ ОСТАНЕТСЯ (Loyal)")

        with col_res2:
            st.metric("Вероятность оттока", f"{prob*100:.2f}%")
            st.progress(prob)

        if prob >= THRESHOLD:
            st.warning("Внимание: Высокий риск потери клиента. Рекомендуется предложить скидку или бонус.")
        else:
            st.info("Клиент стабилен. Продолжайте текущую стратегию взаимодействия.")


def launch_app():
    import subprocess
    import sys
    subprocess.run([sys.executable, "-m", "streamlit", "run", __file__])


if __name__ == "__main__":
    show_ui()
