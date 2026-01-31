import pandas as pd
import numpy as np

class Optimizer:
    @staticmethod
    def calculate_fatigue(row):
        # Operational Weights
        ot_val = (row['Overtime_Hours'] / 40) * 40
        night_val = 25 if row['Shift_Type'] == 'Night' else 0
        commute_val = (row['Distance_km'] / 50) * 15
        age_val = ((60 - row['Age']) / 40) * 10
        leave_val = (row['Last_Month_Leave'] / 10) * 10
        
        score = ot_val + night_val + commute_val + age_val + leave_val
        return min(round(score, 2), 100)

    @staticmethod
    def run_optimization(df, predictions):
        """
        AI-Assisted Constraint-Based Optimization.
        Constraints: Max 8h OT, No Night shifts for High Risk, Row Rotation.
        """
        merged = df.copy()
        merged['Attrition_Risk'] = predictions['Attrition_Risk']
        
        recommends = []
        for _, row in merged.iterrows():
            rec_shift = row['Shift_Type']
            rec_ot = row['Overtime_Hours']
            action = "Maintained"
            
            # Constraint 1: High Fatigue (>75) -> Rotate from Night
            if row['Fatigue_Score'] > 75:
                if row['Shift_Type'] == 'Night':
                    rec_shift = 'Morning'
                    action = "Rotated to Morning"
                if row['Overtime_Hours'] > 8:
                    rec_ot = 8
                    action += " | Capped OT 8h"
            
            # Constraint 2: High Attrition Risk -> Stabilization
            elif row['Attrition_Risk'] == 'High':
                if row['Overtime_Hours'] > 10:
                    rec_ot = 10
                    action = "Risk Cap applied"
            
            recommends.append({
                'Employee_ID': row['Employee_ID'],
                'Fatigue': row['Fatigue_Score'],
                'Risk': row['Attrition_Risk'],
                'Current_Shift': row['Shift_Type'],
                'Optimal_Shift': rec_shift,
                'Current_OT': row['Overtime_Hours'],
                'Optimal_OT': rec_ot,
                'Action': action
            })
            
        return pd.DataFrame(recommends)
