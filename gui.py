import requests
import secrets
import sys
from tkinter import *
import numpy as np
import matplotlib.pyplot as plt

root = tk()
# creating a label widget
myLabel1 = Label(root, text="update the data")
myLabel2 = Label(root, text="run the data visualization")


# printing it onto the screen
myLabel1.grid(row=0, column=0)
myLabel2.grid(row=1, column=0)


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


root.title('graph')


def build_graph():
    most_popular_movies_moving_up = np.random.normal()
    plt.hist(most_popular_movies_moving_up)
    plt.show()


    most_popular_movies_moving_down = np.random.normal()
    plt.hist(most_popular_movies_moving_down)
    plt.show()

    most_popular_tvshows_moving_up = np.random.normal()
    plt.hist(most_popular_tvshows_moving_up)
    plt.show()

    most_popular_tvshows_moving_down = np.random.normal()
    plt.hist(most_popular_tvshows_moving_down)
    plt.show()


    top250_movies = np.random.normal()
    plt.hist(top250_movies)
    plt.show()

    top250_tv = np.random.normal()
    plt.hist(top250_tv)
    plt.show()


my_button = Button(root, text="Graph It", command=graph)
my_button.pack()


root.mainloop()
