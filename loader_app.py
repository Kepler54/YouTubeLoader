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
        self.button_text_color = "#DCE8EE"
        self.button_fg_color = "#5c1f53"
        self.button_hover_color = "#451e3f"
        self.button_hover_color_extra = "#341b30"

        # window
        self.title("YouTubeLoader")
        self.geometry("800x400")

        # grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # textbox
        self.textbox = customtkinter.CTkTextbox(self)
        self.textbox.grid(row=1, column=1, padx=self.pad, pady=self.pad, sticky="nsew")

        # sidebar left frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=100, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")

        # video resolution mode button
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.video_resolution = customtkinter.CTkOptionMenu(
            self.sidebar_frame, fg_color=self.button_fg_color, button_color=self.button_hover_color,
            dropdown_fg_color=self.button_hover_color_extra, button_hover_color=self.button_hover_color_extra,
            text_color=self.button_text_color, dropdown_text_color=self.button_text_color,
            dropdown_hover_color=self.button_hover_color, values=["Highest", "Lowest", "Audio"],
            command=self.change_appearance_mode_event
        )
        self.video_resolution.grid(row=5, column=0, padx=self.pad, pady=self.pad)
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")

        # playlist resolution mode button
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.playlist_resolution = customtkinter.CTkOptionMenu(
            self.sidebar_frame, fg_color=self.button_fg_color, button_color=self.button_hover_color,
            dropdown_fg_color=self.button_hover_color_extra, button_hover_color=self.button_hover_color_extra,
            text_color=self.button_text_color, dropdown_text_color=self.button_text_color,
            dropdown_hover_color=self.button_hover_color, values=["Highest", "Lowest", "Audio"],
            command=self.change_appearance_mode_event
        )
        self.playlist_resolution.grid(row=6, column=0, padx=self.pad, pady=self.pad)
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")

        # appearance mode option button
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame, fg_color=self.button_fg_color, button_color=self.button_hover_color,
            dropdown_fg_color=self.button_hover_color_extra, button_hover_color=self.button_hover_color_extra,
            text_color=self.button_text_color, dropdown_text_color=self.button_text_color,
            dropdown_hover_color=self.button_hover_color, values=["System", "Dark", "Light"],
            command=self.change_appearance_mode_event
        )
        self.appearance_mode_optionemenu.grid(row=1, column=0, padx=self.pad, pady=self.pad)
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")

        # sidebar right frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=100, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=4, rowspan=4, sticky="nsew")

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

    @staticmethod
    def change_appearance_mode_event(new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def get_video_info(self):
        data = YouTube(self.save_video_entry.get())
        self.textbox.insert("1.0", f'Идёт загрузка видео: "{data.title}"\n')

    def get_playlist_info(self):
        try:
            data = Playlist(self.save_playlist_entry.get())
            self.textbox.insert("1.0", f'Идёт загрузка плейлиста: "{data.title}"\n')
        except KeyError:
            self.textbox.insert("1.0", "Введите ссылку на плейлист!\n")

    def clear_video_placeholder(self):
        self.save_video_entry.delete(0, 1000000)

    def clear_playlist_placeholder(self):
        self.save_playlist_entry.delete(0, 1000000)

    def save_video(self):
        try:
            data = YouTube(self.save_video_entry.get())
            self.clear_video_placeholder()
            return data.streams.get_highest_resolution().download('Download/')
        except RegexMatchError:
            self.textbox.insert("1.0", "Введите ссылку на видео!\n")

    def save_playlist(self):
        links = Playlist(self.save_playlist_entry.get())
        self.clear_playlist_placeholder()
        mkdir(f'Download/{"_".join(links.title.split())}')
        for i in links.video_urls:
            data = YouTube(i)
            data.streams.get_highest_resolution().download(f'Download/{"_".join(links.title.split())}')

    def download_video(self):
        Thread(target=self.save_video).start()
        Thread(target=self.get_video_info).start()

    def download_playlist(self):
        Thread(target=self.save_playlist).start()
        Thread(target=self.get_playlist_info).start()
