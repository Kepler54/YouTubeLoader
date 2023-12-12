import tkinter
import customtkinter
from pytube import YouTube, Playlist

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # window
        self.title("YouTubeLoader")
        self.geometry("1000x380")

        # grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=160, corner_radius=4)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Настрайки", font=customtkinter.CTkFont(size=15)
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(15, 15), pady=(20, 10), sticky="nsew")

        # main entry and button
        self.entry1 = customtkinter.CTkEntry(self, placeholder_text="Введи ссылку на видео с Youtube: ")
        self.entry1.grid(row=2, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.main_button_1 = customtkinter.CTkButton(
            master=self, fg_color="transparent", border_width=2, text="Скачать",
            text_color=("gray10", "#DCE4EE"), command=self.download_video
        )
        self.main_button_1.grid(row=2, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # main entry and button
        self.entry2 = customtkinter.CTkEntry(self, placeholder_text="Введи ссылку на плейлист Youtube: ")
        self.entry2.grid(row=3, column=1, columnspan=2, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.main_button_2 = customtkinter.CTkButton(
            master=self, fg_color="transparent", border_width=2, text="Скачать",
            text_color=("gray10", "#DCE4EE"), command=self.download_playlist
        )
        self.main_button_2.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

    def download_video(self):
        youtube = YouTube(self.entry1.get())
        self.textbox.insert("1.0", f'Идёт загрузка видео: "{youtube.title}"\n')
        self.textbox.insert("2.0", f"Автор: {youtube.author}\n")
        self.textbox.insert("3.0", f"Описание: {youtube.description}\n")
        youtube.streams.get_highest_resolution().download('Download/')
        self.textbox.insert("4.0", 'Загрузка завершена!')

    def download_playlist(self):
        global youtube
        links = Playlist(self.entry2.get())
        for i in links.video_urls:
            youtube = YouTube(i)
            youtube.streams.get_highest_resolution().download('Download/')
        self.textbox.insert("1.0", f'Идёт загрузка видео: "{youtube.title}"\n')
        self.textbox.insert("2.0", f"Автор: {youtube.author}\n")
        self.textbox.insert("3.0", f"Описание: {youtube.description}\n")
        self.textbox.insert("4.0", 'Загрузка завершена!')
