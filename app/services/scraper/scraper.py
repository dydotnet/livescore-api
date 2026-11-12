import logging
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from app.services.utils import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from config import TIMEOUT, URL_LIVESPORT, SIMULATE_WAITING_HUMAN_BEING

XPATH_FOOTBALL_BUTTON = "/html/body/nav/div/div[1]/a[1]"

class Scraper:
    """
    A web scraper class to interact with web pages using Selenium WebDriver.

    Attributes:
        driver: The Selenium WebDriver instance used for browsing and interacting with web pages.
    """
    def __init__(self, url: str = None) -> None:
        """
        Initializes the Scraper class with a Selenium WebDriver instance.

        Args:
            url (str, optional): The URL of the web page to navigate to. Defaults to `URL_LIVESPORT`.
        """
        self.driver = get_driver()
        self.wait = WebDriverWait(self.driver, timeout=TIMEOUT)
        self.temporary_wait = WebDriverWait(self.driver, timeout=10)

        self.driver.get(url or URL_LIVESPORT)


     def get_page(self, url: str) -> None:
        """
        Navigates the WebDriver to the specified URL.

        Args:
            url (str): The URL of the web page to navigate to.
        """
        logging.debug(f"Navigating to {url}")
        self.driver.get(url)
        logging.debug(f"Page navigated: {self.driver.current_url}")


    def wait_an_element(self, xpath: str, temporary: bool = False) -> None:
        """
        Waits for an element to become visible based on the specified XPath.

        Args:
            xpath (str): The XPath of the element to wait for.
            temporary (bool, optional): Whether to use a temporary wait time. Defaults to False.
        """
        logging.debug(f"Waiting for {xpath}")
        if temporary:
            self.temporary_wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        else:
            self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
        logging.debug(f"Element {xpath} is visible")


    def find_element(self, xpath: str, element: WebElement = None, temporary: bool = False) -> WebElement:
        """
        Finds and returns a web element based on the given XPath.

        Args:
            xpath (str): The XPath of the element to locate.
            element (WebElement, optional): A parent web element to search within. Defaults to None.
            temporary (bool, optional): Whether to use a temporary wait time. Defaults to False.

        Returns:
            WebElement: The web element located using the specified XPath.
        """
        logging.debug(f"Finding {xpath}")

        if element is None:
            self.wait_an_element(xpath, temporary=temporary)
            element = self.driver.find_element(By.XPATH, xpath)
        else:
            element = element.find_element(By.XPATH, xpath)

        logging.debug(f"Element {xpath} found")
        return element


    def find_elements(self, xpath: str, element: WebElement = None) -> list[WebElement]:
        """
        Finds and returns a list of web elements based on the given XPath.

        Args:
            xpath (str): The XPath of the elements to locate.
            element (WebElement, optional): A parent web element to search within. Defaults to None.

        Returns:
            list[WebElement]: A list of web elements located using the specified XPath.
        """
        logging.debug(f"Finding elements {xpath}")

        if element is None:
            self.wait_an_element(f"{xpath}[1]")
            elements = self.driver.find_elements(By.XPATH, xpath)
        else:
            elements = element.find_elements(By.XPATH, xpath)
        logging.debug(f"Found {len(elements)} elements")
        return elements


    def execute_script(self, element: WebElement, script: str = 'click') -> None:
        """
        Executes a custom JavaScript script on a specified element.

        Args:
            element (WebElement): The web element on which to execute the script.
            script (str, optional): The JavaScript action to execute. Defaults to 'click'.
        """
        logging.debug(f"Executing {script}")

        # Simulate human-like behavior by adding a 5-second sleep
        sleep(SIMULATE_WAITING_HUMAN_BEING)

        if script == 'click':
            self.driver.execute_script("arguments[0].click();", element)
            logging.debug(f"Element {script} executed")


    def get_attribute(self, element: WebElement, attribute: str = 'href') -> str:
        """
        Retrieves the value of a specified attribute from a web element.

        Args:
            element (WebElement): The web element to retrieve the attribute value from.
            attribute (str, optional): The name of the attribute to retrieve. Defaults to 'href'.

        Returns:
            str: The value of the specified attribute.
        """
        logging.debug(f"Get attribute {attribute} from element {element}")
        value = element.get_attribute(attribute)
        logging.debug(f"Attribute value {value}")

        return value
