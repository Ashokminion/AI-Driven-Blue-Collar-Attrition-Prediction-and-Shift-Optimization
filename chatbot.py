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
            "who are you": "I am Minion, your autonomous workforce intelligence assistant. I help you optimize blue-collar shift schedules and predict attrition risk."
        }

    def get_response(self, query, df=None):
        query = query.lower().strip()
        
        # 1. Functional Queries (Working with DF)
        if df is not None and not df.empty:
            # Attendance & Headcount (with typos)
            if any(k in query for k in ["attendance", "toady", "today", "how many", "total", "count"]):
                count = len(df)
                depts = df['Department'].nunique()
                return f"📋 **Minion's Report**: Bello! There are currently **{count}** employees registered in the system across **{depts}** departments. Everything looks good for today!"

            # Roster & Optimization (with typos)
            if any(k in query for k in ["roster", "roaster", "plan", "optimized", "schedule", "shift"]):
                high_fatigue = len(df[df['Fatigue_Score'] > 75])
                return f"📅 **Minion's Roster Summary**: I've analyzed the roaster plan! **{high_fatigue}** employees are flagged for fatigue-induced shift rotation. You can see the full plan in the **Optimization** tab!"

            # Export & PDF (with typos)
            if any(k in query for k in ["pdf", "ecel", "excel", "convert", "export", "download", "print"]):
                return "📄 **Minion's Export Engine**: Poopaye! I can help with that. You can find the **'Download PDF Report'** button in the **Overview** or **Optimization** section. I'll convert everything for you!"

        # 2. Knowledge Base Queries
        for key in self.knowledge_base:
            if key in query:
                return self.knowledge_base[key]
        
        # Keyword-based heuristics for KB
        if "fatigue" in query: return self.knowledge_base["what is fatigue score"]
        if "attrition" in query or "leave" in query: return self.knowledge_base["how to reduce attrition"]
        if "model" in query or "ai" in query or "algorithm" in query: return self.knowledge_base["what is random forest"]
        if "viva" in query or "exam" in query: return self.knowledge_base["viva help"]
            
        return "Bello! I'm not sure about that specific query. You can ask me: 'Show today attendance', 'Give me roster plan', or 'Convert to PDF'. I'm here to help!"

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
