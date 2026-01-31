import pandas as pd
import numpy as np

def advanced_optimize_shifts(df, risk_probs):
    """
    Optimizes based on Fatigue Score and Attrition Probability.
    """
    optimized = df.copy()
    optimized['Risk_Probability'] = risk_probs
    
    recommendations = []
    
    for i, row in optimized.iterrows():
        action = "Keep Current"
        new_shift = row['Shift_Type']
        new_ot = row['Overtime_Hours']
        
        # Rule 1: High Fatigue (>75) OR High Risk (>0.4)
        if row['Fatigue_Score'] > 75 or row['Risk_Probability'] > 0.4:
            if row['Shift_Type'] == 'Night':
                new_shift = 'Morning'
                action = "Rotate to Morning"
            
            if row['Overtime_Hours'] > 8:
                new_ot = 8
                action += " | Cap OT at 8h"
                
        # Rule 2: Moderate Fatigue (>60)
        elif row['Fatigue_Score'] > 60:
            if row['Overtime_Hours'] > 12:
                new_ot = 12
                action = "Cap OT at 12h"

        recommendations.append({
            'Employee_ID': row['Employee_ID'],
            'Department': row['Department'],
            'Fatigue': row['Fatigue_Score'],
            'Current_Shift': row['Shift_Type'],
            'Suggested_Shift': new_shift,
            'Original_OT': row['Overtime_Hours'],
            'Suggested_OT': new_ot,
            'Action': action
        })
        
    return pd.DataFrame(recommendations)

def run_what_if_analysis(df, model, scaler, encoders, wage_mod=0, ot_mod=0):
    """
    Simulates impact of modifying wages or OT on overall attrition risk.
    """
    sim_df = df.copy()
    
    # Apply modifications
    sim_df['Daily_Wages'] = (sim_df['Daily_Wages'] + wage_mod).clip(lower=450)
    sim_df['Overtime_Hours'] = (sim_df['Overtime_Hours'] + ot_mod).clip(lower=0, upper=40)
    
    # Preprocess
    X_sim = sim_df.drop(['Employee_ID', 'Attrition'], axis=1)
    
    for col, le in encoders.items():
        if col in X_sim.columns:
            X_sim[col] = le.transform(X_sim[col].astype(str))
            
    X_scaled = scaler.transform(X_sim)
    probs = model.predict_proba(X_scaled)[:, 1]
    
    return probs.mean(), (probs > 0.5).sum()
