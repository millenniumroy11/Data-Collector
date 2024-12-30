from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from .models import DetailsForm
from django.template.loader import get_template
from xhtml2pdf import pisa

# Create your views here.

def Loginpage(request): 
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password1')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            return HttpResponse("Wronge Username or Password")
    return render (request,'login.html')

def user_logout(request):
    logout(request)  # Logs out the user
    return redirect('login')  # Redirect to login page (or any desired page)

def Details(request):
    if request.method == 'POST':
        fullname=request.POST.get('fullname','')
        email=request.POST.get('email','')
        address=request.POST.get('address','')

        Detail=DetailsForm.objects.create(fullname=fullname,email=email,address=address)
        Detail.save()
        return redirect('index')
    return render(request,'index.html')

def index(request):
    dse=DetailsForm.objects.all()
    return render(request,'index.html',{'dse':dse})

def listcreate(request):
    return render(request,'create.html')

def edit_data(request, id):
    data = get_object_or_404(DetailsForm, id=id)
    if request.method == 'POST':
        data.fullname = request.POST.get('fullname')
        data.email = request.POST.get('email')
        data.address = request.POST.get('address')
        data.save()
        return redirect('index')  # Replace 'home' with your main view name
    return render(request, 'edit.html', {'data': data})

# Delete Function
def delete_data(request, id):
    data = get_object_or_404(DetailsForm, id=id)
    data.delete()
    return redirect('index')  # Replace 'home' with your main view name

def search_records(request):
    query = request.GET.get('q', '').strip()  # Get the query and strip extra whitespace
    results = []
    if query:  # Only perform a search if query is not empty
        results = DetailsForm.objects.filter(
            fullname__icontains=query
        ) | DetailsForm.objects.filter(
            email__icontains=query
        ) | DetailsForm.objects.filter(
            address__icontains=query
        )
    return render(request, 'search_results.html', {'results': results, 'query': query})


def download_pdf(request):
    data = DetailsForm.objects.all()  # Fetch data from the database
    template_path = 'pdf_template.html'  # Your HTML template for the PDF
    context = {'data': data}  # Pass data to the template

    # Render the template to a string
    template = get_template(template_path)
    html = template.render(context)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="data.pdf"'

    # Generate the PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF')
    return response

