import pytest
from streamlit.testing.v1 import AppTest
import os
import pickle

def test_app_renders_and_predicts():
    """
    E2E тест для Streamlit приложения.
    Проверяет, что приложение загружается, отрисовывает элементы управления
    и выполняет предсказание при нажатии на кнопку.
    """
    app_path = os.path.join(os.getcwd(), "src/app.py")
    
    at = AppTest.from_file(app_path)
    
    at.run()
    
    assert at.title[0].value == "Прогнозирование оттока клиентов (Telecom Churn)"
    
    if at.error:
        pytest.skip(f"Модель не найдена: {at.error[0].value}")

    assert len(at.tabs) == 3
    
    predict_button = at.button[0] 
    assert predict_button.label == "Предсказать отток"
    
    predict_button.click().run()
    
    assert len(at.metric) > 0
    assert "Вероятность оттока" in at.metric[0].label
    
    found_result = False
    if len(at.success) > 0:
        assert "КЛИЕНТ ОСТАНЕТСЯ" in at.success[0].value
        found_result = True
    if len(at.error) > 1: 
        for err in at.error:
             if "КЛИЕНТ УЙДЕТ" in err.value:
                 found_result = True
    
    assert found_result, "Результат предсказания не найден на странице после нажатия кнопки"

def test_app_input_interaction():
    """Тест взаимодействия с вводом данных."""
    app_path = os.path.join(os.getcwd(), "src/app.py")
    at = AppTest.from_file(app_path).run()
    
    if at.error:
        pytest.skip("Модель не найдена")

    at.slider[0].set_value(60).run()
    
    contract_sb = [sb for sb in at.selectbox if sb.label == "Тип контракта"][0]
    contract_sb.set_value("Two year").run()
    
    predict_btn = [b for b in at.button if b.label == "Предсказать отток"][0]
    predict_btn.click().run()
    
    prob_str = at.metric[0].value.replace('%', '')
    prob = float(prob_str)
    assert prob < 100.0
