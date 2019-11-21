import time
import sys

LOG_FILE = 'registered.log'

def check_first_login(login_log):
    with open(login_log, 'r') as f:
        lines = f.readlines()

    first_login = None
    last_logout = None
    login_count = 0
    today = None
    for line in lines[::-1]:
        if 'SCREEN_UNLOCKED' in line:
            if today is None:
                today = int(line[16:24])
                first_login = int(line[16:-1])
                login_count += 1
            elif int(line[16:24]) < today:
                break
            else:
                first_login = line[16:-1]
                login_count += 1

        if 'SCREEN_LOCKED' in line:
            if today is not None and int(line[14:22]) < today:
                last_logout = line[14:-1]
                break

    if login_count == 1:
        return True, first_login, last_logout

    else:
        return False, first_login, last_logout


def register_login(userid, password, last_logout=None):
    """
    Register note for logout time
    """
    import time
    from datetime import datetime
    import selenium
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    url = "https://ku1.cybozu.com/g/portal/index.csp?pid=22"
    driver.get(url)

    if url not in driver.current_url:
        # wait until everything is loaded
        time.sleep(2)
        print(driver.current_url)
        
        driver.find_element_by_id("username").send_keys(userid)
        driver.find_element_by_id("password").send_keys(password)
        driver.find_element_by_name("_eventId_proceed").click()

    # register login 
    # sometimes we need to reload the page
    driver.get(url)
    time.sleep(2)
    driver.get(url)
    time.sleep(2)

    driver.execute_script("submitTimeCardForm(this, 'start');return false;")

    xpath = "/html/body/div[2]/div[1]/div/div[2]/div/div[2]/table/tbody/tr/td/div[3]/div/form/table/tbody/tr[2]/td[1]/span"
    button = driver.find_element_by_xpath(xpath)
    button.click()

    with open(LOG_FILE, 'a') as f:
        f.write('login_registered: {}\n'.format(
            datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
        ))

    # register note for logout
    if last_logout is not None:
        year, month, day = last_logout[:4], last_logout[4:6], last_logout[6:8]
        hour, minutes, second = last_logout[8:10], last_logout[10:12], last_logout[12:14]
        url = "https://ku1.cybozu.com/g/timecard/modify.csp?date={}-{}-{}".format(
            year, month, day
        )
        driver.get(url)
        time.sleep(2)
        print(driver.current_url)
        driver.find_element_by_name("remarks").send_keys(
            'actual departure time {}:{}:{}'.format(hour, minutes, second))
        driver.find_element_by_id("timecard_button_save").click()

        with open(LOG_FILE, 'a') as f:
            f.write('logout_registered: {}\n'.format(last_logout))


if __name__ == '__main__':
    # check if this is the first login of this day
    login_log = sys.argv[1]
    account_info = sys.argv[2]
    is_force_register = sys.argv[3].lower() == 'true'

    is_first_login, first_login, last_logout = check_first_login(login_log)
    print(is_first_login, first_login, last_logout)
    if is_first_login or is_force_register:
        # read accout information
        with open(account_info, 'r') as f:
            userid, password = [l.strip() for l in f.readlines()]
        
        # register_login(userid, password)
        register_login(userid, password, last_logout=last_logout)
    
