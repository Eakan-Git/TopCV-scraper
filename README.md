# TopCV-scraper
Lấy dữ liệu các công việc từ web TopCV.vn

A script to scrape/crawl jobs data from TopCV.vn

# ENGLISH BELLOW
___________________________________

# Cách cài đặt
- Tải source code về hoặc clone repo này về máy bằng lệnh
```
git clone https://github.com/Eakan-Git/TopCV-scraper
```
- Chạy file `run.bat`
# Kết quả
- Một file `csv`
- Toàn bộ thông tin công việc từ mục Việc làm mới nhất: `https://www.topcv.vn/tim-viec-lam-moi-nhat`
- Bạn có thể thay đổi link category trong source code `scrape.py` tùy mục đích
- Bạn nên cài giới hạn trang cho chương trình bằng cách thay số trong source code `scrape.py`:
  Nếu không cài thì có thể sẽ bị lặp dữ liệu ở trang cuối.
```
if page == 401: //Thay số này bằng số trang cuối cùng của thư mục
  break
```
Trang web có thể thay đổi cấu trúc và làm chương trình lỗi, bạn có thể tự chỉnh sửa hoặc tạo issues trên repo này.

___________________________________
# Installation
- Clone the repo
```
git clone https://github.com/Eakan-Git/TopCV-scraper
```
- Run the `run.bat` file
# Result
- A `csv` file
- All job from the link `https://www.topcv.vn/tim-viec-lam-moi-nhat`
- You can change the link to any **category** link for specific uses:
- You should set the flag for pagination in the `scrape.py` file (Not implemented to auto detect the last page):

  If you didn't do that, data maybe duplicated in the last page.
```
if page == 401: //replace this with the number of the last page in your category
  break
```
The website may change its structures to prevent scraping, change it yourself or place an issues.
