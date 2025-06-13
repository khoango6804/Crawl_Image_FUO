# FUOverflow Image Scraper

Công cụ tự động đăng nhập và cào toàn bộ ảnh từ thread trên diễn đàn [fuoverflow.com](https://fuoverflow.com) bằng Selenium + Python.

## Tính năng
- Đăng nhập tự động bằng tài khoản/mật khẩu lưu trong file.
- Giao diện cửa sổ đẹp, dễ nhập link thread.
- Tự động lưu ảnh vào thư mục theo tên thread.
- Có thể nhập nhiều link liên tiếp, kết thúc bất cứ lúc nào.

## Hướng dẫn sử dụng

### 1. Chuẩn bị môi trường
- Cài Python 3.7+
- Cài các thư viện cần thiết:
  ```bash
  pip install selenium requests beautifulsoup4
  ```
- Tải [ChromeDriver](https://chromedriver.chromium.org/downloads) đúng phiên bản Chrome, giải nén và đặt cùng thư mục với script hoặc thêm vào PATH.

### 2. Tạo file tài khoản
Tạo file `account.txt` cùng thư mục với script, gồm 2 dòng:
```
TenDangNhap
MatKhau
```
**Ví dụ:**
```
KhoaNgoo
Thinh.@21042009
```

### 3. Chạy script
```bash
python selenium_image_scraper.py
```
- Script sẽ tự động đăng nhập.
- Cửa sổ sẽ hiện ra để bạn nhập link thread muốn cào ảnh.
- Ảnh sẽ được lưu vào thư mục cùng tên thread.
- Sau khi xong, lại hiện cửa sổ để nhập link mới. Để kết thúc, nhấn Cancel hoặc để trống rồi nhấn OK.

### 4. Lưu ý bảo mật
- **KHÔNG chia sẻ file `account.txt` cho bất kỳ ai.**
- Nên đổi mật khẩu định kỳ.
- Không public file `account.txt` lên GitHub hoặc nơi công cộng.

### 5. Giao diện
![image](https://github.com/user-attachments/assets/7e08d6dd-5667-4273-90f0-cddfb9aa4486)

---

**Mọi thắc mắc hoặc cần nâng cấp thêm, hãy tạo issue hoặc liên hệ tác giả!** 

