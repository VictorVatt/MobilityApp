import cv2
import mediapipe as mp
import numpy as np

class FlexionTest:
    def __init__(self):
        self.mp_holistic = mp.solutions.holistic
        self.holistic = self.mp_holistic.Holistic(min_detection_confidence=0.5,
                                                  min_tracking_confidence=0.5,
                                                  model_complexity=2)
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=0, circle_radius=2)

        #Metrics positions
        self.positions_moyennes_majeurs = []
        self.positions_pied = None
        self.distance_doigts_Pieds_cm = []

    def compute_distance(self, point1, point2):
        return np.sqrt((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2)

    def compute_conversion_factor(self, point1, point2, envergure):
        distance_pixels = self.compute_distance(point1, point2)
        conversion_factor = envergure / distance_pixels
        return conversion_factor

    def compute_mean_postion(self, point1, point2):
        return [(point1.x + point2.x) / 2, (point1.y + point2.y) / 2]

    def process_video(self, video_path, envergure):
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print("Erreur : impossible d'ouvrir la vidéo")
            return
        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = True

            results = self.holistic.process(image)

            if frame_count == 0 and results.left_hand_landmarks and results.right_hand_landmarks:
                # Compute conversion factor from envergure length (fingers distance Tpose)
                majeur_gauche = results.left_hand_landmarks.landmark[12]
                majeur_droit = results.right_hand_landmarks.landmark[12]
                conversion_factor = self.compute_conversion_factor(majeur_gauche, majeur_droit, envergure)

                pied_gauche = results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.LEFT_FOOT_INDEX]
                pied_droit = results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.RIGHT_FOOT_INDEX]
                self.positions_pied = self.compute_mean_postion(pied_gauche, pied_droit)

            if results.left_hand_landmarks and results.right_hand_landmarks:
                width, height, _ = image.shape
                majeur_gauche = results.left_hand_landmarks.landmark[12]
                majeur_droit = results.right_hand_landmarks.landmark[12]
                #x_moyen = int((majeur_gauche.x + majeur_droit.x) / 2 * height)
                y_moyen = int((majeur_gauche.y + majeur_droit.y) / 2 * width)

                position_moyenne = self.compute_mean_postion(majeur_gauche, majeur_droit)

                distance_pixels = np.sqrt((position_moyenne[1] - self.positions_pied[1]) ** 2)
                distance_cm = (distance_pixels * conversion_factor) - 1
                self.distance_doigts_Pieds_cm.append(distance_cm)
                self.positions_moyennes_majeurs.append(position_moyenne)


        self.positions_moyennes_majeurs = [coord_frame[1] for coord_frame in self.positions_moyennes_majeurs]
        cap.release()
        return self.distance_doigts_Pieds_cm, self.positions_pied, self.positions_moyennes_majeurs
