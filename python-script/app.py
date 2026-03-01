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
        q_region = st.radio("Где живут пользователи?", ["Один регион", "Весь мир"])
    with col2:
        q_env = st.radio("Откуда заходят?", ["Из офиса/Дома", "На бегу/Транспорт"])

    st.subheader("2. Устройства и Контент")
    col3, col4 = st.columns(2)
    with col3:
        q_dev = st.radio("Основное устройство?", ["ПК/Ноутбуки", "Телефоны"])
    with col4:
        q_content = st.radio("Тяжелый контент?", ["Текст", "Много видео"])
        
    st.subheader("3. Команда и Ресурсы")
    col5, col6 = st.columns(2)
    with col5:
        q_size = st.radio("Размер команды?", ["Много людей", "Мало людей"])
    with col6:
        q_exp = st.radio("Есть опытные профи?", ["Есть Senior", "Нет опытных"])

    st.subheader("4. Бизнес-требования")
    col7, col8 = st.columns(2)
    with col7:
        q_seo = st.radio("Нужно продвижение в поиске?", ["Да (Важно)", "Нет"])
    with col8:
        q_time = st.radio("Сроки горят?", ["Есть время", "Срочно"])

    st.subheader("5. Работа с данными (State)")
    col9, col10 = st.columns(2)
    with col9:
        q_real = st.radio("Нужен мгновенный чат?", ["Нет", "Да"])
    with col10:
        q_offline = st.radio("Нужна работа без интернета?", ["Нет", "Да"])

    st.subheader("6. Сервера и Нагрузка")
    col11, col12 = st.columns(2)
    with col11:
        q_host = st.radio("Бюджет на сервера?", ["Большой", "Ограниченный"])
    with col12:
        q_traffic = st.radio("Будут скачки посетителей?", ["Нет", "Да"])

    st.subheader("7. Дизайн UI")
    col13, col14 = st.columns(2)
    with col13:
        q_lib = st.radio("Есть готовый дизайн?", ["Да", "Нет"])
    with col14:
        q_anim = st.radio("Сложные 3D эффекты?", ["Нет", "Да"])

    st.subheader("8. Мобильность")
    q_store = st.radio("Нужна публикация в AppStore/GooglePlay?", ["Нет", "Да"])
    
    native_req = "Не нужен"
    if q_store == "Да":
        native_req = st.radio("Требуется ли доступ к телефону (Камера/Гео/Контакты)?", ["Не нужен", "Нужен"])

    st.write("")
    submitted = st.form_submit_button("Рассчитать архитектуру", type="primary", use_container_width=True)

if submitted:
    
    # Маппинг ответов в ключи экспертной системы
    answers = {
        'q_region': 'region' if q_region == "Один регион" else 'world',
        'q_env': 'office' if q_env == "Из офиса/Дома" else 'transport',
        'q_dev': 'pc' if q_dev == "ПК/Ноутбуки" else 'phone',
        'q_content': 'text' if q_content == "Текст" else 'video',
        
        'q_size': 'many' if q_size == "Много людей" else 'few',
        'q_exp': 'yes' if q_exp == "Есть Senior" else 'no',
        
        'q_seo': 'yes' if q_seo == "Да (Важно)" else 'no',
        'q_time': 'time' if q_time == "Есть время" else 'urgent',
        
        'q_real': 'yes' if q_real == "Да" else 'no',
        'q_offline': 'yes' if q_offline == "Да" else 'no',
        
        'q_host': 'much' if q_host == "Большой" else 'little',
        'q_traffic': 'yes' if q_traffic == "Да" else 'no',
        
        'q_lib': 'yes' if q_lib == "Да" else 'no',
        'q_anim': 'yes' if q_anim == "Да" else 'no',
        
        'q_store': 'yes' if q_store == "Да" else 'no',
        'native_req': 'yes' if native_req == "Нужен" else 'no',
    }

    st.divider()
    
    with st.spinner("Анализ данных..."):
        engine = FrontendExpert()
        engine.reset()
        engine.declare(ProjectSpecs(**answers))
        engine.run()
        
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
