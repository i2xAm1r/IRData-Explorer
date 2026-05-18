import sys
import re
import csv
import json
import pyodbc
import webbrowser

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem,
    QLabel, QMessageBox, QComboBox,
    QDialog, QTextEdit, QFileDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QGuiApplication


CONFIG_FILE = "config.json"
USERNAME = "I2xAm1r"

COLUMNS = [
    "SourceDB",
    "Code",
    "FirstName",
    "LastName",
    "Name",
    "NamePrint",
    "Title",
    "Tableau",
    "Tel",
    "Mobile",
    "PostCode",
    "IDCode",
    "EconomicCode",
    "FatherName",
    "Address",
    "Address2",
]


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


CONFIG = load_config()
SERVER = CONFIG["server"]
DATABASES = CONFIG["databases"]


def clean_text(value):
    if value is None:
        return ""
    text = str(value)
    if text.upper() == "NULL":
        return ""
    return text


def normalize_persian(text: str) -> str:
    text = clean_text(text)
    text = text.replace("ي", "ی").replace("ك", "ک")
    text = text.replace("‌", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip().lower()


def normalize_phone(text: str) -> str:
    digits = re.sub(r"\D", "", clean_text(text))

    if digits.startswith("0098"):
        digits = digits[4:]
    elif digits.startswith("98"):
        digits = digits[2:]

    if digits.startswith("0"):
        digits = digits[1:]

    return digits


def phone_patterns(text: str):
    phone = normalize_phone(text)

    if not phone:
        return [f"%{text}%"]

    return [
        f"%{phone}%",
        f"%0{phone}%",
        f"%98{phone}%",
        f"%0098{phone}%",
    ]


def get_conn(database):
    return pyodbc.connect(
        "DRIVER={SQL Server};"
        f"SERVER={SERVER};"
        f"DATABASE={database};"
        "Trusted_Connection=yes;"
    )


def get_master_conn():
    return pyodbc.connect(
        "DRIVER={SQL Server};"
        f"SERVER={SERVER};"
        "DATABASE=master;"
        "Trusted_Connection=yes;"
    )


def database_exists(db_name):
    try:
        conn = get_master_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT DB_ID(?)", db_name)
        exists = cursor.fetchone()[0] is not None
        conn.close()
        return exists
    except Exception:
        return False


def attach_database(db):
    db_name = db["name"]
    mdf_path = db["mdf_path"]
    ldf_path = db["ldf_path"]

    if database_exists(db_name):
        return True

    try:
        conn = get_master_conn()
        conn.autocommit = True
        cursor = conn.cursor()

        query = f"""
        CREATE DATABASE [{db_name}]
        ON
        (FILENAME = N'{mdf_path}'),
        (FILENAME = N'{ldf_path}')
        FOR ATTACH;
        """

        cursor.execute(query)
        conn.close()
        return True

    except Exception as e:
        print(f"Attach error for {db_name}:", e)
        return False


def init_databases():
    failed = []

    for db in DATABASES:
        ok = attach_database(db)
        if not ok:
            failed.append(db["name"])

    return failed


class DetailDialog(QDialog):
    def __init__(self, row_data):
        super().__init__()
        self.setWindowTitle("جزئیات رکورد")
        self.resize(800, 600)

        layout = QVBoxLayout()

        text = ""
        for key, value in zip(COLUMNS, row_data):
            text += f"{key}: {clean_text(value)}\n"

        self.detail_box = QTextEdit()
        self.detail_box.setReadOnly(True)
        self.detail_box.setText(text)

        copy_btn = QPushButton("Copy Full Record")
        copy_btn.clicked.connect(
            lambda: QGuiApplication.clipboard().setText(text)
        )

        layout.addWidget(self.detail_box)
        layout.addWidget(copy_btn)

        self.setLayout(layout)


class SearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Iranian DataBase Finder @i2xAm1r")
        self.resize(1650, 850)

        self.all_rows = []
        self.filtered_rows = []

        main_layout = QVBoxLayout()

        title = QLabel("Iranian DataBase Finder")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            "font-size: 26px; font-weight: bold; margin: 10px;"
        )
        main_layout.addWidget(title)

        creator_layout = QHBoxLayout()

        github_btn = QPushButton("GitHub")
        github_btn.clicked.connect(
            lambda: webbrowser.open(f"https://github.com/{USERNAME}")
        )

        telegram_btn = QPushButton("Telegram")
        telegram_btn.clicked.connect(
            lambda: webbrowser.open(f"https://t.me/{USERNAME}")
        )

        self.theme_box = QComboBox()
        self.theme_box.addItems(["Default Dark", "Hacker Green"])
        self.theme_box.currentTextChanged.connect(self.apply_theme)

        creator_layout.addWidget(QLabel("Developer:"))
        creator_layout.addWidget(github_btn)
        creator_layout.addWidget(telegram_btn)
        creator_layout.addStretch()
        creator_layout.addWidget(QLabel("Theme:"))
        creator_layout.addWidget(self.theme_box)

        main_layout.addLayout(creator_layout)

        db_layout = QHBoxLayout()

        self.database_box = QComboBox()
        self.database_box.addItem("All Databases")
        for db in DATABASES:
            self.database_box.addItem(db["name"])

        self.status_label = QLabel("Database Ready")

        db_layout.addWidget(QLabel("Database:"))
        db_layout.addWidget(self.database_box)
        db_layout.addWidget(self.status_label)

        main_layout.addLayout(db_layout)

        search_layout = QHBoxLayout()

        self.search_type = QComboBox()
        self.search_type.addItems([
            "All",
            "Mobile / Tel",
            "Name",
            "Code",
            "PostCode",
            "IDCode",
            "Address",
            "FatherName",
            "EconomicCode",
            "Tableau",
            "Title",
        ])

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("جستجو در دیتابیس...")
        self.search_input.returnPressed.connect(self.search_database)

        self.search_button = QPushButton("Search DB")
        self.search_button.clicked.connect(self.search_database)

        search_layout.addWidget(self.search_type)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)

        main_layout.addLayout(search_layout)

        filter_layout = QHBoxLayout()

        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("فیلتر داخل همین نتایج...")
        self.filter_input.textChanged.connect(self.filter_current_results)

        self.clear_filter_button = QPushButton("Clear Filter")
        self.clear_filter_button.clicked.connect(self.clear_filter)

        self.copy_button = QPushButton("Copy Selected")
        self.copy_button.clicked.connect(self.copy_selected)

        self.export_button = QPushButton("Export CSV")
        self.export_button.clicked.connect(self.export_csv)

        filter_layout.addWidget(self.filter_input)
        filter_layout.addWidget(self.clear_filter_button)
        filter_layout.addWidget(self.copy_button)
        filter_layout.addWidget(self.export_button)

        main_layout.addLayout(filter_layout)

        self.result_label = QLabel("آماده جستجو")
        main_layout.addWidget(self.result_label)

        self.table = QTableWidget()
        self.table.setColumnCount(len(COLUMNS))
        self.table.setHorizontalHeaderLabels(COLUMNS)
        self.table.setAlternatingRowColors(True)
        self.table.setSortingEnabled(True)
        self.table.cellDoubleClicked.connect(self.open_detail)

        main_layout.addWidget(self.table)
        self.setLayout(main_layout)

        self.setStyleSheet(self.default_theme())

    def default_theme(self):
        return """
            QWidget {
                background-color: #1e1e1e;
                color: #ffffff;
                font-family: Segoe UI;
                font-size: 14px;
            }

            QLabel {
                color: white;
            }

            QLineEdit, QComboBox {
                background-color: #2d2d2d;
                color: white;
                border: 1px solid #555;
                border-radius: 7px;
                padding: 9px;
                font-size: 15px;
            }

            QPushButton {
                background-color: #0078d4;
                color: white;
                border-radius: 7px;
                padding: 9px;
                min-width: 110px;
                font-size: 15px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #108ee9;
            }

            QTableWidget {
                background-color: #252526;
                color: white;
                gridline-color: #444;
                font-size: 13px;
                selection-background-color: #0078d4;
                selection-color: white;
            }

            QHeaderView::section {
                background-color: #333333;
                color: white;
                padding: 7px;
                border: 1px solid #444;
                font-weight: bold;
            }

            QTextEdit {
                background-color: #252526;
                color: white;
                font-size: 15px;
                border: 1px solid #555;
            }
        """

    def hacker_theme(self):
        return """
            QWidget {
                background-color: #050505;
                color: #00ff66;
                font-family: Consolas;
                font-size: 14px;
            }

            QLabel {
                color: #00ff66;
            }

            QLineEdit, QComboBox {
                background-color: #000000;
                color: #00ff66;
                border: 1px solid #00aa44;
                border-radius: 7px;
                padding: 9px;
                font-size: 15px;
            }

            QPushButton {
                background-color: #001a0a;
                color: #00ff66;
                border: 1px solid #00aa44;
                border-radius: 7px;
                padding: 9px;
                min-width: 110px;
                font-size: 15px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #003d18;
            }

            QTableWidget {
                background-color: #000000;
                color: #00ff66;
                gridline-color: #004d1f;
                font-size: 13px;
                selection-background-color: #003d18;
                selection-color: white;
            }

            QHeaderView::section {
                background-color: #001a0a;
                color: #00ff66;
                padding: 7px;
                border: 1px solid #00aa44;
                font-weight: bold;
            }

            QTextEdit {
                background-color: #000000;
                color: #00ff66;
                font-size: 15px;
                border: 1px solid #00aa44;
            }
        """

    def apply_theme(self):
        if self.theme_box.currentText() == "Hacker Green":
            self.setStyleSheet(self.hacker_theme())
        else:
            self.setStyleSheet(self.default_theme())

    def selected_databases(self):
        selected = self.database_box.currentText()

        if selected == "All Databases":
            return [db["name"] for db in DATABASES]

        return [selected]

    def build_where(self, keyword, search_type):
        params = []
        where_parts = []
        normal_like = f"%{keyword}%"

        if search_type == "Mobile / Tel":
            for p in phone_patterns(keyword):
                where_parts.append("Mobile LIKE ?")
                params.append(p)
                where_parts.append("Tel LIKE ?")
                params.append(p)

        elif search_type == "Name":
            for col in ["FirstName", "LastName", "Name", "NamePrint"]:
                where_parts.append(f"{col} LIKE ?")
                params.append(normal_like)

        elif search_type == "Code":
            where_parts.append("Code LIKE ?")
            params.append(normal_like)

        elif search_type == "PostCode":
            where_parts.append("PostCode LIKE ?")
            params.append(normal_like)

        elif search_type == "IDCode":
            where_parts.append("IDCode LIKE ?")
            params.append(normal_like)

        elif search_type == "Address":
            where_parts.append("Address LIKE ?")
            params.append(normal_like)
            where_parts.append("Address2 LIKE ?")
            params.append(normal_like)

        elif search_type == "FatherName":
            where_parts.append("FatherName LIKE ?")
            params.append(normal_like)

        elif search_type == "EconomicCode":
            where_parts.append("EconomicCode LIKE ?")
            params.append(normal_like)

        elif search_type == "Tableau":
            where_parts.append("Tableau LIKE ?")
            params.append(normal_like)

        elif search_type == "Title":
            where_parts.append("Title LIKE ?")
            params.append(normal_like)

        else:
            for p in phone_patterns(keyword):
                where_parts.append("Mobile LIKE ?")
                params.append(p)
                where_parts.append("Tel LIKE ?")
                params.append(p)

            for col in [
                "Code",
                "FirstName",
                "LastName",
                "Name",
                "NamePrint",
                "Title",
                "Tableau",
                "PostCode",
                "IDCode",
                "EconomicCode",
                "FatherName",
                "Address",
                "Address2",
            ]:
                where_parts.append(f"{col} LIKE ?")
                params.append(normal_like)

        return " OR ".join(where_parts), params

    def search_one_database(self, db_name, keyword, search_type):
        where_sql, params = self.build_where(keyword, search_type)

        query = f"""
        SELECT TOP 3000
            Code,
            FirstName,
            LastName,
            Name,
            NamePrint,
            Title,
            Tableau,
            Tel,
            Mobile,
            PostCode,
            IDCode,
            EconomicCode,
            FatherName,
            Address,
            Address2
        FROM tblCustomer
        WHERE {where_sql}
        ORDER BY Code
        """

        conn = get_conn(db_name)
        cursor = conn.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        return [
            tuple([db_name] + [clean_text(v) for v in row])
            for row in rows
        ]

    def search_database(self):
        keyword = self.search_input.text().strip()
        search_type = self.search_type.currentText()

        if not keyword:
            QMessageBox.warning(
                self, "خطا", "لطفاً چیزی برای جستجو وارد کنید."
            )
            return

        selected_dbs = self.selected_databases()

        all_results = []
        errors = []

        for db_name in selected_dbs:
            try:
                results = self.search_one_database(
                    db_name, keyword, search_type
                )
                all_results.extend(results)
            except Exception as e:
                errors.append(f"{db_name}: {e}")

        self.all_rows = all_results
        self.filtered_rows = self.all_rows[:]
        self.filter_input.clear()
        self.show_rows(self.filtered_rows)

        msg = f"{len(self.all_rows)} نتیجه پیدا شد"
        if len(selected_dbs) > 1:
            msg += f" از {len(selected_dbs)} دیتابیس"

        self.result_label.setText(msg)

        if errors:
            QMessageBox.warning(
                self,
                "Database Warning",
                "\n\n".join(errors)
            )

    def show_rows(self, rows):
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(rows))

        for row_index, row in enumerate(rows):
            for col_index, value in enumerate(row):
                item = QTableWidgetItem(clean_text(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_index, col_index, item)

        self.table.resizeColumnsToContents()
        self.table.setSortingEnabled(True)

    def filter_current_results(self):
        text = self.filter_input.text().strip()

        if not text:
            self.filtered_rows = self.all_rows[:]
            self.show_rows(self.filtered_rows)
            self.result_label.setText(
                f"{len(self.filtered_rows)} نتیجه نمایش داده می‌شود"
            )
            return

        normalized_filter = normalize_persian(text)
        phone_filter = normalize_phone(text)

        result = []

        for row in self.all_rows:
            row_text = " ".join(normalize_persian(v) for v in row)
            row_phone_text = " ".join(normalize_phone(v) for v in row)

            match_text = normalized_filter in row_text
            match_phone = phone_filter and phone_filter in row_phone_text

            if match_text or match_phone:
                result.append(row)

        self.filtered_rows = result
        self.show_rows(self.filtered_rows)
        self.result_label.setText(
            f"{len(self.filtered_rows)} نتیجه از بین {len(self.all_rows)} نتیجه فیلتر شد"
        )

    def clear_filter(self):
        self.filter_input.clear()
        self.filtered_rows = self.all_rows[:]
        self.show_rows(self.filtered_rows)
        self.result_label.setText(
            f"{len(self.filtered_rows)} نتیجه نمایش داده می‌شود"
        )

    def open_detail(self, row, column):
        if row < 0 or row >= len(self.filtered_rows):
            return

        dialog = DetailDialog(self.filtered_rows[row])
        dialog.exec()

    def copy_selected(self):
        row = self.table.currentRow()

        if row < 0 or row >= len(self.filtered_rows):
            QMessageBox.warning(self, "خطا", "لطفاً یک ردیف انتخاب کنید.")
            return

        data = self.filtered_rows[row]
        text = "\n".join(
            f"{key}: {value}" for key, value in zip(COLUMNS, data)
        )

        QGuiApplication.clipboard().setText(text)
        QMessageBox.information(self, "کپی شد", "رکورد انتخاب‌شده کپی شد.")

    def export_csv(self):
        if not self.filtered_rows:
            QMessageBox.warning(
                self, "خطا", "نتیجه‌ای برای خروجی گرفتن وجود ندارد."
            )
            return

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save CSV",
            "results.csv",
            "CSV Files (*.csv)"
        )

        if not path:
            return

        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(COLUMNS)
                writer.writerows(self.filtered_rows)

            QMessageBox.information(self, "Done", "فایل CSV ذخیره شد.")

        except Exception as e:
            QMessageBox.critical(self, "Export Error", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    failed = init_databases()
    if failed:
        QMessageBox.warning(
            None,
            "Database Attach Warning",
            "این دیتابیس‌ها attach نشدند:\n" + "\n".join(failed)
        )

    window = SearchApp()
    window.show()
    sys.exit(app.exec())
