from src.train import load_and_preprocess_data, train_main_model
from src.app import launch_app

def main():
    """
    Основная функция для запуска пайплайна:
    1. Загрузка и предобработка данных
    2. Обучение модели
    3. Запуск веб-приложения
    """
    print("===== 1. Загрузка и предобработка данных =====")
    df = load_and_preprocess_data("data/WA_Fn-UseC_-Telco-Customer-Churn.csv")
    
    print("\n===== 2. Обучение модели =====")
    train_main_model(df)
    
    print("\n===== 3. Запуск веб-приложения =====")
    print("Откройте http://localhost:8501 в вашем браузере")
    launch_app()

if __name__ == "__main__":
    main()
