import streamlit as st
import requests

st.title("🗓️ AI Appointment Bot")
if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.text_input("You:", key="input")
if user_input:
    st.session_state.chat.append(("user", user_input))
    response = requests.post("http://localhost:8000/chat", json={"message": user_input})

    st.text(f"RAW RESPONSE: {response.text}")  # ← This will show what's coming back

    try:
        bot_reply = response.json().get("response")
    except Exception as e:
        st.error(f"Failed to parse response: {e}")
        bot_reply = "⚠️ Something went wrong on the server."
    
    st.session_state.chat.append(("bot", bot_reply))

for sender, msg in st.session_state.chat:
    if sender == "user":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**Bot:** {msg}")

