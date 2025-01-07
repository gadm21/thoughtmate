
# Define the URL and login credentials
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os 



from globals import FB_email, FB_password, G_email, G_password


def login_to_printify():
    # Set up the web driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    # Define the URL and Google login credentials
    login_url = 'https://printify.com/app/auth/login'  # replace with the actual login URL
    google_username = G_email  # replace with your Google username
    google_password = G_password  # replace with your Google password

    try:
        # Open the login page
        driver.get(login_url)
        # time.sleep(2)  # wait for the page to load
        print("logining in")
        # Locate all iframes on the page and switch to the one containing the Google Sign-In button
        iframes = driver.find_elements(By.TAG_NAME, 'iframe')
        for iframe in iframes:
            driver.switch_to.frame(iframe)
            try:
                # Try to find the Google Sign-In button
                google_sign_in_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "Continue with Google")]/ancestor::div[@role="button"]'))
                )
                google_sign_in_button.click()
                break
            except Exception as e:
                # If not found, switch back to the default content and continue
                driver.switch_to.default_content()
                continue
        else:
            raise Exception("Google Sign-In button not found")
        print("Clicked the Google Sign-In button")

        # # Switch to the Google login window
        original_window = driver.current_window_handle
        for handle in driver.window_handles:
            if handle != original_window:
                driver.switch_to.window(handle)
                break

        # Enter Google username
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'identifierId'))
        )
        email_input.send_keys(google_username)
        
        # Click the Next button
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button/span[text()="Next"]/parent::button'))
        )
        next_button.click()

        # Wait for the password field to be present
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'Passwd'))
        )
        password_input.send_keys(google_password)
        time.sleep(5)  # wait for the new window to appear
        password_input.send_keys(Keys.ENTER)

        # Switch back to the original window after login
        WebDriverWait(driver, 10).until(EC.url_changes(login_url))
        driver.switch_to.window(original_window)
        time.sleep(5)  # wait for the new window to appear
    except Exception as e:
        print(f"An error occurred: {e}")





def post_on_facebook(post = None, file_paths = None):

    # Set up ChromeDriver with options to disable notifications
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-notifications")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Open Facebook
    driver.get('https://www.facebook.com')

    # Log in to Facebook
    email = driver.find_element(By.ID, 'email')
    email.send_keys(FB_email)
    password = driver.find_element(By.ID, 'pass')
    password.send_keys(FB_password)

    login = driver.find_element(By.NAME, 'login')
    login.click()

    # Wait for the homepage to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[aria-label="Create a post"]')))

    # Find the post area and click to activate it
    post_area = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@role="button" and .//span[contains(text(), "What\'s on your mind")]]')))
    post_area.click()
    print("Selected post area")
    # time.sleep(5)

    if post:
        # Wait for the active post area to appear and click the text box
        text_box = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(@aria-label, "on your mind")]')))
        text_box.click()
        # Write the post
        text_box.send_keys(post)
        # Find and click the "Photo/video" button to open the file dialog
        photo_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Photo/video"]')))
        photo_button.click()

    if file_paths:
        absolute_file_paths = [os.path.abspath(file_path) for file_path in file_paths]
        # # Find the file input element and upload the image
        file_input = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@type="file" and @accept="image/*,image/heif,image/heic,video/*,video/mp4,video/x-m4v,video/x-matroska,.mkv"]')))
        file_input.send_keys("\n".join(absolute_file_paths))
        print("Post written")

        time.sleep(2)

        # Click the Next button
        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Next"]')))
        next_button.click()


    #______________________________________________________
    #______________________________________________________
    #______________________________________________________


    post_on_profile = False 

    if not post_on_profile: # post on page
        # Unselect the checkbox for "Gad Gad"
        gad_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@role="checkbox"]//span[text()="Gad Gad"]/ancestor::div[@role="checkbox"]')))
        if gad_checkbox.get_attribute('aria-checked') == 'true':
            gad_checkbox.click()

        # Select the checkbox for "Rock and Balloon"
        rock_checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@role="checkbox"]//span[text()="Rock and Balloon"]/ancestor::div[@role="checkbox"]')))
        if rock_checkbox.get_attribute('aria-checked') == 'false':
            rock_checkbox.click()

    # Click the Post button
    post_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@aria-label="Post"]')))
    post_button.click()

    # Wait for the post to be submitted
    time.sleep(5)

    # Close the driver
    driver.quit()
