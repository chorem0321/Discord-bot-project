from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import subprocess
from webdriver_manager.chrome import ChromeDriverManager
import time
#chrome.exe 경로를 찾아입력
subprocess.Popen(r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chromeCookie"')
#cloudflare 우회 성공

def ask_copilot(user_question):
    # Chrome 드라이버 설정
    option = Options()
    option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
    wait = WebDriverWait(driver, 10)  # 최대 대기 시간 10초

    try:
        # URL로 이동
        url = "https://copilot.microsoft.com/"
        driver.get(url)

        # 질문 입력 필드에 사용자 질문 입력
        question_field_xpath = "/html/body/div/div[2]/div[2]/main/div[3]/div[2]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[1]/div/div/div/div/textarea"
        question_field = wait.until(EC.presence_of_element_located((By.XPATH, question_field_xpath)))
        question_field.send_keys(user_question)

        # 전송 버튼 클릭
        send_button_xpath = "/html/body/div/div[2]/div[2]/main/div[3]/div[2]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[2]/div/button"
        send_button = wait.until(EC.element_to_be_clickable((By.XPATH, send_button_xpath)))
        time.sleep(0.5)
        send_button.click()

        # 새로운 답변이 나타날 때까지 기다리고 출력
        answer_xpath = "/html/body/div/div[2]/div[2]/main/div[3]/div[1]/div/div/div/div[2]/div[2]/div[2]/div[3]/div"
        time.sleep(10)
        answer_element = driver.find_element(By.XPATH, answer_xpath)
        return answer_element.text

    except Exception as e:
        return f"오류가 발생했습니다: {e}"

    finally:
        driver.quit()