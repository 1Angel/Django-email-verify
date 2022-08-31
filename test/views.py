from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from typing import Protocol
from test.forms import RegisterForm
from django.shortcuts import redirect
from django.core.mail import EmailMessage

from test.models import Account
from test.token import account_activation_token


# Create your views here.
def HomeView(request):
    return render(request, 'Index.html')


def activate(request, uidb64, token):
    Account = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)

    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Gracias Por confirmar tu email')
        return redirect('home')

    else:
        messages.error(request, 'error al validar email')
    return redirect('home')


def activateEmail(request, user, to_email):
    mail_subject = 'Activa tu cuenta de usuario',
    message = render_to_string(
        'activate_account.html', {
            'user': user.username,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
            'protocol': 'https' if request.is_secure() else 'http'
        }
    )
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')

    else:
        messages.error(request, f'Problem sending email to {to_email}')


def RegisterView(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('home')

    return render(request, 'Register.html', context={
        'form': form
    })
