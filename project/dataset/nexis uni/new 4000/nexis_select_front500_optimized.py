
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import random

sample_df = pd.read_excel("vasectomy_random_sample_1000.xlsx")
sample_df = sample_df.head(500)
sample_df["Status"] = ""

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)

driver.get("https://advance-lexis-com.proxy-um.researchport.umd.edu")
input("🛑 请在打开的浏览器中登录 Nexis Uni 并打开搜索结果页面，然后回到此窗口按下回车继续...")

BASE_URL = "https://advance-lexis-com.proxy-um.researchport.umd.edu/search/?pdmfid=1519360&crid=20f3519b-d7ae-45a3-a719-4d94a919085d&pdsearchterms=vasectomy%2C+vasectomies&pdstartin=hlct%3A1%3A1&pdcaseshlctselectedbyuser=false&pdtypeofsearch=searchboxclick&pdsearchtype=SearchBox&pdtimeline=01.01.2000to12.31.2025%7Cdatebetween&pdqttype=and&pdpsf=LPF~%5EZW4~%5EEnglish&pdquerytemplateid=urn%3Aquerytemplate%3A77d719975096ca14281c8a50cfd9738a~%5EUnited%2520States%2520of%2520America%253B%2520News&ecomp=wxbhkkk&earg=pdpsf&prid=220f6e6c-61bc-49c5-91b0-b94765a61e5c"

def wait_for_checkboxes(timeout=10):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='checkbox'].tools-toggle.skip-target"))
        )
    except:
        print("⚠️ 等待超时，未检测到复选框")

def go_to_page(page_num):
    print(f"📄 正在跳转第 {page_num} 页...")
    driver.get(BASE_URL + f"&page={page_num}")
    time.sleep(3)
    wait_for_checkboxes()

def select_article(article_num_on_page):
    try:
        checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox'].tools-toggle.skip-target")
        checkbox = checkboxes[article_num_on_page - 1]
        driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(1)
        return True
    except Exception as e:
        print(f"⚠️ 勾选失败（第 {article_num_on_page} 篇文章）: {e}")
        return False

current_page = None

for idx, row in sample_df.iterrows():
    page = row["Page Number"]
    article = row["Article Number on Page"]

    if current_page != page:
        go_to_page(page)
        current_page = page

    success = select_article(article)
    sample_df.at[idx, "Status"] = "Selected" if success else "Failed"
    time.sleep(2 + random.randint(1, 3))

sample_df.to_excel("vasectomy_random_sample_1000_status_front500_checked.xlsx", index=False)
print("✅ 前500篇处理完成")
driver.quit()
