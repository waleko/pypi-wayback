import pytest

# Import the Flask app instance and functions to test
from pypi_wayback import app


@pytest.fixture
def client():
    """Fixture to create a test client for the Flask app."""
    app.config['TESTING'] = True  # Set the app in testing mode
    with app.test_client() as client:
        yield client


def test_index_route(client):
    """Test the index route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'PyPI Wayback Machine' in response.data


def test_pass_through_pypi(client):
    """Test pass-through PyPI route to ensure it returns content."""
    response = client.get('/requests/')
    assert response.status_code == 200
    assert b'requests' in response.data


def test_proxy_pypi_with_cutoff(client):
    """Test filtering PyPI packages by cutoff date."""
    # Here we set a known valid package and a valid cutoff date
    package_name = 'requests'
    cutoff_date = '2021-01-01'

    # Make the request with a valid date and package
    response = client.get(f'/{cutoff_date}/{package_name}/')

    assert response.status_code == 200
    assert b'requests' in response.data

# List of test cases with package name, cutoff (could be date or version), and version to check
test_cases = [
    ("mypy-extensions", "2023-12-01", "1.0.0"),
    ("setuptools", "2024-01-05", "40.8.0"),
    ("packaging", "2024-01-05", "20.0"),
    ("azure-mgmt-batchai", "2023-11-07", "7.0.0b1"),
    ("regex", "2024-01-10", "2013-02-16"),
    ("pbr", "2023-12-24", "2.0.0"),
    ("duckdb", "2023-12-29", "0.9.1")
]


# Parametrized test using pytest
@pytest.mark.parametrize("package, cutoff, version", test_cases)
def test_version_availability(client, package, cutoff, version):
    """Test that the version is available in the filtered HTML."""
    response = client.get(f'/{cutoff}/{package}/')
    assert response.status_code == 200
    assert version in response.text
