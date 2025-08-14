from django.db import models

# Create your models here.
class user_reg(models.Model):
    CHOICES = (
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    Name=models.CharField(max_length=15)
    Email=models.EmailField()
    Username=models.CharField(max_length=15)
    Password=models.IntegerField()
    Phone=models.IntegerField()
    district = models.CharField(max_length=20)
    taluk = models.CharField(max_length=20)
    panchayat = models.CharField(max_length=20)
    ward = models.CharField(max_length=20)
    address = models.CharField(max_length=30)
    status = models.CharField(max_length=10, choices=CHOICES, default='Reject')


class auth_reg(models.Model):
    CHOICES = (
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    section_choice=(
        ('Road','Road'),
        ('Buildings','Buildings'),
        ('Bridges','Bridges'),
        ('Signboard','Signboard'),
        ('Others','Others'),
    )
    SECTION_FEES = {
        'Road': 500,
        'Buildings': 1000,
        'Bridges': 1500,
        'Signboard': 300,
        'Others': 200,
    }


    name=models.CharField(max_length=15)
    Email=models.EmailField()
    auth_name=models.CharField(max_length=15)
    image=models.ImageField()
    uname=models.CharField(max_length=10)
    password=models.IntegerField()
    phone=models.IntegerField()
    status = models.CharField(max_length=10, choices=CHOICES, default='Rejected')
    section= models.CharField(max_length=20, choices=section_choice)

    # Application_fees=models.IntegerField()

# ------------------------
# New Modules (2025-07-07)
# ------------------------

class Feedback(models.Model):
    user = models.ForeignKey(user_reg, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.Username}"

class Complaint(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Resolved', 'Resolved'),
    )

    user = models.ForeignKey(user_reg, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField()
    application_fee=models.IntegerField(default=0)
    AUTH_RESPONSE_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    authority_response = models.CharField(
        max_length=10, choices=AUTH_RESPONSE_CHOICES, default='Pending'
    )
    assigned_to = models.ForeignKey(auth_reg, on_delete=models.SET_NULL, null=True, blank=True)



class ProgressReport(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, null=True, blank=True)
    user_details = models.ForeignKey(user_reg, on_delete=models.CASCADE)
    contractor = models.ForeignKey(auth_reg, on_delete=models.CASCADE)
    description = models.TextField()
    progress_percent = models.PositiveIntegerField()
    image = models.ImageField(upload_to='progress/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class PasswordReset(models.Model):
    user_details = models.ForeignKey(user_reg,on_delete = models.CASCADE)
    token = models.CharField(max_length=255)