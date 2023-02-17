
# Sctipted by:
#   Po-temkin
#
# Tested on:
#   Python: 3.11
#   Selenium: 4.6.0, 4.8.0
#   Webdriver-manager 3.8.5
#   Chrome 108.0.5359.99, 110.0.5481.97 
#   ChromeDriver 109.0.5414.25, 110.0.5481.97
#   AppVolumes: 2111, 2212
#
# Desctiption:
#   Setting Replica AppVolumes instance after install with help of Selenium WebDriver
#   More information in the documentation https://www.selenium.dev/documentation/webdriver/

import sys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

wait_delay = 60 # Element search time
wait_frequency = 2.5 # Frequency of element searching; Decrease on own risk - some stages may corrupt with error "element has zero size"

avm_replica_server_address  = 'https://avm02.example.domain.com/register' # Register page address
avm_registered_manager_address = 'avm01.example.domain.com' # FQDN or IP of Primary instance
avm_admin_username = 'avmuser' # User with AppVolumes admin rights
avm_admin_password = ''

avm_http_register = 0 # Whether or not use http request to register; This option is necessary to bypass registration error on AppVolumes 2111

def click_element_by_id(element_id):
    element = driver.find_element(By.ID, element_id)
    actions.click(element)
    actions.perform()

    return()

def fill_field_by_id(element_id, element_value):
    element = driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(element_value)

    return()

#Initialize WebDriver object
driver_options = webdriver.ChromeOptions()
driver_options.add_argument('--ignore-ssl-errors=yes')
driver_options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = driver_options) # Required webdriver-manager
#driver_service = Service(chromedriver_path) # Required ChromeDriver
#driver = webdriver.Chrome(service=driver_service, options=driver_options) # Required ChromeDriver
driver.get(avm_replica_server_address)

# initialize ActionChain object
actions = ActionChains(driver)

#Initialize WebDriverWait object:
wait = WebDriverWait(driver, wait_delay, wait_frequency)

#Determining request port
if avm_http_register == 1:
    avm_registered_manager_address = avm_registered_manager_address + ':80'
    avm_skip_untrusted_cert_processing = 1
else:
    avm_skip_untrusted_cert_processing = 0

#Filling primary server data
#Filling FQDN
fill_field_by_id('data_secured_address', avm_registered_manager_address)

#Filling 'Username' field
fill_field_by_id('data_username', avm_admin_username)

#Filling 'Password' field
fill_field_by_id('data_password', avm_admin_password)

#Pushing 'Register' button
click_element_by_id('register_btn')

if avm_skip_untrusted_cert_processing == 0:
    #Processing untrusted certificate dialog
    try:
        #Wainting 'Accept' button
        wait.until(EC.element_to_be_clickable((By.ID, 'dialog_view_ssl_accept')))
    except TimeoutException:
        driver.close()
        sys.exit('Unable to locate element: dialog_view_ssl_accept')
    else:
        #Pushing 'Edit' button
        click_element_by_id('dialog_view_ssl_accept')

#End
driver.close()
sys.exit('Execution successfully completed')