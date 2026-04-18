# Telecom Churn Prediction Project

Проект по дисциплине «Интеллектуальные системы» для прогнозирования оттока клиентов в телекоммуникационной компании.

## Структура проекта
- `data/` — исходные данные (`WA_Fn-UseC_-Telco-Customer-Churn.csv`).
- `models/` — сохраненные артефакты модели (`.pkl`).
- `src/` — исходный код:
  - `train.py` — скрипт обучения модели.
  - `app.py` — интерфейс на Streamlit.
- `tests/` — модульные тесты.
- `pyproject.toml` — управление зависимостями через `uv`.

## Установка и запуск

Для работы с проектом рекомендуется использовать [uv](https://github.com/astral-sh/uv).

### 1. Подготовка окружения
Если у вас еще не установлен `uv`:
```bash
pip install uv
```

Синхронизация зависимостей:
```bash
uv sync
```

### 2. Обучение модели
Запустите скрипт для предобработки данных и обучения RandomForest:
```bash
uv run src/train.py
```
После выполнения в консоли появится отчет, а в корне проекта сохранится файл `error_analysis.png`. Модель сохранится в `models/churn_model.pkl`.

### 3. Запуск веб-интерфейса
Запустите Streamlit приложение:
```bash
uv run streamlit run src/app.py
```

### 4. Запуск тестов
```bash
uv run pytest tests/test_basic.py
```

## Используемые технологии
- **Python 3.12+**
- **uv** (Dependency management)
- **Scikit-learn** (ML Model & Preprocessing)
- **Pandas/Numpy** (Data handling)
- **Streamlit** (UI)
- **Matplotlib/Seaborn** (Visualization)
- **Pytest** (Testing)
