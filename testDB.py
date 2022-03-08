import dataBaseStuff
import os

# we'll save this one for the next tests
test_api_data_entry = [{"id": "tttestdata", "rank": "10002", "title": "Comp490 Project 1 Show",
                        "fullTitle": "Comp490 Project 1 Show (2022)", "year": "2022", "image": "",
                        "crew": "Prof. Santore and many hardworking students", "imDbRating": "9.2",
                        "imDbRatingCount": "41"}]


# test here actually showed me a hidden error in my database
def test_enter_data():
    # I should really do some of this in a fixture, but I wanted to do it with just what you already have
    # the database needs to be deleted everytime to make this test run, which is good for github actions
    test_data_entry = [("tttestdata", 10002, "Comp490 Project 1 Show", "Comp490 Project 1 Show (2022)", 2022,
                        "", "Prof. Santore and many hardworking students", 9.2, 41)]

    connection, db_cursor = dataBaseStuff.open_db("testDatabase.sqlite")
    dataBaseStuff.create_top250TV_table(db_cursor)
    dataBaseStuff.put_top_250_in_database("top_show_data", test_data_entry, db_cursor)
    connection.commit()
    # this test in the next four lines wasn't technically required, but I wanted to demo the count feature
    # and it is a good idea. I could test by checking the len of record_count_set also
    db_cursor.execute("SELECT COUNT() FROM top_show_data WHERE ttid = 'tttestdata'")
    record_count_set = db_cursor.fetchone()
    number_of_records = record_count_set[0]  # the count returns a tuple, the count is the first element
    assert number_of_records == 1
    db_cursor.execute("SELECT * FROM top_show_data WHERE ttid = 'tttestdata'")
    record_set = db_cursor.fetchall()
    assert record_set[0] == test_data_entry[0]


def test_table_exists():
    # first lets get rid of the database if it exists
    if os.path.exists("testDatabase.sqlite"):
        os.remove("testDatabase.sqlite")
    connection, db_cursor = dataBaseStuff.open_db("testDatabase.sqlite")
    dataBaseStuff.create_most_pop_movie_table(db_cursor)
    db_cursor.execute('''SELECT * FROM sqlite_master WHERE tbl_name = ? AND type = ?''',
                      ("most_popular_movies", "table"))
    data = db_cursor.fetchall()
    assert len(data) == 1  # since I'm using where clause to only find the most popular movies we should have exactly 1


def test_put_most_popular():
    # first lets get rid of the database if it exists
    if os.path.exists("testDatabase.sqlite"):
        os.remove("testDatabase.sqlite")
    connection, db_cursor = dataBaseStuff.open_db("testDatabase.sqlite")
    dataBaseStuff.create_most_pop_movie_table(db_cursor)
    test_pop_data_entry = [("tttestdata1", 10002, -4, "Comp490 Project 1 Show",
                            "Comp490 Project 1 Show (2022)", 2022, "",
                            "Prof. Santore and many hardworking students", 9.2, 41),
                           ("tttestdata2", 1, 32, "Graduation",
                            "Graduation (2022)", 2022, "",
                            "Many hardworking students", 9.9, 38)
                           ]
    dataBaseStuff.put_most_popular_in_database("most_popular_movies", test_pop_data_entry, db_cursor)
    connection.commit()
    db_cursor.execute('''SELECT * FROM most_popular_movies ''', )
    data = db_cursor.fetchall()
    assert len(data) == 2  # we removed the db, so only the data we put in should be there
    assert data[0][0] == "tttestdata1"  # but we still need to make sure the right data went it
    assert data[1][0] == "tttestdata2"


def test_foriegn_key():
    # first lets get rid of the database if it exists
    if os.path.exists("testDatabase.sqlite"):
        os.remove("testDatabase.sqlite")
    connection, db_cursor = dataBaseStuff.open_db("testDatabase.sqlite")
    dataBaseStuff.create_top250TV_table(db_cursor)
    dataBaseStuff.create_tv_ratings_table(db_cursor)
    db_cursor.execute('''SELECT sql FROM sqlite_master WHERE tbl_name = ? AND type = ?''', ("show_ratings", "table"))
    data = db_cursor.fetchall()
    assert len(data) == 1  # there should only be one table
    sql_statement: str = data[0][0]  # get the only data data is a list of one row, which contains only one column
    assert "FOREIGN KEY" in sql_statement and "REFERENCES top_show_data" in sql_statement