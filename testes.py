
from comunidadeimpressionadora import app, database
from comunidadeimpressionadora.controller.likes_controller import add_like
from comunidadeimpressionadora.models import Usuario, Post, LikeG, LikeNG
from sqlalchemy import update


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

# with app.app_context():
#     posts = Post.query.all()
#     for post in posts:
#         user = Usuario.query.filter_by(id=post.id_usuario).first()
#         print(user.username)
#         print('Titulo : {} -- Corpo: {} -- Data: {}'.format(post.titulo, post.corpo, post.data_criacao))




# with app.app_context():
#     # stmt = update(Usuario).values(cod_ativado=False).where(Usuario.id == 1)
#     stmt = update(Usuario).values(tipo_user=1).where(Usuario.id == 1)
#     database.session.execute(stmt)
#     database.session.commit()
#     users = Usuario.query.all()
#     for user in users:
#         print(user.username)
#         print(
#             ' id : {} \n Username: {} \n Apelido: {} \n Bloqueado: {} \n CodATi: {} \n DataNasc: {} \n TipoUser: {} \n Email: {} \n codigo: {}'.format(
#                 user.id,
#                 user.username,
#                 user.apelido,
#                 user.bloqueado,
#                 user.cod_ativado,
#                 user.data_nascimento,
#                 user.tipo_user,
#                 user.email,
#                 user.codigo_email
#             ))


# with app.app_context():
#     print("oi")
#     users = Usuario.query.all()
#     for user in users:
#
#         print(user.username)
#         print(' id : {} \n Username: {} \n Apelido: {} \n Bloqueado: {} \n CodATi: {} \n DataNasc: {} \n TipoUser: {} \n Email: {} \n Senha: {}'.format(
#             user.id,
#             user.username,
#             user.apelido,
#             user.bloqueado,
#             user.cod_ativado,
#             user.data_nascimento,
#             user.tipo_user,
#             user.email,
#             user.senha
#         ))


# with app.app_context():
#     like_1 = LikeG(id_usuario=1, id_post=2)
#     like_2 = LikeNG(id_usuario=1, id_post=1)
#     database.session.add(like_1)
#     database.session.add(like_2)
#     database.session.commit()


# with app.app_context():
#     deuLike = 0
#     id_user = 1
#     id_post = 1
#
#     verificaLike = LikeG.query.filter_by(id_usuario=id_user, id_post=id_post).first()
#     if verificaLike:
#         if verificaLike.gostei == deuLike:
#             print('excluir like')
#         else:
#             print('Trocar like')
#     else:
#         print('Criar novo like')
#     # like_1 = Like(gostei=1, id_usuario=1, id_post=1)
#     #
#     # database.session.add(like_1)
#     # database.session.commit()


# with app.app_context():
#
#     likes = Like.query.all()
#     for like in likes:
#         print('postID: {} - Usuario: {} - Goste {} - NGostei {}'.format(like.post_like.id, like.id_usuario ))



add_like(1,1)