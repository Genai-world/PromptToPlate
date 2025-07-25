import streamlit as st
import base64
from recipe_generator import get_recipe_mock, stream_recipe_from_gpt


def set_bg(image_file):
    with open(image_file, "rb") as img:
        b64_img = base64.b64encode(img.read()).decode()
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{b64_img}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Set background image
set_bg("background.png")
brown_css = """
<style>
/* All text brown and bold everywhere */
.stApp, .stApp * {
    color: #8B4513 !important;  /* Brown */
    font-weight: bold !important;
    font-style: normal !important;
}

/* Input, textarea, select, and button text also brown, bold */
input, textarea, select, button, .stButton > button, .stButton > button * {
    color: #8B4513 !important;
    font-weight: bold !important;
    font-style: normal !important;
}

/* Placeholder text also brown, maybe slightly lighter */
input::placeholder, textarea::placeholder {
    color: #A0522D !important;
    font-weight: bold !important;
    font-style: normal !important;
    opacity: 1 !important;
}

/* Button background stays white for visibility */
.stButton > button {
    background-color: white !important;
    border-radius: 12px !important;
    min-width: 180px;
    min-height: 48px;
    font-size: 20px !important;
    letter-spacing: 1px;
}

/* Button hover style */
.stButton > button:hover, .stButton > button:hover * {
    color: #5C3317 !important;
    background-color: #f5f5f5 !important;
    border: 2px solid #ff8800 !important;
}
</style>
"""
st.markdown(brown_css, unsafe_allow_html=True)


st.set_page_config(page_title="Prompt to Pate", layout="wide")
st.markdown(
    "<h1 style='color:#8B4513; font-weight:bold; margin-left: 100px;'>🍽️ Cook-o-Matic</h1>",
    unsafe_allow_html=True
)
# Create two columns for split view
left, right = st.columns(2)

# Left column
with left:
    st.subheader("Input Your Preferences")
    with st.form(key="recipe_form"):
        ingredients = st.text_area(
            "Enter ingredients (comma separated):",
            placeholder="e.g. eggs, spinach, cheese"
        )
        meal = st.selectbox("Which meal?", ["Breakfast", "Lunch", "Dinner"])
        cuisine = st.text_input("What kind of cuisine?", placeholder="e.g. Italian, Indian, Chinese")
        time = st.selectbox(
            "How much time should the dish take?",
            ["10-20 min", "20-30 min", "30-45 min", "1 hr"]
        )
        submit = st.form_submit_button("Get Recipe")

with right:
    st.subheader("A handpicked dish just for you:")
    if submit:
        recipe_box = st.empty()
        streamed_text = ""
        try:
            for token in stream_recipe_from_gpt(ingredients, meal, cuisine, time):
                streamed_text += token
                recipe_box.markdown(streamed_text)
            st.session_state['recipe'] = streamed_text
        except Exception as e:
            recipe = get_recipe_mock(ingredients, meal, cuisine, time)
            st.warning(f"Could not reach GPT, showing a sample. Error: {e}")
            st.session_state['recipe'] = recipe
            st.markdown(recipe)
    else:
        # Show previous recipe if available
        if 'recipe' in st.session_state:
            st.markdown(st.session_state['recipe'])
        else:
            st.info("Recipe will appear here after you click 'Get Recipe'.")