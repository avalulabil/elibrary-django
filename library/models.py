from django.db import models

class Book(models.Model):
    STATUS_CHOICES = [
        ('Completed', 'Completed'),
        ('Reading', 'Reading')
    ]
    
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publication_date = models.DateField()
    category = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    score = models.FloatField()
    cover_image = models.ImageField(upload_to='covers/')
    pdf_file = models.FileField(upload_to='pdfs/', null=True, blank=True)

    def __str__(self):
        return self.title
