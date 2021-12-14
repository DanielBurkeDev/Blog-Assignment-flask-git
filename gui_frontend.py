from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
import jsonpickle
import requests
import json
import bcrypt


class GUI:
    def __init__(self, parent):
        # Basic workflow:
        # 1. Create a GUI object and associate it with its parent
        # 2. Pack it or place it on grid - set up a 'geometry manager'

        # Remember who the parent window is
        self.parent = parent

        self.parent.title("Blogging App")
        # self.my_parent.title.set("Tk in-class demo")

        # Make protocol handler to manage interaction between the application and the window handler
        parent.protocol("WM_DELETE_WINDOW", self.catch_destroy)

        # Create Tab Control
        TAB_CONTROL = ttk.Notebook(parent)

        # Tab1 Registration
        TAB1 = ttk.Frame(TAB_CONTROL)
        TAB_CONTROL.add(TAB1, text='Registration')
        TAB_CONTROL.pack(expand=1, fill="both")

        # Tab2 Login
        TAB2 = ttk.Frame(TAB_CONTROL)
        TAB_CONTROL.add(TAB2, text='Login')
        TAB_CONTROL.pack(expand=1, fill="both")

        # Tab3 Create Post
        TAB3 = ttk.Frame(TAB_CONTROL)
        TAB_CONTROL.add(TAB3, text='Create Post')
        TAB_CONTROL.pack(expand=1, fill="both")

        # Tab3 display Post
        TAB4 = ttk.Frame(TAB_CONTROL)
        TAB_CONTROL.add(TAB4, text='Text Display')
        TAB_CONTROL.pack(expand=1, fill="both")

        # ======= User Registration Form =========
        # Create a container to hold the register form widgets
        self.container_register = Frame(TAB1, padx="5m", pady="5m")
        self.container_register.pack()

        # Create a form label
        self.frmlabel = Label(self.container_register, text="Register here", bg="#e3e3e3")
        self.frmlabel.grid(row=1, column=3, columnspan=2, sticky='ew')

        # Create a User Name text entry box
        self.username_text_label = Label(self.container_register, text="Enter Username:", fg="#20bebe")
        self.username_text_label.grid(row=2, column=3, sticky=W)
        self.username_text_input = Entry(self.container_register)
        self.username_text_input.grid(row=2, column=4)

        # Create a Firstname text entry box
        self.firstname_text_label = Label(self.container_register, text="Enter Firstname:", fg="#20bebe")
        self.firstname_text_label.grid(row=3, column=3, sticky=W)
        self.firstname_text_input = Entry(self.container_register)
        self.firstname_text_input.grid(row=3, column=4)

        # Create a Lastname text entry box
        self.lastname_text_label = Label(self.container_register, text="Enter Lastname:", fg="#20bebe")
        self.lastname_text_label.grid(row=4, column=3, sticky=W)
        self.lastname_text_input = Entry(self.container_register)
        self.lastname_text_input.grid(row=4, column=4)

        # Create a Password text entry box
        self.password_text_label = Label(self.container_register, text="Enter Password:", fg="#20bebe")
        self.password_text_label.grid(row=5, column=3, sticky=W)
        self.password_text_input = Entry(self.container_register, show='*')
        self.password_text_input.grid(row=5, column=4)

        # Create an Is Administrator Checkbox
        cbisadmin = BooleanVar()
        self.is_admin_checkbox = Checkbutton(self.container_register, text="Is Admin", variable=cbisadmin,
                                             onvalue=1, offvalue=0, height=5, width=20)
        self.is_admin_checkbox.grid(row=6, column=4)

        # Create a Register/Submit button
        self.register_btn_text = StringVar()
        self.register_btn = Button(self.container_register, textvariable=self.register_btn_text,
                                   command=lambda: self.register_user(cbisadmin), bg="#20bebe", fg="white", height=1,
                                   width=15)
        self.register_btn_text.set('Register')
        self.register_btn.grid(column=4, row=7, padx=15, pady=15)

        # ======= END User Registration Form =========

        # ======= User Login Form =========
        # Create a container to hold the login form widgets
        self.container_login = Frame(TAB2, padx="5m", pady="5m")
        self.container_login.pack()

        # Create a form label
        self.frmlabel_login = Label(self.container_login, text="Login here", bg="#e3e3e3")
        self.frmlabel_login.grid(columnspan=2, sticky='ew')

        # Create a User Name text entry box
        self.login_username_text_label = Label(self.container_login, text="Enter Username:", fg="#20bebe")
        self.login_username_text_label.grid(row=1, column=0, sticky=W)
        self.login_username_text_input = Entry(self.container_login)
        self.login_username_text_input.grid(row=1, column=1)

        # Create a Password text entry box
        self.login_password_text_label = Label(self.container_login, text="Enter Password:", fg="#20bebe")
        self.login_password_text_label.grid(row=4, column=0, sticky=W)
        self.login_password_text_input = Entry(self.container_login, show='*')
        self.login_password_text_input.grid(row=4, column=1)

        # Create a Login/Submit button
        self.login_btn_text = StringVar()
        self.login_btn = Button(self.container_login, textvariable=self.login_btn_text,
                                command=lambda: self.login_user(), bg="#20bebe", fg="white", height=1,
                                width=15)
        self.login_btn_text.set('Login')
        self.login_btn.grid(column=1, row=5, padx=15, pady=15)

        # =======  END User Login Form =========

        # =======  Create Post =========
        # Create a container to hold the create post widgets
        self.container_create_post = Frame(TAB3, padx="5m", pady="5m")
        self.container_create_post.pack()

        # Create a text display label
        self.container_create_post_display_label = Label(self.container_create_post, text="Create Post",
                                                         bg="#e3e3e3")
        self.container_create_post_display_label.grid(columnspan=2, row=0, sticky='ew')

        # Create a Post Title text entry box
        self.post_title_label = Label(self.container_create_post, text="Post Title:", fg="#20bebe")
        self.post_title_label.grid(row=1, column=0, sticky=W)
        self.post_title_input = Entry(self.container_create_post)
        self.post_title_input.grid(row=1, column=0)

        # Create a Post Category text entry box
        self.post_category_label = Label(self.container_create_post, text="Post Category id:", fg="#20bebe")
        self.post_category_label.grid(row=2, column=0, sticky=W)
        self.post_category_input = Entry(self.container_create_post)
        self.post_category_input.grid(row=2, column=0)

        # Scrolled Text Widget for post content Display
        self.post_content_label = Label(self.container_create_post, text="Post Content:", fg="#20bebe")
        self.post_content_label.grid(row=3, column=0, sticky=N)
        self.post_content_text_area = ScrolledText(self.container_create_post, height=10, width=40)
        self.post_content_text_area.grid(column=0, row=4, pady=10, padx=10)

        # Create a Submit button for creating posts
        self.submit_post_btn_text = StringVar()
        self.submit_post_btn = Button(self.container_create_post, textvariable=self.submit_post_btn_text,
                                      command=lambda: self.create_posts(), bg="#20bebe", fg="white", height=1,
                                      width=15)
        self.submit_post_btn_text.set('Submit')
        self.submit_post_btn.grid(column=0, row=5, padx=15, pady=15)

        # =======  END Create Post =========

        # =======  Text Display =========
        # Create a container to hold the text display widgets
        self.container_txtdisplay = Frame(TAB4, padx="5m", pady="5m")
        self.container_txtdisplay.pack()

        # Create a text display label
        self.displaylabel = Label(self.container_txtdisplay, text="Display", bg="#e3e3e3")
        self.displaylabel.grid(columnspan=3, sticky='ew')

        # Scrolled Text Widget Display
        self.text_area = ScrolledText(self.container_txtdisplay, height=10, width=40)
        self.text_area.grid(columnspan=3, row=1, pady=10, padx=10)

        # create a show users button
        self.showusers_text = StringVar()
        self.btn_showusers = Button(self.container_txtdisplay, textvariable=self.showusers_text,
                                    command=lambda: self.list_all_users(), bg="#20bebe", fg="white", height=1,
                                    width=15)
        self.showusers_text.set('Show Users')
        self.btn_showusers.grid(column=0, row=2, padx=15, pady=15, sticky='ew')

        # create a show users full name button
        self.showusers_fullname_text = StringVar()
        self.btn_showusers_fullname = Button(self.container_txtdisplay, textvariable=self.showusers_fullname_text,
                                             command=lambda: self.show_users_fullname(), bg="#20bebe", fg="white",
                                             height=1,
                                             width=15)
        self.showusers_fullname_text.set('Show Fullname')
        self.btn_showusers_fullname.grid(column=1, row=2, padx=15, pady=15, sticky='ew')

        # create a clear contents button
        self.clear_content_text = StringVar()
        self.btn_clear_content = Button(self.container_txtdisplay, textvariable=self.clear_content_text,
                                        command=lambda: self.clear_text_display(), bg="#20bebe", fg="white",
                                        height=1,
                                        width=15)
        self.clear_content_text.set('Clear Display')
        self.btn_clear_content.grid(column=2, row=2, padx=15, pady=15, sticky='ew')

    # =======  END Text Display =========

    # Ask User Do you really want to quit? when closing window
    def catch_destroy(self):
        if messagebox.askokcancel("Quit", "Do you really want to quit?"):
            self.parent.destroy()

    # Get user input from Registration form and POST JSON to Registration URL
    def register_user(self, cbisadmin):
        # get inputted values from fields
        username = self.username_text_input.get()
        firstname = self.firstname_text_input.get()
        lastname = self.lastname_text_input.get()
        pw = self.password_text_input.get()
        isadmin = cbisadmin.get()

        # check if user inputted anything
        if username == "" and firstname == "" and lastname == "" and pw == "" and isadmin == "":

            print("Please enter your details")
            messagebox.showwarning('Registration', 'Please enter your details')

        else:
            print("Thanks for adding details")

            # make up json to be sent
            posted_data = {'user_name': username, 'first_name': firstname, 'last_name': lastname,
                           'password': pw, 'is_admin': isadmin}

            # Post json to api
            requests.post('http://127.0.0.1:5000/register/', json=posted_data)

            print("posting json")
            print(type(posted_data))

    # User login and posting json data
    def login_user(self):
        # get inputted values from fields
        username = self.login_username_text_input.get()
        pw = self.login_password_text_input.get()

        # check if user inputted anything
        if username == "" and pw == "":

            print("Please enter your details")
            messagebox.showwarning('Registration', 'Please enter your details')
        else:
            print("Thanks for adding details")
            posted_data = {'user_name': username, 'password': pw}

            print(type(posted_data))
            print()

            # Post json to api
            requests.post('http://127.0.0.1:5000/login/', json=posted_data)
            print("posting json")
            print(type(posted_data))

    # List Users
    def list_all_users(self):
        display = self.text_area
        # get json from api
        response = requests.get('http://127.0.0.1:5000/list-users/')

        if response.status_code == 200:
            print('Success!')
            print(response.content)
            display.insert(END, response.content)
        elif response.status_code == 404:
            print('Not Found.')

    # Show users Full name in dropdown
    def show_users_fullname(self):
        display = self.text_area
        # get json from api
        response = requests.get('http://127.0.0.1:5000/list-users-full-name')
        if response.status_code == 200:
            print('Success!')

            display.insert(END, response.content)
        elif response.status_code == 404:
            print('Not Found.')

    def create_posts(self):
        # get inputted values from fields
        title = self.post_title_input.get()
        content = self.post_content_text_area.get("1.0", END)
        category_id = self.post_category_input.get()

        # check if user inputted anything
        if title == "" and content == "":

            print("Please enter your title and content")
            messagebox.showwarning('Create Post', 'Please enter post title and content')
        else:
            print("Thanks for adding details")
            posted_data = {"title": title, "category_id": category_id, "content": content}
            print(type(posted_data))
            print()
            # Post json to api
            requests.post('http://127.0.0.1:5000/create-post/', json=posted_data)
            print("posting json")

    # Show posts
    def show_posts(self):
        # get inputted values from fields
        username = self.username_text_input.get()
        pw = self.password_text_input.get()

        # check if user inputted anything
        if username == "" and pw == "":

            print("Please enter your details")
            messagebox.showwarning('Registration', 'Please enter your details')
        else:
            print("Thanks for adding details")
            posted_data = {'user_name': username, 'password': pw}
            print(type(posted_data))
            print()
            # Post json to api
            requests.post('http://127.0.0.1:5000/login/', json=posted_data)
            print("posting json")
            # print(type(posted_data))
        print('All the posts displayed')

    def clear_text_display(self):
        self.text_area.delete(1.0, END)


def login_gui():
    # Contain top level window usually called root
    root = Tk()
    # Create an instance of the class that defines the GUI and associate it with the top level window..
    GUI(root)
    # window size
    root.geometry("500x700")
    # Keep listening for events until destroy event occurs.
    root.mainloop()


if __name__ == "__main__":
    login_gui()
