from django.shortcuts import render, redirect
from .models import Profile
import pdfkit
from django.http import HttpResponse
from django.template import loader
import io

# Create your views here.
def accept(request):
    if request.method == 'POST':
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        summary = request.POST.get('summary','')
        degree = request.POST.get('degree','')
        school = request.POST.get('school','')
        university = request.POST.get('university','')
        previous = request.POST.get('previous','')
        skills = request.POST.get('skills','')
        
        # Create a new Profile object and save it to the database
        profile = Profile(
            name=name,
            email=email,
            phone=phone,
            summary=summary,
            degree=degree,
            school=school,
            university=university,
            previous_work=previous,
            skills=skills
        )
        profile.save()
        
        # Redirect to a new URL or render a success template
        return redirect('accept')  # Replace 'success_url' with the actual URL or view name

    return render(request, 'pdf/accept.html')

def resume(request, id):
    user_profile = Profile.objects.get(pk=id)
    template = loader.get_template('pdf/resume.html')
    html = template.render({"user_profile": user_profile})
    options = {
        'page-size': 'A4',
        'margin-top': '3mm',
        'margin-right': '3mm',
        'margin-bottom': '3mm',
        'margin-left': '3mm',
        'encoding': 'UTF-8',
    }
    pdf = pdfkit.from_string(html, False, options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{user_profile.name}resume.pdf"'
    return response

def list_resume(request):
    user_profile = Profile.objects.all()
    return render(request, 'pdf/list.html', {'user_profile': user_profile})