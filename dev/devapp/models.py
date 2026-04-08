from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
# ---------------------------------ADIMN USE------------------------------------
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        original_slug = self.slug
        counter = 1
        while Category.objects.filter(slug=self.slug).exclude(pk=self.pk):
            self.slug = f"{original_slug}-{counter}"
            counter += 1

        super().save(*args, **kwargs)

    class Meta:
        db_table = 'services'
    def __str__(self):
        return self.name
    
class PostMessage(models.Model):
    name = models.CharField(max_length=100,db_index=True)
    email = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True, null=True)
    service = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'inbox'
    def __str__(self):
        return self.name 

class Logo(models.Model):
    name = models.CharField(max_length=150, unique=True, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    logo = models.ImageField(upload_to='client_logos/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'logo'
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Logo.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Testimonial(models.Model):
    client_name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    client_title = models.CharField(max_length=50, blank=True, null=True)
    company_name = models.CharField(max_length=150, blank=True, null=True)
    company_logo = models.ForeignKey(Logo, on_delete=models.SET_NULL, blank=True, null=True)
    client_image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    rating = models.PositiveSmallIntegerField(default=5, help_text="Rating out of 5")
    testimonial = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'client_information'
        ordering = ["order"]

    def __str__(self):
        return self.client_name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.client_name)
            slug = base_slug
            counter = 1
            while Testimonial.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
class Project(models.Model):
    title = models.CharField(max_length=150, unique=True, db_index=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    type = models.ForeignKey(Category, on_delete=models.CASCADE)
    project_image = models.ImageField(upload_to='projects/')
    website = models.URLField(blank=True, null=True)
    project_summary = models.TextField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'projects'

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Project.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

class SocialMediaAccounts(models.Model):
    PLATFORM_CHOICES = [
        ("facebook", "Facebook"),
        ("instagram", "Instagram"),
        ("twitter", "Twitter / X"),
        ("linkedin", "LinkedIn"),
        ("github", "GitHub"),
        ("youtube", "YouTube"),
        ("tiktok", "TikTok"),
    ]

    platform = models.CharField(max_length=50,choices=PLATFORM_CHOICES,unique=True)
    url = models.URLField()
    icon = models.CharField(max_length=50, default='Unknown')
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'media_accounts'

    def __str__(self):
        return self.platform
    
class AboutUs(models.Model):
    heading = models.CharField(max_length=200, default="We Are YUM Studio")
    subheading = models.TextField()

    story_title = models.CharField(max_length=100, default="Our Story")
    story_description = models.TextField()

    projects_completed = models.PositiveIntegerField(default=0)
    happy_clients = models.PositiveIntegerField(default=0)
    years_experience = models.PositiveIntegerField(default=0)
    team_members_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "About Us Section"

# This is company value    
class Value(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.title
    
class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team/')
    order = models.PositiveIntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
