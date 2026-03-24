from django import forms
from django.core.mail.message import EmailMessage


class ContatoForm(forms.Form):
    nome = forms.CharField(max_length=20, label="Nome")
    email = forms.EmailField(label="E-mail")
    assunto = forms.CharField(max_length=100, label="Assunto")
    mensagem = forms.CharField(widget=forms.Textarea, label="Mensagem")

    def send_email(self):
        nome = self.cleaned_data["nome"]
        email = self.cleaned_data["email"]
        assunto = self.cleaned_data["assunto"]
        mensagem = self.cleaned_data["mensagem"]

        conteudo = f"Nome: {nome}\nE-mail: {email}\nAssunto: {assunto}\nMensagem: {mensagem}"

        mail = EmailMessage(
            subject="Email enviado pelo sistema django2",
            body=conteudo,
            from_email="trainer@djangopersonal.com",
            to=["trainer@djangopersonal.com", ],
            headers={"Reply-to": email}
        )
        return mail.send()

