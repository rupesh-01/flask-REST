from flask import Flask,request,render_template,jsonify
from base64 import main
from models import *
from passlib.hash import pbkdf2_sha256
import sqlite3

app = Flask(__name__) 

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/signup")
def type():
    return render_template("type.html")

@app.route("/signup/user")
def ushow():
    return render_template("useregister.html")

@app.route("/signup/user/success",methods=["POST"])
def uregister():
    fname=request.form.get("fname")
    lname=request.form.get("lname")
    pas=request.form.get("pass")
    email=request.form.get("email")
    mob=request.form.get("mno")
    city=request.form.get("ct")
    state=request.form.get("st")
    pas = pbkdf2_sha256.encrypt(pas)
    user = User(fname=fname,lname=lname,city=city,state=state,mob=mob,email=email,password=pas)
    db.session.add(user)
    db.session.commit()
    return "<h1>USER REGISTRATION SUCCESSFUL</h1>"


@app.route("/signup/doctor")
def docshow():
    return render_template("docregister.html")

@app.route("/signup/doctor/success",methods=["POST"])
def dregister():
    fname=request.form.get("fname")
    lname=request.form.get("lname")
    pas=request.form.get("pass")
    email=request.form.get("email")
    mob=request.form.get("mno")
    city=request.form.get("ct")
    state=request.form.get("st")
    spec=request.form.get("sp")
    pas = pbkdf2_sha256.encrypt(pas)
    doc = Doctor(fname=fname,lname=lname,city=city,state=state,mob=mob,email=email,password=pas,specialization=spec)
    db.session.add(doc)
    db.session.commit()
    return "<h1>DOCTOR REGISTRATION SUCCESSFUL</h1>"

@app.route("/signup/hospital")
def hosshow():
    return render_template("hosregister.html")

@app.route("/signup/hospital/success",methods=["POST"])
def hregister():
    hname=request.form.get("fname")
    pas=request.form.get("pass")
    email=request.form.get("email")
    mob=request.form.get("mno")
    city=request.form.get("ct")
    state=request.form.get("st")
    pas = pbkdf2_sha256.encrypt(pas)
    hos = Hospital(hname=hname,city=city,state=state,mob=mob,email=email,password=pas)
    db.session.add(hos)
    db.session.commit()
    return "<h1>HOSPITAL REGISTRATION SUCCESSFUL</h1>"

@app.route("/signup/lab")
def labshow():
    return render_template("labregister.html")

@app.route("/signup/lab/success",methods=["POST"])
def lregister():
    lname=request.form.get("fname")
    pas=request.form.get("pass")
    email=request.form.get("email")
    mob=request.form.get("mno")
    city=request.form.get("ct")
    state=request.form.get("st")
    pas = pbkdf2_sha256.encrypt(pas)
    lab = Lab(lname=lname,city=city,state=state,mob=mob,email=email,password=pas)
    db.session.add(lab)
    db.session.commit()
    return "<h1>LAB REGISTRATION SUCCESSFUL</h1>"


@app.route("/rate/doctor")
def drating():
    doc=Doctor.query.all()
    return render_template("doclist.html",doctor=doc)

@app.route("/rate/doctor/success",methods=["POST"])
def drate():
    iid=int(request.form.get("id"))
    rate=request.form.get("rate")
    rate=DRating(idoc=iid,rate=rate)
    db.session.add(rate)
    db.session.commit()
    return "<h1>Rated Successfully :)</h1>"

@app.route("/rate/hospital")
def hrating():
    hos=Hospital.query.all()
    return render_template("hoslist.html",hospital=hos)

@app.route("/rate/doctor/success",methods=["POST"])
def hrate():
    iid=int(request.form.get("id"))
    rate=request.form.get("rate")
    rate=HRating(hdoc=iid,rate=rate)
    db.session.add(rate)
    db.session.commit()
    return "<h1>Rated Successfully :)</h1>"

"""API to get single user,doctor,hospital and lab details"""

@app.route("/api/<string:name>/<int:id>")
def singlegetapi(name,id):
    if name=="user":
        user = User.query.get(id)
        if user is None:
            return jsonify({"error": "Invalid user_id "}), 422
        return jsonify(
            {"user_id": user.id,
            "user_name": user.fname+user.lname,
            "user_email":user.email,
            "user_mobile":user.mob,
            "user_city":user.city,
            "user_state":user.state
            }
        )
    if name=="doctor":
        doctor = Doctor.query.get(id)
        if doctor is None:
            return jsonify({"error": "Invalid doctor_id "}), 422
        return jsonify(
            {"doctor_id": doctor.id,
            "doctor_name": doctor.fname+doctor.lname,
            "doctor_email":doctor.email,
            "doctor_mobile":doctor.mob,
            "doctor_city":doctor.city,
            "doctor_state":doctor.state,
            "doctor_specialization":doctor.specialization}
        )
    if name=="hospital":
        hospital = Hospital.query.get(id)
        if hospital is None:
            return jsonify({"error": "hospital_id "}), 422
        return jsonify(
            {"hospital_id": hospital.id,
            "hospital_name": hospital.hname,
            "hospital_email":hospital.email,
            "hospital_mobile":hospital.mob,
            "hospital_city":hospital.city,
            "hospital_state":hospital.state
            }
        )
    if name=="lab":
        lab = Lab.query.get(id)
        if lab is None:
            return jsonify({"error": "lab_id "}), 422
        return jsonify(
            {"lab_id": lab.id,
            "lab_name": lab.lname,
            "lab_email":lab.email,
            "lab_mobile":lab.mob,
            "lab_city":lab.city,
            "lab_state":lab.state
            }
        )

"""API to get details of all the users,doctors,hospitals and labs"""

@app.route("/api/<string:name>")
def getallapi(name):
    output = []
    if name == "users":
        users = User.query.all()
        for user in users:
            user_data = {}
            user_data["id"] = user.id
            user_data["name"] = user.fname+" "+user.lname
            user_data["email"] = user.email
            user_data["mob"] = user.mob
            user_data["city"] = user.city
            user_data["state"] = user.state
            output.append(user_data)
        return jsonify({"users" : output})
    if name == "doctors":
        doctors = Doctor.query.all()
        for doctor in doctors:
            doctor_data = {}
            doctor_data["id"] = doctor.id
            doctor_data["name"] = doctor.fname+" "+doctor.lname
            doctor_data["email"] = doctor.email
            doctor_data["mob"] = doctor.mob
            doctor_data["city"] = doctor.city
            doctor_data["state"] = doctor.state
            output.append(doctor_data)
        return jsonify({"doctors" : output})
    if name == "hospitals":
        hospitals = Hospital.query.all()
        for hospital in hospitals:
            hospital_data = {}
            hospital_data["id"] = hospital.id
            hospital_data["name"] = hospital.hname
            hospital_data["email"] = hospital.email
            hospital_data["mob"] = hospital.mob
            hospital_data["city"] = hospital.city
            hospital_data["state"] = hospital.state
            output.append(hospital_data)
        return jsonify({"hospitals" : output})
    if name == "labs":
        labs = Lab.query.all()
        for lab in labs:
            lab_data = {}
            lab_data["id"] = lab.id
            lab_data["name"] = lab.lname
            lab_data["email"] = lab.email
            lab_data["mob"] = lab.mob
            lab_data["city"] = lab.city
            lab_data["state"] = lab.state
            output.append(lab_data)
        return jsonify({"labs" : output})

"""API to register a user,doctor,hospital and lab"""

@app.route("/api/add/<string:name>", methods=["POST"])
def addhospital(name):
    if name == "user":
        data = request.get_json(force=True)
        pas = pbkdf2_sha256.encrypt(data["password"])
        newuser = User(fname=data['fname'],lname=data["lname"],city=data['city'],state=data['state'],mob=data['mob'],email=data['email'],password=pas)
        db.session.add(newuser)
        db.session.commit()
        return jsonify({"message" : "new user created"})

    if name == "doctor":
        data = request.get_json(force=True)
        pas = pbkdf2_sha256.encrypt(data["password"])
        newdoc = Doctor(fname=data['fname'],lname=data["lname"],city=data['city'],state=data['state'],mob=data['mob'],email=data['email'],password=pas,specialization=data["specialization"])
        db.session.add(newdoc)
        db.session.commit()
        return jsonify({"message" : "new doctor created"})

    if name == "hospital":
        data = request.get_json(force=True)
        pas = pbkdf2_sha256.encrypt(data["password"])
        newhos = Hospital(hname=data['hname'],city=data['city'],state=data['state'],mob=data['mob'],email=data['email'],password=pas)
        db.session.add(newhos)
        db.session.commit()
        return jsonify({"message" : "new hospital created"})
    
    if name == "lab":
        data = request.get_json(force=True)
        pas = pbkdf2_sha256.encrypt(data["password"])
        newlab = Lab(lname=data['lname'],city=data['city'],state=data['state'],mob=data['mob'],email=data['email'],password=pas)
        db.session.add(newlab)
        db.session.commit()
        return jsonify({"message" : "new lab created"})

"""API to delete a single user,doctor,hospital and lab"""

@app.route("/api/delete/<string:name>/<int:uid>",methods=["DELETE"])
def deleteapi(name,uid):
    if name == "user":
        user = User.query.filter_by(id=uid).first()
        if user is None:
            return jsonify({"message" : "no user found!"})
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message" : "user deleted"})
    if name == "doctor":
        doctor = Doctor.query.filter_by(id=uid).first()
        if doctor is None:
            return jsonify({"message" : "no doctor found!"})
        db.session.delete(doctor)
        db.session.commit()
        return jsonify({"message" : "doctor deleted"})
    if name == "hospital":
        hospital = Hospital.query.filter_by(id=uid).first()
        if hospital is None:
            return jsonify({"message" : "no hospital found!"})
        db.session.delete(hospital)
        db.session.commit()
        return jsonify({"message" : "hospital deleted"})
    if name == "lab":
        lab = Lab.query.filter_by(id=uid).first()
        if lab is None:
            return jsonify({"message" : "no lab found!"})
        db.session.delete(lab)
        db.session.commit()
        return jsonify({"message" : "lab deleted"})

if __name__== "__main__":
    main()
