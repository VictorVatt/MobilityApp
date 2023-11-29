import customtkinter
from BDD import PATIENTS_LIST
from PIL import Image
from TestPage import TestPage

class MainPage:
    def __init__(self, master):
        self.master = master
        self.build_page()

    def build_page(self):
        self.profile_name = customtkinter.CTkLabel(self.master, text=f"Bonjour {self.master.user_data['email']} !", font=("", 30))
        self.profile_name.grid(row=0, column=1, columnspan=5, sticky="NSEW", pady=(30, 15))
        self.build_patient_list()


    def get_all_patients(self):
        pass

    def build_patient_list(self):
        patient_noms = [f"{patient['name']} {patient['surname']} id:{str(patient['id'])}" for patient in PATIENTS_LIST]
        self.patient_list = PatientList(self.master)
        for i, patient in enumerate(patient_noms):
            self.patient_card = PatientCard(self.patient_list)
            self.patient_card.infos = patient
            self.patient_card.grid(row=i+1, column=1, columnspan=7, sticky="NSEW", pady=10, )
            self.names = customtkinter.CTkLabel(self.patient_card, text=patient, font=("", 22), text_color="lightblue")
            self.names.grid(row=0, column=1)
            self.image_profile = customtkinter.CTkImage(light_image=Image.open("./assets/patient_icon.png"), dark_image=Image.open("./assets/patient_icon.png"), size=(50, 50))
            self.image_label = customtkinter.CTkLabel(self.patient_card, image=self.image_profile, text="")
            self.image_label.grid(row=0,column=0, pady=(5, 0), padx=(5, 30))
        self.patient_list.grid(row=1, rowspan=5,column=1, columnspan=5, sticky="NSEW")


class PatientList(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.set_grid()

    def set_grid(self):
        for i in range(9):
            self.grid_columnconfigure(i, weight=1)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()


class PatientCard(customtkinter.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.infos = None
        self.configure(fg_color="white")
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    def get_infos(self):
        return self.infos

    def set_grid(self):
            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=2)

    def on_enter(self, event):
        self.master.config(cursor="hand2")
        self.configure(fg_color="lightblue")

    def on_leave(self, event):
        self.configure(fg_color="white")
        self.master.config(cursor="")


    def on_click(self, event):
        self.app = self.master.master.master.master
        self.app.clear_page()
        print(self.get_infos())
        self.test_page = TestPage(self.app, self.get_infos())