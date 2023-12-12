'''
def download_video():
    list_of_links = []
    while True:
        dialog = customtkinter.CTkInputDialog(text="Введи ссылку на видео с Youtube: ", title="Video")
        links = str(dialog.get_input())
        if links == '':
            break
        list_of_links.append(links)
    for i in list_of_links:
        youtube = YouTube(i)
        youtube.streams.get_highest_resolution().download('Download/')
'''
