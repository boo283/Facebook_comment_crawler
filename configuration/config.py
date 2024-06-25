from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By



def login_facebook(username, password, driver):
    '''Log in to Facebook'''

    try:
        # Wait 10s until the login form is loaded
        username_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "email")))
        username_field.send_keys(username)

        password_field = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "pass")))
        password_field.send_keys(password)

        # Submit log in form 
        password_field.send_keys(Keys.RETURN)

    except Exception as e:
        print("Logged in failed. \n")

    finally:
        print("Logged in successfully")
        
def configure_driver():
    '''Configure the webdriver'''

    #Configurations
    webdriver_path = "C:\\Program Files\\Scrapper1\\chromedriver.exe" #your webdriver path (chromedriver.exe)

    chrome_options = Options()

    # Turn off Chrome notification and set language to English
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})

    # Start the service
    service = Service(webdriver_path)

    # Start the driver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver


def set_up_driver(url, service):
    '''Set up the driver and get url'''
    driver = configure_driver()

    # get url
    driver.get(url)
    return driver

