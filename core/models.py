from datetime import timedelta
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from stdimage import StdImageField
import uuid


def get_file_path(_instance_, filename):  # _instance_ > é a instância do modelo que está chamando upload_to.
    ext = filename.split(".")[-1]  # recebe um arquivo e quebra o texto pegando a última parte dele.
    filename = f'{uuid.uuid4()}.{ext}'  # gera um hexadecimal e conecta com a parte tirada.
    return filename


class UsuarioManager(BaseUserManager):

    # use_in_migrations -> Informa que o modelo pode ser criado e ser salvo sua tabela no bd
    use_in_migrations = True

    class Meta:
        abstract = True

    # Método que irá normalizar os dados e salvá-los no banco de dados para o usuário.
    def _create_user(self, email, password, **extra_fields):
        """
        :param email: é obrigatório e recebe uma normalização de e_mails para casos de: acentuação e maiúsculas.
        :param password: é obrigatório o usuário informar a senha.
        :param extra_fields: campos extras que pode ou não ter.
        :return: user
        """
        if not email:
            raise ValueError('O e-mail é obrigatório!')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields)  # cria o e-mail, username (com o email) e os
        # outros dados.
        user.set_password(password)  # salva e encripta a senha
        user.save(using=self._db)
        return user

    # Cria usuário comum
    def create_user(self, email, password=None, **extra_fields):
        # extra_fields.setdefault("is_staff", True) # Só para casos do usuário fazer parte do administrativo
        extra_fields.setdefault("is_superuser", False)  # Cria usuário comum.
        return self._create_user(email, password, **extra_fields)

    # Cria superusuário comum
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser precisa ter is_superuser=True")
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser precisa ter is_staff=True")

        return self._create_user(email, password, **extra_fields)


class CustomUsuario(AbstractUser):
    data_nascimento = models.DateField("Nascimento", null=False)
    email = models.EmailField("E-mail", unique=True)
    is_staff = models.BooleanField("Membro da equipe", default=False)  # Todos os usuários por padrão são staff.

    USERNAME_FIELD = "email"  # por padrão o django ao varrer, vai pegar primeiro o e-mail
    REQUIRED_FIELDS = ["first_name", "last_name", "data_nascimento"]

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.get_full_name()

    # objects = UsuarioManager() -> Irá pegar o modelo com métodos de autenticação customizado criado, se não informado
    # pegará o método de autenticação de usuários padrão do django.
    objects = UsuarioManager()


class BiotipoUsuario(models.Model):
    TIPO_CORPO = [
        ("ectomorfo", "Ectomorfo"),
        ("mesomorfo", 'Mesomorfo'),
        ("endomorfo", "Endomorfo"),
    ]

    SITUACAO = [
        ("sedentário", "Sedentário"),
        ("regular", "Regular"),
        ("praticante", "Praticante")
    ]

    altura = models.DecimalField("Altura (m)", max_digits=3, decimal_places=2, validators=[
        MinValueValidator(0.50),
        MaxValueValidator(2.50)
    ], null=False)
    peso = models.DecimalField("Peso (kg)", max_digits=5, decimal_places=2, null=False)
    tipo_corporal = models.CharField("Tipo do corpo", choices=TIPO_CORPO, max_length=20, blank=False)
    situacao = models.CharField("Situação", choices=SITUACAO, max_length=20, blank=False)
    usuario = models.OneToOneField(CustomUsuario, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Biotipo"
        verbose_name_plural = "Biotipos"


class Exercicio(models.Model):
    PRATICANTE = [
        ("sedentário", "Sedentário"),
        ("regular", "Regular"),
        ("praticante", "Praticante")
    ]

    TIPO_CORPO = [
        ("ectomorfo", "Ectomorfo"),
        ("mesomorfo", "Mesomorfo"),
        ("endomorfo", "Endomorfo")
    ]

    nome = models.CharField("Nome", max_length=40, blank=False)
    objetivo = models.CharField("Objetivo", max_length=80, blank=False)
    repeticoes_ou_tempo = models.CharField("Repetições/Tempo", max_length=10, blank=False)
    pausa = models.DurationField("Pausa (min/s)", default=timedelta(seconds=90))
    imc = models.DecimalField("Imc", max_digits=4, decimal_places=2, blank=False)
    praticante = models.CharField("Situação", choices=PRATICANTE, max_length=20, blank=False)
    tipo_corporal = models.CharField("Tipo do corpo", choices=TIPO_CORPO, max_length=20, blank=True)
    imagem = StdImageField("Imagem", upload_to=get_file_path, variations={
        "thumb": {
            "width": 480,
            "height": 480,
            "crop": True
        }
    })

    class Meta:
        verbose_name = "Exercício"
        verbose_name_plural = "Exercícios"

    def __str__(self):
        return self.nome


class Alimentacao(models.Model):

    TAMANHO = [
        ("pequeno", "Pequeno"),
        ("médio", "Médio"),
        ("grande", "Grande")
    ]

    prato = models.CharField("Prato", max_length=150, blank=False)
    descricao = models.CharField("Descrição", max_length=300, blank=False)
    calorias = models.IntegerField("Calorias", null=False)
    peso = models.IntegerField("Peso", null=False)
    tamanho_prato = models.CharField("Tamanho do prato", choices=TAMANHO, max_length=20, blank=False)
    imc = models.DecimalField("Imc", max_digits=4, decimal_places=2, blank=False)
    imagem = StdImageField("Imagem", upload_to=get_file_path, variations={
        "thumb": {
            "width": 480,
            "height": 480,
            "crop": True
        }
    })

    class Meta:
        verbose_name = "Alimento"
        verbose_name_plural = "Alimentos"

    def __str__(self):
        return self.prato


class Visitantes(models.Model):
    titulo = models.CharField("Título", max_length=40)
    descricao = models.CharField("Descrição", max_length=300)
    imagem = StdImageField("Imagem", upload_to=get_file_path, variations={
        "thumb": {
            "width": 480,
            "height": 480,
            "crop": True
        }
    })

    icone = StdImageField("Ícone", upload_to=get_file_path, variations={
        "thumb": {
            "width": 480,
            "height": 480,
            "crop": True
        }
    })

    class Meta:
        verbose_name = "Visitante"
        verbose_name_plural = "Visitantes"

    def __str__(self):
        return self.titulo


class Servicos(models.Model):
    titulo = models.CharField("Título", max_length=20)
    descricao = models.CharField("Descrição", max_length=50)
    imagem = StdImageField("Imagem", upload_to=get_file_path, variations={
        "thumb": {
            "width": 82,
            "height": 82,
            "crop": True
        }
    })

    class Meta:
        verbose_name = "Serviço"
        verbose_name_plural = "Serviços"

    def __str__(self):
        return self.titulo


class Objetivos(models.Model):
    titulo = models.CharField("Título", max_length=20)
    descricao = models.CharField("Descrição", max_length=50)
    imagem = StdImageField("Imagem", upload_to=get_file_path, variations={
        "thumb": {
            "width": 362,
            "height": 506,
            "crop": True
        }
    })

    class Meta:
        verbose_name = "Objetivo"
        verbose_name_plural = "Objetivos"

    def __str__(self):
        return self.titulo


class TiposTreinos(models.Model):
    treino = models.CharField("Treino", max_length=20)
    repeticoes_ou_tempo_min = models.CharField("Rep. ou tempo mínimo", max_length=20)
    repeticoes_ou_tempo_max = models.CharField("Rep. ou tempo máximo", max_length=20)

    class Meta:
        verbose_name = "Tipo de treino"
        verbose_name_plural = "Tipos de treinos"

    def __str__(self):
        return self.treino


class RedesSociais(models.Model):
    REDESOCIAIS = [
        ("fa fa-pinterest", "Pinterest"),
        ("fa fa-facebook", "Facebook"),
        ("fa fa-instagram", "Instagram"),
        ("fa fa-dribbble", "Dribbble"),
        ("fa fa-behance", "Behance"),
        ("fa fa-youtube", "Youtube")
    ]

    rede_social = models.CharField("Rede social", max_length=200)
    icone = models.CharField("Tamanho do prato", choices=REDESOCIAIS, max_length=50, blank=False)

    class Meta:
        verbose_name = "Rede social"
        verbose_name_plural = "Redes sociais"

    def __str__(self):
        return self.rede_social


# Criar model para links de vídeos de aquecimento
class Aquecimentos(models.Model):
    nome = models.CharField("Nome", max_length=200)
    link = models.CharField("Link",  max_length=400)
    imagem = StdImageField("Imagem", upload_to=get_file_path, variations={
        "thumb": {
            "width": 1280,
            "height": 720,
            "crop": True
        }
    }, blank=False)

    class Meta:
        verbose_name = "Aquecimento"
        verbose_name_plural = "Aquecimentos"

    def __str__(self):
        return self.nome


class Contatos(models.Model):
    endereco = models.CharField("Endereço", max_length=50)
    telefone = PhoneNumberField("Telefone", region="BR")
    email = models.EmailField("E-mail", max_length=50)

    class Meta:
        verbose_name = "Contato"
        verbose_name_plural = "Contatos"

    def __str__(self):
        return self.endereco


class Localizacoes(models.Model):
    contato = models.OneToOneField(Contatos, on_delete=models.CASCADE)
    link = models.CharField("Localização", max_length=500)

    class Meta:
        verbose_name = "Localizacao"
        verbose_name_plural = "Localizacoes"

    def __str__(self):
        return self.link

