import time
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from dotenv import dotenv_values

# get variables from .env file
env_vars = dotenv_values('.env')
email_address = env_vars['EMAIL_ADDRESS']
password = env_vars['PASSWORD']
notion_first_page_link = env_vars['NOTION_FIRST_PAGE_LINK']

driver = uc.Chrome()

def login_into_notion_and_return_page_data():
    try:
        try:
            driver.get(notion_first_page_link)
            time.sleep(5)
        except Exception as e:
            print("There is an exceptio opening the url....",e)
        # Locate Continue with Google button
        google_button = driver.find_element(By.XPATH, "//div[contains(text(),'Continue with Google')]")
        google_button.click()
        print("Locate Continue with Google button")
        # Now as Email is asking in new window so window switching is required.
        driver.switch_to.window(driver.window_handles[1])
        email_input = driver.find_element(By.XPATH, "//input[@type='email']")
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

All_page_links = []

def get_all_links(all_link_divs):
    for div_data in all_link_divs:
        try:
            All_page_links.append(div_data.find('a').get('href'))
        except Exception as e:
            print("There is some exception in find the a tag href",e)


def download_all_pages():
    for page_count,page in enumerate(All_page_links,1):
        # Navigate to the webpage
        print(f"current page is {page_count} and Now we going to download https://www.notion.so{page}")
        driver.get(f"https://www.notion.so{page}")
        if page_count == 1:
            try:
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'notion-topbar-more-button')))
                driver.find_element(By.CLASS_NAME, 'notion-topbar-more-button').click()
                time.sleep(5)
                driver.find_element(By.XPATH, "//div[text()='Export']").click()
                time.sleep(5)
                driver.find_element(By.XPATH, "//div[text()='Markdown & CSV']").click()
                time.sleep(5)
                driver.find_element(By.XPATH, "//div[text()='PDF']").click()
                time.sleep(5)
                driver.find_element(By.XPATH, "//div[text()='Current view']").click()
                time.sleep(5)
                driver.find_elements(By.XPATH, "//div[text()='Everything']")[1].click()
                time.sleep(5)
                driver.find_element(By.XPATH, "//div[text()='Export']").click()
                time.sleep(15)
            except Exception as e:
                print(f"There is some exception on if block on page no {page_count} Exception is {e}")
        else:
            try:
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'notion-topbar-more-button')))
                driver.find_element(By.CLASS_NAME, 'notion-topbar-more-button').click()
                time.sleep(5)
                driver.find_element(By.XPATH, "//div[text()='Export']").click()
                time.sleep(5)

                try:
                    driver.find_element(By.XPATH, "//div[text()='Markdown & CSV']").click()
                    time.sleep(5)
                    driver.find_element(By.XPATH, "//div[text()='PDF']").click()
                except:
                    driver.find_element(By.XPATH, "//div[text()='Current view']").click()
                    time.sleep(5)
                    driver.find_elements(By.XPATH, "//div[text()='Everything']")[1].click()
                time.sleep(7)
                driver.find_element(By.XPATH, "//div[text()='Export']").click()
                time.sleep(15)
            except Exception as e:
                print(f"There is some exception on else block page no {page_count} Exception is {e}")
    else:
        print("Complete Scrapping is Done now you can close the program")

page_data = login_into_notion_and_return_page_data()
soup = BeautifulSoup(page_data, 'html.parser')
all_link_divs = soup.find_all("div", class_="notion-selectable notion-page-block")

print("------------------------now we are going to get all link divs--------------------------------")
get_all_links(all_link_divs)


print(f"we have total {len(All_page_links)} no of pages.")
print("\n Bleow All links need to be scrapped")
for link in All_page_links:
    print(link)

print("--------------------- --Now we going to download All PDFs-------------------------------------")
download_all_pages()

driver.implicitly_wait(20)

# Close the browser
driver.quit()
