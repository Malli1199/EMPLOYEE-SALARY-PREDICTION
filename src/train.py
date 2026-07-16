import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def train_and_save_model():
    print("⏳ Starting model training pipeline...")
    
    # Check if dataset exists
    data_path = 'adult 3.csv'
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Missing dataset: {data_path}. Please ensure it's in the root directory.")

    # 1. Load Data
    data = pd.read_csv(data_path)

    # 2. Data Cleansing & Handling Imputation
    # Replace the '?' placeholder strings with standard NaNs
    data.replace({'?': np.nan}, inplace=True)
    data['occupation'] = data['occupation'].fillna('Others')
    data['workclass'] = data['workclass'].fillna('Notlisted')

    # Exclude minor/extreme outlier classes to prevent distortion
    data = data[~data['workclass'].isin(['Without-pay', 'Never-worked'])]
    data = data[(data['age'] <= 75) & (data['age'] >= 17)]

    # 3. Explicitly Isolate Feature Types
    categorical_features = ['workclass', 'education', 'marital-status', 'occupation', 'relationship', 'race', 'gender', 'native-country']
    numerical_features = ['age', 'capital-gain', 'capital-loss', 'hours-per-week']

    X = data[categorical_features + numerical_features]
    y = data['income']

    # Stratified Split to preserve exact target class distributions
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # 4. Construct Composited Preprocessing Transformers
    numerical_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    # 5. Build Unified End-to-End Execution Pipeline Blueprint
    # Gradient Boosting handles tabular profiling mixed data types extremely well
    best_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42))
    ])

    # Train the pipeline
    best_pipeline.fit(X_train, y_train)

    # 6. Evaluate Model Metrics
    y_pred = best_pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\n✅ Training Complete. Target Test Accuracy: {acc:.4f}")
    print("\n📋 Classification Metrics Summary:")
    print(classification_report(y_test, y_pred))

    # 7. Serialise and Save the entire pipeline architecture 
    joblib.dump(best_pipeline, 'best_model_pipeline.pkl')
    print("💾 Model and preprocessing transformers successfully saved to 'best_model_pipeline.pkl'!")

if __name__ == "__main__":
    train_and_save_model()