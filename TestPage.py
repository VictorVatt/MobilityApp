import cv2
import customtkinter
import threading
from PIL import Image, ImageTk
from firebase_admin import firestore
from tkinter import ttk

class TestPage:

    def __init__(self, master, patient_data, video_data):
        self.master = master
        self.db = firestore.client()
        self.patient_data = patient_data
        self.results = self.get_tests_results_in_db()
        print(self.results)
        self.video_data = video_data
        self.current_video_player = None
        self.video_players = {}
        self.build_page()

    def build_page(self):
        self.back_button = customtkinter.CTkButton(self.master, text="Retour", command=self.get_back)
        self.back_button.grid(row=0, column=0, sticky="nw", pady=(10, 0), padx=(10, 0))
        infos_string = f"Prénom : {self.patient_data['infos_perso'].get('prenom')} | Nom : {self.patient_data['infos_perso'].get('nom')} | Envergure :{self.patient_data['infos_perso'].get('envergure')}"
        self.patient_infos = customtkinter.CTkLabel(self.master, text=infos_string, font=("", 24))
        self.patient_infos.grid(row=0, column=1, columnspan=4, sticky="new")

        for i in range(self.get_unique(self.video_data)):
            tab_name = self.video_data[i]["test"]

            # Création d'un bouton pour chaque test
            button = customtkinter.CTkButton(self.master, text=tab_name, command=lambda name=tab_name: self.show_video(name))
            button.grid(row=1, column=2+i, sticky="new")

            # Création d'un VideoPlayer pour chaque vidéo
            frame = customtkinter.CTkFrame(self.master)
            video_player = VideoPlayer(frame, self.video_data[i]['videoURL'])
            self.video_players[tab_name] = (frame, video_player)

    def show_video(self, name):
        # Arrêter la vidéo courante
        if self.current_video_player:
            self.current_video_player[1].stop_video()
            self.current_video_player[0].grid_forget()

        # Afficher la nouvelle vidéo
        frame, video_player = self.video_players[name]
        frame.grid(row=2, column=0, columnspan = 7, rowspan=6, sticky="NSEW", padx=5, pady=(10, 5 ))
        video_player.reset_video()
        video_player.start_video()
        self.current_video_player = (frame, video_player)


    def get_back(self):
        self.master.page_manager()

    def get_unique(self, video_data):
        unique_values = set()
        for video in video_data:
            unique_values.add(video["test"])

        return len(unique_values)

    def get_tests_results_in_db(self):
        tests = ["Test flexion avant", "Test flexion latéral droit", "Test flexion latéral gauche"]
        results = {}
        for test in tests:
            results_ref = self.db.collection("users").document(self.patient_data["id"]).collection("testResults").document(self.patient_data["email"]).collection(test)
            docs = results_ref.stream()
            for doc in docs:
                results[test] = doc.to_dict()
        return results

class VideoPlayer:
    def __init__(self, master, url):
        self.video_url = url
        self.master = master
        self.video_capture = cv2.VideoCapture(self.video_url)

        self.video_label = customtkinter.CTkLabel(self.master, text="")
        self.video_label.grid(padx=5, pady=5)
        self.playing = False
        self.thread = None

    def play_video_loop(self):
        if not self.playing:
            return  # Arrêtez la lecture si le drapeau playing est False

        success, frame = self.video_capture.read()
        if success:
            frame_height = self.master.winfo_height() - 10
            # Calculer la nouvelle largeur tout en maintenant le rapport largeur/hauteur
            aspect_ratio = frame.shape[1] / frame.shape[0]
            new_width = int(frame_height * aspect_ratio)
            frame = cv2.resize(frame, (new_width, frame_height), interpolation=cv2.INTER_AREA)
            if self.video_label.winfo_exists():
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.configure(image=imgtk)
                self.video_label.image = imgtk

                # Planifiez la prochaine mise à jour
                self.video_label.after(33, self.play_video_loop)
            else:
                # Si le label n'existe plus, arrêtez la boucle
                self.playing = False
        else:
            # Si la lecture de la vidéo est terminée, rembobinez
            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.video_label.after(33, self.play_video_loop)

    def reset_video(self):
        """ Remettre à zéro la vidéo sans libérer la capture vidéo. """
        if self.video_capture.isOpened():
            self.video_capture.release()
            self.video_capture = cv2.VideoCapture(self.video_url)
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
            self.thread = None
