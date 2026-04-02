import logging
import sys
from file_utils import load_json_file, extract_video_urls
from tiktok_bot import TikTokBot

# Cài đặt cấu hình hiển thị Log ra màn hình
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

def main():
    logging.info("Bắt đầu khởi chạy chương trình...")
    
    # 1. Đọc file
    try:
        cookies_data = load_json_file('cookies.json')
        user_data = load_json_file('user.json')
    except Exception as e:
        logging.critical(f"Lỗi khởi tạo dữ liệu: {e}")
        return

    # 2. Lấy danh sách URL
    video_urls = extract_video_urls(user_data)
    
    if not video_urls:
        logging.warning("Không có link video nào được tìm thấy trong user.json.")
        return

    # 3. Khởi tạo Bot và chạy
    bot = TikTokBot(cookies_data)
    
    try:
        bot.start_browser()
        
        if not bot.verify_login():
            logging.critical("Cookie không hợp lệ. Dừng chương trình.")
            return

        # 4. Lưu video
        for index, url in enumerate(video_urls):
            logging.info(f"--- Đang xử lý video {index + 1}/{len(video_urls)} ---")
            bot.save_video(url)
            bot.random_delay()

    except KeyboardInterrupt:
        logging.info("Người dùng đã dừng chương trình bằng tay.")
    except Exception as e:
        logging.error(f"Lỗi không xác định: {e}")
    finally:
        bot.close()
        logging.info("Hoàn thành quá trình automation.")

# QUAN TRỌNG NHẤT: 2 dòng dưới đây để kích hoạt chương trình
if __name__ == "__main__":
    main()