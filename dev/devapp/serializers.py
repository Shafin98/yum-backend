from rest_framework import serializers
from .models import *


# ==============================================================================
# CONTACT / INBOX
# ==============================================================================

class ContactSerializer(serializers.ModelSerializer):
    service = serializers.SlugRelatedField(
        queryset=Service.objects.filter(is_active=True),
        slug_field="slug",
        required=False,
        allow_null=True
    )

    class Meta:
        model = PostMessage
        fields = [
            "name",
            "email",
            "company",
            "service",
            "message",
        ]


class MessageReadSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(source="service.name", read_only=True)

    class Meta:
        model = PostMessage
        fields = [
            "id",
            "name",
            "email",
            "company",
            "message",
            "is_read",
            "created_at",
            "service",
            "service_name",
        ]


# ==============================================================================
# LOGOS
# ==============================================================================

class ClientLogoSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(read_only=True)

    class Meta:
        model = Logo
        fields = [
            "name",
            "slug",
            "logo",
            "order_no",
        ]


# ==============================================================================
# SOCIAL MEDIA
# ==============================================================================

class SocialMediaAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaAccounts
        fields = [
            "platform",
            "url",
            "icon",
            "username",
            "order_no",
        ]


# ==============================================================================
# TESTIMONIALS
# ==============================================================================

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = [
            "client_name",
            "client_title",
            "client_image",
            "testimonial",
            "rating",
            "order_no",
        ]


# ==============================================================================
# PROJECTS
# ==============================================================================

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "title",
            "slug",
            "type",
            "project_image",
            "website",
            "project_summary",
            "description",
            "created_at",
        ]


# ==============================================================================
# SERVICES — Sub-resource serializers
# ==============================================================================

class ServiceProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProcess
        fields = ["title", "description", "order_no"]


class ServiceGallerySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ServiceGallery
        fields = ["id", "type", "src", "caption", "order_no"]


class ServiceDeliverableSerializer(serializers.ModelSerializer):
    """Returns a flat string list — just the name value."""
    class Meta:
        model = ServiceDeliverable
        fields = ["name"]

    def to_representation(self, instance):
        return instance.name


class ServiceToolSerializer(serializers.ModelSerializer):
    """Returns a flat string list — just the name value."""
    class Meta:
        model = ServiceTool
        fields = ["name"]

    def to_representation(self, instance):
        return instance.name


class ServicePricingFeatureSerializer(serializers.ModelSerializer):
    """Returns a flat string list — just the feature value."""
    class Meta:
        model = ServicePricingFeature
        fields = ["feature"]

    def to_representation(self, instance):
        return instance.feature


class ServicePricingTierSerializer(serializers.ModelSerializer):
    """
    Matches spec shape:
    {
        "id": "basic",
        "name": "Basic",
        "price": 1597,
        "tagline": "Ideal for startups",
        "features": ["Single Page", "Responsive Design"],
        "deliveryDays": 9,
        "revisions": 5,
        "highlight": false
    }
    """
    id = serializers.IntegerField(read_only=True)
    deliveryDays = serializers.IntegerField(source="delivery_days")
    features = ServicePricingFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = ServicePricingTier
        fields = [
            "id",
            "name",
            "tagline",
            "price",
            "deliveryDays",
            "revisions",
            "highlight",
            "features",
        ]


class ServiceReviewSerializer(serializers.ModelSerializer):
    """
    Matches spec shape:
    {
        "id": 1,
        "author": "Mark Fritsch",
        "role": "Corporate Branding Administrator",
        "company": "Mills - Hartmann",
        "rating": 4,
        "text": "The execution was excellent.",
        "date": "Tue Jun 16 2026"
    }
    """
    id = serializers.IntegerField(read_only=True)
    author = serializers.CharField(source="client_name")
    role = serializers.CharField(source="client_title")
    company = serializers.CharField(source="client_company", default=None)
    text = serializers.CharField(source="testimonial")
    date = serializers.DateField(source="review_date", format="%a %b %d %Y", allow_null=True)

    class Meta:
        model = ServiceReview
        fields = [
            "id",
            "author",
            "role",
            "company",
            "rating",
            "text",
            "date",
        ]


class ServiceRelatedSerializer(serializers.ModelSerializer):
    """
    Matches spec shape:
    {
        "slug": "branding",
        "name": "Strategic Brand Identity",
        "image": "https://cdn.site.com/services/branding.jpg"
    }
    """
    slug = serializers.CharField(source="related_service.slug", read_only=True)
    name = serializers.CharField(source="related_service.name", read_only=True)
    image = serializers.ImageField(source="related_service.cover", read_only=True)

    class Meta:
        model = ServiceRelated
        fields = ["slug", "name", "image"]


# ==============================================================================
# SERVICES — List & Detail serializers
# ==============================================================================

class ServiceMetaSerializer(serializers.ModelSerializer):
    """
    Nested 'meta' object matching spec:
    {
        "rating": 4.92,
        "reviewCount": 202,
        "priceFrom": 215,
        "deliveryDays": 8,
        "badges": ["Popular", "Fast Delivery"]
    }
    """
    reviewCount = serializers.IntegerField(source="review_count")
    priceFrom = serializers.DecimalField(source="price_from", max_digits=10, decimal_places=2)
    deliveryDays = serializers.IntegerField(source="delivery_days")
    badges = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = ["rating", "reviewCount", "priceFrom", "deliveryDays", "badges"]

    def get_badges(self, obj):
        return list(obj.badges.values_list("badge", flat=True))


# Full detail serializer — base service info + meta (no sub-resources; those have dedicated endpoints)
class ServiceDetailSerializer(serializers.ModelSerializer):
    """
    Matches spec shape for GET /api/v1/portfolio/services/{slug}/:
    {
        "name": "logo design",
        "slug": "logo-design",
        "description": "...",
        "cover": "https://...",
        "timeline": "3-7 weeks",
        "pitch": "...",
        "meta": { "rating": 4.92, "reviewCount": 202, ... }
    }
    """
    meta = ServiceMetaSerializer(source="*", read_only=True)

    class Meta:
        model = Service
        fields = [
            "name",
            "slug",
            "description",
            "cover",
            "pitch",
            "timeline",
            "created_at",
            "meta",
        ]


# List serializer — lightweight card view
class ServiceListSerializer(serializers.ModelSerializer):
    meta = ServiceMetaSerializer(source="*", read_only=True)

    class Meta:
        model = Service
        fields = [
            "name",
            "slug",
            "description",
            "cover",
            "meta",
        ]


# ==============================================================================
# ABOUT US
# ==============================================================================

class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = [
            "heading",
            "subheading",
            "story_title",
            "story_description",
            "projects_completed",
            "happy_clients",
            "years_experience",
            "team_members_count",
            "mission",
            "vision",
        ]


# ==============================================================================
# VALUES
# ==============================================================================

class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = [
            "title",
            "description",
            "icon",
            "order_no",
        ]


# ==============================================================================
# TEAM MEMBERS
# ==============================================================================

class TeamMemberSerializer(serializers.ModelSerializer):
    # Model field is `order`, not `order_no` — map it correctly
    order_no = serializers.IntegerField(source="order", read_only=True)

    class Meta:
        model = TeamMember
        fields = [
            "name",
            "designation",
            "image",
            "order_no",
        ]