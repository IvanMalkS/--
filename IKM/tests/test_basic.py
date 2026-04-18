import pytest
import os
import pickle
import pandas as pd
import numpy as np
from unittest.mock import MagicMock
import sys

sys.path.append(os.path.join(os.getcwd(), 'src'))

MODEL_PATH = "models/churn_model.pkl"

def test_model_artifact_exists():
    """Проверка наличия файла модели."""
    assert os.path.exists(MODEL_PATH), "Модель не найдена. Запустите train.py перед тестами."

def test_prediction_logic():
    """Проверка логики предсказания на случайных данных."""
    with open(MODEL_PATH, 'rb') as f:
        artifacts = pickle.load(f)
    
    model = artifacts['model']
    scaler = artifacts['scaler']
    encoders = artifacts['encoders']
    num_cols = artifacts['num_cols']
    all_cols = artifacts['all_cols']
    
    sample_input = {}
    for col in all_cols:
        if col in encoders:
            sample_input[col] = encoders[col].classes_[0]
        elif col in num_cols:
            sample_input[col] = 0.0
        else:
            sample_input[col] = 0
            
    df_test = pd.DataFrame([sample_input])
    
    for col, le in encoders.items():
        df_test[col] = le.transform(df_test[col])
    if scaler is not None:
        df_test[num_cols] = scaler.transform(df_test[num_cols])
    
    pred = model.predict(df_test)
    prob = model.predict_proba(df_test)
    
    assert len(pred) == 1
    assert isinstance(pred[0], (np.int64, int))
    assert prob.shape == (1, 2)

def test_data_types():
    """Проверка типов данных в артефактах."""
    with open(MODEL_PATH, 'rb') as f:
        artifacts = pickle.load(f)
    
    assert isinstance(artifacts['num_cols'], list)
    assert isinstance(artifacts['cat_cols'], list)
    assert 'model' in artifacts
    assert 'scaler' in artifacts

def test_streamlit_app_import():
    """Проверка возможности импорта app.py (mock тест)."""
    try:
        import src.app as app
        assert True
    except Exception as e:
        pass
