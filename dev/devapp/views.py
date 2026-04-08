# API imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
# Basic imports
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here. 
# API Config
#=================================================================================

class CategoryListAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        categories = Category.objects.filter(is_active=True).order_by("name")
        serializer = CategoryPublicSerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProjectListAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        projects = Project.objects.select_related("type").order_by("-created_at")
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TestimonialListAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        testomonial = Testimonial.objects.filter(is_active=True).order_by("order")
        serializer = TestimonialSerializer(testomonial, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SocialMediaAccountListAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        accounts = SocialMediaAccounts.objects.filter(is_active=True)
        serializer = SocialMediaAccountSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ClientLogoListAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        logos = Logo.objects.filter(is_active=True)
        serializer = ClientLogoSerializer(logos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ContactCreateAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ContactSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "Message submitted successfully"
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "success": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
class AboutUsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        about = AboutUs.objects.first() 
        serializer = AboutUsSerializer(about)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ValueListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        values = Value.objects.all()
        serializer = ValueSerializer(values, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TeamMemberListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        team = TeamMember.objects.all()  
        serializer = TeamMemberSerializer(team, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# CMS
#=================================================================================

@login_required
def paginate_data(request, page_num, data_list):
    items_per_page, max_pages = 5, 10
    paginator = Paginator(data_list, items_per_page)
    last_page_number = paginator.num_pages

    try:
        data_list = paginator.page(page_num)
    except PageNotAnInteger:
        data_list = paginator.page(1)
    except EmptyPage:
        data_list = paginator.page(paginator.num_pages)

    current_page = data_list.number
    start_page = max(current_page - int(max_pages / 2), 1)
    end_page = start_page + max_pages

    if end_page > last_page_number:
        end_page = last_page_number + 1
        start_page = max(end_page - max_pages, 1)

    paginator_list = range(start_page, end_page)

    return data_list, paginator_list, last_page_number


def login_view(request):

    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect("dashboard")
    
    if request.method == "GET" and 'next' in request.GET:
        messages.warning(request, "Please login first to access that page.")

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, "Logged in successfully!")

            next_url = request.GET.get('next')
            if next_url:
                next_url = next_url.strip()
            else:
                next_url = "dashboard"

            return redirect(next_url)

        messages.error(request, "Invalid credentials or not authorized.")

    return render(request, 'login/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def contact_inbox(request):

    messages = PostMessage.objects.all().order_by('-created_at')
    unread_count = messages.filter(is_read=False).count()

    context = {
        "message": messages,
        "unread_count": unread_count
    }

    return render(request, 'home/inbox.html', context)

@require_POST
def mark_seen(request, id):
    message = get_object_or_404(PostMessage, id=id)

    if not message.is_read:
        message.is_read = True
        message.save()
        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "already_seen"})

@require_POST
def delete_message(request, id):
    message = get_object_or_404(PostMessage, id=id)

    was_unread = not message.is_read
    message.delete()

    return JsonResponse({
        "status": "success",
        "was_unread": was_unread
    })


@login_required
def dashboard(request):

    return render(request, 'home/home.html')

#Admin Posts
@login_required
def add_service(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        service = Category(
            name=name,
            description=description
        )
        service.save()

    return render(request, 'services/add_service.html')

@login_required
def service_list(request):

    services = Category.objects.all().order_by('-id')
    page_number = int(request.GET.get('page', 1))
    services, paginator_list, last_page_number = paginate_data(request, page_number, services)

    context = {
        'paginator_list': paginator_list,
        'last_page_number': last_page_number,
        'services': services,
        'first_page_number': 1
    }

    return render(request, 'services/service_list.html', context)

@login_required
def service_details(request, slug):

    service = get_object_or_404(Category, slug=slug)
    context = {
        'service': service
    }

    return render(request, 'services/service_details.html', context)

@login_required
def edit_service(request, slug):

    service = get_object_or_404(Category, slug=slug)

    if request.method == 'POST':
        service.name = request.POST.get('name')
        service.description = request.POST.get('description')
        service.is_active = request.POST.get('is_active') == 'on'
        service.save()

        messages.success(request, 'Service updated successfully.')
        return redirect('service_details', slug=service.slug)

    context = {
        'service': service
    }

    return render(request, 'services/edit_service.html', context)

@login_required
def add_logo(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        logo = request.FILES.get('logo')
        logos = Logo(
            name=name,
            logo=logo,
        )
        logos.save()

    return render(request, 'logo/add_logo.html')

@login_required
def view_logo(request):

    logos = Logo.objects.all().order_by('-id')
    page_number = int(request.GET.get('page', 1))
    logos, paginator_list, last_page_number = paginate_data(request, page_number, logos)

    context = {
        'paginator_list': paginator_list,
        'last_page_number': last_page_number,
        'logos': logos,
        'first_page_number': 1
    }

    return render(request, 'logo/logo_list.html', context)

@login_required
def logo_details(request, slug):
    logo = get_object_or_404(Logo, slug=slug)
    context = {
        'logo': logo
    }

    return render(request, 'logo/logo_details.html', context)


@login_required
def edit_logo(request, slug):
    
    logo = get_object_or_404(Logo, slug=slug)

    if request.method == 'POST':
        logo.name = request.POST.get('name')
        logo.is_active = request.POST.get('is_active') == 'on'

        if 'logo' in request.FILES:
            logo.logo = request.FILES['logo']

        logo.save()
        messages.success(request, 'Logo updated successfully.')
        return redirect('logo_details', slug=logo.slug)
    
    context = {
        'logo': logo
    }

    return render(request, 'logo/edit_logo.html', context)


@login_required
def add_testimonial(request):
    if request.method == 'POST':
        client_name = request.POST.get('client_name')
        client_title = request.POST.get('client_title')
        company_name = request.POST.get('company_name')
        company_logo_id  = request.POST.get('company_logo')
        rating = int(request.POST.get('rating') or 5)
        testimonial = request.POST.get('testimonial')
        is_active = request.POST.get('is_active') == 'on'
        order = int(request.POST.get('order') or 0)
        company_logo = None
        if company_logo_id:
            company_logo = Logo.objects.filter(id=company_logo_id).first()

        client_image = request.FILES.get('client_image')

        testimonials = Testimonial(
            client_name=client_name,
            client_title=client_title,
            company_name=company_name,
            company_logo=company_logo,
            client_image=client_image,
            rating=rating,
            testimonial=testimonial,
            is_active=is_active,
            order=order
        )
        testimonials.save()
        messages.success(request, 'Testimonial added successfully.')
        return redirect('testimonial')
    
    logos = Logo.objects.filter(is_active=True)

    context = {
        'logos': logos
    }

    return render(request, 'testimonial/add_testimonial.html', context)

@login_required
def view_testimonial(request):

    testimonials = Testimonial.objects.all().order_by('-id')
    page_number = int(request.GET.get('page', 1))
    testimonials, paginator_list, last_page_number = paginate_data(request, page_number, testimonials)

    context = {
        'paginator_list': paginator_list,
        'last_page_number': last_page_number,
        'testimonials': testimonials,
        'first_page_number': 1
    }

    return render(request, 'testimonial/testimonial_list.html', context)

@login_required
def testimonial_details(request, slug):
    testimonial = get_object_or_404(Testimonial, slug=slug)
    context = {
        'testimonial': testimonial
    }

    return render(request, 'testimonial/testimonial_details.html', context)

@login_required
def edit_testimonial(request, slug):
    testimonial = get_object_or_404(Testimonial, slug=slug)

    if request.method == 'POST':
        testimonial.client_name = request.POST.get('client_name')
        testimonial.client_title = request.POST.get('client_title')
        testimonial.company_name = request.POST.get('company_name')

        company_logo_id = request.POST.get('company_logo')
        if company_logo_id:
            testimonial.company_logo = Logo.objects.filter(id=company_logo_id).first()
        else:
            testimonial.company_logo = None

        if 'client_image' in request.FILES:
            testimonial.client_image = request.FILES['client_image']

        testimonial.rating = int(request.POST.get('rating') or 5)
        testimonial.testimonial = request.POST.get('testimonial')
        testimonial.is_active = request.POST.get('is_active') == 'on'
        testimonial.order = int(request.POST.get('order') or 0)

        testimonial.save()
        messages.success(request, 'Testimonial updated successfully.')
        return redirect('testimonial_details', slug=testimonial.slug)
    
    logos = Logo.objects.filter(is_active=True)

    context = {
        'testimonial': testimonial,
        'logos': logos
    }

    return render(request, 'testimonial/edit_testimonial.html', context)

@login_required
def add_projects(request):

    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('type')
        website = request.POST.get('website')
        project_summary = request.POST.get('project_summary')
        description = request.POST.get('description')

        if not title:
            messages.error(request, "Title is required.")
            return redirect('add_new_project')

        category = None
        if category_id:
            category = Category.objects.filter(id=category_id).first()
        
        project_image = request.FILES.get('project_image')

        project = Project(
            title=title,
            type=category,
            project_image=project_image,
            website=website,
            project_summary=project_summary,
            description=description
        )

        project.save()

        messages.success(request, 'Project added successfully.')
        return redirect('project')
    
    categories = Category.objects.all()

    context = {
        'categories': categories
    }

    return render(request, 'project/add_project.html', context)

@login_required
def view_projects(request):

    projects = Project.objects.all().order_by('-id')
    page_number = int(request.GET.get('page', 1))
    projects, paginator_list, last_page_number = paginate_data(request, page_number, projects)


    context = {
        'paginator_list': paginator_list,
        'last_page_number': last_page_number,
        'projects': projects,
        'first_page_number': 1
    }

    return render(request, 'project/project_list.html', context)

@login_required
def project_details(request, slug):
    project = get_object_or_404(Project, slug=slug)
    context = {
        'project': project
    }

    return render(request, 'project/project_details.html', context)

@login_required
def edit_project(request, slug):
    project = get_object_or_404(Project, slug=slug)

    if request.method == 'POST':
        project.title = request.POST.get('title')
        project.website = request.POST.get('website')
        project.description = request.POST.get('description')
        project.project_summary = request.POST.get('project_summary')

        category_id = request.POST.get('type')
        if category_id:
            project.type = Category.objects.filter(id=category_id).first()
        else:
            project.type = None

        if 'project_image' in request.FILES:
            project.project_image = request.FILES['project_image']

        project.save()

        messages.success(request, 'Project updated successfully.')
        return redirect('project_details', slug=project.slug)
    
    categories = Category.objects.all()

    context = {
        'project': project,
        'categories': categories
    }

    return render(request, 'project/edit_project.html', context)

@login_required
def add_acc(request):
    if request.method == 'POST':
        platform = request.POST.get('platform')
        url = request.POST.get('url')
        icon = request.POST.get('icon')
        is_active = request.POST.get('is_active') == 'on'
        order = int(request.POST.get('order') or 0)

        if not platform:
            messages.error(request, "Platform is required.")
            return redirect('add_new_accounts')
        
        if SocialMediaAccounts.objects.filter(platform=platform).exists():
            messages.error(request, "This platform already exists.")
            return redirect('add_new_accounts')

        account = SocialMediaAccounts(
            platform=platform,
            url=url,
            icon=icon,
            is_active=is_active,
            order=order
        )

        account.save()

        messages.success(request, "Account added successfully.")
        return redirect('accounts')
    
    return render(request, 'accounts/add_accounts.html')

@login_required
def social_media_acc(request):

    accounts = SocialMediaAccounts.objects.all().order_by('order')
    page_number = int(request.GET.get('page', 1))
    accounts, paginator_list, last_page_number = paginate_data(request, page_number, accounts)

    context = {
        'paginator_list': paginator_list,
        'last_page_number': last_page_number,
        'accounts': accounts,
        'first_page_number': 1
    }

    return render(request, 'accounts/accounts_list.html', context)

@login_required
def accounts_details(request, platform):
    account = get_object_or_404(SocialMediaAccounts, platform=platform)

    context = {
        'account': account
    }

    return render(request, 'accounts/accounts_details.html', context)

@login_required
def edit_accounts(request, platform):
    account = get_object_or_404(SocialMediaAccounts, platform=platform)

    if request.method == 'POST':
        account.url = request.POST.get('url')
        account.icon = request.POST.get('icon')
        account.is_active = request.POST.get('is_active') == 'on'
        account.order = int(request.POST.get('order') or 0)

        account.save()

        messages.success(request, "Account updated successfully.")
        return redirect('accounts')

    context = {
        'account': account
    }

    return render(request, 'accounts/edit_accounts.html', context)
# ------------------About Us Start-----------------------
@login_required
def edit_about_us(request):
    about = AboutUs.objects.first()

    # Ensure one object exists
    if not about:
        about = AboutUs.objects.create(subheading="", story_description="")

    if request.method == 'POST':
        about.heading = request.POST.get('heading')
        about.subheading = request.POST.get('subheading')
        about.story_title = request.POST.get('story_title')
        about.story_description = request.POST.get('story_description')

        about.projects_completed = request.POST.get('projects_completed') or 0
        about.happy_clients = request.POST.get('happy_clients') or 0
        about.years_experience = request.POST.get('years_experience') or 0
        about.team_members_count = request.POST.get('team_members_count') or 0

        about.save()

        messages.success(request, 'About Us updated successfully.')
        return redirect('edit_about_us')

    context = {
        'about': about
    }

    return render(request, 'about/edit_about.html', context)
# ------------------About Us End-----------------------

# ------------------Company Values Start-----------------------
@login_required
def add_value(request):

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        icon = request.POST.get('icon')

        if not title:
            messages.error(request, "Title is required.")
            return redirect('add_value')

        Value.objects.create(
            title=title,
            description=description,
            icon=icon
        )

        messages.success(request, 'Value added successfully.')
        return redirect('value_list')

    return render(request, 'value/add_value.html')

@login_required
def view_values(request):
    values = Value.objects.all().order_by('-id')

    context = {
        'values': values
    }

    return render(request, 'value/value_list.html', context)

@login_required
def edit_value(request, pk):
    value = get_object_or_404(Value, pk=pk)

    if request.method == 'POST':
        value.title = request.POST.get('title')
        value.description = request.POST.get('description')
        value.icon = request.POST.get('icon')

        value.save()

        messages.success(request, 'Value updated successfully.')
        return redirect('value_list')

    context = {
        'value': value
    }

    return render(request, 'value/edit_value.html', context)

@login_required
def delete_value(request, pk):
    value = get_object_or_404(Value, pk=pk)
    value.delete()

    messages.success(request, 'Value deleted successfully.')
    return redirect('value_list')
# ------------------Company Values End-----------------------

# ------------------Team Member Start-----------------------
@login_required
def add_team_member(request):

    if request.method == 'POST':
        name = request.POST.get('name')
        designation = request.POST.get('designation')
        order = request.POST.get('order')

        image = request.FILES.get('image')

        if not name:
            messages.error(request, "Name is required.")
            return redirect('add_team_member')

        TeamMember.objects.create(
            name=name,
            designation=designation,
            image=image,
            order=order or 0
        )

        messages.success(request, 'Team member added successfully.')
        return redirect('team_list')

    return render(request, 'team/add_team.html')

@login_required
def view_team_members(request):
    members = TeamMember.objects.all()  # already ordered by Meta

    context = {
        'members': members
    }

    return render(request, 'team/team_list.html', context)

@login_required
def edit_team_member(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)

    if request.method == 'POST':
        member.name = request.POST.get('name')
        member.designation = request.POST.get('designation')
        member.order = request.POST.get('order') or 0

        if 'image' in request.FILES:
            member.image = request.FILES['image']

        member.save()

        messages.success(request, 'Team member updated successfully.')
        return redirect('team_list')

    context = {
        'member': member
    }

    return render(request, 'team/edit_team.html', context)

@login_required
def delete_team_member(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    member.delete()

    messages.success(request, 'Team member deleted successfully.')
    return redirect('team_list')
# ------------------Team Member End-----------------------

@login_required
@require_POST
def delete_service(request, slug):
    service = get_object_or_404(Category, slug=slug)
    service.delete()
    messages.success(request, 'Service deleted successfully.')
    return redirect('service')


@login_required
@require_POST
def delete_logo(request, slug):
    logo = get_object_or_404(Logo, slug=slug)
    logo.delete()
    messages.success(request, 'Logo deleted successfully.')
    return redirect('logo')


@login_required
@require_POST
def delete_testimonial(request, slug):
    testimonial = get_object_or_404(Testimonial, slug=slug)
    testimonial.delete()
    messages.success(request, 'Testimonial deleted successfully.')
    return redirect('testimonial')


@login_required
@require_POST
def delete_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    project.delete()
    messages.success(request, 'Project deleted successfully.')
    return redirect('project')

