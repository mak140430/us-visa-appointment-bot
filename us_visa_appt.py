import argparse
import time
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



while True:
    parser = argparse.ArgumentParser(description="Process some arguments.")
    parser.add_argument('-login', type=str, help='First argument')
    parser.add_argument('-password', type=str, help='Second argument')
    
    telegram_url = "https://api.telegram.org/bot<botToken>/sendMessage?chat_id=<chatID>&text={}"

    args = parser.parse_args()

    login = args.login
    password = args.password

    driver = webdriver.Chrome()
    time.sleep(2)
    driver.get('https://ais.usvisa-info.com/en-rs/niv/users/sign_in')
    time.sleep(2)

    email_input = driver.find_element(By.ID,"user_email")
    time.sleep(1)
    # your email for login
    email_input.send_keys(login)
    time.sleep(1)
    password_input = driver.find_element(By.ID,"user_password")
    time.sleep(1)
    # your password for login
    password_input.send_keys(password)
    time.sleep(1)

    policy_confirm_input = driver.find_element(By.CLASS_NAME, "icheckbox")
    time.sleep(1)
    policy_confirm_input.click()

    time.sleep(1)
    login_form = driver.find_element(By.TAG_NAME,"form")
    time.sleep(1)
    login_form.submit()

    time.sleep(2)
    try:
        wait = WebDriverWait(driver, 10)  # wait for up to 10 seconds
        continue_button = driver.find_element(By.XPATH, "//a[starts-with(@href, '/en-rs/niv/schedule/') and contains(@href, '/continue_actions')]")
        continue_button.click()
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.quit() # Close the current driver instance before restarting
        continue  # This will restart the loop from the beginning

    time.sleep(2)
    schedule_button = driver.find_element(By.CLASS_NAME,"accordion-title")
    schedule_button.click()
    try:
        time.sleep(2)
        continue_button = driver.find_element(By.XPATH,"//a[@href='/en-rs/niv/schedule/53010002/continue']")
        continue_button.click()
    except Exception as e:
        print(f"An error occurred: {e}")
        driver.quit() # Close the current driver instance before restarting
        continue

    time.sleep(2)
    wait = WebDriverWait(driver, 10)  # wait for up to 10 seconds
    element = wait.until(EC.presence_of_element_located((By.XPATH, "//h3[text()='There are no available appointments at this time. Please check back in a few days as the Consular Section will open more appointments.']")))
    if element:
        message = "No Appointments Available, not proceeding further"
        print(message)
        response = requests.get(telegram_url.format(message))

    else:
        print("Appointments Available, proceeding further")

        try:
            location_select = driver.find_element(By.ID,"appointments_consulate_appointment_facility_id")
            location_select.click()
            location_option = driver.find_element(By.XPATH,"//option[contains(text(), 'Belgrade')]")
            location_option.click()
            time.sleep(1)
            location_select = driver.find_element(By.ID,"appointments_consulate_appointment_facility_id")
            location_select.click()
            time.sleep(1)


            element = driver.find_element(By.ID,"consulate_date_time")
            display_style = element.value_of_css_property("display")
                # find the element on the page and check for css property
            if display_style == "block":
                message = 'There is availability in Belgrade, hurry up!'
            else:
                message = 'No availability in Belgrade!'

            response = requests.get(telegram_url.format(message))

            if response.status_code == 200:
                print('Notification sent successfully')
            else:
                print(f'Failed to send notification: {response.content}')

            # time.sleep function makes while loop wait for 30 mins
            time.sleep(30 * 60)

        except Exception as e:
            print(f"An error occurred: {e}")

