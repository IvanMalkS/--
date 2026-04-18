import pandas as pd
import numpy as np
import os
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from imblearn.over_sampling import SMOTE

DATA_PATH = "data/WA_Fn-UseC_-Telco-Customer-Churn.csv"
MODEL_PATH = "models/churn_model.pkl"
ERROR_PLOT_PATH = "error_analysis.png"

def load_and_preprocess_data(file_path):
    print(f"Загрузка данных из {file_path}...")
    df = pd.read_csv(file_path)
    
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df.loc[df['tenure'] == 0, 'TotalCharges'] = 0
    df = df.dropna(subset=['TotalCharges'])
    
    if 'customerID' in df.columns:
        df = df.drop('customerID', axis=1)
        
    return df

def train_baseline(df):
    print("\n--- Baseline Model (Rule-based: Contract) ---")
    y_true = df['Churn'].apply(lambda x: 1 if x == 'Yes' else 0)
    y_pred = df['Contract'].apply(lambda x: 1 if x == 'Month-to-month' else 0)
    
    acc = accuracy_score(y_true, y_pred)
    print(f"Accuracy baseline модели: {acc:.4f}")
    return acc

def train_main_model(df):
    print("\n--- Основная модель: RandomForestClassifier с SMOTE ---")
    
    le_target = LabelEncoder()
    df['Churn'] = le_target.fit_transform(df['Churn'])
    
    cat_cols = df.select_dtypes(include=['object']).columns.tolist()
    encoders = {}
    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le
        
    X = df.drop('Churn', axis=1)
    y = df['Churn']
    
    all_cols = X.columns.tolist()
    num_cols = df.select_dtypes(exclude=['object']).columns.tolist()
    if 'Churn' in num_cols:
        num_cols.remove('Churn')
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print("Применение SMOTE...")
    smote = SMOTE(random_state=42, sampling_strategy=0.4) 
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
    
    rf = RandomForestClassifier(random_state=42)
    param_grid = {
        'n_estimators': [200, 500],
        'max_depth': [10, 15, None],
        'min_samples_split': [5, 10],
        'max_features': ['sqrt']
    }
    
    print("Запуск GridSearchCV...")
    grid_search = GridSearchCV(rf, param_grid, cv=5, scoring='accuracy', n_jobs=-1)
    grid_search.fit(X_train_res, y_train_res)
    
    best_model = grid_search.best_estimator_
    print(f"Лучшие параметры: {grid_search.best_params_}")
    
    y_pred = best_model.predict(X_test)
    final_acc = accuracy_score(y_test, y_pred)
    print(f"\nФИНАЛЬНАЯ ТОЧНОСТЬ (Accuracy) на тестовой выборке: {final_acc:.4f}")
    
    print("\nОтчет о классификации:")
    print(classification_report(y_test, y_pred))
    
    artifacts = {
        'model': best_model,
        'scaler': None,
        'encoders': encoders,
        'le_target': le_target,
        'num_cols': num_cols,
        'cat_cols': cat_cols,
        'all_cols': all_cols,
        'accuracy': final_acc
    }
    
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(artifacts, f)
    
    plt.figure(figsize=(10, 8))
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f'Confusion Matrix (Accuracy: {final_acc:.4f})')
    plt.savefig(ERROR_PLOT_PATH)

def check_existing_model(threshold=0.79):
    if os.path.exists(MODEL_PATH):
        try:
            with open(MODEL_PATH, 'rb') as f:
                artifacts = pickle.load(f)
            acc = artifacts.get('accuracy', 0)
            if acc >= threshold:
                print(f"Найдена существующая модель с точностью {acc:.4f} >= {threshold}. Пропуск обучения.")
                return True
            else:
                print(f"Существующая модель имеет низкую точность {acc:.4f} < {threshold}. Переобучение...")
        except Exception as e:
            print(f"Ошибка при загрузке модели: {e}. Переобучение...")
    return False

if __name__ == "__main__":
    force_train = os.environ.get("FORCE_TRAIN", "false").lower() == "true"
    
    if not force_train and check_existing_model():
        print("Готово.")
    elif os.path.exists(DATA_PATH):
        df = load_and_preprocess_data(DATA_PATH)
        train_baseline(df.copy())
        train_main_model(df)
    else:
        print(f"Файл {DATA_PATH} не найден!")
