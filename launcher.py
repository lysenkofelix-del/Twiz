import customtkinter as ctk
import os
import sys
import json
import requests
import psutil
import subprocess
import threading
import zipfile
import re
from pathlib import Path
from tkinter import messagebox

# Constants
GAME_PATH = "C:/Twix"
CONFIG_FILE = os.path.join(GAME_PATH, "launcher_config.json")
VERSIONS_FILE = os.path.join(GAME_PATH, "versions.json")


def convert_google_drive_url(url):
    """
    Конвертирует обычную ссылку Google Drive в прямую ссылку для скачивания

    Примеры:
    https://drive.google.com/file/d/FILE_ID/view -> https://drive.google.com/uc?export=download&id=FILE_ID
    https://drive.google.com/open?id=FILE_ID -> https://drive.google.com/uc?export=download&id=FILE_ID
    """
    if "drive.google.com" not in url:
        return url

    # Извлекаем ID файла из разных форматов ссылок
    patterns = [
        r'/file/d/([a-zA-Z0-9_-]+)',  # /file/d/FILE_ID/view
        r'id=([a-zA-Z0-9_-]+)',        # ?id=FILE_ID
        r'/d/([a-zA-Z0-9_-]+)'         # /d/FILE_ID
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            file_id = match.group(1)
            return f"https://drive.google.com/uc?export=download&id={file_id}"

    return url


def extract_zip(zip_path, extract_to):
    """
    Извлекает содержимое zip-архива
    Возвращает True при успехе, False при ошибке
    """
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        return True
    except Exception as e:
        print(f"Ошибка распаковки: {e}")
        return False


class TwixLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Twix Client")
        self.geometry("900x600")
        self.resizable(False, False)

        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Initialize game path
        self.initialize_game_directory()

        # Load configuration
        self.config = self.load_config()

        # Setup UI
        self.setup_ui()

        # Load available versions
        self.load_versions()

    def initialize_game_directory(self):
        """Create game directory if it doesn't exist"""
        try:
            os.makedirs(GAME_PATH, exist_ok=True)
            print(f"Game directory initialized at: {GAME_PATH}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create game directory: {e}")
            sys.exit(1)

    def load_config(self):
        """Load launcher configuration"""
        default_config = {
            "ram_allocated": 2048,  # MB
            "selected_version": "ALPHA 1.16.5",
            "last_played": None,
            "game_url": ""
        }

        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return default_config
        return default_config

    def save_config(self):
        """Save launcher configuration"""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Failed to save config: {e}")

    def load_versions(self):
        """Load available game versions"""
        default_versions = {
            "versions": [
                {
                    "name": "ALPHA 1.16.5",
                    "description": "Последняя стабильная версия",
                    "download_url": "",
                    "installed": False
                },
                {
                    "name": "ALPHA 1.16.4",
                    "description": "Предыдущая версия",
                    "download_url": "",
                    "installed": False
                },
                {
                    "name": "ALPHA 1.16.3",
                    "description": "Старая версия",
                    "download_url": "",
                    "installed": False
                }
            ]
        }

        if os.path.exists(VERSIONS_FILE):
            try:
                with open(VERSIONS_FILE, 'r', encoding='utf-8') as f:
                    self.versions_data = json.load(f)
            except:
                self.versions_data = default_versions
        else:
            self.versions_data = default_versions
            with open(VERSIONS_FILE, 'w', encoding='utf-8') as f:
                json.dump(default_versions, f, indent=4, ensure_ascii=False)

        # Update version selector
        version_names = [v["name"] for v in self.versions_data["versions"]]
        if hasattr(self, 'version_selector'):
            self.version_selector.configure(values=version_names)
            if self.config["selected_version"] in version_names:
                self.version_selector.set(self.config["selected_version"])
            elif version_names:
                self.version_selector.set(version_names[0])

    def setup_ui(self):
        """Setup the user interface"""

        # Main container with gradient effect (simulated with frames)
        self.main_frame = ctk.CTkFrame(self, fg_color="#1a1a2e")
        self.main_frame.pack(fill="both", expand=True, padx=0, pady=0)

        # Header with logo area
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="#16213e", height=100)
        self.header_frame.pack(fill="x", padx=20, pady=(20, 10))
        self.header_frame.pack_propagate(False)

        # Title
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="TWIX CLIENT",
            font=ctk.CTkFont(size=32, weight="bold"),
            text_color="#00d4ff"
        )
        self.title_label.pack(pady=25)

        # Content area
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="#1a1a2e")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Left panel - Game info
        self.left_panel = ctk.CTkFrame(self.content_frame, fg_color="#16213e", width=400)
        self.left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Game image placeholder (gradient effect)
        self.game_image_frame = ctk.CTkFrame(self.left_panel, fg_color="#0f3460", height=250)
        self.game_image_frame.pack(fill="x", padx=20, pady=20)
        self.game_image_frame.pack_propagate(False)

        # Large play button icon
        self.play_icon_label = ctk.CTkLabel(
            self.game_image_frame,
            text="▶",
            font=ctk.CTkFont(size=80),
            text_color="#00d4ff"
        )
        self.play_icon_label.pack(expand=True)

        # Version info
        self.version_info_label = ctk.CTkLabel(
            self.left_panel,
            text="Выберите версию игры",
            font=ctk.CTkFont(size=14),
            text_color="#a0a0a0"
        )
        self.version_info_label.pack(pady=(0, 10))

        # Right panel - Settings and controls
        self.right_panel = ctk.CTkFrame(self.content_frame, fg_color="#16213e", width=400)
        self.right_panel.pack(side="right", fill="both", expand=True)

        # Version selector
        self.version_label = ctk.CTkLabel(
            self.right_panel,
            text="Версия игры:",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff"
        )
        self.version_label.pack(pady=(20, 5), padx=20, anchor="w")

        self.version_selector = ctk.CTkComboBox(
            self.right_panel,
            values=["ALPHA 1.16.5"],
            command=self.on_version_change,
            width=360,
            height=40,
            font=ctk.CTkFont(size=14),
            dropdown_font=ctk.CTkFont(size=12)
        )
        self.version_selector.pack(pady=(0, 20), padx=20)
        self.version_selector.set(self.config["selected_version"])

        # RAM allocation
        self.ram_label = ctk.CTkLabel(
            self.right_panel,
            text=f"Выделенная RAM: {self.config['ram_allocated']} MB",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff"
        )
        self.ram_label.pack(pady=(10, 5), padx=20, anchor="w")

        # Get system RAM
        total_ram = psutil.virtual_memory().total // (1024 * 1024)  # Convert to MB

        self.ram_slider = ctk.CTkSlider(
            self.right_panel,
            from_=1024,
            to=min(total_ram, 16384),
            command=self.on_ram_change,
            width=360,
            height=20
        )
        self.ram_slider.pack(pady=(0, 10), padx=20)
        self.ram_slider.set(self.config["ram_allocated"])

        # RAM info
        self.ram_info_label = ctk.CTkLabel(
            self.right_panel,
            text=f"Доступно RAM: {total_ram} MB | Рекомендуется: 4096 MB",
            font=ctk.CTkFont(size=12),
            text_color="#a0a0a0"
        )
        self.ram_info_label.pack(pady=(0, 20), padx=20)

        # Game path info
        self.path_label = ctk.CTkLabel(
            self.right_panel,
            text=f"Путь установки:\n{GAME_PATH}",
            font=ctk.CTkFont(size=12),
            text_color="#a0a0a0",
            justify="left"
        )
        self.path_label.pack(pady=(10, 20), padx=20, anchor="w")

        # Status label
        self.status_label = ctk.CTkLabel(
            self.right_panel,
            text="Готов к запуску",
            font=ctk.CTkFont(size=14),
            text_color="#00ff00"
        )
        self.status_label.pack(pady=(10, 20), padx=20)

        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.right_panel, width=360)
        self.progress_bar.pack(pady=(0, 20), padx=20)
        self.progress_bar.set(0)
        self.progress_bar.pack_forget()  # Hide initially

        # Main action button (динамическая кнопка УСТАНОВИТЬ/ЗАПУСТИТЬ)
        self.main_action_button = ctk.CTkButton(
            self.right_panel,
            text="УСТАНОВИТЬ",
            command=self.handle_main_action,
            width=360,
            height=50,
            font=ctk.CTkFont(size=18, weight="bold"),
            fg_color="#00d4ff",
            hover_color="#0099cc",
            text_color="#000000"
        )
        self.main_action_button.pack(pady=(0, 20), padx=20)

        # Footer
        self.footer_frame = ctk.CTkFrame(self.main_frame, fg_color="#16213e", height=50)
        self.footer_frame.pack(fill="x", padx=20, pady=(10, 20))
        self.footer_frame.pack_propagate(False)

        self.footer_label = ctk.CTkLabel(
            self.footer_frame,
            text="Twix Client v1.0.0 | t.me/TwixClient",
            font=ctk.CTkFont(size=12),
            text_color="#666666"
        )
        self.footer_label.pack(pady=15)

        # Обновляем состояние кнопки при запуске
        self.update_main_button()

    def check_if_installed(self, version_name):
        """Проверяет, установлена ли игра"""
        version_path = os.path.join(GAME_PATH, version_name)
        if not os.path.exists(version_path):
            return False

        # Ищем исполняемый файл (JAR или EXE)
        for file in os.listdir(version_path):
            if file.endswith(('.jar', '.exe')):
                return True
        return False

    def update_main_button(self):
        """Обновляет текст и функцию главной кнопки в зависимости от статуса установки"""
        selected_version = self.version_selector.get()

        if self.check_if_installed(selected_version):
            # Игра установлена - показываем ЗАПУСТИТЬ
            self.main_action_button.configure(
                text="ЗАПУСТИТЬ",
                fg_color="#00d4ff",
                hover_color="#0099cc"
            )
            self.status_label.configure(text="Готов к запуску", text_color="#00ff00")
        else:
            # Игра не установлена - показываем УСТАНОВИТЬ
            self.main_action_button.configure(
                text="УСТАНОВИТЬ",
                fg_color="#4CAF50",
                hover_color="#45a049"
            )
            self.status_label.configure(text="Нажмите 'УСТАНОВИТЬ' для загрузки", text_color="#ff9800")

    def handle_main_action(self):
        """Обрабатывает нажатие на главную кнопку (установить или запустить)"""
        selected_version = self.version_selector.get()

        if self.check_if_installed(selected_version):
            # Игра установлена - запускаем
            self.launch_game()
        else:
            # Игра не установлена - скачиваем
            self.download_game()

    def on_version_change(self, choice):
        """Handle version selection change"""
        self.config["selected_version"] = choice
        self.save_config()
        self.update_main_button()

    def on_ram_change(self, value):
        """Handle RAM slider change"""
        ram_value = int(value)
        self.config["ram_allocated"] = ram_value
        self.ram_label.configure(text=f"Выделенная RAM: {ram_value} MB")
        self.save_config()

    def download_game(self):
        """Download game files"""
        selected_version = self.version_selector.get()

        # Find version data
        version_data = None
        for v in self.versions_data["versions"]:
            if v["name"] == selected_version:
                version_data = v
                break

        if not version_data:
            messagebox.showerror("Ошибка", "Версия не найдена")
            return

        if not version_data["download_url"]:
            messagebox.showinfo(
                "Информация",
                "URL для скачивания не настроен.\n\n"
                "Чтобы добавить ссылку на игру:\n"
                f"1. Откройте файл: {VERSIONS_FILE}\n"
                "2. Добавьте 'download_url' для нужной версии\n"
                "3. Перезапустите лаунчер"
            )
            return

        # Start download in separate thread
        self.main_action_button.configure(state="disabled")
        self.progress_bar.pack(pady=(0, 20), padx=20)
        self.progress_bar.set(0)

        thread = threading.Thread(target=self._download_thread, args=(version_data,))
        thread.daemon = True
        thread.start()

    def _download_thread(self, version_data):
        """Download game in background thread"""
        zip_file_path = None
        try:
            # Конвертируем Google Drive ссылку в прямую ссылку
            download_url = convert_google_drive_url(version_data["download_url"])

            self.status_label.configure(text="Скачивание...", text_color="#00d4ff")

            version_path = os.path.join(GAME_PATH, version_data["name"])
            os.makedirs(version_path, exist_ok=True)

            # Скачивание файла
            self.status_label.configure(text="Загрузка игры...", text_color="#00d4ff")
            response = requests.get(download_url, stream=True, allow_redirects=True)
            response.raise_for_status()  # Проверка на ошибки HTTP

            total_size = int(response.headers.get('content-length', 0))

            downloaded = 0
            chunk_size = 8192

            zip_file_path = os.path.join(version_path, "game.zip")

            # Скачивание с прогресс-баром
            with open(zip_file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = (downloaded / total_size) * 0.7  # 70% на скачивание
                            self.progress_bar.set(progress)

            # Распаковка архива
            self.status_label.configure(text="Распаковка файлов...", text_color="#00d4ff")
            self.progress_bar.set(0.7)

            if extract_zip(zip_file_path, version_path):
                self.progress_bar.set(0.9)

                # Удаление zip-файла после успешной распаковки
                try:
                    os.remove(zip_file_path)
                    zip_file_path = None
                except:
                    pass

                self.progress_bar.set(1.0)
                self.status_label.configure(text="Установка завершена!", text_color="#00ff00")

                # Обновляем статус установки в versions.json
                for v in self.versions_data["versions"]:
                    if v["name"] == version_data["name"]:
                        v["installed"] = True
                        break

                # Сохраняем обновленный versions.json
                try:
                    with open(VERSIONS_FILE, 'w', encoding='utf-8') as f:
                        json.dump(self.versions_data, f, indent=4, ensure_ascii=False)
                except:
                    pass

                # Обновляем кнопку на ЗАПУСТИТЬ
                self.update_main_button()
                self.main_action_button.configure(state="normal")

                messagebox.showinfo("Успех", f"Игра {version_data['name']} успешно установлена!\n\nНажмите 'ЗАПУСТИТЬ' чтобы играть")
            else:
                raise Exception("Не удалось распаковать архив")

        except requests.exceptions.RequestException as e:
            self.status_label.configure(text="Ошибка загрузки", text_color="#ff0000")
            messagebox.showerror("Ошибка", f"Не удалось скачать игру:\n\nПроверьте:\n- Интернет соединение\n- Правильность ссылки\n\nОшибка: {str(e)}")

        except Exception as e:
            self.status_label.configure(text=f"Ошибка: {str(e)}", text_color="#ff0000")
            messagebox.showerror("Ошибка", f"Не удалось установить игру:\n{e}")

            # Очистка при ошибке
            if zip_file_path and os.path.exists(zip_file_path):
                try:
                    os.remove(zip_file_path)
                except:
                    pass

        finally:
            self.main_action_button.configure(state="normal")
            self.progress_bar.pack_forget()

    def check_java_installed(self):
        """Проверяет, установлена ли Java"""
        try:
            result = subprocess.run(['java', '-version'],
                                  capture_output=True,
                                  text=True,
                                  timeout=5)
            return result.returncode == 0
        except:
            return False

    def launch_game(self):
        """Launch the game (поддержка JAR и EXE файлов)"""
        selected_version = self.version_selector.get()
        version_path = os.path.join(GAME_PATH, selected_version)

        if not os.path.exists(version_path):
            messagebox.showwarning(
                "Игра не найдена",
                f"Игра не установлена.\n\nНажмите 'УСТАНОВИТЬ' чтобы загрузить игру."
            )
            return

        # Ищем исполняемый файл (приоритет: JAR > EXE)
        jar_file = None
        exe_file = None

        for file in os.listdir(version_path):
            if file.endswith('.jar'):
                jar_file = os.path.join(version_path, file)
            elif file.endswith('.exe'):
                exe_file = os.path.join(version_path, file)

        try:
            self.status_label.configure(text="Запуск игры...", text_color="#00d4ff")

            # Если есть JAR файл - запускаем через Java
            if jar_file:
                # Проверяем наличие Java
                if not self.check_java_installed():
                    messagebox.showerror(
                        "Java не найдена",
                        "Для запуска игры требуется Java!\n\n"
                        "Скачайте и установите Java с:\n"
                        "https://www.java.com/download\n\n"
                        "После установки перезапустите лаунчер."
                    )
                    self.status_label.configure(text="Требуется Java", text_color="#ff0000")
                    return

                # Запускаем JAR с выделенной RAM
                ram_mb = self.config['ram_allocated']
                subprocess.Popen([
                    'java',
                    f'-Xmx{ram_mb}M',
                    f'-Xms{ram_mb // 2}M',  # Минимальная RAM = половина от максимальной
                    '-jar',
                    jar_file
                ], cwd=version_path)  # Устанавливаем рабочую директорию

                self.status_label.configure(text="Игра запущена!", text_color="#00ff00")

            # Если нет JAR, но есть EXE - запускаем EXE
            elif exe_file:
                subprocess.Popen([exe_file], cwd=version_path)
                self.status_label.configure(text="Игра запущена!", text_color="#00ff00")

            else:
                messagebox.showwarning(
                    "Игра не найдена",
                    f"Не найден исполняемый файл игры (.jar или .exe) в:\n{version_path}\n\n"
                    "Переустановите игру, нажав 'УСТАНОВИТЬ'."
                )
                self.status_label.configure(text="Файл игры не найден", text_color="#ff0000")
                return

            # Сохраняем последнюю играную версию
            self.config["last_played"] = selected_version
            self.save_config()

        except Exception as e:
            self.status_label.configure(text="Ошибка запуска", text_color="#ff0000")
            messagebox.showerror("Ошибка", f"Не удалось запустить игру:\n\n{str(e)}")

    def on_closing(self):
        """Handle window closing"""
        self.save_config()
        self.destroy()

def main():
    """Main entry point"""
    app = TwixLauncher()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()

if __name__ == "__main__":
    main()
