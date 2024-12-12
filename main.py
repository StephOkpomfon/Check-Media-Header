from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd
import requests
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.


def setup_driver_with_cookie_header(url, cookie_header):
    """
    Set up the WebDriver with cookies from a raw cookie header string.

    Args:
        url (str): The URL to load.
        cookie_header (str): The raw cookie header string (e.g., "name1=value1; name2=value2").

    Returns:
        WebDriver: The Selenium WebDriver instance.
    """
    driver = webdriver.Chrome()
    driver.get(url)

    # Parse and set cookies
    for cookie_entry in cookie_header.split(";"):
        cookie_parts = cookie_entry.split("=", 1)
        if len(cookie_parts) == 2:
            name = cookie_parts[0].strip()
            value = cookie_parts[1].strip()
            driver.add_cookie({"name": name, "value": value})

    driver.refresh()  # Reload the page to apply cookies
    return driver


def check_header(driver, header_xpath):
    """
    Check if a header element exists on the page using XPath.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        header_xpath (str): The XPath of the header element.
    """
    try:
        wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
        wait.until(EC.presence_of_element_located((By.XPATH, header_xpath)))
        print("Header found")
    except TimeoutException:
        print("No header found")


def main():
    url = f"https://{os.environ['UNICC_AUTH']
                     }@drupalandia.unhcr.info/nl/3072"
    header_xpath = "//header"  # Update the XPath to target the header you want
    file_location = "file.xlsx"
    # To select A and B

    # Insert excel file in this folder
    # I'm reading from just one column the one that has the links
    sheet = pd.read_excel(file_location, sheet_name="Task 28", usecols="G")
    # Ensure URLs start with http/https
    sheet = sheet[sheet.iloc[:, 0].str.startswith("http", na=False)]

    # Clean the DataFrame: drop NaN values and keep valid URLs
    sheet = sheet.dropna()  # Remove NaN rows
    # Loop through the URLs in column G
    # for url in sheet['G']:
    for url in sheet.iloc[:, 0]:  # This refers to the first column, i.e., 'G'
        try:
            # Check if the URL is valid by making an HTTP request
            response = requests.head(url, allow_redirects=True)

            if response.status_code == 200:  # URL is valid
                cookie_header = os.environ['COOKIE_CONSENT']
                driver = setup_driver_with_cookie_header(url, cookie_header)

                header_xpath = "//header"  # Update the XPath to target the header you want
                check_header(driver, header_xpath)

        except (requests.exceptions.RequestException, TimeoutException) as e:
            print(f"Skipping URL {url} due to error: {e}")
            continue  # Proceed to next URL
        finally:
            if 'driver' in locals():
                driver.quit()

    # driver = setup_driver_with_cookie_header(url, cookie_header)

    # try:
    #     check_header(driver, header_xpath)
    # except Exception as e:
    #     print(f"An error occurred: {e}")
    # finally:
    #     driver.quit()


if __name__ == "__main__":
    main()
    # Example raw cookie header string
