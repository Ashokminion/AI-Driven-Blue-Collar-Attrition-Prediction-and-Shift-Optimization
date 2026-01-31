import pandas as pd
import numpy as np
import os

def generate_advanced_data(n=1200):
    np.random.seed(123)
    
    data = {
        'Employee_ID': [f'EMP_{i:04d}' for i in range(1, n+1)],
        'Age': np.random.randint(19, 58, n),
        'Gender': np.random.choice(['Male', 'Female'], n, p=[0.75, 0.25]),
        'Department': np.random.choice(['Production', 'Logistics', 'Quality', 'Maintenance'], n),
        'Shift_Type': np.random.choice(['Morning', 'Evening', 'Night'], n),
        'Daily_Wages': np.random.randint(450, 1500, n),
        'Overtime_Hours': np.random.randint(0, 25, n),
        'Distance_km': np.random.randint(1, 45, n),
        'Years_of_Service': np.random.randint(0, 20, n),
        'Last_Month_Leave': np.random.randint(0, 8, n),
        'Satisfaction': np.random.randint(1, 6, n),
    }
    
    df = pd.DataFrame(data)
    
    # Derived Feature: Fatigue Score (1-100)
    # Weight: 0.4*OT + 0.2*NightShift + 0.1*Commute + 0.1*(60-Age) + 0.2*Leaves
    night_weight = (df['Shift_Type'] == 'Night').astype(int) * 20
    df['Fatigue_Score'] = (
        (df['Overtime_Hours'] / 25 * 40) + 
        night_weight + 
        (df['Distance_km'] / 45 * 10) + 
        ((60 - df['Age']) / 40 * 10) + 
        (df['Last_Month_Leave'] / 8 * 20)
    ).clip(1, 100).round(2)
    
    # New Actionable Features
    df['OT_Trend'] = np.random.choice(['Rising', 'Stable', 'Falling'], n, p=[0.3, 0.5, 0.2])
    df['Leave_Trend'] = np.random.choice(['Rising', 'Stable', 'Falling'], n, p=[0.2, 0.6, 0.2])
    
    # Target Logic: Attrition (highly imbalanced ~15%)
    # Risk Factor Calculation
    risk = (
        (df['Fatigue_Score'] > 75).astype(int) * 4 +
        (df['Satisfaction'] < 3).astype(int) * 3 +
        (df['OT_Trend'] == 'Rising').astype(int) * 2 +
        (df['Daily_Wages'] < 600).astype(int) * 2 +
        (df['Years_of_Service'] < 2).astype(int) * 1
    )
    
    # 0.15 probability of churn if risk > 5
    df['Attrition'] = (risk > 6).map({True: 'Yes', False: 'No'})
    
    output_path = r"c:\Users\ashok\OneDrive\Desktop\AI-Driven Blue-Collar Attrition Prediction and Shift Optimization\data\advanced_hr_data.csv"
    df.to_csv(output_path, index=False)
    print(f"Advanced dataset generated: {output_path}")

if __name__ == "__main__":
    generate_advanced_data()
