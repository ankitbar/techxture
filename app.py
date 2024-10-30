import streamlit as st
from PIL import Image
import sqlite3
import pandas as pd

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
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (food_name, texture_ratings.get('Crispy', 0), texture_ratings.get('Creamy', 0),
          texture_ratings.get('Chewy', 0), texture_ratings.get('Crunchy', 0), texture_ratings.get('Soft', 0),
          texture_ratings.get('Slimy', 0), texture_ratings.get('Firm', 0), texture_ratings.get('Fluffy', 0)))
    conn.commit()

# Function to search for food and calculate average ratings
def search_food(food_name: str):
    df = pd.read_sql_query(f"SELECT * FROM ratings WHERE food_name='{food_name}'", conn)
    if df.empty:
        return None
    avg_ratings = df.mean(numeric_only=True).to_dict()
    return avg_ratings

# Clear function
def clear_inputs():
    for key in st.session_state.keys():
        del st.session_state[key]

# Ensure keys are initialized
if 'search_food_name' not in st.session_state:
    st.session_state['search_food_name'] = ''
if 'food_name' not in st.session_state:
    st.session_state['food_name'] = ''
if 'uploaded_file' not in st.session_state:
    st.session_state['uploaded_file'] = None
if 'selected_textures' not in st.session_state:
    st.session_state['selected_textures'] = []
if 'food_found' not in st.session_state:
    st.session_state['food_found'] = True

# App title
st.title("Food Texture Rating App")

# Search box
search_food_name = st.text_input("Search for a food", key='search_food_name')

if search_food_name:
    avg_ratings = search_food(search_food_name)
    if avg_ratings:
        st.subheader(f"Average ratings for {search_food_name}")
        for texture, rating in avg_ratings.items():
            if texture != 'id' and rating > 0:
                st.write(f"{texture.capitalize()}: {rating:.1f}")

        # Ask if the user wants to add their own review
        add_review = st.checkbox("Add your own review")
        
        if add_review:
            # File uploader
            uploaded_file = st.file_uploader("Upload a food image", type=["jpg", "jpeg", "png"], key='uploaded_file')
            
            if uploaded_file:
                # Display the uploaded image
                image = Image.open(uploaded_file)
                st.image(image, caption='Uploaded Food Image', use_column_width=True)
                
                # Multi-select menu for texture options
                st.subheader("Rate the texture")
                texture_options = ["Crispy", "Creamy", "Chewy", "Crunchy", "Soft", "Slimy", "Firm", "Fluffy"]
                selected_textures = st.multiselect("Select textures present in the dish", texture_options, key='selected_textures')
                
                # Create sliders for each selected texture
                texture_ratings = {}
                for texture in selected_textures:
                    rating = st.slider(f"Rate the presence of {texture} texture on a scale of 1 to 10", 1, 10, 5, key=f"slider_{texture}")
                    texture_ratings[texture] = rating
                
                # Display selected textures and their ratings
                st.write("Your selected textures and their ratings:")
                for texture, rating in texture_ratings.items():
                    st.write(f"{texture}: {rating}/10")

                # Save ratings to database
                if st.button("Submit"):
                    save_ratings(search_food_name, texture_ratings)
                    st.write("Thank you for your feedback! The ratings have been saved.")
                    clear_inputs()
                
    else:
        st.write("No ratings found for this food. You can be the first to review!")
        
        # File uploader
        uploaded_file = st.file_uploader("Upload a food image", type=["jpg", "jpeg", "png"], key='uploaded_file')
        
        if uploaded_file:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Food Image', use_column_width=True)
            
            # Multi-select menu for texture options
            st.subheader("Rate the texture")
            texture_options = ["Crispy", "Creamy", "Chewy", "Crunchy", "Soft", "Slimy", "Firm", "Fluffy"]
            selected_textures = st.multiselect("Select textures present in the dish", texture_options, key='selected_textures')
            
            # Create sliders for each selected texture
            texture_ratings = {}
            for texture in selected_textures:
                rating = st.slider(f"Rate the presence of {texture} texture on a scale of 1 to 10", 1, 10, 5, key=f"slider_{texture}")
                texture_ratings[texture] = rating
            
            # Display selected textures and their ratings
            st.write("Your selected textures and their ratings:")
            for texture, rating in texture_ratings.items():
                st.write(f"{texture}: {rating}/10")

            # Save ratings to database
            if st.button("Submit"):
                save_ratings(search_food_name, texture_ratings)
                st.write("Thank you for your feedback! The ratings have been saved.")
                clear_inputs()

    # Optional: Collect and store user feedback
    feedback = st.text_area("Additional feedback", key='feedback')
    if st.button("Submit Feedback"):
        st.write("Thank you for your feedback!")
        clear_inputs()

# Clear button
if st.button("Clear"):
    clear_inputs()
    st.write("Inputs have been cleared.")
