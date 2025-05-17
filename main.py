import os
from io import BytesIO
import random
from PIL import Image

from form import *
from flask import Flask, render_template, redirect, request, session
from data import db_session
from flask_login import LoginManager, login_user
from data.users import User

from data.ad import Ad

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/blogs.db")
db_sess = db_session.create_session()

global images
images = []

import requests

server_address = 'http://geocode-maps.yandex.ru/1.x/?'
api_key = '8013b162-6b42-4997-9691-77b7074026e0'

k = []
ads = dict()
for ad in db_sess.query(Ad).all():
    ads["photo"] = ad.photo.split(", ")
    ads["name"] = ad.name
    ads["id"] = ad.id
    k.append(ads)
    ads = dict()

global past
past = ""


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/', methods=['GET', 'POST'])
def entry():
    global past
    session['name'] = "Войти"
    past = "/"
    params = {"ad": k}
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            session['name'] = f"{user.surename}_{user.name}"
            return redirect("/home")
        return render_template('entry.html',
                               message="Неправильный логин или пароль",
                               form=form, name=session['name'])
    return render_template('entry.html', **params, form=form, name=session['name'])


@app.route('/home', methods=['GET', 'POST'])
def home():
    if session['name'] != "Войти":
        k = []
        ads = dict()
        for ad in db_sess.query(Ad).all():
            ads["photo"] = ad.photo.split(", ")
            ads["name"] = ad.name
            ads["id"] = ad.id
            k.append(ads)
            ads = dict()
        global past
        past = "/home"
        params = {"ad": k}
        form = LoginForm()
        return render_template('home.html', **params, form=form, name=session['name'])
    else:
        return session['name']


@app.route('/new_ad', methods=['GET', 'POST'])
def new_ad():
    global images
    if session['name'] != "Войти":
        form = СreateForm()
        params = {"method": request.method}
        if request.method == 'GET':
            params["images"] = images
            return render_template("new_ad.html", **params, form=form, name=session['name'], past=past)

        elif form.validate_on_submit():
            n = session['name'].split("_")
            Ad1 = Ad(creator_id=db_sess.query(User).filter(User.name == n[1], User.surename == n[0]).first().id,
                     photo=" ,".join(images), address=form.address.data, name=form.name.data,
                     description=form.description.data,
                     category=form.category.data, design=form.design.data, floor=form.floor.data,
                     purpose=form.purpose.data,
                     square=form.square.data, state=form.state.data)
            db_sess.add(Ad1)
            db_sess.commit()

        elif request.method == 'POST':
            f = request.files['file']
            n = 0
            for currentdir, dirs, files in os.walk('static/img'):
                n = len(files)
            p = f"{n + 1}.jpg"
            with open(f"static/img/{p}", "wb") as k:
                k.write(f.read())
            images.append(p)
            params["images"] = images
            return render_template("new_ad.html", **params, form=form, name=session['name'], past=past)
        return render_template('new_ad.html', **params, form=form, name=session['name'], past=past)


@app.route('/menu', methods=['GET', 'POST'])
def menu():
    params = {"ad": k}
    form = FindForm()
    if form.validate_on_submit():
        h = []
        ads = dict()
        from sqlalchemy import or_
        for ad in db_sess.query(Ad).filter(or_(Ad.floor == form.floor.data, form.floor.data == ""),
                                           or_(Ad.category == form.category.data, form.category.data == ""),
                                           or_(Ad.design == form.design.data, form.design.data == ""),
                                           or_(Ad.purpose == form.purpose.data, form.purpose.data == ""),
                                           or_(Ad.square == form.square.data, form.square.data == ""),
                                           or_(Ad.state == form.state.data, form.state.data == "")):
            ads["photo"] = ad.photo.split(", ")
            ads["name"] = ad.name
            ads["id"] = ad.id
            h.append(ads)
            ads = dict()
        params = {"ad": h}
    return render_template('menu.html', **params, form=form, name=session['name'], past=past)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surename=form.surename.data, name=form.name.data, age=form.age.data,
            address=form.address.data, email=form.email.data, hashed_password=form.password.data
        )
        db_sess.add(user)
        db_sess.commit()
        session['name'] = f"{user.surename}_{user.name}"
        return redirect('/home')
    return render_template('register.html', title='Регистрация', form=form, name=session['name'])


@app.route('/description/<id>', methods=['GET', 'POST'])
def description(id):
    h = []
    ad = db_sess.query(Ad).filter(Ad.id == id).first()
    ads = dict()
    ads["photo"] = ad.photo.split(", ")
    ads["name"] = ad.name
    ads["floor"] = ad.floor
    ads["category"] = ad.category
    ads["design"] = ad.design
    ads["purpose"] = ad.purpose
    ads["square"] = ad.square
    ads["state"] = ad.state
    ads["address"] = ad.address
    us = db_sess.query(User).filter(User.id == ad.creator_id).first()
    ads["email"] = us.email
    h.append(ads)
    params = {"ad": h}
    print(params)
    toponym_to_find = " ".join(params["ad"][0]["address"])

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)

    if not response:
        pass
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    delta = "0.005"
    apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"

    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta, delta]),
        "apikey": apikey,

    }

    map_api_server = "https://static-maps.yandex.ru/v1"
    response = requests.get(map_api_server, params=map_params)
    im = BytesIO(response.content)
    opened_image = Image.open(im)
    opened_image.save("static/address/A.png")
    return render_template('description.html', **params, image="static/address/A.png", name=session['name'], past=past)


@app.route('/my_ad', methods=['GET', 'POST'])
def my_ad():
    if session['name'] != "Войти":
        n = session['name'].split("_")
        k1 = []
        ads = dict()
        for ad in db_sess.query(Ad).filter(
                Ad.creator_id == db_sess.query(User).filter(User.name == n[1], User.surename == n[0]).first().id):
            ads["photo"] = ad.photo.split(", ")
            ads["name"] = ad.name
            ads["id"] = ad.id
            k1.append(ads)
            ads = dict()
        params = {"ad": k1}
        form = LoginForm()
        return render_template('my_ad.html', **params, form=form, name=session['name'], past=past)
    else:
        return session['name']


@app.route('/delete/<id>', methods=['GET', 'POST'])
def delete(id):
    if session['name'] != "Войти":
        import sqlite3
        conn = sqlite3.connect('db/blogs.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ad WHERE id=?", (id,))
        conn.commit()
        my_ad()
    else:
        return session['name']


def main():
    db_session.global_init("db/blogs.db")
    port = int(os.environ.get("PORT", 8080))
    app.run(port=port, debug=True)


if __name__ == '__main__':
    main()
