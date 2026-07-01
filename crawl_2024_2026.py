import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException

BOARD_URL = "https://everytime.kr/386930/p/"
LOGIN_URL = "https://everytime.kr/login"
BATCH_SIZE = 100
OUTPUT_FILE = "everytime_posts_2024_2026.xlsx"


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


def login(driver):
    driver.get(LOGIN_URL)
    print("\n브라우저 창에서 직접 로그인해주세요.")
    print("로그인 완료 후 여기서 Enter를 누르세요...")
    input()
    print("로그인 확인 완료, 크롤링 시작합니다.")


def diagnose(driver):
    """게시판/게시글 구조 파악용 — 한 번만 실행"""
    print("\n=== 구조 진단 ===")
    driver.get(BOARD_URL + "1")
    time.sleep(2)

    articles = driver.find_elements(By.CSS_SELECTOR, "article.list")
    print(f"article.list 개수: {len(articles)}")

    if not articles:
        print("article.list 없음. 현재 URL:", driver.current_url)
        return

    first = articles[0]
    links = first.find_elements(By.TAG_NAME, "a")
    times = first.find_elements(By.TAG_NAME, "time")
    print(f"첫 article — a태그: {len(links)}개, time태그: {len(times)}개")

    if links:
        href = links[0].get_attribute("href")
        print(f"첫 링크: {href}")

        # 게시글 상세 페이지 진단
        driver.get(href)
        time.sleep(2)
        print(f"\n게시글 페이지 URL: {driver.current_url}")

        for sel in ["p.large", "div.large", "article p", "section p", ".content p"]:
            els = driver.find_elements(By.CSS_SELECTOR, sel)
            print(f"  {sel}: {len(els)}개", els[0].text[:30] if els else "")

        for sel in ["time.large", "time", ".time", "span.time"]:
            els = driver.find_elements(By.CSS_SELECTOR, sel)
            print(f"  {sel}: {len(els)}개", els[0].get_attribute("datetime") or els[0].text if els else "")

        for sel in ["h2.large", "h2", ".title"]:
            els = driver.find_elements(By.CSS_SELECTOR, sel)
            print(f"  {sel}: {len(els)}개", els[0].text[:30] if els else "")

        print("\n[반응 셀렉터]")
        for sel in ["ul.status.left", "ul.status", ".status", "ul.like", ".like", "div.status", "span.like", "em"]:
            els = driver.find_elements(By.CSS_SELECTOR, sel)
            print(f"  {sel}: {len(els)}개", els[0].text[:50] if els else "")


def parse_reactions(text):
    likes = comments = scraps = 0
    lines = [l.strip() for l in text.split("\n") if l.strip()]

    # 현재 형식: 숫자만 순서대로 "0\n0\n0"
    if lines and all(l.isdigit() for l in lines):
        if len(lines) >= 1: likes = int(lines[0])
        if len(lines) >= 2: comments = int(lines[1])
        if len(lines) >= 3: scraps = int(lines[2])
        return likes, comments, scraps

    # 구버전 형식: "좋아요 5\n댓글 3\n스크랩 1"
    for line in lines:
        if line.startswith("좋아요"):
            try: likes = int(line.replace("좋아요", "").strip())
            except ValueError: pass
        elif line.startswith("댓글"):
            try: comments = int(line.replace("댓글", "").strip())
            except ValueError: pass
        elif line.startswith("스크랩"):
            try: scraps = int(line.replace("스크랩", "").strip())
            except ValueError: pass
    return likes, comments, scraps


def is_before_2024(time_text):
    """연도 포함 형식(2023/01/01)이면 2024 이전인지 확인, MM/DD 형식은 현재 연도라 항상 False"""
    t = time_text.strip()
    if len(t) >= 4 and t[:4].isdigit():
        return int(t[:4]) < 2024
    return False


def crawl_post(driver, link):
    try:
        driver.get(link)
    except (TimeoutException, WebDriverException):
        print(f"페이지 로드 실패, 건너뜀: {link}")
        return None

    time.sleep(1.5)

    try:
        try:
            title = driver.find_element(By.CSS_SELECTOR, "h2.large").text.strip()
        except NoSuchElementException:
            title = ""

        content = driver.find_element(By.CSS_SELECTOR, "p.large").text.strip()
        t_el = driver.find_element(By.CSS_SELECTOR, "time.large")
        post_time = t_el.get_attribute("datetime") or t_el.text.strip()

        try:
            reaction_text = driver.find_element(By.CSS_SELECTOR, "ul.status.left").text
            likes, comments, scraps = parse_reactions(reaction_text)
        except NoSuchElementException:
            likes = comments = scraps = 0

        return {
            "title": title,
            "content": content,
            "time": post_time,
            "likes": likes,
            "comments": comments,
            "scraps": scraps,
            "link": link,
        }
    except NoSuchElementException:
        return None


def crawl(driver):
    all_posts = []
    page = 1
    batch = 1
    stop = False

    while not stop:
        driver.get(BOARD_URL + str(page))
        time.sleep(2)

        articles = driver.find_elements(By.CSS_SELECTOR, "article.list")
        if not articles:
            print(f"페이지 {page}: 게시글 없음, 종료")
            break

        links = []
        for article in articles:
            try:
                a_tags = article.find_elements(By.TAG_NAME, "a")
                if not a_tags:
                    continue
                href = a_tags[0].get_attribute("href")
                links.append(href)
            except Exception:
                continue

        for link in links:
            post = crawl_post(driver, link)
            if post is None:
                continue

            if is_before_2024(str(post["time"])):
                stop = True
                break

            all_posts.append(post)
            print(f"수집: {post['time']} | {post['content'][:30]}...")

            if len(all_posts) % BATCH_SIZE == 0:
                df = pd.DataFrame(all_posts)
                batch_file = f"everytime_posts_2024_2026_batch{batch}.xlsx"
                df.to_excel(batch_file, index=False)
                print(f"배치 저장: {batch_file} ({len(all_posts)}개)")
                batch += 1

        print(f"페이지 {page} 완료 | 누적 {len(all_posts)}개")
        page += 1

    return all_posts


def main():
    print("=== 에브리타임 경희대 우울증 게시판 크롤러 (2024~2026) ===")
    print("1) 구조 진단만  2) 크롤링 시작")
    mode = input("선택 (1/2): ").strip()

    driver = init_driver()
    try:
        login(driver)

        if mode == "1":
            diagnose(driver)
            input("\n진단 완료. Enter 누르면 종료...")
            return

        posts = crawl(driver)

        if posts:
            df = pd.DataFrame(posts)
            df.to_excel(OUTPUT_FILE, index=False)
            print(f"\n완료! 총 {len(posts)}개 저장 → {OUTPUT_FILE}")
        else:
            print("수집된 게시글이 없습니다.")
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
