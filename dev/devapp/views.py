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


# ==============================================================================
# API — PUBLIC ENDPOINTS
# ==============================================================================

class ServiceListAPI(APIView):
    """Returns all active services (lightweight — no nested children)."""
    permission_classes = [AllowAny]

    def get(self, request):
        services = Service.objects.filter(is_active=True).prefetch_related(
            "badges"
        ).order_by("name")
        serializer = ServiceListSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ServiceDetailAPI(APIView):
    """Returns full service detail including all nested children."""
    permission_classes = [AllowAny]

    def get(self, request, slug):
        service = get_object_or_404(Service, slug=slug, is_active=True)
        serializer = ServiceDetailSerializer(service)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ==============================================================================
# API — SERVICE SUB-RESOURCE ENDPOINTS
# Each resolves the parent Service by slug, then returns only the requested
# sub-resource — keeping the detail endpoint lightweight.
# ==============================================================================

class ServiceProcessAPI(APIView):
    """GET /api/v1/portfolio/services/{slug}/process/"""
    permission_classes = [AllowAny]

    def get(self, request, slug):
        service = get_object_or_404(Service, slug=slug, is_active=True)
        steps = service.process_steps.all()
        serializer = ServiceProcessSerializer(steps, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ServiceGalleryAPI(APIView):
    """GET /api/v1/portfolio/services/{slug}/gallery/"""
    permission_classes = [AllowAny]

    def get(self, request, slug):
        service = get_object_or_404(Service, slug=slug, is_active=True)
        gallery = service.gallery.all()
        serializer = ServiceGallerySerializer(gallery, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ServiceDeliverablesAPI(APIView):
    """GET /api/v1/portfolio/services/{slug}/deliverables/
    Returns a flat string array: ["Item 1", "Item 2"]
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        service = get_object_or_404(Service, slug=slug, is_active=True)
        serializer = ServiceDeliverableSerializer(service.deliverables.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ServiceToolsAPI(APIView):
    """GET /api/v1/portfolio/services/{slug}/tools/
    Returns a flat string array: ["Figma", "Photoshop"]
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        service = get_object_or_404(Service, slug=slug, is_active=True)
        serializer = ServiceToolSerializer(service.tools.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ServicePricingTiersAPI(APIView):
    """GET /api/v1/portfolio/services/{slug}/pricingtiers/"""
    permission_classes = [AllowAny]

    def get(self, request, slug):
        service = get_object_or_404(Service, slug=slug, is_active=True)
        tiers = service.pricing_tiers.prefetch_related("features").all()
        serializer = ServicePricingTierSerializer(tiers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ServiceReviewsAPI(APIView):
    """GET /api/v1/portfolio/services/{slug}/reviews/"""
    permission_classes = [AllowAny]

    def get(self, request, slug):
        service = get_object_or_404(Service, slug=slug, is_active=True)
        reviews = service.reviews.all()
        serializer = ServiceReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ServiceRelatedAPI(APIView):
    """GET /api/v1/portfolio/services/{slug}/related/"""
    permission_classes = [AllowAny]

    def get(self, request, slug):
        service = get_object_or_404(Service, slug=slug, is_active=True)
        related = service.related_from.select_related("related_service").all()
        serializer = ServiceRelatedSerializer(related, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectListAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        projects = Project.objects.order_by("-created_at")
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TestimonialListAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        testimonials = Testimonial.objects.order_by("order_no")
        serializer = TestimonialSerializer(testimonials, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SocialMediaAccountListAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        accounts = SocialMediaAccounts.objects.filter(is_active=True).order_by("order_no")
        serializer = SocialMediaAccountSerializer(accounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClientLogoListAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        logos = Logo.objects.filter(is_active=True).order_by("order_no")
        serializer = ClientLogoSerializer(logos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContactCreateAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ContactSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"success": True, "message": "Message submitted successfully"},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
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
        values = Value.objects.all().order_by("order_no")
        serializer = ValueSerializer(values, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeamMemberListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        team = TeamMember.objects.all()  # already ordered by order_no via Meta
        serializer = TeamMemberSerializer(team, many=True, context={"request": request})
        return Response(serializer.data, status=status.HTTP_200_OK)


# ==============================================================================
# CMS — HELPERS
# ==============================================================================

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


# ==============================================================================
# CMS — AUTH
# ==============================================================================

def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect("dashboard")

    if request.method == "GET" and "next" in request.GET:
        messages.warning(request, "Please login first to access that page.")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, "Logged in successfully!")
            next_url = request.GET.get("next", "").strip() or "dashboard"
            return redirect(next_url)

        messages.error(request, "Invalid credentials or not authorized.")

    return render(request, "login/login.html")


@login_required
def user_logout(request):
    logout(request)
    return redirect("login")


# ==============================================================================
# CMS — INBOX
# ==============================================================================

@login_required
def contact_inbox(request):
    inbox = PostMessage.objects.all().order_by("-created_at")
    unread_count = inbox.filter(is_read=False).count()

    context = {
        "message": inbox,
        "unread_count": unread_count,
    }

    return render(request, "home/inbox.html", context)


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
    return JsonResponse({"status": "success", "was_unread": was_unread})


# ==============================================================================
# CMS — DASHBOARD
# ==============================================================================

@login_required
def dashboard(request):
    return render(request, "home/home.html")


# ==============================================================================
# CMS — SERVICES  (replaces old Category views)
# ==============================================================================

@login_required
def add_service(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        pitch = request.POST.get("pitch", "")
        timeline = request.POST.get("timeline", "")
        price_from = request.POST.get("price_from") or 0
        delivery_days = request.POST.get("delivery_days") or 0
        rating = request.POST.get("rating") or 5.0
        review_count = request.POST.get("review_count") or 0
        cover = request.FILES.get("cover")

        if not name:
            messages.error(request, "Name is required.")
            return redirect("add_service")

        Service.objects.create(
            name=name,
            description=description,
            pitch=pitch,
            timeline=timeline,
            price_from=price_from,
            delivery_days=delivery_days,
            rating=rating,
            review_count=review_count,
            cover=cover,
        )

        messages.success(request, "Service added successfully.")
        return redirect("service")

    return render(request, "services/add_service.html")


@login_required
def service_list(request):
    services = Service.objects.all().order_by("-id")
    page_number = int(request.GET.get("page", 1))
    services, paginator_list, last_page_number = paginate_data(request, page_number, services)

    context = {
        "services": services,
        "paginator_list": paginator_list,
        "last_page_number": last_page_number,
        "first_page_number": 1,
    }

    return render(request, "services/service_list.html", context)


@login_required
def service_details(request, slug):
    service = get_object_or_404(Service, slug=slug)
    context = {"service": service}
    return render(request, "services/service_details.html", context)


@login_required
def edit_service(request, slug):
    service = get_object_or_404(Service, slug=slug)

    if request.method == "POST":
        service.name = request.POST.get("name")
        service.description = request.POST.get("description")
        service.pitch = request.POST.get("pitch")
        service.timeline = request.POST.get("timeline")
        service.price_from = request.POST.get("price_from") or 0
        service.delivery_days = request.POST.get("delivery_days") or 0
        service.rating = request.POST.get("rating") or 5.0
        service.review_count = request.POST.get("review_count") or 0
        service.is_active = request.POST.get("is_active") == "on"

        if "cover" in request.FILES:
            service.cover = request.FILES["cover"]

        service.save()
        messages.success(request, "Service updated successfully.")
        return redirect("service_details", slug=service.slug)

    context = {"service": service}
    return render(request, "services/edit_service.html", context)


@login_required
@require_POST
def delete_service(request, slug):
    service = get_object_or_404(Service, slug=slug)
    service.delete()
    messages.success(request, "Service deleted successfully.")
    return redirect("service")


# ==============================================================================
# CMS — LOGOS
# ==============================================================================

@login_required
def add_logo(request):
    if request.method == "POST":
        name = request.POST.get("name")
        logo = request.FILES.get("logo")
        order_no = int(request.POST.get("order_no") or 0)

        Logo.objects.create(name=name, logo=logo, order_no=order_no)
        messages.success(request, "Logo added successfully.")
        return redirect("logo")

    return render(request, "logo/add_logo.html")


@login_required
def view_logo(request):
    logos = Logo.objects.all().order_by("-id")
    page_number = int(request.GET.get("page", 1))
    logos, paginator_list, last_page_number = paginate_data(request, page_number, logos)

    context = {
        "logos": logos,
        "paginator_list": paginator_list,
        "last_page_number": last_page_number,
        "first_page_number": 1,
    }

    return render(request, "logo/logo_list.html", context)


@login_required
def logo_details(request, slug):
    logo = get_object_or_404(Logo, slug=slug)
    context = {"logo": logo}
    return render(request, "logo/logo_details.html", context)


@login_required
def edit_logo(request, slug):
    logo = get_object_or_404(Logo, slug=slug)

    if request.method == "POST":
        logo.name = request.POST.get("name")
        logo.is_active = request.POST.get("is_active") == "on"
        logo.order_no = int(request.POST.get("order_no") or 0)

        if "logo" in request.FILES:
            logo.logo = request.FILES["logo"]

        logo.save()
        messages.success(request, "Logo updated successfully.")
        return redirect("logo_details", slug=logo.slug)

    context = {"logo": logo}
    return render(request, "logo/edit_logo.html", context)


@login_required
@require_POST
def delete_logo(request, slug):
    logo = get_object_or_404(Logo, slug=slug)
    logo.delete()
    messages.success(request, "Logo deleted successfully.")
    return redirect("logo")


# ==============================================================================
# CMS — TESTIMONIALS
# ==============================================================================

@login_required
def add_testimonial(request):
    if request.method == "POST":
        client_name = request.POST.get("client_name")
        client_title = request.POST.get("client_title")
        rating = int(request.POST.get("rating") or 5)
        testimonial_text = request.POST.get("testimonial")
        order_no = int(request.POST.get("order_no") or 0)
        client_image = request.FILES.get("client_image")

        Testimonial.objects.create(
            client_name=client_name,
            client_title=client_title,
            client_image=client_image,
            rating=rating,
            testimonial=testimonial_text,
            order_no=order_no,
        )

        messages.success(request, "Testimonial added successfully.")
        return redirect("testimonial")

    return render(request, "testimonial/add_testimonial.html")


@login_required
def view_testimonial(request):
    testimonials = Testimonial.objects.all().order_by("-id")
    page_number = int(request.GET.get("page", 1))
    testimonials, paginator_list, last_page_number = paginate_data(request, page_number, testimonials)

    context = {
        "testimonials": testimonials,
        "paginator_list": paginator_list,
        "last_page_number": last_page_number,
        "first_page_number": 1,
    }

    return render(request, "testimonial/testimonial_list.html", context)


@login_required
def testimonial_details(request, pk):
    # slug removed from Testimonial — route by pk instead
    testimonial = get_object_or_404(Testimonial, pk=pk)
    context = {"testimonial": testimonial}
    return render(request, "testimonial/testimonial_details.html", context)


@login_required
def edit_testimonial(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)

    if request.method == "POST":
        testimonial.client_name = request.POST.get("client_name")
        testimonial.client_title = request.POST.get("client_title")
        testimonial.rating = int(request.POST.get("rating") or 5)
        testimonial.testimonial = request.POST.get("testimonial")
        testimonial.order_no = int(request.POST.get("order_no") or 0)

        if "client_image" in request.FILES:
            testimonial.client_image = request.FILES["client_image"]

        testimonial.save()
        messages.success(request, "Testimonial updated successfully.")
        return redirect("testimonial_details", pk=testimonial.pk)

    context = {"testimonial": testimonial}
    return render(request, "testimonial/edit_testimonial.html", context)


@login_required
@require_POST
def delete_testimonial(request, pk):
    testimonial = get_object_or_404(Testimonial, pk=pk)
    testimonial.delete()
    messages.success(request, "Testimonial deleted successfully.")
    return redirect("testimonial")


# ==============================================================================
# CMS — PROJECTS
# ==============================================================================

@login_required
def add_projects(request):
    if request.method == "POST":
        title = request.POST.get("title")
        project_type = request.POST.get("type", "")  # now a plain string
        website = request.POST.get("website")
        project_summary = request.POST.get("project_summary")
        description = request.POST.get("description")
        project_image = request.FILES.get("project_image")

        if not title:
            messages.error(request, "Title is required.")
            return redirect("add_new_project")

        Project.objects.create(
            title=title,
            type=project_type,
            project_image=project_image,
            website=website,
            project_summary=project_summary,
            description=description,
        )

        messages.success(request, "Project added successfully.")
        return redirect("project")

    # Provide the type choices from the model for the dropdown
    PROJECT_TYPE_CHOICES = [
        "ecommerce", "branding", "web-design",
        "mobile-app", "ui-ux", "marketing",
    ]

    context = {"project_type_choices": PROJECT_TYPE_CHOICES}
    return render(request, "project/add_project.html", context)


@login_required
def view_projects(request):
    projects = Project.objects.all().order_by("-id")
    page_number = int(request.GET.get("page", 1))
    projects, paginator_list, last_page_number = paginate_data(request, page_number, projects)

    context = {
        "projects": projects,
        "paginator_list": paginator_list,
        "last_page_number": last_page_number,
        "first_page_number": 1,
    }

    return render(request, "project/project_list.html", context)


@login_required
def project_details(request, slug):
    project = get_object_or_404(Project, slug=slug)
    context = {"project": project}
    return render(request, "project/project_details.html", context)


@login_required
def edit_project(request, slug):
    project = get_object_or_404(Project, slug=slug)

    PROJECT_TYPE_CHOICES = [
        "ecommerce", "branding", "web-design",
        "mobile-app", "ui-ux", "marketing",
    ]

    if request.method == "POST":
        project.title = request.POST.get("title")
        project.type = request.POST.get("type", "")  # plain string, no FK lookup
        project.website = request.POST.get("website")
        project.project_summary = request.POST.get("project_summary")
        project.description = request.POST.get("description")

        if "project_image" in request.FILES:
            project.project_image = request.FILES["project_image"]

        project.save()
        messages.success(request, "Project updated successfully.")
        return redirect("project_details", slug=project.slug)

    context = {
        "project": project,
        "project_type_choices": PROJECT_TYPE_CHOICES,
    }

    return render(request, "project/edit_project.html", context)


@login_required
@require_POST
def delete_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    project.delete()
    messages.success(request, "Project deleted successfully.")
    return redirect("project")


# ==============================================================================
# CMS — SOCIAL MEDIA ACCOUNTS
# ==============================================================================

@login_required
def add_acc(request):
    if request.method == "POST":
        platform = request.POST.get("platform")
        url = request.POST.get("url")
        icon = request.POST.get("icon")
        username = request.POST.get("username", "")
        is_active = request.POST.get("is_active") == "on"
        order_no = int(request.POST.get("order_no") or 0)

        if not platform:
            messages.error(request, "Platform is required.")
            return redirect("add_new_accounts")

        if SocialMediaAccounts.objects.filter(platform=platform).exists():
            messages.error(request, "This platform already exists.")
            return redirect("add_new_accounts")

        SocialMediaAccounts.objects.create(
            platform=platform,
            url=url,
            icon=icon,
            username=username,
            is_active=is_active,
            order_no=order_no,
        )

        messages.success(request, "Account added successfully.")
        return redirect("accounts")

    return render(request, "accounts/add_accounts.html")


@login_required
def social_media_acc(request):
    accounts = SocialMediaAccounts.objects.all().order_by("order_no")
    page_number = int(request.GET.get("page", 1))
    accounts, paginator_list, last_page_number = paginate_data(request, page_number, accounts)

    context = {
        "accounts": accounts,
        "paginator_list": paginator_list,
        "last_page_number": last_page_number,
        "first_page_number": 1,
    }

    return render(request, "accounts/accounts_list.html", context)


@login_required
def accounts_details(request, platform):
    account = get_object_or_404(SocialMediaAccounts, platform=platform)
    context = {"account": account}
    return render(request, "accounts/accounts_details.html", context)


@login_required
def edit_accounts(request, platform):
    account = get_object_or_404(SocialMediaAccounts, platform=platform)

    if request.method == "POST":
        account.url = request.POST.get("url")
        account.icon = request.POST.get("icon")
        account.username = request.POST.get("username", "")
        account.is_active = request.POST.get("is_active") == "on"
        account.order_no = int(request.POST.get("order_no") or 0)
        account.save()

        messages.success(request, "Account updated successfully.")
        return redirect("accounts")

    context = {"account": account}
    return render(request, "accounts/edit_accounts.html", context)


# ==============================================================================
# CMS — ABOUT US
# ==============================================================================

@login_required
def edit_about_us(request):
    about = AboutUs.objects.first()

    if not about:
        about = AboutUs.objects.create(subheading="", story_description="")

    if request.method == "POST":
        about.heading = request.POST.get("heading")
        about.subheading = request.POST.get("subheading")
        about.story_title = request.POST.get("story_title")
        about.story_description = request.POST.get("story_description")
        about.projects_completed = request.POST.get("projects_completed") or 0
        about.happy_clients = request.POST.get("happy_clients") or 0
        about.years_experience = request.POST.get("years_experience") or 0
        about.team_members_count = request.POST.get("team_members_count") or 0
        about.mission = request.POST.get("mission", "")   # NEW
        about.vision = request.POST.get("vision", "")     # NEW
        about.save()

        messages.success(request, "About Us updated successfully.")
        return redirect("edit_about_us")

    context = {"about": about}
    return render(request, "about/edit_about.html", context)


# ==============================================================================
# CMS — COMPANY VALUES
# ==============================================================================

@login_required
def add_value(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        icon = request.POST.get("icon")
        order_no = int(request.POST.get("order_no") or 0)

        if not title:
            messages.error(request, "Title is required.")
            return redirect("add_value")

        Value.objects.create(title=title, description=description, icon=icon, order_no=order_no)
        messages.success(request, "Value added successfully.")
        return redirect("value_list")

    return render(request, "value/add_value.html")


@login_required
def view_values(request):
    values = Value.objects.all().order_by("order_no")
    context = {"values": values}
    return render(request, "value/value_list.html", context)


@login_required
def edit_value(request, pk):
    value = get_object_or_404(Value, pk=pk)

    if request.method == "POST":
        value.title = request.POST.get("title")
        value.description = request.POST.get("description")
        value.icon = request.POST.get("icon")
        value.order_no = int(request.POST.get("order_no") or 0)
        value.save()

        messages.success(request, "Value updated successfully.")
        return redirect("value_list")

    context = {"value": value}
    return render(request, "value/edit_value.html", context)


@login_required
def delete_value(request, pk):
    value = get_object_or_404(Value, pk=pk)
    value.delete()
    messages.success(request, "Value deleted successfully.")
    return redirect("value_list")


# ==============================================================================
# CMS — TEAM MEMBERS
# ==============================================================================

@login_required
def add_team_member(request):
    if request.method == "POST":
        name = request.POST.get("name")
        designation = request.POST.get("designation")
        order_no = request.POST.get("order_no") or 0
        image = request.FILES.get("image")

        if not name:
            messages.error(request, "Name is required.")
            return redirect("add_team_member")

        TeamMember.objects.create(
            name=name,
            designation=designation,
            image=image,
            order_no=order_no,
        )

        messages.success(request, "Team member added successfully.")
        return redirect("team_list")

    return render(request, "team/add_team.html")


@login_required
def view_team_members(request):
    members = TeamMember.objects.all()  # ordered by order_no via Meta
    context = {"members": members}
    return render(request, "team/team_list.html", context)


@login_required
def edit_team_member(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)

    if request.method == "POST":
        member.name = request.POST.get("name")
        member.designation = request.POST.get("designation")
        member.order_no = request.POST.get("order_no") or 0

        if "image" in request.FILES:
            member.image = request.FILES["image"]

        member.save()
        messages.success(request, "Team member updated successfully.")
        return redirect("team_list")

    context = {"member": member}
    return render(request, "team/edit_team.html", context)


@login_required
def delete_team_member(request, pk):
    member = get_object_or_404(TeamMember, pk=pk)
    member.delete()
    messages.success(request, "Team member deleted successfully.")
    return redirect("team_list")