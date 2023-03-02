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
- Chạy file `run.bat`:
	- Chỉnh sửa file: Thêm 2 giá trị ở dòng `python scrape.py` để chỉ định lấy dữ liệu từ trang a-b
	- Ví dụ: `python scrape.py 3 10`: `Lấy dữ liệu từ trang 3-10`
	- `Mặc định:` Nếu không có 2 giá trị ở sau thì sẽ lấy tối đa số trang mà thư mục có được
- Tự chạy bằng Terminal:
	- Vào đây chắc biết code rồi, tự chạy đi :D
# Kết quả
- Hai file `csv`:
	- jobs_data.csv: Dữ liệu công việc
	- companies_data.csv: Dữ liệu các công ty đăng những công việc đã lấy về
- Mặc định lấy thông tin công việc từ mục Việc làm mới nhất: `https://www.topcv.vn/tim-viec-lam-moi-nhat`
- Bạn có thể thay đổi link category trong source code `scrape.py` tùy mục đích sử dụng

Trang web có thể thay đổi cấu trúc ở tương lai và làm chương trình lỗi, bạn có thể tự chỉnh sửa hoặc tạo issues trên repo này.

___________________________________
# Installation
- Clone the repo
```
git clone https://github.com/Eakan-Git/TopCV-scraper
```
- Run the `run.bat` file:
	- File editing needed: Pass 2 arguments at the line `python scrape.py` to scrape specific pages from a to b
	- ex.: `python scrape.py 3 10`: `Scrape data from page 3-10`
	- `Default:` If there are no arguments: Scrape all pages
- Run specific task in Terminal:
	- Run it yourself, I believe you.
# Result
- Two `csv` files:
	- jobs_data.csv: Jobs data
	- companies_data.csv: All companies data that posted the jobs which is crawled
- Default target: `https://www.topcv.vn/tim-viec-lam-moi-nhat`
- You can change the link to any **category** link for specific uses:

The website may change its structures in the future, change it yourself or place an issues.
