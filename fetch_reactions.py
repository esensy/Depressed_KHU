import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

INPUT_FILE = "everytime_posts_2024_2026.xlsx"
OUTPUT_FILE = "everytime_posts_2024_2026.xlsx"
SAVE_EVERY = 100


def init_driver():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(5)
    driver.set_page_load_timeout(30)
    return driver


def parse_reactions(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    likes = comments = scraps = 0
    if lines and all(l.isdigit() for l in lines):
        if len(lines) >= 1: likes = int(lines[0])
        if len(lines) >= 2: comments = int(lines[1])
        if len(lines) >= 3: scraps = int(lines[2])
    return likes, comments, scraps


def fetch_reactions(driver, url):
    try:
        driver.get(url)
    except (TimeoutException, WebDriverException):
        return None
    time.sleep(1)
    try:
        text = driver.find_element(By.CSS_SELECTOR, "ul.status.left").text
        return parse_reactions(text)
    except NoSuchElementException:
        return None


def main():
    df = pd.read_excel(INPUT_FILE)
    total = len(df)
    print(f"총 {total}개 게시글 반응 수집 시작")

    driver = init_driver()
    print("\n브라우저에서 에브리타임 로그인 후 Enter를 누르세요...")
    driver.get("https://everytime.kr/login")
    input()

    failed = 0
    for i, row in df.iterrows():
        result = fetch_reactions(driver, row["link"])
        if result:
            df.at[i, "likes"] = result[0]
            df.at[i, "comments"] = result[1]
            df.at[i, "scraps"] = result[2]
        else:
            failed += 1

        if (i + 1) % SAVE_EVERY == 0:
            df.to_excel(OUTPUT_FILE, index=False)
            print(f"  [{i+1}/{total}] 중간 저장 완료 (실패: {failed}개)")

    df.to_excel(OUTPUT_FILE, index=False)
    driver.quit()
    print(f"\n완료! 총 {total}개 중 {total - failed}개 성공, {failed}개 실패")
    print(f"저장: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
