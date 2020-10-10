from rest_framework import serializers
from .models import Project, Domain, Bug


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name']

class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ['id', 'quarter', 'name', 'department', 'project']

class BugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bug
        fields = ['id', 'title', 'risk', 'abstract', 'impact', 'ease_of_exploitation', 'owasp_category', 'cvss', 'cwe', 'domain', 'recommendation', 'poc', 'date']