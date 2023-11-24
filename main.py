import customtkinter
from login import LoginPage
from main_page import MainPage


class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("1000x650")
        self.set_grid()
        self.is_authenticated = False
        self.user_data = None
        self.page_manager()

    def set_authentication(self, value):
        self.is_authenticated = value
        self.page_manager()

    def set_user(self, user):
        self.user_data = user
        print(f"Données utilisateur mises à jour : {self.user_data}")


    def page_manager(self):
        self.clear_page()
        if self.is_authenticated:
            self.main_page = MainPage(self)
        else:
            self.login_page = LoginPage(self)


    def clear_page(self):
        for widget in self.winfo_children():
            widget.destroy()


    def set_grid(self):
        for i in range(7):
            self.grid_columnconfigure(i, weight=1)
            self.grid_rowconfigure(i, weight=1)

app = App()
app.mainloop()
