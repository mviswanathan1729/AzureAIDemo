import streamlit as st
import streamlit.components.v1 as components

key = st.secrets["Benefits_Chatbot_key"]

components.html(
  f"""
    <html>
    <head>
        <script src="https://cdn.botpress.cloud/webchat/v1/inject.js"></script>
        <script src="https://mediafiles.botpress.cloud/{key}/webchat/config.js" defer></script>
 </head>
 <body />
 </html>
      """, height=500
)