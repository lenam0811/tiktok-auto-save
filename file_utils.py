import json
import logging

def load_json_file(filepath: str) -> dict:
    """Đọc và load file JSON."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            logging.info(f"Đã đọc thành công file {filepath}")
            return data
    except FileNotFoundError:
        logging.error(f"Không tìm thấy file: {filepath}")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Lỗi format JSON ở file {filepath}: {e}")
        raise

def extract_video_urls(data) -> list:
    """
    Tự động dò tìm mục 'FavoriteVideoList' trong file JSON 
    và trích xuất tất cả các đường link video.
    """
    urls = []

    # Hàm đệ quy để tìm key "FavoriteVideoList" ở bất kỳ độ sâu nào trong JSON
    def find_favorite_list(d):
        if isinstance(d, dict):
            if "FavoriteVideoList" in d:
                return d["FavoriteVideoList"]
            for k, v in d.items():
                result = find_favorite_list(v)
                if result is not None:
                    return result
        return None

    # Lấy danh sách video
    fav_list = find_favorite_list(data)

    if not fav_list:
        logging.warning("Không tìm thấy mục 'FavoriteVideoList' trong file JSON.")
        return urls

    # Quét qua từng item trong danh sách để lấy Link
    for item in fav_list:
        if isinstance(item, dict):
            if "Link" in item:
                urls.append(item["Link"])
        elif isinstance(item, str):
            urls.append(item)

    logging.info(f"Đã trích xuất thành công {len(urls)} link video từ FavoriteVideoList.")
    return urls