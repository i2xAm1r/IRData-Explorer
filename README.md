# ⚡ دیتابیس ثبت احوال ایران + آپدیت دیتابیس ایرانسل 
این برنامه با دیتابیس لیک شده ثبت احوال و ایرانسل به شما اجازه میده مشخصات افراد رو با شماره تلفن و ادرس و اسم جستجو کنید تا به تارگت مدنظرتون برسید + 20 میلیون مشخصات

# ⚡ IRData Explorer v1.1.0

🇺🇸 English

IRData Explorer is a modern Windows desktop application developed with Python, PySide6, and SQL Server for searching and exploring large Iranian databases through a simple graphical interface.

The application supports SQL Server MDF/LDF databases and Microsoft Access MDB databases with fast searching, smart filtering, Persian text normalization, and phone number matching.

---

# 🚀 Features

* Fast multi-database search
* SQL Server MDF/LDF support
* Microsoft Access MDB support
* Irancell database support
* Smart phone number matching
* Persian text normalization
* Search by:

  * Name
  * Mobile
  * Telephone
  * Address
  * IDCode
  * PostCode
* Live filtering inside results
* Multiple database selection
* Auto detect MDB tables
* CSV export
* Double click record details
* Hacker Green Theme
* Dark Theme
* Config-based database management
* Windows EXE support

---
## 📸 Screenshots

![Main Dashboard](https://github.com/i2xAm1r/IRData-Explorer/blob/main/Screenshot%202026-05-18%20182539.png?raw=true)
# 📥 Download Database Files

Download database files from Telegram:

👉 t.me/i2xAm1r

---

# 1️⃣ Requirements

Before running the application install:

* Windows 10 / 11
* Microsoft SQL Server

  * SQL Server Express
  * or SQL Server Developer
* Microsoft Access Database Engine 2016 x64

Optional:

* SQL Server Management Studio (SSMS)

Python packages (for source version):

```bash
pip install PySide6 pyodbc pyinstaller
```

---

# 2️⃣ Supported Database Types

IRData Explorer supports:

## SQL Server Databases

* KDB_M.mdf
* KDB98_M.mdf

These databases require SQL Server.

## Access MDB Databases

* 935_1.mdb
* 935-2.mdb
* 936.mdb
* 937.mdb
* 938.mdb
* 939.mdb

MDB databases do NOT require SQL Server.

---

# 🗄️ SQL Database Setup

## Step 1 — Download Database Files

First download the database files from Telegram:

👉 t.me/i2xAm1r

After downloading, extract the ZIP/RAR file.

You should have files like these:

```text
KDB_M.mdf
KDB_M.ldf
KDB98_M.mdf
KDB98_M.ldf
```

These files are required for the application.

---

## Step 2 — Install SQL Server

Before using the application you must install:

- Microsoft SQL Server
- SQL Server Express
  or
- SQL Server Developer

Optional but recommended:
- SQL Server Management Studio (SSMS)

---

## Step 3 — Attach Database to SQL Server

1. Open **SQL Server Management Studio (SSMS)**
2. Connect to your SQL Server
3. Right click on **Databases**
4. Click **Attach**
5. Click **Add**
6. Select:

```text
KDB_M.mdf
```

7. SQL Server should automatically detect:

```text
KDB_M.ldf
```

8. Click **OK**

Repeat the same steps for:

```text
KDB98_M.mdf
```

After attaching both databases, the application will connect automatically.

---

# 📁 Irancell MDB Databases

Irancell databases with `.mdb` extension do NOT require SQL Server attach.

You only need:

- Microsoft Access Database Engine 2016 x64
- Correct MDB paths inside `config.json`

Example:

```json
{
  "name": "Irancell:935",
  "path": "D:\\MDB\\935_1.mdb"
}
```

# 4️⃣ Configure config.json

Place `config.json` next to the EXE file.

Example:

```json
{
  "server": "localhost",

  "databases": [
    {
      "name": "KDB_M",
      "mdf_path": "D:\\Database\\KDB_M.mdf",
      "ldf_path": "D:\\Database\\KDB_M.ldf"
    },
    {
      "name": "KDB98_M",
      "mdf_path": "D:\\Database\\KDB98_M.mdf",
      "ldf_path": "D:\\Database\\KDB98_M.ldf"
    }
  ],

  "access_databases": [
    {
      "name": "Irancell:935",
      "path": "D:\\MDB\\935_1.mdb"
    },
    {
      "name": "Irancell:935|2",
      "path": "D:\\MDB\\935-2.mdb"
    }
  ]
}
```

Important:
Windows paths must use double backslashes.

Correct:

```text
D:\\Database\\KDB_M.mdf
```

Wrong:

```text
D:\Database\KDB_M.mdf
```

---

# 5️⃣ SQL Server Name

Default SQL Server:

```json
"server": "localhost"
```

SQL Express:

```json
"server": "localhost\\SQLEXPRESS"
```

Custom Instance:

```json
"server": "DESKTOP-123ABC\\SQLEXPRESS"
```

---

# 6️⃣ Final Folder Structure

```text
IRDataExplorer/
├── IRDataExplorer.exe
├── config.json
├── icon.ico
└── Database/
```

---

# 7️⃣ Run Application

Run:

```text
IRDataExplorer.exe
```

If databases are already attached:

* App connects automatically

If not attached:

* App tries auto attach using config.json paths

---

# 8️⃣ Troubleshooting

If the application cannot connect:

* Make sure SQL Server is running
* Check config.json
* Check MDF/LDF paths
* Check MDB paths
* Check server name
* Run app as Administrator

---

# 🇮🇷 فارسی

IRData Explorer یک برنامه دسکتاپ ویندوزی برای جستجو و مدیریت دیتابیس‌های بزرگ ایرانی است که با Python و PySide6 ساخته شده است.

این برنامه از دیتابیس‌های:

* SQL Server (MDF/LDF)
* Access MDB

پشتیبانی می‌کند و قابلیت جستجوی سریع، فیلتر زنده، جستجوی شماره موبایل و متن فارسی را دارد.

---

# 🚀 قابلیت‌ها

* جستجوی سریع بین چند دیتابیس
* پشتیبانی از MDF/LDF
* پشتیبانی از MDB
* پشتیبانی از دیتابیس‌های ایرانسل
* جستجوی هوشمند شماره موبایل
* جستجوی فارسی
* جستجو بر اساس:

  * نام
  * موبایل
  * تلفن
  * آدرس
  * کدملی
  * کدپستی
* فیلتر زنده نتایج
* تشخیص خودکار Table فایل‌های MDB
* خروجی CSV
* تم Hacker Green
* تم Dark
* مدیریت دیتابیس با config.json
* نسخه EXE ویندوز

---
## 📸 عکس برنامه

![Main Dashboard](https://github.com/i2xAm1r/IRData-Explorer/blob/main/Screenshot%202026-05-18%20182539.png?raw=true)
# 📥 دانلود دیتابیس

دانلود دیتابیس‌ها از تلگرام:

👉 t.me/i2xAm1r

---

# ⚙️ پیش‌نیازها

قبل از اجرای برنامه نصب کنید:

* Windows 10 / 11
* Microsoft SQL Server
* Microsoft Access Database Engine 2016 x64

اختیاری:

* SQL Server Management Studio

---

# 🗄️ # 🗄️ اتصال دیتابیس SQL

## مرحله 1 — دانلود فایل‌های دیتابیس

ابتدا فایل‌های دیتابیس را از تلگرام دانلود کنید:

👉 t.me/i2xAm1r

بعد از دانلود، فایل ZIP یا RAR را Extract کنید.

باید فایل‌هایی مشابه این داشته باشید:

```text
KDB_M.mdf
KDB_M.ldf
KDB98_M.mdf
KDB98_M.ldf
```

این فایل‌ها برای اجرای برنامه ضروری هستند.

---

## مرحله 2 — نصب SQL Server

قبل از اجرای برنامه باید این موارد نصب باشند:

- Microsoft SQL Server
- SQL Server Express
یا
- SQL Server Developer

اختیاری ولی پیشنهادی:
- SQL Server Management Studio (SSMS)

---

## مرحله 3 — اتصال دیتابیس به SQL Server

1. برنامه **SQL Server Management Studio (SSMS)** را باز کنید
2. به SQL Server متصل شوید
3. روی **Databases** راست کلیک کنید
4. گزینه **Attach** را بزنید
5. روی **Add** کلیک کنید
6. فایل زیر را انتخاب کنید:

```text
KDB_M.mdf
```

7. SQL Server به‌صورت خودکار فایل زیر را شناسایی می‌کند:

```text
KDB_M.ldf
```

8. روی **OK** بزنید

همین مراحل را برای فایل زیر نیز تکرار کنید:

```text
KDB98_M.mdf
```

بعد از Attach شدن دیتابیس‌ها، برنامه به‌صورت خودکار به آن‌ها متصل می‌شود.

---

# 📁 دیتابیس‌های MDB ایرانسل

فایل‌های ایرانسل با پسوند `.mdb` نیازی به Attach داخل SQL Server ندارند.

فقط کافیست:

- Microsoft Access Database Engine 2016 x64 نصب باشد
- مسیر فایل‌های MDB داخل `config.json` درست تنظیم شود

مثال:

```json
{
  "name": "Irancell:935",
  "path": "D:\\MDB\\935_1.mdb"
}
```
# 🛠 تنظیم config.json

فایل config.json باید کنار exe باشد.

داخل آن:

* نام سرور SQL
* مسیر دیتابیس‌ها
* مسیر MDBها

قرار می‌گیرد.

---

# ▶️ اجرای برنامه

فایل زیر را اجرا کنید:

```text
IRDataExplorer.exe
```

اگر دیتابیس attach شده باشد:

* برنامه مستقیم وصل می‌شود

اگر attach نشده باشد:

* برنامه سعی می‌کند خودکار attach کند

---

# ⚠️ رفع مشکل

اگر برنامه وصل نشد:

* SQL Server را بررسی کنید
* config.json را بررسی کنید
* مسیر دیتابیس‌ها را بررسی کنید

[![Telegram](https://img.shields.io/badge/Telegram-Join-blue)](https://t.me/I2xAm1r)  
[![Instagram](https://img.shields.io/badge/Instagram-Follow-red)](https://instagram.com/2xam1r)  
[![GitHub](https://img.shields.io/badge/GitHub-View-black)](https://github.com/I2xAm1r)

[![Discord server](https://discordapp.com/api/guilds/938143724565835848/embed.png?style=banner3)](https://discord.gg/WtPzSe94)

---

## 👨‍💻 Developer

Developed by **I2xAm1r**
