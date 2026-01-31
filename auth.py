import streamlit as st

class Auth:
    @staticmethod
    def init_session():
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user_role' not in st.session_state:
            st.session_state.user_role = None

    @staticmethod
    def login(role):
        st.session_state.authenticated = True
        st.session_state.user_role = role

    @staticmethod
    def logout():
        st.session_state.authenticated = False
        st.session_state.user_role = None
        st.rerun()

    @staticmethod
    def is_authenticated():
        return st.session_state.authenticated
