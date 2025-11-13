DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS playlist;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE movies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    year INTEGER,
    genre TEXT,
    synopsis TEXT
);

CREATE TABLE playlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    movie_id INTEGER NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(movie_id) REFERENCES movies(id)
);

-- seed data (15 sample movies)
INSERT INTO movies (title, year, genre, synopsis) VALUES
('The Matrix', 1999, 'Sci-Fi', 'A hacker discovers a shocking truth about reality and joins a rebellion.'),
('Inception', 2010, 'Sci-Fi/Thriller', 'A thief who steals secrets through dream-sharing technology is given a chance at redemption.'),
('Interstellar', 2014, 'Sci-Fi/Drama', 'Explorers travel through a wormhole in space in an attempt to ensure humanity''s survival.'),
('The Shawshank Redemption', 1994, 'Drama', 'Two imprisoned men bond over years, finding solace and eventual redemption.'),
('The Dark Knight', 2008, 'Action/Crime', 'Batman faces the Joker, a criminal mastermind who seeks to create chaos in Gotham.'),
('Forrest Gump', 1994, 'Drama', 'The presidencies of Kennedy and Johnson, the Vietnam War, and more through the eyes of Forrest.'),
('The Lord of the Rings: The Fellowship of the Ring', 2001, 'Fantasy', 'A meek Hobbit begins a journey to destroy a powerful ring.'),
('Pulp Fiction', 1994, 'Crime', 'The lives of two mob hitmen, a boxer, and others intertwine in tales of violence and redemption.'),
('The Social Network', 2010, 'Drama', 'The story of Facebook''s founding and the conflicts that followed.'),
('Parasite', 2019, 'Thriller/Drama', 'A poor family schemes to become employed by a wealthy household.'),
('Gladiator', 2000, 'Action/Drama', 'A former Roman General seeks revenge after being betrayed.'),
('The Prestige', 2006, 'Mystery/Thriller', 'Two magicians engage in a fierce rivalry.'),
('Whiplash', 2014, 'Drama', 'A young drummer enrolls at a music conservatory and endures an intense instructor.'),
('Mad Max: Fury Road', 2015, 'Action', 'In a post-apocalyptic wasteland, a woman rebels against a tyrant.'),
('La La Land', 2016, 'Musical/Romance', 'An aspiring actress and a jazz musician fall in love.');