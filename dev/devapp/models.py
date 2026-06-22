from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
# ---------------------------------ADIMN USE------------------------------------
class Service(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    cover = models.ImageField(upload_to='services/covers/')       # NEW
    pitch = models.TextField()                                     # NEW
    timeline = models.CharField(max_length=100)                   # NEW
    rating = models.DecimalField(max_digits=3, decimal_places=1)  # NEW
    review_count = models.PositiveIntegerField(default=0)         # NEW
    price_from = models.DecimalField(max_digits=10, decimal_places=2)  # NEW
    delivery_days = models.PositiveIntegerField()                  # NEW
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True
    )

    class Meta:
        db_table = 'services'
        
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        original_slug = self.slug
        counter = 1
        while Service.objects.filter(slug=self.slug).exclude(pk=self.pk):
            self.slug = f"{original_slug}-{counter}"
            counter += 1

        super().save(*args, **kwargs)

class ServiceBadge(models.Model):
    """
    Examples: Popular, Top Rated, Fast Delivery, Expert Verified
    Relationship: Service → Many Badges
    """
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='badges')
    badge = models.CharField(max_length=100)
 
    class Meta:
        db_table = 'service_badges'
 
    def __str__(self):
        return f"{self.service.name} — {self.badge}"
    
class ServiceProcess(models.Model):
    """
    Relationship: Service → Many Process Steps
    """
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='process_steps')
    title = models.CharField(max_length=200)
    description = models.TextField()
    order_no = models.PositiveIntegerField(default=0)
 
    class Meta:
        db_table = 'service_processes'
        ordering = ['order_no']
 
    def __str__(self):
        return f"{self.service.name} — Step {self.order_no}: {self.title}"
    
class ServiceGallery(models.Model):
    """
    Supported media: image, video
    Relationship: Service → Many Gallery Items
    """
    MEDIA_TYPE_CHOICES = [
        ("image", "Image"),
        ("video", "Video"),
    ]
 
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='gallery')
    type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    src = models.URLField()
    caption = models.CharField(max_length=255, blank=True, null=True)
    order_no = models.PositiveIntegerField(default=0)
 
    class Meta:
        db_table = 'service_gallery'
        ordering = ['order_no']
 
    def __str__(self):
        return f"{self.service.name} — {self.type} #{self.order_no}"
    
class ServiceDeliverable(models.Model):
    """
    Relationship: Service → Many Deliverables
    """
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='deliverables')
    name = models.CharField(max_length=200)
    order_no = models.PositiveIntegerField(default=0)
 
    class Meta:
        db_table = 'service_deliverables'
        ordering = ['order_no']
 
    def __str__(self):
        return f"{self.service.name} — {self.name}"
    
class ServiceTool(models.Model):
    """
    Relationship: Service → Many Tools
    """
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='tools')
    name = models.CharField(max_length=200)
    order_no = models.PositiveIntegerField(default=0)
 
    class Meta:
        db_table = 'service_tools'
        ordering = ['order_no']
 
    def __str__(self):
        return f"{self.service.name} — {self.name}"
    
class ServicePricingTier(models.Model):
    """
    Examples: Basic, Professional, Enterprise
    Relationship: Service → Many Pricing Tiers
    """
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='pricing_tiers')
    name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_days = models.PositiveIntegerField()
    revisions = models.CharField(max_length=100)  # e.g. "3", "Unlimited"
    highlight = models.BooleanField(default=False)
    order_no = models.PositiveIntegerField(default=0)
 
    class Meta:
        db_table = 'service_pricing_tiers'
        ordering = ['order_no']
 
    def __str__(self):
        return f"{self.service.name} — {self.name}"
    
class ServicePricingFeature(models.Model):
    """
    Relationship: Pricing Tier → Many Features
    """
    pricing_tier = models.ForeignKey(
        ServicePricingTier, on_delete=models.CASCADE, related_name='features'
    )
    feature = models.CharField(max_length=255)
    order_no = models.PositiveIntegerField(default=0)
 
    class Meta:
        db_table = 'service_pricing_features'
        ordering = ['order_no']
 
    def __str__(self):
        return f"{self.pricing_tier.name} — {self.feature}"
    
class ServiceReview(models.Model):
    """
    Per-service client reviews (separate from global Testimonials).
    Relationship: Service → Many Reviews
    Rating range: 1–5
    """
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='reviews')
    client_name = models.CharField(max_length=200)
    client_title = models.CharField(max_length=100)
    client_image = models.URLField()
    testimonial = models.TextField()
    rating = models.PositiveSmallIntegerField(help_text="Rating out of 5 (1–5)")
    review_date = models.DateField(blank=True, null=True)
 
    class Meta:
        db_table = 'service_reviews'
 
    def __str__(self):
        return f"{self.service.name} — Review by {self.client_name}"
    
class ServiceRelated(models.Model):
    """
    Many-to-many self-referential relationship between services.
    Example: Web Design → Branding, Web Design → SEO
    """
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name='related_from'
    )
    related_service = models.ForeignKey(
        Service, on_delete=models.CASCADE, related_name='related_to'
    )
 
    class Meta:
        db_table = 'service_related'
        unique_together = ('service', 'related_service')
 
    def __str__(self):
        return f"{self.service.name} → {self.related_service.name}"
    
class PostMessage(models.Model):
    name = models.CharField(max_length=100,db_index=True)
    email = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, null=True)
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
    order_no = models.PositiveIntegerField(default=0)  # NEW FIELD
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'client_logos'
        ordering = ['order_no']
 
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
    client_title = models.CharField(max_length=50)        # was blank/null — now required per spec
    client_image = models.ImageField(upload_to='testimonials/')  # was blank/null — now required per spec
    testimonial = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5, help_text="Rating out of 5 (1–5)")
    order_no = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'testimonials'
        ordering = ["order_no"]

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
    # type is now a plain string (e.g. "ecommerce", "branding") instead of FK to Category
    type = models.CharField(max_length=100)
    project_image = models.ImageField(upload_to='projects/')
    website = models.URLField(blank=True, null=True)
    project_summary = models.TextField()
    description = models.TextField()
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
        ("behance", "Behance"),    # NEW
        ("dribbble", "Dribbble"),  # NEW
    ]

    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES, unique=True)
    icon = models.CharField(max_length=50, default='Unknown')
    url = models.URLField()
    username = models.CharField(max_length=100, blank=True, null=True)  # NEW FIELD
    is_active = models.BooleanField(default=True)
    order_no = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'social_media'
        ordering = ['order_no']

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

    # NEW FIELDS
    mission = models.TextField(blank=True, null=True)
    vision = models.TextField(blank=True, null=True)
 
    class Meta:
        db_table = 'about'
        verbose_name = 'About Us'
        verbose_name_plural = 'About Us'

    def __str__(self):
        return "About Us Section"

# This is company value    
class Value(models.Model):
    icon = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    description = models.TextField()
    order_no = models.PositiveIntegerField(default=0) # NEW FIELD

    class Meta:
        db_table = 'values'
        ordering = ['order_no']

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
        db_table = 'team_members'
        ordering = ['order']
