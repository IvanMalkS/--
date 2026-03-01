import streamlit as st
from engine import FrontendExpert, ProjectSpecs

st.set_page_config(
    page_title="Аналитическая Экспертная Система - Фронтенд", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .stForm > div {
        padding: 1rem;
    }
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        color: #1E293B;
    }
</style>
""", unsafe_allow_html=True)

st.title("Аналитическая Экспертная Система")
st.markdown("Пожалуйста, ответьте на вопросы ниже. Система логически вычислит и порекомендует оптимальный стек и архитектуру для вашего фронтенд-проекта.")

st.divider()

with st.form("expert_form", border=True):
    st.subheader("1. Аудитория и География")
    col1, col2 = st.columns(2)
    with col1:
        q_region = st.radio("Регион пользователей", ["По всему миру", "В одном регионе/РФ"])
    with col2:
        q_env = st.radio("Среда использования", ["Из дома/офиса", "На бегу/в транспорте"])

    st.subheader("2. Устройства и Контент")
    col3, col4 = st.columns(2)
    with col3:
        q_dev = st.radio("Основной тип устройств", ["Компьютеры/Ноутбуки", "Мобильные телефоны"])
    with col4:
        q_content = st.radio("Тяжесть контента", ["В основном текст", "Много тяжелого (видео/фото)"])
        
    st.subheader("3. Команда и Ресурсы")
    col5, col6 = st.columns(2)
    with col5:
        q_size = st.radio("Размер команды", ["Маленькая (1-3 чел.)", "Большая (от 4 чел.)"])
    with col6:
        q_exp = st.radio("Опыт команды", ["Есть Senior", "Нет (Junior/Middle)"])
        
    q_ts = st.radio("Строгая типизация (TypeScript)", ["Да", "Нет"])

    st.subheader("4. Бизнес-требования")
    col7, col8 = st.columns(2)
    with col7:
        q_seo = st.radio("Требования к SEO", ["Да (Важно)", "Нет"])
    with col8:
        q_time = st.radio("Сроки горят?", ["Горят сроки (MVP)", "Есть время на качество"])

    st.subheader("5. Работа с данными (State)")
    col9, col10 = st.columns(2)
    with col9:
        q_real = st.radio("Обновление данных в реальном времени", ["Да (чат)", "Нет"])
    with col10:
        q_offline = st.radio("Оффлайн режим", ["Да", "Нет"])

    st.subheader("6. Сервера и Нагрузка")
    col11, col12 = st.columns(2)
    with col11:
        q_host = st.radio("Бюджет на сервера", ["Большой (свои сервера)", "Маленький (облако / serverless)"])
    with col12:
        q_traffic = st.radio("Будут ли резкие скачки посетителей?", ["Да", "Нет, стабильно"])

    st.subheader("7. Дизайн UI")
    col13, col14 = st.columns(2)
    with col13:
        q_lib = st.radio("Готовый дизайн", ["Да, готовый", "Нет, свой с нуля"])
    with col14:
        q_anim = st.radio("Анимации", ["Да", "Нет"])

    st.subheader("8. Мобильность")
    q_store = st.radio("Публикация в сторы (AppStore/GooglePlay)", ["Да", "Нет"])
    
    native_req = "Нет"
    if q_store == "Да":
        native_req = st.radio("Доступ к функциям телефона", ["Да", "Нет"])

    st.write("")
    submitted = st.form_submit_button("Рассчитать архитектуру", type="primary", use_container_width=True)

if submitted:
    
    # Маппинг ответов в ключи экспертной системы
    answers = {
        'q_region': 'world' if q_region == "По всему миру" else 'region',
        'q_env': 'office' if q_env == "Из дома/офиса" else 'transport',
        'q_dev': 'pc' if q_dev == "Компьютеры/Ноутбуки" else 'phone',
        'q_content': 'text' if q_content == "В основном текст" else 'video',
        
        'q_size': 'few' if q_size == "Маленькая (1-3 чел.)" else 'many',
        'q_exp': 'yes' if q_exp == "Есть Senior" else 'no',
        'q_ts': 'yes' if q_ts == "Да" else 'no',
        
        'q_seo': 'yes' if q_seo == "Да (Важно)" else 'no',
        'q_time': 'urgent' if q_time == "Горят сроки (MVP)" else 'time',
        
        'q_real': 'yes' if q_real == "Да (чат)" else 'no',
        'q_offline': 'yes' if q_offline == "Да" else 'no',
        
        'q_host': 'much' if q_host == "Большой (свои сервера)" else 'little',
        'q_traffic': 'yes' if q_traffic == "Да" else 'no',
        
        'q_lib': 'yes' if q_lib == "Да, готовый" else 'no',
        'q_anim': 'yes' if q_anim == "Да" else 'no',
        
        'q_store': 'yes' if q_store == "Да" else 'no',
        'native_req': 'yes' if native_req == "Да" else 'no',
    }

    st.divider()
    
    with st.spinner("Анализ данных..."):
        engine = FrontendExpert()
        engine.reset()
        engine.declare(ProjectSpecs(**answers))
        engine.run()
        engine.get_final_recommendation()
        
    st.header("Результаты Анализа")
    
    if engine.recommendations:
        for idx, rec in enumerate(engine.recommendations):
            st.markdown(f"### Вариант {idx+1}: {rec['stack']}")
            
            with st.expander("Посмотреть обоснование экспертной системы", expanded=True):
                st.info(rec['reason'])
            st.write("")
            
        if len(engine.recommendations) >= 1:
            st.caption("Обратите внимание: система выявила наиболее подходящие варианты, основываясь на графе принятия решений.")
            
        with st.expander("Журнал логических выводов (Logs)"):
            for log in engine.logs:
                st.write(f"- {log}")
    else:
        st.error("Система не смогла подобрать однозначный стек, так как не был активирован ни один из финальных узлов (вероятно, уникальное пересечение, не описанное в графе).")
