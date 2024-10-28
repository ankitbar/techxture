import streamlit as st
from PIL import Image
import sqlite3

# Database setup
conn = sqlite3.connect('food_ratings.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''
CREATE TABLE IF NOT EXISTS ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    food_name TEXT,
    crispy INTEGER,
    creamy INTEGER,
    chewy INTEGER,
    crunchy INTEGER,
    soft INTEGER,
    slimy INTEGER,
    firm INTEGER,
    fluffy INTEGER
)
''')
conn.commit()

# Function to save ratings
def save_ratings(food_name, texture_ratings):
    c.execute('''
        INSERT INTO ratings (food_name, crispy, creamy, chewy, crunchy, soft, slimy, firm, fluffy)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (food_name, texture_ratings.get('Crispy', 0), texture_ratings.get('Creamy', 0),
          texture_ratings.get('Chewy', 0), texture_ratings.get('Crunchy', 0), texture_ratings.get('Soft', 0),
          texture_ratings.get('Slimy', 0), texture_ratings.get('Firm', 0), texture_ratings.get('Fluffy', 0)))
    conn.commit()

# App title
st.title("Food Texture Rating App")

# User input for food name
food_name = st.text_input("Enter the name of the food")

# File uploader
uploaded_file = st.file_uploader("Upload a food image", type=["jpg", "jpeg", "png"])

if uploaded_file and food_name:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Food Image', use_column_width=True)
    
    # Multi-select menu for texture options
    st.subheader("Rate the texture")
    texture_options = ["Crispy", "Creamy", "Chewy", "Crunchy", "Soft", "Slimy", "Firm", "Fluffy"]
    selected_textures = st.multiselect("Select textures present in the dish", texture_options)
    
    # Create sliders for each selected texture
    texture_ratings = {}
    for texture in selected_textures:
        rating = st.slider(f"Rate the presence of {texture} texture on a scale of 1 to 10", 1, 10, 5)
        texture_ratings[texture] = rating
    
    # Display selected textures and their ratings
    st.write("Your selected textures and their ratings:")
    for texture, rating in texture_ratings.items():
        st.write(f"{texture}: {rating}/10")

    # Save ratings to database
    if st.button("Submit"):
        save_ratings(food_name, texture_ratings)
        st.write("Thank you for your feedback! The ratings have been saved.")

    # Optional: Collect and store user feedback
    feedback = st.text_area("Additional feedback")
    if st.button("Submit Feedback"):
        st.write("Thank you for your feedback!")
