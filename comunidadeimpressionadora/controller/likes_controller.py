from comunidadeimpressionadora import app, database
from comunidadeimpressionadora.models import LikeG, LikeNG


def add_like(user, post):
    with app.app_context():
        verificaLike = LikeNG.query.filter_by(id_usuario=user, id_post=post).first()
        if verificaLike:
            database.session.delete(verificaLike)
            database.session.commit()
            like_1 = LikeG(id_usuario=user, id_post=post)
            database.session.add(like_1)
            database.session.commit()
        else:
            verificaLike2 = LikeG.query.filter_by(id_usuario=user, id_post=post).first()
            if verificaLike2:
                database.session.delete(verificaLike2)
                database.session.commit()
            else:
                like_1 = LikeG(id_usuario=user, id_post=post)
                database.session.add(like_1)
                database.session.commit()

def add_deslike(user, post):
    with app.app_context():
        verificaLike = LikeG.query.filter_by(id_usuario=user, id_post=post).first()
        if verificaLike:
            database.session.delete(verificaLike)
            database.session.commit()
            like_1 = LikeNG(id_usuario=user, id_post=post)
            database.session.add(like_1)
            database.session.commit()
        else:
            verificaLike2 = LikeNG.query.filter_by(id_usuario=user, id_post=post).first()
            if verificaLike2:
                database.session.delete(verificaLike2)
                database.session.commit()
            else:
                like_1 = LikeNG(id_usuario=user, id_post=post)
                database.session.add(like_1)
                database.session.commit()

