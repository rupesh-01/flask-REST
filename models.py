from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class User(db.Model):
    __tablename__="users"
    id =  db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=True)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    mob = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String,nullable=False)

class Doctor(db.Model):
    __tablename__="doctors"
    id =  db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=True)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    mob = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String,nullable=False)
    specialization = db.Column(db.String, nullable=False)

class Hospital(db.Model):
    __tablename__="hospitals"
    id =  db.Column(db.Integer, primary_key=True)
    hname = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    mob = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String,nullable=False)
    

class Lab(db.Model):
    __tablename__="labs"
    id =  db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    mob = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String,nullable=False)

class DRating(db.Model):
    __tablename__="ratedoc"
    idoc = db.Column(db.Integer,db.ForeignKey("doctors.id"),nullable=False)
    rate = db.Column(db.Integer,nullable=False)
    db.PrimaryKeyConstraint(idoc,rate)

class HRating(db.Model):
    __tablename__="ratehos"
    hdoc = db.Column(db.Integer,db.ForeignKey("hospitals.id"),nullable=False)
    rate = db.Column(db.Integer,nullable=False)
    db.PrimaryKeyConstraint(hdoc,rate)


