import logging
from datetime import datetime

import Levenshtein
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import logging
import Levenshtein


def get_driver() -> webdriver.Chrome:
    """
    Get a configured Chrome WebDriver instance.

    :return: Configured WebDriver instance for Chrome.
    """
    try:
        logging.debug('Getting Chrome WebDriver instance...')
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.binary_location = "/usr/bin/chromium"
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_driver = webdriver.Chrome(
            service=Service(
                "/usr/bin/chromedriver",
                service_args=["--verbose"],
                log_output="/dev/stderr",
            ),
            options=chrome_options,
        )
        chrome_driver.delete_all_cookies()

        logging.debug("WebDriver initialized successfully.")
        return chrome_driver
    except Exception as ex:
        logging.error(f"Failed to initialize WebDriver: {ex}")
        raise ex


def calculate_similarity(str1: str, str2: str, threshold: float = 65) -> float:
    """
    Calculate whether the similarity percentage between two strings exceeds a given threshold
    using Levenshtein distance.

    :param str1: The first string.
    :param str2: The second string.
    :param threshold: The minimum similarity percentage (as a float between 0 and 1) required to consider the strings similar.
    :return: True if the similarity exceeds the threshold, otherwise False.
    """
    try:
        logging.debug(f"Calculating Similarity between strings {str1} and {str2}...")
        # Compute Levenshtein distance
        distance = Levenshtein.distance(str1, str2)

        # Normalized distance
        max_len = max(len(str1), len(str2))
        similarity = (1 - distance / max_len) * 100

        logging.debug(f"Similarity between {str1}&{str2} computed: {similarity:.2f}%. Return: {similarity > threshold}")

        return similarity > threshold
    except Exception as ex:
        logging.error(f"Failed to calculate similarity: {ex}")
        raise ex


def get_match_datetime(match_date_str: str, season: str = None) -> datetime:
    """
    Converts a match date string and season into a datetime object.

    Args:
        match_date_str (str): The date of the match as a string (e.g., '26.05. 20:45' or '22.12.2024 17:30').
        season (str): The season as a string (e.g., '2023/2024').

    Returns:
        datetime: The datetime object representing the match date and time.
    """
    try:
        # Attempt to parse the full datetime string (e.g., '22.12.2024 17:30')
        return datetime.strptime(match_date_str, "%d.%m.%Y %H:%M")
    except ValueError:
        # Parse the season years
        start_year, end_year = map(int, season.split('/'))
        # If parsing fails, handle the shorter format (e.g., '26.05. 20:30')
        day, month, time = match_date_str.split('.')
        day = int(day.strip())
        month = int(month.strip())
        time = time.strip()

        # Determine the year based on the month
        year = end_year if month >= 6 else start_year

        # Combine into a datetime object
        return datetime.strptime(f"{day}.{month}.{year} {time}", "%d.%m.%Y %H:%M")
