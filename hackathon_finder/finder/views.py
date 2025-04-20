from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from .forms import UserRegistrationForm, ProfileForm, MessageForm, ProfileSearchForm
from .models import Profile, Message, TechStack, User
from django.core.paginator import Paginator
from .models import Profile, Skill, TechStack, Hackathon  # Make sure to import all needed models
from django.utils import timezone


@login_required
def edit_profile(request):
    profile = request.user.profile
    logger.debug("Edit profile view accessed for user: %s", request.user)
    
    if request.method == 'POST':
        logger.debug("POST data: %s", request.POST)
        logger.debug("FILES data: %s", request.FILES)
        
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            try:
                # Save basic profile info
                profile = form.save(commit=False)
                
                # Handle profile picture
                if 'profile_picture' in request.FILES:
                    profile.profile_picture = request.FILES['profile_picture']
                profile.save()
                
                # Save many-to-many relationships
                form.save_m2m()
                
                # Process skills from the multi-select
                skill_ids = request.POST.getlist('skills', [])
                profile.skills.clear()
                if skill_ids:
                    profile.skills.add(*skill_ids)
                
                # Process new skills from text input
                new_skills = request.POST.get('new_skills', '')
                for skill_name in [s.strip() for s in new_skills.split(',') if s.strip()]:
                    skill_obj, created = Skill.objects.get_or_create(name=skill_name.lower())
                    profile.skills.add(skill_obj)
                
                # Process tech stack from multi-select
                tech_ids = request.POST.getlist('tech_stack', [])
                profile.tech_stack.clear()
                if tech_ids:
                    profile.tech_stack.add(*tech_ids)
                
                # Process new tech from text input
                new_tech = request.POST.get('new_tech_stack', '')
                for tech_name in [t.strip() for t in new_tech.split(',') if t.strip()]:
                    tech_obj, created = TechStack.objects.get_or_create(name=tech_name.lower())
                    profile.tech_stack.add(tech_obj)
                
                # Process hackathons
                hackathon_ids = request.POST.getlist('interested_hackathons', [])
                profile.interested_hackathons.clear()
                if hackathon_ids:
                    profile.interested_hackathons.add(*hackathon_ids)
                
                # Process new hackathon
                hackathon_name = request.POST.get('hackathon_name', '').strip()
                if hackathon_name:
                    hackathon_level = request.POST.get('hackathon_level', 'other')
                    hackathon_location = request.POST.get('hackathon_location', 'Online').strip()
                    
                    if not hackathon_location:
                        hackathon_location = 'Online'
                    
                    hackathon_obj, created = Hackathon.objects.get_or_create(
                        name=hackathon_name,
                        defaults={
                            'level': hackathon_level,
                            'start_date': request.POST.get('hackathon_date') or None,
                            'end_date': request.POST.get('hackathon_date') or None,
                            'description': request.POST.get('hackathon_description', ''),
                            'location': hackathon_location
                        }
                    )
                    profile.interested_hackathons.add(hackathon_obj)
                
                messages.success(request, 'Profile updated successfully!')
                return redirect('profile_detail', pk=profile.pk)
            
            except Exception as e:
                logger.error(f"Error saving profile: {str(e)}")
                messages.error(request, 'An error occurred while saving your profile.')
        
        else:
            logger.error("Form validation failed. Errors: %s", form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'finder/edit_profile.html', {
        'form': form,
        'today': timezone.now().date()  # Add this for hackathon date comparisons
    })

# @login_required
# def edit_profile(request):
#     profile = request.user.profile
#     logger.debug("Edit profile view accessed for user: %s", request.user)
    
#     if request.method == 'POST':
#         logger.debug("POST data: %s", request.POST)
#         logger.debug("FILES data: %s", request.FILES)
        
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             # Save basic profile info
#             profile = form.save(commit=False)
            
#             # Handle profile picture
#             if 'profile_picture' in request.FILES:
#                 profile.profile_picture = request.FILES['profile_picture']
#             profile.save()
            
#             # Save many-to-many relationships
#             form.save_m2m()
            
#             # Process skills
#             skill_ids = request.POST.getlist('skills')
#             profile.skills.clear()
#             for skill_id in skill_ids:
#                 try:
#                     skill_obj = Skill.objects.get(id=skill_id)  # Changed variable name
#                     profile.skills.add(skill_obj)
#                 except Skill.DoesNotExist:
#                     logger.warning("Skill with ID %s not found", skill_id)
#                     pass
            
#             # Process new skills
#             new_skills = request.POST.get('new_skills', '')
#             for skill_name in [s.strip() for s in new_skills.split(',') if s.strip()]:
#                 skill_obj, created = Skill.objects.get_or_create(name=skill_name.lower())
#                 profile.skills.add(skill_obj)
            
#             # Process tech stack
#             tech_ids = request.POST.getlist('tech_stack')
#             profile.tech_stack.clear()
#             for tech_id in tech_ids:
#                 try:
#                     tech_obj = TechStack.objects.get(id=tech_id)
#                     profile.tech_stack.add(tech_obj)
#                 except TechStack.DoesNotExist:
#                     logger.warning("TechStack with ID %s not found", tech_id)
#                     pass
            
#             # Process new tech
#             new_tech = request.POST.get('new_tech_stack', '')
#             for tech_name in [t.strip() for t in new_tech.split(',') if t.strip()]:
#                 tech_obj, created = TechStack.objects.get_or_create(name=tech_name.lower())
#                 profile.tech_stack.add(tech_obj)
            
#             hackathon_ids = request.POST.getlist('interested_hackathons')
#             profile.interested_hackathons.clear()
#             for hackathon_id in hackathon_ids:
#                 try:
#                     hackathon_obj = Hackathon.objects.get(id=hackathon_id)
#                     profile.interested_hackathons.add(hackathon_obj)
#                 except Hackathon.DoesNotExist:
#                     logger.warning("Hackathon with ID %s not found", hackathon_id)
            
#             # Process new hackathon
#             hackathon_name = request.POST.get('hackathon_name', '').strip()
#             if hackathon_name:
#                 hackathon_level = request.POST.get('hackathon_level', 'other')
#                 hackathon_location = request.POST.get('hackathon_location', 'Online').strip()  # Get location from input
                
#                 # Validate location - default to "Online" if empty
#                 if not hackathon_location:
#                     hackathon_location = 'Online'
#                     messages.info(request, "Location defaulted to 'Online' as no value was provided")
                
#                 # Create or get the Hackathon object
#                 hackathon_obj, created = Hackathon.objects.get_or_create(
#                     name=hackathon_name,
#                     defaults={
#                         'level': hackathon_level,
#                         'start_date': request.POST.get('hackathon_date') or None,
#                         'end_date': request.POST.get('hackathon_date') or None,
#                         'description': request.POST.get('hackathon_description', ''),
#                         'location': hackathon_location  # Use the user-provided location
#                     }
#                 )
#                 profile.interested_hackathons.add(hackathon_obj)
            
#             messages.success(request, 'Profile updated successfully!')
#             return redirect('profile_detail', pk=profile.pk)
#         else:
#             logger.error("Form validation failed. Errors: %s", form.errors)
#             for field, errors in form.errors.items():
#                 for error in errors:
#                     messages.error(request, f"{field}: {error}")
#     else:
#         form = ProfileForm(instance=profile)
    
#     return render(request, 'finder/edit_profile.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('edit_profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'finder/register.html', {'form': form})

@login_required
def profile_detail(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    return render(request, 'finder/profile_detail.html', {'profile': profile})

@login_required
def profile_list(request):
    profiles = Profile.objects.exclude(user=request.user).select_related('user').order_by('-user__last_login')
    form = ProfileSearchForm(request.GET)
    
    if form.is_valid():
        search = form.cleaned_data.get('search')
        skills = form.cleaned_data.get('skills')
        location = form.cleaned_data.get('location')
        hackathon = form.cleaned_data.get('hackathon')
        
        if search:
            profiles = profiles.filter(
                Q(user__username__icontains=search) |
                Q(bio__icontains=search)
            )
        if skills:
            profiles = profiles.filter(skills__in=skills).distinct()
        if location:
            profiles = profiles.filter(location__icontains=location)
        if hackathon:
            profiles = profiles.filter(interested_hackathons=hackathon)
    
    paginator = Paginator(profiles, 10)
    page = request.GET.get('page')
    profiles = paginator.get_page(page)
    
    return render(request, 'finder/profile_list.html', {
        'profiles': profiles,
        'form': form
    })

@login_required
def inbox(request):
    messages_received = Message.objects.filter(receiver=request.user).order_by('-timestamp')
    messages_sent = Message.objects.filter(sender=request.user).order_by('-timestamp')
    unread_count = messages_received.filter(is_read=False).count()
    
    return render(request, 'finder/inbox.html', {
        'messages_received': messages_received,
        'messages_sent': messages_sent,
        'unread_count': unread_count,
    })


@login_required
def send_message(request, receiver_pk):
    receiver = get_object_or_404(User, pk=receiver_pk)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            messages.success(request, 'Message sent successfully!')
            return redirect('inbox')
    else:
        form = MessageForm()
    
    return render(request, 'finder/send_message.html', {
        'form': form,
        'receiver': receiver
    })

@login_required
def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk)
    if message.receiver == request.user and not message.is_read:
        message.is_read = True
        message.save()
    return render(request, 'finder/message_detail.html', {'message': message}) 


def some_view(request):
    unread_count = 0
    if request.user.is_authenticated:
        unread_count = request.user.received_messages.filter(is_read=False).count()
    return render(request, 'template.html', {'unread_count': unread_count})

from django.contrib.auth import logout
from django.views.decorators.http import require_POST

@require_POST
def logout_view(request):
    logout(request)
    return redirect('register')  # or redirect to your preferred page

import logging
logger = logging.getLogger(__name__)

