import random
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import PhoneNumber
from django.contrib.auth.models import User
from django.contrib.auth import login

@csrf_exempt
def send_verification_code(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        
        # Generate a random verification code
        code = str(random.randint(100000, 999999))

        # Check if the user already exists
        user, created = User.objects.get_or_create(username=phone_number)

        # Store the phone number and verification code
        phone_entry, _ = PhoneNumber.objects.get_or_create(user=user)
        phone_entry.phone_number = phone_number
        phone_entry.verification_code = code
        phone_entry.save()

        # Simulate sending the code (replace with actual SMS logic if needed)
        print(f"Verification code for {phone_number}: {code}")

        return JsonResponse({'message': 'Verification code sent.'})

    return JsonResponse({'error': 'Invalid request.'}, status=400)

@csrf_exempt
def verify_code(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        code = request.POST.get('code')

        try:
            phone_entry = PhoneNumber.objects.get(phone_number=phone_number)

            if phone_entry.verification_code == code:
                phone_entry.is_verified = True
                phone_entry.save()
                login(request, phone_entry.user)  # Log the user in if needed
                return JsonResponse({'message': 'Phone number verified successfully.'})
            else:
                return JsonResponse({'error': 'Invalid verification code.'}, status=400)
        except PhoneNumber.DoesNotExist:
            return JsonResponse({'error': 'Phone number not found.'}, status=404)

    return JsonResponse({'error': 'Invalid request.'}, status=400)
