from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.edge import service
from selenium.webdriver.support import expected_conditions as EC


def ask_gemini(user_question):
    # Chrome 드라이버 설정
    options = webdriver.EdgeOptions()
    options.add_experimental_option('excludeSwitches',['enable-logging'])
    options.use_chromium = True
    options.binary_location = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe"
    s = service.Service(r"C:/Users/Junsu Choi/Desktop/jikbak/Discord bot project/shinano_bot/edgedriver_win64/msedgedriver.exe")
    driver = webdriver.Edge(options=options, service = s)
    wait = WebDriverWait(driver, 10)

    try:
        # URL로 이동
        url = "https://gemini.google.com/"
        driver.get(url)

        # 질문 입력 필드에 사용자 질문 입력
        question_field_xpath = "/html/body/chat-app/main/side-navigation-v2/mat-sidenav-container/mat-sidenav-content/div/div[2]/chat-window/div/input-container/div/input-area-v2/div/div/div[2]/div/div/rich-textarea/div[1]/p"
        question_field = wait.until(EC.presence_of_element_located((By.XPATH, question_field_xpath)))
        question_field.send_keys(user_question)

        # 전송 버튼 클릭
        send_button_xpath = "/html/body/chat-app/main/side-navigation-v2/mat-sidenav-container/mat-sidenav-content/div/div[2]/chat-window/div/input-container/div/input-area-v2/div/div/div[3]/div/div[2]/button/mat-icon"
        send_button = wait.until(EC.element_to_be_clickable((By.XPATH, send_button_xpath)))
        send_button.click()

        # 새로운 답변이 나타날 때까지 기다리고 출력
        answer_xpath = "/html/body/chat-app/main/side-navigation-v2/mat-sidenav-container/mat-sidenav-content/div/div[2]/chat-window/div/chat-window-content/div[1]/infinite-scroller/div[1]/model-response/div/response-container/div/div[2]/div/div/message-content/div"
        answer_element = wait.until(EC.presence_of_element_located((By.XPATH, answer_xpath)))
        return answer_element.text

    except Exception as e:
        return f"오류가 발생했습니다: {e}"

    finally:
        driver.quit()