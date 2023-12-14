from ast import literal_eval

import customtkinter
from os import mkdir
from threading import Thread
from pytube import YouTube, Playlist
from pytube.exceptions import RegexMatchError
from http.client import RemoteDisconnected

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.pad = 10
        self.ver = 1.0
        self.button_text_color = "#c0c0c0"
        self.button_fg_color = "#552b55"
        self.button_hover_color = "#412641"
        self.button_hover_color_extra = "#341b30"
        self.video_resolution_mode = "Highest"

        # window
        self.title(f"YouTubeLoader v. {self.ver}")
        self.geometry("1000x500")

        # grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # sidebar left frame with widgets
        self.sidebar_frame_left = customtkinter.CTkFrame(self, width=100)
        self.sidebar_frame_left.grid(row=0, column=0, rowspan=4, sticky="nsew")

        # settings label
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame_left, text="Настройки:", font=customtkinter.CTkFont(size=10, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=self.pad, pady=(10, 0))

        # appearance mode option button
        self.sidebar_frame_left.grid_rowconfigure(1)
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame_left, fg_color=self.button_fg_color, button_color=self.button_hover_color,
            dropdown_fg_color=self.button_hover_color_extra, button_hover_color=self.button_hover_color_extra,
            text_color=self.button_text_color, dropdown_text_color=self.button_text_color,
            dropdown_hover_color=self.button_hover_color, values=["System", "Dark", "Light"],
            command=self.change_appearance_mode_event
        )
        self.appearance_mode_optionemenu.grid(row=1, column=0, padx=self.pad, pady=self.pad)

        # scaling mode option button
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame_left, fg_color=self.button_fg_color, button_color=self.button_hover_color,
            dropdown_fg_color=self.button_hover_color_extra, button_hover_color=self.button_hover_color_extra,
            text_color=self.button_text_color, dropdown_hover_color=self.button_hover_color,
            values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event
        )
        self.scaling_optionemenu.grid(row=2, column=0, padx=(0, 0), pady=(0, 0))

        # resolution mode
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame_left, text="Качество видео:", font=customtkinter.CTkFont(size=10, weight="bold")
        )
        self.logo_label.grid(row=6, column=0, padx=self.pad)

        # video resolution mode button
        self.sidebar_frame_left.grid_rowconfigure(2, weight=1)
        self.video_resolution = customtkinter.CTkOptionMenu(
            self.sidebar_frame_left, fg_color=self.button_fg_color, button_color=self.button_hover_color,
            dropdown_fg_color=self.button_hover_color_extra, button_hover_color=self.button_hover_color_extra,
            text_color=self.button_text_color, dropdown_text_color=self.button_text_color,
            dropdown_hover_color=self.button_hover_color, values=["Highest", "Lowest", "Audio"],
            command=self.get_video_resolution_mode
        )
        self.video_resolution.grid(row=7, column=0, padx=self.pad, pady=self.pad)
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame_left, anchor="w")

        # playlist resolution mode button
        self.sidebar_frame_left.grid_rowconfigure(3, weight=1)
        self.playlist_resolution = customtkinter.CTkOptionMenu(
            self.sidebar_frame_left, fg_color=self.button_fg_color, button_color=self.button_hover_color,
            dropdown_fg_color=self.button_hover_color_extra, button_hover_color=self.button_hover_color_extra,
            text_color=self.button_text_color, dropdown_text_color=self.button_text_color,
            dropdown_hover_color=self.button_hover_color, values=["Highest", "Lowest", "Audio"],
            command=self.get_video_resolution_mode
        )
        self.playlist_resolution.grid(row=8, column=0, padx=self.pad, pady=self.pad)
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame_left, anchor="w")

        # textbox
        self.textbox = customtkinter.CTkTextbox(self, text_color="#228b22")
        self.textbox.grid(row=1, column=1, padx=self.pad, pady=self.pad, sticky="nsew")

        # sidebar right frame with widgets
        self.sidebar_frame_right = customtkinter.CTkFrame(self, width=100)
        self.sidebar_frame_right.grid(row=0, column=3, rowspan=4, sticky="nsew")

        # info entry and button
        self.info_button = customtkinter.CTkButton(
            master=self, fg_color=self.button_fg_color, hover_color=self.button_hover_color, text="Инфо",
            text_color=self.button_text_color, command=self.get_info
        )
        self.info_button.grid(row=1, column=3, padx=self.pad, pady=(0, 0))

        # save video entry and button
        self.save_video_entry = customtkinter.CTkEntry(
            self, border_color=self.button_fg_color, placeholder_text="Введи ссылку на видео с Youtube: "
        )
        self.save_video_entry.grid(row=2, column=1, columnspan=2, padx=self.pad, pady=self.pad, sticky="nsew")
        self.save_video_button = customtkinter.CTkButton(
            master=self, fg_color=self.button_fg_color, hover_color=self.button_hover_color, text="Скачать",
            text_color=self.button_text_color, command=self.download_video
        )
        self.save_video_button.grid(row=2, column=3, padx=self.pad, pady=self.pad, sticky="nsew")

        # save playlist entry and button
        self.save_playlist_entry = customtkinter.CTkEntry(
            self, border_color=self.button_fg_color, placeholder_text="Введи ссылку на плейлист Youtube: "
        )
        self.save_playlist_entry.grid(row=3, column=1, columnspan=2, padx=self.pad, pady=self.pad, sticky="nsew")
        self.save_playlist_button = customtkinter.CTkButton(
            master=self, fg_color=self.button_fg_color, hover_color=self.button_hover_color, text="Скачать",
            text_color=self.button_text_color, command=self.download_playlist
        )
        self.save_playlist_button.grid(row=3, column=3, padx=self.pad, pady=self.pad, sticky="nsew")

        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

    def get_start_image(self):
        try:
            with open('images.spec') as img:
                image = literal_eval(img.read())
                self.textbox.insert("1.0", image)
        except FileNotFoundError:
            pass

    def get_info(self):
        self.textbox.insert(
            "1.0",
            f"\n{41 * '─'}\nhttps://github.com/Kepler54/YouTubeLoader\n© 2024 YouTubeLoader\n{41 * '─'}\n\n"
        )

    @staticmethod
    def change_appearance_mode_event(new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    @staticmethod
    def change_scaling_event(new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def get_video_resolution_mode(self, new_video_resolution_mode: str):
        self.video_resolution_mode = new_video_resolution_mode

    def get_video_info(self):
        try:
            data = YouTube(self.save_video_entry.get())
            self.textbox.insert("1.0", f"\n{41 * '─'}\nИдёт загрузка видео: '{data.title}'\n{41 * '─'}\n")
        except RegexMatchError:
            pass

    def get_playlist_info(self):
        try:
            data = Playlist(self.save_playlist_entry.get())
            self.textbox.insert("1.0", f"\n{41 * '─'}\nИдёт загрузка плейлиста: '{data.title}'\n{41 * '─'}\n")
        except KeyError:
            pass

    def save_video(self):
        try:
            data = YouTube(self.save_video_entry.get())
            self.save_video_entry.delete(0, 1000000)
            if self.video_resolution_mode == "Highest":
                return data.streams.get_highest_resolution().download('Download/')
            elif self.video_resolution_mode == "Lowest":
                return data.streams.get_lowest_resolution().download('Download/')
            elif self.video_resolution_mode == "Audio":
                return data.streams.get_audio_only().download('Download/')
        except RegexMatchError:
            self.textbox.insert("1.0", f"\n{41 * '─'}\nВведите ссылку на видео!\n{41 * '─'}\n")
            self.save_video_entry.delete(0, 1000000)
        except RemoteDisconnected:
            self.textbox.insert("1.0", f"\n{41 * '─'}\nНет подключения к Интернету!\n{41 * '─'}\n")

    def save_playlist(self):
        try:
            links = Playlist(self.save_playlist_entry.get())
            self.save_playlist_entry.delete(0, 1000000)
            mkdir(f'Download/{"_".join(links.title.split())}')
            for i in links.video_urls:
                data = YouTube(i)
                if self.video_resolution_mode == "Highest":
                    data.streams.get_highest_resolution().download(f'Download/{"_".join(links.title.split())}')
                elif self.video_resolution_mode == "Lowest":
                    data.streams.get_lowest_resolution().download(f'Download/{"_".join(links.title.split())}')
                elif self.video_resolution_mode == "Audio":
                    data.streams.get_audio_only().download(f'Download/{"_".join(links.title.split())}')
        except KeyError:
            self.textbox.insert("1.0", f"\n{41 * '─'}\nВведите ссылку на плейлист!\n{41 * '─'}\n")
        except FileExistsError:
            self.textbox.insert("1.0", f"\n{41 * '─'}\nПлейлист уже существует!\n{41 * '─'}\n")
        except RemoteDisconnected:
            self.textbox.insert("1.0", f"\n{41 * '─'}\nНет подключения к Интернету!\n{41 * '─'}\n")

    def download_video(self):
        Thread(target=self.save_video).start()
        Thread(target=self.get_video_info).start()

    def download_playlist(self):
        Thread(target=self.save_playlist).start()
        Thread(target=self.get_playlist_info).start()
