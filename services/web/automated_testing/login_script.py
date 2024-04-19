from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Replace these with the actual login credentials and book details
username = "surya@gmail.com"
password = "hello123"
book_title = "Example Book Title"
book_author = "Example Author"
publication_date = "2023-01-01"
description = "An example book description."
language = "English"
num_pages = "300"
genre_id = "1"

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Function to log in
def login_to_site():
    driver.get("http://localhost:5173/login")
    driver.implicitly_wait(5)
    driver.find_element(By.XPATH, "//input[@type='email']").send_keys(username)
    driver.find_element(By.XPATH, "//input[@type='password']").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

# Function to add a book
def add_book():
    driver.implicitly_wait(5)
    driver.get("http://localhost:5001/add-book")
    driver.implicitly_wait(5)
    driver.find_element(By.NAME, "title").send_keys(book_title)
    driver.find_element(By.NAME, "authors").send_keys(book_author)
    driver.find_element(By.NAME, "publication_date").send_keys(publication_date)
    driver.find_element(By.NAME, "description").send_keys(description)
    driver.find_element(By.NAME, "language").send_keys(language)
    driver.find_element(By.NAME, "num_pages").send_keys(num_pages)
    driver.find_element(By.NAME, "genre_id").send_keys(genre_id)
    # Skipping file upload for cover_image
    driver.find_element(By.XPATH, "//button[contains(text(),'Submit')]").click()

# Log in to the site
login_to_site()
time.sleep(5)  # Wait for login to complete and session to start

# Add a book
add_book()
time.sleep(3)  # Wait for book addition to complete

# Close the browser
driver.quit()
