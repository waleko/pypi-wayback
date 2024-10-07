from argparse import ArgumentParser
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from flask import Flask, Response

app = Flask(__name__)
INDEX_URL = "https://pypi.org/simple/"


def get_allowed_files(package_name: str, cutoff_date: datetime) -> list[str]:
    """Get the latest version of a package before the cutoff date using PyPI's JSON API."""
    response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
    package_data = response.json()
    releases = package_data["releases"]

    allowed_files = []

    # Loop through all versions and find the latest one before the cutoff date
    for uploads in releases.values():
        for upload in uploads:
            release_date = datetime.strptime(upload["upload_time"][:10], "%Y-%m-%d")
            if release_date <= cutoff_date:
                allowed_files.append(upload["filename"])

    return allowed_files


def filter_html(package_name: str, allowed_versions: list[str]) -> str:
    """Filter the HTML page to include only up to the latest version."""
    response = requests.get(f"{INDEX_URL}{package_name}/")
    soup = BeautifulSoup(response.text, "html.parser")

    result_html = f"<h1>Links for {package_name}</h1>\n"
    for anchor in soup.find_all("a"):
        filename = anchor.text
        if filename in allowed_versions:
            result_html += str(anchor) + "<br />\n"

    soup.body.replace_with(BeautifulSoup(result_html, "html.parser"))
    res: str = soup.prettify(encoding=None)
    return res


@app.route("/<date_string>/<package_name>/")
def proxy_pypi_with_cutoff(package_name: str, date_string: str) -> Response:
    try:
        cutoff_date = datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError:
        return Response("Invalid date format. Use YYYY-MM-DD.", status=400)

    allowed_files = get_allowed_files(package_name, cutoff_date)
    if not allowed_files:
        return Response("No valid versions found before the cutoff date.", status=404)

    filtered_html = filter_html(package_name, allowed_files)
    return Response(filtered_html, mimetype="text/html")


@app.route("/<package_name>/")
def pass_through_pypi(package_name: str) -> Response:
    response = requests.get(f"https://pypi.org/simple/{package_name}/")
    return Response(response.text, mimetype="text/html")


@app.route("/")
def index() -> str:
    return """PyPI Wayback Machine<br>
    Usage:<br>
    - /{package_name}/: Pass through the PyPI index for the package<br>
    - /{date_string}/{package_name}/: Filter the PyPI index for the package to include only versions before the date<br>
    Example:<br>
    - /requests/: Pass through the PyPI index for the requests package<br>
    - /2021-01-01/requests/: Filter the PyPI index for the requests
    package to include only versions before 2021-01-01<br>
    """


if __name__ == "__main__":
    parser = ArgumentParser("PyPI Wayback Machine")
    parser.add_argument("--host", type=str, default="localhost", help="Host to run the server on")
    parser.add_argument("--port", type=int, default=8080, help="Port to run the server on")
    parser.add_argument(
        "--index-url",
        type=str,
        default="https://pypi.org/simple/",
        help="PyPI index URL",
    )
    args = parser.parse_args()
    INDEX_URL = args.index_url
    app.run(host=args.host, port=args.port)
