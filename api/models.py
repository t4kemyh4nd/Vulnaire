from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Project(models.Model):
    name = models.CharField(max_length = 100)

    def __str__(self):
        return self.name

class Domain(models.Model):
    quarter = models.IntegerField(default = 1, validators=[MaxValueValidator(3), MinValueValidator(1)])
    name = models.CharField(max_length = 100)
    department = models.CharField(max_length = 10)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Bug(models.Model):
    #below fields are the main attributes
    title = models.CharField(max_length = 200, blank = False)
    risk = models.CharField(max_length = 10)
    abstract = models.CharField(max_length = 300, blank = False)
    impact = models.CharField(max_length = 400)
    ease_of_exploitation = models.CharField(max_length = 10)
    owasp_category = models.CharField(max_length = 100)
    cvss = models.FloatField(blank = False)
    cwe = models.IntegerField(blank = False)
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    recommendation = models.TextField(blank = False)
    reference = models.TextField(blank = False)
    poc = models.ImageField(upload_to = 'uploads/')
    status = models.CharField(max_length = 10, choices = [('OPEN', 'OPEN'), ('CLOSE', 'CLOSE')], default = 'OPEN')
    date = models.DateField(auto_now_add = True)

    #below fields are the attributes required only for exporting in tracker (csv)
    host_ip = models.CharField(max_length = 100)
    port = models.CharField(max_length = 20)

    def __str__(self):
        return self.title