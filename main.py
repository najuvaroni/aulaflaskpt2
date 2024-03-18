from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app= Flask (__name__)
app.config['SECRET_KEY'] = 'chave'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/financeiro'
db = SQLAlchemy(app)

class Financeiro(db.Model):
    id_despesa = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_receita = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_receita = db.Column(db.String(100))
    nome_despesa = db.Column(db.String(100))
    valor_despesa = db.Column(db.Integer)
    valor_receita = db.Column(db.Integer)
    data_receita = db.Column(db.Interger)
    data_despesa = db.Column(db.Interger)
@app.route('/')
def index():
    financia = Financeiro.query.all()
    return render_template('cadastro_livros.html', outro=financia)

@app.route('/novo')
def novo():
        return render_template('novo.html', titulo='Novo Livro')

@app.route('/criar', methods=['POST'])
def criar():
    titulo = request.form['titulo']
    autor = request.form['autor']
    ano_publicacao = request.form['ano_publicacao']

    livro = Financeiro.query.filter_by(titulo=titulo).first()
    if livro:
        flash("Livro já existente!")
        return redirect(url_for('novo'))

    novo_livro = Financeiro(titulo=titulo, autor=autor, ano_publicacao=ano_publicacao)
    db.session.add(novo_livro)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/editar/<int:id>')
def editar(id):
    livro = Financeiro.query.filter_by(id_livro=id).first()
    return render_template('editar.html',
                           titulo='Editando Livro', livro=livro)

@app.route('/atualizar', methods=['POST'])
def atualizar():
    livro = Financeiro.query.filter_by(id_livro=request.form['id']).first()
    livro.titulo= request.form['titulo']
    livro.autor = request.form['autor']
    livro.ano_publicacao = request.form['ano_publicacao']

    db.session.add(livro)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/deletar/<int:id>')
def deletar(id):
    Financeiro.query.filter_by(id_livro=id).delete()
    db.session.commit()
    flash('Livro excluido com sucesso.')
    return redirect(url_for('index'))


if __name__  == '__main__':
    app.run(debug=True)