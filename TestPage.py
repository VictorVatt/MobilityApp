import cv2
import customtkinter
import threading
from PIL import Image, ImageTk
from firebase_admin import firestore
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TestPage:

    def __init__(self, master, patient_data, video_data):
        self.master = master

        self.db = firestore.client()
        self.patient_data = patient_data
        self.video_data = video_data
        self.results = self.get_tests_results_in_db()
        self.current_video_player = None
        self.video_players = {}
        self.build_page()

    def build_page(self):
        self.page_container = customtkinter.CTkFrame(self.master)
        self.page_container.rowconfigure(0, weight=1)  # Première ligne fine
        self.page_container.rowconfigure(1, weight=1)  # Deuxième ligne fine
        self.page_container.rowconfigure(2, weight=10)
        self.page_container.columnconfigure(0, weight=1)
        self.page_container.grid(row=0, column=0, columnspan = 7, rowspan = 7, sticky="nsew")

        self.back_button = customtkinter.CTkButton(self.page_container, text="Retour", command=self.get_back)
        self.back_button.grid(row=0, column=0, sticky="nw", pady=(10, 0), padx=(10, 0))
        infos_string = f"Prénom : {self.patient_data['infos_perso'].get('prenom')} | Nom : {self.patient_data['infos_perso'].get('nom')} | Envergure :{self.patient_data['infos_perso'].get('envergure')}"
        self.patient_infos = customtkinter.CTkLabel( self.page_container, text=infos_string, font=("", 24))
        self.patient_infos.grid(row=0, column=0, columnspan=4, sticky="new")

        button_frame = customtkinter.CTkFrame(self.page_container)
        button_frame.grid(row=1, column=0, sticky="new", padx= 150)
        for i in range(self.get_unique(self.video_data)):
            tab_name = self.video_data[i]["test"]

            # Création d'un bouton pour chaque test
            button = customtkinter.CTkButton(button_frame, text=tab_name, command=lambda name=tab_name: self.show_video(name))
            button_frame.columnconfigure(tuple(range(self.get_unique(self.video_data))), weight=1)
            button.grid(row=0, column=i, padx=5, pady=5)

            # Création d'un VideoPlayer pour chaque vidéo
            frame = customtkinter.CTkFrame(self.page_container)
            video_player = VideoPlayer(frame, self.video_data[i]['videoURL'], self.results[tab_name])
            self.video_players[tab_name] = (frame, video_player)

            fig = Figure(figsize=(5, 4), dpi=100)
            t = range(100)
            fig.add_subplot(111).plot(self.results[tab_name].get('distanceDP'))

            # Ajout du graphique à la frame Tkinter
            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().grid(row= 0, column=0, sticky="ne")

            distance_label = DistanceCard(frame, str(min(self.results[tab_name].get('distanceDP'))))


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
        tests_results = {}
        for test in self.video_data:
            results_ref = self.db.collection("users").document(self.patient_data["id"]).collection("testResults").document(self.patient_data["email"]).collection(test["test"])
            docs = results_ref.stream()
            for doc in docs:
                tests_results[test["test"]] = doc.to_dict()

        return tests_results

class VideoPlayer:
    def __init__(self, master, url, results):
        self.video_url = url
        self.frame_counter = 0
        self.master = master
        self.video_capture = cv2.VideoCapture(self.video_url)
        self.video_test_results = results
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

            aspect_ratio = frame.shape[1] / frame.shape[0]
            new_width = int(frame_height * aspect_ratio)
            frame = cv2.resize(frame, (new_width, frame_height), interpolation=cv2.INTER_AREA)

            # Dessiner la ligne statique des pieds
            y_pied = int(self.video_test_results["PosPied"] * frame.shape[0])
            y_mains = int(self.video_test_results["PosMoyenneMajeurs"][self.frame_counter] * frame.shape[0])

            cv2.line(frame, (0, y_pied), (frame.shape[1], y_pied), (255, 0, 0), 2)
            cv2.line(frame, (0, y_mains), (frame.shape[1], y_mains), (255, 0, 0), 2)

            self.frame_counter += 1
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
            self.frame_counter = 0
            self.video_label.after(0, self.play_video_loop)

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

    def draw_line(self, frame, y):
        cv2.line(frame, (0, y), (frame.shape[1], y), (255, 0, 0), 2)

    def display_distance_value(self):
        pass



class DistanceCard(customtkinter.CTkFrame):
    def __init__(self, master, text):
        super(DistanceCard, self).__init__(master)
        self.master = master
        self.text = text
        self.build_card()

    def build_card(self):
        card_test = customtkinter.CTkLabel(self.master, text=self.text)
        card_test.grid(row = 0, column=1)
    def set_grid(self):
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)