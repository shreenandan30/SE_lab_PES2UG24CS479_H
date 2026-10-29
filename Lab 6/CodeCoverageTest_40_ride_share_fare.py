"""Statement/code-coverage tests for ride_share_fare.py."""

import pytest

from ride_share_fare import (
    extra_distance_fare,
    pickup_status,
    seats_and_bags_ok,
)


def test_unknown_cab_type_raises_value_error():
    with pytest.raises(ValueError, match="unknown cab type"):
        extra_distance_fare("bike", 10, "city", False)


def test_negative_distance_raises_value_error():
    with pytest.raises(ValueError, match="invalid distance"):
        extra_distance_fare("mini", -1, "city", False)


def test_no_extra_fare_within_included_distance():
    assert extra_distance_fare("sedan", 5, "city", False) == 0


def test_subscriber_mini_city_fare():
    # Mini includes 5 km + 3 km for subscribers; 10 - 8 = 2 extra km.
    assert extra_distance_fare("mini", 10, "city", True) == 24


def test_long_city_fare_adds_long_distance_rate():
    # 25 extra km at (12 + 8) per km.
    assert extra_distance_fare("mini", 30, "city", False) == 500


def test_long_outstation_fare_adds_both_surcharges():
    # 25 extra km at (18 + 8 + 4) per km.
    assert extra_distance_fare("mini", 30, "outstation", False) == 750


def test_suv_subscriber_does_not_get_extra_included_kilometres():
    # SUV includes 12 km even for subscribers; 3 extra km at city rate 12.
    assert extra_distance_fare("suv", 15, "city", True) == 36


def test_wheelchair_passenger_limit_accepts_two():
    assert seats_and_bags_ok(2, 5, True) is True


def test_wheelchair_passenger_limit_rejects_three():
    assert seats_and_bags_ok(3, 0, True) is False


def test_more_than_four_passengers_is_rejected():
    assert seats_and_bags_ok(5, 0, False) is False


def test_regular_ride_accepts_two_bags():
    assert seats_and_bags_ok(4, 2, False) is True


def test_regular_ride_rejects_more_than_two_bags():
    assert seats_and_bags_ok(4, 3, False) is False


def test_scheduled_pickup_on_time():
    assert pickup_status(10, True, False) == "on_time"


def test_pickup_is_delayed():
    assert pickup_status(0, False, False) == "delayed"


def test_pickup_is_missed():
    assert pickup_status(-6, True, False) == "missed"
