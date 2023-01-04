from comunidadeimpressionadora import app, database
from comunidadeimpressionadora.models import Usuario, Post


""" with app.app_context():
    database.create_all()
 """


# with app.app_context():
#     usuario_1 = Usuario(username='Henrique',email='portskoll@gmail.com',senha='1234567')
#     usuario_2 = Usuario(username='Fabio Portella',email='portskoll@gmail.bat',senha='1234567')
#     database.session.add(usuario_1)
#     database.session.add(usuario_2)
#     database.session.commit()


# with app.app_context():
#     usuarios = Usuario.query.all()
#     for user in usuarios:
#         print('User : {} -- Cursos: {} -- Email {}'.format(user.username, user.cursos, user.email))

with app.app_context():
    posts = Post.query.all()
    for post in posts:
        user = Usuario.query.filter_by(id=post.id_usuario).first()
        print(user.username)
        print('Titulo : {} -- Corpo: {} -- Data: {}'.format(post.titulo, post.corpo, post.data_criacao))