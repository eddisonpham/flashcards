import csv
import random

import pandas
from tkinter import *
import time

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    card.itemconfig(language, text="French", fill="black")
    card.itemconfig(word, text=current_card["French"], fill="black")
    card.itemconfig(background, image=front_photo)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    card.itemconfig(language, text="English", fill="white")
    card.itemconfig(word, text=current_card["English"], fill="white")
    card.itemconfig(background, image=back_photo)


def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


window = Tk()
front_photo = PhotoImage(file="images/card_front.png")
back_photo = PhotoImage(file="images/card_back.png")
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

card = Canvas(width=800, height=526)
background = card.create_image(400, 263, image=front_photo)
language = card.create_text(400, 150, text="French", font=("Ariel", 40, "italic"))
word = card.create_text(400, 263, text="trouve", font=("Ariel", 60, "bold"))
card.config(bg=BACKGROUND_COLOR, highlightthickness=0)
card.grid(row=0, column=0, columnspan=2)

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

next_card()

window.mainloop()
