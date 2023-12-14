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

        self.tab_view = customtkinter.CTkTabview(self.master)
        self.tab_view.pack(expand=True, fill='both', padx=20, pady=20)

        # Création des onglets pour différents tests

        for i in range(self.get_unique(self.video_data)):

            tab_name = self.video_data[i]["test"]
            print(tab_name)
            self.tab_view.add(tab_name)

            self.video_player = VideoPlayer(self.tab_view.tab(tab_name), self.video_data[i]['videoURL'])

        if self.get_unique(self.video_data) > 1:
            self.tab_view.bind('<<NotebookTabChanged>>', self.on_tab_change)
        else:
            self.video_player.start_video()
    def on_tab_change(self, event=None):
        selected_tab = self.tab_view.index("current")
        if selected_tab == 1:  # Index de l'onglet vidéo
            self.video_player.start_video()
        else:
            self.video_player.stop_video()

    def get_back(self):
        self.master.page_manager()

    def get_unique(self, video_data):
        unique_values = set()
        for video in video_data:
            unique_values.add(video["test"])

        return len(unique_values)


class VideoPlayer:
    def __init__(self, master, url):
        self.video_url = url
        self.master = master
        self.video_capture = cv2.VideoCapture(self.video_url)

        self.video_label = customtkinter.CTkLabel(self.master, image=None)
        self.video_label.pack(padx=10, pady=10)

        self.playing = False
        self.thread = None

    def play_video_loop(self):
        while self.playing:
            success, frame = self.video_capture.read()
            if success:
                # Vérifiez si le label existe toujours
                if self.video_label.winfo_exists():
                    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                    img = Image.fromarray(cv2image)
                    imgtk = ImageTk.PhotoImage(image=img)
                    self.video_label.configure(image=imgtk)
                    self.video_label.image = imgtk
                else:
                    break  # Arrêtez la boucle si le label n'existe plus
            else:
                self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def start_video(self):
        if not self.playing:
            self.playing = True
            self.thread = threading.Thread(target=self.play_video_loop, daemon=True)
            self.thread.start()

    def stop_video(self):
        self.playing = False
        if self.thread is not None:
            self.thread.join()