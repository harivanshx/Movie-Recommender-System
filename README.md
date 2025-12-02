# Movie Recommender System

A content-based movie recommendation system that uses cosine similarity to find similar movies based on genres, keywords, cast, crew, and overview.

## Project Structure

- `tmdb_5000_movies.csv` - Movie data from The Movie Database (TMDb)
- `tmdb_5000_credits.csv` - Cast and crew data from TMDb
- `movie_recommender_system.ipynb` - Jupyter notebook with data exploration and model building
- `generate_pickles.py` - Script to generate pickle files (run this first!)
- `app.py` - Streamlit web application for recommendations
- `requirements.txt` - Python dependencies

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate Pickle Files
The large binary pickle files (`Movies.pkl` and `similarity.pkl`) are NOT included in the repository. Generate them by running:
```bash
python generate_pickles.py
```
This will process the CSV files and create the necessary pickle files. This may take a few minutes.

### 3. Set Up TMDb API Key
Create a `.env` file in the project root:
```
TMDB_API_KEY=your_api_key_here
```
Get your API key from: https://www.themoviedb.org/settings/api

### 4. Run the Application
```bash
streamlit run app.py
```
The app will open in your browser at `http://localhost:8501`

## How It Works

1. **Data Processing**: Combines movie and credits data, extracting genres, keywords, top 3 cast members, and director
2. **Text Preprocessing**: Uses stemming to normalize words and create feature tags
3. **Vectorization**: Converts text to numerical vectors using CountVectorizer (5000 most common words)
4. **Similarity Calculation**: Computes cosine similarity between all movie vectors
5. **Recommendation**: Returns top 5 most similar movies for a given input movie

## File Sizes

The generated pickle files are large and should NOT be committed to Git:
- `Movies.pkl` - ~20 MB
- `similarity.pkl` - ~200+ MB

These are automatically ignored by `.gitignore`

## Troubleshooting

**Cannot fetch movie posters?**
- Ensure you have an internet connection
- Check if your API key is valid
- If behind a corporate firewall, try using a VPN
- The app will gracefully handle API failures by showing placeholder images