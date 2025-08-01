from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
import time
#Var
qqid = 3077906125  #QQ号,请保持电脑QQ处于登录状态
service = FirefoxService(executable_path="/usr/bin/geckodriver")
options = webdriver.FirefoxOptions()
#Set preferences
#options.add_argument("--headless") #是否启用无头模式,不保证是否不影响主程序
options.set_preference("network.proxy.type", 1)
options.set_preference("geo.enabled", False)
options.set_preference("geo.provider.use_corelocation", False)
options.set_preference("geo.prompt.testing", False)
options.set_preference("geo.prompt.testing.allow", False)
driver = webdriver.Firefox(service=service, options=options)
driver.implicitly_wait(10)
#log in to QQ zone
driver.get("https://user.qzone.qq.com/%d/infocenter" % (qqid))
driver.switch_to.frame("login_frame")
ele_user = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[4]/div[8]/div/a"))
)
ele_user.click()
driver.switch_to.default_content()
element=driver.find_element(By.ID,"tab_menu_friend")
element.click()
print("Went into main page")
time.sleep(20)
#Process every element
print("starting to process elements")
j=0
while True:
    flag=0
    ele_clis = driver.find_elements(By.CLASS_NAME,"qz_like_btn_v3")
    print("Processing element (%d,%d)..." % (j,len(ele_clis)))
    for ele_cli in ele_clis:
        try:
            attr = ele_cli.get_attribute("data-clicklog")
        except StaleElementReferenceException:
            print("skipping...")
            continue
        
        if attr == "cancellike":
            continue
        elif attr == "like":
            driver.execute_script("arguments[0].scrollIntoView();",ele_cli)
            driver.execute_script('window.scrollBy(0,-100)')
            ele_cli.click()
            flag=1
            time.sleep(0.5) #实测应该没用
    if flag==1:
        print("Some elements wasn't processed.")
        continue            
    ele_move = WebDriverWait(driver,2).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[3]/div[2]/p[2]"))
    )
    try:
        driver.execute_script("arguments[0].scrollIntoView();",ele_move)
    except:
        print("Scroll failed")
    time.sleep(5) #理论上来讲，这句话没用
    j+=1

#item qz_like_btn_v3 
#item qz_like_btn_v3 item-on