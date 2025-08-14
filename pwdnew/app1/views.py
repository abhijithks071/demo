from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from.models import *

# Create your views here.
def index(re):
    return render(re,'index.html')

def contact(re):
    return render(re,'contact.html')



def registration(re):
    if re.method=='POST':
        a=re.POST['Name']
        b=re.POST['Email']
        c=re.POST['Username']
        d=int(re.POST['Password'])
        e=int(re.POST['Phone'])
        dic=re.POST['district']
        tal=re.POST['taluk']
        pan=re.POST['panchayat']
        war=re.POST['ward']
        add=re.POST['address']

        data=user_reg.objects.create(Name=a,Email=b,Username=c,Password=d,Phone=e,district=dic,taluk=tal,panchayat=pan,ward=war,address=add)
        data.save()
        return HttpResponse('Registration completed .Wait for approval ')
    return render(re,'registration.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('Username')
        password =int(request.POST.get('Password')) # Treat as string, not int

        if not username or not password:
            return HttpResponse('Username and password are required.')

        # Admin Login
        if username == 'admin' and password == 12345:
            request.session['admin'] = True
            return redirect(adminhome)

        # User Login
        try:
            user = user_reg.objects.get(Username=username)
            if user.Password == password:
                request.session['user'] = username
                return redirect(userhome)
            else:
                return HttpResponse('Incorrect password')
        except user_reg.DoesNotExist:
            pass  # continue checking auth_reg

        # Authority Login
        try:
            auth_user = auth_reg.objects.get(uname=username)
            if auth_user.password == password:
                request.session['authid'] = username
                return redirect(authorityhome)
            else:
                return HttpResponse('Incorrect password')
        except auth_reg.DoesNotExist:
            return HttpResponse('Invalid username')

    return render(request,'login.html')

# def auth_login(re):
#     return render(re,'auth_login.html')

def adminhome(re):
    if 'admin' in re.session:
        return render(re,'adminhome.html')
    return redirect(login)


def userhome(re):
    if 'user' in re.session:
        return render(re,'userhome.html')
    return redirect(login)

def authorityhome(re):
    if 'authority' in re.session:
        return render(re,'authorityhome.html')
    return redirect(login)

#
# def complaints(re):
#     return render(re,'complaints.html')

def authority_reg(re):
    if re.method=='POST':
        f=re.POST['name']
        g=re.POST['Email']
        h=re.POST['auth_name']
        i=re.POST['image']
        j=re.POST['uname']
        k=int(re.POST['password'])
        l=int(re.POST['phone'])
        m=re.POST['section']
        data=auth_reg.objects.create(name=f,Email=g,auth_name=h,image=i,uname=j,password=k,phone=l,section=m)
        data.save()
        return HttpResponse('Registration completed .Wait for approval')
    return render(re,'authority_reg.html')


def auth_log(re):
        if re.method == 'POST':
            j = re.POST['uname']
            k = int(re.POST['password'])
            data = auth_reg.objects.get(uname=j)
            if data.status== 'Approve' :
                if j == data.uname and k == data.password:
                    re.session['authority'] = j
                    return redirect(authorityhome)
                else:
                    return HttpResponse('Incorrect password')
            else:
                return HttpResponse('is NOT APPROVED')

        return render(re, 'auth_login.html')



# def view_comp(request):
#     if 'authority' not in request.session:
#         return HttpResponse('Unauthorized', status=401)
#
#     auth = auth_reg.objects.get(uname=request.session['authority'])  # ✅ fix here
#     complaints = Complaint.objects.filter(assigned_to=auth).order_by('-created_at')
#     return render(request, 'view_comp.html', {'data': complaints})
def view_comp(request):
    if 'authority' not in request.session:
        return HttpResponse('Unauthorized', status=401)

    auth = auth_reg.objects.get(uname=request.session['authority'])  # or use id if stored
    if request.method == 'POST':
        comp_id = request.POST.get('complaint_id')
        action = request.POST.get('action')  # "Accept" or "Reject"

        try:
            complaint = Complaint.objects.get(id=comp_id, assigned_to=auth)
            if action == 'Accept':
                complaint.authority_response = 'Accepted'
            elif action == 'Reject':
                complaint.authority_response = 'Rejected'
            complaint.save()
        except Complaint.DoesNotExist:
            pass

        return redirect(view_comp)  # reload page

    complaints = Complaint.objects.filter(assigned_to=auth).order_by('-created_at')
    return render(request, 'view_comp.html', {'data': complaints})






def add_workers(re,id):
    if 'admin' not in re.session:
        return HttpResponse('Unauthorized', status=401)
    if re.method == 'POST':
        status = re.POST.get('status')
        try:
            a_w = auth_reg.objects.get(id=id)
            a_w.status = status
            a_w.save()
        except Complaint.DoesNotExist:
            pass
    add = auth_reg.objects.all()
    return render(re, 'add_workers.html', {'data': add})


    # if request.method == 'POST':
    #     username = request.POST.get('uname')
    #     password =int(request.POST.get('password'))
    #
    #     if not username or not password:
    #         return HttpResponse('Username and password are required.')
    #     try:
    #         auth_user = auth_reg.objects.get(uname=username)
    #         if auth_user.password == password:
    #             request.session['authid'] = username
    #             return redirect(authorityhome)
    #         else:
    #             return HttpResponse('Incorrect password')
    #     except auth_reg.DoesNotExist:
    #         return HttpResponse('Invalid username')
    #
    # return render(request, 'login.html')



#     if re.method=='POST':
#         j=re.POST['uname']
#         k=re.POST['password']
#         try:
#             data=auth_reg.objects.get(uname=j)
#             if data.password==k:
#                 re.session['uname']=j
#                 return redirect(authorityhome)
#             else:
#                 return HttpResponse('INVALID USERNAME')
#         except:
#             return render(re,'login.html')




def edit_profile(request):
    if 'user' not in request.session:
        return HttpResponse("can't find user details")  # or wherever your login is

    username = request.session['user']
    user = user_reg.objects.get(Username=username)

    if request.method == 'POST':
        user.Name = request.POST['Name']
        user.Email = request.POST['Email']
        user.Phone = request.POST['Phone']
        user.district = request.POST['district']
        user.taluk = request.POST['taluk']
        user.panchayat = request.POST['panchayat']
        user.ward = request.POST['ward']
        user.address = request.POST['address']
        user.save()
        return HttpResponse('Profile updated successfully.')

    return render(request, 'edit_profile.html', {'user': user})




def about(re):
    return render(re,'about.html')

def about_admin(re):
    return render(re,'about_admin.html')

def about_user(re):
    return render(re,'about_user.html')


def user_data(re):
    data=user_reg.objects.all()
    return render(re,'user_details.html',{'data':data})





def logout(re):
    if 'user' in re.session or 'admin' in re.session:
        re.session.flush()
        return redirect(index)
    return redirect(login)

# ------------------------
# ------------------------
from django.utils import timezone
from .models import Feedback, Complaint, ProgressReport

# ---- Feedback ----
def feedback_submit(request):
    # Citizen submits feedback
    if 'user' not in request.session:
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        message = request.POST.get('message')
        user = user_reg.objects.get(Username=request.session['user'])
        Feedback.objects.create(user=user, message=message)
        return redirect('feedback')
    return render(request, 'feedback.html')

def feedback_list(request):
    # Admin views feedback
    if 'admin' not in request.session or 'authority' not in request.session:
        return HttpResponse('Unauthorized', status=401)

    data = Feedback.objects.all().order_by('-created_at')
    auth = auth_reg.objects.all()
    return render(request, 'feedback_list.html', {'data': data,'auth': auth})



# ---- Complaint ----
def complaint_submit(request):
    user = user_reg.objects.get(Username=request.session['user'])
    if 'user' not in request.session:
        return HttpResponse('Unauthorized', status=401)
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        image = request.POST.get('image')

        user = user_reg.objects.get(Username=request.session['user'])
        Complaint.objects.create(user=user,subject=subject, message=message,image=image).save()
        return HttpResponse("saved")
    return render(request, 'complaints.html',{'user':user})

# def complaint_list_user(request):
#     # Admin views / updates complaints
#     if 'user' not in request.session:
#         return HttpResponse('Unauthorized', status=401)
#     user= user_reg.objects.get(Username=request.session['user'])
#     comps = ProgressReport.objects.filter(user_details=user)
#     return render(request, 'complaint_list_user.html', {'data': comps})

def complaint_list_user(request):
    if 'user' not in request.session:
        return HttpResponse('Unauthorized', status=401)
    user = user_reg.objects.get(Username=request.session['user'])
    complaints = Complaint.objects.filter(user=user).order_by('-created_at').prefetch_related('progressreport_set')
    return render(request, 'complaint_list_user.html', {'data': complaints})





# ------------------------------------------------------------------

def complaint_list(request):
    if request.method == "POST":
        complaint_id = request.POST.get("id")
        authority_id = request.POST.get("authority")

        if complaint_id and authority_id:
            complaint = get_object_or_404(Complaint, id=complaint_id)
            authority = get_object_or_404(auth_reg, id=authority_id)
            complaint.assigned_to = authority
            complaint.save()

            messages.success(request, "Authority assigned successfully.")
        return redirect(complaint_list)

    comps = Complaint.objects.all().order_by('-created_at')
    auth = auth_reg.objects.all()

    # Add expected fee for template usage
    for complaint in comps:
        if complaint.assigned_to:
            section = complaint.assigned_to.section
            complaint.expected_fee = auth_reg.SECTION_FEES.get(section, 0)
        else:
            complaint.expected_fee = 0

    return render(request, 'complaint_list.html', {
        'data': comps,
        'auth': auth
    })



# ---- Progress Report ----
def progress_submit(request):
    if 'authority' not in request.session:
        return HttpResponse('Unauthorized', status=401)

    auth = auth_reg.objects.get(uname=request.session['authority'])

    if request.method == 'POST':
        complaint_id = request.POST.get('complaint_id')  # Get complaint ID from form
        if not complaint_id:
            return HttpResponse("Complaint ID missing", status=400)

        try:
            complaint = Complaint.objects.get(id=complaint_id)
            user_details = complaint.user
        except Complaint.DoesNotExist:
            return HttpResponse("Complaint not found", status=404)

        description = request.POST.get('description')
        percent = int(request.POST.get('percent', 0))
        image = request.FILES.get('image')
        contractor = auth  # same as authority logged in

        ProgressReport.objects.create(
            complaint=complaint,  # <-- link to complaint here
            user_details=user_details,
            contractor=contractor,
            description=description,
            progress_percent=percent,
            image=image
        )
        return redirect(progress_submit)

    complaints = Complaint.objects.filter(assigned_to=auth).order_by('-created_at')
    return render(request, 'progress_report.html', {'data': complaints})



def progress_list(request):
    if 'admin' not in request.session:
        return HttpResponse('Unauthorized', status=401)

    if request.method == 'POST':
        progress_report_id = request.POST.get('id')
        new_status = request.POST.get('status')

        if progress_report_id and new_status:
            progress_report = get_object_or_404(ProgressReport, id=progress_report_id)
            complaint = progress_report.complaint  # or whatever FK field name is
            complaint.status = new_status
            complaint.save()

    reports = ProgressReport.objects.all().order_by('-created_at')
    return render(request, 'progress_list.html', {'data': reports})



import razorpay


def make_payment(request, complaint_id):
    complaint = get_object_or_404(Complaint, pk=complaint_id)

    if not complaint.assigned_to:
        return HttpResponse("No authority assigned.")

    section = complaint.assigned_to.section
    expected_fee = complaint.assigned_to.SECTION_FEES.get(section, 0)

    if complaint.application_fee == expected_fee and expected_fee > 0:
        return HttpResponse("Payment already completed.")

    client = razorpay.Client(auth=("rzp_test_SROSnyInFv81S4", "WIWYANkTTLg7iGbFgEbwj4BM"))

    payment = client.order.create({
        'amount': expected_fee * 100,
        'currency': 'INR',
        'payment_capture': '1'
    })

    context = {
        'complaint': complaint,
        'order_id': payment['id'],
        'amount': payment['amount'],
        'display_amount': expected_fee,
        'razorpay_key': "rzp_test_SROSnyInFv81S4",
    }
    return render(request, 'payment.html', context)





def payment_success(request):
    if request.method == 'POST':
        complaint_id = request.POST.get('complaint_id')
        amount = request.POST.get('amount')

        if complaint_id and amount:
            complaint = get_object_or_404(Complaint, id=complaint_id)
            complaint.application_fee = int(amount)
            complaint.save()

            return render(request, 'payment_sucess.html', {
                'complaint': complaint
            })

    return redirect(complaint_list)






from django.utils.crypto import get_random_string # type: ignore
from django.core.mail import send_mail # type: ignore

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = user_reg.objects.get(Email=email)
        except:  # noqa: E722
            messages.info(request, "Email id not registered")
            return redirect(forgot_password)
        # Generate and save a unique token
        token = get_random_string(length=4)
        PasswordReset.objects.create(user_details=user, token=token)

        # Send email with reset link
        reset_link = f'http://127.0.0.1:8000/reset_password/{token}'
        try:
            send_mail('Reset Your Password', f'Click the link to reset your password: {reset_link}',
                      'settings.EMAIL_HOST_USER', [email], fail_silently=False)
            # return render(request, 'emailsent.html')
        except:  # noqa: E722
            messages.info(request, "Network connection failed")
            return redirect(forgot_password)

    return render(request,'forgot.html')

def reset_password(request,token):
    # Verify token and reset the password
    print(token)
    password_reset = PasswordReset.objects.get(token=token)
    # usr = User.objects.get(id=password_reset.user_id)
    if request.method == 'POST':
        new_password = request.POST.get('newpassword')
        repeat_password = request.POST.get('cpassword')
        if repeat_password == new_password:
            password_reset.user_details.Password=new_password
            password_reset.user_details.save()
            # password_reset.delete()
            return redirect(login)
    return render(request, 'reset_password.html', {'token': token})

