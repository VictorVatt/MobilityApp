import customtkinter
from login import LoginPage
from main_page import MainPage


class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1000x650")
        self.maxsize(1000, 650)
        self.minsize(1000, 650)
        self.user = None
        self.is_authenticated = False
        self.page_manager()

    def set_authentication(self, value):
        self.is_authenticated = value
        self.page_manager()

    def set_user(self, user):
        self.user = user
    def page_manager(self):
        self.clear_page()
        if self.is_authenticated:
            self.main_page = MainPage(self)
        else:
            self.login_page = LoginPage(self)



    def clear_page(self):
        for widget in self.winfo_children():
            widget.destroy()

app = App()
app.mainloop()
