from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///basa_visechek.db'
db = SQLAlchemy


class Visechka(db.Model):
    id = db.Column(db.Integer, primary_key=True) #Порядковый номер высечки в базе данных
    visechka_no = db.Column(db.Text, nullable=False) #Номер высечки присвоенный технологом
    size = db.Column(db.Text, nullable=False) #Размер высечки
    matherial = db.Column(db.Text, nullable=False)  #Для какого материала высечка
    wide = db.Column(db.Integer, nullable=False) #ширина высечки в мм
    length = db.Column(db.Integer, nullable=False)  #длинна высечки в мм
    streams = db.Column(db.Integer, nullable=False) #Количество ручьев в высечке
    el_in_streams = db.Column(db.Integer, nullable=False)  #Количество элементов в одном ручье
    shaft = db.Column(db.Integer, nullable=False)  #Вал на котором располагается высечка
    form = db.Column(db.Text, nullable=False) #форма высечки
    iznos = db.Column(db.Integer, nullable=False) #пробег высечки в м.п.


@app.route('/')
def main():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
