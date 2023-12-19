import customtkinter
import pyrebase
from config import config
from PIL import Image
import webbrowser

class LoginPage:
    def __init__(self, master):
        self.master = master
        self.firebase = pyrebase.initialize_app(config)
        self.auth = self.firebase.auth()
        self.display_login()

    def display_login(self):
        self.container = customtkinter.CTkFrame(self.master, corner_radius=10)
        self.container.configure(fg_color="white")
        [self.container.grid_rowconfigure(i, weight=1) for i in range(7)]
        [self.container.grid_columnconfigure(i, weight=1) for i in range(9)]
        self.label = customtkinter.CTkLabel(self.container, text="Bienvenue, connectez-vous ! ", font=("", 30),
                                            text_color="black")
        self.label.grid(column=1, columnspan=7, sticky="nsew", pady=(10, 0))
        self.image_profile = customtkinter.CTkImage(light_image=Image.open("./assets/loginImage.png"),
                                                    dark_image=Image.open("./assets/loginImage.png"), size=(300,300))
        self.image_label = customtkinter.CTkLabel(self.container, image=self.image_profile, text="")
        self.image_label.grid(row=1, rowspan=5, column=0, columnspan=4, pady=(5, 0))
        self.email = customtkinter.CTkEntry(self.container, placeholder_text="Email", font=("", 22))
        self.email.grid(row=2, column=5, columnspan=3, sticky="ew", pady=(0, 120))
        self.password = customtkinter.CTkEntry(self.container, placeholder_text="Password", show="*", font=("", 22))
        self.password.grid(row=2, column=5, columnspan=3, sticky="ew")
        self.login_button = customtkinter.CTkButton(self.container, text="Login", command=self.login, font=("", 16), height=35)
        self.login_button.grid(row=3, column=5, columnspan=3, sticky="ew")
        self.infos_massage = customtkinter.CTkLabel(self.container, text="En savoir plus sur le projet", font=("",16, "italic"), text_color="blue", cursor="hand2")
        self.infos_massage.grid(row=7, column=0, columnspan=9, sticky="nsew", pady=(0, 10))
        self.infos_massage.bind("<Button-1>", self.open_link)

        self.container.grid(row=1, column=1, columnspan=5, rowspan=5, sticky="NSEW")


    def login(self):
        try:
            user = self.auth.sign_in_with_email_and_password(self.email.get(), self.password.get())
            self.master.set_user(user)
            self.master.set_authentication(True)

        except Exception as e:
            print(e)
            self.master.set_authentication(False)


    def open_link(self, event):
        webbrowser.open_new(r"https://github.com/VictorVatt")