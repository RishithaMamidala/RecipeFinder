from models import User

def create_user(email, name, password):
    user = User.objects.create_user(email=email, name=name, password=password)
    return user

def create_superuser(email, name, password):
    superuser = User.objects.create_superuser(email=email, name=name, password=password)
    return superuser
