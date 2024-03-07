
import time, os
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twocaptcha import TwoCaptcha
from dotenv import load_dotenv


load_dotenv()
my_api = os.getenv('MYAPIKEY_2CAPTCHA')
proxy_username = os.getenv("APIKEY_PROXY")
url = os.getenv("AMAZON_URL")
sw_options = {
    'proxy': {
        'http': f'http://{proxy_username}:@proxy.zenrows.com:8001',
        'verify_ssl': False,
    },
}
browser = webdriver.Chrome(
    seleniumwire_options=sw_options,
)
browser.get(url)

def checkamazonpage():
    try:
        check = browser.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div/div/form/div[1]/div/div/div[2]/div/div[2]/a').text
        if check == "Try different image":
            return True
        else:
            print(check)
            return False
    except NoSuchElementException:
        return False

status = checkamazonpage()
while status:
    captcha_img = browser.find_element(By.XPATH, '/html/body/div/div[1]/div[3]/div/div/form/div[1]/div/div/div[1]/img')
    captcha_img.screenshot('captchas/Acaptcha.png')

    api_key = os.getenv('APIKEY_2CAPTCHA', my_api)

    solver = TwoCaptcha(api_key)

    try:
        result = solver.normal('captchas/Acaptcha.png')

    except Exception as e:
        print(e)

    else:
        code = result['code']
        print(code)

        # WebDriverWait(browser, 10).until(EC.presence_of_element_located(
        #         (By.ID, 'captchacharacters')))
        
        browser.find_element(By.ID, 'captchacharacters').send_keys(code)
        browser.find_element(
            By.XPATH, '/html/body/div/div[1]/div[3]/div/div/form/div[2]/div/span/span/button'
            ).click()

# get name, img and price of first 5 tags
counter = 0
while counter<=5:
    try:
        elem_list = browser.find_element(By.CSS_SELECTOR, "div.s-main-slot.s-result-list.s-search-results.sg-row")
        items = elem_list.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')
        
        for item in items:
            print(item[0:5].text)
            # title = item.find_element(By.XPATH, '//span[@class="a-size-medium a-color-base a-text-normal"]').text
            # price = item.find_element(By.CSS_SELECTOR, '.a-color-base').text
            # img = item.find_element(By.CSS_SELECTOR, '#search > div.s-desktop-width-max.s-desktop-content.s-opposite-dir.s-wide-grid-style.sg-row > div.sg-col-20-of-24.s-matching-dir.sg-col-16-of-20.sg-col.sg-col-8-of-12.sg-col-12-of-16 > div > span.rush-component.s-latency-cf-section > div.s-main-slot.s-result-list.s-search-results.sg-row > div:nth-child(6) > div > div > span > div > div > div > div.puisg-col.puisg-col-4-of-12.puisg-col-4-of-16.puisg-col-4-of-20.puisg-col-4-of-24.puis-list-col-left > div > div.s-product-image-container.aok-relative.s-text-center.s-image-overlay-grey.puis-image-overlay-grey.s-padding-left-small.s-padding-right-small.puis-flex-expand-height.puis.puis-v10dnrav6sitdx2esf8fqwtjtbs > div > span > a > div > img').get_attribute('src')
            # link = item.find_element(By.CSS_SELECTOR, '#search > div.s-desktop-width-max.s-desktop-content.s-opposite-dir.s-wide-grid-style.sg-row > div.sg-col-20-of-24.s-matching-dir.sg-col-16-of-20.sg-col.sg-col-8-of-12.sg-col-12-of-16 > div > span.rush-component.s-latency-cf-section > div.s-main-slot.s-result-list.s-search-results.sg-row > div:nth-child(6) > div > div > span > div > div > div > div.puisg-col.puisg-col-4-of-12.puisg-col-4-of-16.puisg-col-4-of-20.puisg-col-4-of-24.puis-list-col-left > div > div.s-product-image-container.aok-relative.s-text-center.s-image-overlay-grey.puis-image-overlay-grey.s-padding-left-small.s-padding-right-small.puis-flex-expand-height.puis.puis-v10dnrav6sitdx2esf8fqwtjtbs > div > span > a').get_attribute('href')
            
            # print('Title: ' +title)
            # print('Price:' +price)
            # print('Image:' +img)
            # print('Link:' +link+'\n')

            # # data object
            # write_json({
            #     "title": title,
            #     "price": price,
            #     "image": img,
            #     "link": link
            # })
        
    except Exception as e:
        print(e)
    counter+=1


time.sleep(10)
