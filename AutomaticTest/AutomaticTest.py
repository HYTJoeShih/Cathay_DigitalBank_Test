"""
Joe.Shih的國泰世華數位銀行部的考題測驗
測試網頁：https://www.cathaybk.com.tw/cathaybk/
工具：Python、Selenium、Selenium Gird
待研究：Appium
"""
import os
import re
import time
import unittest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

test_time = ''                                                       # 測試時間 initial()產生
test_url = 'https://www.cathaybk.com.tw/cathaybk/'                   # 測試網址
log_path = 'D:\\PycharmProjects\\Cathay_DigitalBank_Test\\log\\'     # log路徑
img_path = ''                                                        # 圖片路徑 initial()產生
driver_path = 'C:\\webdriver\\chromedriver-win64\\chromedriver.exe'  # 驅動路境
timeout = 30                                                         # timeout時間
window_width = 375                                                   # 視窗寬度
window_high = 812                                                    # 視窗高度

# ------------設定驅動------------
# 第一種(Selenium Grid)
try:
    # grid_url = 'http://localhost:4444'
    # # 設定瀏覽器選項
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.set_capability("browserVersion", "115")
    # chrome_options.set_capability("platformName", "Windows 10")
    # # 建立與Grid節點的連接
    # driver = webdriver.Remote(command_executor=grid_url, options=chrome_options)
# 第二種(自行下載driver)
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    driver.implicitly_wait(timeout)                    # 隱性等待
    driver.set_window_size(window_width, window_high)  # 視窗模擬iphone X大小
    driver.get(test_url)                               # 開啟網頁
except:
    print("還沒測試driver就壞了")
    driver.quit()

# ------------unit_test程式------------

class MyTestCase(unittest.TestCase):
    def assert_equal(self, expected, actual):
        self.assertEqual(expected, actual, "兩個值不相等")

test_obj = MyTestCase()

# ------------自定義程式------------

# 初始化(設定測試時間與圖片路徑)
def initial():
    # 產生測試時間
    global test_time
    now = datetime.now()
    test_time = now.strftime("%y%m%d_%H%M%S")
    # 設定截圖路徑
    global img_path
    img_path = log_path + test_time

# 檢查網頁標題
def test_title_equal(verify_text):
    test_obj.assert_equal('國泰世華銀行', verify_text)

# 截圖路徑設定輔助
def take_screenshot(file_name, delay_time):
    # 資料夾路徑和檔案名稱
    global img_path
    # 確認資料夾存在，如果不存在則建立資料夾
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    file_name = file_name + '.png'
    # 完整的截圖路徑
    screenshot_path = os.path.join(img_path, file_name)
    time.sleep(delay_time)
    driver.save_screenshot(screenshot_path)

# 元素顯性等待
def wait_element(driver, selecter, location, wait_time):
    WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((selecter, location)))

# 查找元素
def find_element(driver, selecter, location, wait_time):
    wait_element(driver, selecter, location, wait_time)
    return driver.find_element(selecter, location)

# 查找元素群
def find_elements(driver, selecter, location, wait_time):
    wait_element(driver, selecter, location, wait_time)
    return driver.find_elements(selecter, location)

# 元素可點擊後並點擊
def click_element(driver, selecter, location, wait_time):
    wait_element(driver, selecter, location, wait_time)
    element = WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((selecter, location)))
    element.click()

# 正規表示法取元素width(針對第三題)
def extract_width_value(attribute):
    pattern = r"width:\s*(\d+)px;"
    match = re.search(pattern, attribute)
    if match:
        width_value = match.group(1)
        return width_value
    else:
        print("匹配不到attribute：" + attribute)
        return None

# ------------測試------------

try:
    initial()
    test_title_equal('國泰世華銀行')

    # 第一步
    wait_element(driver, By.XPATH, "//div[@class='cubre-o-quickLink']/div[6]", timeout)  # 顯性等待到"活動專區"出現
    take_screenshot('Step1', 1)

    # 第二步
    click_element(driver, By.XPATH, "//div[@class='cubre-o-header__burger']", timeout)
    click_element(driver, By.XPATH, "//div[normalize-space(text())='產品介紹']/../..", timeout)
    click_element(driver, By.XPATH, "//div[@class='cubre-o-menuLinkList__btn']/div[normalize-space(text())='信用卡']/..", timeout)
    take_screenshot("Step2", 1)
    # 計算信用卡下有多少功能列表
    card_elements = find_elements(driver, By.XPATH, "//div[@class='cubre-o-menuLinkList__content']/div[normalize-space(text())='信用卡']/..//a", timeout)
    card_func = len(card_elements)
    print("信用卡功能總共：", card_func)

    # 第三步
    # 進入卡片介紹
    click_element(driver, By.XPATH, "//a[normalize-space(text())='卡片介紹']", timeout)
    actions = ActionChains(driver)
    # 滾動直到指定元素可見 (這裡使用詳細說明為定位)
    st_card_page_point = find_element(driver, By.XPATH, "//div[normalize-space(text())='停發卡']/../../../..//div[@class='cubre-m-compareCard__action']", timeout)
    actions.move_to_element(st_card_page_point).perform()
    # 計算停發卡張數
    st_card_swipe_div = find_elements(driver, By.XPATH, "//div[normalize-space(text())='停發卡']/../../../..//div[@class='swiper-wrapper']/div", timeout)
    st_card_num = len(st_card_swipe_div)
    print("停發卡張數：", st_card_num)
    # 一邊截圖一邊滑起來
    i = 1
    for st_div in st_card_swipe_div:
        take_screenshot("停發卡" + str(i), 1)
        style_attribute = st_div.get_attribute("style")
        width_value = extract_width_value(style_attribute)
        int_width_value = int(width_value) / 2  # 自行評估滑動範圍只需要該div寬度的一半就好
        actions.click_and_hold(st_div).move_by_offset(int_width_value, 0).release().perform()
        i = i + 1

    time.sleep(5)
finally:
    driver.quit()





# unitest示範區
# if __name__ == '__main__':
#     unittest.main()
