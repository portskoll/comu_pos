from comunidadeimpressionadora import database, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    apelido = database.Column(database.String, nullable=False, default='leitor')
    bloqueado = database.Column(database.Boolean, nullable=False, default=False)
    cod_ativado = database.Column(database.Boolean, nullable=False, default=False)
    codigo_email = database.Column(database.String, nullable=False, default='000000')
    data_nascimento = database.Column(database.Date, nullable=False)
    tipo_user = database.Column(database.Integer, nullable=False, default=3)# 1 ADM - 2 AUTOR -3 LEITOR
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default='default.jpg')
    posts = database.relationship('Post', backref='autor', lazy=True)
    comentarios = database.relationship('Comentario', backref='autor_com', lazy=True)
    cursos = database.Column(database.String, nullable=False, default='Não informado')

    def contar_posts(self):
        return len(self.posts)


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    sub_titulo = database.Column(database.String, nullable=False)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.String, nullable=False)
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    likes_g = database.relationship('LikeG', backref='post_like_gostei', lazy=True)
    likes_ng = database.relationship('LikeNG', backref='post_like_ngostei', lazy=True)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)

    def contar_likes(self):
        return len(self.likes_g)

    def contar_deslikes(self):
        return len(self.likes_ng)


class Comentario(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    texto_comentario = database.Column(database.String, nullable=False)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    id_post = database.Column(database.Integer, nullable=False)


class LikeG(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    id_usuario = database.Column(database.Integer, nullable=False)
    id_post = database.Column(database.Integer, database.ForeignKey('post.id'), nullable=False)




class LikeNG(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    id_usuario = database.Column(database.Integer, nullable=False)
    id_post = database.Column(database.Integer, database.ForeignKey('post.id'), nullable=False)



