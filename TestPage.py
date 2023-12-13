import cv2
import customtkinter
import threading
from PIL import Image, ImageTk

class Test:
    def __init__(self, test_name, video, ID, patient_email):
        self.id = ID
        self.test_name = test_name
        self.video = video
        self.patient_email = patient_email

    def set_test_parameters(self):
        pass

    def compute_test(self):
        pass

    def create_results(self):
        pass


class TestPage:

    def __init__(self, master, patient_data, video_data):
        self.master = master
        self.patient_data = patient_data
        self.video_data = video_data
        self.build_page()

    def build_page(self):
        self.back_button = customtkinter.CTkButton(self.master, text="Retour", command=self.get_back)
        self.back_button.pack()
        self.patient_infos = customtkinter.CTkLabel(self.master, text=str(self.patient_data))
        self.patient_infos.pack()

        tab_view = customtkinter.CTkTabview(self.master)
        tab_view.pack(expand=True, fill='both', padx=20, pady=20)

        # Création des onglets pour différents tests
        for i in range(1, 5):
            tab_view.add(f'Test {i}')
            # Ajout de contenu spécifique à chaque onglet
            label = customtkinter.CTkLabel(tab_view.tab(f"Test {i}"), text=self.video_data)
            label.pack()
        tab_view.set("Test 1")

    def get_back(self):
        self.master.page_manager()




class VideoPlayer:
    def __init__(self, url, master):
        self.video_url = url
        self.master = master
        self.video_capture = cv2.VideoCapture(self.video_url)
