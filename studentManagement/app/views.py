from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from app.models import CustomUser
from app.models import Staff , Course , Subject, Session_Year , Staff_Notifications, Staff_Feedback,Staff_leave

# Create your views here.
def index(request):
    return render(request,'homepage.html')


def login_page(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST.get('email'),
            password = request.POST.get('password')
        )
        if user is not None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('HOD')
            elif user_type == '2':
                return redirect('STAFF')
            else:

                return redirect('login_page')

        else:
            messages.error(request, 'Invalid Email and Password')
            return redirect('login_page')

    return render(request, 'loginpage.html')

def HOD(request):
    return render(request,'HOD_dashboard.html')

def STAFF(request):
    return render(request,'STAFF_dashboard.html')

def dash(request):
    return render(request,'dashboard.html')

def profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    context ={
        'user':user
    }
    return render(request,'profile.html',context)

def profile_update(request):
    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

    try:
        customuser = CustomUser.objects.get(id=request.user.id)
        customuser.profile_pic = profile_pic
        customuser.first_name = first_name
        customuser.last_name = last_name
        customuser.email = email
        customuser.username = username
        if password != None and password != '':
           customuser.set_password(password)
        if profile_pic != None and profile_pic != '':
           customuser.profile_pic = profile_pic
        customuser.save()
        messages.success(request, 'Your profile successfully updated')
        return redirect('profile_update')

    except:
        messages.error(request, 'failed to update your profile')
    return render(request, 'profile.html')

@login_required(login_url='login_page')
def add_staff(request):
    if request.method == 'POST':
        profile_pic = request.FILES.get('profilePic')  # Ensure the field name matches your form
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        # Ensure email and username are unique
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, "Email is already taken")
            return render(request, 'add_staff.html', {'first_name': first_name, 'last_name': last_name, 'email': email, 'username': username, 'address': address, 'gender': gender})

        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, "Username is already taken")
            return render(request, 'add_staff.html', {'first_name': first_name, 'last_name': last_name, 'email': email, 'username': username, 'address': address, 'gender': gender})

        # Create the user
        user = CustomUser(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            profile_pic=profile_pic,
            user_type=2  # Assuming '2' is the user type for staff
        )
        user.set_password(password)  # Hashes the password before saving
        user.save()

        # Create the staff profile
        staff = Staff(
            admin=user,  # Assuming Staff has a OneToOneField with CustomUser
            address=address,
            gender=gender
        )
        staff.save()

        messages.success(request, "Staff added successfully")
        return redirect('add_staff')

    # No email variable is used here, so no error will occur
    return render(request, 'add_staff.html')

def logout_page(request):
   logout(request)
   return redirect('login_page')

def views_staff(request):
    views_staff = Staff.objects.all()

    return render(request, 'views_staff.html',{'views_staff':views_staff})


def edit_staff(request,id):
    staff = Staff.objects.get(id=id)

    return render(request,'edit_staff.html',{'staff':staff})

def update_staff(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        profilePic = request.FILES.get('profilePic')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        address = request.POST.get('address')
        gender = request.POST.get('gender')

        user = CustomUser.objects.get(id=staff_id)
        user.firstname = firstname
        user.lastname = lastname
        user.email = email
        user.username = username
        if password != None and password != '':
            user.set_password(password)
        if profilePic != None and profilePic != '':
            user.profilePic = profilePic
        user.save()

        staff = Staff.objects.get(admin=staff_id)
        staff.address = address
        staff.gender = gender
        staff.save()
        messages.success(request, "Staff Updated SuccessFully")
        return redirect('views_staff')

    return render(request,'edit_staff.html')

def delete_staff(request,admin):
   staff = CustomUser.objects.get(id=admin)
   staff.delete()
   messages.success(request,'Staff Deleted Successfully')
   return redirect('views_staff')

def add_course(request):
   if request.method == 'POST':
       course_name = request.POST.get('course_name')
       course = Course(
           name = course_name,
       )
       course.save()
       messages.success(request,'Course Added Successfully')
       return redirect('add_course')
   return render(request,'add_course.html')


def view_course(request):
    course = Course.objects.all()

    return render(request,'view_course.html',{'course':course})

def edit_course(request,id):
    course = Course.objects.get(id = id)

    return render(request, 'edit_course.html',{'course':course})

def update_course(request):
   if request.method == 'POST':
       name = request.POST.get('course_name')
       course_id = request.POST.get('course_id')
       course = Course.objects.get(id=course_id)
       course.name = name
       course.save()
       messages.success(request, 'Course Updated Successfully')
       return redirect('view_course')
   return render(request, 'edit_course.html')


def delete_course(request,id):
   course = Course.objects.get(id=id)
   course.delete()
   messages.success(request,'Course Deleted Successfully')
   return redirect('view_course')


def add_subject(request):
   course = Course.objects.all()
   staff = Staff.objects.all()
   context = {
       'course':course,
       'staff':staff,
   }
   if request.method == 'POST':
       subject_name = request.POST.get('subject_name')
       course_id = request.POST.get('course_id')
       staff_id = request.POST.get('staff_id')


       course = Course.objects.get(id = course_id)
       staff = Staff.objects.get(id = staff_id)


       subject = Subject(
           name = subject_name,
           course = course,
           staff = staff,
       )
       subject.save()
       messages.success(request,"Subject Added SuccessFully")
       return redirect('add_subject')
   return render(request,'add_subject.html',context)


def view_subject(request):
    subject = Subject.objects.all()

    return render(request,'view_subject.html',{'subject':subject})

def edit_subject(request,id):
   subject = Subject.objects.get(id = id)
   course = Course.objects.all()
   staff = Staff.objects.all()
   context = {
       'subject': subject,
       'course':course,
       'staff':staff,
   }
   return render(request, 'edit_subject.html', context)


def update_subject(request):
    if request.method == 'POST':
        subject_id =request.POST.get('subject_id')
        subject_name =request.POST.get('subject_name')
        course_id = request.POST.get('course_id')
        staff_id = request.POST.get('staff_id')

        subject = Subject.objects.get(id=subject_id)
        subject.name = subject_name
        subject.course =Course.objects.get(id=course_id)
        subject.staff =Staff.objects.get(id=staff_id)
        subject.save()

        messages.success(request,"Subject updated successfully!")
        return redirect('view_subject')

    return render(request,'edit_subject.html')


def delete_subject(request,id):
   subject = Subject.objects.filter(id=id)
   subject.delete()
   messages.success(request,'Subject Deleted Successfully')
   return redirect('view_subject')

def add_session(request):
    if request.method == 'POST':
        session_year_start = request.POST.get('session_year_start')
        session_year_end = request.POST.get('session_year_end')

        session = Session_Year(
            session_start=session_year_start,
            session_end=session_year_end,
        )
        session.save()
        messages.success(request, 'Session Added Successfully')
        return redirect('add_session')

    return render(request,'add_session.html')


def view_session(request):
    session = Session_Year.objects.all()

    return render(request,'view_session.html',{'session':session})

def edit_session(request,id):
   session = Session_Year.objects.get(id=id)

   return render(request,'edit_session.html',{'session':session})


def update_session(request):
   if request.method == 'POST':
       session_id = request.POST.get('session_id')
       session_year_start = request.POST.get('session_year_start')
       session_year_end = request.POST.get('session_year_end')


       session = Session_Year(
           id = session_id,
           session_start = session_year_start,
           session_end = session_year_end,
       )
       session.save()
       messages.success(request,"Session Updated SuccessFully")
       return redirect('view_session')
   return render(request,'edit_session.html')


def delete_session(request,id):
   session = Session_Year.objects.get(id=id)
   session.delete()
   messages.success(request,'Session Deleted Successfully')
   return redirect('view_session')


def send_staff_notifications(request):
    staff = Staff.objects.all()
    see_notification = Staff_Notifications.objects.all()
    context = {
        'staff':staff,
        'see_notification': see_notification,
    }
    return render(request,'send_staff_notifications.html', context)


def save_staff_notifications(request):
    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        message = request.POST.get('message')
        try:
            staff = Staff.objects.get(id=staff_id)
            notification = Staff_Notifications(
                staff_id=staff,
                message=message,
            )
            notification.save()
            messages.success(request, 'Notification successfully sent.')
        except Staff.DoesNotExist:
            messages.error(request, f"Staff with ID {staff_id} does not exist.")

        return redirect('send_staff_notifications')

    return render(request, 'send_staff_notifications.html')


def notify_view(request):
    staff = Staff.objects.get(admin=request.user.id)
    messages = Staff_Notifications.objects.filter(staff_id=staff.id, status=False)
    context = {
        'messages': messages
    }

    return render(request, 'view_notification.html', context)


def notifications_done(request,status):
    notification = Staff_Notifications.objects.get(id=status)
    notification.status = 1
    notification.save()
    return redirect('notify_view')
    return render(request,'view_notification.html')


def staff_feedback(request):
    return render(request, 'feedback.html')

def save_feedback(request):
    if request.method == 'POST':
        feedback_text = request.POST.get('feedback')
        try:
            staff = Staff.objects.get(admin=request.user.id)
            feedback = Staff_Feedback(
                staff_id=staff,
                feedback=feedback_text,
            )
            feedback.save()
            messages.success(request, 'Feedback Sent Successfully')
        except Staff.DoesNotExist:
            messages.error(request, 'Staff user not found.')
        return redirect('staff_feedback')
    return render(request, 'feedback.html')


def staff_feedback_view(request):
   feedback = Staff_Feedback.objects.all()
   feedback_history = Staff_Feedback.objects.all()
   context = {
       'feedback': feedback,
       'feedback_history':feedback_history,
   }
   return render(request,'staff_feedback.html',context)


def staff_feedback_view(request):
    if request.method == 'POST':
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('feedback_reply')

        try:
            feedback = Staff_Feedback.objects.get(id=feedback_id)
            feedback.feedback_reply = feedback_reply
            feedback.status = 1
            feedback.save()
            messages.success(request, 'Feedback Sent Successfully')
        except Staff_Feedback.DoesNotExist:
            messages.error(request, 'Feedback not found.')

        return redirect('staff_feedback_view')

    feedback_list = Staff_Feedback.objects.all()
    return render(request, 'staff_feedback_view.html', {'feedback_list': feedback_list})

def staff_feedback(request):
    staff_id = Staff.objects.get(admin=request.user.id)
    feedback_history = Staff_Feedback.objects.filter(staff_id=staff_id)
    context = {
        'feedback_history': feedback_history,
    }
    return render(request,'feedback.html',context)


def apply_leave(request):
    staff = Staff.objects.filter(admin=request.user.id)
    for i in staff:
        staff_id = i.id
        staff_leave_history = Staff_leave.objects.filter(staff_id=staff_id)
        context = {
            'staff_leave_history': staff_leave_history,
        }
    return render(request, 'Apply_leave.html', context)


def staff_leave_view(request):
        staff_leave = Staff_leave.objects.all()
        context = {
            'staff_leave': staff_leave,
        }
        return render(request, 'staff_leave_view.html', context)

def staff_approve_leave(request,id):
    leave = Staff_leave.objects.get(id=id)
    leave.status = 1
    leave.save()
    return redirect('staff_leave_view')
    return render(request, 'Apply_leave.html')


def staff_disapprove_leave(request,id):
   leave = Staff_leave.objects.get(id=id)
   leave.status = 2
   leave.save()
   return redirect('staff_leave_view')
   return render(request, 'Apply_leave.html')
