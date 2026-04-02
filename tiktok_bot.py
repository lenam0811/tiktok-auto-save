import time
import random
import logging
from playwright.sync_api import sync_playwright, Page, BrowserContext, TimeoutError as PlaywrightTimeout
from config import SELECTORS, HEADLESS_MODE, MIN_DELAY, MAX_DELAY

class TikTokBot:
    def __init__(self, cookies_data: list):
        self.raw_cookies = cookies_data
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def clean_cookies(self) -> list:
        cleaned = []
        for cookie in self.raw_cookies:
            c = cookie.copy()
            if 'sameSite' in c:
                val = str(c['sameSite']).lower()
                if val in ['no_restriction', 'none', 'unspecified']:
                    c['sameSite'] = 'None'
                elif val == 'lax':
                    c['sameSite'] = 'Lax'
                elif val == 'strict':
                    c['sameSite'] = 'Strict'
                else:
                    del c['sameSite']
            for key in ['hostOnly', 'session', 'storeId', 'id']:
                c.pop(key, None)
            cleaned.append(c)
        return cleaned

    def start_browser(self):
        self.playwright = sync_playwright().start()
        
        # Thêm args để giả dạng người thật, chống bị nhận diện là Bot
        self.browser = self.playwright.chromium.launch(
            headless=HEADLESS_MODE,
            args=["--disable-blink-features=AutomationControlled"]
        )
        self.context = self.browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        # Ẩn biến webdriver để Tiktok không biết đang dùng Tool
        self.context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        valid_cookies = self.clean_cookies()
        self.context.add_cookies(valid_cookies)
        self.page = self.context.new_page()
        logging.info("Đã mở trình duyệt và bơm Cookie thành công.")

    def random_delay(self):
        sleep_time = random.uniform(MIN_DELAY, MAX_DELAY)
        time.sleep(sleep_time)

    def verify_login(self) -> bool:
        logging.info("Đang kiểm tra trạng thái đăng nhập...")
        try:
            self.page.goto("https://www.tiktok.com/", timeout=45000)
            self.page.wait_for_timeout(3000) 
            
            if self.page.locator(SELECTORS["profile_icon"]).count() > 0:
                logging.info("Xác nhận đăng nhập THÀNH CÔNG.")
                return True
            elif self.page.locator(SELECTORS["login_button"]).count() > 0:
                logging.error("Cookie đã hết hạn (Thấy nút Đăng nhập).")
                return False
            else:
                return True 
                
        except Exception as e:
            logging.error(f"Lỗi khi kiểm tra đăng nhập: {e}")
            return False

    def save_video(self, url: str):
        logging.info(f"Đang mở: {url}")
        try:
            self.page.goto(url, timeout=45000)
            self.page.wait_for_timeout(6000) 
            
            self.page.keyboard.press("Escape")
            self.page.wait_for_timeout(500)

            if self.page.locator(SELECTORS["error_container"]).count() > 0:
                logging.error("-> THẤT BẠI: Video không tồn tại hoặc link hỏng.")
                return

            # DANH SÁCH SELECTOR MỚI (CHỈ NHẮM VÀO THẺ <button>)
            possible_selectors = [
                # Tọa độ của bạn, NHƯNG thêm chữ 'button' vào cuối để chọt đúng cái nút bấm, không chọt vào cái hộp
                'section[class*="SectionActionBarContainer"] > div:nth-child(4) button',
                
                # Các phương án dự phòng
                'button[data-e2e="browser-book-mark"]',
                'button[data-e2e="feed-video-save"]',
                'button[aria-label*="Lưu"]',
                'button[aria-label*="Save"]'
            ]

            is_clicked = False

            for selector in possible_selectors:
                elements = self.page.locator(selector)
                
                if elements.count() > 0:
                    for i in range(elements.count()):
                        try:
                            btn = elements.nth(i)
                            
                            # CU CLICK NGƯỜI THẬT: Nhấn giữ chuột 150ms rồi mới nhả ra, Ép click dù có bị che
                            btn.click(force=True, delay=150)
                            
                            # Đợi 1 giây để xem hiệu ứng nút có đổi sang màu vàng không
                            self.page.wait_for_timeout(1000)
                            
                            logging.info(f"-> THÀNH CÔNG: Đã click Lưu.")
                            is_clicked = True
                            break 
                        except Exception:
                            pass
                
                if is_clicked:
                    break 

            if not is_clicked:
                screenshot_path = "loi_hien_thi.png"
                self.page.screenshot(path=screenshot_path)
                logging.error(f"-> THẤT BẠI: Không tìm thấy nút thực sự. Đã lưu ảnh '{screenshot_path}'.")

        except Exception as e:
            logging.error(f"-> LỖI KHI XỬ LÝ {url}: {e}")

    def close(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        logging.info("Đã đóng trình duyệt.")