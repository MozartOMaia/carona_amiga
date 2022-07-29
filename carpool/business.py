from carpool.utils.date import getDayOfWeekStr, dateToDayOfWeekInInt
from .models import Carona


class SearchCaronaBusiness:
    def execute(origem: str, destino, data, horario):
        weekdayBits = 0

        # if horario is something valid, then split it -- Get hour
        if horario != '':
            horario = horario.split(':')[0]

        # if data is something valid, then do the logic -- Get data to something valid
        # data para int
        if data != '':
            weekdayBits = dateToDayOfWeekInInt(data)

        # if origem != '' or destino != '' or horario != '':
        caronas = Carona.objects.filter(enderecoSaida__bairro__contains=origem).filter(
            enderecoDestino__bairro__contains=destino)

        if horario != '':
            caronas = caronas.filter(horario__hour=horario or None)

        if data != '' and caronas.count() == 0:
            caronas = Carona.objects.all()

        if data != '':
            # filter by day of week
            caronas = filter(lambda carona: carona.dias
                             & weekdayBits, caronas)

        # make a list of it
        caronas = list(caronas)

        for carona in caronas:
            carona.diaStr = getDayOfWeekStr(carona.dias)

        return caronas


class AddMemberBusiness:
    def execute(usuarios_adicionados, mensagens):
        usuarios = []

        for mensagem in mensagens:
            remetente = mensagem.remetente

            if (remetente not in usuarios_adicionados and remetente not in usuarios):
                usuarios.append(remetente)

        return usuarios
