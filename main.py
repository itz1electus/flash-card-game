from tkinter import *
import pandas as pd
from random import choice


# Constants -->
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
records = {}


# Reading CSV file -->
try:
    data = pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/french_words.csv")
    records = original_data.to_dict(orient="records")
else:
    records = data.to_dict(orient="records")


# Card input logic -->
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = choice(records)
    french_word = current_card["French"]
    canvas.itemconfig(lang_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=french_word, fill="black")
    canvas.itemconfig(canvas_image, image=card_front_image)
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    english_word = current_card["English"]
    canvas.itemconfig(canvas_image, image=card_back_image)
    canvas.itemconfig(lang_text, fill="white")
    canvas.itemconfig(lang_text, text="English")
    canvas.itemconfig(word_text, fill="white")
    canvas.itemconfig(word_text, text=english_word)


def is_known():
    records.remove(current_card)
    print(len(records))
    new_data = pd.DataFrame(records)
    new_data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# User interface -->
window = Tk()
window.title("Flashy")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 263, image=card_front_image)
lang_text = canvas.create_text(400, 150, text="", fill="black", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="", fill="black", font=("Ariel", 60, "bold"))
canvas.grid(row=1, column=1, columnspan=2)

wrong_button_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=wrong_button_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=next_card)
unknown_button.grid(row=2, column=1)

okay_button_image = PhotoImage(file="images/right.png")
known_button = Button(image=okay_button_image, highlightthickness=0, bg=BACKGROUND_COLOR, command=is_known)
known_button.grid(row=2, column=2)

next_card()

window.mainloop()
