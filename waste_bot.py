import streamlit as st

# Waste Categories with keywords (India-specific common items)
waste_categories = {
    "Dry Waste": [
        "plastic bottle", "plastic bag", "newspaper", "magazine", "cardboard", "glass bottle", "metal can",
        "aluminium foil", "tin can", "paper", "carton", "thermocol", "rubber", "old clothes",
        "shoes", "toys", "packaging material", "polythene bag", "milk packet"
    ],
    "Wet Waste": [
        "banana peel", "fruit", "vegetable", "cooked food", "leftover rice", "tea leaves", "coffee grounds",
        "egg shell", "garden waste", "dry leaves", "green grass", "chapati", "flowers",
        "coconut shell", "onion peel", "potato peel", "fish waste", "meat waste"
    ],
    "Hazardous Waste": [
        "used battery", "expired medicine", "paint can", "chemical bottle", "syringe", "injection needle",
        "mask", "sanitizer bottle", "e-waste", "old mobile", "tube light", "cfl bulb", "mercury thermometer",
        "pesticide bottle", "nail polish", "blade", "razor"
    ]
}

# Flatten dictionary into a list
all_items = []
for category, items in waste_categories.items():
    for i in items:
        all_items.append(i)

# Classification function
def classify_waste(item):
    item = item.lower()
    for category, keywords in waste_categories.items():
        for word in keywords:
            if word in item:
                return category
    return None

# Streamlit UI
st.set_page_config(page_title="Waste Classifier Bot", page_icon="♻️")
st.title("♻️ Waste Classifier Chatbot (India)")
st.write("Select a waste item from dropdown OR type your own to know whether it is **Dry, Wet, or Hazardous Waste**.")

# Dropdown with search
dropdown_choice = st.selectbox("👉 Choose from list:", [""] + sorted(all_items))

# Manual input
manual_input = st.text_input("✍️ Or enter your own item:")

# Final user input (priority: manual > dropdown)
user_input = manual_input if manual_input.strip() != "" else dropdown_choice

if user_input:
    category = classify_waste(user_input)
    if category:
        st.success(f"🗑️ Item: **{user_input.capitalize()}** \n\n🔎 Category: **{category}**")
    else:
        st.error("❌ Item not found in database! Please try another waste name.")
