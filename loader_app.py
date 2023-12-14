import customtkinter
from os import mkdir
from threading import Thread
from pytube import YouTube, Playlist
from pytube.exceptions import RegexMatchError

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.pad = 10
        self.ver = 1.0
        self.button_text_color = "#DCE8EE"
        self.button_fg_color = "#5c1f53"
        self.button_hover_color = "#451e3f"
        self.button_hover_color_extra = "#341b30"
        self.video_resolution_mode = "Highest"

        # window
        self.title(f"YouTubeLoader v. {self.ver}")
        self.geometry("800x400")

        # grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # sidebar left frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=100, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Тема приложения:", font=customtkinter.CTkFont(size=10, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=self.pad, pady=(10, 10))

        # appearance mode option button
        self.sidebar_frame.grid_rowconfigure(1, weight=1)
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame, fg_color=self.button_fg_color, button_color=self.button_hover_color,
            dropdown_fg_color=self.button_hover_color_extra, button_hover_color=self.button_hover_color_extra,
            text_color=self.button_text_color, dropdown_text_color=self.button_text_color,
            dropdown_hover_color=self.button_hover_color, values=["System", "Dark", "Light"],
            command=self.change_appearance_mode_event
        )
        self.appearance_mode_optionemenu.grid(row=1, column=0, padx=(0, 0), pady=(0, 0))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")

        # scaling mode option button
        self.scaling_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Масштабирование:", font=customtkinter.CTkFont(size=10, weight="bold")
        )
        self.scaling_label.grid(row=2, column=0, padx=20, pady=(20, 10))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event
        )
        self.scaling_optionemenu.grid(row=3, column=0, padx=(0, 0), pady=(0, 0))

        # resolution mode
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame, text="Качество видео:", font=customtkinter.CTkFont(size=10, weight="bold")
        )
        self.logo_label.grid(row=6, column=0, padx=self.pad)

        # video resolution mode button
        self.sidebar_frame.grid_rowconfigure(2, weight=1)
        self.video_resolution = customtkinter.CTkOptionMenu(
            self.sidebar_frame, fg_color=self.button_fg_color, button_color=self.button_hover_color,
            dropdown_fg_color=self.button_hover_color_extra, button_hover_color=self.button_hover_color_extra,
            text_color=self.button_text_color, dropdown_text_color=self.button_text_color,
            dropdown_hover_color=self.button_hover_color, values=["Highest", "Lowest", "Audio"],
            command=self.get_video_resolution_mode
        )
        self.video_resolution.grid(row=7, column=0, padx=self.pad, pady=self.pad)
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")

        # playlist resolution mode button
        self.sidebar_frame.grid_rowconfigure(3, weight=1)
        self.playlist_resolution = customtkinter.CTkOptionMenu(
            self.sidebar_frame, fg_color=self.button_fg_color, button_color=self.button_hover_color,
            dropdown_fg_color=self.button_hover_color_extra, button_hover_color=self.button_hover_color_extra,
            text_color=self.button_text_color, dropdown_text_color=self.button_text_color,
            dropdown_hover_color=self.button_hover_color, values=["Highest", "Lowest", "Audio"],
            command=self.get_video_resolution_mode
        )
        self.playlist_resolution.grid(row=8, column=0, padx=self.pad, pady=self.pad)
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")

        # textbox
        self.textbox = customtkinter.CTkTextbox(self, text_color="#228b22")
        self.textbox.grid(row=1, column=1, padx=self.pad, pady=self.pad, sticky="nsew")

        # sidebar right frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=100, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=4, rowspan=4, sticky="nsew")

        # info entry and button
        self.info_button = customtkinter.CTkButton(
            master=self, fg_color=self.button_fg_color, hover_color=self.button_hover_color, text="Инфо",
            text_color=self.button_text_color, command=self.get_info
        )
        self.info_button.grid(row=1, column=4, padx=self.pad, pady=self.pad)

        # save video entry and button
        self.save_video_entry = customtkinter.CTkEntry(self, placeholder_text="Введи ссылку на видео с Youtube: ")
        self.save_video_entry.grid(row=2, column=1, columnspan=2, padx=self.pad, pady=self.pad, sticky="nsew")
        self.save_video_button = customtkinter.CTkButton(
            master=self, fg_color=self.button_fg_color, hover_color=self.button_hover_color, text="Скачать",
            text_color=self.button_text_color, command=self.download_video
        )
        self.save_video_button.grid(row=2, column=4, padx=self.pad, pady=self.pad, sticky="nsew")

        # save playlist entry and button
        self.save_playlist_entry = customtkinter.CTkEntry(self, placeholder_text="Введи ссылку на плейлист Youtube: ")
        self.save_playlist_entry.grid(row=3, column=1, columnspan=2, padx=self.pad, pady=self.pad, sticky="nsew")
        self.save_playlist_button = customtkinter.CTkButton(
            master=self, fg_color=self.button_fg_color, hover_color=self.button_hover_color, text="Скачать",
            text_color=self.button_text_color, command=self.download_playlist
        )
        self.save_playlist_button.grid(row=3, column=4, padx=self.pad, pady=self.pad, sticky="nsew")
        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

    def get_info(self):
        self.textbox.insert("1.0", "https://github.com/Kepler54/YouTubeLoader\n")

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
            self.textbox.insert("1.0", f'Идёт загрузка видео: "{data.title}"\n')
        except RegexMatchError:
            pass

    def get_playlist_info(self):
        try:
            data = Playlist(self.save_playlist_entry.get())
            self.textbox.insert("1.0", f'Идёт загрузка плейлиста: "{data.title}"\n')
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
            self.textbox.insert("1.0", "Введите ссылку на видео!\n")
            self.save_video_entry.delete(0, 1000000)

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
            self.textbox.insert("1.0", "Введите ссылку на плейлист!\n")
        except FileExistsError:
            self.textbox.insert("1.0", "Плейлист уже существует!\n")
            raise FileExistsError

    def download_video(self):
        Thread(target=self.save_video).start()
        Thread(target=self.get_video_info).start()

    def download_playlist(self):
        Thread(target=self.save_playlist).start()
        Thread(target=self.get_playlist_info).start()
