import streamlit as st
import pandas as pd
import plotly.express as px
from auth import Auth
from database import Database
from model import Model
from optimizer import Optimizer
from report_generator import ReportGenerator

# --- INIT ---
db = Database()
ai = Model()
opt = Optimizer()
rep = ReportGenerator()
Auth.init_session()

# --- THEME & UI ---
st.set_page_config(page_title="ShiftSync AI | Enterprise", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="st-"] { font-family: 'Inter', sans-serif; }
    .main { background-color: #f8fafc; }
    .stMetric { background: white; padding: 15px; border-radius: 12px; border: 1px solid #eef2f6; }
    .login-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 50px; border-radius: 20px; color: white; text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- UTILITY ---
def standardize_columns(df):
    if df.empty: return df
    df.columns = [str(c).strip().lower().replace(' ', '_') for c in df.columns]
    mapping = {
        'employee_id': 'Employee_ID', 'age': 'Age', 'gender': 'Gender', 
        'department': 'Department', 'shift_type': 'Shift_Type', 
        'daily_wages': 'Daily_Wages', 'overtime_hours': 'Overtime_Hours', 
        'distance_km': 'Distance_km', 'years_of_service': 'Years_of_Service', 
        'last_month_leave': 'Last_Month_Leave', 'satisfaction': 'Satisfaction',
        'fatigue_score': 'Fatigue_Score', 'attrition': 'Attrition',
        'ot_trend': 'OT_Trend', 'leave_trend': 'Leave_Trend'
    }
    df = df.rename(columns={c: mapping[c] for c in df.columns if c in mapping})
    defaults = {
        'Employee_ID': 'Unknown', 'Age': 30, 'Gender': 'Male', 'Department': 'Production',
        'Shift_Type': 'Morning', 'Daily_Wages': 500, 'Overtime_Hours': 0, 'Distance_km': 5,
        'Years_of_Service': 1, 'Last_Month_Leave': 0, 'Satisfaction': 3,
        'OT_Trend': 'Stable', 'Leave_Trend': 'Stable'
    }
    for col, val in defaults.items():
        if col not in df.columns: df[col] = val
        else: df[col] = df[col].fillna(val)
    return df

def ensure_fatigue(df):
    df = standardize_columns(df)
    if df.empty: return df
    if 'Fatigue_Score' in df.columns: return df
    try:
        df['Fatigue_Score'] = df.apply(opt.calculate_fatigue, axis=1)
    except Exception as e:
        st.error(f"Fatigue calculation error: {e}")
    return df

# --- PAGES ---
def login_view():
    # ... (rest of function)
    st.write("## ")
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        st.markdown("""
            <div class="login-card">
                <h1>🛡️ ShiftSync AI</h1>
                <p style="color:#94a3b8;">Final Year Project | B.Tech AI & DS</p>
            </div>
        """, unsafe_allow_html=True)
        with st.form("Auth"):
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.form_submit_button("Access Portal"):
                role = db.verify_user(u, p)
                if role:
                    Auth.login(role)
                    st.success(f"Welcome, {role}")
                    st.rerun()
                else:
                    st.error("Access Denied.")

def dashboard_view():
    st.sidebar.title("🛡️ ShiftSync AI")
    st.sidebar.markdown(f"**Role:** {st.session_state.user_role}")
    st.sidebar.write("---")
    menu = st.sidebar.selectbox("Navigation", ["Overview", "Risk Analytics", "Optimization", "Data Management", "AI Expert Chat"])
    if st.sidebar.button("Logout"): Auth.logout()

    df = db.get_employees()
    df = ensure_fatigue(df)
    
    if menu == "Overview":
        st.title("Workforce Overview")
        if df.empty:
            st.warning("No data found. Please upload a CSV in Data Management.")
        else:
            m1, m2, m3 = st.columns(3)
            m1.metric("Strength", len(df))
            m2.metric("Avg Fatigue", f"{df['Fatigue_Score'].mean():.1f}")
            m3.metric("Critical Nodes", len(df[df['Fatigue_Score'] > 75]))
            
            st.divider()
            c1, c2 = st.columns(2)
            fig1 = px.histogram(df, x="Department", color="Shift_Type", barmode="group", title="Department Distribution")
            c1.plotly_chart(fig1, use_container_width=True)
            
            fig2 = px.scatter(df, x="Overtime_Hours", y="Fatigue_Score", color="Attrition", title="Overtime vs Fatigue")
            c2.plotly_chart(fig2, use_container_width=True)

    elif menu == "Risk Analytics":
        st.title("AI Attrition Risk Analytics")
        if not df.empty:
            if st.button("Run AI Risk Assessment"):
                preds = ai.predict_attrition(df)
                db.save_predictions(preds)
                st.success("Risk patterns identified.")
                
            # Load Predictions
            try:
                conn = db.get_connection()
                preds_db = pd.read_sql("SELECT * FROM predictions", conn)
                conn.close()
                
                c1, c2 = st.columns([1, 2])
                fig_risk = px.pie(preds_db, names="Attrition_Risk", color="Attrition_Risk", 
                                 color_discrete_map={"High":"#ef4444", "Medium":"#f59e0b", "Low":"#10b981"})
                c1.plotly_chart(fig_risk, use_container_width=True)
                
                c2.write("### Risk Registry")
                c2.dataframe(preds_db.sort_values('Probability', ascending=False), use_container_width=True)
            except:
                st.info("Run assessment to view results.")

    elif menu == "Optimization":
        st.title("Fatigue-Aware Roster Optimization")
        if not df.empty:
            try:
                conn = db.get_connection()
                preds_db = pd.read_sql("SELECT * FROM predictions", conn)
                conn.close()
                
                if st.button("Generate Optimized Roster"):
                    optimized_df = opt.run_optimization(df, preds_db)
                    st.write("### AI Recommended Shift Adjustments")
                    st.dataframe(optimized_df[optimized_df['Action'] != 'Maintained'], use_container_width=True)
                    
                    if st.button("Export Final PDF Report"):
                        path = rep.generate_pdf(df, preds_db, optimized_df)
                        with open(path, "rb") as f:
                            st.download_button("Download Official Report", f, "ShiftSync_Report.pdf")
            except:
                st.error("Please run Risk Assessment first.")

    elif menu == "Data Management":
        st.title("System Data Management")
        st.info("💡 Data is merged automatically. You can upload multiple files sequentially.")
        
        col_up1, col_up2 = st.columns([2, 1])
        with col_up1:
            up = st.file_uploader("Upload Employee Records (CSV - Max 1GB)", type="csv")
            if up:
                up_df = pd.read_csv(up)
                if st.button("Commit to Database (Merge)"):
                    with st.spinner("Merging data..."):
                        up_df = ensure_fatigue(up_df)
                        db.save_employees(up_df)
                        st.success(f"Added {len(up_df)} records!")
                        st.rerun()
        
        with col_up2:
            st.write("### Database Actions")
            if st.button("🗑️ Wipe All Records"):
                db.clear_employees()
                st.warning("All data cleared successfully.")
                st.rerun()
        
        st.divider()
        st.write("### Active Records")
        st.write(f"Total Rows: **{len(df)}**")
        st.dataframe(df.head(50), use_container_width=True)

    elif menu == "AI Expert Chat":
        st.title("🤖 ShiftSync AI Assistant")
        st.info("Ask me about ATTRITION, FATIGUE, ML MODELS, or VIVA TIPS!")
        from chatbot import render_chat_interface
        render_chat_interface(df)

# --- ROUTER ---
if not Auth.is_authenticated():
    login_view()
else:
    dashboard_view()
