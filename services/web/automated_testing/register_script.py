from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# User details for registration
email = "newuser@example.com"
first_name = "New"
last_name = "User"
password = "newpassword123"

# Initialize the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open the registration page
driver.get("http://localhost:5000/register")  # Replace with the correct URL

# Fill in the registration form
driver.find_element(By.NAME, "email").send_keys(email)
driver.find_element(By.NAME, "first_name").send_keys(first_name)
driver.find_element(By.NAME, "last_name").send_keys(last_name)
driver.find_element(By.NAME, "password").send_keys(password)

# Submit the registration form
driver.find_element(By.XPATH, "//button[contains(text(),'Register')]").click()

# Check for success message (this depends on how your application displays success messages)
success_message = driver.find_element(By.CLASS_NAME, "success").text
assert "User created successfully!" in success_message

# Close the browser
driver.quit()
