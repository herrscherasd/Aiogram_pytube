from pytube import YouTube
from pytube.exceptions import RegexMatchError

url = input("Ссылка: ")
try:
    yt = YouTube(url)
except RegexMatchError:
    raise ValueError("Неверный формат ссылки")

print(yt.title)
print(yt.author)
print("Скачиваем файл")

type = input("1 - mp4, 2 - mp3: ")
if type == "1":
    try:
        yt.streams.filter(progressive=True, file_extension="mp4").order_by('resolution').desc().first().download('video', f"{yt.title}.mp4")
    except OSError:
        yt.streams.filter(progressive=True, file_extension="mp4").order_by('resolution').desc().first().download('video', f"{yt.video_id}.mp4")
    print("Скачано")
elif type == "2":
    print("Начато скачивание аудио")
    yt.streams.filter(only_audio=True).first().download('audio', f'{yt.title}.mp3')
    print("Скачивание аудио файла завершено")
