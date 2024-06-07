import os
import sys
import pandas as pd

from datetime import datetime
from fake_headers import Headers
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    WebDriverException,
)

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

from webdriver_manager.firefox import GeckoDriverManager

TWITTER_LOGIN_URL = "https://twitter.com/i/flow/login"


mail = ""
username = ""
password = ""
path = ""
tweet_ids = set()
data = []
tweet_cards = []


# Driver


def _get_driver():
    header = Headers().generate()["User-Agent"]

    # browser_option = ChromeOptions()
    browser_option = FirefoxOptions()
    browser_option.add_argument("--no-sandbox")
    browser_option.add_argument("--disable-dev-shm-usage")
    browser_option.add_argument("--ignore-certificate-errors")
    browser_option.add_argument("--disable-gpu")
    browser_option.add_argument("--log-level=3")
    browser_option.add_argument("--disable-notifications")
    browser_option.add_argument("--disable-popup-blocking")
    browser_option.add_argument("--user-agent={}".format(header))

    # For Hiding Browser
    browser_option.add_argument("--headless")

    try:
        driver = webdriver.Firefox(
            options=browser_option,
        )
        return driver
    except WebDriverException:
        try:
            print("Downloading FirefoxDriver...")
            firefoxdriver_path = GeckoDriverManager().install()
            firefox_service = FirefoxService(executable_path=firefoxdriver_path)

            print("Initializing FirefoxDriver...")
            driver = webdriver.Firefox(
                service=firefox_service,
                options=browser_option,
            )

            return driver
        except Exception as e:
            print(f"Error setting up WebDriver: {e}")
            sys.exit(1)


driver = _get_driver()

###


def _input_username():
    input_attempt = 0

    while True:
        try:
            username_input = driver.find_element(
                "xpath", "//input[@autocomplete='username']"
            )

            username_input.send_keys(mail)
            username_input.send_keys(Keys.RETURN)
            sleep(3)
            break
        except NoSuchElementException:
            input_attempt += 1
            if input_attempt >= 3:
                print()
                print(
                    """There was an error inputting the username.

It may be due to the following:
- Internet connection is unstable
- Username is incorrect
- Twitter is experiencing unusual activity"""
                )
                driver.quit()
                sys.exit(1)
            else:
                print("Re-attempting to input username...")
                sleep(2)


def _input_unusual_activity():
    input_attempt = 0

    while True:
        try:
            unusual_activity = driver.find_element(
                "xpath", "//input[@data-testid='ocfEnterTextTextInput']"
            )
            unusual_activity.send_keys(username)
            unusual_activity.send_keys(Keys.RETURN)
            sleep(3)
            break
        except NoSuchElementException:
            input_attempt += 1
            if input_attempt >= 3:
                break


def _input_password():
    input_attempt = 0

    while True:
        try:
            password_input = driver.find_element(
                "xpath", "//input[@autocomplete='current-password']"
            )

            password_input.send_keys(password)
            password_input.send_keys(Keys.RETURN)
            sleep(3)
            break
        except NoSuchElementException:
            input_attempt += 1
            if input_attempt >= 3:
                print()
                print(
                    """There was an error inputting the password.

It may be due to the following:
- Internet connection is unstable
- Password is incorrect
- Twitter is experiencing unusual activity"""
                )
                driver.quit()
                sys.exit(1)
            else:
                print("Re-attempting to input password...")
                sleep(2)
    

def login():
    print()
    print("Logging in to Twitter...")

    try:
        driver.maximize_window()
        driver.get(TWITTER_LOGIN_URL)
        sleep(5)  # TODO: should be a proper wait

        _input_username()
        _input_unusual_activity()
        _input_password()

        cookies = driver.get_cookies()

        auth_token = None

        for cookie in cookies:
            if cookie["name"] == "auth_token":
                auth_token = cookie["value"]
                break

        if auth_token is None:
            raise ValueError(
                """This may be due to the following:

- Internet connection is unstable
- Username is incorrect
- Password is incorrect
"""
            )

        print()
        print("Login Successful")
        print()
    except Exception as e:
        print()
        print(f"Login Failed: {e}")
        sys.exit(1)


def go_to_path():
    driver.get(f"https://twitter.com/{path}")
    sleep(3)


def get_tweet_cards():
    tweet_cards = driver.find_elements(
        "xpath", '//article[@data-testid="tweet" and not(@disabled)]'
    )
    
    return tweet_cards


def remove_hidden_cards():
    try:
        hidden_cards = driver.find_elements(
            "xpath", '//article[@data-testid="tweet" and @disabled]'
        )

        for card in hidden_cards[1:-2]:
            driver.execute_script(
                "arguments[0].parentNode.parentNode.parentNode.remove();", card
            )
    except Exception as e:
        return
    

def get_tweet(card):
    error = False

    try:
        handle = card.find_element(
            "xpath", './/span[contains(text(), "@")]'
        ).text
    except NoSuchElementException:
        error = True
        handle = "skip"

    try:
        date_time = card.find_element("xpath", ".//time").get_attribute(
            "datetime"
        )

        if date_time is not None:
            is_ad = False
    except NoSuchElementException:
        is_ad = True
        error = True
        date_time = "skip"

    if error:
        return

    content = ""
    contents = card.find_elements(
        "xpath",
        '(.//div[@data-testid="tweetText"])[1]/span | (.//div[@data-testid="tweetText"])[1]/a',
    )

    for c in contents:
        content += c.text

    return (
        handle,
        date_time,
        content,
        is_ad,
    )


def scrape_tweets():
    go_to_path()

    # Accept cookies to make the banner disappear
    try:
        accept_cookies_btn = driver.find_element(
        "xpath", "//span[text()='Refuse non-essential cookies']/../../..")
        accept_cookies_btn.click()
    except NoSuchElementException:
        pass

    refresh_count = 0
    added_tweets = 0
    empty_count = 0
    retry_cnt = 0

    while True:
        try:
            tweet_cards = get_tweet_cards()
            added_tweets = 0

            for card in tweet_cards[-15:]:
                try:
                    tweet_id = str(card)

                    if tweet_id not in tweet_ids:
                        tweet_ids.add(tweet_id)

                        driver.execute_script(
                            "arguments[0].scrollIntoView();", card
                        )

                        tweet = get_tweet(card)

                        if tweet:
                            if tweet is not None:
                                if not tweet[-1]:  # is_ad
                                    data.append(tweet)
                                    added_tweets += 1
                                else:
                                    continue
                            else:
                                continue
                        else:
                            continue
                    else:
                        continue
                except NoSuchElementException:
                    continue

            if added_tweets == 0:
                # Check if there is a button "Retry" and click on it with a regular basis until a certain amount of tries
                try:
                    while retry_cnt < 15:
                        retry_button = driver.find_element(
                        "xpath", "//span[text()='Retry']/../../..")
                        sleep(58)
                        retry_button.click()
                        retry_cnt += 1
                        sleep(2)
                # There is no Retry button so the counter is reseted
                except NoSuchElementException:
                    retry_cnt = 0

                if empty_count >= 5:
                    if refresh_count >= 3:
                        print()
                        print("No more tweets to scrape")
                        break
                    refresh_count += 1
                empty_count += 1
                sleep(1)
            else:
                empty_count = 0
                refresh_count = 0
        except StaleElementReferenceException:
            sleep(2)
            continue

    print("")


def save_to_csv():
    print("Saving Tweets to CSV...")
    now = datetime.now()
    folder_path = "./tweets/"

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print("Created Folder: {}".format(folder_path))

    csv_data = {
        "Handle": [tweet[0] for tweet in data],
        "Timestamp": [tweet[1] for tweet in data],
        "Content": [tweet[2] for tweet in data],
    }

    df = pd.DataFrame(csv_data)

    current_time = now.strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f"{folder_path}{current_time}_tweets.csv"
    pd.set_option("display.max_colwidth", None)
    df.to_csv(file_path, index=False, encoding="utf-8")

    print("CSV Saved: {}".format(file_path))


def main():
    login()
    scrape_tweets()
    save_to_csv()


if __name__ == "__main__":
    main()