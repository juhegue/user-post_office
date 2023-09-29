# Fork de Django Post Office

Para poder enviar emails según la configuración del usuario


```python
from post_office import mail

mail.send(
    'recipient@example.com',
    'from@example.com',
    subject='My email',
    message='Hi there!',
    html_message='Hi <strong>there</strong>!',
    user_id=request.user.id  # el usario actual 
)
```

Es necesario sobreescribir el backend:

```python
# -*- coding: utf-8 -*-

import logging
from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings
from api.views.util.utiles import desencripta
from web.models import User

logger = logging.getLogger(__name__)


class UserEmailBackend(EmailBackend):
    def __init__(self,
                 host=None,
                 port=None,
                 username=None,
                 password=None,
                 use_tls=None,
                 fail_silently=None,
                 use_ssl=None,
                 timeout=None,
                 ssl_keyfile=None,
                 ssl_certfile=None,
                 **kwargs):

        user_id = kwargs.pop('user_id', 0)
        query = User.objects.filter(id=user_id).first()
        if query and query.host:
            host = query.host
            port = query.port
            username = query.user_email
            password = desencripta(query.pass_email)
            use_tls = query.use_tls
            use_ssl = query.use_ssl
            timeout = query.timeout or timeout
            logger.info(f'{query}={host}:{port}:{username}:{use_tls}:{use_ssl}')
        else:
            host = settings.EMAIL_HOST
            port = settings.EMAIL_PORT
            username = settings.EMAIL_HOST_USER
            password = settings.EMAIL_HOST_PASSWORD
            use_tls = settings.EMAIL_USE_TLS
            use_ssl = settings.EMAIL_USE_SSL
            logger.info(f'Defecto: {host}:{port}:{username}:{use_tls}:{use_ssl}')

        super().__init__(
            host=host,
            port=port,
            username=username,
            password=password,
            use_tls=use_tls,
            fail_silently=fail_silently,
            use_ssl=use_ssl,
            timeout=timeout,
            ssl_keyfile=ssl_keyfile,
            ssl_certfile=ssl_certfile,
            **kwargs)
```

### NOTAS

Para que esto funcione se debe añadir en el settings.py

```python
EMAIL_BACKEND = "miapp.backends.UserEmailBackend"
```

Y haber añadido al model User los campos:
```
...
    host = models.CharField(blank=True, null=True, max_length=256, verbose_name=_('Servidor'))
    port = models.SmallIntegerField(blank=True, null=True, verbose_name=_('Puerto'))
    from_email = models.CharField(blank=True, null=True,max_length=256, verbose_name=_('De Email (from email)'))
    user_email = models.CharField(blank=True, null=True,max_length=256, verbose_name=_('Usuario Autenticación'))
    pass_email = models.CharField(blank=True, null=True,max_length=256, verbose_name=_('Clave Autenticación'))
    use_tls = models.BooleanField(default=False, verbose_name=_('Usar TLS'))
    use_ssl = models.BooleanField(default=False, verbose_name=_('Usar SSL'))
    timeout = models.SmallIntegerField(blank=True, null=True,verbose_name=_('Timeout Envio (segundos)'))
    empresa = models.CharField(blank=True, null=True, max_length=256, verbose_name=_('Empresa'))
...
```
