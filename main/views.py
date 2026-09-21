from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Notice, FounderInfo, UserProfile

def home(request):
    notices = Notice.objects.all().order_by('-uploaded_at')
    founders = FounderInfo.objects.all()
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        passport = request.FILES.get('passport_photo')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username hii tayari ipo, tumia nyingine!")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            UserProfile.objects.create(user=user, phone_number=phone, passport_photo=passport)
            messages.success(request, "Akaunti yako imetengenezwa vizuri!")
            return redirect('home')

    context = {'notices': notices, 'founders': founders}
    return render(request, 'home.html', context)
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Notice, FounderInfo, UserProfile

# Ukurasa wa nyumbani (Utafunguka kwa walioingia tu)
@login_required(login_url='login')
def home(request):
    notices = Notice.objects.all().order_by('-uploaded_at')
    founders = FounderInfo.objects.all()
    user_profile = UserProfile.objects.filter(user=request.user).first()
    
    context = {
        'notices': notices, 
        'founders': founders,
        'user_profile': user_profile
    }
    return render(request, 'home.html', context)

# Ukurasa wa Kuingia (Login) & Usajili
def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        # Kama mtumiaji anajisajili
        if 'register' in request.POST:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            phone = request.POST.get('phone')
            passport = request.FILES.get('passport_photo')
            
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username hii tayari ipo!")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                UserProfile.objects.create(user=user, phone_number=phone, passport_photo=passport)
                messages.success(request, "Akaunti imetengenezwa! Sasa ingia kwa nenosiri lako.")
                return redirect('login')

        # Kama mtumiaji anaingia (Login)
        elif 'login' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Username au Nenosiri sio sahihi!")

    return render(request, 'login.html')

# Kutoka kwenye Mfumo
def logout_user(request):
    logout(request)
    return redirect('login')
from google import genai
from django.http import JsonResponse
import os

# Weka API Key yako hapa au kwenye envirAQ.Ab8RN6Lmq_jrfbNRbciVGlNywcX6o9LnyjNl_CJE9xPtsi9Oqgonment variable
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
@login_required(login_url='login')
def ai_tutor(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        
        if not user_message:
            return JsonResponse({'error': 'Tafadhali andika swali.'})
            
        try:
            client = genai.Client(api_key=GEMINI_API_KEY)
            
            prompt = f"""
            Wewe ni Sir Nyuki, mwalimu/tutor rasmi kwenye mfumo huu wa masomo. 
            Mwanzilishi na mmiliki wa tovuti hii ni Hussein Juma. Ukiulizwa kuhusu aliyekutengeneza au mmiliki wa tovuti, mtaje Hussein Juma.

            Msaidie mwanafunzi anayeuliza swali lifuatalo. 
            
            Mambo ya kuzingatia kwenye mpangilio wa jibu lako:
            1. Anza kujibu kwa **Kiswahili** fasaha na rahisi kueleweka.
            2. Ruka mistari miwili.
            3. Weka sehemu ya Kiingereza ikiwa ndani ya tag ya HTML ya rangi ya bluu hivi:
               <br><br>
               <div style="color: #0d6efd; margin-top: 15px; border-top: 1px dashed #ccc; padding-top: 10px;">
               <strong>English Version:</strong><br>
               [Tafsiri ya Kiingereza hapa]
               </div>

            Swali la mwanafunzi: {user_message}
            """
            
            # Tumia model iliyothibitishwa kufanya kazi vizuri
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=prompt,
            )
            
            return JsonResponse({'reply': response.text})
            
        except Exception as e:
            return JsonResponse({'error': 'Server za AI zipo busy kwa sekunde chache. Bonyeza "Uliza" tena kupata jibu.'})

    return JsonResponse({'error': 'Invalid request'})
@login_required(login_url='login')
def jet_game(request):
    return render(request, 'game.html')