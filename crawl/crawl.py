import configuration
import pandas as pd
import numpy as np
import json

from selenium.webdriver.common.by import By

import time
from io import StringIO




def crawl(driver, url, username, password, threshold, ite):

    driver.get(url)
    # Login Facebook
    login_facebook(username, password, driver)
    scroll_and_click_button(driver)
    click_showed_type_btn(driver, "All comments")

    #Show more comments
    try:
      show_more_comments(driver)
    except:
       print('No more cmt')

    # Scroll to top
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.CONTROL + Keys.HOME)

    # Show comment and scroll step by step
    driver.execute_script("window.scrollTo(0, 700);") #cuộn
    driver.execute_script("window.scrollTo(0, 700);")  #cuộn

    # Sleep 5s
    time.sleep(5)

    # Scroll để các button visible and show replies
    driver.execute_script("window.scrollTo(0, 900);")

    #Show replies
    try:
      show_all_replies(driver, threshold, ite)
    except Exception as e:
      print('Replies are limited', e)
      pass

    #driver.minimize_window()
    #driver.maximize_window()

    # Get comments
    cmts, cnt = get_comments(driver, 2500)

    return cmts, cnt

if __name__ == '__main__':

    cnt = 0
    threshold = 50 #Base on the Internet speed (300 - 400)
    ite = 15 # Use to check whether it reaches the end of the page (Should be 20 - 30)

    # Login info
    username = "quockietuit2021@gmail.com" #your fb username
    password = "qk123456" #your fb password

    url = get_url()
    driver = configure_driver()
    # starter = 0
    # limit = 10

    cmt_data, cnt = crawl(driver, url, username, password, threshold, ite)
    cmt_data_json = json.dumps(cmt_data, ensure_ascii=False)
    cmts = pd.read_json(StringIO(cmt_data_json), orient='records')

    save_to_csv(cmts, 'D:\ki6\Preprocess and Mining\Project\comments.csv')
    time.sleep(50)
    driver.quit()