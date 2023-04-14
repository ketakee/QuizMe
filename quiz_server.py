from flask import Flask, request, Response
import openai
from youtube_transcript_api import YouTubeTranscriptApi
import json

app = Flask(__name__)

def get_transcript(videoid):
    srt = YouTubeTranscriptApi.get_transcript(videoid)
    text = [elem["text"] for elem in srt]
    return(" ".join(text))

#"Generate Quiz questions and options from this paragraph. Use small case letter for options and give 4 options for each question. Add answer after every question. Add two new lines before answer. Add --- and a new line before every question : "
def get_quiz_from_openai(text):
    openai.api_key = "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"
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Generate Quiz questions and options from this paragraph. Use small case letter for options and give 4 options for each question. Add answer for every question. Return the response in the format json where every entry has the keys question, options and answer " + text}]
    )
    # print(completion)
    questions = completion["choices"][0]["message"]["content"]
    return questions

@app.route("/home", methods=['GET'])
def home():
    return Response(
        response=json.dumps("HOME PAGE"), status=200, mimetype="text/plain")

@app.route('/quiz', methods=['POST'])
def get_quiz():
    # get the data URI from the request
    video_id = request.json.get('videoId')
    questions = get_quiz_from_openai(get_transcript(video_id))
    resp = Response(
        response=json.dumps(questions), status=200, mimetype="text/plain")
    return resp

if __name__ == '__main__':
    app.run()
