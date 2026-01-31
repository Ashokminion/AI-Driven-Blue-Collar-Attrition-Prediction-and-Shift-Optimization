import joblib
import pandas as pd
import numpy as np
import os

class Model:
    def __init__(self, model_dir="src"):
        self.model_dir = model_dir
        self.load_artifacts()

    def load_artifacts(self):
        try:
            self.clf = joblib.load(os.path.join(self.model_dir, 'adv_model.pkl'))
            self.scaler = joblib.load(os.path.join(self.model_dir, 'adv_scaler.pkl'))
            self.encoders = joblib.load(os.path.join(self.model_dir, 'adv_encoders.pkl'))
            self.importance = joblib.load(os.path.join(self.model_dir, 'adv_importance.pkl'))
            self.feature_names = joblib.load(os.path.join(self.model_dir, 'adv_features.pkl'))
        except Exception as e:
            print(f"Error loading models: {e}")
            self.clf = None

    def predict_attrition(self, df):
        if self.clf is None: return None
        
        X = df.copy()
        # Drop only non-feature identification columns
        cols_to_drop = ['Employee_ID', 'Attrition', 'last_updated']
        X = X.drop([c for c in cols_to_drop if c in X.columns], axis=1)
        
        # Proper order
        X = X[self.feature_names]
        
        # Encode
        for col, le in self.encoders.items():
            X[col] = le.transform(X[col].astype(str))
            
        # Scale
        X_scaled = self.scaler.transform(X)
        
        # Predict
        probs = self.clf.predict_proba(X_scaled)[:, 1]
        
        results = pd.DataFrame({
            'Employee_ID': df['Employee_ID'],
            'Probability': probs,
            'Attrition_Risk': ["High" if p > 0.6 else "Medium" if p > 0.3 else "Low" for p in probs]
        })
        return results

    def get_importance_df(self):
        return self.importance
