import streamlit as st
import pandas as pd
import pickle
import os

MODEL_PATH = "models/churn_model.pkl"

def load_artifacts():
    if not os.path.exists(MODEL_PATH):
        return None
    with open(MODEL_PATH, 'rb') as f:
        return pickle.load(f)

def show_ui():
    artifacts = load_artifacts()

    st.set_page_config(page_title="Telecom Churn Prediction", layout="wide")

    st.title("Прогнозирование оттока клиентов (Telecom Churn)")

    if artifacts is None:
        st.error(f"Модель не найдена в {MODEL_PATH}. Сначала запустите `uv run src/train.py`.")
    else:
        st.markdown("### Введите данные клиента для прогноза")
        
        tab1, tab2, tab3 = st.tabs(["Демография", "Услуги", "Контракт"])
        
        input_data = {}
        
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                input_data['gender'] = st.selectbox("Пол", ["Female", "Male"])
                input_data['SeniorCitizen'] = st.selectbox("Пожилой гражданин", [0, 1])
            with col2:
                input_data['Partner'] = st.selectbox("Наличие партнера", ["Yes", "No"])
                input_data['Dependents'] = st.selectbox("Наличие иждивенцев", ["Yes", "No"])
                
        with tab2:
            col1, col2, col3 = st.columns(3)
            with col1:
                input_data['tenure'] = st.slider("Срок обслуживания (мес)", 0, 72, 12)
                input_data['PhoneService'] = st.selectbox("Телефонная связь", ["Yes", "No"])
                input_data['MultipleLines'] = st.selectbox("Несколько линий", ["No phone service", "No", "Yes"])
            with col2:
                input_data['InternetService'] = st.selectbox("Интернет", ["DSL", "Fiber optic", "No"])
                input_data['OnlineSecurity'] = st.selectbox("Онлайн-безопасность", ["No", "Yes", "No internet service"])
                input_data['OnlineBackup'] = st.selectbox("Облачное хранилище", ["No", "Yes", "No internet service"])
            with col3:
                input_data['DeviceProtection'] = st.selectbox("Защита устройств", ["No", "Yes", "No internet service"])
                input_data['TechSupport'] = st.selectbox("Техподдержка", ["No", "Yes", "No internet service"])
                input_data['StreamingTV'] = st.selectbox("Стриминговое ТВ", ["No", "Yes", "No internet service"])
                input_data['StreamingMovies'] = st.selectbox("Стриминговое кино", ["No", "Yes", "No internet service"])

        with tab3:
            col1, col2 = st.columns(2)
            with col1:
                input_data['Contract'] = st.selectbox("Тип контракта", ["Month-to-month", "One year", "Two year"])
                input_data['PaperlessBilling'] = st.selectbox("Электронный чек", ["Yes", "No"])
                input_data['PaymentMethod'] = st.selectbox("Способ оплаты", [
                    "Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"
                ])
            with col2:
                input_data['MonthlyCharges'] = st.number_input("Ежемесячный платеж", 0.0, 200.0, 50.0)
                input_data['TotalCharges'] = st.number_input("Общая сумма платежей", 0.0, 10000.0, 500.0)

        if st.button("Предсказать отток"):
            df_input = pd.DataFrame([input_data])
            
            for col, le in artifacts['encoders'].items():
                df_input[col] = le.transform(df_input[col])
                
            if artifacts.get('scaler') is not None:
                df_input[artifacts['num_cols']] = artifacts['scaler'].transform(df_input[artifacts['num_cols']])
            
            model = artifacts['model']
            prob = model.predict_proba(df_input)[0][1]
            pred = model.predict(df_input)[0]
            
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
                
            if prob > 0.5:
                st.warning("Внимание: Высокий риск потери клиента. Рекомендуется предложить скидку или бонус.")
            else:
                st.info("Клиент стабилен. Продолжайте текущую стратегию взаимодействия.")

def launch_app():
    """Функция для запуска приложения из внешних скриптов."""
    import subprocess
    import sys
    subprocess.run([sys.executable, "-m", "streamlit", "run", __file__])

if __name__ == "__main__":
    show_ui()
