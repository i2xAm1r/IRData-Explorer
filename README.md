# ⚡ IRData Explorer

**IRData Explorer** is a modern Windows desktop application built for fast searching, filtering, and exploring large SQL Server databases through a clean graphical interface.

The application is developed with **Python**, **PySide6**, and **Microsoft SQL Server**, and is designed to work with large `.mdf` / `.ldf` database files without requiring users to write SQL queries manually.

It provides a simple and powerful interface for searching across multiple databases, filtering results instantly, exporting data, and working with large datasets in a user-friendly way.

---

## 🚀 Features

- 🔎 **Fast Multi-Database Search**
- 🗄️ **SQL Server MDF/LDF Database Support**
- 📱 **Smart Phone Number Matching**
- 🇮🇷 **Persian Text Normalization**
- 🧠 **Search by Name, Phone, Code, PostCode, IDCode, Address and more**
- 🧩 **Multiple Database Selection**
- ⚡ **Live Filtering Inside Current Results**
- 📋 **Copy Selected Record**
- 📤 **Export Results to CSV**
- 🖱️ **Double Click Record Details**
- 🎨 **Default Dark Theme**
- 🟢 **Hacker Green Theme**
- ⚙️ **Config-based Database Management**
- 🪟 **Windows EXE Build Support**

---

## 📸 Screenshots

![Main Dashboard](https://github.com/i2xAm1r/IRData-Explorer/blob/main/Screenshot%202026-05-18%20182539.png?raw=true)

## 📦 Requirements

Before running IRData Explorer, make sure the following requirements are installed:
- **first Download DataBase File check this link https://t.me/i2xAm1r for download the Leak DataBase For Iranian**
- **Windows 10 / Windows 11**
- **Microsoft SQL Server**
  - SQL Server Developer
  - or SQL Server Express
- **SQL Server Management Studio (SSMS)**  
  Optional, but recommended for manual database attach and troubleshooting.

For development/building from source:

- Python 3.10+
- PySide6
- pyodbc
- PyInstaller

Install Python dependencies:

```bash
pip install PySide6 pyodbc pyinstaller
```

---

## 🗄️ Database Setup

IRData Explorer works with SQL Server databases such as:

```text
KDB_M.mdf
KDB_M.ldf
KDB98_M.mdf
KDB98_M.ldf
```

You can attach the databases manually using **SQL Server Management Studio**.

### Manual Attach with SSMS

1. Open **SQL Server Management Studio**
2. Connect to your SQL Server instance
3. Right click on **Databases**
4. Click **Attach**
5. Click **Add**
6. Select the `.mdf` file
7. SQL Server should automatically detect the `.ldf` file
8. Click **OK**
9. Repeat for other databases if needed

---

## ⚙️ Configuration

The application uses a `config.json` file to detect:

- SQL Server name
- Database names
- MDF file path
- LDF file path

`config.json` must be placed next to the `.exe` file.

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
    ]
}
```

### Important Path Note

In JSON files, Windows paths must use double backslashes:

```json
"D:\\Database\\KDB_M.mdf"
```

Do **not** use single backslashes like this:

```json
"D:\Database\KDB_M.mdf"
```

---

## 🖥️ Server Name Guide

If SQL Server is installed as the default instance:

```json
"server": "localhost"
```

If SQL Server Express is installed:

```json
"server": "localhost\\SQLEXPRESS"
```

If your SQL Server uses a custom instance name:

```json
"server": "DESKTOP-123ABC\\SQLEXPRESS"
```

You can find the correct server name from the SSMS connection window.

---

## 📁 Final Release Structure

Keep the files like this:

```text
IRDataExplorer/
├── IRDataExplorer.exe
├── config.json
└── Database/
    ├── KDB_M.mdf
    ├── KDB_M.ldf
    ├── KDB98_M.mdf
    └── KDB98_M.ldf
```

---

## ⚠️ Troubleshooting

If the app cannot connect to the database:

- Make sure SQL Server is installed
- Make sure SQL Server service is running
- Make sure `config.json` is next to the `.exe`
- Make sure the server name is correct
- Make sure MDF/LDF paths are correct
- Make sure the database files were not moved after attach
- Try running the app as Administrator

---

## 📡 Social Media

[![Telegram](https://img.shields.io/badge/Telegram-Join-blue)](https://t.me/I2xAm1r)  
[![Instagram](https://img.shields.io/badge/Instagram-Follow-red)](https://instagram.com/2xam1r)  
[![GitHub](https://img.shields.io/badge/GitHub-View-black)](https://github.com/I2xAm1r)

[![Discord server](https://discordapp.com/api/guilds/938143724565835848/embed.png?style=banner3)](https://discord.gg/WtPzSe94)

---

## 👨‍💻 Developer

Developed by **I2xAm1r**

- GitHub: [I2xAm1r](https://github.com/I2xAm1r)
- Telegram: [@I2xAm1r](https://t.me/I2xAm1r)

---
