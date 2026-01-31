import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
try:
    from imblearn.over_sampling import SMOTE
except ImportError:
    SMOTE = None

def train_advanced_model():
    data_path = r"c:\Users\ashok\OneDrive\Desktop\AI-Driven Blue-Collar Attrition Prediction and Shift Optimization\data\advanced_hr_data.csv"
    if not os.path.exists(data_path):
        print("Data not found. Running generation script first...")
        from src.advanced_data_gen import generate_advanced_data
        generate_advanced_data()
        
    df = pd.read_csv(data_path)
    
    # Encoders
    encoders = {}
    cat_cols = ['Gender', 'Department', 'Shift_Type', 'OT_Trend', 'Leave_Trend']
    
    for col in cat_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le
    
    df['Attrition'] = df['Attrition'].map({'Yes': 1, 'No': 0})
    
    X = df.drop(['Employee_ID', 'Attrition'], axis=1)
    y = df['Attrition']
    
    # Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # Scale
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Handle Class Imbalance with SMOTE
    if SMOTE:
        smote = SMOTE(random_state=42)
        X_train_res, y_train_res = smote.fit_resample(X_train_scaled, y_train)
        print("SMOTE applied to handle class imbalance.")
    else:
        X_train_res, y_train_res = X_train_scaled, y_train
        print("SMOTE not available. Using weighted training.")
    
    # Model: Balanced Random Forest
    model = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=42)
    model.fit(X_train_res, y_train_res)
    
    # Eval
    y_pred = model.predict(X_test_scaled)
    print("\nAdvanced Model Classification Report (Random Forest):")
    print(classification_report(y_test, y_pred))
    
    # Feature Importance (XAI)
    importances = pd.DataFrame({
        'Feature': X.columns,
        'Importance': model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    # Save Artifacts
    model_dir = r"c:\Users\ashok\OneDrive\Desktop\AI-Driven Blue-Collar Attrition Prediction and Shift Optimization\src"
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        
    joblib.dump(model, os.path.join(model_dir, 'adv_model.pkl'))
    joblib.dump(scaler, os.path.join(model_dir, 'adv_scaler.pkl'))
    joblib.dump(encoders, os.path.join(model_dir, 'adv_encoders.pkl'))
    joblib.dump(importances, os.path.join(model_dir, 'adv_importance.pkl'))
    joblib.dump(list(X.columns), os.path.join(model_dir, 'adv_features.pkl'))
    
    print(f"Advanced model artifacts saved in {model_dir}")

if __name__ == "__main__":
    train_advanced_model()
