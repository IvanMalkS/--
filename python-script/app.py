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
    .st-emotion-cache-16idsys p {
        font-size: 1.05rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("Аналитическая Экспертная Система")
st.markdown("Пожалуйста, ответьте на вопросы ниже. Система логически вычислит и порекомендует оптимальную архитектуру для вашего фронтенд-проекта.")

st.divider()

with st.form("expert_form", border=True):
    st.subheader("Аудитория и География")
    col1, col2 = st.columns(2)
    with col1:
        region = st.radio("Где живут ваши пользователи?", ["В одной стране/регионе", "По всему миру"])
    with col2:
        env = st.radio("Как чаще заходят на сайт?", ["Из дома/офиса (надежный интернет)", "На бегу/в транспорте"])

    st.subheader("Устройства и Контент")
    col3, col4 = st.columns(2)
    with col3:
        device = st.radio("Основной тип устройств?", ["Мобильные телефоны", "Компьютеры / Ноутбуки"])
    with col4:
        content_heavy = st.radio("Много ли на сайте тяжелого контента (видео)?", ["Да, много", "Нет, в основном текст и картинки"])
        
    st.subheader("Функциональность")
    col5, col6 = st.columns(2)
    with col5:
        real_time = st.radio("Нужен ли живой чат или обновление цен?", ["Да", "Нет"])
    with col6:
        offline = st.radio("Должен ли сайт работать без интернета?", ["Да", "Нет"])

    st.subheader("Инфраструктура")
    col7, col8 = st.columns(2)
    with col7:
        budget = st.radio("Какой бюджет на сервера?", ["Большой (свои сервера)", "Маленький (облачный хостинг)"])
    with col8:
        traffic = st.radio("Ожидаются ли резкие скачки посетителей?", ["Да (Например, в Черную пятницу)", "Нет, трафик стабильный"])

    st.subheader("Дизайн")
    col9, col10 = st.columns(2)
    with col9:
        design = st.radio("Есть ли готовый UI-шаблон/дизайн?", ["Да, используем готовый", "Нет, рисуем всё с нуля"])
    with col10:
        anim = st.radio("Будут ли сложные 3D-эффекты?", ["Да", "Нет"])

    st.subheader("Команда и Ресурсы")
    col11, col12 = st.columns(2)
    with col11:
        team_size = st.radio("Каков размер вашей команды?", ["Большая (от 4 человек)", "Маленькая (1-3 человека)"])
    with col12:
        team_exp = st.radio("Есть ли в команде опытные Senior-разработчики?", ["Да", "Нет"])

    st.subheader("Бизнес-требования")
    col13, col14 = st.columns(2)
    with col13:
        seo = st.radio("Важно ли продвижение в поисковиках (SEO)?", ["Критично важно", "Не важно"])
    with col14:
        deadline = st.radio("Горят ли сроки?", ["Да, нужно быстрее сделать MVP", "Нет, есть время сделать качественно"])

    st.subheader("Мобильное приложение")
    is_mobile = st.radio("Планируется ли мобильное приложение?", ["Да", "Нет"])
    native_req = "Нет"
    if is_mobile == "Да":
        native_req = st.radio("Требуется ли доступ к железу (Камера, GPS, Пуши)?", ["Да", "Нет"])

    st.write("")
    submitted = st.form_submit_button("Рассчитать архитектуру", type="primary", use_container_width=True)


if submitted:
    def t(val, opt1): return '1' if val == opt1 else '2'
    
    answers = {
        'region': t(region, "В одной стране/регионе"),
        'env': t(env, "Из дома/офиса (надежный интернет)"),
        'device': t(device, "Мобильные телефоны"),
        'content_heavy': t(content_heavy, "Да, много"),
        'real_time': t(real_time, "Да"),
        'offline': t(offline, "Да"),
        'budget': t(budget, "Большой (свои сервера)"),
        'traffic': t(traffic, "Да (Например, в Черную пятницу)"),
        'design': t(design, "Да, используем готовый"),
        'anim': t(anim, "Да"),
        'team_size': t(team_size, "Большая (от 4 человек)"),
        'team_exp': t(team_exp, "Да"),
        'seo': t(seo, "Критично важно"),
        'deadline': t(deadline, "Да, нужно быстрее сделать MVP"),
        'is_mobile': t(is_mobile, "Да"),
        'native_req': t(native_req, "Да") if is_mobile == "Да" else "2"
    }

    st.divider()
    
    with st.spinner("Анализ данных алгоритмом Rete..."):
        engine = FrontendExpert()
        engine.reset()
        engine.declare(ProjectSpecs(**answers))
        engine.run()
        
    st.header("Результаты Анализа")
    
    if engine.recommendations:
        for idx, rec in enumerate(engine.recommendations):
            st.markdown(f"### Вариант {idx+1}: {rec['stack']}")
            st.markdown(f"**Обоснование Экспертной Системой:**")
            st.info(rec['reason'])
            st.write("") # Отступ
            
        if len(engine.recommendations) > 1:
            st.caption("Обратите внимание: система выявила несколько подходящих вариантов, так как в ваших требованиях присутствуют противоречащие факторы (например, могут одновременно требоваться легковесный UI и архитектура для мощной команды с большим стейтом).")
    else:
        st.error("Система не смогла подобрать однозначный стек под заданные требования. Попробуйте изменить некоторые параметры.")
