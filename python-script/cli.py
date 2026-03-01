import time
from engine import FrontendExpert, ProjectSpecs

def ask(question, option1, val1, option2, val2):
    print(f"\n{question}")
    print(f"1) {option1}")
    print(f"2) {option2}")
    while True:
        ans = input("Ваш выбор (1/2): ").strip()
        if ans == '1':
            return val1
        elif ans == '2':
            return val2
        print("Ошибка. Введите 1 или 2.")

def start_expert_system():
    print("=== АНАЛИТИЧЕСКАЯ ЭКСПЕРТНАЯ СИСТЕМА ===")
    print("Ответьте на вопросы, и система логически вычислит архитектуру.\n")
    
    answers = {}
    
    # 1. Аудитория и География
    answers['q_region'] = ask("Регион пользователей", "По всему миру", 'world', "В одном регионе/РФ", 'region')
    answers['q_env'] = ask("Среда использования", "Из дома/офиса", 'office', "На бегу/в транспорте", 'transport')

    # 2. Устройства и Контент
    answers['q_dev'] = ask("Основной тип устройств", "Компьютеры/Ноутбуки", 'pc', "Мобильные телефоны", 'phone')
    answers['q_content'] = ask("Тяжесть контента", "В основном текст", 'text', "Много тяжелого (видео/фото)", 'video')

    # 3. Команда и Ресурсы
    answers['q_size'] = ask("Размер команды", "Маленькая (1-3 чел.)", 'few', "Большая (от 4 чел.)", 'many')
    answers['q_exp'] = ask("Опыт команды", "Есть Senior", 'yes', "Нет (Junior/Middle)", 'no')
    answers['q_ts'] = ask("Строгая типизация (TypeScript)", "Да", 'yes', "Нет", 'no')

    # 4. Бизнес-требования
    answers['q_seo'] = ask("Требования к SEO", "Да (Важно)", 'yes', "Нет", 'no')
    answers['q_time'] = ask("Сроки горят?", "Горят сроки (MVP)", 'urgent', "Есть время на качество", 'time')

    # 5. Работа с данными (State)
    answers['q_real'] = ask("Обновление данных в реальном времени", "Да (чат)", 'yes', "Нет", 'no')
    answers['q_offline'] = ask("Оффлайн режим", "Да", 'yes', "Нет", 'no')

    # 6. Сервера и Нагрузка
    answers['q_host'] = ask("Бюджет на сервера", "Большой (свои сервера)", 'much', "Маленький (облако / serverless)", 'little')
    answers['q_traffic'] = ask("Будут ли резкие скачки посетителей?", "Да", 'yes', "Нет, стабильно", 'no')

    # 7. Дизайн UI
    answers['q_lib'] = ask("Готовый дизайн", "Да, готовый", 'yes', "Нет, свой с нуля", 'no')
    answers['q_anim'] = ask("Анимации", "Да", 'yes', "Нет", 'no')

    # 8. Мобильность
    answers['q_store'] = ask("Публикация в сторы (AppStore/GooglePlay)", "Да", 'yes', "Нет", 'no')
    if answers['q_store'] == 'yes':
        answers['native_req'] = ask("Доступ к функциям телефона", "Да", 'yes', "Нет", 'no')
    else:
        answers['native_req'] = 'no'

    print("\n" + "*"*50)
    print("ЗАПУСК ДВИЖКА ЛОГИЧЕСКОГО ВЫВОДА...")
    print("*"*50 + "\n")
    time.sleep(1)

    engine = FrontendExpert()
    engine.reset()
    engine.declare(ProjectSpecs(**answers))
    engine.run()
    engine.get_final_recommendation()
    
    if not engine.recommendations:
        print("\n[ ОШИБКА ] Система не смогла подобрать архитектуру по введенным параметрам (нет подходящего исхода).")

if __name__ == "__main__":
    start_expert_system()
