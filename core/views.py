from core.models import CustomUsuario, BiotipoUsuario, Exercicio, Visitantes, Servicos, Objetivos, TiposTreinos
from core.models import RedesSociais, Aquecimentos, Contatos, Localizacoes, Alimentacao
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from .forms import ContatoForm


def login_view(request):
    # Verifica se a requisição no template é do tipo post, caso seja, pegará os dados e os submeterá.
    if request.method == "POST":
        # Pegará os dados de e-mail
        email = request.POST.get("username")
        password = request.POST.get("password")

        # Com os dados em ambas variáveis, fornecerá o que foi pego de cada campo e passará para o método autenticar.
        usuario = authenticate(request, username=email, password=password)

        # se houver dados fornecidos para os parâmetros da função de autenticação, logará no sistema e redirecionará o
        # usuário à página inicial.
        if usuario is not None:
            login(request, usuario)
            messages.success(request, "Login feito com sucesso!", extra_tags="login_view")
            return redirect("index")
        # Em caso de erro, enviará uma mensagem no template do problema ocorrido.
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    return render(request, "registration/login.html")


def cadastro_view(request):
    """
    :method post: posta os dados que o usuários fornecer no formulário e os armazena em cada atributos do model
    CustomUsuario para persisti-lo no banco de dados.
    :method .save(): salva os dados, persistindo-os no model CustomUsuario.
    :param render: Carrega o template para exibi-lo quando o usuário fizer acesso.
    :param request: requisição que aponta e renderiza dados oriundos do template.
    :return:
    """
    # Verifica se a requisição no template é do tipo post, caso seja, pegará os dados e os submeterá.
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST.get("password")
        data_nascimento = request.POST.get("data_nascimento")

        # Checa se cada dado fornecido está realmente dentro de cada variável que aponta para o modelo.
        if first_name and last_name and email and password and data_nascimento:
            # Irá tentar persistir os dados.
            try:
                usuario = CustomUsuario.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    data_nascimento=data_nascimento
                )

                usuario.save()

                # Autenticando usuário para já entrar logado no sistema.
                usuario_autenticado = authenticate(request, email=email, password=password)
                if usuario_autenticado is not None:
                    login(request, usuario_autenticado)
                    messages.success(request, "Conta criada com sucesso. Seja bem-vindo!", extra_tags="cadastro_view")
                    return redirect("index")

            # Caso não dê certo, o sistema apontará erro de Integridade nos dados e carregará novamente o template.
            except IntegrityError:
                messages.error(request, "Algo está dando erro. Tente novamente!")
                return render(request, "cadastro.html")
        # Em caso de campos não preenchidos, pedirá que verifique e forneça os dados aos campos faltantes.
        else:
            messages.error(request, "Por favor, preencha os campos faltantes!")
    return render(request, "cadastro.html")


def index(request):
    servicos = Servicos.objects.all()
    tipos_de_treinos = TiposTreinos.objects.all()
    redes_sociais = RedesSociais.objects.all()
    objetivos = Objetivos.objects.all()
    aquecimentos = Aquecimentos.objects.all()

    # Checa se o usuário não está autenticado.
    if not request.user.is_authenticated:
        # Fornece dados para usuários visitantes
        visitantes = Visitantes.objects.all()
        context = {
            "visitantes": visitantes,
            "servicos": servicos,
            "tipos_de_treinos": tipos_de_treinos,
            "redes_sociais": redes_sociais,
            "objetivos": objetivos,
            "aquecimentos": aquecimentos
        }
    # Se autenticado, exibirá os dados cadastrados do usuário autenticado.
    else:
        usuario_imc = 0
        valor = 0
        dados_cadastrados = False
        dados_cadastrados_biotipo = False
        tipo_corporal = ""
        usuarios = CustomUsuario.objects.all()
        biotipos_usuarios = BiotipoUsuario.objects.all().filter(usuario=request.user)[:4]

        for biotipo_usuario in biotipos_usuarios:
            usuario_imc = biotipo_usuario.peso/(biotipo_usuario.altura * biotipo_usuario.altura)

        for usuario in usuarios:
            dados_cadastrados = str(request.user) == str(usuario.get_full_name())

            if dados_cadastrados:
                break

        for biotipo in biotipos_usuarios:
            dados_cadastrados_biotipo = str(request.user) == str(biotipo.usuario)
            if dados_cadastrados_biotipo:
                tipo_corporal = biotipo.situacao
                break

        # Aplicando filtro e Limitando quantidade de dados até 4 que sejam somente iguais aos do usuário
        exercicios = Exercicio.objects.all().filter(imc__lte=usuario_imc, praticante=tipo_corporal)[:4]

        # Uma forma de validação, caso usuário tenha cadastrado os seus dados físicos, ele obterá um imc e só será
        # mostrado o plano de dieta quando o imc dele for obtido.
        if usuario_imc > 0:
            alimentacao = Alimentacao.objects.all().filter(imc__gte=usuario_imc)[:4]
        else:
            alimentacao = ""

        context = {
            "exercicios": exercicios,
            "usuario_imc": usuario_imc,
            "valor": valor,
            "dados_cadastrados": dados_cadastrados,
            "tipo_corporal": tipo_corporal,
            "servicos": servicos,
            "objetivos": objetivos,
            "tipos_de_treinos": tipos_de_treinos,
            "dados_cadastrados_biotipo": dados_cadastrados_biotipo,
            "redes_sociais": redes_sociais,
            "aquecimentos": aquecimentos,
            "alimentacao": alimentacao
        }

    return render(request, "index.html", context)


def imc(request):
    """
    A lógica aqui é semelhante a view index, porém aqui, serão registrados dados separados do usuário e fornecidos
    para entidade BiotipoUsuario que irá linkar aos dados que o usuário já possuí. Entretanto, nesta view, serão
    fornecidos os dados de: altura, peso, tipo_corporal e situacao ao modelo em questão, para que seja possível
    postar, gravando os dados no banco de dados.
    """
    if request.method == "POST":
        altura = request.POST.get("altura")
        peso = request.POST.get("peso")
        tipo_corporal = request.POST.get("tipo_corporal")
        situacao = request.POST.get("situacao")

        if altura and peso and tipo_corporal and situacao:
            # Cria ou atualiza os dados de BiotipoUsuario ligado ao usuário logado
            biotipo, created = BiotipoUsuario.objects.update_or_create(
                usuario=request.user,
                defaults={
                    'altura': altura,
                    'peso': peso,
                    'tipo_corporal': tipo_corporal,
                    'situacao': situacao,
                }
            )
            messages.success(request, "Dados físicos cadastrados com sucesso!", extra_tags="imc")
            return redirect("index")
        else:
            messages.error(request, "Todos os campos são obrigatórios!")

    context = {
        'TIPO_CORPO': BiotipoUsuario.TIPO_CORPO,
        'SITUACAO': BiotipoUsuario.SITUACAO,
    }
    return render(request, "imc.html", context)


def contato(request):
    contatos = Contatos.objects.all()
    localizacoes = Localizacoes.objects.all()
    redes_sociais = RedesSociais.objects.all()

    if str(request.method) == "POST":
        formulario = ContatoForm(request.POST or None)
        if formulario.is_valid():
            formulario.send_email()
            messages.success(request, "E-mail enviado com sucesso!", extra_tags="contato")
            return redirect("contato")
        else:
            messages.error(request, "Erro ao enviar o e-mail", extra_tags="contato")
    else:
        formulario = ContatoForm()

    context = {
        "contatos": contatos,
        "localizacoes": localizacoes,
        "redes_sociais": redes_sociais,
        "formulario": formulario
    }
    return render(request, "contato.html", context)


def cadastro(request):
    return render(request, "cadastro.html")


def error404(request, exception):
    template = loader.get_template("404.html")
    return HttpResponse(content=template.render(), content_type='text/html; charset=utf-8', status=404)


"""def error500(request, exception):
    template = loader.get_template("500.html")
    return HttpResponse(content=template.render(), content_type='text/html; charset=utf-8', status=500)
"""