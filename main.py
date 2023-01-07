from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

driver.get('https://nid.naver.com/nidlogin.login')

# wait until someid is clickable


def login():
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'id')))
    wait.until(EC.presence_of_element_located((By.ID, 'pw')))

    idInput = driver.find_element(By.ID, 'id')
    pwInput = driver.find_element(By.ID, 'pw')

    idInput.send_keys('')
    pwInput.send_keys('')

    loginButton = driver.find_element(By.ID, 'log.login')
    loginButton.click()


def wait_login():
    wait = WebDriverWait(driver, 1000)
    wait.until(EC.url_to_be("https://www.naver.com/"))


wait_login()

# navigate cafe
driver.get("https://cafe.naver.com/joonggonara")
# click menu
# menu_name = "놓치지마!중나앱 꿀팁"
# find menu

total_articles_menu_link = driver.find_element(
    By.ID, 'menuLink0').get_attribute("href")

first_travel = True
latest_link = ''

while True:
    # go to menu
    driver.get(total_articles_menu_link)

    # WebDriverWait(driver, 1000).until(
    #     EC.presence_of_element_located((By.ID, 'content-area')))

    sleep(1)

    driver.switch_to.frame('cafe_main')

    # latest article
    # latest_id = driver.find_element(By.CSS_SELECTOR,
    #                                 'div.inner_number').text

    # extract article links
    target_links = driver.find_elements(
        By.CSS_SELECTOR, 'div.inner_list > a[onclick*=\'atitle\']')

    if latest_link is target_links[0].get_attribute('href'):
        sleep(2)
        continue

    previous_latest_link = latest_link
    latest_link = target_links[0].get_attribute('href')

    # extract target articles url
    wait_queue = list(map(lambda x: x.get_attribute('href'), target_links))

    if first_travel:
        wait_queue = [wait_queue[0]]
        first_travel = False
    else:
        try:
            slicing_index = wait_queue.index(previous_latest_link)
            wait_queue = wait_queue[0:slicing_index]
        except:
            print(
                'probably bug is occurred, you must check second page of selected menu')

    for article_link in wait_queue:
        try:
            # show article
            driver.get(article_link)

            sleep(1)

            driver.switch_to.frame('cafe_main')

            comment_area = driver.find_element(
                By.CSS_SELECTOR, 'textarea.comment_inbox_text')
            comment_area.send_keys('안녕하세요!')

            comment_button = driver.find_element(
                By.CSS_SELECTOR, 'div.comment_attach a[class*=\'btn_register\']')
            comment_button.click()

            print(f'success: {article_link}')

        except:
            print(f'error: {article_link}')

        sleep(1)
