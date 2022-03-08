import requests
import secrets
import sys


def get_top_250_data(what_kind: str) -> list[dict]:
    api_query = f"https://imdb-api.com/en/API/Top250{what_kind}s/{secrets.secret_key}"
    response = requests.get(api_query)
    if response.status_code != 200:  # if we don't get an ok response we have trouble
        print(f"Failed to get data, response code:{response.status_code} and error message: {response.reason} ")
        sys.exit(-1)
    # jsonresponse is a kinda useless dictionary, but the items element has what we need
    jsonresponse = response.json()
    top250_list = jsonresponse["items"]
    return top250_list


def get_most_popular(type: str) -> list[tuple]:
    api_query = f"https://imdb-api.com/en/API/MostPopular{type}/{secrets.secret_key}"
    response = requests.get(api_query)
    if response.status_code != 200:  # if we don't get an ok response we have trouble
        print(f"Failed to get data, response code:{response.status_code} and error message: {response.reason} ")
        sys.exit(-1)
    jsonresponse = response.json()
    most_pop_list = jsonresponse["items"]
    most_pop_ready = prepare_most_popular(most_pop_list)
    return most_pop_ready


def get_ratings(top_show_data: list[dict]) -> list[dict]:
    results = []
    api_queries = []
    base_query = f"https://imdb-api.com/en/API/UserRatings/{secrets.secret_key}/"
    wheel_of_time_query = f"{base_query}tt7462410"
    api_queries.append(wheel_of_time_query)
    first_query = f"{base_query}{top_show_data[0]['id']}"
    api_queries.append(first_query)
    fifty_query = f"{base_query}{top_show_data[49]['id']}"
    api_queries.append(fifty_query)
    hundred_query = f"{base_query}{top_show_data[99]['id']}"
    api_queries.append(hundred_query)
    two_hundered = f"{base_query}{top_show_data[199]['id']}"
    api_queries.append(two_hundered)
    for query in api_queries:
        response = requests.get(query)
        if response.status_code != 200:  # if we don't get an ok response we have trouble, skip it
            print(f"Failed to get data, response code:{response.status_code} and error message: {response.reason} ")
            continue
        rating_data = response.json()
        results.append(rating_data)
    return results


def prepare_most_popular(top_show_data: list[dict]) -> list[tuple]:
    data_for_database = []
    for show_data in top_show_data:
        show_values = list(show_data.values())  # dict values is now an object that is almost a list, lets make it one
        # now we have the values, but several of them are strings and I would like them to be numbers
        # since python 3.7 dictionaries are guaranteed to be in insertion order
        show_values[1] = int(show_values[1])  # convert rank to int
        show_values[2] = rank_to_int(show_values[2])  # rank up down sometimes has bad data so handle it specially
        show_values[4] = int(show_values[5])  # convert year to int
        show_values[7] = rating_to_float(show_values[8])  # convert rating to float, some are '' and need to become 0
        show_values[8] = int(show_values[9])  # convert rating count to int
        # now covert the list of values to a tuple to easy insertion into the database
        show_values = tuple(show_values)
        data_for_database.append(show_values)
    return data_for_database


def rank_to_int(rank_val: str) -> int:
    try:
        real_rank = int(rank_val)
        return real_rank
    except ValueError:
        return 0


def rating_to_float(rating: str) -> float:
    try:
        real_rank = float(rating)
        return real_rank
    except ValueError:
        return 0


def get_big_movers(popular_movies: list[tuple]) -> list[tuple]:
    popular_movies.sort(key=get_sort_key, reverse=True)  # order the list by rankupdown with positive moves first
    big_movers = []
    big_movers.extend(popular_movies[:3])  # put the first three items from the sorted list into the final list
    big_movers.append(popular_movies[-1])  # put the last item from the sorted list into the final list
    return big_movers


def get_big_mover_ratings(big_movers: list[tuple]) -> list[tuple]:
    big_mover_rating_data = []
    for mover in big_movers:
        url = f"https://imdb-api.com/en/API/UserRatings/{secrets.secret_key}/{mover[0]}"  # the ttid is in position 0
        response = requests.get(url)
        if response.status_code != 200:
            print(f"response code for {mover[3]} came back : {response.status_code}")
            continue
        big_mover_rating_data.append(response.json())
    big_mover_rating_data = prepare_ratings_for_db(big_mover_rating_data)
    return big_mover_rating_data


def get_sort_key(item):
    if len(item) < 3:
        raise ValueError
    return item[2]  # rank up down is in index 2 of the tuple


def prepare_top_250_data(most_popular_json: list[dict]) -> list[tuple]:
    data_for_database = []
    for show_data in most_popular_json:
        show_values = list(show_data.values())  # dict values is now an object that is almost a list, lets make it one
        # now we have the values, but several of them are strings and I would like them to be numbers
        # since python 3.7 dictionaries are guaranteed to be in insertion order
        show_values[1] = int(show_values[1])  # convert rank to int
        show_values[4] = int(show_values[4])  # convert year to int
        show_values[7] = float(show_values[7])  # convert rating to float
        show_values[8] = int(show_values[8])  # convert rating count to int
        # now covert the list of values to a tuple to easy insertion into the database
        show_values = tuple(show_values)
        data_for_database.append(show_values)
    return data_for_database


def make_zero_values() -> list[dict]:
    """this is a kludge to deal with the fact that one record has no ratings data"""
    zero_rating = []
    for rating_value in range(10, 0, -1):
        rating = {}
        rating['rating'] = rating_value
        rating['percent'] = '0%'
        rating['votes'] = 0
        zero_rating.append(rating)
    return zero_rating


def _flatten_and_tuplize(ratings_entry: dict) -> tuple:
    db_ready_list = []
    db_ready_list.append(ratings_entry['imDbId'])
    db_ready_list.append(ratings_entry['title'])
    db_ready_list.append(ratings_entry['fullTitle'])
    db_ready_list.append(int(ratings_entry['year']))
    db_ready_list.append(int(ratings_entry['totalRating']))
    db_ready_list.append(int(ratings_entry['totalRatingVotes']))
    if not ratings_entry['ratings']:  # deal with #200 missing ratings
        ratings_entry['ratings'] = make_zero_values()
    for rating in ratings_entry['ratings']:
        # the first data is a percent and we need to remove the % then conver it to a float
        str_percent = rating['percent']
        str_percent = str_percent[:-1]  # slice with all but the last character
        db_ready_list.append(float(str_percent))
        db_ready_list.append(int(rating['votes']))
    return tuple(db_ready_list)


def prepare_ratings_for_db(ratings: list[dict]) -> list[tuple]:
    data_for_database = []
    for ratings_entry in ratings:
        db_redy_entry = _flatten_and_tuplize(ratings_entry)
        data_for_database.append(db_redy_entry)
    return data_for_database