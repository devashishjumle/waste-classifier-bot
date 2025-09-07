import streamlit as st

# Waste Categories with keywords (India-specific common items)
waste_categories = {
    "Dry Waste": [
        "plastic", "bottle", "newspaper", "magazine", "cardboard", "glass", "metal",
        "aluminium", "tin", "paper", "carton", "thermocol", "rubber", "old clothes",
        "shoes", "toys", "packaging", "polythene", "milk packet"
    ],
    "Wet Waste": [
        "banana", "fruit", "vegetable", "food", "leftover", "tea", "coffee", "egg",
        "garden", "leaves", "grass", "cooked rice", "bread", "chapati", "flowers",
        "coconut", "onion peel", "potato peel", "fish", "meat"
    ],
    "Hazardous Waste": [
        "battery", "medicine", "paint", "chemical", "syringe", "injection", "mask",
        "sanitizer", "e-waste", "mobile", "tube light", "cfl", "thermometer",
        "pesticide", "nail polish", "blade", "razor"
    ]
}

# Classification function
def classify_waste(item):
    item = item.lower()
    for category, keywords in waste_categories.items():
        for word in keywords:
            if word in item:
                return category
    return None

# Streamlit App UI
st.set_page_config(page_title="Waste Classifier Bot", page_icon="♻️")
st.title("♻️ Waste Classifier Chatbot (India)")
st.write("Enter a waste item to know whether it is **Dry, Wet, or Hazardous Waste** as per Indian guidelines.")

user_input = st.text_input("👉 Enter Waste Item:")

if user_input:
    category = classify_waste(user_input)
    if category:
        st.success(f"🗑️ Item: **{user_input.capitalize()}** \n\n🔎 Category: **{category}**")
    else:
        st.error("❌ Item not found in database! Please try another waste name.")
