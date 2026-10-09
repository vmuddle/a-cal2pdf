# tests for cal2pdf.py

from typing import Literal

import cal2pdf
import pytest
import os
import datetime


@pytest.fixture
def sample_cal_data():
    """Sample output from the 'cal' command for October 2024."""
    return "   October 2024\nSu Mo Tu We Th Fr Sa\n       1  2  3  4  5\n 6  7  8  9 10 11 12\n13 14 15 16 17 18 19\n20 21 22 23 24 25 26\n27 28 29 30 31"


@pytest.fixture
def sample_month_map():
    return {
        "header": "   October 2024",
        "weekdays": "Su Mo Tu We Th Fr Sa",
        "date_1": "       1  2  3  4  5",
        "date_2": " 6  7  8  9 10 11 12",
        "date_3": "13 14 15 16 17 18 19",
        "date_4": "20 21 22 23 24 25 26",
        "date_5": "27 28 29 30 31",
    }


@pytest.mark.parametrize(
    "inputs, expected",
    [
        ((10, 2024), "cal_10_2024.pdf"),
        ((1, 2024), "cal_01_2024.pdf"),
        (
            (13, 2024),
            "cal_13_2024.pdf",
        ),  # Invalid month, but still tests filename generation
    ],
)
def test_cal2pdf_get_filename(
    inputs: tuple[int, int],
    expected: Literal["cal_10_2024.pdf"]
    | Literal["cal_01_2024.pdf"]
    | Literal["cal_13_2024.pdf"],
):
    filename = cal2pdf.get_filename(*inputs)
    print(f"Test get_filename: {filename}")
    assert filename == expected, f"Expected '{expected}', but got '{filename}'"


def test_cal2pdf_run_cal_command():
    month = 10
    year = 2024
    output = cal2pdf.run_cal_command(month, year)
    print(f"Test run_cal_command output:\n{output}")
    assert "October" in output, "Expected 'October' in the output"
    assert str(year) in output, f"Expected '{year}' in the output"


def test_cal2pdf_parse_cal_output(sample_cal_data: LiteralString):
    calendar_data = cal2pdf.parse_cal_output(sample_cal_data)
    print(f"Test parse_cal_output calendar_data: {calendar_data}")
    assert calendar_data["header"] == "   October 2024", "Header line mismatch"
    assert calendar_data["weekdays"] == "Su Mo Tu We Th Fr Sa", "Weekdays line mismatch"
    assert calendar_data["date_1"] == "       1  2  3  4  5", "Date line mismatch"


def test_cal2pdf_main_functionality(monkeypatch: pytest.MonkeyPatch):
    # Mock the command line arguments
    monkeypatch.setattr("sys.argv", ["cal2pdf.py", "--month", "10", "--year", "2024"])

    # Run the main function
    cal2pdf.main()

    # Check if the PDF file was created
    expected_filename = cal2pdf.get_filename(10, 2024)
    assert os.path.exists(
        expected_filename
    ), f"Expected PDF file '{expected_filename}' to be created"

    # Clean up the generated PDF file after test
    os.remove(expected_filename)


def test_cal2pdf_main_functionality_default(monkeypatch: pytest.MonkeyPatch):
    # Mock the command line arguments without month and year
    monkeypatch.setattr("sys.argv", ["cal2pdf.py"])

    # Run the main function
    cal2pdf.main()

    # Get current month and year
    now = datetime.datetime.now()
    expected_filename = cal2pdf.get_filename(now.month, now.year)

    # Check if the PDF file was created
    assert os.path.exists(
        expected_filename
    ), f"Expected PDF file '{expected_filename}' to be created"

    # Clean up the generated PDF file after test
    os.remove(expected_filename)


def test_cal2pdf_main_functionality_invalid_month(monkeypatch: pytest.MonkeyPatch):
    # Mock the command line arguments with an invalid month
    monkeypatch.setattr("sys.argv", ["cal2pdf.py", "--month", "13", "--year", "2024"])

    # Run the main function and expect it to exit with an error
    with pytest.raises(SystemExit) as e:
        cal2pdf.main()

    assert e.type == SystemExit
    assert e.value.code == 1, "Expected exit code 1 for invalid month"


def test_cal2pdf_main_functionality_invalid_year(monkeypatch: pytest.MonkeyPatch):
    # Mock the command line arguments with an invalid year
    monkeypatch.setattr("sys.argv", ["cal2pdf.py", "--month", "10", "--year", "-2024"])

    # Run the main function and expect it to exit with an error
    with pytest.raises(SystemExit) as e:
        cal2pdf.main()

    assert e.type == SystemExit
    assert e.value.code == 1, "Expected exit code 1 for invalid year"


def test_cal2pdf_main_functionality_invalid_month_and_year(
    monkeypatch: pytest.MonkeyPatch,
):
    # Mock the command line arguments with an invalid month and year
    monkeypatch.setattr("sys.argv", ["cal2pdf.py", "--month", "0", "--year", "-2024"])

    # Run the main function and expect it to exit with an error
    with pytest.raises(SystemExit) as e:
        cal2pdf.main()

    assert e.type == SystemExit
    assert e.value.code == 1, "Expected exit code 1 for invalid month and year"


def test_cal2pdf_main_functionality_invalid_month_and_year_2(
    monkeypatch: pytest.MonkeyPatch,
):
    # Mock the command line arguments with an invalid month and year
    monkeypatch.setattr("sys.argv", ["cal2pdf.py", "--month", "15", "--year", "0"])

    # Run the main function and expect it to exit with an error
    with pytest.raises(SystemExit) as e:
        cal2pdf.main()

    assert e.type == SystemExit
    assert e.value.code == 1, "Expected exit code 1 for invalid month and year"


def test_cal2pdf_main_functionality_invalid_month_and_year_3(
    monkeypatch: pytest.MonkeyPatch,
):
    # Mock the command line arguments with an invalid month and year
    monkeypatch.setattr("sys.argv", ["cal2pdf.py", "--month", "-1", "--year", "2024"])

    # Run the main function and expect it to exit with an error
    with pytest.raises(SystemExit) as e:
        cal2pdf.main()

    assert e.type == SystemExit
    assert e.value.code == 1, "Expected exit code 1 for invalid month and year"


def test_cal2pdf_main_functionality_invalid_month_and_year_4(
    monkeypatch: pytest.MonkeyPatch,
):
    # Mock the command line arguments with an invalid month and year
    monkeypatch.setattr("sys.argv", ["cal2pdf.py", "--month", "10", "--year", "-1"])

    # Run the main function and expect it to exit with an error
    with pytest.raises(SystemExit) as e:
        cal2pdf.main()

    assert e.type == SystemExit
    assert e.value.code == 1, "Expected exit code 1 for invalid month and year"


def test_cal2pdf_main_functionality_invalid_month_and_year_5(
    monkeypatch: pytest.MonkeyPatch,
):
    # Mock the command line arguments with an invalid month and year
    monkeypatch.setattr("sys.argv", ["cal2pdf.py", "--month", "0", "--year", "0"])

    # Run the main function and expect it to exit with an error
    with pytest.raises(SystemExit) as e:
        cal2pdf.main()

    assert e.type == SystemExit
    assert e.value.code == 1, "Expected exit code 1 for invalid month and year"


def test_cal2pdf_main_functionality_invalid_month_and_year_6(
    monkeypatch: pytest.MonkeyPatch,
):
    # Mock the command line arguments with an invalid month and year
    monkeypatch.setattr("sys.argv", ["cal2pdf.py", "--month", "13", "--year", "-1"])

    # Run the main function and expect it to exit with an error
    with pytest.raises(SystemExit) as e:
        cal2pdf.main()

    assert e.type == SystemExit
    assert e.value.code == 1, "Expected exit code 1 for invalid month and year"


def test_cal2pdf_main_functionality_invalid_month_and_year_7(
    monkeypatch: pytest.MonkeyPatch,
):
    # Mock the command line arguments with an invalid month and year
    monkeypatch.setattr("sys.argv", ["cal2pdf.py", "--month", "-5", "--year", "0"])

    # Run the main function and expect it to exit with an error
    with pytest.raises(SystemExit) as e:
        cal2pdf.main()

    assert e.type == SystemExit
    assert e.value.code == 1, "Expected exit code 1 for invalid month and year"


def test_cal2pdf_get_days_of_week_list(sample_month_map: dict[str, str]):
    days_list = cal2pdf.get_days_of_week_list(sample_month_map)
    print(f"Test get_days_of_week_list: {days_list}")
    assert days_list == [
        "Su",
        "Mo",
        "Tu",
        "We",
        "Th",
        "Fr",
        "Sa",
    ], "Days of week list mismatch"


def test_cal2pdf_get_day_number_list():
    numbers = "       1  2  3  4  5"
    number_list = cal2pdf.get_day_number_list(numbers)
    print(f"Test get_day_number_list: {number_list}")
    assert number_list == ["", "", "1", "2", "3", "4", "5"], "Day number list mismatch"
