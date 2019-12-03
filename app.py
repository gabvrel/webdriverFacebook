import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import urllib.request


chromedriver = "C:/Users/user/Desktop/chromedriver"
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chromedriver, chrome_options=chrome_options)


class FacebookDeletePhotosBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.bot = driver

    def login(self):
        bot = self.bot
        bot.get('https://www.facebook.com/')
        time.sleep(2)
        email = bot.find_element_by_name('email')
        password = bot.find_element_by_name("pass")
        email.clear()
        password.clear()
        email.send_keys(self.username)
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        time.sleep(2)

    def get_photos(self):
        bot = self.bot
        user_account = bot.find_element_by_class_name("_5afe")
        user_link = user_account.get_attribute("href")
        bot.get(user_link)
        time.sleep(2)
        photos_link = user_link.split("?")[0] + "/photos"
        bot.get(photos_link)
        time.sleep(2)

        your_photos = bot.find_element_by_id("u_0_21")
        your_photos_link = your_photos.get_attribute("href")
        bot.get(your_photos_link)

        img_arr = []

        for i in range(5):
            bot.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1)
            photos_grid = bot.find_elements_by_class_name("uiMediaThumb")
            links_photos_grid = [elem.get_attribute("href") for elem in photos_grid]
            if i == 4:
                img_arr = links_photos_grid

        for j in img_arr:
            self.save_and_delete(j)

    def save_and_delete(self, img):
        bot = self.bot
        bot.get(img)
        time.sleep(3)
        main_img = bot.find_element_by_class_name("spotlight")
        img_url = main_img.get_attribute("src")
        img_name = img_url.split("/")[-1].split("?")[0]
        urllib.request.urlretrieve(img_url, 'fb_images/' + img_name)
        time.sleep(2)


gb = FacebookDeletePhotosBot('', '')
gb.login()
gb.get_photos()