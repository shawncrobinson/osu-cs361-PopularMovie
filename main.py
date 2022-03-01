import tkinter as tk
import json
import itertools
from tkcalendar import DateEntry
from PIL import Image, ImageTk

# Create list of most popular movies by year. Placeholder while service doesn't exist.
with open('movies.json') as f:
    temp = json.load(f)
movies = {}
for entry in temp:
    try:
        if len(entry["No. 1 Movie"]) > 0:
            movies[int(entry["Year"])] = {"Title": entry["No. 1 Movie"],
                                          "Box Office": entry["Combined\nWorldwide\nBox Office"],
                                          "Poster": "cats_00007.jpg",
                                          "Synopsis": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc "
                                                      "vehicula vulputate vulputate. Morbi tellus lorem, ultrices nec "
                                                      "sodales a, maximus quis odio. Lorem ipsum dolor sit amet, "
                                                      "consectetur adipiscing elit. Duis quis enim rhoncus, "
                                                      "dignissim urna sed, dignissim elit. Nunc aliquet turpis nec "
                                                      "aliquam feugiat."}
    except ValueError:
        pass

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

boxoffice_label = tk.Label(root, text="Box Office $:")
boxoffice_label.grid(column=0, row=4)

synopsis_label = tk.Label(root, text="Synopsis:")
synopsis_label.grid(column=0, row=5)

movie_labels = [title_label, boxoffice_label, synopsis_label]
for widget in movie_labels:
    widget.grid_remove()

# Movie info
INFO_WRAPLENGTH = 500
movie_title = tk.Label(root, height=1, wraplength=INFO_WRAPLENGTH)
movie_title.grid(columnspan=3, column=1, row=3)

movie_boxoffice = tk.Label(root, height=1, wraplength=INFO_WRAPLENGTH)
movie_boxoffice.grid(columnspan=3, column=1, row=4)

movie_synopsis = tk.Label(root, height=5, wraplength=INFO_WRAPLENGTH)
movie_synopsis.grid(columnspan=3, rowspan=3, column=1, row=5)

movie_text = [movie_title, movie_boxoffice, movie_synopsis]
for widget in movie_text:
    widget.grid_remove()

# Movie poster
movie_poster = tk.Label()
movie_poster.grid(rowspan=7, column=4, row=3)
movie_poster.grid_remove()


def update_movie(movie):
    img = Image.open("cats_00007.jpg")
    img = ImageTk.PhotoImage(img)
    movie_poster.configure(image=img)
    movie_poster.image = img

    movie_title.config(text=movie['Title'])
    movie_boxoffice.config(text=movie['Box Office'])
    movie_synopsis.config(text=movie['Synopsis'])

    for movie_widget in itertools.chain(movie_labels, movie_text, [movie_poster]):
        movie_widget.grid()


def get_movie(year):
    query_year = date.get_date().year
    if query_year < 1920:
        return None
    if query_year > 2022:
        query_year = query_year - 100
    # Determine movie to be displayed
    movie = None
    while movie is None:
        if query_year in movies.keys():
            movie = movies[query_year]
        else:
            query_year = query_year + 1

    return movie


def toggle_element(element):
    if element.winfo_viewable():
        element.grid_remove()
    else:
        element.grid()


def submit_date():
    query_year = date.get_date().year
    # Call service for info (Placeholder atm. Also unsure of final structure of movie object rn)
    movie = get_movie(query_year)
    if movie is not None:
        update_movie(movie)
    submit_text.set("Submit New Date")


root.mainloop()
