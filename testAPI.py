import api_data
import pytest


def test_gettop250():
    top250_results = api_data.get_top_250_data("TV")
    assert len(top250_results) == 250


def test_get_big_movers():
    # 'Happy Path'
    # creating short test data because my function never look beyond the third item
    test_data = [("ttstuff1", 1, 35, "sprint2", "@#$@# sprint 2"),
                 ("ttstuff2", 35, -40, "sprint4", "@#$@# sprint 4"),
                 ("ttstuff3", 3, 50, "Sprint3", "Hey this isn't so bad sprint 3"),
                 ("ttstuff4", 4, -3, "Midterm", "Take Home Midterm"),
                 ("ttstuff5", 6, 12, "sprint1", "Sprint1 , a new beginning"),
                 ("ttstuff6", 12, 22, "Quiz1", "Quiz1 2022"),
                 ("ttstuff7", 14, -7, "Quiz2", "Quiz2 2022")]

    test_result1 = api_data.get_big_movers(test_data)
    assert test_result1[0][0] == "ttstuff3"  # the first one should be the biggest positive, first item is ttcode
    assert test_result1[-1][0] == "ttstuff2"  # -1 gives last item in list, which should be biggest negative mover

    # 'bad test' data add

    test_data[3] = ("ttbadData", 1)
    with pytest.raises(ValueError):
        api_data.get_big_movers(test_data)