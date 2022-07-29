from django.contrib import admin
from .models import Usuario, Endereco, Carona, MensagemUsuarios, MensagemCarona

admin.site.register(Usuario)
admin.site.register(Endereco)
admin.site.register(Carona)
admin.site.register(MensagemUsuarios)
admin.site.register(MensagemCarona)
