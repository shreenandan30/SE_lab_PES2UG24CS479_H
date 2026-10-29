"""Branch-coverage tests for every decision in ride_share_fare.py."""

import pytest

from ride_share_fare import (
    extra_distance_fare,
    pickup_status,
    seats_and_bags_ok,
)


# extra_distance_fare: unknown/known cab types and invalid/valid distances.
def test_unknown_cab_type_takes_error_branch():
    with pytest.raises(ValueError, match="unknown cab type"):
        extra_distance_fare("bike", 10, "city", False)


def test_negative_distance_takes_error_branch():
    with pytest.raises(ValueError, match="invalid distance"):
        extra_distance_fare("mini", -1, "city", False)


# The subscriber condition is true, false on its first term, and false on
# its second term (subscriber SUV).
def test_subscriber_non_suv_gets_included_distance_bonus():
    assert extra_distance_fare("mini", 10, "city", True) == 24


def test_non_subscriber_does_not_get_included_distance_bonus():
    assert extra_distance_fare("mini", 10, "city", False) == 60


def test_subscriber_suv_does_not_get_included_distance_bonus():
    assert extra_distance_fare("suv", 15, "city", True) == 36


# extra <= 0: true and false.
def test_distance_at_included_limit_has_zero_fare():
    assert extra_distance_fare("sedan", 8, "city", False) == 0


def test_distance_above_included_limit_has_positive_fare():
    assert extra_distance_fare("mini", 10, "city", False) == 60


# zone == city: true and false; extra > 20: true and false;
# nested zone == outstation: true and false.
def test_non_city_zone_with_short_extra_distance_uses_base_outstation_rate():
    assert extra_distance_fare("mini", 10, "outstation", False) == 90


def test_long_city_distance_uses_city_surcharge_without_outstation_surcharge():
    assert extra_distance_fare("mini", 30, "city", False) == 500


def test_long_outstation_distance_uses_all_surcharges():
    assert extra_distance_fare("mini", 30, "outstation", False) == 750


# seats_and_bags_ok: wheelchair true/false, passenger limit true/false,
# regular passenger limit true/false, and bag limit true/false.
def test_wheelchair_ride_accepts_two_passengers():
    assert seats_and_bags_ok(2, 0, True) is True


def test_wheelchair_ride_rejects_more_than_two_passengers():
    assert seats_and_bags_ok(3, 0, True) is False


def test_regular_ride_rejects_more_than_four_passengers():
    assert seats_and_bags_ok(5, 0, False) is False


def test_regular_ride_checks_bag_limit_and_accepts_two_bags():
    assert seats_and_bags_ok(4, 2, False) is True


def test_regular_ride_rejects_more_than_two_bags():
    assert seats_and_bags_ok(4, 3, False) is False


# pickup_status: scheduled/unscheduled, airport/non-airport, and all three
# outcomes of on_time / delayed / missed decisions.
def test_scheduled_non_airport_pickup_on_time():
    assert pickup_status(10, True, False) == "on_time"


def test_scheduled_non_airport_pickup_delayed():
    assert pickup_status(9, True, False) == "delayed"


def test_scheduled_non_airport_pickup_missed():
    assert pickup_status(-6, True, False) == "missed"


def test_unscheduled_non_airport_pickup_on_time():
    assert pickup_status(5, False, False) == "on_time"


def test_unscheduled_airport_pickup_on_time():
    # Unscheduled cutoff is 5 minutes; airport adds 10, making it 15.
    assert pickup_status(15, False, True) == "on_time"


def test_unscheduled_airport_pickup_delayed():
    # Airport cutoff is 15; delayed threshold is 0.
    assert pickup_status(0, False, True) == "delayed"
