from models import Post, User, db
from app import app

db.drop_all()
db.create_all()


river = User(firstname="river", lastname="bottom", image_url="https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png")
jack = User(firstname="jack", lastname="smith", image_url="https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png")
ozgenur = User(firstname="ozgenur", lastname="catal", image_url="https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png")
summer = User(firstname="summer", lastname="winter", image_url="https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png")
larry = User(firstname="larry", lastname="david", image_url="https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png")
kurt = User(firstname="kurt", lastname="cobain", image_url="https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png")
rain = User(firstname="rain", lastname="phoenix", image_url="https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png")
octavia = User(firstname="octavia", lastname="spencer", image_url="https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png")

db.session.add_all([river, jack, ozgenur, summer, larry, kurt, rain, octavia])
db.session.commit()

post1 = Post(title="Breaking News", content="I dont know what is going on in the world, i am just coding all the time", user_id=river.id)
post2 = Post(title="Breaking News", content="I dont know what is going on in the world, i am just coding all the time", user_id=jack.id)
post3 = Post(title="Breaking News", content="I dont know what is going on in the world, i am just coding all the time", user_id=ozgenur.id)
post4 = Post(title="Breaking News", content="I dont know what is going on in the world, i am just coding all the time", user_id=summer.id)
post5 = Post(title="Breaking News", content="I dont know what is going on in the world, i am just coding all the time", user_id=larry.id)
post6 = Post(title="Breaking News", content="I dont know what is going on in the world, i am just coding all the time", user_id=kurt.id)
post7 = Post(title="Breaking News", content="I dont know what is going on in the world, i am just coding all the time", user_id=rain.id)
post8 = Post(title="Breaking News", content="I dont know what is going on in the world, i am just coding all the time", user_id=octavia.id)





db.session.add_all([post1, post2, post3, post4, post5, post6, post7, post8])
db.session.commit()