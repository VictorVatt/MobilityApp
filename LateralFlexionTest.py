import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
from Test import FlexionTest


class RightFlexionTest(FlexionTest):
    def __init__(self):
        super().__init__()

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
                majeur_gauche = results.left_hand_landmarks.landmark[12]
                majeur_droit = results.right_hand_landmarks.landmark[12]
                conversion_factor = self.compute_conversion_factor(majeur_gauche, majeur_droit, envergure)

                position_pied_droit_frame1 = results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.RIGHT_FOOT_INDEX]

            if results.right_hand_landmarks:
                width, height, _ = image.shape
                majeur_droit = results.right_hand_landmarks.landmark[12]
                y = int(majeur_droit.y * width)
                cv2.line(image, (0, y), (frame.shape[1], y), (255, 0, 0), 2)

                distance_pixels = np.sqrt((majeur_droit.y - position_pied_droit_frame1.y) ** 2)
                distance_cm = distance_pixels * conversion_factor
                self.distance_doigts_Pieds_cm.append(distance_cm)
                self.positions_moyennes_majeurs.append(majeur_droit)

            frame_count += 1

        self.positions_moyennes_majeurs = [coord_frame.y for coord_frame in self.positions_moyennes_majeurs]
        cap.release()
        return self.distance_doigts_Pieds_cm, position_pied_droit_frame1.y, self.positions_moyennes_majeurs


class LeftFlexionTest(FlexionTest):
    def __init__(self):
        super().__init__()

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
                majeur_gauche = results.left_hand_landmarks.landmark[12]
                majeur_droit = results.right_hand_landmarks.landmark[12]
                conversion_factor = self.compute_conversion_factor(majeur_gauche, majeur_droit, envergure)

                position_pied_gauche_frame1 = results.pose_landmarks.landmark[self.mp_holistic.PoseLandmark.LEFT_FOOT_INDEX]

            if results.left_hand_landmarks:
                width, height, _ = image.shape
                majeur_gauche = results.left_hand_landmarks.landmark[12]


                distance_pixels = np.sqrt((majeur_gauche.y - position_pied_gauche_frame1.y) ** 2)
                distance_cm = (distance_pixels * conversion_factor) - 1
                self.distance_doigts_Pieds_cm.append(distance_cm)
                self.positions_moyennes_majeurs.append(majeur_gauche)

            frame_count += 1
        self.positions_moyennes_majeurs = [coord_frame.y for coord_frame in self.positions_moyennes_majeurs]
        cap.release()
        return self.distance_doigts_Pieds_cm, position_pied_gauche_frame1.y, self.positions_moyennes_majeurs








