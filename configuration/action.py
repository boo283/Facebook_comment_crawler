
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time


def scroll_and_click_button(driver):
    '''Scroll down and click the button to load button "All comments| Most relevant,...'''
    cnt = 3
    try:
        # Scroll down until the button is found and clickable
        while True:
            if cnt <= 0:
                break
            try:
                # Locate the button using its class names
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.x9f619.x1n2onr6.x1ja2u2z.x6s0dn4.x3nfvp2.xxymvpz"))
                )
                button.click()
                print("Button clicked successfully.")
                break
            except Exception as e:
                # Scroll down a bit and try again
                driver.execute_script("window.scrollBy(0, 1000);")
                cnt -= 1
        return True
    except Exception as e:
        print("Unable to locate and click the button.", e)
        return False

def click_view_more_btn(driver):
    '''Click the view more button to change the show style of comments of a post'''

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    # Find the view more button
    view_more_btn = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'more comments')]")))
    view_more_btn.click()
    print("View more button clicked successfully.")
    return None

def click_showed_type_btn(driver, btn_name):
    '''Click the button to show the most relevant comments or all comments under a post by the argument btn_name'''

    try:
        # Scroll down to the button and click
        driver.execute_script("window.scrollTo(0, window.scrollY)")  # Scroll to the top

        # Find the button by its text
        most_relevant_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), '%s')]"%(btn_name))))
        most_relevant_button.click()
    except Exception as e:
        print("Can not click", btn_name)
        return False

def show_more_comments1(driver, time = 50):
    while True:
        try:
            click_view_more_btn(driver)
            time -= 1
            if time < 0:
                break
        except Exception as e:
            print("Out of contents")
            break

def show_more_comments(driver):
    '''Show more comments under a post'''

    # Limit the number of attempts to load more comments
    max_attempts = 10  # Adjust based on typical post length and your needs
    attempts = 0
    last_count = 0
    stable_attempts = 3  # Number of attempts with no new comments before considering end

    # Keep trying to load more comments until the limit is reached
    while attempts < max_attempts:
        try:
            click_view_more_btn(driver)
            time.sleep(2)  # Give some time for comments to load
            current_count = len(driver.find_elements(By.XPATH, "//div[contains(@class, 'x1n2onr6 x46jau6')]"))

            if current_count == last_count:
                stable_attempts -= 1
                if stable_attempts == 0:
                    print("No more comments to load.")
                    break
            else:
                last_count = current_count
                stable_attempts = 3  # Reset the stable_attempts counter

            attempts += 1
        except Exception as e:
            print("All comments loaded.")
            break

def show_all_replies(driver, threshold, ite):
    '''Show all replies of comments under a post
    Limited time: start - end = 3s => If there is no comment shown in 3s, stop
    Threshold: maximum number of comments'''
    arr = []
    cnt = 1
    while True:
        start = time.time() 
        if cnt > threshold: #Threshold
            break
        try:
            # Find replied comments
            all_replied_comments = driver.find_elements(By.XPATH, "//div[contains(@class, 'x1n2onr6 x46jau6')]")
        except:
            break
        
        # save count of comments to check if all comments are shown
        arr.append(len(all_replied_comments))
        if arr.count(max(arr)) >= ite:
            print("All replies are shown")
            return
        
        # Try to show sub-replied comments in replied-comments
        for comment in all_replied_comments:

            driver.execute_script("window.scrollBy(0, -50);")  # Scroll down 50px to load more comments
        
            try:
                view_more_buttons = WebDriverWait(comment, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'html-div xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x78zum5 x1iyjqo2 x21xpn4 x1n2onr6')]")))
                view_more_buttons.click()
                sub_cmt = comment.find_elements(By.XPATH, "//div[contains(@class, 'x1n2onr6 x1swvt13 x1iorvi4 x78zum5 x1q0g3np x1a2a7pz')]")
                for sub_cmt in comment:
                    try:
                        view_more_sub_buttons = WebDriverWait(sub_cmt, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'html-div xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x78zum5 x1iyjqo2 x21xpn4 x1n2onr6')]")))
                        view_more_sub_buttons.click()
                        #cnt += 1
                    except:
                        break

                cnt += 1

            except Exception as e:
                break

            finally:
                end = time.time()
                if end - start > 3:
                    #print("Finally")
                    return

def filter_spam(text):
    '''Filter spam comments based on user-defined keywords'''

    spam_text = ['http', 'miễn phí', '100%', 'kèo bóng', 'khóa học', 'netflix', 'Net Flix', 'shopee', 'lazada']
    for spam in spam_text:
        if spam in text.lower():
            return True
    return False

def get_comments(driver, limit_text=2500):
    '''Get comments under a post and filter spam comments
    Return:  - dataframe of comments: id, text, is_spam, tag_name.
             - number of comments'''
    cnt = 0
    treasured_comments = []
    is_spam = 0
    comments = driver.find_elements(By.XPATH, "//div[contains(@class, 'x1n2onr6 x1swvt13 x1iorvi4 x78zum5 x1q0g3np x1a2a7pz') or contains(@class, 'x1n2onr6 xurb0ha x1iorvi4 x78zum5 x1q0g3np x1a2a7pz')]")
    for comment in comments:
        try:
            # Check if comment contains text
            text_ele = comment.find_element(By.XPATH, ".//div[contains(@class, 'xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs')]")
            username = comment.find_element(By.XPATH, ".//span[@class='x3nfvp2']/span")

            if text_ele:
                try:
                    name_tag = text_ele.find_element(By.XPATH, ".//span[@class='xt0psk2']/span")
                    name_tag = name_tag.text
                except:
                    name_tag = None

                # Limit the number of comments  
                cnt += 1
                if cnt > limit_text:
                    break
                text = text_ele.text
                if cnt % 10 == 0:
                    print("Count: ", cnt)

                # Filter spam comments    
                if filter_spam(text):
                    is_spam = 1
                else:
                    is_spam = 0
                treasured_comments.append({
                    "id" : cnt,
                    "username": username.text,
                    "text": text,
                    'tag_name': name_tag,
                    'is_spam': is_spam
                })
        except Exception as e:
            continue
    print("Crawl successfully!!! \nTotal Comments: ", cnt)
    return treasured_comments, cnt

def get_url():
    '''Get the URL of a Facebook post from the user input'''
    #get url from input
    url = input("Enter the URL: ")
    return url


def save_to_csv(df, file_name):
    '''Save the dataframe to a CSV file'''
    df.to_csv(file_name, index=False)
