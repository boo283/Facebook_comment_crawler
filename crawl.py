import configuration as cf
import pandas as pd
import numpy as np
import json

from selenium.webdriver.common.by import By

import time
from io import StringIO




def crawl(driver, url, username, password, threshold, ite):

    driver.get(url)
    # Login Facebook
    cf.login_facebook(username, password, driver)
    if cf.scroll_and_click_button(driver):
      cf.click_showed_type_btn(driver, "All comments")

      #Show more comments
      try:
        cf.show_more_comments1(driver, 100)
      except:
        print('No more cmt')

      # Scroll to top
      driver.find_element(By.TAG_NAME, 'body').send_keys(cf.Keys.CONTROL + cf.Keys.HOME)

      # Show comment and scroll step by step
      driver.execute_script("window.scrollTo(0, 700);") #cuộn
      driver.execute_script("window.scrollTo(0, 700);")  #cuộn

      # Sleep 5s
      time.sleep(5)

      # Scroll để các button visible and show replies
      driver.execute_script("window.scrollTo(0, 900);")

      #Show replies
      try:
        cf.show_all_replies(driver, threshold, ite)
      except Exception as e:
        print('Replies are limited', e)
        pass

      #driver.minimize_window()
      #driver.maximize_window()

      # Get comments
      cmts, cnt = cf.get_comments(driver, 2500)

      return cmts, cnt
    else:
      print("No comment found!")
      return None

if __name__ == '__main__':

    cnt = 0
    threshold = 60 #Base on the Internet speed (300 - 400)
    ite = 20 # Use to check whether it reaches the end of the page (Should be 20 - 30)

    # Login info
    username = "" #your fb username
    password = "" #your fb password

    url = cf.get_url()
    driver = cf.configure_driver()
    # starter = 0
    # limit = 10

    cmt_data, cnt = crawl(driver, url, username, password, threshold, ite)
    cmt_data_json = json.dumps(cmt_data, ensure_ascii=False)
    cmts = pd.read_json(StringIO(cmt_data_json), orient='records')

    cf.save_to_csv(cmts, 'D:\ki6\Preprocess and Mining\Project\comments.csv')
    time.sleep(50)
    driver.quit()