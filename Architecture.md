# System Architecture & Academic Documentation

## 1. Overall System Architecture
The application follows a **Modular Tiered Architecture**, ensuring high cohesion and low coupling. This structure is ideal for academic evaluation and maintenance.

- **Presentation Tier (`app.py`)**: Built with Streamlit to handle the UI, routing, and user interaction.
- **Logic Tier (`model.py`, `optimizer.py`, `auth.py`)**: Contains the Brain of the system—ML prediction logic, constraint-based optimization, and security protocols.
- **Data Tier (`database.py`)**: Manages data persistence using SQLite, ensuring records are stored even when the session ends.
- **Reporting Tier (`report_generator.py`)**: Generates professional PDF outputs for HR decision-makers.

## 2. Component Explanations (Exam-Friendly)

### 🔐 Authentication (`auth.py`)
- **Mechanism**: Implements Session State variables in Streamlit to track if a user has logged in.
- **Viva Reason**: Prevents unauthorized access to sensitive employee risk data. In a real-world scenario, data privacy is paramount.

### 🗄️ Database Integration (`database.py`)
- **Mechanism**: Uses SQLite to store structured tables for Users, Employees, and AI Predictions.
- **Viva Reason**: Traditional CSV-only systems lose data when the app closes. Persistence ensures the system can be used over multiple days with growing data.

### 🧠 Attrition Prediction (`model.py`)
- **Mechanism**: Uses a **Random Forest Classifier** trained on blue-collar features. It categorizes risk into Low, Medium, and High based on probability thresholds.
- **Viva Reason**: Random Forest is robust to noise and handles categorical data well, which is common in HR datasets.

### 📅 Shift Optimization (`optimizer.py`)
- **Mechanism**: A **Heuristic Constraint Optimizer**. It checks two primary conditions:
    1. **Constraint 1**: If Fatigue > 75 AND Shift == Night, rotate to Morning.
    2. **Constraint 2**: If Risk == High, cap overtime to prevent burnout.
- **Viva Reason**: Optimization adds "Prescriptive Analytics"—it doesn't just tell you what WILL happen, it tells you what to DO.

### 📄 PDF Export (`report_generator.py`)
- **Mechanism**: Uses the FPDF library to iterate through results and format them into a printable executive summary.
- **Viva Reason**: HR managers need a "Paper Trail" for board meetings or official audits. Digital-only dashboards are not always sufficient in manual industries.

---

## 3. Folder Structure
```text
/Project_Root
|-- app.py                # Main Entrance (UI)
|-- auth.py               # Login & Security Logic
|-- database.py           # SQL Persistence System
|-- model.py              # ML Prediction Interface
|-- optimizer.py          # Shift Recommendation Engine
|-- report_generator.py    # PDF Creation Module
|-- requirements.txt      # Dependency List
|-- data/
|   |-- shiftsync_v2.db   # The actual database file
|-- src/
|   |-- adv_model.pkl     # Pre-trained ML weights
|-- reports/
|   |-- Executive.pdf     # Generated PDF outputs
```

---

## 4. Viva Talking Points (Senior Engineer Style)
1. **"Why SQLite over CSV?"** 
   - *Answer*: "SQL provides ACID properties and allows for complex queries and multi-table relationships (Predictions linked to Employees) which CSV cannot handle efficiently."
2. **"How do you handle class imbalance in Attrition?"**
   - *Answer*: "I implemented **SMOTE** (Synthetic Minority Over-sampling Technique) in the training pipeline to ensure the model doesn't ignore the minority 'Attrition=Yes' class."
3. **"What is 'Explainable AI' in your project?"**
   - *Answer*: "We use Feature Importance scores. The system tells HR that 'Fatigue' or 'Wages' are the top reason for risk, rather than just giving a Black-Box prediction."
4. **"Is the system CPU-only?"**
   - *Answer*: "Yes, by utilizing Scikit-learn and Random Forest, we ensure professional performance without needing expensive GPUs, making it suitable for low-cost implementation."
