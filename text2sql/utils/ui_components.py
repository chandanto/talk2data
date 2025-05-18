import streamlit as st
import base64
from pathlib import Path

def get_base64_image(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def display_logo():
    logo_path = Path("static/logo/TakePart_In_AI_logo.png")
    logo_base64 = get_base64_image(logo_path)

    st.markdown(
        f"""
        <div style="display: flex; flex-direction: column; align-items: flex-start;">
            <div style="display: flex; align-items: center;">
                <img src="data:image/png;base64,{logo_base64}" style="width: 150px; margin-right: 15px;" />
                <div>
                    <h1 style="margin: 0; font-size: 36px; font-weight: bold; color: #1F4E79;">Talk2Data</h1>
                    <p style="margin: 0; font-size: 16px; color: #6c757d; font-style: italic;">Explore. Learn. Build. TakePart In AI.</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def display_instructions():
    st.markdown("""
    ### 💬 How to Ask Questions

    Try questions like:
    - `What is the total sales for each products category with name?`
    - `What is the total sales for each products category in January 2020?`
    - `Show the amount spent by each customer?`
    - `Show total amount spent by each customers in the year 2020?`
    """)
