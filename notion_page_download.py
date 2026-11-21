import time, traceback
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from dotenv import dotenv_values


# get variables from .env file
env_vars = dotenv_values('.env')
email_address = env_vars['EMAIL_ADDRESS']
password = env_vars['PASSWORD']
notion_first_page_link = env_vars['NOTION_FIRST_PAGE_LINK']
chrome_version = int(env_vars['CHROME_VERSION'])

driver = uc.Chrome(version_main = chrome_version)

def login_into_notion_and_return_page_data():
    try:
        try:
            driver.get(notion_first_page_link)
            time.sleep(5)
        except Exception as e:
            print("There is an exceptio opening the url....",e)
            print(traceback.format_exc())
        # Locate Continue with Google button
        # google_button = driver.find_element(By.XPATH, "//div[contains(text(),'Continue with Google')]")
        google_button = driver.find_element(By.XPATH, "/html/body/div/div/div/div[1]/div/div[2]/div/div/div/main/section/div[2]/div[3]/div[1]/div[2]/div[1]")
        google_button.click()
        print("Located Continue with Google button and clicked on it.")

        # Now as Email is asking in new window so window switching is required.
        driver.switch_to.window(driver.window_handles[1])
        # email_input = driver.find_element(By.XPATH, "//input[@type='email']")
        email_input = driver.find_element(By.XPATH, "/html/body/div[2]/div[1]/div[1]/div[2]/c-wiz/main/div[2]/div/div/div[1]/span/section/div/div/div[1]/div[1]/div[1]/div/div[1]/input")
        email_input.send_keys(email_address)
        email_input.send_keys(Keys.RETURN)
        print("Email entered successfully..........")
        # wait for the element to become visible
        wait = WebDriverWait(driver, 10)
        password_input = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@type='password']")))
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        print("Password entered successfully..........")
        time.sleep(30)

        # Now we need to switch from small window to full width window
        driver.switch_to.window(driver.window_handles[0])
        return driver.page_source
    except Exception as e:
        print("there is an Exception in login_into_notion_and_return_page_data: ",e)
        print(traceback.format_exc())

All_page_links = []

def open_export_menu():
    wait = WebDriverWait(driver, 30)

    def click_visible_item(locator):
        element = wait.until(
            lambda _: next(
                (
                    candidate
                    for candidate in driver.find_elements(*locator)
                    if candidate.is_displayed()
                    and candidate.is_enabled()
                    and candidate.size["width"] > 0
                    and candidate.size["height"] > 0
                ),
                False,
            )
        )
        element.click()

    wait.until(
        EC.element_to_be_clickable((By.CLASS_NAME, 'notion-topbar-more-button'))
    ).click()
    click_visible_item(
        (
            By.XPATH,
            "//div[@role='option'][.//div[normalize-space()='More']]"
            "//div[normalize-space()='More']",
        )
    )
    click_visible_item((By.XPATH, "//div[normalize-space()='Export']"))


def navigate_to_page(url):
    for attempt in range(3):
        try:
            driver.get(url)
            return
        except WebDriverException as e:
            error_message = str(e).lower()
            is_transient_navigation_error = (
                "cannot determine loading status" in error_message
                or "target frame detached" in error_message
            )
            if not is_transient_navigation_error or attempt == 2:
                raise
            print(f"Navigation failed temporarily; retrying ({attempt + 1}/2): {e}")
            time.sleep(2)


def get_all_links(all_link_divs):
    for div_data in all_link_divs:
        try:
            All_page_links.append(div_data.find('a').get('href'))
        except Exception as e:
            print("There is some exception in find the a tag href",e)
            print(traceback.format_exc())


def download_all_pages():
    for page_count,page in enumerate(All_page_links,1):
        # Navigate to the webpage
        print(f"current page is {page_count} and Now we going to download https://www.notion.so{page}")
        try:
            navigate_to_page(f"https://www.notion.so{page}")
        except WebDriverException as e:
            print(f"Could not open page no {page_count} after retries: {e}")
            print(traceback.format_exc())
            continue
        if page_count == 1:
            try:
                open_export_menu()
                time.sleep(5)
                driver.find_element(By.XPATH, "//div[text()='Markdown & CSV']").click()
                time.sleep(5)
                driver.find_element(By.XPATH, "//div[text()='PDF']").click()
                time.sleep(5)
                driver.find_element(By.XPATH, "//div[text()='Current view']").click()
                time.sleep(5)
                driver.find_elements(By.XPATH, "//div[text()='Current view']")[-1].click()
                time.sleep(5)
                driver.find_element(By.XPATH, "//div[text()='Everything']").click()
                time.sleep(5)
                driver.find_elements(By.XPATH, "//div[text()='Everything']")[-1].click()
                time.sleep(5)
                driver.find_element(By.XPATH, "//div[text()='Export']").click()
                time.sleep(45)
            except Exception as e:
                print(f"There is some exception on if block on page no {page_count} Exception is {e}")
                print(traceback.format_exc())
        else:
            try:
                open_export_menu()
                time.sleep(5)

                try:
                    driver.find_element(By.XPATH, "//div[text()='Markdown & CSV']").click()
                    time.sleep(5)
                    driver.find_element(By.XPATH, "//div[text()='PDF']").click()
                except:
                    driver.find_element(By.XPATH, "//div[text()='Current view']").click()
                    time.sleep(5)
                    driver.find_elements(By.XPATH, "//div[text()='Current view']")[-1].click()
                    time.sleep(5)
                    driver.find_element(By.XPATH, "//div[text()='Everything']").click()
                    time.sleep(5)
                    driver.find_elements(By.XPATH, "//div[text()='Everything']")[-1].click()
                    time.sleep(5)
                driver.find_element(By.XPATH, "//div[text()='Export']").click()
                time.sleep(45)
            except Exception as e:
                print(f"There is some exception on else block page no {page_count} Exception is {e}")
                print(traceback.format_exc())
    else:
        print("Complete Scrapping is Done now you can close the program")

page_data = login_into_notion_and_return_page_data()
soup = BeautifulSoup(page_data, 'html.parser')
all_link_divs = soup.select('.notion-outliner-private-header-container .notion-selectable.notion-page-block, .notion-outliner-private-header .notion-selectable.notion-page-block')

print("------------------------now we are going to get all link divs--------------------------------")
get_all_links(all_link_divs)


print(f"we have total {len(All_page_links)} no of pages.")
print("\n Bleow All links need to be scrapped")
for link_count, link in enumerate(All_page_links,1):
    print(f"{link_count} ==> {link}")

print("--------------------- --Now we going to download All PDFs-------------------------------------")
download_all_pages()
driver.implicitly_wait(20)

# Close the browser
driver.quit()
