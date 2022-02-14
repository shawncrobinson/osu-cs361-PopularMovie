import tkinter as tk
import json
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
canvas = tk.Canvas(root, width=1280, height=720)
canvas.grid(columnspan=5, rowspan=10)

# Instructions
instructions = tk.Label(root, text="What was the highest grossing movie in the year you were born?\n"
                                   "Enter and submit your date of birth.")
instructions.grid(columnspan=5, column=0, row=0)

# Help Button
help_text = tk.StringVar()
help_text.set("?")
help_button = tk.Button(root, textvariable=help_text)
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

# Dynamic Widgets -- Not initially displayed or filled in
dynamic_labels = []
dynamic_widgets = []

def destroy_dynamic_widgets():
    for widget in dynamic_widgets:
        dynamic_widgets.remove(widget)
        widget.destroy()

def create_dynamic_labels():
    title_label = tk.Label(root, text="Title:")
    title_label.grid(column=0, row=3)
    dynamic_labels.append(title_label)

    boxoffice_label = tk.Label(root, text="Box Office $:")
    boxoffice_label.grid(column=0, row=4)
    dynamic_labels.append(boxoffice_label)

    synopsis_label = tk.Label(root, text="Synopsis:")
    synopsis_label.grid(column=0, row=5)
    dynamic_labels.append(synopsis_label)


def update_movie(movie):
    destroy_dynamic_widgets()

    if len(dynamic_labels) == 0:
        create_dynamic_labels()

    img = Image.open("cats_00007.jpg")
    img = ImageTk.PhotoImage(img)
    movie_poster = tk.Label(image=img)
    movie_poster.image = img
    movie_poster.grid(rowspan=5, column=4, row=3)
    dynamic_widgets.append(movie_poster)

    movie_title = tk.Label(root, text=f"{movie['Title']}")
    movie_title.grid(columnspan=3, column=1, row=3)
    dynamic_widgets.append(movie_title)

    movie_boxoffice = tk.Label(root, text=f"{movie['Box Office']}")
    movie_boxoffice.grid(columnspan=3, column=1, row=4)
    dynamic_widgets.append(movie_boxoffice)

    movie_synopsis = tk.Text(root)
    movie_synopsis.insert(1.0, movie['Synopsis'])
    movie_synopsis.grid(columnspan=3, rowspan=3, column=1, row=5)
    movie_synopsis.text = movie["Synopsis"]



def get_movie(year):
    query_year = date.get_date().year
    if query_year > 2022 | query_year < 1920:
        return None

    # Determine movie to be displayed
    movie = None
    while movie is None:
        if query_year in movies.keys():
            movie = movies[query_year]
        else:
            query_year = query_year + 1

    return movie


def submit_date():
    query_year = date.get_date().year

    # Call service for info (Placeholder atm. Also unsure of final structure of movie object rn)
    movie = get_movie(query_year)
    if movie is None:
        return

    update_movie(movie)


root.mainloop()
