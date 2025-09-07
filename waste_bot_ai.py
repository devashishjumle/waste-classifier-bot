import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
import numpy as np

st.set_page_config(page_title="AI Waste Classifier", page_icon="♻️", layout="centered")

st.title("♻️ AI Waste Classifier (India) — Streamlit")
st.write("Type or choose a waste item. The AI model will predict whether it's **Dry**, **Wet** or **Hazardous**.")

# ---------- 1) Labelled dataset (text examples) ----------
# (Seed dataset — add more rows if you want stronger model)
examples = {
    # Dry
    "plastic bottle": "Dry Waste", "plastic bag": "Dry Waste", "newspaper": "Dry Waste",
    "magazine": "Dry Waste", "cardboard box": "Dry Waste", "glass bottle": "Dry Waste",
    "aluminium can": "Dry Waste", "paper": "Dry Waste", "tin can": "Dry Waste",
    "polythene": "Dry Waste", "thermocol": "Dry Waste", "old clothes": "Dry Waste",
    "shoe": "Dry Waste", "toy": "Dry Waste", "broken umbrella": "Dry Waste",
    "metal scrap": "Dry Waste", "packaging": "Dry Waste", "milk pouch": "Dry Waste",
    "chip packet": "Dry Waste", "plastic straw": "Dry Waste",

    # Wet
    "banana peel": "Wet Waste", "fruit waste": "Wet Waste", "vegetable peels": "Wet Waste",
    "cooked food": "Wet Waste", "leftover rice": "Wet Waste", "tea leaves": "Wet Waste",
    "coffee grounds": "Wet Waste", "egg shell": "Wet Waste", "garden leaves": "Wet Waste",
    "flower waste": "Wet Waste", "coconut husk": "Wet Waste", "onion peel": "Wet Waste",
    "potato peel": "Wet Waste", "meat scraps": "Wet Waste", "fish waste": "Wet Waste",
    "food scraps": "Wet Waste", "wet napkin": "Wet Waste", "bread": "Wet Waste",

    # Hazardous
    "used battery": "Hazardous Waste", "expired medicine": "Hazardous Waste",
    "paint can": "Hazardous Waste", "chemical bottle": "Hazardous Waste",
    "syringe": "Hazardous Waste", "injection needle": "Hazardous Waste",
    "cfl bulb": "Hazardous Waste", "tube light": "Hazardous Waste",
    "mercury thermometer": "Hazardous Waste", "pesticide bottle": "Hazardous Waste",
    "nail polish": "Hazardous Waste", "razor blade": "Hazardous Waste",
    "mobile battery": "Hazardous Waste", "e-waste": "Hazardous Waste",
    "dirty mask": "Hazardous Waste", "chemical waste": "Hazardous Waste"
}

# enlarge dataset a bit by adding keyword variants (helps coverage)
more_examples = {
    "plastic bottle cap": "Dry Waste", "plastic container": "Dry Waste", "glass jar": "Dry Waste",
    "cardboard": "Dry Waste", "paper bag": "Dry Waste", "aluminium foil": "Dry Waste",
    "banana skin": "Wet Waste", "fruit peels": "Wet Waste", "vegetable scraps": "Wet Waste",
    "leftover food plate": "Wet Waste", "used tissue": "Wet Waste",
    "battery acid": "Hazardous Waste", "old syringe": "Hazardous Waste", "paint bucket": "Hazardous Waste"
}
examples.update(more_examples)

# Flatten lists for selectbox
all_items = sorted(list(examples.keys()))

# ---------- 2) Train model on startup (small dataset -> fast) ----------
@st.cache_resource(show_spinner=False)
def train_model(examples_dict):
    X = list(examples_dict.keys())
    y = list(examples_dict.values())
    # pipeline tfidf + logistic regression
    pipe = make_pipeline(TfidfVectorizer(ngram_range=(1,2), analyzer='word'), LogisticRegression(max_iter=1000))
    pipe.fit(X, y)
    return pipe

model = train_model(examples)

# ---------- 3) Rule-based fallback (keywords) ----------
rule_keywords = {
    "Dry Waste": ["plastic", "paper", "cardboard", "glass", "metal", "aluminium", "tin", "polythene", "thermocol", "packaging", "pouch", "jar", "can"],
    "Wet Waste": ["banana", "vegetable", "fruit", "food", "leftover", "tea", "coffee", "egg", "garden", "leaf", "peel", "meat", "fish", "coconut"],
    "Hazardous Waste": ["battery", "medicine", "paint", "chemical", "syringe", "cfl", "tube light", "thermometer", "pesticide", "e-waste", "mobile", "razor", "blade"]
}

def rule_based(item):
    it = item.lower()
    for cat, kws in rule_keywords.items():
        for kw in kws:
            if kw in it:
                return cat
    return None

# ---------- 4) UI: Hybrid (dropdown + manual) ----------
st.subheader("Choose from list (search) OR type your own:")

dropdown_choice = st.selectbox("Pick item from suggestions:", [""] + all_items, index=0)
manual_input = st.text_input("Or type here (e.g. 'used tea leaves'):")

user_text = manual_input.strip() if manual_input.strip() != "" else dropdown_choice

if user_text:
    # model prediction + probabilities
    pred = model.predict([user_text])[0]
    probs = model.predict_proba([user_text])[0]
    classes = model.classes_
    # find confidence for predicted class
    pred_idx = list(classes).index(pred)
    confidence = probs[pred_idx]

    st.markdown("### 🔎 Result")
    st.write(f"**Item:** `{user_text}`")
    st.write(f"**AI Prediction:** **{pred}**  —  Confidence: **{confidence:.2f}**")

    # show top 3 probabilities
    top_idx = np.argsort(probs)[::-1][:3]
    probs_table = {classes[i]: float(probs[i]) for i in top_idx}
    st.write("**Top probabilities:**")
    for c,v in probs_table.items():
        st.write(f"- {c}: {v:.2f}")

    # If low confidence, show rule-based fallback suggestion
    if confidence < 0.6:
        rb = rule_based(user_text)
        if rb and rb != pred:
            st.warning(f"Low confidence. Rule-based suggestion: **{rb}**")
        elif not rb:
            st.info("Low confidence. No clear keyword found — consider selecting from suggestions or try a different wording.")
    else:
        st.success("Model confidence is good ✅")

    # Show explanation-ish info (nearest training examples)
    st.markdown("**Nearest training examples (helpful examples model saw):**")
    # compute cosine-like similarity via vectorizer transform
    try:
        vect = model.named_steps['tfidfvectorizer']
        lr = model.named_steps['logisticregression']
        x_user = vect.transform([user_text])
        # get training X transformed
        X_train_texts = list(examples.keys())
        X_train_vec = vect.transform(X_train_texts)
        # cosine similarity
        sims = (X_train_vec @ x_user.T).toarray().ravel()
        top_sim_idx = sims.argsort()[::-1][:5]
        for i in top_sim_idx:
            if sims[i] > 0:
                st.write(f"- `{X_train_texts[i]}`  (label: {examples[X_train_texts[i]]})  — similarity {sims[i]:.2f}")
    except Exception:
        pass

st.markdown("---")
st.caption("Model trained on a small seed dataset on app start. For better accuracy, expand labeled examples or integrate a larger training dataset / fine-tuned model.")
