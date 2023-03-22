"""
A module for managing passwords.
"""

from tkinter import *
from tkinter import messagebox
import tkinter as tk
from random import choice, randint, shuffle
import pyperclip
import json

BACKGROUND_COLOR = 'gray18'


def writing_to_file(new_data):
    """Write save data to a json file."""
    with open("data.json", "w") as data_file:
        json.dump(new_data, data_file, indent=4)


class PasswordManager(tk.Tk):
    """A class representing password manager gui."""
    def __init__(self):
        super().__init__()
        self.search_button = Button(text="Search", bg=BACKGROUND_COLOR, fg="snow",
                               command=self.search, width=15)

        self.password_entry = Entry(width=26, border="4")
        self.email_entry = Entry(width=35, border="4")
        self.website_entry = Entry(width=32, border="4")
        self.canvas = Canvas(width=200, height=200)
        self.logo_img = PhotoImage(file="logo.png")
        self.title("My Password Manager")
        self.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
        self.center_window(width=500, height=400)
        self.create_widgets()

    def center_window(self, width, height):
        """Center gui window according to current screen resolution."""
        width_screen = self.winfo_screenwidth()
        height_screen = self.winfo_screenheight()
        x = (width_screen / 2) - (width / 2)
        y = (height_screen / 2) - (height / 2)

        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def create_widgets(self):
        """Create gui widgets."""
        # Image
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.configure(bg=BACKGROUND_COLOR, borderwidth=0, highlightthickness=0)
        self.canvas.grid(row=0, column=1)

        # Labels
        website_label = Label(text="Website:", bg=BACKGROUND_COLOR, fg="snow")
        website_label.grid(row=1, column=0)
        email_label = Label(text="Email/Username:", bg=BACKGROUND_COLOR, fg="snow")
        email_label.grid(row=2, column=0)
        password_label = Label(text="Password:", bg=BACKGROUND_COLOR, fg="snow")
        password_label.grid(row=3, column=0)

        # Entries
        self.website_entry.grid(row=1, column=1, columnspan=1, sticky="W")
        self.website_entry.focus()
        self.email_entry.grid(row=2, column=1, columnspan=2, sticky="EW")
        self.password_entry.grid(row=3, column=1, sticky="W")

        # Buttons
        self.search_button.grid(row=1, column=2)

        generate_passwords_button = Button(
            text="Generate Password",
            bg=BACKGROUND_COLOR,
            fg="snow",
            command=self.generate_password)

        generate_passwords_button.grid(row=3, column=2)

        copy_button = Button(text="Copy", bg=BACKGROUND_COLOR, fg="snow", padx=0.1,
                             command=self.copy)

        copy_button.grid(row=3, column=1, sticky="E")

        add_button = Button(text="Add", width=36, bg=BACKGROUND_COLOR, fg="snow", command=self.save)

        add_button.grid(row=4, column=1, columnspan=2, sticky="EW")

    def search(self):
        """Search for saved password and retrieve its values."""
        website = self.website_entry.get()

        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showinfo(title="Notice", message="No Data File Found.")
        else:
            if website in data:
                saved_data = data[website]
                self.email_entry.insert(0, saved_data["email"])
                self.password_entry.insert(0, saved_data["password"])
            else:
                messagebox.showinfo(title="Notice",
                                    message=f"No details for {website} exists.")

    def generate_password(self):
        """Generate random strong password."""
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                   'u',
                   'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
                   'P',
                   'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

        password_letters = [choice(letters) for letter in range(randint(8, 10))]
        password_symbols = [choice(numbers) for symbol in range(randint(2, 4))]
        password_numbers = [choice(symbols) for number in range(randint(2, 4))]

        password_list = password_letters + password_symbols + password_numbers
        shuffle(password_list)

        password = "".join(password_list)
        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, password)
        pyperclip.copy(password)

    def copy(self):
        """Copy action for password."""
        pyperclip.copy(self.password_entry.get())

    def save(self):
        """Save entries to json file."""
        website = self.website_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        new_data = {
            website: {
                "email/user": email,
                "password": password,
            }
        }

        if len(website) == 0 or len(email) == 0 or len(password) == 0:
            messagebox.showinfo(
                title="Notice",
                message="Please make sure you haven't left any field empty.")

        else:
            is_ok = messagebox.askokcancel(
                title="Save", message=f"These are the details entered:"
                                      f"\nWebsite: {website}\nEmail: {email} "
                                      f"\nPassword: {password} \nIs it ok to save?")

            if is_ok:
                try:
                    with open("data.json", "r") as data_file:
                        # Reading old data
                        data = json.load(data_file)
                except FileNotFoundError:
                    writing_to_file(new_data)
                else:
                    # Updating old data with new data
                    data.update(new_data)
                    writing_to_file(data)
                finally:
                    self.website_entry.delete(0, END)
                    self.password_entry.delete(0, END)


if __name__ == "__main__":
    app = PasswordManager()
    app.mainloop()