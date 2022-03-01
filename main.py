import tkinter as tk
import json
import itertools
import os
import requests
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from io import BytesIO

# Create canvas and root
root = tk.Tk()
canvas = tk.Canvas(root, width=1280, height=1000)
canvas.grid(columnspan=5, rowspan=13)

# Instructions
instructions = tk.Label(root, text="What was the highest grossing movie in the year you were born?\n\n"
                                   "Enter and submit your date of birth to find out.")
instructions.grid(columnspan=5, column=0, row=0)

help_box = tk.Label(root, width=30, height=7, wraplength=200, text="Enter a date into the box and press Submit to "
                                                                   "look up the highest grossing movie during your "
                                                                   "birth year. The date provided must be between "
                                                                   "1920 and 2022.")
help_box.grid(rowspan=2, columnspan=2, column=4, row=1)
help_box.grid_remove()

# Help Button
help_text = tk.StringVar()
help_text.set("Help")
help_button = tk.Button(root, textvariable=help_text, command=lambda: toggle_element(help_box), height=2, width=7,
                        bg="#FFFF00",
                        fg="#000000")
help_button.grid(column=4, row=0)

# Date Entry
date = DateEntry(root,
                 selectmode='day',
                 year=2022,
                 month=2,
                 day=14)
date.grid(columnspan=5, column=0, row=1)

# Submit Date Button
submit_text = tk.StringVar()
submit_text.set("Submit")
submit_button = tk.Button(root, textvariable=submit_text, command=lambda: submit_date(), height=2, width=13)
submit_button.grid(columnspan=5, column=0, row=2)

# Movie info labels (grid_remove() run to hide at app start)
title_label = tk.Label(root, text="Title:")
title_label.grid(column=0, row=3)

rating_label = tk.Label(root, text="Rating (out of 10):")
rating_label.grid(column=0, row=4)

genres_label = tk.Label(root, text="Genres:")
genres_label.grid(column=0, row=5)

synopsis_label = tk.Label(root, text="Synopsis:")
synopsis_label.grid(column=0, row=6, rowspan=4)

movie_labels = [title_label, rating_label, genres_label, synopsis_label]
for widget in movie_labels:
    widget.grid_remove()

# Movie info
INFO_WRAPLENGTH = 500
movie_title = tk.Label(root, height=1, wraplength=INFO_WRAPLENGTH)
movie_title.grid(columnspan=3, column=1, row=3)

movie_rating = tk.Label(root, height=1, wraplength=INFO_WRAPLENGTH)
movie_rating.grid(columnspan=3, column=1, row=4)

movie_genres = tk.Label(root, height=1, wraplength=INFO_WRAPLENGTH)
movie_genres.grid(columnspan=3, column=1, row=5)

movie_synopsis = tk.Label(root, height=5, wraplength=INFO_WRAPLENGTH)
movie_synopsis.grid(columnspan=3, rowspan=4, column=1, row=6)

movie_text = [movie_title, movie_rating, movie_genres, movie_synopsis]
for widget in movie_text:
    widget.grid_remove()

# Movie poster
movie_poster = tk.Label()
movie_poster.grid(rowspan=7, column=4, row=3)
movie_poster.grid_remove()


def update_movie(movie):
    img = Image.open("cats_00007.jpg")
    img = ImageTk.PhotoImage(img)

    # Update text fields
    movie_title.config(text=movie['title'])
    movie_rating.config(text=str(movie['rating']))  # movie['rating'] is an int
    movie_synopsis.config(text=movie['synopsis'])
    movie_genres.config(text=", ".join(movie['genre']))  # movie['genre'] is a list of genres, not a single genre

    # Fetch and update poster
    response = requests.get(movie['poster_path'])
    img = Image.open(BytesIO(response.content))

    img.thumbnail((270, 400), Image.ANTIALIAS)

    img = ImageTk.PhotoImage(img)
    movie_poster.configure(image=img)
    movie_poster.image = img

    for movie_widget in itertools.chain(movie_labels, movie_text, [movie_poster]):
        movie_widget.grid()


def get_movie(year):
    # Clear (and create if doesn't exist) file that the movie info service will write response to
    with open("movie_infos.json", "w") as io_file:
        io_file.truncate(0)

    # Call Amelia's movie info service
    os.system(f"python movieScraper.py {str(year)}")

    # Keep checking for file writes
    movie = None
    while movie is None:
        with open("movie_infos.json", "r") as io_file:
            if len(io_file.readlines()) > 0:
                io_file.seek(0)
                movie = json.load(io_file)

    return movie


def toggle_element(element):
    if element.winfo_viewable():
        element.grid_remove()
    else:
        element.grid()


def submit_date():
    query_year = date.get_date().year

    # region Workaround for an issue in tkcalendar
    # Selecting a 19XX date in the calendar converts to DD/MM/YY text, which causes get_date().year to return as 20XX
    if query_year < 1920:
        return None
    if query_year > 2022:
        query_year = query_year - 100
    # endregion

    movie = get_movie(query_year)
    if movie is not None:
        update_movie(movie)
    submit_text.set("Submit New Date")


root.mainloop()
