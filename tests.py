'''
    def change_video_resolution(self, new_video_resolution: str):
        data = YouTube(self.save_video_entry.get())
        if new_video_resolution == "highest":
            return data.streams.get_highest_resolution().download('Download/')
        elif new_video_resolution == "lowest":
            return data.streams.get_lowest_resolution().download('Download/')
        elif new_video_resolution == "audio":
            return data.streams.get_audio_only().download('Download/')
'''
