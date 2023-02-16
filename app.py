from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///basa_visechek.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Visechka(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Порядковый номер высечки в базе данных
    visechka_no = db.Column(db.String(20), nullable=False)  # Номер высечки присвоенный технологом
    size = db.Column(db.String(20), nullable=False)  # Размер высечки
    matherial = db.Column(db.String(20), nullable=False)  # Для какого материала высечка
    wide = db.Column(db.Integer, nullable=False)  # ширина высечки в мм
    length = db.Column(db.Integer, nullable=False)  # длинна высечки в мм
    streams = db.Column(db.Integer, nullable=False)  # Количество ручьев в высечке
    el_in_streams = db.Column(db.Integer, nullable=False)  # Количество элементов в одном ручье
    shaft = db.Column(db.Integer, nullable=False)  # Вал на котором располагается высечка
    form = db.Column(db.String(20), nullable=False)  # форма высечки
    iznos = db.Column(db.Integer, nullable=False)  # пробег высечки в м.п.

    def __repr__(self):
        return f'<Высечка {self.size}>'


@app.route('/')
def main():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/plenka')
def plenka():
    visechki = Visechka.query.filter(Visechka.matherial == 'Пленка').all()
    return render_template('plenka.html', visechki=visechki)

@app.route('/<int:id>')
def detail(id):
    visechka = Visechka.query.get(id)
    return render_template('detail.html', visechka=visechka)

@app.route('/<int:id>/delete')
def delete(id):
    visechka = Visechka.query.get_or_404(id)

    try:
        db.session.delete(visechka)
        db.session.commit()
        return redirect('/')
    except:
        return "При удалении возникла ошибка"

@app.route('/<int:id>/update', methods=['POST', 'GET'])
def update(id):
    visechka = Visechka.query.get(id)
    if request.method == 'POST':
        visechka.visechka_no = request.form['visechka_no']
        visechka.matherial = request.form['matherial']
        visechka.wide = request.form['wide']
        visechka.length = request.form['length']
        visechka.size = str(visechka.wide) + 'x' + str(visechka.length)
        visechka.streams = request.form['streams']
        visechka.el_in_streams = request.form['el_in_streams']
        visechka.shaft = request.form['shaft']
        visechka.form = request.form['form']
        visechka.iznos = request.form['iznos']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'При добавлении записи возникла ощибка'
    else:
        visechka = Visechka.query.get(id)
        return render_template('update.html', visechka=visechka)

@app.route('/bumaga')
def bumaga():
    visechki = Visechka.query.filter(Visechka.matherial == 'Бумага').all()
    return render_template('bumaga.html', visechki=visechki)

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        visechka_no = request.form['visechka_no']
        matherial = request.form['matherial']
        wide = request.form['wide']
        length = request.form['length']
        size = str(wide) + 'x' + str(length)
        streams = request.form['streams']
        el_in_streams = request.form['el_in_streams']
        shaft = request.form['shaft']
        form = request.form['form']
        iznos = 0

        visechka = Visechka(visechka_no=visechka_no, size=size, matherial=matherial, wide=wide, length=length,
                            streams=streams, el_in_streams=el_in_streams, shaft=shaft, form=form, iznos=iznos)

        try:
            db.session.add(visechka)
            db.session.commit()
            return redirect('/')
        except:
            return "Произошла ошибка"
    else:
        return render_template('create.html')


if __name__ == '__main__':
    app.run(debug=True)
