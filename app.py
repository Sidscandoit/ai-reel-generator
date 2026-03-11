from flask import Flask, request, send_file
import yt_dlp
from moviepy.editor import *

app = Flask(__name__)

@app.route("/")
def home():
    return '''
    <h2>AI Reel Generator</h2>
    <form action="/generate" method="post" enctype="multipart/form-data">
    Reel Link:<br>
    <input type="text" name="link"><br><br>

    Upload Photos:<br>
    <input type="file" name="photos" multiple><br><br>

    <button type="submit">Generate Reel</button>
    </form>
    '''

@app.route("/generate", methods=["POST"])
def generate():

    link = request.form["link"]
    photos = request.files.getlist("photos")

    paths = []

    for p in photos:
        p.save(p.filename)
        paths.append(p.filename)

    with yt_dlp.YoutubeDL({"outtmpl":"reel.mp4"}) as ydl:
        ydl.download([link])

    video = VideoFileClip("reel.mp4")
    audio = video.audio

    duration = video.duration / len(paths)

    clips = []

    for img in paths:
        clip = ImageClip(img).set_duration(duration)
        clips.append(clip)

    final = concatenate_videoclips(clips)
    final = final.set_audio(audio)

    final.write_videofile("output.mp4", fps=30)

    return send_file("output.mp4", as_attachment=True)

app.run()
