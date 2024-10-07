# PyPI Wayback Machine

[![PyPI - Version](https://img.shields.io/pypi/v/pypi-wayback)](https://pypi.org/project/pypi-wayback)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pypi-wayback)](https://pypi.org/project/pypi-wayback)
![Python Version](https://img.shields.io/badge/python-3.10-blue)
[![License](https://img.shields.io/github/license/waleko/pypi-wayback)](https://github.com/waleko/pypi-wayback/blob/main/LICENSE)
[![Build Status](https://img.shields.io/github/actions/workflow/status/waleko/pypi-wayback/main.yaml)](https://github.com/<your-repo>/actions)

---

**PyPI Wayback Machine** is a modern and simple tool to retrieve historical PyPI pages of any package at a specific date — think of it as a next-gen version of `pypi-timemachine` but with added flexibility. Whether you're tracking down a past release or examining dependency changes, this tool has you covered.

## 🚀 Features

- **Access PyPI pages at any past date**
- **Dockerized for quick setup** 
- **Lightweight and performant**

## 📦 Installation & Usage

### Docker
Quickly start the server using Docker:
```bash
docker run -p 8080:8080 ghcr.io/waleko/pypi-wayback
```

### Python
Alternatively, you can run it directly using Python:
```bash
pip install pypi-wayback
python -m pypi_wayback --port 8080
```

### Accessing a Package's Historical Page

Once the server is running, access the PyPI page of a package by navigating to the following URL:
```
http://localhost:8080/<date>/<package_name>
```

For example, to view the PyPI page for the `requests` package on **January 1, 2020**:
```
http://localhost:8080/2020-01-01/requests
```

## 🤝 Contributing
Feel free to open issues or pull requests if you want to help improve this project. Contributions are more than welcome!

## ⚖️ License
This project is licensed under the MIT License.
