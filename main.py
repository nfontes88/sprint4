import sqlite3

import api_data
import dataBaseStuff


def report_results(data_to_write: list):
    with open("Output.txt", mode='a') as outputFile:  # open the output file for appending
        for show in data_to_write:
            print(show, file=outputFile)  # write each data item to file
            print("\n", file=outputFile)
            print("===================================================================", file=outputFile)


def get_data_and_put_in_db(db_cursor: sqlite3.Cursor):
    top_show_data = api_data.get_top_250_data("TV")
    top_movie_data = api_data.get_top_250_data("Movie")
    top_show_data_for_db = api_data.prepare_top_250_data(top_show_data)
    top_movie_data_for_db = api_data.prepare_top_250_data(top_movie_data)
    most_pop_movies = api_data.get_most_popular("Movies")
    most_pop_tv = api_data.get_most_popular("TVs")
    # I'm getting sloppy here to make this quicker and the code smaller
    dataBaseStuff.put_top_250_in_database("top_show_data", top_show_data_for_db, db_cursor)
    dataBaseStuff.put_top_250_in_database("top_movie_data", top_movie_data_for_db, db_cursor)
    dataBaseStuff.put_most_popular_in_database("most_popular_movies", most_pop_movies, db_cursor)
    dataBaseStuff.put_most_popular_in_database("most_popular_shows", most_pop_tv, db_cursor)
    dataBaseStuff.put_in_wheel_of_time(db_cursor)
    big_mover_records = api_data.get_big_movers(most_pop_movies)
    big_mover_ratings = api_data.get_big_mover_ratings(big_mover_records)
    ratings_data = api_data.get_ratings(top_show_data)
    db_ready_ratings_data = api_data.prepare_ratings_for_db(ratings_data)
    dataBaseStuff.put_ratings_into_db(db_ready_ratings_data, db_cursor)
    dataBaseStuff.put_ratings_into_db(big_mover_ratings, db_cursor)


def main():
    connection, db_cursor = dataBaseStuff.open_db("project1db.sqlite")
    dataBaseStuff.create_all_tables(db_cursor)
    get_data_and_put_in_db(db_cursor)
    dataBaseStuff.close_db(connection)


if __name__ == '__main__':
    main()