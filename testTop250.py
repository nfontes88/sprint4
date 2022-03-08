import api_data


def test_top_250_data():
    top250_results = api_data.get_top_250_data("TV")
    assert len(top250_results) == 250


def test_most_popular():
    most_pop_results = api_data.get_most_popular("crossovers")
    assert len(most_pop-results) == 200

