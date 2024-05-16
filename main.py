from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():

    website = website_entry.get().upper()
    username = user_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": username,
            "password": password,
        }
    }

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showinfo(title="OOPS", message="Please don't leave any fields empty!")

    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details that you have entered:\n "
                                                              f"\nEmail/Username: {username}"
                                                              f"\nPassword: {password}\n "
                                                              f"\nIs it okay to save?")

        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    # Read old data
                    data = json.load(data_file)

            except (FileNotFoundError, json.decoder.JSONDecodeError):
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)

            else:
                # Update old data with new data
                data.update(new_data)

                with open("data.json", "w") as data_file:
                    # Saving updated data
                    json.dump(data, data_file, indent=4)

            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():

    website = website_entry.get().upper()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)

    except (FileNotFoundError, json.decoder.JSONDecodeError):
        messagebox.showinfo(title="ERROR", message="No Data Found.")

    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}"
                                                       f"\nPassword: {password}")
        else:
            messagebox.showinfo(title="ERROR", message=f"No details for {website} exists.")


# ---------------------------- UI SETUP ------------------------------- #


windows = Tk()
windows.title("Password Manager")
windows.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=1, row=0)


# Labels
website_label = Label(text="Website :")
website_label.grid(row=1, column=0)
user_label = Label(text="Email/Username :")
user_label.grid(row=2, column=0)
password_label = Label(text="Password :")
password_label.grid(row=3, column=0)


# Entry
website_entry = Entry()
website_entry.grid(column=1, row=1, sticky="EW")
website_entry.focus()
user_entry = Entry()
user_entry.grid(column=1, row=2, columnspan=2, sticky="EW")
user_entry.insert(0, "aneeshsingha@gmail.com")
password_entry = Entry()
password_entry.grid(column=1, row=3, sticky="EW")


# Buttons
search_button = Button(text="Search", command=find_password)
search_button.grid(column=2, row=1, sticky="EW")
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3, sticky="EW")
add_button = Button(text="Add", width=35, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")


windows.mainloop()
