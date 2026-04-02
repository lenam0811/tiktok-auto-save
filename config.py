# Cấu hình các element trên web TikTok
SELECTORS = {
    "login_button": '[data-e2e="top-login-button"]',
    "profile_icon": '[data-e2e="profile-icon"]',
    
    # Kẹp nhiều thẻ tìm kiếm lại với nhau: Nếu web đổi tên nút, bot vẫn tìm ra
    "save_button": '[data-e2e="browser-book-mark"], [data-e2e="feed-video-save"], [data-e2e="video-save-button"]',
    
    "error_container": '[data-e2e="error-page"]'
}

# Cài đặt cho Bot
HEADLESS_MODE = False  
MIN_DELAY = 3.0        
MAX_DELAY = 7.0