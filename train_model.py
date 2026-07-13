import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
movies = pd.read_csv("dataset/movies.csv")

# Replace missing genres (if any)
movies["genres"] = movies["genres"].fillna("")

# Create TF-IDF vectors from genres
tfidf = TfidfVectorizer(stop_words="english")
tfidf_matrix = tfidf.fit_transform(movies["genres"])

# Calculate cosine similarity
similarity = cosine_similarity(tfidf_matrix)

# Save the movie dataset
pickle.dump(movies, open("model/movies.pkl", "wb"))

# Save the similarity matrix
pickle.dump(similarity, open("model/similarity.pkl", "wb"))

print("✅ Recommendation model created successfully!")