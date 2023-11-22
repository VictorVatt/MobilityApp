import customtkinter

class MainPage:
    def __init__(self, master):
        self.master = master


    def get_user_infos(self):
        username = self.master['email']
        self.name = customtkinter.CTkLabel(text=username)
        self.name.pack()
