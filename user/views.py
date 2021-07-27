import datetime

import razorpay
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import ReviewForm
from .models import customer_data, contact_us_data, category_data, sub_category_data, product_data, \
    cart_data, order_data, payment_data, review_data, order_item_data
from admin1.views import render_to_pdf, download_pdf

# Create your views here.

def index(request):
    category_all_data = category_data.objects.all()[:4]
    sub_category_data_all = sub_category_data.objects.all()
    product_data_all = product_data.objects.all()[:4]
    product_data_last = product_data.objects.all().order_by('-created_at')[:6]
    all_cart = cart_data.objects.all().filter(cust_id=request.user.id)
    return render(request, 'user/index.html',
                  {'all_cart': all_cart, 'product_data_all': product_data_all, 'category_all_data': category_all_data,
                   'sub_category_data_all': sub_category_data_all, 'product_data_last': product_data_last})


def about_us(request):
    category_all_data = category_data.objects.all()[:4]
    sub_category_data_all = sub_category_data.objects.all()
    return render(request, 'user/about_us.html',
                  {'category_all_data': category_all_data, 'sub_category_data_all': sub_category_data_all})


def contact_us(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        contact_no = request.POST['contact_no']
        msg = request.POST['msg']
        subject = request.POST['subject']
        contact_data_store = contact_us_data(name=name, email=email, con_no=contact_no, msg=msg, subject=subject)
        contact_data_store.save()
        return redirect('/user/contact_us')
    else:
        category_all_data = category_data.objects.all()[:4]
        sub_category_data_all = sub_category_data.objects.all()
        return render(request, 'user/contact_us.html',
                      {'category_all_data': category_all_data, 'sub_category_data_all': sub_category_data_all})


def cart(request):
    grand_total = 0
    category_all_data = category_data.objects.all()[:4]
    sub_category_data_all = sub_category_data.objects.all()
    all_cart = cart_data.objects.filter(cust_id=request.user.id)
    for total in all_cart:
        grand_total += total.order_price
    print(grand_total)
    return render(request, 'user/cart.html', {'all_cart': all_cart, 'category_all_data': category_all_data,
                                              'sub_category_data_all': sub_category_data_all, "grand_total":grand_total})


def cart_delete(request, id):
    cart_delete = cart_data.objects.filter(id=id, cust_id=request.user.id)
    cart_delete.delete()
    return redirect('/user/cart')


def product(request):
    return render(request, 'user/product.html')


def single_product(request, id):
    revie = review_data.objects.all()
    for x in revie:
        print(revie)
    form = ReviewForm()

    if request.method == 'POST' and request.user.is_authenticated:
        p_id = product_data.objects.get(id=id)
        p_id = p_id
        c_id = customer_data(request.user.id)
        rating = request.POST['rating']
        review = request.POST['review']
        review_store = review_data(p_id=p_id, c_id=c_id, rating=rating, review=review)
        review_store.save()
        return redirect('user-home')

    product_data_show = product_data.objects.filter(id=id)
    sub_category_id = ''
    for x in product_data_show:
        sub_category_id = x.s_id
    product_featured = product_data.objects.filter(s_id=sub_category_id)[:7]
    category_all_data = category_data.objects.all()[:4]
    sub_category_data_all = sub_category_data.objects.all()
    return render(request, 'user/single_product.html',
                  {'form': form, 'product_data_show': product_data_show, 'product_featured': product_featured,
                   'category_all_data': category_all_data, 'sub_category_data_all': sub_category_data_all})


@login_required(login_url="user-login")
def payment(request):
    amount = 0
    all_cart = cart_data.objects.filter(cust_id=request.user.id)
    for x in all_cart:
        amount+=x.order_price
    p = amount
    order_amount = amount * 100
    order_currency = 'INR'
    client = razorpay.Client(auth=('rzp_test_sICiDAziTKEuG2', 'kpOKwqY2zbtu76bDKgJxXiM4'))
    payment = client.order.create({'amount': order_amount, 'currency': order_currency, 'payment_capture': '1'})
    order_data_store = order_data(c_id=customer_data(request.user.id), order_id=payment['id'], o_amount=p,
                                  o_address='Pending', status="pending")
    order_data_store.save()
    for x in all_cart:
        order_item_data_store=order_item_data(o_id=order_data_store,p_id=x.p_id,qty=x.quantity,amount=x.order_price)
        order_item_data_store.save()
    category_all_data = category_data.objects.all()[:4]
    sub_category_data_all = sub_category_data.objects.all()
    return render(request, 'user/checkout.html',
                  {'category_all_data': category_all_data, 'sub_category_data_all': sub_category_data_all,
                   'payment': payment, 'all_cart': all_cart, 'amount': amount})


@login_required(login_url="user-login")
def confirmation(request):
    return render(request, 'user/confirmation.html')


def search(request):
    search_product_name = request.GET.get('search_product')
    all_search_product = product_data.objects.filter(p_name__contains=search_product_name)
    category_all_data = category_data.objects.all()[:5]
    sub_category_data_all = sub_category_data.objects.all()
    return render(request, 'user/search.html',
                  {'all_search_product': all_search_product, 'category_all_data': category_all_data,
                   'sub_category_data_all': sub_category_data_all, 'search_product_name': search_product_name})


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username)
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            print("Hello")
            auth.login(request, user)
            return redirect('/user')
        else:
            messages.error(request, "Username or Password is Incorrect")
            return redirect('/user')
    else:
        return redirect('/user')


def logout(request):
    auth.logout(request)
    return redirect('/user')


def registration(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        c_password = request.POST['confirm_password']
        gender = request.POST['gender']
        contact_no = request.POST['con_no']
        address = request.POST['address']
        username = request.POST['username']
        if request.FILES:
            image = request.FILES['image']
            print(firstname)
            fs1 = FileSystemStorage()
            filename1 = fs1.save(image.name, image)
            url1 = fs1.url(filename1)
            try:
                user = User.objects.get(username=username)
                print(lastname)
                return render(request, 'user/index.html', {'username_error': 'Username Already Exists.'})

            except User.DoesNotExist:
                if password == c_password:
                    user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname,
                                                    email=email,
                                                    password=password)
                    print(username)
                    profile_data1 = customer_data(user_id=user, f_name=firstname, l_name=lastname, email=email,
                                                  image=url1,
                                                  gender=gender, address=address, con_no=contact_no)
                    profile_data1.save()
                    return redirect('user-login')
                else:
                    return render(request, 'user/index.html',
                                  {'password_error': 'Password And Confirm Password must be same'})
        else:
            try:
                user = User.objects.get(username=username)
                print(lastname)
                return render(request, 'user/index.html', {'username_error': 'Username Already Exists.'})

            except User.DoesNotExist:
                if password == c_password:
                    user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname,
                                                    email=email,
                                                    password=password)
                    print(username)
                    profile_data1 = customer_data(user_id=user, f_name=firstname, l_name=lastname, email=email,
                                                  gender=gender, address=address, con_no=contact_no)
                    profile_data1.save()
                    return redirect('user-login')
                else:
                    return render(request, 'user/index.html',
                                  {'password_error': 'Password And Confirm Password must be same'})
    else:
        return render(request)


def search_sub_cat(request, sub_cat):
    all_product = product_data.objects.all()
    category_all_data = category_data.objects.all()[:5]
    sub_category_data_all = sub_category_data.objects.all()
    return render(request, 'user/search.html',
                  {'all_product': all_product, 'sub_cat': sub_cat, 'category_all_data': category_all_data,
                   'sub_category_data_all': sub_category_data_all})


@login_required(login_url='user-login')
def add_to_cart(request, id):
    p=product_data.objects.get(id=id)
    add_to_cart_store = cart_data(p_id=product_data(id), cust_id=User(request.user.id),
                                  created_at=datetime.datetime.now(),order_price=p.p_price)
    add_to_cart_store.save()
    return redirect('/user')


def filter(request):
    p_name = request.GET.get('search_product')
    price = request.GET.get('amount')
    filter_price = product_data.objects.filter(p_name__contains=p_name).filter(p_price__lte=price)
    print(filter_price)
    return render(request, 'user/search.html', {'filter_price': filter_price, 'price': price})


def discount(request):
    print("HELLOW WORLD")
    return redirect('/user/cart')


@login_required(login_url="user-login")
def checkout(request):
    amount = 0
    category_all_data = category_data.objects.all()[:4]
    sub_category_data_all = sub_category_data.objects.all()
    all_cart = cart_data.objects.filter(cust_id=request.user.id)
    for x in all_cart:
        amount+=x.order_price
    return render(request, 'user/checkout.html',
                  {'all_cart': all_cart, 'amount': amount, 'category_all_data': category_all_data,
                   'sub_category_data_all': sub_category_data_all})


@login_required(login_url="user-login")
def payment_store(request):
    payment_id = request.GET.get('payment_id')
    order_id = request.GET.get('order_id')
    signature = request.GET.get('signature')
    o = order_data.objects.get(order_id=order_id)
    o_i_d = order_item_data.objects.filter(o_id=o.id)
    order_data.objects.filter(order_id=order_id).update(status="Paid")
    cart_user_data = cart_data.objects.filter(cust_id=request.user.id)
    cart_user_data.delete()
    payment_data_store = payment_data(user_id=User(request.user.id), payment_id=payment_id, signature=signature,
                                      o_id=o, pay_date=datetime.datetime.now(), pay_status='Success',
                                      pay_mode='online')
    payment_data_store.save()
    pdf = render_to_pdf('reports/invoice.html', {'order_detail': o, 'order_item_data': o_i_d})
    response = download_pdf(pdf)
    if response:
        return response
    return redirect('confirm')


@login_required(login_url="user-login")
def update_add_quantity_cart(request, id):
    g_t=0
    p_d = product_data.objects.get(id=id)
    c_d = cart_data.objects.get(p_id=p_d.id, cust_id=request.user.id)
    u_q = c_d.quantity + 1
    order_price = u_q * p_d.p_price
    c_i_u = cart_data(id=c_d.id, quantity=u_q, updated_at=datetime.datetime.now(), created_at=c_d.created_at,
                      cust_id=request.user, p_id=p_d,order_price=order_price)
    c_i_u.save()
    cart_total = cart_data.objects.filter(cust_id=request.user.id)
    for t in cart_total:
        g_t += t.order_price
    return JsonResponse([u_q, order_price,g_t], safe=False)


@login_required(login_url="user-login")
def update_minus_quantity_cart(request, id):
    g_t=0
    p_d = product_data.objects.get(id=id)
    c_d = cart_data.objects.get(p_id=p_d.id, cust_id=request.user.id)
    u_q = c_d.quantity - 1
    if u_q <1:
        cart_delete(request,c_d.id)
    else:
        order_price = (u_q * p_d.p_price)
        c_i_u = cart_data(id=c_d.id, quantity=u_q, updated_at=datetime.datetime.now(), created_at=c_d.created_at,
                          cust_id=request.user, p_id=p_d,order_price=order_price)
        c_i_u.save()
        cart_total = cart_data.objects.filter(cust_id=request.user.id)
        for t in cart_total:
            g_t += t.order_price
        return JsonResponse([u_q, order_price, g_t], safe=False)
