import pandas as pd
import numpy as np
import os

# Set seed for reproducibility
np.random.seed(42)

def generate_data(num_records=1000):
    data = {
        'Employee_ID': range(1001, 1001 + num_records),
        'Age': np.random.randint(18, 60, size=num_records),
        'Gender': np.random.choice(['Male', 'Female'], size=num_records, p=[0.7, 0.3]),
        'Shift_Type': np.random.choice(['Morning', 'Evening', 'Night'], size=num_records),
        'Daily_Wages': np.random.randint(400, 1200, size=num_records),
        'Overtime_Hours': np.random.randint(0, 20, size=num_records),
        'Distance_From_Home': np.random.randint(1, 50, size=num_records),
        'Work_Experience': np.random.randint(0, 40, size=num_records),
        'Attendance_Rate': np.random.uniform(70, 100, size=num_records),
        'Satisfaction_Score': np.random.randint(1, 6, size=num_records),
        'Physical_Fatigue_Level': np.random.randint(1, 6, size=num_records)
    }

    df = pd.DataFrame(data)

    # Logic to create realistic Attrition (Target Variable)
    # High risk if: High Night Shifts + High Overtime + Low satisfaction
    risk_score = (
        (df['Shift_Type'] == 'Night').astype(int) * 2 +
        (df['Overtime_Hours'] > 12).astype(int) * 3 +
        (5 - df['Satisfaction_Score']) * 1.5 +
        (df['Distance_From_Home'] > 30).astype(int) * 1 +
        (df['Attendance_Rate'] < 85).astype(int) * 2
    )

    # Threshold for Attrition
    df['Attrition'] = (risk_score > 8).map({True: 'Yes', False: 'No'})

    # Save to CSV
    output_dir = r"c:\Users\ashok\OneDrive\Desktop\AI-Driven Blue-Collar Attrition Prediction and Shift Optimization\data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    file_path = os.path.join(output_dir, "hr_attrition_data.csv")
    df.to_csv(file_path, index=False)
    print(f"Dataset generated with {num_records} records at {file_path}")

if __name__ == "__main__":
    generate_data()
