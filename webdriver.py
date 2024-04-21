from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

project_titles=[]
chrome_options = Options()
service = Service('./chromedriver') 
driver = webdriver.Chrome(service=service, options=chrome_options)

# Open the website
driver.get("https://www.educative.io/projects")

# Function to scrape and print collection titles
def scrape_collection_titles():
    collection_titles = driver.find_elements(By.XPATH, '//p[@class="heading-five webkit-line-clamp-2 m-1"]')
    for title in collection_titles:
        project_titles.append(title.text)

# Scroll to the bottom of the page to load more content
def scroll_to_bottom():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

# Find and click the "Show More" button
def click_show_more():
    wait = WebDriverWait(driver, 10)
    show_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@class="outlined-default mx-3 mt-6 w-40 gap-2.5 px-3 py-2.5 text-black sm:w-72"]')))    
    ActionChains(driver).move_to_element(show_more_button).click().perform()

# Scrape initial content
scrape_collection_titles()

while True:
    try:
        click_show_more()
        time.sleep(2)  # Wait for new content to load
        scrape_collection_titles()
    except Exception :
        print("No more 'Show More' button found.")
        break

driver.quit()

with open("project_titles.txt", "w") as f:
    for title in project_titles:
        f.write(title + "\n")

print("Project titles saved to project_titles.txt file.")