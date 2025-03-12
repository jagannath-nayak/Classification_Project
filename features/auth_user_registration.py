import streamlit as st
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import os

# Define config file
CONFIG_FILE = "config.yaml"

# Ensure config file exists and is properly initialized
if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "w") as file:
        yaml.dump({"credentials": {"usernames": {}}}, file)

# Load config file safely
with open(CONFIG_FILE, "r", encoding="utf-8") as file:
    config = yaml.load(file, Loader=SafeLoader)

# Ensure `config` has the correct structure
if config is None:
    config = {"credentials": {"usernames": {}}}
elif "credentials" not in config:
    config["credentials"] = {"usernames": {}}
elif "usernames" not in config["credentials"]:
    config["credentials"]["usernames"] = {}

def show_register_form():
    with st.container():
        st.write("## Register")
        st.divider()
        new_username = st.text_input("Enter Username")
        new_name = st.text_input("Enter Your Full Name")
        new_password = st.text_input("Enter Password", type="password")
        new_email = st.text_input("Enter Your Email")

        if st.button("Submit Registration"):
            if new_username and new_password and new_email:
                # Ensure the config structure is correct
                if "credentials" not in config:
                    config["credentials"] = {}
                if "usernames" not in config["credentials"]:
                    config["credentials"]["usernames"] = {}

                # Check if username already exists
                if new_username in config["credentials"]["usernames"]:
                    st.error("Username already exists. Please choose a different one.")
                    return

                # Hash the password
                hashed_password = stauth.Hasher().hash(new_password)

                # Store user data
                config["credentials"]["usernames"][new_username] = {
                    "name": new_name,
                    "password": hashed_password,
                    "email": new_email,
                }

                # Save updated config to file
                with open(CONFIG_FILE, "w") as file:
                    yaml.dump(config, file)

                st.success("User registered successfully! You can now log in.")

    if st.button("Back to Login"):
        st.session_state["register"] = False
