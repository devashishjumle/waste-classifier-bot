import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

st.set_page_config(page_title="Waste Classifier Bot", page_icon="♻️", layout="centered")

st.title("♻️ Waste Classifier Bot (India)")
st.write("Select from dropdown OR type your own waste item. AI predicts the category.")

# ---------- Seed dataset ----------
examples = {
    # Dry Waste
    "plastic bottle": "Dry Waste", "plastic bag": "Dry Waste", "newspaper": "Dry Waste",
    "magazine": "Dry Waste", "cardboard box": "Dry Waste", "glass bottle": "Dry Waste",
    "aluminium can": "Dry Waste", "paper": "Dry Waste", "tin can": "Dry Waste",
    "polythene": "Dry Waste", "thermocol": "Dry Waste", "old clothes": "Dry Waste",
    "shoe": "Dry Waste", "toy": "Dry Waste",

    # Wet Waste
    "banana peel": "Wet Waste", "fruit waste": "Wet Waste", "vegetable peels": "Wet Waste",
    "cooked food": "Wet Waste", "leftover rice": "Wet Waste", "tea leaves": "Wet Waste",
    "coffee grounds": "Wet Waste", "egg shell": "Wet Waste", "garden leaves": "Wet Waste",

    # Hazardous Waste
    "used battery": "Hazardous Waste", "expired medicine": "Hazardous Waste",
    "paint can": "Hazardous Waste", "chemical bottle": "Hazardous Waste",
    "syringe": "Hazardous Waste", "injection needle": "Hazardous Waste",
    "cfl bulb": "Hazardous Waste", "tube light": "Hazardous Waste"
}

all_items = sorted(list(examples.keys()))

# ---------- Train ML model ----------
@st.cache_resource(show_spinner=False)
def train_model(examples_dict):
    X = list(examples_dict.keys())
    y = list(examples_dict.values())
    pipeline = make_pipeline(
        TfidfVectorizer(ngram_range=(1,2), analyzer='word'),
        LogisticRegression(max_iter=1000)
    )
    pipeline.fit(X, y)
    return pipeline

model = train_model(examples)

# ---------- UI ----------
st.subheader("Select from dropdown OR type manually:")

# Dropdown
dropdown_choice = st.selectbox("Pick from list:", [""] + all_items)

# Manual input
manual_input = st.text_input("Or type here:")

# Final user input (manual > dropdown)
user_text = manual_input.strip() if manual_input.strip() != "" else dropdown_choice

if user_text:
    # AI prediction
    category = model.predict([user_text])[0]
    st.success(f"🗑️ Item: `{user_text}` \n🔎 Category: **{category}**")
