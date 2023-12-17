import customtkinter
import pyrebase
from config import config
from PIL import Image


class LoginPage:
    def __init__(self, master):
        self.master = master
        self.firebase = pyrebase.initialize_app(config)
        self.auth = self.firebase.auth()
        self.display_login()

    def display_login(self):
        self.label = customtkinter.CTkLabel(self.master, text="Bienvenue, connectez-vous ! ",font=("", 25), text_color="white")
        self.label.pack(pady=(50, 0))
        self.email = customtkinter.CTkEntry(self.master, placeholder_text="Email", width=300, font=("", 16))
        self.email.pack(pady=(150, 5))
        self.password = customtkinter.CTkEntry(self.master, placeholder_text="Password", show="*", width=300, font=("", 16))
        self.password.pack(pady=(5, 20))
        self.login_button = customtkinter.CTkButton(self.master, text="Login", command=self.login, width=400, font=("", 16), height=35)
        self.login_button.pack(pady=(20, 10))

    def login(self):
        try:
            user = self.auth.sign_in_with_email_and_password(self.email.get(), self.password.get())
            self.master.set_user(user)
            self.master.set_authentication(True)

        except Exception as e:
            print(e)
            self.master.set_authentication(False)

