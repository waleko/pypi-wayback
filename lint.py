import subprocess
import sys


def run_command(command: str) -> None:
    """Run a shell command and handle errors."""
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        sys.exit(result.returncode)


def main() -> None:
    run_command("black --check .")
    run_command("isort --profile=black --check .")
    # run_command("flake8 . --max-line-length=120")
    run_command("ruff check .")
    run_command("mypy .")


if __name__ == "__main__":
    main()
