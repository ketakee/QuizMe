# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import openai
from youtube_transcript_api import YouTubeTranscriptApi


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

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


def get_formatted_question(question_text):
    question = question_text.split("\n")
    return question

def format_quiz(text):
    questions = text.split("---")
    question_bank = []
    print(questions)
    questions = list(filter(None, questions))
    for elem in questions:
        new_question={}
        question_entry = elem.split("\n\n")
        print(question_entry)
        question_entry = list(filter(None, question_entry))
        question_options = get_formatted_question(question_entry[0])
        new_question["question"] = question_options[0]
        new_question["options"] = question_options[1:]
        new_question["answer"] = question_entry[1]
        # print(new_question)
        question_bank.append(new_question)
    return question_bank



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    transcript = get_transcript("xpy_rAWSWkA")
    quiz = get_quiz_from_openai(transcript)
    print(quiz)
    # response = format_quiz(quiz)
    # for elem in response:
    #     print(elem)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
