import random
import time
import numpy
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import json

# 问卷地址
url = 'https://www.wjx.cn/vm/QaaZ20B.aspx#'
number = 1
# 生成滑动轨迹
tracks = [i for i in range(1, 50, 3)]

option = webdriver.EdgeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Edge(options=option)
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                       {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
                        })
# 设置浏览器的大小和位置
driver.set_window_size(800, 700)
driver.set_window_position(x=400, y=50)
# 访问问卷链接
driver.get(url)

def read_json():
    with open('./config.json', 'r', encoding='utf-8') as configs:
        content = json.load(configs)
        return content['configs']
configs = read_json()
# 单选


def radio(config, index):
    xpath = f'//*[@id="div{index}"]/div[2]/div'
    a = driver.find_elements(By.XPATH, xpath)
    r = numpy.random.choice(a=numpy.arange(1, len(a) + 1), p=config['gai_lv'])
    driver.find_element(By.CSS_SELECTOR,
                        f'#div{index} > div.ui-controlgroup > div:nth-child({r})').click()

# 多选


def check(config, index):
    xpath = f'//*[@id="div{index}"]/div[2]/div'
    a = driver.find_elements(By.XPATH, xpath)
    # b = random.randint(1, len(a))
    # q = int_random(1, len(a), config['options'])
    q = numpy.random.choice(a=numpy.arange(
        1, len(a) + 1), size=2, p=config['gai_lv'], replace=False)
    q.sort()
    for r in q:
        driver.find_element(
            By.CSS_SELECTOR,   f'#div{index} > div.ui-controlgroup > div:nth-child({r})').click()

# 矩阵


def matrix(config, index):
    topic_nums = config['item_nums']
    for item in range(1, topic_nums + 1):
        r = numpy.random.choice(a=numpy.arange(
            2, topic_nums + 1), p=config['gai_lv'])
        # r = random.randint(2, 6)  # 随机选择
        driver.find_element(
            By.CSS_SELECTOR, f'#drv{index}_{item} > td:nth-child({r})').click()

# 滑动


def slide(config, index):
    interval = numpy.random.choice(a=config['intervals'], p=config['gao_lv'])
    score = random.randint(interval[0], interval[1])
    driver.find_element(By.CSS_SELECTOR, f'#q{index}').send_keys(score)

# 填空


def fill(config, index):
    driver.find_element(By.CSS_SELECTOR, f'#q{index}').send_keys(1)

# 排序


def sort(config, index):
    xpath = f'//*[@id="div{index}"]/ul/li'
    a = driver.find_elements(By.XPATH, xpath)
    q = numpy.random.choice(a=numpy.arange(
        1, len(a) + 1), replace=False, p=config['gai_lv'])
    for b in q:
        driver.find_element(
            By.CSS_SELECTOR, f'#div{index} > ul > li:nth-child({b})').click()
        time.sleep(0.4)

# 量表


def fun1(config, index):
    xpath = f'//*[@id="div{index}"]/ul/li'
    a = driver.find_elements(By.XPATH, xpath)
    q = numpy.random.choice(a=numpy.arange(1, len(a) + 1), p=config['gai_lv'])
    driver.find_element(
        By.CSS_SELECTOR, f'#div{index} > div.scale-div > div > ul > li:nth-child({q})').click()


def run():
    index = 0
    for config in configs:
        index += 1
        match(config['t-type']):
            case 1:
                radio(config, index)
            case 2:
                check(config, index)
            case 3:
                matrix(config, index)
            case 4:
                slide(config, index)
            case 5:
                fill(config, index)
            case 6:
                sort(config, index)
            case 7:
                fun1(config, index)
        # if config['item_type'] == 1:
        #     radio(config, driver, index)
        # elif config['item_type'] == 2:
        #     check(config, driver, index)
    driver.find_element(By.XPATH, '//*[@id="ctlNext"]').click()
    # 出现点击验证码验证
    time.sleep(1)
    # 点击对话框的确认按钮
    driver.find_element(
        By.XPATH, '//*[@id="layui-layer1"]/div[3]/a[1]').click()
    time.sleep(0.5)
    # 点击智能检测按钮
    driver.find_element(By.XPATH, '//*[@id="SM_BTN_1"]').click()
    time.sleep(4)
    # 尝试滑块验证
    try:
        slider = driver.find_element(
            By.XPATH, '//*[@id="nc_1__scale_text"]/span')
        if str(slider.text).startswith("请按住滑块"):
            width = slider.size.get('width')
            ActionChains(driver).drag_and_drop_by_offset(
                slider, width, 0).perform()
    except:
        pass
    # 关闭页面
    time.sleep(1)
    handles = driver.window_handles
    driver.switch_to.window(handles[0])
    # 关闭当前页面，如果只有一个页面，则也关闭浏览器
    driver.close()


count = 0
while count < number:
    count += 1
    run()
