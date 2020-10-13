from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Project, Domain, Bug
from .serializers import ProjectSerializer, DomainSerializer, BugSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes

#this view is for viewing all projects or creating a project
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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

#this view is for viewing / updating vulnerabilities in the domain of a project using project ID and domain ID
@api_view(['GET', 'PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
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

#view for generation of excel report for each domain
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def generate_csv_by_domain_id(request, pk, dk):
    try:
        Project.objects.get(id = pk)
    except Project.DoesNotExist:
        return HttpResponse("Project not found", status = 404)
    
    try:
        domain = Domain.objects.get(id = dk)
    except Domain.DoesNotExist:
        return HttpResponse("Domain not found", status = 404)

    bugs = Bug.objects.filter(domain_id = dk)

    csv_columns = "S.no., Department, URL, Host-IP/Device Name, Open Port, Vulnerability title, CVSS / CWE, POCs, Q3 Vulnerability Status, Owasp category, Observation, Impact, Recommendation, Risk Rating, Ease of exploition, Reported source of Vulnerability (Reference)"

    file_contents = csv_columns + "\n"

    s_no = 1

    for bug in bugs:
        array = [str(s_no), domain.department, str(bug.domain), bug.host_ip, bug.port, bug.title, str(bug.cvss) + "/" + str(bug.cwe) , "<add-poc-here>", bug.status, bug.owasp_category, bug.abstract, bug.impact, bug.recommendation, bug.risk, bug.ease_of_exploitation, bug.reference]
        file_contents += ",".join(array) + "\n"
        s_no += 1

    response = HttpResponse(file_contents, status = 200, content_type = "text/csv")
    response['Content-Disposition'] = 'attachment; filename="VA TRACKER ' + str(domain.name) + '.csv"'
    return response


@api_view(['GET'])
def generate_word_report_by_domain_id(request, pk, dk):
    #code to generate word report with all bugs here
    pass