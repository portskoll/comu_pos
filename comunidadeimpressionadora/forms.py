from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, HiddenField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from comunidadeimpressionadora.models import Usuario
from flask_login import current_user

class FormCriarConta(FlaskForm):
    username = StringField('Nome de Usuario', validators=[DataRequired()])
    apelido = StringField('Apelido', validators=[DataRequired()])
    aniversario = DateField('Data de Nascimento', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criar_conta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Email já cadastrado. Cadastre-se com outro email ou faça login para continual')


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(),Length(6,20)])
    lembrar_dados = BooleanField('Lembrar Senha')
    botao_submit_login = SubmitField('Login')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de Usuario', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    foto_perfil = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['png', 'jpg'])])
    curso_excell = BooleanField('Curso Excell')
    curso_vba = BooleanField('Curso VBA')
    curso_powerbi = BooleanField('Curso Power BI')
    curso_python = BooleanField('Curso Python')
    curso_ppt = BooleanField('Curso Power Point')
    curso_sql = BooleanField('Curso SQL')
    botao_submit_editarperfil = SubmitField('Salvar Perfil')

    def validate_email(self, email):
        if current_user.email != email.data:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError('Já existe um usuario com este E-mail, cadastre outro E-mail')


class FormCriarPost(FlaskForm):
    titulo = StringField('Titulo do post', validators=[DataRequired(), Length(2, 140)])
    sub_titulo = StringField('Sub Titulo do post', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Escreva seu Post Aqui', validators=[DataRequired()])
    botao_submit = SubmitField('Salvar')

class FormCriarComentario(FlaskForm):
    comentario = StringField('Comentar', validators=[DataRequired(), Length(2, 140)])
    id_post = HiddenField('id_post')
    botao_submit = SubmitField('Salvar')

class FormValidarCodigoEmail(FlaskForm):
    codigo = StringField('Digite o código recebido no seu e-mail', validators=[DataRequired(), Length(6)])
    botao_submit = SubmitField('Enviar')