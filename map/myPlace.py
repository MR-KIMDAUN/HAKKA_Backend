from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse, parse_qs

def scrape_my_place(initial_url: str):
    # ChromeDriver 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 헤드리스 모드
    chrome_options.add_argument("--disable-software-rasterizer")  # 소프트웨어 렌더링 비활성화
    chrome_options.add_argument("--no-sandbox")  # 샌드박스 비활성화
    chrome_options.add_argument("--disable-dev-shm-usage")  # /dev/shm 사용 비활성화
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")

    # WebDriver 설정
    service = Service(ChromeDriverManager().install())

    driver = None
    try:
        # 초기 URL 설정

        # 브라우저 열기
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(initial_url)

        # URL 리다이렉트 확인
        current_url = driver.current_url
        
        # 데이터 ID 추출
        data_id = None
        
        if "nidlogin.login" in current_url:
            # 로그인 페이지로 리다이렉트된 경우
            parsed_url = urlparse(current_url)
            query_params = parse_qs(parsed_url.query)
            
            if "url" in query_params:
                target_url = query_params["url"][0]
                parsed_target_url = urlparse(target_url)
                data_id = parsed_target_url.path.split("/")[-2]
                
        elif "/p/favorite/myPlace/folder/" in current_url:
            # 정상적으로 특정 페이지로 이동한 경우
            parsed_url = urlparse(current_url)
            data_id = parsed_url.path.split("/")[-1].split("?")[0]
            
        if not data_id:
            raise Exception("데이터 ID를 추출하지 못했습니다.")

        # 두 번째 URL 생성
        detail_url = f"https://pages.map.naver.com/save-pages/web/detail-list/{data_id}?at=a"

        # 두 번째 URL로 이동
        driver.get(detail_url)

        # 데이터 수집
        titles = WebDriverWait(driver, 20).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, "_main_title_v2kvr_70"))
        )
        addresses = WebDriverWait(driver, 20).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, "_address_area_v2kvr_88"))
        )
        images = WebDriverWait(driver, 20).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME, "_place_info_card_image_v2kvr_169"))
        )
        
        # 데이터가 없을 경우 빈 리스트 반환
        if not titles or not addresses:
            print("추출된 데이터가 없습니다.")
            return None

        result = []

        print("가져온 데이터:")
        for title, address, image in zip(titles, addresses, images):
            # 주소 세부 요소를 찾을 때도 시간 대기를 추가
            WebDriverWait(address, 20).until(
                EC.visibility_of_all_elements_located((By.TAG_NAME, "span"))
            )
            address_detail = address.find_element(By.TAG_NAME, "span").text
            
            # 이미지 URL 추출
            img_tag = image.find_element(By.TAG_NAME, "img")
            img_src = img_tag.get_attribute("src") if img_tag else "이미지 없음"
            
            result.append({"title": title.text, "address": address_detail, "image": img_src})

        return result

    except Exception as e:
        print("오류 발생:", e)
        return None

    finally:
        if driver:
            driver.quit()

