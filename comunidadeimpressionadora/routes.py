from flask import render_template, flash, redirect, url_for, request, abort

from comunidadeimpressionadora.controller.likes_controller import add_like, add_deslike
from comunidadeimpressionadora.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost, \
    FormCriarComentario, FormValidarCodigoEmail
from comunidadeimpressionadora import app, database, bcrypt
from comunidadeimpressionadora.models import Usuario, Post, Comentario, LikeNG, LikeG
from flask_login import login_user, logout_user, current_user, login_required
import secrets
import os
from PIL import Image
from sqlalchemy import update
from comunidadeimpressionadora.util.envia_codigo_email import enviar_email
from comunidadeimpressionadora.util.gera_codigo import gerar_cod


@app.route("/", methods=['GET', 'POST'])
def home():

    form_com = FormCriarComentario()

    if form_com.validate_on_submit():
        if current_user.is_authenticated:
            post = Comentario(
                texto_comentario=form_com.comentario.data, autor_com=current_user, id_post=form_com.id_post.data)
            database.session.add(post)
            database.session.commit()
            flash('Comentário slavo com sucesso!', 'alert-success')
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))

    posts = Post.query.order_by(Post.id.desc())
    com = Comentario.query.order_by(Comentario.id.desc())
    if current_user.is_authenticated:
        deslike = LikeNG.query.all()
        like = LikeG.query.all()
        deslike_ = []
        like_ = []
        for l in deslike:
            if l.id_usuario == current_user.id:
                deslike_.append(l.id_post)
        for l in like:
            if l.id_usuario == current_user.id:
                like_.append(l.id_post)
    else:
        like_ = []
        deslike_=[]
    return render_template('home.html', posts=posts, form=form_com, com=com, deslike=deslike_, like=like_)


@app.route('/validar_email', methods=['GET', 'POST'])
def contato():
    form = FormValidarCodigoEmail()

    if form.validate_on_submit():
        if form.codigo.data == current_user.codigo_email:
            stmt = update(Usuario).values(cod_ativado=True).where(Usuario.id == current_user.id)
            database.session.execute(stmt)
            database.session.commit()
            flash('Seu código foi ativado com sucesso!', 'alert-success')
            return redirect(url_for('home'))
        else:
            flash('código invalido!', 'alert-success')
    return render_template('contato.html', form=form)


@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criar_conta = FormCriarConta()

    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha,form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso para o e-mail: {form_login.email.data}', 'alert-success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                if current_user.cod_ativado:
                    return redirect(url_for('home'))
                else:
                    return redirect(url_for('contato'))
        else:
            flash('Falha de Login. Email ou Senha Incorretos', 'alert-danger')
    if form_criar_conta.validate_on_submit() and 'botao_submit_criar_conta' in request.form:
        #enviando o código de ativação
        codigo = gerar_cod()
        if enviar_email(form_criar_conta.email.data, 'O seu codigo de acesso {}'.format(codigo)):
            senha_crypt = bcrypt.generate_password_hash(form_criar_conta.senha.data)
            usuario = Usuario(
                username=form_criar_conta.username.data,
                apelido=form_criar_conta.apelido.data,
                data_nascimento=form_criar_conta.aniversario.data,
                codigo_email=codigo,
                bloqueado=False,
                cod_ativado=False,
                tipo_user=3,
                email=form_criar_conta.email.data,
                senha=senha_crypt)
            database.session.add(usuario)
            database.session.commit()
            flash(f'Um código de ativação foi enviado para seu email: {form_criar_conta.email.data} \n ', 'alert-success')
            flash(f'Faça o login: {form_criar_conta.email.data} \n ', 'alert-success')
        else:
            flash('Erro ao enviar código de ativação', 'alert-success')

        return redirect(url_for('login'))

    return render_template('login.html', form_login=form_login, form_criar_conta=form_criar_conta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Logout feito com sucesso!', 'alert-success')
    return redirect(url_for('home'))



@app.route('/perfil')
@login_required
def perfil():
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)

@app.route('/post/criar', methods=['GET', 'POST'])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(sub_titulo=form.sub_titulo.data, titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post Gravado com Sucesso', 'alert-success')
        return redirect(url_for('home'))

    return render_template('criarpost.html', form=form)

def salvar_imagem(imagem):

    # adicionar um código aleatório no nome da imagem
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    # reduzir o tamanho da imagem
    tamanho = (500, 500)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    # salvar a imagem na pasta fotos_perfil
    imagem_reduzida.save(caminho_completo)
    # mudar o campo foto_perfil do usiuario para o novo nome da imagem
    return nome_arquivo

def atualizar_cursos(form):
    lista_cursos = []
    for campo in form:
        if 'curso' in campo.name:
            if campo.data:
                lista_cursos.append(campo.label.text)


    if len(lista_cursos) > 0:
        return ';'.join(lista_cursos)
    else:
        return 'Não informado'

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()
        flash('Perfil editado com sucesso!', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == "GET":
        form.email.data = current_user.email
        form.username.data = current_user.username
        #marca os checkbox
        if 'Curso Excell' in current_user.cursos.split(';'):
            form.curso_excell.data = True
        if 'Curso Power Point' in current_user.cursos.split(';'):
            form.curso_ppt.data = True
        if 'Curso Python' in current_user.cursos.split(';'):
            form.curso_python.data = True
        if 'Curso VBA' in current_user.cursos.split(';'):
            form.curso_vba.data = True
        if 'Curso SQL' in current_user.cursos.split(';'):
            form.curso_sql.data = True
        if 'Curso Power BI' in current_user.cursos.split(';'):
            form.curso_powerbi.data = True

    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)

@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.sub_titulo.data = post.sub_titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.sub_titulo = form.sub_titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post Alterado com Sucesso', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)

@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post excluido com Sucessos', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)

@app.route('/home/<post_id>/gostei', methods=['GET', 'POST'])
@login_required
def gostei_post(post_id):
    user = current_user.id
    add_like(user, post_id)

    return redirect(url_for('home'))


@app.route('/home/<post_id>/nao_gostei', methods=['GET', 'POST'])
@login_required
def nao_gostei_post(post_id):
    user = current_user.id
    add_deslike(user, post_id)

    return redirect(url_for('home'))

