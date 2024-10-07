# PyPI Wayback Machine

Retrieve the PyPI page of a package at a specific date.

## Usage
Start the server with the following command:
```bash
python -m pypi_wayback_machine --port 8080
```

Access the pypi page of a package at a specific date by visiting the following URL:
```
http://localhost:8080/<date>/<package_name>
```

For example, to access the PyPI page of the package `requests` on the 1st of January 2020, visit:
```
http://localhost:8080/2020-01-01/requests
```
