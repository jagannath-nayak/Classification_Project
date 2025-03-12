import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import os

# Define config file
CONFIG_FILE = "config.yaml"
if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "w") as file:
        yaml.dump({"credentials": {"usernames": {}}}, file)

# Load config file safely
with open(CONFIG_FILE, "r", encoding="utf-8") as file:
    config = yaml.load(file, Loader=SafeLoader)

# Ensure config structure
if config is None:
    config = {"credentials": {"usernames": {}}}
elif "credentials" not in config:
    config["credentials"] = {"usernames": {}}
elif "usernames" not in config["credentials"]:
    config["credentials"]["usernames"] = {}

# ✅ Fix: Ensure unique keys for authentication
def show_login_form():
    authenticator = stauth.Authenticate(
        config["credentials"],
        config.get("cookie", {}).get("name", "auth_cookie"),  # Unique Cookie Name
        config.get("cookie", {}).get("key", "random_key_123"),  # Unique Key
        config.get("cookie", {}).get("expiry_days", 30),
    )

    authenticator.login()
    
    if st.session_state["authentication_status"]:
        authenticator.logout("Logout", "sidebar")
        st.sidebar.write(f'Welcome **{st.session_state["name"]}** 👋')

    elif st.session_state["authentication_status"] is False:
        st.error("Username/password is incorrect")
    elif st.session_state["authentication_status"] is None:
        st.warning("Please enter your username and password")

    if not st.session_state["authentication_status"]:
        st.write("---")
        if st.button("Register"):
            st.session_state["register"] = True

def authentication():
    if st.session_state.get("register", False):
        from features.auth_user_registration import show_register_form
        show_register_form()
    else:
        show_login_form()
