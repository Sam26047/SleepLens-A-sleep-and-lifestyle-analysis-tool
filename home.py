import streamlit as st
import base64

st.set_page_config(page_title="SleepLens", page_icon="💤", layout="centered")


def img_to_bytes(img_path):
    with open(img_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = img_to_bytes("Images/full5.jpg")   # Main app background
simg = img_to_bytes("Images/side.jpg")   # Sidebar background

custom_css = f"""
<style>
/* Main app background */
.stApp {{
    background-image: url("data:image/png;base64,{img}");
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center center;
    background-attachment: fixed;
}}

/* Sidebar background */
section[data-testid="stSidebar"] > div:first-child {{
    background-image: url("data:image/png;base64,{simg}");
    background-repeat: no-repeat;
    background-size: cover;
    background-position: center center;
    background-attachment: scroll;
    min-height: 100vh;
}}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)
st.title("SleepLens:")
st.subheader("💤 A tool to help you understand sleep & lifestyle Patterns")
st.markdown("""
<style>
.custom-header {
    color: white; /* Teal or bottle green */ 00695C
    font-size: 24px;
    font-weight: bold;
}
.sub{
        color: white; 
        font-weight:bold;
   }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="custom-header">Welcome to the Sleep & Lifestyle Data Dashboard! 💫</div><br>', unsafe_allow_html=True)

st.markdown('<div class="sub"> This project explores how factors such as <strong>occupation</strong>,<strong>student lifestyle habits</strong>, and <strong>sleep behavior</strong> affect sleep quality and health.<br><br>🔍 Navigate to the <strong>Analyze</strong> tab in the sidebar to explore the datasets with interactive visualizations.<hr><br>---</div>', unsafe_allow_html=True)


btn=st.button("Analyse")
if btn:
    st.switch_page("pages/Analyse.py") 
