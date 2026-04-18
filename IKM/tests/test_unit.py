import pytest
import pandas as pd
import numpy as np
import os
from unittest.mock import patch, MagicMock
from src.train import load_and_preprocess_data, train_baseline
from main import main

def test_load_and_preprocess_data(tmp_path):
    d = {
        'customerID': ['1', '2', '3'],
        'gender': ['Male', 'Female', 'Male'],
        'tenure': [1, 0, 5],
        'TotalCharges': ['10.5', ' ', '50.0'],
        'Churn': ['No', 'No', 'Yes']
    }
    df_dummy = pd.DataFrame(data=d)
    csv_file = tmp_path / "test_data.csv"
    df_dummy.to_csv(csv_file, index=False)
    
    processed_df = load_and_preprocess_data(str(csv_file))
    
    assert 'customerID' not in processed_df.columns
    assert pd.api.types.is_numeric_dtype(processed_df['TotalCharges'])
    assert processed_df.iloc[1]['TotalCharges'] == 0
    assert len(processed_df) == 3

def test_train_baseline():
    d = {
        'Churn': ['No', 'Yes', 'No', 'Yes'],
        'Contract': ['One year', 'Month-to-month', 'Two year', 'Month-to-month']
    }
    df = pd.DataFrame(d)
    acc = train_baseline(df)
    assert isinstance(acc, float)
    assert acc == 1.0 

@patch('main.load_and_preprocess_data')
@patch('main.train_main_model')
@patch('main.launch_app')
def test_main_orchestration(mock_launch, mock_train, mock_load):
    mock_load.return_value = pd.DataFrame({'dummy': [1]})
    
    main()
    
    mock_load.assert_called_once()
    mock_train.assert_called_once()
    mock_launch.assert_called_once()
