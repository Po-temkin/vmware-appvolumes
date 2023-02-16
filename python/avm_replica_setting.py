
# Sctipted by:
#   Po-temkin
#
# Tested on:
#   Python: 3.11
#   Selenium: 4.6.0
#   Webdriver-manager 3.8.5
#   Chrome 108.0.5359.99
#   ChromeDriver 109.0.5414.25
#   AppVolumes: 2111
#
# Desctiption:
#   Setting Replica AppVolumes instance after install with help of Selenium WebDriver
#   More information in the documentation https://www.selenium.dev/documentation/webdriver/

from inspect import currentframe, getframeinfo
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


avm_admin_username = 'avmuser' # User with AppVolumes admin rights 
avm_admin_password = ''
avm_replica_server_address = 'https://avm02.example.domain.com/register' # Register page address
avm_registered_manager_address = 'avm01.example.domain.com:80' # FQDN or IP of Primary instance

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

actions = ActionChains(driver) # initialize ActionChain object

#Filling primary server data
#Filling FQDN
fill_field_by_id('data_secured_address', avm_registered_manager_address)

#Filling 'Username' field
fill_field_by_id('data_username', avm_admin_username)

#Filling 'Password' field
fill_field_by_id('data_password', avm_admin_password)

#Pushing 'Register' button
click_element_by_id('register_btn')

#End
driver.close()