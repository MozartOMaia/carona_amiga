from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views import View, generic
from carpool.business import SearchCaronaBusiness
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from carpool.utils.date import getDayOfWeekStr

from .models import Usuario, Endereco, Carona, MensagemUsuarios
from carpool.business import AddMemberBusiness, SearchCaronaBusiness


class IndexView(View):
    @login_required
    def template(request, **kwargs):
        # Somente caronas com vagas
        caronas = Carona.objects.filter(vagas__gte=1).order_by('-criado_em')

        # Somente motorista que tem caronas com vagas
        motoristas = Usuario.objects.filter(
            temCarro=True).filter(motorista__vagas__gte=1).distinct().order_by('-criado_em')

        # Limitar a quantidade 4
        caronas = caronas[:4]
        motoristas = motoristas[:4]

        usuarioLogado = request.user.perfil

        return render(request, 'carpool/index.html', {
            'caronas': caronas,
            'motoristas': motoristas,
            'usuarioLogado': usuarioLogado
        })


class SearchView(View):
    @login_required
    def pesquisa(request):
        if request.method == 'GET':
            return render(request, 'carpool/results.html')

        try:
            origem = request.POST['origem']
            destino = request.POST['destino']
            data = request.POST['data']
            horario = request.POST['horario']

            caronas = SearchCaronaBusiness.execute(
                origem=origem, destino=destino, data=data, horario=horario)

            if not origem and not destino and not data and not horario:
                error = 'A pesquisa não foi realizada. Preencha pelo menos um dos campos de pesquisa.'

                return render(request, 'carpool/results.html', {
                    'error': error,
                    'pages': range(1, 2)
                })

        except Carona.DoesNotExist:
            caronas = None

        usuarioLogado = request.user.perfil
        length = len(caronas)
        # pages = 1 if length // 5 == 0 else length // 5

        return render(request, 'carpool/results.html', {
            'caronas': caronas,
            'usuarioLogado': usuarioLogado,
            'length': length,
            'body': request.POST
        })


class ListMessagesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        activeChat = kwargs['active']
        usuarioLogado = request.user.perfil
        destinatarios = Usuario.objects.filter(
            msgdestinatario__remetente__id=usuarioLogado.id).distinct()
        remetentes = Usuario.objects.filter(
            msgremetente__destinatario_id=usuarioLogado.id).distinct()
        usuarios = destinatarios | remetentes
        usuarios = usuarios.distinct()

        mensagensComoDestinatario = MensagemUsuarios.objects.filter(
            destinatario__id=usuarioLogado.id)
        mensagensComoRemetente = MensagemUsuarios.objects.filter(
            remetente__id=usuarioLogado.id)
        mensagens = mensagensComoDestinatario | mensagensComoRemetente
        mensagens = mensagens.order_by('-diaHora')

        activeChatUser = get_object_or_404(Usuario, pk=activeChat)
        mensagensActiveDest = MensagemUsuarios.objects.filter(
            destinatario=usuarioLogado).filter(remetente=activeChatUser)
        mensagensActiveRem = MensagemUsuarios.objects.filter(
            destinatario=activeChatUser).filter(remetente=usuarioLogado)
        mensagensActive = mensagensActiveDest | mensagensActiveRem
        mensagensActive = mensagensActive.order_by('diaHora')

        for usuario in usuarios:
            usuario.mensagemRecente = usuario.ultimaMensagem(
                request.user.perfil)

        contexto = {
            'usuarios': usuarios,
            'mensagens': mensagens,
            'usuarioLogado': usuarioLogado,
            'activeChatUser': activeChatUser,
            'mensagensActive': mensagensActive
        }

        return render(request, 'carpool/list_messages.html', contexto)


class ListGroupsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        usuarioLogado = request.user.perfil
        caronasPassageiro = Carona.objects.filter(
            passageiros__id=usuarioLogado.id)
        caronasMotorista = Carona.objects.filter(
            motorista__id=usuarioLogado.id
        )

        caronas = caronasPassageiro | caronasMotorista
        return render(request, 'carpool/list_carona.html', {
            'caronas': caronas
        })


class UserMessageView(LoginRequiredMixin, View):
    def get(self, request):
        usuarioLogado = request.user.perfil
        destinatarios = Usuario.objects.filter(
            msgdestinatario__remetente__id=usuarioLogado.id).distinct()
        remetentes = Usuario.objects.filter(
            msgremetente__destinatario_id=usuarioLogado.id).distinct()
        usuarios = destinatarios | remetentes
        usuarios = usuarios.distinct()

        for usuario in usuarios:
            usuario.mensagemRecente = usuario.ultimaMensagem(
                request.user.perfil)

        return render(request, 'carpool/list_messages.html', {
            'usuarios': usuarios
        })

    def post(self, request, *args, **kwargs):
        id_carona = request.POST['caronaid']
        id_usuarioChat = request.POST['usuarioChat']
        carona = get_object_or_404(Carona, pk=id_carona)
        usuarioLogado = request.user.perfil
        mensagem = request.POST['msg']
        if id_usuarioChat:
            usuarioChat = get_object_or_404(Usuario, pk=id_usuarioChat)
        else:
            usuarioChat = carona.motorista

        mensagemUsuario = MensagemUsuarios(conteudo=mensagem, diaHora=timezone.now(
        ), destinatario=usuarioChat, remetente=usuarioLogado, carona=carona)
        mensagemUsuario.save()

        return redirect('userMessage')


class create_caronaView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        usuarioLogado = request.user.perfil
        contexto = {
            'usuarioLogado': usuarioLogado
        }
        return render(request, 'carpool/create_carona.html', contexto)

    def post(self, request, *args, **kwargs):
        nome = request.POST['name']
        seg = request.POST['monday']
        ter = request.POST['tuesday']
        qua = request.POST['wednesday']
        qui = request.POST['thursday']
        sex = request.POST['friday']
        sab = request.POST['saturday']
        dom = request.POST['sunday']
        horario = request.POST['time']
        cidadeSaida = request.POST['pickup-from-city']
        estadoSaida = request.POST['pickup-from-state']
        ruaSaida = request.POST['pickup-from-street']
        numeroSaida = request.POST['pickup-from-number']
        bairroSaida = request.POST['pickup-from-district']
        cidadeDestino = request.POST['destination-city']
        estadoDestino = request.POST['destination-state']
        ruaDestino = request.POST['destination-street']
        numeroDestino = request.POST['destination-number']
        bairroDestino = request.POST['destination-district']
        descricao = request.POST['description']
        vagas = request.POST['vagas']

        enderecoSaida = Endereco(cidade=cidadeSaida, estado=estadoSaida,
                                 rua=ruaSaida, numero=numeroSaida, bairro=bairroSaida)
        enderecoDestino = Endereco(cidade=cidadeDestino, estado=estadoDestino,
                                   rua=ruaDestino, numero=numeroDestino, bairro=bairroDestino)

        dias = int(seg)+int(ter)+int(qua)+int(qui)+int(sex)+int(sab)+int(dom)

        user = request.user

        motorista = user.perfil

        if descricao:
            carona = Carona(nome=nome, vagas=vagas, horario=horario, descricao=descricao, dias=dias,
                            enderecoSaida=enderecoSaida, enderecoDestino=enderecoDestino, motorista=motorista)
        else:
            carona = Carona(nome=nome, vagas=vagas, horario=horario, dias=dias, enderecoSaida=enderecoSaida,
                            enderecoDestino=enderecoDestino, motorista=motorista)

        enderecoSaida.save()
        enderecoDestino.save()
        carona.save()

        motorista.temCarro = True

        motorista.save()

        return redirect('listGroups')


class edit_caronaView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        id_carona = kwargs['pk']
        carona = get_object_or_404(Carona, pk=id_carona)
        days = carona.dias
        days = list(str(bin(days)))
        del days[0]
        del days[0]
        while (len(days) != 7):
            days.insert(0, '0')
        contexto = {
            'carona': carona,
            'days': days,
        }
        return render(request, 'carpool/edit_carona.html', contexto)

    def post(self, request, *args, **kwargs):
        id_carona = kwargs['pk']
        carona = get_object_or_404(Carona, pk=id_carona)
        carona.nome = request.POST['name']
        seg = request.POST['monday']
        ter = request.POST['tuesday']
        qua = request.POST['wednesday']
        qui = request.POST['thursday']
        sex = request.POST['friday']
        sab = request.POST['saturday']
        dom = request.POST['sunday']
        carona.horario = request.POST['time']
        carona.enderecoSaida.cidade = request.POST['pickup-from-city']
        carona.enderecoSaida.estado = request.POST['pickup-from-state']
        carona.enderecoSaida.rua = request.POST['pickup-from-street']
        carona.enderecoSaida.numero = request.POST['pickup-from-number']
        carona.enderecoSaida.bairro = request.POST['pickup-from-district']
        carona.enderecoDestino.cidade = request.POST['destination-city']
        carona.enderecoDestino.estado = request.POST['destination-state']
        carona.enderecoDestino.rua = request.POST['destination-street']
        carona.enderecoDestino.numero = request.POST['destination-number']
        carona.enderecoDestino.bairro = request.POST['destination-district']
        carona.descricao = request.POST['description']

        carona.dias = int(seg)+int(ter)+int(qua)+int(qui) + \
            int(sex)+int(sab)+int(dom)

        carona.enderecoSaida.save()
        carona.enderecoDestino.save()
        carona.save()

        return redirect('listGroups')


class AddMember(View):
    @login_required
    @require_http_methods(['GET'])
    def template(request, **kwargs):
        # Pegar id da carona
        id = kwargs['id']
        # Pegar a corona com o id
        carona = Carona.objects.get(id=id)
        # Pegar os usuarios (aqueles que enviaram mensagem e não são passageiros dessa carona)
        mensagens = MensagemUsuarios.objects.filter(carona=carona)

        usuarios_adicionados = carona.passageiros.all()

        usuarios = AddMemberBusiness.execute(usuarios_adicionados, mensagens)

        # Passar os passageiros para o template

        return render(request, 'carpool/add_member.html', {
            'usuarios': usuarios,
            'carona': carona
        })

    @login_required
    @require_http_methods(['POST'])
    def add(request):
        carona_id = request.POST['carona_id']

        carona = Carona.objects.get(pk=carona_id)

        for field in request.POST:
            if request.POST[field] == 'on':
                usuario = Usuario.objects.get(nomeUsuario=field)
                carona.passageiros.add(usuario)
                carona.vagas = carona.vagas - 1
        carona.save()

        return redirect('add_member_template', id=carona_id)


class DetalharCarona(View):
    @login_required
    def template(request, *args, **kwargs):
        carona_id = kwargs['pk']

        carona = Carona.objects.get(pk=carona_id)

        usuarioLogado = request.user.perfil

        vagas_total = carona.passageiros.count() + carona.vagas

        diaStr = getDayOfWeekStr(carona.dias)

        return render(request, 'carpool/detail_carona.html', {
            'carona': carona,
            'vagas_total': vagas_total,
            'dias': diaStr,
            'usuarioLogado': usuarioLogado
        })


class ListarCaronaView(View):
    @login_required
    def template(request):
        caronas = Carona.objects.all()

        return render(request, 'carpool/list_carona.html', {
            'caronas': caronas
        })


class UserView(View):
    def template(request):
        return render(request, 'carpool/create_account.html')

    def create(request):
        name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(username, email, password)

        perfil = Usuario(nome=name, cpf="0", cnh="0", telefone="0", email=email,
                         nomeUsuario=username, temCarro=False, avaliacao=5.0, conta=user)

        perfil.save()

        return redirect('index')


class LoginUserView(View):
    def template(request):
        return render(request, 'carpool/login.html')

    def login(request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)

            return redirect('index')

        return redirect('login_template')

    def logout(request):
        logout(request)

        return redirect('login_template')
