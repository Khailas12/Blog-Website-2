from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from .tokens import account_activaton_token
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string


def signup(request, *args, **kwargs):
    if request.method == 'POST':
        form = SignUpForm(request.POST or None)
        
        if form.is_valid():
            user = form.save()
            
            # Retreives the profile instance created by signal by hard refresh from db and calling this fixes the synchronism issue.
            user.refresh_from_db()  
            
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            
            user.profile.email = form.cleaned_data.get('email')
            user.profile.birthday = form.cleaned_data.get('birthday')
            
            user.is_active = False  # false lets the user unable to login until they confirm registration
            user.save()     # saves the user model after refresh which also triggers to save the profile too.
            
            current_site = get_current_site(request)     # this solves the task of hard coding site ID's incase it gets changed, 

            subject = 'Please Activate your account'
            message = render_to_string(
                'user_auth/activation_request.html',
                {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(
                        force_bytes(user.pk)
                        ),
                    'token': account_activaton_token.make_token(user),
            })

            user.email_user(subject, message)
            return redirect('activation_sent')
        # this no longer authenticats the user until they confirm 

            # username = form.cleaned_data.get('username')
            # the_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, passsword=the_password)
            
            # login(request, user)
            # return redirect('/')
            
    else:
        form = SignUpForm()
    
        context = {'form': form}
        return render(request, 'user_auth/signup.html', context)
    
    
def activate(request, uidb64, token, *args, **kwargs):
    try: 
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        pass
        
