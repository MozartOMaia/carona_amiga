from carpool.utils.bits import bitsToInteger
from datetime import date


def numberToDayOfWeekBits(number):
    if number == 0:
        return {
            'Segunda': 1,
            'Terça': 0,
            'Quarta': 0,
            'Quinta': 0,
            'Sexta': 0,
            'Sábado': 0,
            'Domingo': 0
        }
    elif number == 1:
        return {
            'Segunda': 0,
            'Terça': 1,
            'Quarta': 0,
            'Quinta': 0,
            'Sexta': 0,
            'Sábado': 0,
            'Domingo': 0
        }
    elif number == 2:
        return {
            'Segunda': 0,
            'Terça': 0,
            'Quarta': 1,
            'Quinta': 0,
            'Sexta': 0,
            'Sábado': 0,
            'Domingo': 0
        }
    elif number == 3:
        return {
            'Segunda': 0,
            'Terça': 0,
            'Quarta': 0,
            'Quinta': 1,
            'Sexta': 0,
            'Sábado': 0,
            'Domingo': 0
        }
    elif number == 4:
        return {
            'Segunda': 0,
            'Terça': 0,
            'Quarta': 0,
            'Quinta': 0,
            'Sexta': 1,
            'Sábado': 0,
            'Domingo': 0
        }
    elif number == 5:
        return {
            'Segunda': 0,
            'Terça': 0,
            'Quarta': 0,
            'Quinta': 0,
            'Sexta': 0,
            'Sábado': 1,
            'Domingo': 0
        }
    elif number == 6:
        return {
            'Segunda': 0,
            'Terça': 0,
            'Quarta': 0,
            'Quinta': 0,
            'Sexta': 0,
            'Sábado': 0,
            'Domingo': 1
        }


def getDayOfWeekStr(number: int):
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


def dateToDayOfWeekInInt(data: str):
    data = data.split('-')

    data = date(year=int(data[0]), month=int(
        data[1]), day=int(data[2]))
    bitsDict = numberToDayOfWeekBits(data.weekday())
    weekdayBits = bitsToInteger(bitsDict)

    return weekdayBits
