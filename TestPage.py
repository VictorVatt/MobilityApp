import customtkinter

class Test:
    def __init__(self, test_name, video, ID, patient_email):
        self.id = ID
        self.test_name = test_name
        self.video = video
        self.patient_email = patient_email

class TestPage:

    def __init__(self, master):
        self.master = master
        self.test = customtkinter.CTkLabel(self.master, text="Test")