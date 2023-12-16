import customtkinter
from os import mkdir
from threading import Thread
from ast import literal_eval
from pytube import YouTube, Playlist, exceptions
from pytube.exceptions import RegexMatchError
from http.client import RemoteDisconnected, IncompleteRead

customtkinter.set_appearance_mode("System")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.pad = 10
        self.ver = 1.0
        self.line = 67
        self.row_first = 0
        self.row_second = 1
        self.row_third = 2
        self.row_fourth = 3
        self.col_first = 0
        self.col_second = 1
        self.col_third = 2
        self.txt_clr = "#c0c0c0"
        self.fg_clr = "#19476b"
        self.hvr_clr = "#1b384f"
        self.clr_ext = "#1a2c3b"
        self.video_resolution_mode = "Highest"

        # window
        self.title(f"YouTubeLoader v. {self.ver} (Beta)")
        self.geometry("900x450")

        # grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # sidebar frame left, right with widgets and textbox
        self.sidebar_frame_left = customtkinter.CTkFrame(self, width=1)
        self.sidebar_frame_left.grid(row=self.row_second, column=self.col_first, rowspan=3, sticky="nsew")
        self.sidebar_frame_right = customtkinter.CTkFrame(self, width=1)
        self.sidebar_frame_right.grid(row=self.row_second, column=self.col_third, rowspan=3, sticky="nsew")
        self.textbox = customtkinter.CTkTextbox(self, width=1, text_color="#6c4e86")
        self.textbox.grid(row=self.row_second, column=self.col_second, padx=self.pad, pady=self.pad, sticky="nsew")

        # appearance mode option button
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame_left, fg_color=self.fg_clr, button_color=self.hvr_clr, dropdown_fg_color=self.clr_ext,
            button_hover_color=self.clr_ext, text_color=self.txt_clr, dropdown_text_color=self.txt_clr,
            dropdown_hover_color=self.hvr_clr, values=["System", "Dark", "Light"], command=self.change_appearance_mode
        )
        self.appearance_mode_optionemenu.grid(row=self.row_first, column=self.col_first, padx=self.pad, pady=self.pad)

        # scaling mode option button
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(
            self.sidebar_frame_left, fg_color=self.fg_clr, button_color=self.hvr_clr, dropdown_fg_color=self.clr_ext,
            button_hover_color=self.clr_ext, text_color=self.txt_clr, dropdown_hover_color=self.hvr_clr,
            values=["80%", "90%", "100%", "110%", "120%"], command=self.change_scaling_event
        )
        self.scaling_optionemenu.grid(row=self.row_second, column=self.col_first, padx=self.pad, pady=(0, 50))

        # video resolution mode button
        self.sidebar_frame_left.grid_rowconfigure(1, weight=1)
        self.video_resolution = customtkinter.CTkOptionMenu(
            self.sidebar_frame_left, fg_color=self.fg_clr, button_color=self.hvr_clr, dropdown_fg_color=self.clr_ext,
            button_hover_color=self.clr_ext, text_color=self.txt_clr, dropdown_text_color=self.txt_clr,
            dropdown_hover_color=self.hvr_clr, values=["Highest", "Lowest", "Audio"], command=self.get_resolution_mode
        )
        self.video_resolution.grid(row=self.row_third, column=self.col_first, padx=self.pad, pady=self.pad)
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame_left, anchor="w")

        # playlist resolution mode button
        self.sidebar_frame_left.grid_rowconfigure(1, weight=1)
        self.playlist_resolution = customtkinter.CTkOptionMenu(
            self.sidebar_frame_left, fg_color=self.fg_clr, button_color=self.hvr_clr, dropdown_fg_color=self.clr_ext,
            button_hover_color=self.clr_ext, text_color=self.txt_clr, dropdown_text_color=self.txt_clr,
            dropdown_hover_color=self.hvr_clr, values=["Highest", "Lowest", "Audio"], command=self.get_resolution_mode
        )
        self.playlist_resolution.grid(row=self.row_fourth, column=self.col_first, padx=self.pad, pady=self.pad)
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame_left, anchor="w")

        # YouTubeLoader label
        self.logo_label = customtkinter.CTkLabel(
            self.sidebar_frame_right, text="YouTubeLoader", font=customtkinter.CTkFont(size=15, weight="bold")
        )
        self.logo_label.grid(row=self.row_first, column=self.col_third, padx=self.pad, pady=self.pad)

        # info entry and button
        self.info_button = customtkinter.CTkButton(
            master=self, fg_color=self.fg_clr, hover_color=self.hvr_clr,
            text="Инфо", text_color=self.txt_clr, command=self.get_info
        )
        self.info_button.grid(row=self.row_second, column=self.col_third, padx=self.pad, pady=self.pad)

        # save video entry and button
        self.save_video_entry = customtkinter.CTkEntry(
            self, border_color=self.clr_ext, placeholder_text="Введи ссылку на видео с Youtube: "
        )
        self.save_video_entry.grid(
            row=self.row_third, column=self.col_second, columnspan=1, padx=self.pad, pady=self.pad, sticky="nsew"
        )
        self.save_video_button = customtkinter.CTkButton(
            master=self, fg_color=self.fg_clr, hover_color=self.hvr_clr,
            text="Скачать", text_color=self.txt_clr, command=self.download_video
        )
        self.save_video_button.grid(
            row=self.row_third, column=self.col_third, padx=self.pad, pady=self.pad, sticky="nsew"
        )

        # save playlist entry and button
        self.save_playlist_entry = customtkinter.CTkEntry(
            self, border_color=self.clr_ext, placeholder_text="Введи ссылку на плейлист Youtube: "
        )
        self.save_playlist_entry.grid(
            row=self.row_fourth, column=self.col_second, columnspan=1, padx=self.pad, pady=self.pad, sticky="nsew"
        )
        self.save_playlist_button = customtkinter.CTkButton(
            master=self, fg_color=self.fg_clr, hover_color=self.hvr_clr, text="Скачать",
            text_color=self.txt_clr, command=self.download_playlist
        )
        self.save_playlist_button.grid(
            row=self.row_fourth, column=self.col_third, padx=self.pad, pady=self.pad, sticky="nsew"
        )

        # set default values
        self.appearance_mode_optionemenu.set("System")
        self.scaling_optionemenu.set("100%")

    def get_start_image(self):
        try:
            with open('images.spec', encoding='UTF-8') as img:
                self.textbox.insert("1.0", literal_eval(img.read()))
        except (FileNotFoundError, SyntaxError):
            pass

    def get_info(self):
        self.textbox.insert(
            "1.0",
            f"\n{self.line * '─'}\nhttps://github.com/Kepler54/YouTubeLoader\n"
            f"© 2024 YouTubeLoader v. {self.ver} (Beta)\n{self.line * '─'}\n\n"
        )

    @staticmethod
    def change_appearance_mode(new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    @staticmethod
    def change_scaling_event(new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def get_resolution_mode(self, new_video_resolution_mode: str):
        self.video_resolution_mode = new_video_resolution_mode

    def get_video_info(self):
        try:
            data = YouTube(self.save_video_entry.get())
            self.textbox.insert(
                "1.0", f"\n{self.line * '─'}\nИдёт загрузка видео: '{data.title}'\n{self.line * '─'}\n"
            )
        except RegexMatchError:
            pass

    def get_playlist_info(self):
        try:
            data = Playlist(self.save_playlist_entry.get())
            self.textbox.insert(
                "1.0", f"\n{self.line * '─'}\nИдёт загрузка плейлиста: '{data.title}'\n{self.line * '─'}\n"
            )
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
            self.textbox.insert("1.0", f"\n{self.line * '─'}\nВведите ссылку на видео!\n{self.line * '─'}\n")
            self.save_video_entry.delete(0, 1000000)
        except RemoteDisconnected:
            self.textbox.insert("1.0", f"\n{self.line * '─'}\nНет подключения к Интернету!\n{self.line * '─'}\n")
        except exceptions.AgeRestrictedError:
            self.textbox.insert("1.0", f"\n{self.line * '─'}\nВидео имеет возрастные ограничения!\n{self.line * '─'}\n")
        except exceptions.LiveStreamError:
            self.textbox.insert("1.0", f"\n{self.line * '─'}\nПодождите завершения прямого эфира!\n{self.line * '─'}\n")
        except exceptions.VideoUnavailable:
            self.textbox.insert("1.0", f"\n{self.line * '─'}\nДанный видос больше не доступен...\n{self.line * '─'}\n")
        except IncompleteRead:
            self.textbox.insert("1.0", f"\n{self.line * '─'}\nНе удалось скачать видео!\n{self.line * '─'}\n")
        except KeyboardInterrupt:
            self.textbox.insert("1.0", f"\n{self.line * '─'}\nПрограмма прервана!\n{self.line * '─'}\n")

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
        except RegexMatchError:
            self.textbox.insert("1.0", f"\n{self.line * '─'}\nВведите ссылку на плейлист!\n{self.line * '─'}\n")
        except RemoteDisconnected:
            self.textbox.insert("1.0", f"\n{self.line * '─'}\nНет подключения к Интернету!\n{self.line * '─'}\n")
        except exceptions.AgeRestrictedError:
            self.textbox.insert("1.0", f"\n{self.line * '─'}\nВидео имеет возрастные ограничения!\n{self.line * '─'}\n")
        except exceptions.LiveStreamError:
            self.textbox.insert("1.0", f"\n{self.line * '─'}\nПодождите завершения прямого эфира!\n{self.line * '─'}\n")
        except exceptions.VideoUnavailable:
            self.textbox.insert("1.0", f"\n{self.line * '─'}\nПлейлист больше не доступен!\n{self.line * '─'}\n")
        except IncompleteRead:
            self.textbox.insert("1.0", f"\n{self.line * '─'}\nНе удалось скачать видео!\n{self.line * '─'}\n")
        except KeyError:
            self.textbox.insert("1.0", f"\n{self.line * '─'}\nВведите ссылку на плейлист!\n{self.line * '─'}\n")
        except FileExistsError:
            self.textbox.insert("1.0", f"\n{self.line * '─'}\nПлейлист уже существует!\n{self.line * '─'}\n")
        except KeyboardInterrupt:
            pass

    def download_video(self):
        Thread(target=self.save_video).start()
        Thread(target=self.get_video_info).start()

    def download_playlist(self):
        Thread(target=self.save_playlist).start()
        Thread(target=self.get_playlist_info).start()
