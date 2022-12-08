# Sctipted by:
#   Po-temkin
#
# Tested on:
#   Python: 3.11
#   Selenium: 4.6.0
#   AppVolumes: 2111
#
# Desctiption:
#   Setting Primary(first) AppVolumes instance after install with help of Selenium WebDriver
#   More information in the documentation https://www.selenium.dev/documentation/webdriver/

import sys
import time
from inspect import currentframe, getframeinfo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select

wait_delay = 60 # Element search time
wait_frequency = 2.5 # Frequency of element searching; Decrease on own risk - some stages may corrupt with error "element has zero size"
separator = '\\'

avm_primary_server_address = 'https://avm01.example.domain.com' # Address of fresh-install App Volumes instance

#Vars for 'License' page
license_file_path = r'C:\Example\Folder\lic.key' # Path to AppVolumes license key

#Vars for 'AD Domains' page
ad_domain_name = 'example.domain.com' # Active Directory Domain Name
ad_domain_controller_host = '' # Domain controller name or IP
ad_ldap_base = '' # LDAP filter
ad_username = 'ldapuser' # User with AD access rights
ad_password = '' #
ad_security_type = 0 # 0 = 'LDAPS'; 1 = 'LDAP over TLS'; 2 = 'LDAP'
ad_skip_cert_validation = 1 # Disable (1) or enable (0) certificate validation check
ad_port = 636 # 

#Vars for 'Admin Roles' page
admin_role = 0 # 0 = 'Administrators'; 1 = 'Administrators (Read only)'; 2 = 'AppStacks Administrators'; 3 = 'Inventory Administrators'; 4 = 'Security Administrators'; 5 = 'Writables Administrators'
search_domain_name = 0 # 0 = 'All';
admin_role_ad_group = 'AD_Admin_Group'
search_all_domains = 0 # Disable (0) or enable (1) recursive search

#Vars for 'Machine Managers' page
#Used for all machine managers
machine_managers_list = 'vcs01.example.domain.com,vcs02.example.domain.com' # One name of vCenter Server or List of vCenter Servers separated by ','
machine_manager_domain = 'DOMAN' # 
machine_manager_username = 'avmqavsiuser' # User with required vCS rights
machine_manager_password = '' #
vmware_cloud = 0 # 1 if vCS configured for VMware Cloud on Amazon Web Services
mount_esxi = 0 # Disable (0) or enable (1) direct connections to ESXi hosts
mount_esxi_username = '' # Used for direct connections; Define if mount_esxi = 0; Must be the same on every ESXi host server
mount_esxi_password = '' # Used for direct connections; Define if mount_esxi = 0; Must be the same on every ESXi host server
mount_local = 0 # Prioritize volumes available on locally attached storage
mount_queue = 1 # Disable (0) or enable (1) shared queues
mount_async = 1 # Disable (0) or enable (1) wait of mount request completion; moout_queue = 1 required
mount_throttle = 1 # Disable (0) or enable (1) queue throttle; moout_queue = 1 required
maximun_operations = 5 # Number of concurrent mount operations per queue; moout_throttle = 1 required
confirm_untrusred_cert = 1 # 0 if vCS certificate is trusted

#Vars for 'Storage' page
packages_datastore_name = 'DATASTORE01_NAME' # Defatult datastore name for packages
packages_storage_path = 'appvolumes/packages' # Path to packages
packages_templates_path = 'appvolumes/packages_templates' # Path to packages templates
writable_datastore_name = packages_datastore_name # Default datastore name for writables
writable_storage_path = 'appvolumes/writables' # Path to writables
writable_templates_path = 'appvolumes/writables_templates' # Path to writable templates
writable_backup_path = 'appvolumes/writables_backup' # Path to writables backup

#Vars for 'Uppload Templates' page
upload_all_templates = 1 # Uploading all templates

#Vars for 'Settings' page
ui_session_timeout = '15' # Timeout for web-session
non_domaint_entitles = 0 # 0 = 'Disallow'; 1 = 'Allow'
writable_backup = 0 # 1 for enable writables backup
writable_backup_interval = 7 # Backup frequency in days
writable_backup_datastore_name = '' # Different datastore for writables backup
writable_backup_path_new = '' # New path if it required
disable_agent_session_cookie = 0 # Disable (1) or enable (0) Agent session cookie
disable_volume_cache = 1 # Disable (1) or enable (0) volume cache
disable_ad_token_query = 0 # Disable (1) or enable (0) AD queries cache
enable_to_any_os = 0 # Disable (0) or enable (1) ignoring difference between target OS and OS used for packaging

#Vars for pop-up CEIP dialog
popup_join_ceip = 0 # 1 to enable CEIP

#Vars for creating Storage group
storage_group_name = 'Group' # Storage group name
template_datastore_name = 'DATASTORE02_NAME' # Datastore name for templates
auto_import_apps = 0 # Disable (0) or enable (1) auto import new appstacks 
auto_replicate_apps = 1 # Disable (0) or enable (1) auto replicate appstacks
datastore_distribution_strategy = 0 # 0 = 'Spread'; 1 = 'Round-robin'
storage_selection_type = 1 # 1 = 'Direct'; 2 = 'Automatic'
storage_prefix = '' # Datastore prefix for Automatic selection
datastores_list = 'DATASTORE02_NAME,DATASTORE03_NAME' # Datastores list for Direct selection

def checkbox_define_by_id(element_id, switch):
    element = driver.find_element(By.ID, element_id)
    if not element.is_selected() and switch == 1:
        actions.click(element)
        actions.perform()
    if element.is_selected() and switch == 0:
        actions.click(element)
        actions.perform()

    return()

def click_element_by_id(element_id):
    element = driver.find_element(By.ID, element_id)
    actions.click(element)
    actions.perform()

    return()

def click_element_by_xpath(element_xpath):
    element = driver.find_element(By.XPATH, element_xpath)
    actions.click(element)
    actions.perform()

    return()

def fill_field_by_id(element_id, element_value):
    element = driver.find_element(By.ID, element_id)
    element.clear()
    element.send_keys(element_value)

    return()

def fill_field_by_xpath(element_xpath, element_value):
    element = driver.find_element(By.XPATH, element_xpath)
    element.clear()
    element.send_keys(element_value)

    return()

def option_select_by_index(element_id, option_index):
    element = driver.find_element(By.ID, element_id)
    actions.click(element)
    actions.perform()
    element_dropdown = Select(element)
    element_dropdown.select_by_index(option_index)
    actions.click(element)
    actions.perform()

    return()

def toggle_define(element_id, element_xpath, switch):
    element_value = driver.find_element(By.ID, element_id).get_attribute('value')
    if element_value == 'false' and switch == 1:
        click_element_by_xpath(element_xpath)
    if element_value == 'true' and switch == 0:
        click_element_by_xpath(element_xpath)

    return()

options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(options=options)
driver.get(avm_primary_server_address)

#Initialize ActionChain object
actions = ActionChains(driver)

#Initialize WebDriverWait object:
wait = WebDriverWait(driver, wait_delay, wait_frequency)

#Waiting AppVolume service start-up
time.sleep(30)
driver.refresh()

#Pushing 'Get Started" button
#click_element_by_id('ft_getstarted')
click_element_by_id('ft_getstarted')

#License
#License setup
try:
    #Wainting 'Edit' button
    wait.until(EC.element_to_be_clickable((By.ID, 'edit_license_btn')))
except TimeoutException:
    driver.close()
    sys.exit('Unable to locate element')
else:
    #Pushing 'Edit' button
    click_element_by_id('edit_license_btn')

    #Attaching license file
    license_file_path_temp = license_file_path.split('separator') 
    license_file_path = 'separator'.join(license_file_path_temp)
    fill_field_by_id('upload_license_key', license_file_path)

    #Uploading license file
    click_element_by_id('license_upload_btn')

    try:
        #Waining 'Edit' button
        wait.until(EC.element_to_be_clickable((By.ID, 'license_next_btn')))
    except:
        driver.close()
        sys.exit('Unable to locate element')
    else:
        #Pushing 'Next' button on 'License' page
        click_element_by_id('license_next_btn')

#Filling fields on 'AD Domains' page
try:
    #Waiting 'Active Directory Domain Name' field
    wait.until(EC.element_to_be_clickable((By.ID, 'ad_domain_i')))
except TimeoutException:
    driver.close()
    sys.exit()
else:
    #Filling 'Active Directory Domain Name' field
    fill_field_by_id('ad_domain_i', ad_domain_name)

    #Filling 'Domain Controller Hosts' field
    fill_field_by_id('ad_controller_hosts_i', ad_domain_controller_host)

    #Filling 'LDAP Base' field
    fill_field_by_id('ad_base_i', ad_ldap_base)

    #Filling 'Username' field
    fill_field_by_id('ad_username_i', ad_username)

    #Filling 'Password' field
    fill_field_by_id('ad_password_i', ad_password)

    #Selecting 'Distribution Strategy' option
    option_select_by_index('ad_security_s', ad_security_type)
    #Defining certificate validation
    checkbox_define_by_id('ad_skip_cert_i', ad_skip_cert_validation)

    #Filling 'Port' field
    fill_field_by_id('ad_port_i', ad_port)

    #Pushing 'Save' button
    click_element_by_id('ad_save_or_update_button')

    try:
        #Waiting 'Next' button
        wait.until(EC.element_to_be_clickable((By.ID, 'ad_next_button')))
    except TimeoutException:
        driver.close()
        sys.exit('Unable to locate element')
    else:
        #Pushing 'Next' button on 'AD Domain' page
        click_element_by_id('ad_next_button')

#Filling 'Admin Roles' 
try:
    #Waiting 'Role' selector
    wait.until(EC.element_to_be_clickable((By.ID, 'role')))
except TimeoutException:
    driver.close()
    sys.exit('Unable to locate element')
else:
    #Selecting 'Role' option
    option_select_by_index('role', admin_role)

    #Selecting 'Search Domain' option
    option_select_by_index('role_assignment_domain_name', search_domain_name)

    #Defining 'Search all domains in the Active Directory forest'
    checkbox_define_by_id('role_assignment_search_recursive', search_all_domains)

    #Fillng 'Search' field
    fill_field_by_id('role_assignment_search_field', admin_role_ad_group)

    #Puhsing 'Search' button
    click_element_by_id('role_assignment_search_button')

    try:
        #Waiting 'Assign' Button
        wait.until(EC.element_to_be_clickable((By.ID, 'ra_save_or_update_button')))
    except TimeoutException:
        driver.close()
        sys.exit('Unable to locate element')
    else:
        #Pushing 'Assign' Button
        click_element_by_id('ra_save_or_update_button')

        try:
            #Waiting 'Next' Button
            wait.until(EC.element_to_be_clickable((By.ID, 'roles_next_button')))
        except TimeoutException:
            driver.close()
            sys.exit('Unable to locate element')
        else:
            #Pushing 'Next' button on 'Admin Roles' page
            click_element_by_id('roles_next_button')

#Filling 'Machines Manager' page
#Skipping 'Add Machine Manager' button for first machine
machine_managers_array = machine_managers_list.split(',')
for index, machine_manager in enumerate(machine_managers_array):
    if index > 0:
        try:
            #Waiting 'Add Machine Manager' Button
            wait.until(EC.element_to_be_clickable((By.ID, 'add_machine_manager_btn')))
        except TimeoutException:
            driver.close()
            sys.exit('Unable to locate element')
        else:
            #Pushing 'Register Machine Manager' button
            click_element_by_id('add_machine_manager_btn')

    try:
        #Waiting 'Add Machine Manager' Button
        wait.until(EC.element_to_be_clickable((By.ID, 'hyp_hostname_i')))
    except TimeoutException:
        driver.close()
        sys.exit('Unable to locate element')
    else:
        #Filling 'Hostname' field
        fill_field_by_id('hyp_hostname_i', machine_manager)

        #Filling 'Username' field
        fill_field_by_id('hyp_username_i', machine_manager_domain + separator + machine_manager_username)

        #Filling 'Password' field
        fill_field_by_id('hyp_password_i', machine_manager_password)

        #Defining 'VMware Cloud' checkbox
        checkbox_define_by_id('is_vmc_option', vmware_cloud)

        #Defining 'Mount ESXi' checkbox
        checkbox_define_by_id('hyp_host_mount_i', mount_esxi)

        if mount_esxi == 1:
            #Filling 'Username' filed
            fill_field_by_id('hyp_host_username_i', mount_esxi_username)

            #Filling 'Password' field
            fill_field_by_id('hyp_host_password_i', mount_esxi_password)

        #Defining 'Mount Local' checkbox
        checkbox_define_by_id('hyp_use_local_i', mount_local)

        #Defining 'Mount Queue'
        checkbox_define_by_id('use_reconfig_queues', mount_queue)

        if mount_queue == 1:
            #Defining 'Mount Async'
            checkbox_define_by_id('use_async', mount_async)

            #Defining 'Mount Throttle'
            checkbox_define_by_id('mount_throttle', mount_throttle)

            #Filling maximum opetations field
            if mount_throttle == 1:
                fill_field_by_id('concurrent_reconfigs', maximun_operations)

        #Pushing 'Save' button
        click_element_by_id('hyp_config_save_button')

        #Processing untrusted certificate dialog
        if confirm_untrusred_cert == 1:
            try:
                #Waiting 'Accept' Button
                wait.until(EC.element_to_be_clickable((By.ID, 'dialog_confirm_hypervisor_change')))
            except TimeoutException:
                driver.close()
                sys.exit('Unable to locate element')
            else:
                #Pushing 'Accept' button; Confirming certificate
                click_element_by_id('dialog_confirm_hypervisor_change')
    
try:
    #Waiting 'Next' Button
    wait.until(EC.element_to_be_clickable((By.ID, 'ft_next_btn')))
except TimeoutException:
    driver.close()
    sys.exit('Unable to locate element')
else:
    #Pushing 'Next' button on 'Machine Managers' page
    click_element_by_id('ft_next_btn')

#Filling 'Storage' page
#Filling 'Packages' block
try:
    #Waiting 'Default Storage Location' field
    wait.until(EC.element_to_be_clickable((By.ID, 'p_datastores_sel_chosen')))
except TimeoutException:
    driver.close()
    sys.exit('Unable to locate element')
else:
    #Moving to 'Default Storage Location' search field
    click_element_by_id('p_datastores_sel_chosen')

    #Filing 'Default Storage Location' search field
    fill_field_by_xpath('//*[@id="p_datastores_sel_chosen"]/div/div/input', packages_datastore_name )

    #Confirming search result
    click_element_by_xpath('//*[@id="p_datastores_sel_chosen"]/div/ul/li[2]')

    #Filling 'Default Storage Path' field
    fill_field_by_id('p_path_i', packages_storage_path)

    #Filling 'Templates Path' field
    fill_field_by_id('p_template_path_i', packages_templates_path)

    #Filling 'Writable Volumes' block
    #Moving to 'Default Storage Location' search field
    click_element_by_id('dd_datastores_sel_chosen')

    #Filing 'Default Storage Location' search field
    fill_field_by_xpath('//*[@id="dd_datastores_sel_chosen"]/div/div/input', writable_datastore_name)

    #Confirming search result
    click_element_by_xpath('//*[@id="dd_datastores_sel_chosen"]/div/ul/li[2]')

    #Filling 'Default Storage Path' field
    fill_field_by_id('dd_path_i', writable_storage_path)

    #Filling 'Templates Path' field
    fill_field_by_id('dd_template_path_i', writable_templates_path)

    #Filling 'Default Backup Path'  field
    fill_field_by_id('dd_ar_path_i', writable_backup_path)

    #Pushing 'Next' button on 'Storage' page
    click_element_by_id('storage_config_save_button')

    try:
        #Waiting 'Set defaults' button
        wait.until(EC.element_to_be_clickable((By.ID, 'dialog_set_datastore')))
    except TimeoutException:
        driver.close()
        sys.exit('Unable to locate element')
    else:
        #Pushing 'Set defaults' button; Confirming tamplates import in background
        click_element_by_id('dialog_set_datastore')

        try:
            #Waiting first template checkbox
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="apptemplate_list_table"]/tbody/tr[1]/td[5]/input')))
        except TimeoutException:
            driver.close()
            sys.exit('Unable to locate element')
        else:
            #Defining all templates checkbox
            checkbox_define_by_id('apptemplate_list_check_all', upload_all_templates)

            #Pushing 'Upload' button
            click_element_by_id('save_imp_apptemplate_btn')

            try:
                #Waiting 'Upload' button
                wait.until(EC.element_to_be_clickable((By.ID, 'dialog_prepackaged_volumes')))
            except TimeoutException:
                driver.close()
                sys.exit('Unable to locate element')
            else:
                #Pushing 'Upload' button; Confirming upload
                click_element_by_id('dialog_prepackaged_volumes')

#Filling 'Settings' page
try:
    #Waiting 'UI Session Timeout' field
    wait.until(EC.element_to_be_clickable((By.ID, 'session_timeout')))
except TimeoutException:
    driver.close()
    sys.exit('Unable to locate element')
else:
    #Filling 'UI Session Timeout' field
    fill_field_by_id('session_timeout', ui_session_timeout)

    #Selecting 'Non-Domain Entities' option
    option_select_by_index('ad_enforce_domain_entities', non_domaint_entitles)

    #Defining 'Regular Backups' toggle
    toggle_define('enable_data_disk_recurrent_backup','//*[@id="data_disk_recurrent_backup_fieldset"]/div[1]/div/label', writable_backup)

    if writable_backup == 1:
        #Filling backup interval field
        fill_field_by_id('data_disk_backup_recurrent_interval', writable_backup_interval)

        #Moving to 'Storage Location' search field
        click_element_by_id('data_disk_recurrent_backup_datastores_sel_chosen')

        #Filling 'Storage Location' seatch field
        fill_field_by_xpath('//*[@id="data_disk_recurrent_backup_datastores_sel_chosen"]/div/div/input', writable_backup_datastore_name)

        #Confirming search results
        click_element_by_xpath('//*[@id="data_disk_recurrent_backup_datastores_sel_chosen"]/div/ul/li[2]')

        #Filling 'Storage Path' field
        fill_field_by_id('data_disk_recurrent_backup_datastores_path', writable_backup_path_new)

    #Expanding 'Advanced settings'
    click_element_by_id('advanced_settings_toggler')
        
    #Difining 'Disable Agent Session Cookie' toggele
    toggle_define('disable_agent_session_cookie','//*[@id="advanced_settings_fieldset"]/div[1]/div[2]/label', disable_agent_session_cookie)

    #Difining 'Disable Volume Cache' toggele
    toggle_define('DISABLE_SNAPVOL_CACHE', '//*[@id="advanced_settings_fieldset"]/div[2]/div[2]/label', disable_volume_cache)

    #Defining 'Disable Token AD query' toggele
    toggle_define('DISABLE_TOKEN_AD_QUERY', '//*[@id="advanced_settings_fieldset"]/div[3]/div[2]/label', disable_ad_token_query)

    #Defining 'Allow package delivery to any operating system' toggele
    toggle_define('ENABLE_ALLOW_PACKAGE_DELIVERY_TO_ANY_OS','//*[@id="advanced_settings_fieldset"]/div[5]/div[2]/label', enable_to_any_os)

    #Processing 'Allow delivery to any operating system' dialog
    if enable_to_any_os == 1:
        #Waiting 'ОК' button
        try:
            wait.until(EC.element_to_be_clickable((By.ID, 'info_ok_button')))
        except TimeoutException:
            driver.close()
            sys.exit('Unable to locate element')
        else:
            #Pushing 'OK' button
            click_element_by_id('info_ok_button')
            #Waiting for dialog closingg
            try:
                wait.until(EC.element_to_be_clickable((By.ID, 'settings_save_button')))
            except:
                driver.close()
                sys.exit('Unable to locate element')

    #Pushing 'Save' button on 'Settings' page
    click_element_by_id('settings_save_button')

#Processing CEIP diaolog
try:
    #Waiting 'CEIP' checkbox
    wait.until(EC.element_to_be_clickable((By.ID, 'dialog_checkbox')))
except TimeoutException:
    driver.close()
    sys.exit('Unable to locate element')
else:
    #Unchecking 'CEIP' checkbox
    checkbox_define_by_id('dialog_checkbox', popup_join_ceip)

    #Pushing 'OK' button in CEIP dialog
    click_element_by_id('ok_ceip_dialog_btn')

try:
    #Waiting 'Infrastructure' page button
    wait.until(EC.element_to_be_clickable((By.ID, 'infrastructure_btn')))
except TimeoutException:
    driver.close()
    sys.exit('Unable to locate element')
else:
    #Moving to 'Infrastructure' page
    click_element_by_id('infrastructure_btn')

    try:
        #Waiting 'Infrastructure' page button
        wait.until(EC.element_to_be_clickable((By.ID, 'ui-id-7')))
    except TimeoutException:
        driver.close()
        sys.exit('Unable to locate element')
    else:
        #Moving to 'Storage Groups' page
        click_element_by_id('ui-id-7')

        try:
            #Waiting 'Create Storage Group' button
            wait.until(EC.element_to_be_clickable((By.ID, 'sgroups_start_create_button')))
        except TimeoutException:
            driver.close()
            sys.exit('Unable to locate element')
        else:
            #Creating Storage Groups
            #Pusshing 'Create Storage Group' button
            click_element_by_id('sgroups_start_create_button')

            try:
                #Waiting 'Create Storage Group' button
                wait.until(EC.element_to_be_clickable((By.ID, 'sgroups_create_name_field')))
            except TimeoutException:
                driver.close()
                sys.exit('Unable to locate element')
            else:
                #Filling 'Group Name' field
                fill_field_by_id('sgroups_create_name_field', storage_group_name)

                #Defining 'Automatically Import AppStacks and Packages' checkbox
                checkbox_define_by_id('sgroups_create_import_field', auto_import_apps)

                #Defining 'Automatically Replicate AppStacks and Packages' checkbox
                checkbox_define_by_id('sgroups_create_replicate_field', auto_replicate_apps)

                #Selecting 'Distribution Strategy' option
                option_select_by_index('sgroups_create_strategy_field',datastore_distribution_strategy)

                #Moving to 'Template Storage' search
                click_element_by_id('sgroups_create_template_field_chosen')

                #Filling 'Template Storage' search
                fill_field_by_xpath('//*[@id="sgroups_create_template_field_chosen"]/div/div/input', template_datastore_name)

                #Confirming search result
                click_element_by_xpath('//*[@id="sgroups_create_template_field_chosen"]/div/ul/li[2]')

                #Selecting 'Storage Selection' option
                option_select_by_index('sgroups_create_select_field', storage_selection_type)

                if storage_selection_type == 1:
                #Selecting members of Storage Group
                    datastores_array = datastores_list.split(',')
                    datastores_input_checkbox_array = driver.find_elements(By.XPATH,'//*[@id="sgroups_create_direct_list"]//label/input')
                    datastores_span_text_array = driver.find_elements(By.XPATH,'//*[@id="sgroups_create_direct_list"]//label/span')
                    for index, datastore in enumerate(datastores_array):
                        while datastore not in datastores_span_text_array[index].text:
                            index += 1
                        actions.click(datastores_input_checkbox_array[index])
                        actions.perform()
                else:
                    #Filling 'Storage Name Prefix' field
                    fill_field_by_id('sgroups_create_prefix_field', storage_prefix)

                #Pushing 'Create' button
                click_element_by_id('sgroups_create_save_button')

                #Confirming creation, pushing 'Create' button
                click_element_by_id('dialog_create_sg')

#End
driver.close()
sys.exit('Complete')