
# Sctipted by:
#   Po-temkin
#
# Tested on:
#   Python: 3.11
#   Selenium: 4.6.0
#   AppVolumes: 2111
#
# Desctiption:
#   Setting Replica AppVolumes instance after install with help of Selenium WebDriver
#   More information in the documentation https://www.selenium.dev/documentation/webdriver/

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

avm_replica_server_address = 'https://avm02.example.domain.com/register' # Register page address
registered_manager_address = 'avm01.example.domain.com:80' # FQDN or IP of Primary instance
admin_username = 'avmuser' # User with AppVolumes admin rights 
admin_password = ''

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

options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(options=options)
driver.get(avm_replica_server_address)

actions = ActionChains(driver) # initialize ActionChain object

#Filling primary server data
#Filling FQDN
fill_field_by_id('data_secured_address', registered_manager_address)

#Filling 'Username' field
fill_field_by_id('data_username', admin_username)

#Filling 'Password' field
fill_field_by_id('data_password', admin_password)

#Pushing 'Register' button
click_element_by_id('register_btn')

#End
driver.close()