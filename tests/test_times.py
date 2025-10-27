import time
from times import time_range, compute_overlap_time
import pytest

def test_overlap():
    large = time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
    expected = [("2010-01-12 10:30:00","2010-01-12 10:37:00"), ("2010-01-12 10:38:00", "2010-01-12 10:45:00")]
    assert compute_overlap_time(large, short) == expected

def test_value_error_on_invalid_range():
    pytest.raises(ValueError, time_range, "2010-01-12 12:00:00", "2010-01-12 10:00:00")

def test_no_overlap():
    range1 = time_range("2022-01-01 10:00:00", "2022-01-01 11:00:00")
    range2 = time_range("2022-01-01 11:30:00", "2022-01-01 12:30:00")
    expected = []
    assert compute_overlap_time(range1, range2) == expected

@pytest.mark.parametrize("range1, range2, expected", [
    # Normal overlapping ranges
    (time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00"),
     time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60),
     [("2010-01-12 10:30:00","2010-01-12 10:37:00"), ("2010-01-12 10:38:00", "2010-01-12 10:45:00")]),
    # Non-overlapping ranges
    (time_range("2022-01-01 10:00:00", "2022-01-01 11:00:00"),
     time_range("2022-01-01 11:30:00", "2022-01-01 12:30:00"),
     []),
    # Overlapping at the edge
    ( [("2022-01-01 10:00:00", "2022-01-01 11:00:00")],
      [("2022-01-01 11:00:00", "2022-01-01 12:00:00")],
      []),
    # One range completely inside another
    ([("2022-01-01 10:00:00", "2022-01-01 11:00:00")],
     [("2022-01-01 10:15:00", "2022-01-01 10:45:00")],
     [("2022-01-01 10:15:00", "2022-01-01 10:45:00")]),
])
        
def test_compute_overlap_time_parametrized(range1, range2, expected):
    assert compute_overlap_time(range1, range2) == expected                  