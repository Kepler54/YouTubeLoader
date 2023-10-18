from pytube import YouTube, Playlist, exceptions
from pytube.helpers import DeferredGeneratorList


class ConsoleLoader:
    @staticmethod
    def get_video_links() -> list:
        """
        Links of video entering function
        :return: list
        """
        list_of_links = []
        while True:
            link = input("Введи ссылку на видео с Youtube: ")
            if link == '':
                break
            list_of_links.append(link)
        return list_of_links

    @staticmethod
    def get_playlist_links() -> DeferredGeneratorList:
        """
        Links of playlist entering function
        :return: DeferredGeneratorList
        """
        link = Playlist(input("Введи ссылку на плейлист Youtube: "))
        return link.video_urls

    def download_choose_method(self) -> list | DeferredGeneratorList:
        """
        Function to choose between downloading videos or a playlist
        :return: list | DeferredGeneratorList
        """
        video_or_playlist = input("Скачать отдельные видео или плейлист? ")
        if video_or_playlist.lower() == 'видео' or video_or_playlist.lower() == 'в':
            return self.get_video_links()
        if video_or_playlist.lower() == 'плейлист' or video_or_playlist.lower() == 'п':
            return self.get_playlist_links()
        print("Неверный ввод!")

    def download_video(self) -> None:
        """
        The function takes a list of links and downloads the video for each of them
        :return: None
        """
        try:
            for i in self.download_choose_method():
                youtube = YouTube(i)

                print(f'\nИдёт загрузка видео: "{youtube.title}"\n')
                youtube.streams.get_highest_resolution().download('Download/')
                print(f"\nАвтор: {youtube.author}\nОписание: {youtube.description}\n")
                print("\nЗагрузка завершена!\n")

        except exceptions.RegexMatchError:
            print("\nБитая ссылка...\n")  # не останавливать загрузку при битой ссылке
        except exceptions.AgeRestrictedError:
            print("\nВидос имеет возрастные ограничения!\n")
        except exceptions.LiveStreamError:
            print("\nПопробуй скачать видео после завершения прямого эфира...\n")
        except exceptions.VideoUnavailable:
            print("\nДанный видос больше не доступен...\n")
        except KeyboardInterrupt:
            print("\nПрограмма прервана!\n")
        except:
            pass
