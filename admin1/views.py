from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from user.models import category_data,sub_category_data,product_data, customer_data,contact_us_data,reply_data,discount_data,order_data,payment_data,review_data,order_item_data
from django.conf import settings
import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from .filters import OrderFilter
# Create your views here.


def isadmin(user):
    if user.is_superuser:
        return True
    else:
        return False


@login_required(login_url="admin-login")
def index(request):
    return render(request, 'admin1/layout/master.html')


def export_pdf(request):
    try:
        if 'order_status' in request.GET:
            new_order = order_data.objects.all().order_by('-id')
            order_f = OrderFilter(request.GET, queryset=new_order)
            new_order = order_f.qs
            queryset = new_order
            print(queryset)
            if queryset:
                pdf = render_to_pdf('reports/order_report.html', {"queryset": queryset})
                response = download_pdf(pdf)
                return response
            else:
                return HttpResponse("No Data ")
        return HttpResponse("Please Perform a Search Operation")
    except ValueError:
        return HttpResponse(ValueError)


def download_pdf(pdf):
    response = HttpResponse(pdf, content_type='application/pdf')
    filename = "Report_%s.pdf" % (datetime.datetime.now())
    content = "attachment; filename='%s'" % (filename)
    response['Content-Disposition'] = content
    return response


@login_required(login_url="admin-login")
def add_user(request):
    if request.method == 'POST':
        firstname = request.POST['f_name']
        lastname = request.POST['l_name']
        email = request.POST['email']
        password = request.POST['password']
        gender = request.POST['gender']
        contact_no = request.POST['con_no']
        address = request.POST['address']
        username = request.POST['username']
        image = request.FILES['image']
        print(firstname)
        fs1= FileSystemStorage()
        filename1= fs1.save(image.name,image)
        url1=fs1.url(filename1)
        try:
            user = User.objects.get(username=username)
            print(lastname)
            return render(request,'admin1/add_user.html',{'username_error':'Username Already Exists.'})
        except User.DoesNotExist:
            user = User.objects.create_user(username=username,first_name=firstname,last_name=lastname,email	=email,password=password)
            print(username)
            profile_data1 = customer_data(user_id=user,f_name=firstname,l_name=lastname,email=email, image=url1, gender=gender,address=address,con_no=contact_no, status="Active")
            profile_data1.save()
            return redirect('/admin1/add_user')
    else:
        customer_data_read = customer_data.objects.all()
        paginator = Paginator(customer_data_read,4) #Start Pagination Logic
        page = request.GET.get('page')
        try:
            customer_data_read = paginator.page(page)
        except PageNotAnInteger:
            customer_data_read = paginator.page(1)
        except EmptyPage:
            customer_data_read = paginator.page(paginator.num_pages)
            #End Pagination
        return render(request, 'admin1/add_user.html', {'customer_data_read':customer_data_read})


@login_required(login_url="admin-login")
def add_user_delete(request,id):
    add_user_delete=User.objects.filter(id=id)
    customer_data_delete=customer_data.objects.filter(user_id=id)
    add_user_delete.delete()
    customer_data_delete.delete()
    return redirect('/admin1/add_user')


@login_required(login_url="admin-login")
def user_show(request,id):
    user_show1=customer_data.objects.filter(user_id=id)
    return render(request,'admin1/add_user.html',{'user_show1':user_show1})


@login_required(login_url="admin-login")
def user_edit(request,id):
    if request.method == 'POST':
        firstname = request.POST['f_name']
        lastname = request.POST['l_name']
        email = request.POST['email']
        gender = request.POST['gender']
        contact_no = request.POST['con_no']
        address = request.POST['address']
        username = request.POST['username']
        image = request.FILES['image']
        print(firstname)
        fs1= FileSystemStorage()
        filename1= fs1.save(image.name,image)
        url1=fs1.url(filename1)
        user = User.objects.create_user(id=id, username=username,first_name=firstname,last_name=lastname,email	=email)
        print(username)
        profile_data1 = customer_data(user_id=user,f_name=firstname,l_name=lastname,email=email, image=url1, gender=gender,address=address,con_no=contact_no, status="Active")
        profile_data1.save()
        return redirect('/admin1/add_user')
    else:
        customer_data_edit = customer_data.objects.filter(user_id=id)
        return render(request, 'admin1/add_user.html', {'customer_data_edit':customer_data_edit})


@login_required(login_url="admin-login")
@user_passes_test(isadmin)
def dashboard(request):
    users = customer_data.objects.all().count()
    payment = order_data.objects.filter(order_id__isnull='').count()
    contact_us = contact_us_data.objects.all().count()
    review = review_data.objects.all().count()
    new_order = order_data.objects.all()
    order_count = new_order.count()

    order_list = order_data.objects.all().order_by('-id')
    order_f = OrderFilter(request.GET, queryset=order_list)
    print(order_f.qs)
    order_list = order_f.qs

    context = {
        'users': users,
        'order_list': order_list,
        'new_order': new_order,
        'payment': payment,
        'contact_us': contact_us,
        'order_count': order_count,
        'order_f': order_f,
        'review': review,

    }
    return render(request, 'admin1/dashboard.html',context)


@login_required(login_url="admin-login")
def category(request):
    if request.method == 'POST':
        category_store=request.POST['cat_name']
        print(category)
        category_update = category_data(cat_name=category_store)
        category_update.save()
        return redirect('/admin1/category')
    else:
        category_show = category_data.objects.all()
        paginator = Paginator(category_show,5) #Start Pagination Logic
        page = request.GET.get('page')
        try:
            category_show = paginator.page(page)
        except PageNotAnInteger:
            category_show = paginator.page(1)
        except EmptyPage:
            category_show = paginator.page(paginator.num_pages) #End Pagination
        return render(request,'admin1/category.html', {'category_show':category_show})

def cat_delete(request,id):
    cat_deletee=category_data.objects.filter(id=id)
    cat_deletee.delete()
    return redirect('/admin1/category')

def edit(request,id):
    edit_data=category_data.objects.filter(id=id)
    return render(request, 'admin1/category.html', {'edit_data':edit_data})

def edit_data_update(request,id):
    if request.method == 'POST':
        category_store=request.POST['cat_name']
        category_update = category_data(id=id,cat_name=category_store)
        category_update.save()
        return redirect('/admin1/category')


@login_required(login_url="admin-login")
def sub_category(request):
    if request.method == 'POST':
        category=request.POST['cat_name']
        sub_category=request.POST['s_name']
        sub_category_store = sub_category_data(cat_id=category_data(category), s_name=sub_category)
        sub_category_store.save()
        return redirect('/admin1/sub_category')
    else:
        category_show = category_data.objects.all()
        sub_category_show = sub_category_data.objects.all()
        paginator = Paginator(sub_category_show,5) #Start Pagination Logic
        page = request.GET.get('page')
        try:
            sub_category_show = paginator.page(page)
        except PageNotAnInteger:
            sub_category_show = paginator.page(1)
        except EmptyPage:
            sub_category_show = paginator.page(paginator.num_pages) #End Pagination
        return render(request, 'admin1/sub_category.html', {'category_show':category_show, 'sub_category_show':sub_category_show})

def sub_category_delete(request,id):
    sub_cat_delete=sub_category_data.objects.filter(id=id)
    sub_cat_delete.delete()
    return redirect('/admin1/sub_category')

def sub_category_edit(request,id):
    if request.method == 'POST':
        category=request.POST['cat_name']
        sub_category=request.POST['s_name']
        sub_category_store = sub_category_data(id=id,cat_id=category_data(category), s_name=sub_category)
        sub_category_store.save()
        return redirect('/admin1/sub_category')

    else:
        category_show = category_data.objects.all()
        sub_category_edit=sub_category_data.objects.filter(id=id)
        return render(request, 'admin1/sub_category.html',{'sub_category_edit':sub_category_edit,'category_show':category_show})

@login_required(login_url="admin-login")
def product(request):
    if request.method == 'POST':
        sub_category=request.POST['s_name']
        product_name=request.POST['p_name']
        product_price=request.POST['p_price']
        product_desc=request.POST['p_desc']
        product_image=request.FILES['p_image']
        fs1=FileSystemStorage()
        filename1=fs1.save(product_image.name, product_image)
        url1=fs1.url(filename1)
        product_store=product_data(s_id=sub_category_data(sub_category),p_name=product_name,p_price=product_price,p_desc=product_desc,p_image=url1)
        product_store.save()
        return redirect('/admin1/product')
    else:
        sub_category_show = sub_category_data.objects.all()
        product_show=product_data.objects.all()
        paginator = Paginator(product_show,3) #Start Pagination Logic
        page = request.GET.get('page')
        try:
            product_show = paginator.page(page)
        except PageNotAnInteger:
            product_show = paginator.page(1)
        except EmptyPage:
            product_show = paginator.page(paginator.num_pages) #End Pagination
        return render(request,'admin1/product.html',{'sub_category_show':sub_category_show,'product_show':product_show})

def product_delete(request,id):
    product_delete=product_data.objects.filter(id=id)
    product_delete.delete()
    return redirect('/admin1/product')


def product_edit(request,id):
    if request.method == 'POST':
        sub_category=request.POST['s_name']
        product_name=request.POST['p_name']
        product_price=request.POST['p_price']
        product_desc=request.POST['p_desc']
        product_image=request.FILES['p_image']
        fs1=FileSystemStorage()
        filename1=fs1.save(product_image.name,product_image)
        url1=fs1.url(filename1)
        product_store=product_data(id=id,s_id=sub_category_data(sub_category),p_name=product_name,p_price=product_price,p_desc=product_desc,p_image=product_image)
        product_store.save()
        return redirect('/admin1/product')

    else:
        sub_category_show=sub_category_data.objects.all()
        product_edit=product_data.objects.filter(id=id)
        return render(request,'admin1/product.html',{'product_edit':product_edit,'sub_category_show':sub_category_show})



def product_show1(request,id):
    product_show1=product_data.objects.filter(id=id)
    return render(request,'admin1/product.html', {'product_show1':product_show1})


@login_required(login_url="admin-login")
def order(request):
    all_order = order_data.objects.all()
    return render(request,'admin1/order.html', {'all_order':all_order})

def order_show(request,id):
    order_show=order_data.objects.filter(id=id)
    return render(request,'admin1/order.html',{'order_show':order_show})


def order_delete(request,id):
    order_delete=order_data.objects.filter(id=id)
    order_delete.delete()
    return redirect('/admin1/order')


@login_required(login_url="admin-login")
def account(request):
    account_dat_store=order_item_data.objects.all()
    return render(request,'admin1/account.html',{'account_dat_store':account_dat_store})


def account_show(request,id):
    account_show=order_item_data.objects.filter(id=id)
    return render(request,'admin1/account.html', {'account_show':account_show})

@login_required(login_url="admin-login")
def payment(request):
    all_payment=payment_data.objects.all()
    return render(request,'admin1/payment.html',{'all_payment':all_payment})

def payment_show(request,id):
    payment_show=payment_data.objects.filter(user_id=id)
    return render(request,'admin1/payment.html',{'payment_show':payment_show})

@login_required(login_url="admin-login")
def discount(request):
    if request.method == 'POST':
        discount_name=request.POST['discount_name']
        amount=request.POST['amount']
        validate_date=request.POST['validate_date']
        discount_update = discount_data(discount_name=discount_name,amount=amount,validate_date=validate_date,created_at=datetime.datetime.now())
        discount_update.save()
        return redirect('/admin1/discount')
    else:
        discount_show = discount_data.objects.all()
        paginator = Paginator(discount_show,2) #Start Pagination Logic
        page = request.GET.get('page')
        try:
            discount = paginator.page(page)
        except PageNotAnInteger:
            discount_show = paginator.page(1)
        except EmptyPage:
            discount_show = paginator.page(paginator.num_pages) #End Pagination
        return render(request,'admin1/discount.html', {'discount_show':discount_show})

def discount_delete(request,id):
    discount_delete = discount_data.objects.filter(id=id)
    discount_delete.delete()
    return redirect('/admin1/discount')


def discount_edit(request,id):
    edit_data=discount_data.objects.filter(id=id)
    return render(request, 'admin1/discount.html', {'discount_data':discount_data})

def discount_show1(request,id):
    discount_show1=discount_data.objects.filter(id=id)
    return render(request,'admin1/discount.html', {'discount_show1':discount_show1})



@login_required(login_url="admin-login")
def contactus(request):
    all_contact=contact_us_data.objects.all()
    all_reply = reply_data.objects.all()
    paginator = Paginator(all_contact,2)
    page = request.GET.get('page')
    try:
        all_contact = paginator.page(page)
    except PageNotAnInteger:
        all_contact = paginator.page(1)
    except EmptyPage:
        all_contact = paginator.page(paginator.num_pages)

    return render(request,'admin1/contactus.html', {'all_contact':all_contact,'all_reply':all_reply})

def contactus_delete(request,id):
    contactus_delete=contact_us_data.objects.filter(id=id)
    contactus_delete.delete()
    return redirect('/admin1/contactus')

@login_required(login_url="admin-login")
def reply(request,id):
    reply = request.POST['reply']
    reply_store = reply_data(contact_us=contact_us_data(id), reply=reply)
    email = request.POST['email']
    reply_store.save()
    html_content = render_to_string("admin1/reply.html", {"title":"Fitness Contact Reply", "reply":reply})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives("Fitness Reply",text_content, settings.EMAIL_HOST_USER, [email])
    email.attach_alternative(html_content, "text/html")
    email.send()

    return redirect('/admin1/contactus')

def review(request):
    review=review_data.objects.all()
    return render(request,'admin1/review.html',{'review':review})

def review_show(request,id):
    review_show=review_data.objects.filter(id=id)
    return render(request,'admin1/review.html',{'review_show':review_show})


#def login(request):
    #return render(request,'login.html')
def login1(request):
    return render(request,'login1.html')
def visitor(request):
    return render(request,'admin1/visitor.html')


def user_active(request, id):
    cust_read_data = customer_data.objects.filter(user_id=id)
    for x in cust_read_data:
        first_name = x.user_id.first_name
        last_name = x.user_id.last_name
        email = x.user_id.email
        username = x.user_id.username
        gender = x.gender
        image = x.image
        con_no = x.con_no
        address = x.address
    user = User.objects.create_user(id=id, username=username,first_name=first_name,last_name=last_name, email=email)
    status_active = customer_data(user_id=user, f_name=first_name,l_name=last_name, email=email, image=image, gender=gender, address=address, con_no=con_no, status="Active")
    status_active.save()
    return redirect('/admin1/add_user')

def user_deactive(request, id):
    cust_read_data = customer_data.objects.filter(user_id=id)
    for x in cust_read_data:
        first_name = x.user_id.first_name
        last_name = x.user_id.last_name
        email = x.user_id.email
        username = x.user_id.username
        gender = x.gender
        image = x.image
        con_no = x.con_no
        address = x.address
    user = User.objects.create_user(id=id, username=username,first_name=first_name,last_name=last_name, email=email)
    status_deactive = customer_data(user_id=user, f_name=first_name,l_name=last_name, email=email, image=image, gender=gender, address=address, con_no=con_no, status="Deactive")
    status_deactive.save()
    return redirect('/admin1/add_user')



def adminLogin(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin-home')
        if request.user.is_active:
            return redirect('user-home')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                if request.user.is_superuser:
                    return redirect('admin-dashboard')
                if request.user.is_active:
                    return redirect('user-home')
        return render(request, 'login1.html')

@login_required(login_url="admin-login")
def adminLogout(request):
    logout(request)
    return redirect('admin-login')


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None