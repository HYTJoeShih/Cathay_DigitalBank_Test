"""
Joe.Shih的國泰世華數位銀行部的考題測驗
測試網頁：https://www.cathaybk.com.tw/cathaybk/
工具：Python、Selenium、Selenium Gird
待研究：Appium
"""
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#####  自定義程式  #####

# 元素顯性等待
def wait_element(driver, location, time):
    WebDriverWait(driver, time).until(EC.presence_of_element_located(location))

# 元素可點擊後並點擊
def click_element(driver, location, time):
    wait_element(driver, location, time)
    element = WebDriverWait(driver, time).until(EC.element_to_be_clickable(location))
    element.click()

#####  設定驅動  #####

# 設定Selenium Grid的URL
grid_url = 'http://localhost:4444'
# 設定瀏覽器選項
chrome_options = webdriver.ChromeOptions()
chrome_options.set_capability("browserVersion", "114")
chrome_options.set_capability("platformName", "Windows 10")
# 建立與Grid節點的連接
driver = webdriver.Remote(command_executor=grid_url, options=chrome_options)

#####  連線與其他設定  #####

test_url = 'https://www.cathaybk.com.tw/cathaybk/'
timeout = 90
window_width = 375
window_high = 812

try:
    driver.implicitly_wait(timeout)  # 隱性等待(適合設定整體timeout)
    driver.set_window_size(window_width, window_high)  # 模擬iphone X大小
    driver.get(test_url)  # 開啟網頁

#####  測試  #####

    # 第一步
    wait_element(driver, (By.XPATH, "//div[@class='cubre-o-indexKv__scroll']"), 10)  # 顯性等待到下滑箭頭出現
    driver.save_screenshot("images/Step1.png")

    # 第二步
    click_element(driver, (By.XPATH, "//div[@class='cubre-o-header__burger']"), 10)
    click_element(driver, (By.XPATH, "//div[normalize-space(text())='產品介紹']/../.."), 10)
    click_element(driver, (By.XPATH, "//div[@class='cubre-o-menuLinkList__btn']/div[normalize-space(text())='信用卡']/.."), 10)
    driver.save_screenshot("images/Step2.png")
    # 計算信用卡下有多少功能列表
    card_items = len(driver.find_elements(By.XPATH, "//div[@class='cubre-o-menuLinkList__content']/div[normalize-space(text())='信用卡']/..//a"))
    print("card_items:", card_items)

    # 第三步
    # 進入卡片介紹
    click_element(driver, (By.XPATH, "//a[normalize-space(text())='卡片介紹']"), 10)

    # 卡片介紹列表滑動
    card_box = driver.find_element(By.CSS_SELECTOR, "div.cubre-m-anchor__nav")
    card_box_location = card_box.location
    card_box_size = card_box.size
    box_height = card_box_size["height"]
    box_width = card_box_size["width"]
    print(card_box_location, card_box_size, box_width, box_height)
    start_x = card_box_location['x'] + box_width * 0.2
    start_y = card_box_location['y'] + box_height / 2
    end_x = card_box_location['x'] + box_width * 0.6
    end_y = card_box_location['y'] + box_height / 2

    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(x=end_x, y=end_y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.move_to_location(x=start_x, y=start_y)
    actions.w3c_actions.pointer_action.release()
    actions.perform()

    # 進入停發卡畫面
    a = card_box.find_element(By.XPATH, "停發卡")
    print(a.text)
    a.click()
    time.sleep(2)
    a.click()

    # 先抓一下數量
    card_abandoned = len(driver.find_elements(By.XPATH, "/html/body/div[1]/main/article/section[6]/div/div[2]/div/div[2]/span"))
    print("card_abandoned:", card_abandoned)

    for i in range(card_abandoned):
        time.sleep(1)
        driver.save_screenshot("images/credit_card_abandoned_"+str(i+1)+".png")
        if i < 10:
            driver.find_element(By.XPATH, "/html/body/div[1]/main/article/section[6]/div/div[2]/div/div[2]/span[" + str(i+2) + "]").click()
        else:
            break
finally:
    driver.quit()
