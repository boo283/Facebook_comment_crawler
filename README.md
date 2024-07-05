# FACEBOOK COMMENTS CRAWLER using Selenium in Python

This is the unofficial FACEBOOK COMMENTS CRAWLER in Python. 
The main purpose is support to my study.

 ## Main Fuction 
- Scrape comments with related information such as: 
  - Comment - text 
  - User 
  - Nametag (like @name_tag) 
  - Check if it is spam (based on user-defined demand)  
  
## Installation
- Clone the repository
  ``` git clone https://github.com/boo283/Facebook_comment_crawler.git ```
- Install dependencies: 
 ``` pip install -r requirements.txt ```
 
 ## Usage
 1. Clone this repository 
 2. Open this repository and add some information: 
 - In folder "configuration":
   -  config.py:
      -    In function configure_driver(), replace by the path to your chrome driver, which could be download at
        ref: https://googlechromelabs.github.io/chrome-for-testing/#stable
 - In main folder: 
   - crawl.py:  
      - Just type your Facebook account in the Login info part in main function. 
      - Choose your destination to save crawled data 
 3. Cd to folder and run script: python crawl.py
 4. Simply enter the Facebook URL post and press Enter
  ## Note
  - You must have a stable connection to ensure that this code run correctly  
  - Try to rerun this code if you have any web or driver exceptions 
  - Update requirement: Because the html tag will be update monthly(some tag not all of them), so when any function do not run accurately, 
      you just have to open any post and change to developer mode (F12) to look for the name of the parent-html tag 
      of your failed clicking tag. After that, just replace it by the xpath element or css_selector,... 
      They are all located on the config.py and action.py. 

  ## Contact:    
  - LinkedIn: https://www.linkedin.com/in/phutrungnguyen283/ 
  - Facebook: https://www.facebook.com/ngphtrungboo 
  - Email: trung280302@gmail.com 
  
<strong> Feel free to adjust my code, practice makes perfect ❤️❤️❤️ <strong>
