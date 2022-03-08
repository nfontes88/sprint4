import sqlite3


def open_db(filename: str) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)  # connect to existing DB or create new one
    cursor = db_connection.cursor()  # get ready to read/write data
    return db_connection, cursor


def close_db(connection: sqlite3.Connection):
    connection.commit()  # make sure any changes get saved
    connection.close()


def create_top250TV_table(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS top_show_data(
    ttid TEXT PRIMARY KEY,
    rank INTEGER DEFAULT 0,
    title TEXT,
    fulltitle TEXT,
    year INTEGER,
    image_url TEXT,
    crew TEXT,
    imdb_rating REAL,
    imdb_rating_count INTEGER);''')


def create_most_pop_tv_table(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS most_popular_shows(
    ttid TEXT PRIMARY KEY,
    rank INTEGER,
    rankchange INTEGER DEFAULT 0,
    title TEXT,
    fulltitle TEXT,
    year INTEGER,
    image_url TEXT,
    crew TEXT,
    rating REAL,
    ratingCount INTEGER);
    ''')


def create_most_pop_movie_table(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS most_popular_movies(
    ttid TEXT PRIMARY KEY,
    rank INTEGER,
    rankchange INTEGER DEFAULT 0,
    title TEXT,
    fulltitle TEXT,
    year INTEGER,
    image_url TEXT,
    crew TEXT,
    rating REAL,
    ratingCount INTEGER);
    ''')


def create_top250movie_table(cursor: sqlite3.Cursor):
    # if I was trying to be clever, I would use the same table for top250 movies and top250 tv and just use an extra
    # field in the database to mark it as movie or TV, but since most of you who are looking for this are looking for
    # a straightforward solution we'll do it this way.
    cursor.execute('''CREATE TABLE IF NOT EXISTS top_movie_data(
    ttid TEXT PRIMARY KEY,
    rank INTEGER DEFAULT 0,
    title TEXT,
    fulltitle TEXT,
    year INTEGER,
    image_url TEXT,
    crew TEXT,
    imdb_rating REAL,
    imdb_rating_count INTEGER);''')


def create_tv_ratings_table(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS show_ratings(
    ratings_key INTEGER PRIMARY KEY,
    imdb_ttcode TEXT NOT NULL,
    title TEXT,
    fulltitle TEXT,
    year INTEGER,
    total_rating INT DEFAULT 0,
    total_votes INTEGER,
    rating10_percent REAL,
    rating10_votes INTEGER,
    rating9_percent REAL,
    rating9_votes INTEGER,
    rating8_percent REAL,
    rating8_votes INTEGER,
    rating7_percent REAL,
    rating7_votes INTEGER,
    rating6_percent REAL,
    rating6_votes INTEGER,
    rating5_percent REAL,
    rating5_votes INTEGER,
    rating4_percent REAL,
    rating4_votes INTEGER,
    rating3_percent REAL,
    rating3_votes INTEGER,
    rating2_percent REAL,
    rating2_votes INTEGER,
    rating1_percent REAL,
    rating1_votes INTEGER,
    FOREIGN KEY (imdb_ttcode) REFERENCES top_show_data (ttid)
    ON DELETE CASCADE ON UPDATE NO ACTION
    );''')


def create_all_tables(db_cursor: sqlite3.Cursor):
    create_top250TV_table(db_cursor)
    create_tv_ratings_table(db_cursor)
    create_top250movie_table(db_cursor)
    create_most_pop_tv_table(db_cursor)
    create_most_pop_movie_table(db_cursor)


def put_top_250_in_database(table: str, data_to_add: list[tuple], db_cursor: sqlite3.Cursor):
    db_cursor.executemany(f"""INSERT INTO {table}(ttid, rank, title, fulltitle, year, image_url, crew, imdb_rating,
    imdb_rating_count)
    VALUES(?,?,?,?,?,?,?,?,?)""", data_to_add)


def put_most_popular_in_database(table: str, data_to_add: list[tuple], db_cursor: sqlite3.Cursor):
    db_cursor.executemany(f"""INSERT INTO {table}(ttid, rank, rankchange, title, fulltitle, year, image_url, crew, rating,
    ratingcount)
    VALUES(?,?,?,?,?,?,?,?,?, ?)""", data_to_add)


def put_in_wheel_of_time(db_cursor: sqlite3.Cursor):
    """this is just a total kludge. I need a Wheel of time Entry for the foreign key to work, so I'm just adding it"""
    db_cursor.execute("""INSERT INTO top_show_data(ttid, rank, title, fulltitle, year, image_url, crew, imdb_rating, imdb_rating_count)
    VALUES('tt7462410',0,'The Wheel of Time','The Wheel of Time (TV Series 2021– )',2021,'','Rosamund Pike, Daniel Henney',
    7.2,85286)""")


def put_ratings_into_db(data_to_add: list[tuple], db_cursor: sqlite3.Cursor):
    db_cursor.executemany("""INSERT INTO show_ratings(imdb_ttcode, title, fulltitle, year, total_rating, total_votes,
    rating10_percent,
    rating10_votes, rating9_percent, rating9_votes, rating8_percent, rating8_votes, rating7_percent, rating7_votes,
    rating6_percent, rating6_votes, rating5_percent, rating5_votes, rating4_percent, rating4_votes, rating3_percent,
    rating3_votes, rating2_percent, rating2_votes, rating1_percent, rating1_votes)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", data_to_add)