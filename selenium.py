# selenium 4
import selenium
from selenium.webdriver.chrome.service import Service as ChromiumService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

driver = webdriver.Chrome(service=ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()))

base_url = 'https://www.topcv.vn/tim-viec-lam-thuc-tap-t5'
max_page = 35

for i in range(1, max_page):
    url = f"{base_url}?page={i}"
    driver.get(url)
    print(url)

# After scraping is done, don't forget to close the web driver
driver.quit()