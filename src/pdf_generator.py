from fpdf import FPDF
import pandas as pd
import os

class PDFGenerator(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'ShiftSync AI - Workforce Intelligence Report', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def create_report(self, df, metrics, output_path="docs/ShiftSync_Report.pdf"):
        self.add_page()
        
        # Summary Section
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Executive Summary', 0, 1)
        self.set_font('Arial', '', 10)
        for key, val in metrics.items():
            self.cell(0, 8, f'{key}: {val}', 0, 1)
        self.ln(10)

        # Risk Table
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'High-Risk Employee Segments', 0, 1)
        self.set_font('Arial', 'B', 10)
        self.cell(40, 10, 'Employee ID', 1)
        self.cell(60, 10, 'Department', 1)
        self.cell(40, 10, 'Fatigue Score', 1)
        self.cell(40, 10, 'Shift', 1)
        self.ln()

        self.set_font('Arial', '', 10)
        high_risk = df[df['Fatigue_Score'] > 75].head(10)
        for _, row in high_risk.iterrows():
            self.cell(40, 8, str(row['Employee_ID']), 1)
            self.cell(60, 8, str(row['Department']), 1)
            self.cell(40, 8, str(row['Fatigue_Score']), 1)
            self.cell(40, 8, str(row['Shift_Type']), 1)
            self.ln()

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        self.output(output_path)
        return output_path
