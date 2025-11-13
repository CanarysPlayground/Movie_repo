Simple Movie Website (Flask)
---------------------------

This is a minimal Flask application that demonstrates a movie website with API routes for:
- Listing movies: GET /api/movies
- Movie details: GET /api/movies/<id>
- Add movie to playlist: POST /api/playlist  (JSON body: {"movie_id": 1})
- View playlist: GET /api/playlist

How to run:
1. Create a virtualenv and install requirements: pip install -r requirements.txt
2. Run the app: python app.py
3. Open http://127.0.0.1:5000 in your browser.

The project includes a small SQLite database (movies.db) seeded with sample movies.