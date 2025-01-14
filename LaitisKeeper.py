import customtkinter
from ctypes import windll
from PIL import Image, ImageTk
import os
import zipfile
import getpass
from datetime import datetime
from tkinter import filedialog
import sys

# Константы
WINDOW_HEIGHT = 130  # Высота окна
WINDOW_WIDTH = 330   # Ширина окна
CENTER_WINDOW = True  # Центрировать окно по экрану (True или False)
ROUND_CORNER = 16  # Закругление углов окна (например, 12)
WINDOW_COLOR = "#f0f0f0"  # Мягкий белый цвет фона окна
WINDOW_FONT = "Segoe UI"  # Шрифт окна (например, "default" или "Arial")
WINDOW_FONT_SIZE = 16  # Размер шрифта окна (например, 12)
WINDOW_FONT_COLOR = "#333333"  # Темно-серый цвет шрифта окна
WINDOW_TRANSPARENCY = 0.97  # Прозрачность окна (0.0 - полностью прозрачное, 1.0 - непрозрачное)
TITLE_TEXT = "Laitis Keeper"  # Текст заголовка окна
TITLE_COLOR = "default"  # Цвет заголовка окна (например, "default" или "#FFFFFF")
TITLE_FONT = "Arial"  # Шрифт заголовка окна (например, "default" или "Arial")
TITLE_FONT_SIZE = 14  # Размер шрифта заголовка окна (например, 12)
TITLE_BUTTON_COLOR = "default"  # Цвет кнопок заголовка окна (например, "default" или "#FF0000")
TITLE_JUSTIFY = "left"  # Положение текста заголовка окна (например, "left", "center", "right")
ICON_SIZE = (16, 16)  # Размер иконки заголовка окна (например, (16, 16))
ALLOW_RESIZE = False  # Разрешить изменение размеров окна (например, True или False)
ALLOW_MOVE = True  # Разрешить изменение положения окна (например, True или False)
BUTTON_WIDTH = WINDOW_WIDTH - 50  # Ширина кнопок
BUTTON_FONT = "Segoe UI"  # Шрифт кнопок
BUTTON_FONT_SIZE = 14  # Размер шрифта кнопок
BUTTON_FONT_COLOR = "#333333"  # Цвет шрифта кнопок
BUTTON_BG_COLOR = "#e0e0e0"  # Цвет фона кнопок
BUTTON_HOVER_COLOR = "#c0c0c0"  # Цвет фона кнопок при наведении

class CTkWindow(customtkinter.CTk):
    def __init__(self, app_title=TITLE_TEXT, geometry=f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}", titlebar_color=TITLE_COLOR,
                 title_color=TITLE_COLOR, fg_color=WINDOW_COLOR, resizable=ALLOW_RESIZE, movable=ALLOW_MOVE,
                 icon=None, justify=TITLE_JUSTIFY, style="classic", app_icon=None):
        super().__init__()
        self.overrideredirect(1)
        transparent_color = self._apply_appearance_mode(['#f2f2f2', '#000001'])
        self.config(background=transparent_color)
        self.attributes("-transparentcolor", transparent_color)
        self.attributes("-alpha", WINDOW_TRANSPARENCY)
        self.geometry(geometry)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        if CENTER_WINDOW:
            self.center_window()

        self.x = self.winfo_x()
        self.y = self.winfo_y()
        self.fullscreen = False
        self.GWL_EXSTYLE = -20
        self.WS_EX_APPWINDOW = 0x00040000
        self.WS_EX_TOOLWINDOW = 0x00000080
        self.titlebar_color = ["#e0e0e0", "#c0c0c0"] if titlebar_color == "default" else titlebar_color
        title_color = ["#333333", "#222222"] if title_color == "default" else title_color
        self.header = customtkinter.CTkFrame(self, corner_radius=ROUND_CORNER, fg_color=self.titlebar_color,
                                             background_corner_colors=(transparent_color, transparent_color, None, None))
        self.header.grid(sticky="nwe", row=0)
        self.header.grid_columnconfigure(0, weight=1)
        self.header.grid_rowconfigure(0, weight=1)

        if movable:
            self.header.bind("<ButtonPress-1>", self.oldxyset)
            self.header.bind("<B1-Motion>", self.move_window)

        fg_color = customtkinter.ThemeManager.theme["CTk"]["fg_color"] if fg_color == "default" else fg_color

        self.app = customtkinter.CTkFrame(self, corner_radius=ROUND_CORNER, bg_color=transparent_color, fg_color=fg_color,
                                          background_corner_colors=(fg_color, fg_color, None, None))
        self.app.grid(sticky="nsew", row=0, pady=(29, 0))
        self.app.bind("<Map>", self.frame_mapped)

        if resizable:
            self.app.bind("<Motion>", self.change_cursor)
            self.app.bind("<B1-Motion>", self.resize)

        self.resizable = resizable
        self.ctkimage = self.create_icon(icon)

        if app_icon:
            self.iconbitmap(app_icon)

        self.title_label = customtkinter.CTkLabel(self.header, width=10, image=self.ctkimage, compound="left",
                                                 text=f"  {app_title}", anchor="n", text_color=WINDOW_FONT_COLOR,
                                                 font=(WINDOW_FONT, WINDOW_FONT_SIZE))
        if justify == "center":
            self.title_label.grid(row=0, sticky="we", padx=(30, 0), pady=7)
        else:
            self.title_label.grid(row=0, sticky="w", padx=(10, 0), pady=7)  # Уменьшили отступ слева

        self.title_label.bind("<ButtonPress-1>", self.oldxyset)
        self.title_label._label.bind("<ButtonPress-1>", self.oldxyset)
        self.title_label.bind("<B1-Motion>", self.move_window)
        self.minmize = False
        self.style = style
        self.create_buttons(transparent_color)

    def create_icon(self, icon):
        default_icon_path = os.path.join(os.path.dirname(customtkinter.__file__), "assets", "icons", "CustomTkinter_icon_Windows.ico")
        return customtkinter.CTkImage(Image.open(icon if icon else default_icon_path), size=ICON_SIZE)

    def create_buttons(self, transparent_color):
        if self.style == "modern":
            self.button_close = customtkinter.CTkButton(self.header, corner_radius=10, width=10, height=10, text="",
                                                       hover_color="#ff6666", fg_color="#ff0000", command=self.close_window,
                                                       font=(BUTTON_FONT, BUTTON_FONT_SIZE), text_color=BUTTON_FONT_COLOR)
            self.button_close.grid(row=0, column=2, sticky="ne", padx=(0, 15), pady=10)
            self.button_close.configure(cursor="arrow")
        else:
            self.button_close = customtkinter.CTkButton(self.header, corner_radius=ROUND_CORNER, width=40, height=30, text="✕",
                                                       hover_color="#ff6666", fg_color="transparent", text_color=["#333333", "#222222"],
                                                       background_corner_colors=(None, transparent_color, None, None), command=self.close_window,
                                                       font=(BUTTON_FONT, BUTTON_FONT_SIZE))
            self.button_close.grid(row=0, column=2, sticky="ne", padx=0, pady=0)
            self.button_close.configure(cursor="arrow")
            self.button_close.bind("<Enter>", lambda e: self.change_bg(transparent_color, 1), add="+")
            self.button_close.bind("<Leave>", lambda e: self.change_bg(transparent_color, 0), add="+")

        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_columnconfigure(2, weight=1)

        self.button_backup = customtkinter.CTkButton(self.app, text="Создать резервную копию настроек", width=BUTTON_WIDTH, command=self.create_backup,
                                                     font=(BUTTON_FONT, BUTTON_FONT_SIZE), text_color=BUTTON_FONT_COLOR, fg_color=BUTTON_BG_COLOR,
                                                     hover_color=BUTTON_HOVER_COLOR)
        self.button_backup.grid(row=1, column=1, pady=10, sticky="ew")

        self.button_restore = customtkinter.CTkButton(self.app, text="Восстановить настройки из резервной копии", width=BUTTON_WIDTH, command=self.restore_backup,
                                                      font=(BUTTON_FONT, BUTTON_FONT_SIZE), text_color=BUTTON_FONT_COLOR, fg_color=BUTTON_BG_COLOR,
                                                      hover_color=BUTTON_HOVER_COLOR)
        self.button_restore.grid(row=2, column=1, pady=10, sticky="ew")

    def create_backup(self):
        username = getpass.getuser()
        source_dir = f"C:\\Users\\{username}\\AppData\\Local\\Laitis"
        backup_dir = self.get_backup_dir()
        backup_file = os.path.join(backup_dir, f"laitis_config_{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.zip")

        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_dir)
                    zipf.write(file_path, arcname)
                for dir in dirs:
                    dir_path = os.path.join(root, dir)
                    arcname = os.path.relpath(dir_path, source_dir)
                    zipf.write(dir_path, arcname)

    def restore_backup(self):
        backup_dir = self.get_backup_dir()
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        file_path = filedialog.askopenfilename(
            title="Выберите файл резервной копии",
            initialdir=backup_dir,
            filetypes=(("ZIP files", "laitis_config*.zip"), ("All files", "*.*"))
        )
        if file_path:
            self.extract_backup(file_path)

    def extract_backup(self, file_path):
        username = getpass.getuser()
        extract_dir = f"C:\\Users\\{username}\\AppData\\Local\\Laitis"

        if not os.path.exists(extract_dir):
            os.makedirs(extract_dir)

        with zipfile.ZipFile(file_path, 'r') as zipf:
            zipf.extractall(extract_dir)

    def get_backup_dir(self):
        if getattr(sys, 'frozen', False):
            return os.path.join(os.path.dirname(sys.executable), "Backups")
        else:
            return os.path.join(os.path.dirname(os.path.abspath(__file__)), "Backups")

    def center_window(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - WINDOW_WIDTH) // 2
        y = (screen_height - WINDOW_HEIGHT) // 2
        self.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}')

    def change_bg(self, transparent_color, hover):
        if hover:
            self.button_close.configure(background_corner_colors=("#ff6666", transparent_color, "#ff6666", "#ff6666"), fg_color="#ff6666")
        else:
            self.button_close.configure(background_corner_colors=(self.titlebar_color, transparent_color, self.titlebar_color, self.titlebar_color),
                                        fg_color=self.titlebar_color)

    def geometry(self, geometry):
        super().geometry(geometry)

    def iconbitmap(self, icon):
        self.icon = customtkinter.CTkImage(Image.open(icon), size=ICON_SIZE)
        self.title_label.configure(image=self.icon)

    def oldxyset(self, event):
        self.oldx = event.x
        self.oldy = event.y

    def move_window(self, event):
        if self.fullscreen == False:
            self.y = event.y_root - self.oldy
            self.x = event.x_root - self.oldx
            self.geometry(f'+{self.x}+{self.y}')

    def close_window(self):
        super().destroy()

    def frame_mapped(self, e):
        self.update_idletasks()
        self.overrideredirect(True)
        self.state('normal')
        if self.minmize:
            self.fullscreen = False
            self.max_window()
        self.minmize = False

    def min_window(self):
        self.update_idletasks()
        self.overrideredirect(False)
        self.withdraw()
        self.state('iconic')
        if self.fullscreen:
            self.minmize = True

    def set_appwindow(self):
        hwnd = windll.user32.GetParent(self.winfo_id())
        style = windll.user32.GetWindowLongW(hwnd, self.GWL_EXSTYLE)
        style = style & ~self.WS_EX_TOOLWINDOW
        style = style | self.WS_EX_APPWINDOW
        res = windll.user32.SetWindowLongW(hwnd, self.GWL_EXSTYLE, style)
        self.wm_withdraw()
        self.after(10, lambda: self.wm_deiconify())

    def max_window(self):
        if self.resizable == True:
            if self.fullscreen == False:
                self.update_idletasks()
                self.overrideredirect(False)
                self.wm_state('zoomed')
                self.overrideredirect(True)
                self.after(10, lambda: self.set_appwindow())
                self.state('normal')
                self.fullscreen = True
                if self.style == "classic": self.button_close.configure(text="❒")
            else:
                self.geometry(f'+{self.x}+{self.y}')
                self.fullscreen = False
                if self.style == "classic": self.button_close.configure(text="□")

    def change_cursor(self, event):
        if (event.x in range(self.app.winfo_width() - 10, self.app.winfo_width())
                and event.y in range(self.app.winfo_height() - 10, self.app.winfo_height())):
            self.config(cursor="size_nw_se")
            return
        else:
            self.config(cursor="")

        if (event.x in range(self.app.winfo_width() - 5, self.app.winfo_width())
                and event.y in range(0, self.app.winfo_height())):
            self.config(cursor="sb_h_double_arrow")
            return
        else:
            self.config(cursor="")

        if (event.x in range(0, self.app.winfo_width())
                and event.y in range(self.app.winfo_height() - 5, self.app.winfo_height())):
            self.config(cursor="sb_v_double_arrow")
            return
        else:
            self.config(cursor="")

    def resize(self, event):
        if self.cget('cursor') == "size_nw_se":
            if event.x > 100 and event.y > 100:
                self.geometry(f"{event.x_root - self.x}x{event.y_root - self.y}")
        elif self.cget('cursor') == "sb_h_double_arrow":
            self.geometry(f"{event.x_root - self.x}x{self.winfo_height()}")
        elif self.cget('cursor') == "sb_v_double_arrow":
            self.geometry(f"{self.winfo_width()}x{event.y_root - self.y}")

    def configure(self, **kwargs):
        if "titlebar_color" in kwargs:
            self.titlebar_color = kwargs["titlebar_color"]
            self.header.configure(fg_color=self.titlebar_color)
        if "title" in kwargs:
            self.title_label.configure(text=f"  {kwargs['title']}")
        if "icon" in kwargs:
            self.icon = customtkinter.CTkImage(Image.open(kwargs["icon"]), size=ICON_SIZE)
            self.title_label.configure(image=self.icon)
        if "fg_color" in kwargs:
            self.app.configure(fg_color=fg_color)
        if "title_color" in kwargs:
            self.title_label.configure(text_color=kwargs['title_color'])

if __name__ == "__main__":
    window = CTkWindow()
    window.mainloop()