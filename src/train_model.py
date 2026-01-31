import pandas as pd
import numpy as np
import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib

def train_models():
    # Load dataset
    data_path = r"c:\Users\ashok\OneDrive\Desktop\AI-Driven Blue-Collar Attrition Prediction and Shift Optimization\data\hr_attrition_data.csv"
    df = pd.read_csv(data_path)

    # Preprocessing
    le_gender = LabelEncoder()
    le_shift = LabelEncoder()
    
    df['Gender'] = le_gender.fit_transform(df['Gender'])
    df['Shift_Type'] = le_shift.fit_transform(df['Shift_Type'])
    df['Attrition'] = df['Attrition'].map({'Yes': 1, 'No': 0})

    X = df.drop(['Employee_ID', 'Attrition'], axis=1)
    y = df['Attrition']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Models to compare
    models = {
        'Logistic Regression': LogisticRegression(),
        'Decision Tree': DecisionTreeClassifier(max_depth=5),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42)
    }

    results = []
    best_model = None
    best_f1 = 0

    for name, model in models.items():
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        results.append({
            'Model': name,
            'Accuracy': acc,
            'Precision': prec,
            'Recall': rec,
            'F1-Score': f1
        })
        
        if f1 > best_f1:
            best_f1 = f1
            best_model = model

    # Display results
    results_df = pd.DataFrame(results)
    print("\nModel Comparison Results:")
    print(results_df)

    # Save best model and artifacts
    model_dir = r"c:\Users\ashok\OneDrive\Desktop\AI-Driven Blue-Collar Attrition Prediction and Shift Optimization\src"
    joblib.dump(best_model, os.path.join(model_dir, 'attrition_model.pkl'))
    joblib.dump(scaler, os.path.join(model_dir, 'scaler.pkl'))
    joblib.dump(le_gender, os.path.join(model_dir, 'le_gender.pkl'))
    joblib.dump(le_shift, os.path.join(model_dir, 'le_shift.pkl'))
    
    # Save the feature names for inference
    with open(os.path.join(model_dir, 'features.pkl'), 'wb') as f:
        pickle.dump(list(X.columns), f)

    print(f"\nBest model (F1-score: {best_f1:.2f}) saved successfully.")

if __name__ == "__main__":
    train_models()
