import customtkinter

class MainPage:
    def __init__(self, master):
        self.master = master
        self.build_profile()
    def build_profile(self):
        mail = self.master.user_data["email"]
        self.profile_name = customtkinter.CTkLabel(self.master, text=mail)
        self.profile_name.pack()

