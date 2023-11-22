import pyrebase


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

email = input("Email : ")
password = input("Password : ")


def login(email, password):
  try:
    user = auth.sign_in_with_email_and_password(email, password)
    print("Connexion réussi")
    return user
  except Exception:
    print("Echec de la connexion")


login(email, password)
#idToken = user["idToken"]
#print(idToken)
#storage = firebase.storage()
#storage.child("test1.mp4").put("video30sec.mp4")



