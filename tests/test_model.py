import pytest
import pandas as pd
import numpy as np
import joblib

def test_model_pipeline_loading():
    """Ensure the exported pipeline loads and evaluates data types correctly."""
    try:
        model = joblib.load('best_model_pipeline.pkl')
        assert model is not None
    except FileNotFoundError:
        pytest.fail("Model pipeline file missing.")

def test_prediction_output_format():
    """Verify inference output format matches specifications."""
    model = joblib.load('best_model_pipeline.pkl')
    # Mocking sample evaluation payload data 
    mock_data = pd.DataFrame([{
        'age': 35, 'workclass': 'Private', 'education': 'Bachelors',
        'marital-status': 'Never-married', 'occupation': 'Tech-support',
        'relationship': 'Not-in-family', 'race': 'White', 'gender': 'Male',
        'capital-gain': 0, 'capital-loss': 0, 'hours-per-week': 40, 'native-country': 'United-States'
    }])
    prediction = model.predict(mock_data)
    assert len(prediction) == 1
    assert prediction[0] in ['<=50K', '>50K', 0, 1]