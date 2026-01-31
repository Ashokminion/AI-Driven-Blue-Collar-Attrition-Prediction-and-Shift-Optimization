import random

class ShiftSyncBot:
    def __init__(self):
        self.knowledge_base = {
            "what is fatigue score": "The Fatigue Score is a calculated metric (0-100) that considers Overtime Hours, Shift Type (Night shifts increase fatigue), Age, and Distance to work. High fatigue increases attrition risk.",
            "how to reduce attrition": "To reduce attrition, you can cap Overtime Hours at 8-12 hours, rotate high-risk employees from Night to Morning shifts, and increase workforce engagement for the Production department.",
            "what is random forest": "Random Forest is a 'Decision Tree' based Machine Learning algorithm. It's used here to predict the probability of an employee leaving based on historical patterns.",
            "what is smote": "SMOTE (Synthetic Minority Over-sampling Technique) is used to balance the dataset. In HR data, 'Attrition' is often a minority, so SMOTE creates synthetic samples to make the model training fair.",
            "how does optimization work": "The optimizer identifies employees with Fatigue Scores > 75 or Attrition Probabilities > 0.4 and recommends shift rotations or overtime caps to prevent burnout.",
            "viva help": "For your Viva: Focus on 'Feature Engineering' (Fatigue Score), 'Data Imbalance' (SMOTE), and 'Explainable AI' (Feature Importance charts). These are the most important technical aspects.",
            "who are you": "I am ShiftSync AI, your autonomous workforce intelligence assistant. I help you optimize blue-collar shift schedules and predict attrition risk."
        }

    def get_response(self, query, df=None):
        query = query.lower().strip()
        
        # 1. Functional Queries (Working with DF)
        if df is not None and not df.empty:
            if "attendance" in query or "many employees" in query or "total" in query:
                count = len(df)
                depts = df['Department'].nunique()
                return f"📋 **Workforce Status**: There are currently **{count}** employees registered in the system across **{depts}** departments."

            if "roster" in query or "plan" in query or "optimized" in query:
                high_fatigue = len(df[df['Fatigue_Score'] > 75])
                return f"📅 **Roster Summary**: I have processed the optimization. **{high_fatigue}** employees are flagged for fatigue-induced shift rotation. You can view the full detailed list in the **Optimization** tab."

            if "pdf" in query or "excel" in query or "convert" in query or "export" in query:
                return "📄 **Export Engine**: I've prepared the data for export. You can find the **'Download PDF Report'** button in the **Overview** or **Optimization** section to get the official document."

        # 2. Knowledge Base Queries
        for key in self.knowledge_base:
            if key in query:
                return self.knowledge_base[key]
        
        # Keyword-based heuristics
        if "fatigue" in query:
            return self.knowledge_base["what is fatigue score"]
        if "attrition" in query or "leave" in query:
            return self.knowledge_base["how to reduce attrition"]
        if "model" in query or "ai" in query or "algorithm" in query:
            return self.knowledge_base["what is random forest"]
        if "shift" in query or "optimize" in query:
            return self.knowledge_base["how does optimization work"]
        if "viva" in query or "exam" in query:
            return self.knowledge_base["viva help"]
            
        return "I'm not sure about that specific query. You can ask me about 'Attendance', 'Today's Roster', 'PDF Export', or 'Viva Preparation'!"

def render_chat_interface(df=None):
    import streamlit as st
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask ShiftSync AI assistant..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate bot response
        bot = ShiftSyncBot()
        response = bot.get_response(prompt, df)
        
        # Add bot message
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
