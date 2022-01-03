import json
import tkinter as tk
import validators
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi
from tkinter import filedialog
from keybert import KeyBERT


def kw(doc):
    kw_model = KeyBERT()
    with open('keywords.txt', "w") as kw:
        keywords = kw_model.extract_keywords(doc,keyphrase_ngram_range=(1, 1), stop_words=None)
        kw.write(str(keywords))
    with open('keywordsphrases.txt', "w") as kp:
        keywphrases = kw_model.extract_keywords(doc,keyphrase_ngram_range=(1, 2), stop_words=None)
        kw.write(str(keywphrases))
    

summed = ""

def generate_transcript(id):
	transcript = YouTubeTranscriptApi.get_transcript(id,languages=('en','en-IN'))
	script = ""

	for text in transcript:
		t = text["text"]
		if t != '[Music]':
			script += t + " "
		
	return script


def check_yt(url):
    if url:
        if validators.url(url):
            if "youtube.com" in url or "youtu.be" in url:
                url = url.split('/')[-1]
                url = url.split("watch?v=")[-1]
                return generate_transcript(url)

            else:
                return "Not a youtube link"
        else:
            return "Please check it is not a link!"
    else:
        return "blank"


def summarize(text):
    summarizer = pipeline("summarization")
    summarized = summarizer(text, min_length=50, max_length=300, truncation=True)
    return summarized


win = tk.Tk()

win.geometry("520x530")
win['bg'] = "grey20"
url = tk.StringVar()
title = tk.Frame(win, bg="grey20")
title.pack()
body = tk.Frame(win, bg='grey20')
body.pack()
lb3 = tk.Text(body, fg="white", bg="grey18", height=20, width=40)
lb = tk.Label(title,text="Quickie lecture", font="Calibri 23 bold", fg="white", bg="grey20")
lb.pack(anchor="center",  pady=25)



def sub_():
    tk.messagebox.showinfo("Wait..",  "Processing...pls wait......")
    summ = summarize(check_yt(url.get()))[0]['summary_text']
    summed = summ
    lb3.insert(tk.END, summed)
    kw(check_yt(url.get()))
    tk.messagebox.showinfo("info",  "Keywords and key phrases have been saved.")
    

lb2 = tk.Label(body,text="Enter Url: ", font="Arial 13 bold", fg="white", bg="grey18")
lb2.grid(row=0,column=0,padx=10)
sub = tk.Button(body, text= "Submit",fg="white", bg="grey18", command=sub_).grid(row=0,column=2, padx=10)
urlEnt = tk.Entry(body, textvariable = url, font=('calibre',13,'normal'), fg="white", bg="grey18", width=20).grid(row=0,column=1)
lb4 = tk.Label(body,text="Summary:", font="Arial 13 bold", fg="white", bg="grey18")
lb4.grid(row=1,column=1, pady=10)

lb3.grid(row=2,column=1)

win.mainloop()

