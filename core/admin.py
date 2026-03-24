from django.contrib import admin
from .models import CustomUsuario, BiotipoUsuario, Exercicio, Alimentacao, Visitantes, Servicos, Objetivos, TiposTreinos
from .models import RedesSociais, Aquecimentos, Contatos, Localizacoes


@admin.register(CustomUsuario)
class CustomUsuarioAdmin(admin.ModelAdmin):
    list_display = ("email", "password", "first_name", "last_name", "data_nascimento")


@admin.register(BiotipoUsuario)
class BiotipoUsuarioAdmin(admin.ModelAdmin):
    list_display = ("altura", "peso", "tipo_corporal", "situacao")


@admin.register(Exercicio)
class ExercicioAdmin(admin.ModelAdmin):
    list_display = ("nome", "objetivo", "repeticoes_ou_tempo", "pausa", "imc", "praticante", "imagem")


@admin.register(Alimentacao)
class AlimentacaoAdmin(admin.ModelAdmin):
    list_display = ("prato", "descricao", "calorias", "peso", "imc", "imagem")


@admin.register(Visitantes)
class VisitantesAdmin(admin.ModelAdmin):
    list_display = ("titulo", "descricao", "imagem")


@admin.register(Servicos)
class ServicosAdmin(admin.ModelAdmin):
    list_display = ("titulo", "descricao", "imagem")


@admin.register(Objetivos)
class ObjetivosAdmin(admin.ModelAdmin):
    list_display = ("titulo", "descricao", "imagem")


@admin.register(TiposTreinos)
class TiposTreinosAdmin(admin.ModelAdmin):
    list_display = ("treino", "repeticoes_ou_tempo_min", "repeticoes_ou_tempo_max")


@admin.register(RedesSociais)
class RedesSociaisAdmin(admin.ModelAdmin):
    list_display = ("rede_social", "icone")


@admin.register(Aquecimentos)
class AquecimentosAdmin(admin.ModelAdmin):
    list_display = ("nome", "link")


@admin.register(Contatos)
class ContatosAdmin(admin.ModelAdmin):
    list_display = ("endereco", "telefone", "email")


@admin.register(Localizacoes)
class LocalizacoesAdmin(admin.ModelAdmin):
    list_display = ("link",)

