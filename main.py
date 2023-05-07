from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
import os

def write_log(text, log_mode='log', mode='a'):
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    text = '[' + log_mode.upper() + ' ' + now + '] ' + text + '\n'

    log_file = open('log_like.txt', mode)
    log_file.write(text)
    log_file.close

write_log('Programm started', mode='w+')
print("Привет! Добро пожаловать в 'VK Target auto bot' - программу, которая автоматически выполняет задания на vktarget.ru. \nЯ буду помогать вам легко зарабатывать деньги, выполняя различные задания. \nЛог ведётся в файл log_like.txt\nУдачи!\n\n\n")

# Проверяем, существует ли файл options.py
if os.path.exists("options.py"):
    # Если файл уже существует, загружаем данные из него
    from options import email, password, visible
else:
    # Если файла нет, запрашиваем у пользователя данные и сохраняем их в файл
    print('Авторизация на vktarget.ru\n')
    email = input("Введите ваш email: ")
    password = input("Введите ваш пароль: ")
    visible = input("Будете ли вы видеть окно браузера? (yes/no): ").lower() == "yes"

    with open("options.py", "w") as f:
        f.write(f"email = '{email}'\n")
        f.write(f"password = '{password}'\n")
        f.write(f"visible = {visible}\n")

# Далее можно использовать переменные email, password и visible в коде
print('\n')
print(f"Email = {email}")
print(f"Пароль = {password}")
print(f"Видимость браузера = {str(visible)}\n")
check = input("Всё верно? (yes/no): ").lower() == 'yes'
if check:
    print('Продолжаю выполнение программы...\n')
else:
    print('Что бы изменить данные перезапустите программу')
    os.remove("options.py")
    quit()

# создаем экземпляр драйвера для Chrome
options = webdriver.ChromeOptions()

if visible == False:
    options.add_argument('headless')

options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--log-level=3')  # установить уровень журналирования на SEVEREc
driver = webdriver.Chrome(options=options)

# переходим на страницу vktarget.ru
driver.get("https://vktarget.ru")
write_log('Opened a website vktarget.ru')

# находим поле для ввода email, вводим значение и переходим к полю для ввода пароля
email_field = driver.find_element(By.NAME, "email")
email_field.send_keys(email)
email_field.send_keys(Keys.RETURN)
write_log(f'Email ({email}) entered')

# находим поле для ввода пароля, вводим значение и нажимаем на кнопку "Войти"
password_field = driver.find_element(By.NAME, "password")
password_field.send_keys(password)
write_log(f'Password ({password}) entered')

login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Войти')]")
login_button.click()

time.sleep(2)

if driver.current_url == 'https://vktarget.ru/list/':
    write_log('Successfully logged in')
elif driver.current_url == 'https://vktarget.ru/':
    write_log("Couldn't log in")


x = 0
while True:
    time.sleep(10)
    x += 1
    try:
        # находим элемент с классом "task__link" и кликаем на него
        task_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "task__link")))
        task_link.click()

        # находим элементы с id "public_subscribe" и классом "like_wrap" и кликаем на них
        try:
            public_subscribe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "public_subscribe")))
            public_subscribe.click()
            print(f'[TASK] Like the post: \n{driver.current_url}')
            write_log(f'[TASK] Like the post: \n{driver.current_url}', log_mode='task')
        except:
            pass

        try:
            like_wrap = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "like_wrap")))
            like_wrap.click()
            print(f'[TASK] Subscribe to the community: \n{driver.current_url}')
            write_log(f'[TASK] Subscribe to the community: \n{driver.current_url}', log_mode='task')
        except:
            pass

        try:
            like_wrap = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "channel-subscribe-button__desktopButton-1J")))
            like_wrap.click()
            print(f"[TASK] Subscription to the user's Dzen: \n{driver.current_url}")
            write_log(f"[TASK] Subscription to the user's Dzen: \n{driver.current_url}", log_mode='task')
        except:
            pass

        try:
            friend_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Добавить в друзья')]")
            friend_button.click()
            print(f'[TASK] Added to friends: \n{driver.current_url}')
            write_log(f'[TASK] Added to friends: \n{driver.current_url}', log_mode='task')
        except:
            pass

        # возвращаемся на предыдущую страницу
        handles = driver.window_handles
        driver.switch_to.window(handles[0])
        driver.refresh()

        # кликаем на элемент с классом "check_btn"
        check_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "check_btn")))
        check_btn.click()

        print(f'Attempt {x} is successful :)')
        write_log(f'Attempt {x} is successful :)')
    except:
        print(f'Attempt {x} failed :(')
        write_log(f'Attempt {x} failed :(')
        handles = driver.window_handles
        driver.switch_to.window(handles[0])
        driver.refresh()

# закрываем браузер
driver.quit()