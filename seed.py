from app import app
from models import db, User, Feedback


db.drop_all()
db.create_all()


u1 = User.register(username = 'BobRoberts', 
            first_name = 'bob',
            last_name = 'Roberts',
            email = 'bob.roberts@gmail.com', 
            password = 'banana')

u2 = User.register(username = 'TomDomwell', 
            first_name = 'Tom',
            last_name = 'Domwell',
            email = 'tom.dom@gmail.com', 
            password = 'strawberry')

db.session.add_all([u1, u2])
db.session.commit()

