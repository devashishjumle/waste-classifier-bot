import streamlit as st

# Waste Data
waste_data = {
    "plastic bottle": "Dry Waste",
    "banana peel": "Wet Waste",
    "vegetable": "Wet Waste",
    "newspaper": "Dry Waste",
    "battery": "Hazardous Waste",
    "glass": "Dry Waste",
    "food waste": "Wet Waste",
    "medicine": "Hazardous Waste"
}

def classify_waste(item):
    return waste_data.get(item.lower().strip(), None)

st.set_page_config(page_title="Waste Classifier Bot", page_icon="♻️")
st.title("♻️ Waste Classifier Chatbot")
st.write("Type a waste item to know whether it is **Dry, Wet, or Hazardous**.")

user_input = st.text_input("👉 Enter Waste Item:")

if user_input:
    category = classify_waste(user_input)
    if category:
        st.success(f"🗑️ Item: **{user_input.capitalize()}** \n\n🔎 Category: **{category}**")
    else:
        st.error("❌ Item not found in database! Please try another waste name.")
