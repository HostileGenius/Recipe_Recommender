import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
import streamlit as st

# Load the dataset
@st.cache_data
def load_data(file_path):
    df = pd.read_csv(file_path)
    df['Cleaned-Ingredients'] = df['Cleaned-Ingredients'].str.lower()
    df['Cleaned-Ingredients'] = df['Cleaned-Ingredients'].apply(lambda x: ' '.join(x.split(',')))
    return df

# Train the model
@st.cache_data
def train_model(df):
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df['Cleaned-Ingredients'])
    knn = NearestNeighbors(n_neighbors=5, metric='cosine')
    knn.fit(X)
    return vectorizer, knn

# Recommend recipes
def recommend_recipes(user_ingredients, vectorizer, knn, df):
    user_input_vector = vectorizer.transform([' '.join(user_ingredients.lower().split(','))])
    distances, indices = knn.kneighbors(user_input_vector)
    recommendations = df.iloc[indices[0]].copy()
    recommendations['Similarity'] = 1 - distances[0]  # Convert distance to similarity
    return recommendations[['TranslatedRecipeName', 'TranslatedIngredients', 'Cuisine', 'TotalTimeInMins', 'Similarity', 'URL']]

# Streamlit UI
st.title("Recipe Recommender")

# File upload
file_path = st.text_input("Enter the path to your dataset:", "C:/Users/shiva/Downloads/Cleaned_Indian_Food_Dataset/Recipes.csv")
if file_path:
    recipes_df = load_data(file_path)
    vectorizer, knn = train_model(recipes_df)

    st.write("### Enter the ingredients you have:")
    user_input = st.text_input("Ingredients (comma-separated):")

    if st.button("Find Recipes"):
        if user_input:
            recommendations = recommend_recipes(user_input, vectorizer, knn, recipes_df)
            if not recommendations.empty:
                st.write("### Top Recommended Recipes:")
                for _, row in recommendations.iterrows():
                    st.write(f"**Recipe Name:** {row['TranslatedRecipeName']}")
                    st.write(f"**Ingredients:** {row['TranslatedIngredients']}")
                    st.write(f"**Cuisine:** {row['Cuisine']}")
                    st.write(f"**Total Time (mins):** {row['TotalTimeInMins']}")
                    st.write(f"**Similarity Score:** {row['Similarity']:.2f}")
                    st.write(f"[Recipe Link]({row['URL']})")
                    st.write("---")
            else:
                st.write("No recipes found for the given ingredients.")
        else:
            st.write("Please enter some ingredients.")
