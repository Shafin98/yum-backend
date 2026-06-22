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
            "type",           # now a plain CharField, no source remapping needed
            "project_image",
            "website",
            "project_summary",
            "description",
            "created_at",
        ]


# ==============================================================================
# SERVICES  (replaces CategoryPublicSerializer)
# ==============================================================================

class ServiceBadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceBadge
        fields = ["badge"]


class ServiceProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceProcess
        fields = ["title", "description", "order_no"]


class ServiceGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceGallery
        fields = ["type", "src", "caption", "order_no"]


class ServiceDeliverableSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceDeliverable
        fields = ["name", "order_no"]


class ServiceToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceTool
        fields = ["name", "order_no"]


class ServicePricingFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicePricingFeature
        fields = ["feature", "order_no"]


class ServicePricingTierSerializer(serializers.ModelSerializer):
    features = ServicePricingFeatureSerializer(many=True, read_only=True)

    class Meta:
        model = ServicePricingTier
        fields = [
            "name",
            "tagline",
            "price",
            "delivery_days",
            "revisions",
            "highlight",
            "order_no",
            "features",
        ]


class ServiceReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceReview
        fields = [
            "client_name",
            "client_title",
            "client_image",
            "testimonial",
            "rating",
            "review_date",
        ]


class ServiceRelatedSerializer(serializers.ModelSerializer):
    """Lightweight nested serializer — avoids infinite recursion."""
    name = serializers.CharField(source="related_service.name", read_only=True)
    slug = serializers.CharField(source="related_service.slug", read_only=True)
    cover = serializers.ImageField(source="related_service.cover", read_only=True)

    class Meta:
        model = ServiceRelated
        fields = ["name", "slug", "cover"]


# Full detail serializer — used on the service detail endpoint
class ServiceDetailSerializer(serializers.ModelSerializer):
    badges = ServiceBadgeSerializer(many=True, read_only=True)
    process_steps = ServiceProcessSerializer(many=True, read_only=True)
    gallery = ServiceGallerySerializer(many=True, read_only=True)
    deliverables = ServiceDeliverableSerializer(many=True, read_only=True)
    tools = ServiceToolSerializer(many=True, read_only=True)
    pricing_tiers = ServicePricingTierSerializer(many=True, read_only=True)
    reviews = ServiceReviewSerializer(many=True, read_only=True)
    related_services = ServiceRelatedSerializer(source="related_from", many=True, read_only=True)

    class Meta:
        model = Service
        fields = [
            "name",
            "slug",
            "description",
            "cover",
            "pitch",
            "timeline",
            "rating",
            "review_count",
            "price_from",
            "delivery_days",
            "created_at",
            # nested
            "badges",
            "process_steps",
            "gallery",
            "deliverables",
            "tools",
            "pricing_tiers",
            "reviews",
            "related_services",
        ]


# List serializer — lightweight, no nested children
class ServiceListSerializer(serializers.ModelSerializer):
    badges = ServiceBadgeSerializer(many=True, read_only=True)

    class Meta:
        model = Service
        fields = [
            "name",
            "slug",
            "description",
            "cover",
            "rating",
            "review_count",
            "price_from",
            "delivery_days",
            "badges",
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
            "mission",   # NEW
            "vision",    # NEW
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
            "order_no",  # NEW
        ]


# ==============================================================================
# TEAM MEMBERS
# ==============================================================================

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = [
            "name",
            "designation",
            "image",
            "order_no",  # renamed from order
        ]