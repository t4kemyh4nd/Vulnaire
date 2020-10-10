from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Project, Domain, Bug
from .serializers import ProjectSerializer, DomainSerializer, BugSerializer

#this view is for viewing all projects or creating a project
@api_view(['GET', 'POST'])
def get_create_projects(request):
    try:
        projects = Project.objects.all()
    except Project.DoesNotExist: 
        return HttpResponse("Project not found", status = 404)

    if request.method == 'GET':
        serializer = ProjectSerializer(projects, many = True)
        return JsonResponse(serializer.data, status = 200, safe = False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProjectSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)
        return JsonResponse(serializer.errors, status = 400)

#this view is for getting / deleting a project by its id
@api_view(['GET', 'DELETE'])
def get_delete_project_by_id(request, pk):
    try:
        project = Project.objects.get(id = pk)
    except Project.DoesNotExist:
        return HttpResponse("Project not found", status = 404)

    if request.method == 'GET':
        serializer = ProjectSerializer(project)
        return JsonResponse(serializer.data, status = 200, safe = False)

    elif request.method == 'DELETE':
        project.delete()
        return JsonResponse(status = 404)

#this view is for getting all domains in a project
@api_view(['GET', 'POST'])
def get_add_domains_in_project(request, pk):
    try:
        Project.objects.get(id = pk)
    except Project.DoesNotExist:
        return HttpResponse("Project not found", status = 404)
    
    try:
        domains = Domain.objects.filter(project_id = pk)
    except Domain.DoesNotExist:
        return HttpResponse("No domains found", status = 404)

    if request.method == 'GET':
        serializer = DomainSerializer(domains, many = True)
        return JsonResponse(serializer.data, status = 200, safe = False)
    
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = DomainSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)
        return JsonResponse(serializer.errors, status = 400)

#this view is for getting / deleting domains in a project by the project ID and the domain ID
@api_view(['GET', 'DELETE'])
def get_delete_domain_in_project_by_id(request, pk, dk):
    try:
        Project.objects.get(id = pk)
    except Project.DoesNotExist:
        return HttpResponse("Project not found", status = 404)
    
    try:
        domain = Domain.objects.get(project_id = pk, id = dk)
    except Domain.DoesNotExist:
        return HttpResponse("No domains found", status = 404)
    
    if request.method == 'GET':
        serializer = DomainSerializer(domain)
        return JsonResponse(serializer.data, status = 200, safe = False)

    elif request.method == 'DELETE':
        domain.delete()
        return HttpResponse("Domain deleted", status = 404)

#this view is for getting / creating vulnerabilities in the domain of a project using project ID and domain ID    
@api_view(['GET', 'POST'])
def get_add_vulns_in_domain_by_id(request, pk, dk):
    try:
        Project.objects.get(id = pk)
    except Project.DoesNotExist:
        return HttpResponse("Project not found", status = 404)
    
    try:
        Domain.objects.get(project_id = pk, id = dk)
    except Domain.DoesNotExist:
        return HttpResponse("No domains found", status = 404)

    try:
        bugs = Bug.objects.filter(domain_id = dk)
    except Bug.DoesNotExist:
        return HttpResponse("No vulnerabilities found", status = 404)
    
    if request.method == 'GET':
        serializer = BugSerializer(bugs, many = True)
        return JsonResponse(serializer.data, status = 200, safe = False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = BugSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 201)
        return JsonResponse(serializer.errors, status = 400)

#this view is for viweing / updating vulnerabilities in the domain of a project using project ID and domain ID
@api_view(['GET', 'PATCH'])
def get_update_vulns_by_id(request, pk, dk, vk):
    try:
        Project.objects.get(id = pk)
    except Project.DoesNotExist:
        return HttpResponse("Project not found", status = 404)
    
    try:
        Domain.objects.get(project_id = pk, id = dk)
    except Domain.DoesNotExist:
        return HttpResponse("No domains found", status = 404)

    try:
        bug = Bug.objects.get(id = vk)
    except Bug.DoesNotExist:
        return HttpResponse("No vulnerabilities found", status = 404)
    
    if request.method == 'GET':
        serializer = BugSerializer(bug)
        return JsonResponse(serializer.data, status = 200, safe = False)
    
    elif request.method == 'PATCH':
        data = JSONParser().parse(request)
        serializer = BugSerializer(bug, data = data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status = 200, safe = False)
        return HttpResponse("Invalid data", status = 400)

@api_view(['GET'])
def generate_word_report_for_domain(request, pk, dk):
    #code to generate word report with all bugs here
    pass