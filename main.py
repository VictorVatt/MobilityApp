import customtkinter
from login import LoginPage
from main_page import MainPage
import firebase_admin
from firebase_admin import credentials
from config import config2

class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cred = credentials.Certificate(config2)
        firebase_admin.initialize_app(self.cred)
        self.geometry("1000x650")
        self.title("DigiKineApp")
        self.iconbitmap("./assets/icone.ico")
        self.set_grid(7)
        self.video_loaded = False
        self.is_authenticated = False
        self.user_data = None
        self.page_manager()

    def set_authentication(self, value):
        self.is_authenticated = value
        self.page_manager()

    def set_user(self, user):
        self.user_data = user

    def page_manager(self):
        self.clear_page()
        if self.is_authenticated:
            self.main_page = MainPage(self)
        else:
            self.login_page = LoginPage(self)


    def clear_page(self):
        for widget in self.winfo_children():
            widget.destroy()


    def set_grid(self, number):
        for i in range(number):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)

customtkinter.set_default_color_theme("green")
customtkinter.set_appearance_mode("light")
app = App()
app.mainloop()
