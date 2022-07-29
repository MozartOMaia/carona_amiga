from django.db import models
from django.contrib.auth.models import User


class Usuario(models.Model):
    nome = models.CharField(max_length=50)
    cpf = models.CharField(max_length=11)
    avatar = models.CharField(
        max_length=100, default='/carpool/assets/profiles/avatar.svg')
    cnh = models.CharField(max_length=11)
    telefone = models.CharField(max_length=11)
    temCarro = models.BooleanField()
    email = models.CharField(max_length=50)
    nomeUsuario = models.CharField(max_length=50)
    bio = models.CharField(max_length=400)
    avaliacao = models.FloatField(default=5.0)
    criado_em = models.DateTimeField(auto_now_add=True)
    conta = models.OneToOneField(
        User, on_delete=models.DO_NOTHING, related_name='perfil')

    def caronasRecentes(self):
        caronas = Carona.objects.filter(
            motorista=self).order_by('-criado_em')

        caronas = caronas[:4]

        return caronas

    def ultimaMensagem(self, usuario):
        mensagensUsuarioRem = MensagemUsuarios.objects.filter(
            remetente=self).filter(destinatario=usuario)
        mensagensUsuarioDest = MensagemUsuarios.objects.filter(
            remetente=usuario).filter(destinatario=self)
        mensagensUsuario = mensagensUsuarioRem | mensagensUsuarioDest
        mensagensUsuario = mensagensUsuario.order_by('-diaHora')
        return mensagensUsuario.first

    def __str__(self):
        return self.nomeUsuario


class Endereco(models.Model):
    cidade = models.CharField(max_length=30)
    estado = models.CharField(max_length=2)
    rua = models.CharField(max_length=100)
    numero = models.IntegerField()
    bairro = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.rua} nº{self.numero}, {self.bairro}, {self.cidade} - {self.estado}"


class Carona(models.Model):
    nome = models.CharField(max_length=50)
    horario = models.TimeField()
    descricao = models.CharField(max_length=400)
    dias = models.IntegerField()
    vagas = models.IntegerField()
    passageiros = models.ManyToManyField(
        Usuario, related_name='passageiro', blank=True)
    motorista = models.ForeignKey(
        Usuario, on_delete=models.DO_NOTHING, related_name='motorista')
    enderecoSaida = models.ForeignKey(
        Endereco, on_delete=models.CASCADE, related_name='enderecoSaida')
    enderecoDestino = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)

    def diasStr(self):
        number = self.dias
        bits = [
            {'dia': 'Segunda', 'inteiro': 1},
            {'dia': 'Terça', 'inteiro': 2},
            {'dia': 'Quarta', 'inteiro': 4},
            {'dia': 'Quinta', 'inteiro': 8},
            {'dia': 'Sexta', 'inteiro': 16},
            {'dia': 'Sábado', 'inteiro': 32},
            {'dia': 'Domingo', 'inteiro': 64},
        ]

        daysOfWeek = list()
        daysStr = ''

        for bit in bits:
            result = number & bit['inteiro']

            if result > 0:
                daysOfWeek.append(bit['dia'])

        for i in range(len(daysOfWeek)):
            daysStr += daysOfWeek[i]

            if (i < len(daysOfWeek) - 2):
                daysStr += ", "
            elif (i < len(daysOfWeek) - 1):
                daysStr += " e "

        return daysStr

    def __str__(self):
        return self.nome


class MensagemUsuarios(models.Model):
    conteudo = models.TextField()
    diaHora = models.DateTimeField()
    destinatario = models.ForeignKey(
        Usuario, on_delete=models.DO_NOTHING, related_name='msgdestinatario')
    remetente = models.ForeignKey(
        Usuario, on_delete=models.DO_NOTHING, related_name='msgremetente')
    carona = models.ForeignKey(Carona, on_delete=models.CASCADE)

    def __str__(self):
        return self.conteudo


class MensagemCarona(models.Model):
    conteudo = models.TextField()
    diaHora = models.DateTimeField()
    carona = models.ForeignKey(Carona, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.conteudo
