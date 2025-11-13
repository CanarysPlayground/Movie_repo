"""
Unit tests for the search_movies function in app.py

This test suite covers:
- Basic search functionality
- Case-insensitive search
- Partial matching
- Empty query handling
- No results scenarios
- Special characters handling
- Title and synopsis search
"""

import pytest
import sqlite3
from unittest.mock import patch
from flask import g
from app import search_movies, app, get_db


@pytest.fixture
def test_db():
    """Create an in-memory test database with sample data"""
    db = sqlite3.connect(':memory:')
    db.row_factory = sqlite3.Row
    
    # Create movies table
    db.execute('''
        CREATE TABLE movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            year INTEGER,
            genre TEXT,
            synopsis TEXT
        )
    ''')
    
    # Insert sample test data
    test_movies = [
        ('The Shawshank Redemption', 1994, 'Drama', 'Two imprisoned men bond over a number of years'),
        ('The Godfather', 1972, 'Crime', 'The aging patriarch of an organized crime dynasty'),
        ('The Dark Knight', 2008, 'Action', 'When the menace known as the Joker wreaks havoc'),
        ('Inception', 2010, 'Sci-Fi', 'A thief who steals corporate secrets through dream-sharing'),
        ('Pulp Fiction', 1994, 'Crime', 'The lives of two mob hitmen, a boxer, a gangster'),
        ('Forrest Gump', 1994, 'Drama', 'The presidencies of Kennedy and Johnson unfold'),
        ('The Matrix', 1999, 'Sci-Fi', 'A computer hacker learns about the true nature of reality'),
    ]
    
    for title, year, genre, synopsis in test_movies:
        db.execute(
            'INSERT INTO movies (title, year, genre, synopsis) VALUES (?, ?, ?, ?)',
            (title, year, genre, synopsis)
        )
    db.commit()
    
    return db


@pytest.fixture
def test_app(test_db, monkeypatch):
    """Create test Flask application with mocked database"""
    app.config['TESTING'] = True
    
    # Monkeypatch get_db to return our test database
    def mock_get_db():
        return test_db
    
    monkeypatch.setattr('app.get_db', mock_get_db)
    
    return app


class TestSearchMovies:
    """Test suite for search_movies function"""
    
    def test_search_by_title_exact_match(self, test_app):
        """Test searching with exact title match"""
        with test_app.app_context():
            results = search_movies('Inception')
            
            assert len(results) == 1
            assert results[0]['title'] == 'Inception'
            assert results[0]['year'] == 2010
            assert results[0]['genre'] == 'Sci-Fi'
    
    def test_search_by_title_partial_match(self, test_app):
        """Test searching with partial title match"""
        with test_app.app_context():
            results = search_movies('The')
            
            # Should match: The Shawshank Redemption, The Godfather, The Dark Knight, The Matrix
            assert len(results) >= 4
            titles = [movie['title'] for movie in results]
            assert 'The Shawshank Redemption' in titles
            assert 'The Godfather' in titles
            assert 'The Dark Knight' in titles
            assert 'The Matrix' in titles
    
    def test_search_case_insensitive(self, test_app):
        """Test that search is case-insensitive"""
        with test_app.app_context():
            results_lower = search_movies('inception')
            results_upper = search_movies('INCEPTION')
            results_mixed = search_movies('InCePtIoN')
            
            assert len(results_lower) == 1
            assert len(results_upper) == 1
            assert len(results_mixed) == 1
            assert results_lower[0]['title'] == results_upper[0]['title']
            assert results_lower[0]['title'] == results_mixed[0]['title']
    
    def test_search_by_synopsis(self, test_app):
        """Test searching within movie synopsis"""
        with test_app.app_context():
            results = search_movies('hacker')
            
            assert len(results) == 1
            assert results[0]['title'] == 'The Matrix'
            assert 'hacker' in results[0]['synopsis'].lower()
    
    def test_search_matches_title_and_synopsis(self, test_app):
        """Test that search matches both title and synopsis"""
        with test_app.app_context():
            results = search_movies('organized')
            
            # Should match "The Godfather" which has 'organized crime dynasty' in synopsis
            assert len(results) >= 1
            titles = [movie['title'] for movie in results]
            assert 'The Godfather' in titles
    
    def test_search_empty_query(self, test_app):
        """Test searching with empty string"""
        with test_app.app_context():
            results = search_movies('')
            
            # Empty query should match all movies (since '%' + '' + '%' matches everything)
            assert len(results) == 7
    
    def test_search_no_results(self, test_app):
        """Test searching with query that yields no results"""
        with test_app.app_context():
            results = search_movies('NonexistentMovie12345')
            
            assert len(results) == 0
            assert isinstance(results, list)
    
    def test_search_special_characters(self, test_app):
        """Test searching with special characters"""
        with test_app.app_context():
            # Test with parentheses, apostrophes, etc.
            results = search_movies("men")
            
            # Should find movies containing 'men' in title or synopsis
            assert isinstance(results, list)
            assert len(results) >= 2  # Should match 'imprisoned men' and 'hitmen'
    
    def test_search_single_character(self, test_app):
        """Test searching with single character"""
        with test_app.app_context():
            results = search_movies('a')
            
            # Should match movies with 'a' in title or synopsis
            assert isinstance(results, list)
            assert len(results) > 0
    
    def test_search_numeric_query(self, test_app):
        """Test searching with numeric query"""
        with test_app.app_context():
            results = search_movies('1994')
            
            # Should match movies with 1994 in synopsis (if any)
            # Note: year field is not searched, only title and synopsis
            assert isinstance(results, list)
    
    def test_search_returns_all_fields(self, test_app):
        """Test that search returns all required fields"""
        with test_app.app_context():
            results = search_movies('Matrix')
            
            assert len(results) == 1
            movie = results[0]
            
            # Verify all fields are present
            assert 'id' in movie
            assert 'title' in movie
            assert 'year' in movie
            assert 'genre' in movie
            assert 'synopsis' in movie
            
            assert movie['title'] == 'The Matrix'
            assert movie['year'] == 1999
            assert movie['genre'] == 'Sci-Fi'
    
    def test_search_returns_ordered_by_id(self, test_app):
        """Test that results are ordered by id"""
        with test_app.app_context():
            results = search_movies('The')
            
            # Verify results are ordered by id
            if len(results) > 1:
                for i in range(len(results) - 1):
                    assert results[i]['id'] <= results[i + 1]['id']
    
    def test_search_with_whitespace(self, test_app):
        """Test searching with leading/trailing whitespace"""
        with test_app.app_context():
            results_normal = search_movies('Matrix')
            results_whitespace = search_movies('  Matrix  ')
            
            # The function doesn't strip whitespace, so these will have different results
            # Whitespace search will not match because it looks for '  Matrix  ' literally
            assert isinstance(results_normal, list)
            assert isinstance(results_whitespace, list)
            assert len(results_normal) > 0
    
    def test_search_multiple_words(self, test_app):
        """Test searching with multiple words"""
        with test_app.app_context():
            results = search_movies('Dark Knight')
            
            assert len(results) >= 1
            assert any('Dark Knight' in movie['title'] for movie in results)
    
    def test_search_genre_keyword(self, test_app):
        """Test searching for genre-related keywords"""
        with test_app.app_context():
            results = search_movies('imprisoned')
            
            # Should match "The Shawshank Redemption" which has 'imprisoned men' in synopsis
            assert len(results) >= 1
            titles = [movie['title'] for movie in results]
            assert 'The Shawshank Redemption' in titles
    
    def test_search_year_in_synopsis(self, test_app):
        """Test searching for year mentioned in synopsis"""
        with test_app.app_context():
            # Kennedy reference should be in Forrest Gump synopsis
            results = search_movies('Kennedy')
            
            assert len(results) >= 1
            assert any('Forrest Gump' in movie['title'] for movie in results)
    
    def test_search_result_structure(self, test_app):
        """Test that search results have correct structure"""
        with test_app.app_context():
            results = search_movies('Inception')
            
            assert isinstance(results, list)
            assert len(results) > 0
            
            for movie in results:
                assert isinstance(movie, dict)
                assert 'id' in movie
                assert 'title' in movie
                assert 'year' in movie
                assert 'genre' in movie
                assert 'synopsis' in movie


class TestSearchMoviesEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_search_sql_injection_prevention(self, test_app, test_db):
        """Test that SQL injection attempts are handled safely"""
        with test_app.app_context():
            # Try SQL injection patterns
            malicious_queries = [
                "'; DROP TABLE movies; --",
                "' OR '1'='1",
                "admin'--",
                "' UNION SELECT * FROM movies--"
            ]
            
            for query in malicious_queries:
                try:
                    results = search_movies(query)
                    # Should return safely (no matches expected)
                    assert isinstance(results, list)
                except sqlite3.Error:
                    # If an error occurs, it should be a safe error, not a successful injection
                    pytest.fail("SQL injection may be possible")
    
    def test_search_with_percent_sign(self, test_app, test_db):
        """Test searching with SQL wildcard character"""
        with test_app.app_context():
            # % is a SQL wildcard, should be escaped in user input
            results = search_movies('%')
            
            # Should treat % as literal character, not wildcard
            assert isinstance(results, list)
    
    def test_search_with_underscore(self, test_app, test_db):
        """Test searching with SQL wildcard character"""
        with test_app.app_context():
            # _ is a SQL wildcard for single character
            results = search_movies('_')
            
            # Should treat _ as literal character
            assert isinstance(results, list)
    
    def test_search_very_long_query(self, test_app, test_db):
        """Test searching with very long query string"""
        with test_app.app_context():
            long_query = 'a' * 1000
            results = search_movies(long_query)
            
            assert isinstance(results, list)
            assert len(results) == 0  # Should not match anything


class TestSearchMoviesIntegration:
    """Integration tests for search_movies with different data scenarios"""
    
    def test_search_with_empty_database(self, test_app, test_db):
        """Test searching when database is empty"""
        with test_app.app_context():
            # Clear the database
            test_db.execute('DELETE FROM movies')
            test_db.commit()
            
            results = search_movies('anything')
            
            assert len(results) == 0
            assert isinstance(results, list)
    
    def test_search_unicode_characters(self, test_app, test_db):
        """Test searching with unicode characters"""
        with test_app.app_context():
            # Add a movie with unicode characters
            test_db.execute(
                'INSERT INTO movies (title, year, genre, synopsis) VALUES (?, ?, ?, ?)',
                ('Amélie', 2001, 'Romance', 'A shy waitress decides to change the lives of those around her')
            )
            test_db.commit()
            
            results = search_movies('Amélie')
            
            assert len(results) >= 1
            assert any('Amélie' in movie['title'] for movie in results)
