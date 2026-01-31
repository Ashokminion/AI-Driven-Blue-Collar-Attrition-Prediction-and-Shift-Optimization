import random

class MinionVibeBot:
    def __init__(self):
        # The ultimate humble, lovable, multilingual vibe persona
        self.greetings = {
            "english": ["Hello friend! How can I help you vibes today? ✨", "Bello! Minion here to make your day better! 💛"],
            "tamil": ["Vanakkam nanba! Enna help venum? Sollunga! 😊", "Bello! Ella work-um super-ah nadakkum, don't worry! ✨"],
            "tanglish": ["Dei buddy! What's the vibe today? Enna solve pannalam? 🔥", "Don't tension, Minion is here! Work-ah chill-ah mudikalam! 🚀"],
            "hindi": ["Namaste dost! Aaj kya dhamaka karna hai? 🌟", "Main hoon na! Tension mat lo, sab theek ho jayega! ✨"],
            "malayalam": ["Namaskaram koottukara! Enthoke undu vishesham? 😊", "Ningale sahayikkan Minion koodeundu! Vibe aakkalam! 🌈"],
            "kannada": ["Namaskara geleya! Naanu yaavaga sahaya madali? ✨", "Tension beda kanda! Minion ideene, ella sari hogutte! 🌟"]
        }
        
        self.humble_responses = [
            "I'm just a small Minion trying to make your workforce smarter! 💛",
            "You are the real boss! I'm just here to give you the data vibe! ✨",
            "Learning every day from a legend like you! How can I help? 😊",
            "Always happy to serve! Your project is going to be the best! 🚀"
        ]

        self.knowledge_base = {
            "what is fatigue score": "The Fatigue Score is a calculated metric (0-100) that considers Overtime Hours, Shift Type (Night shifts increase fatigue), Age, and Distance to work. It's like a 'tiredness meter' for our team! 📉",
            "how to reduce attrition": "To keep the vibe high and attrition low: Cap OT at 8 hours, rotate shifts, and give some appreciation to the Production team! Happy workers = No attrition! 🌈",
            "what is random forest": "Random Forest is like a team of Minions making decisions! It's an ML model that predicts if someone might leave by looking at patterns. Very powerful! 🧠",
            "what is smote": "SMOTE is a balancing act! It creates synthetic data for the minority class so our AI is fair to everyone. No bias, only vibes! ⚖️",
            "viva help": "Don't panic for Viva! Focus on: Feature Engineering (Fatigue), Class Imbalance (SMOTE), and Explainable AI. You will rock it! 🔥",
            "who are you": "I am Minion 2.0 (Vibe Edition)! Your humble, multilingual, and super-smart AI assistant. I'm like a mini ChatGPT for your project! 💛"
        }

    def detect_language(self, query):
        q = query.lower()
        if any(w in q for w in ["vanakkam", "enna", "sollunga", "nanba"]): return "tamil"
        if any(w in q for w in ["dei", "chill", "buddy", "pannalam", "vibe"]): return "tanglish"
        if any(w in q for w in ["namaste", "dost", "kya", "theek", "mat lo"]): return "hindi"
        if any(w in q for w in ["namaskaram", "enthoke", "koodeundu"]): return "malayalam"
        if any(w in q for w in ["namaskara", "geleya", "beda", "hogutte"]): return "kannada"
        return "english"

    def get_response(self, query, df=None):
        query = query.lower().strip()
        lang = self.detect_language(query)
        greet = random.choice(self.greetings[lang])
        humble = random.choice(self.humble_responses)
        
        # 1. Functional Queries (Working with DF)
        if df is not None and not df.empty:
            if any(k in query for k in ["attendance", "toady", "today", "many", "total", "count"]):
                count = len(df)
                return f"{greet}\n\n📋 **Minion's Live Report**: We have **{count}** hardworking people today! Such a great vibe! {humble}"

            if any(k in query for k in ["roster", "roaster", "plan", "optimized", "schedule"]):
                high_fatigue = len(df[df['Fatigue_Score'] > 75])
                return f"{greet}\n\n📅 **Minion's Roster Plan**: Optimized and ready! Found **{high_fatigue}** team members who need a break. Check the Optimization tab, boss! {humble}"

            if any(k in query for k in ["pdf", "ecel", "excel", "convert", "export", "download"]):
                return f"{greet}\n\n📄 **Minion's Export Engine**: Poopaye! I'm preparing the PDF/Excel vibes for you. Just click the download button in the Overview tab! {humble}"

        # 2. Knowledge Base Queries
        for key in self.knowledge_base:
            if key in query:
                return f"{greet}\n\n{self.knowledge_base[key]}\n\n{humble}"
        
        # 3. Handle Greetings/Vibe directly
        if any(k in query for k in ["hi", "hello", "bello", "yo", "hey", "super", "thanks", "vibe"]):
            return f"{greet}\n\nI'm ready to help you with anything! {humble}"
            
        return f"{greet}\n\nI'm still learning, but I can check your results, explain the ML models, or help with Viva tips! Just ask me comfortably. {humble}"

def render_chat_interface(df=None):
    import streamlit as st
    
    # Custom CSS for a "Lovable Vibe" Chat
    st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 20px;
        padding: 10px;
        margin-bottom: 10px;
        border: 1px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask Minion (Vibe AI) anything..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        bot = MinionVibeBot()
        response = bot.get_response(prompt, df)
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)
