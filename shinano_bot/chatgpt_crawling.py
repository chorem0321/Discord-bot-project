from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#chromedriver로 chatgpt.com 들어가면 작동을 하지 않음..
#쉬벌.. gemini도 안됨.. 개빡침.. google에서 traffic을 차단함..
#copilot도 안됨.. cloudflare에서 traffic을 차단함..
#copilot cloudflare 우회 성공

# Chrome 드라이버 설정
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")  # 시크릿 모드로 실행
chrome_service = Service(r'C:/Users/Junsu Choi/Desktop/jikbak/Discord bot project/shinano_bot/chromedriver-win64/chromedriver.exe')  # chromedriver 경로 지정

# 웹드라이버 초기화
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

###########variables##########
wait = WebDriverWait(driver, 10)  # 최대 대기 시간 10초
##############################

try:
    # URL로 이동
    url = "https://gemini.google.com/"
    driver.get(url)
    
    
    processed_count = 1  # 처리된 답변 수 추적
    base_url = "/html/body/chat-app/main/side-navigation-v2/mat-sidenav-container/mat-sidenav-content/div/div[2]/chat-window/div/chat-window-content/div[1]/infinite-scroller/div"

    while True:
        # 사용자로부터 질문 입력받기
        user_question = input("질문을 입력하세요 (종료하려면 '!exit' 입력): ")
        if user_question.lower() == "!exit":
            print("프로그램을 종료합니다.")
            break
        
        # 질문 입력 필드에 사용자 질문 입력
        question_field_xpath = "/html/body/chat-app/main/side-navigation-v2/mat-sidenav-container/mat-sidenav-content/div/div[2]/chat-window/div/input-container/div/input-area-v2/div/div/div[2]/div/div/rich-textarea/div[1]/p"
        question_field = wait.until(EC.presence_of_element_located((By.XPATH, question_field_xpath)))
        question_field.send_keys(user_question)
        
        # 전송 버튼 클릭
        send_button_xpath = "/html/body/chat-app/main/side-navigation-v2/mat-sidenav-container/mat-sidenav-content/div/div[2]/chat-window/div/input-container/div/input-area-v2/div/div/div[3]/div/div[2]/button/mat-icon"
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, send_button_xpath)))
        send_button = driver.find_element(By.XPATH, send_button_xpath)
        send_button.click()
        print(f"질문 '{user_question}'이(가) 성공적으로 전송되었습니다.")
        
        # 새로운 답변이 나타날 때까지 기다리고 출력
        answer_xpath = f"{base_url}[{processed_count}]/model-response/div/response-container/div/div[2]/div/div/message-content/div"
        try:
            answer_element = wait.until(EC.presence_of_element_located((By.XPATH, answer_xpath)))
            print(f"답변 {processed_count + 1}: {answer_element.text}")
            processed_count += 1  # 처리된 답변 수 증가
        except Exception as e:
            print(f"답변을 가져오는 중 오류 발생: {e}")
            break

except Exception as e:
    print(f"오류가 발생했습니다: {e}")

finally:
    driver.quit()  # 브라우저 종료