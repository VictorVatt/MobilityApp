import cv2
import customtkinter
import threading
from PIL import Image, ImageTk

class TestPage:

    def __init__(self, master, patient_data, video_data):
        self.master = master
        self.patient_data = patient_data
        self.video_data = video_data
        self.current_video_player = None
        self.video_players = {}
        self.build_page()

    def build_page(self):
        self.back_button = customtkinter.CTkButton(self.master, text="Retour", command=self.get_back)
        self.back_button.pack()
        infos_string = f"Prénom : {self.patient_data['infos_perso'].get('prenom')} | Nom : {self.patient_data['infos_perso'].get('nom')} | Envergure :{self.patient_data['infos_perso'].get('envergure')}"
        self.patient_infos = customtkinter.CTkLabel(self.master, text=infos_string)
        self.patient_infos.pack()

        for i in range(self.get_unique(self.video_data)):
            tab_name = self.video_data[i]["test"]

            # Création d'un bouton pour chaque test
            button = customtkinter.CTkButton(self.master, text=tab_name, command=lambda name=tab_name: self.show_video(name))
            button.pack()

            # Création d'un VideoPlayer pour chaque vidéo
            frame = customtkinter.CTkFrame(self.master)
            video_player = VideoPlayer(frame, self.video_data[i]['videoURL'])
            self.video_players[tab_name] = (frame, video_player)

    def show_video(self, name):
        # Arrêter la vidéo courante
        if self.current_video_player:
            self.current_video_player[1].stop_video()
            self.current_video_player[0].pack_forget()

        # Afficher la nouvelle vidéo
        frame, video_player = self.video_players[name]
        frame.pack(expand=True, fill='both')
        video_player.start_video()
        self.current_video_player = (frame, video_player)


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

        self.video_label = customtkinter.CTkLabel(self.master, text="")
        self.video_label.pack(padx=10, pady=10)

        self.playing = False
        self.thread = None

    def play_video_loop(self):
        if not self.playing:
            return  # Arrêtez la lecture si le drapeau playing est False

        success, frame = self.video_capture.read()
        if success:
            frame = cv2.resize(frame, None, fx=0.35, fy=0.35, interpolation=cv2.INTER_AREA)
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
        if self.video_capture.isOpened():
            self.video_capture.release()