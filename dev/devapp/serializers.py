from rest_framework import serializers
from .models import * # import all models


class ContactSerializer(serializers.ModelSerializer):
    service = serializers.SlugRelatedField(
        queryset=Category.objects.filter(is_active=True),
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
            "message"
        ]

class MessageReadSerializer(serializers.ModelSerializer):
    service_name = serializers.CharField(
        source="service.name",
        read_only=True
    )

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

class ClientLogoSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(read_only=True)

    class Meta:
        model = Logo
        fields = [
            "name", 
            "slug", 
            "logo",
        ]

class SocialMediaAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaAccounts
        fields = [
            "platform",
            "url",
            "icon",
        ]

class TestimonialSerializer(serializers.ModelSerializer):
    
    client_title = serializers.CharField(read_only=True)

    company_logo = serializers.ImageField(
        source="company_logo.logo",
        read_only=True
    )

    class Meta:
        model = Testimonial
        fields = [
            "client_name",
            "client_title",
            "company_name",
            "company_logo",
            "client_image",
            "testimonial",
            "rating",
        ]
        
class ProjectSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source="type.name", read_only=True)

    class Meta:
        model = Project
        fields = [
            "title",
            "type",
            "project_image",
            "website",
            "project_summary",
            "description",
        ]

class CategoryPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "name",
            "slug",
            "description",
        ]

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
        ]


class ValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Value
        fields = [
            "title",
            "description",
            "icon",
        ]


class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = [
            "name",
            "designation",
            "image",
            "order",
        ]