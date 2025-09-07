import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline

st.set_page_config(page_title="Waste Classifier Bot", page_icon="♻️", layout="centered")

st.title("♻️ Waste Classifier Bot (India)")
st.write("Type or select a waste item. Backend AI processes it silently.")

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

# ---------- Typeahead logic ----------
def get_suggestions(query, items):
    query = query.lower()
    return [item for item in items if query in item.lower()]

st.subheader("Type to see suggestions OR type your own:")

typed_text = st.text_input("Enter waste item:")

# Filter suggestions
suggestions = get_suggestions(typed_text, all_items) if typed_text else []

selected_item = None
if suggestions:
    selected_item = st.selectbox("Suggestions:", [""] + suggestions)
elif typed_text:
    selected_item = typed_text

if selected_item:
    # Backend AI processes silently
    _ = model.predict([selected_item])
    st.success(f"✅ You entered: `{selected_item}` (processed successfully)")
