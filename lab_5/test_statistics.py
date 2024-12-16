import pytest
from statistics_class import Statistics


@pytest.fixture
def sample_data():
    return [10, 20, 30, 40, 50]


def test_init_valid_data(sample_data):
    stats = Statistics(sample_data)
    assert stats.data == sample_data


def test_mean(sample_data):
    stats = Statistics(sample_data)
    assert stats.mean() == 30


def test_median_odd():
    stats = Statistics([10, 20, 30])
    assert stats.median() == 20


def test_median_even():
    stats = Statistics([10, 20, 30, 40])
    assert stats.median() == 25


def test_variance(sample_data):
    stats = Statistics(sample_data)
    assert stats.variance() == 200


def test_standard_deviation(sample_data):
    stats = Statistics(sample_data)
    assert pytest.approx(stats.standard_deviation(), 0.1) == 14.14


def test_variance_insufficient_data():
    stats = Statistics([10])
    with pytest.raises(ValueError):
        stats.variance()


def test_min_max(sample_data):
    stats = Statistics(sample_data)
    assert stats.min_max() == (10, 50)


def test_count_above(sample_data):
    stats = Statistics(sample_data)
    assert stats.count_above(25) == 3


def test_normalize(sample_data):
    stats = Statistics(sample_data)
    result = stats.normalize()
    assert result == [0.0, 0.25, 0.5, 0.75, 1.0]


@pytest.mark.parametrize(
    "data, threshold, expected_count",
    [
        ([10, 20, 30], 15, 2),
        ([5, 5, 5], 5, 0),  
        ([100, 200, 300], 150, 2),
        ([1, 2, 3, 4, 5], 0, 5), 
    ],
)
def test_count_above_parametrized(data, threshold, expected_count):
    stats = Statistics(data)
    assert stats.count_above(threshold) == expected_count


@pytest.mark.parametrize(
    "data, expected_normalized",
    [
        ([10, 20, 30], [0.0, 0.5, 1.0]),         
        ([1, 1, 1], None),                       
        ([100, 50, 0], [1.0, 0.5, 0.0]),        
        ([0, 10, 20], [0.0, 0.5, 1.0]),          
        ([-10, 0, 10], [0.0, 0.5, 1.0]),         
    ],
)
def test_normalize_parametrized(data, expected_normalized):
    stats = Statistics(data)
    if expected_normalized is None:
        with pytest.raises(ValueError):
            stats.normalize()
    else:
        assert stats.normalize() == expected_normalized
