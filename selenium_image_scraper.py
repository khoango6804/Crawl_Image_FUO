from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
import re
from tkinter import Tk, simpledialog, Label, Entry, Button, StringVar, CENTER, Frame

def get_cookies_from_driver(driver):
    cookies = driver.get_cookies()
    cookie_dict = {}
    for cookie in cookies:
        cookie_dict[cookie['name']] = cookie['value']
    return cookie_dict

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def download_image(url, save_path, referer=None, cookies=None):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        if referer:
            headers['Referer'] = referer
        response = requests.get(url, stream=True, headers=headers, cookies=cookies)
        response.raise_for_status()
        # Tự động nhận diện đuôi file từ Content-Type
        ext = '.jpg'
        content_type = response.headers.get('Content-Type', '')
        if 'image/webp' in content_type:
            ext = '.webp'
        elif 'image/png' in content_type:
            ext = '.png'
        elif 'image/jpeg' in content_type:
            ext = '.jpg'
        elif 'image/gif' in content_type:
            ext = '.gif'
        if not save_path.endswith(ext):
            save_path += ext
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"Downloaded: {save_path}")
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")

def scrape_images(url, cookies):
    # Lấy tên folder từ phần cuối của link thread
    folder_name = url.rstrip('/').split('/')[-1]
    image_dir = folder_name
    create_directory(image_dir)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, cookies=cookies)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        image_links = soup.find_all('a', class_='file-preview')
        for i, link in enumerate(image_links):
            href = link.get('href')
            if href:
                img_url = urljoin(url, href)
                img_tag = link.find('img')
                if img_tag and img_tag.get('alt'):
                    original_filename = img_tag.get('alt')
                else:
                    original_filename = os.path.basename(href.strip('/'))
                original_filename = re.sub(r'[<>:"/\\|?*]', '_', original_filename)
                filename = f"{original_filename}"
                save_path = os.path.join(image_dir, filename)
                download_image(img_url, save_path, referer=url, cookies=cookies)
                time.sleep(0.5)
        print(f"\nDownloaded images to {image_dir} directory")
    except Exception as e:
        print(f"Error: {str(e)}")

def read_account(filename='account.txt'):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
        if len(lines) < 2:
            raise Exception('File account.txt phải có 2 dòng: tài khoản và mật khẩu!')
        return lines[0], lines[1]

def get_thread_url_window():
    url = None
    def on_ok():
        nonlocal url
        url = entry.get().strip()
        root.destroy()
    def on_cancel():
        nonlocal url
        url = None
        root.destroy()
    root = Tk()
    root.title("Cào ảnh từ thread FUOverflow")
    root.geometry("420x140+600+300")
    root.resizable(False, False)
    Label(root, text="Nhập link thread FUOverflow muốn cào ảnh:", font=("Arial", 12)).pack(pady=(18, 5))
    entry = Entry(root, width=50, font=("Arial", 11), justify=CENTER)
    entry.pack(pady=5)
    entry.focus()
    btn_frame = Frame(root)
    btn_frame.pack(pady=10)
    Button(btn_frame, text="OK", width=10, command=on_ok).pack(side="left", padx=10)
    Button(btn_frame, text="Cancel", width=10, command=on_cancel).pack(side="right", padx=10)
    root.bind('<Return>', lambda event: on_ok())
    root.bind('<Escape>', lambda event: on_cancel())
    root.mainloop()
    return url

if __name__ == "__main__":
    # Đọc tài khoản và mật khẩu
    username, password = read_account()
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)  # Không tự động đóng Chrome
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://fuoverflow.com/login/")
    # Tự động đăng nhập
    time.sleep(2)
    user_input = driver.find_element('name', 'login')
    pass_input = driver.find_element('name', 'password')
    user_input.clear()
    user_input.send_keys(username)
    pass_input.clear()
    pass_input.send_keys(password)
    pass_input.submit()
    time.sleep(3)  # Đợi đăng nhập xong

    while True:
        THREAD_URL = get_thread_url_window()
        if not THREAD_URL:
            print("Kết thúc chương trình!")
            break
        driver.get(THREAD_URL)
        time.sleep(2)  # Đợi trang thread load xong
        cookies = get_cookies_from_driver(driver)
        scrape_images(THREAD_URL, cookies)
    driver.quit() 