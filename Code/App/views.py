from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import logout
from datetime import date, datetime,timedelta
from django.forms.models import model_to_dict
import datetime
import smtplib, ssl
from email.message import EmailMessage
import math
import csv


def check_admin(user):
    return user.is_superuser

def check_student(user):
    return (not user.is_staff)

def check_teacher(user):
    return user.is_staff

def newSupplier(request):
    sup = Supplier.objects.all()
    length = len(sup) + 1
    context = {
        'ls': sup,
        'len': length,
    }
    if 'submit' in request.POST:

        name = request.POST["name"]
        email = request.POST["email"]
        mobile = request.POST["mobile"]
        product_type = request.POST["product_type"]
        GST = request.POST["GST"]
        address = request.POST["address"]
        pincode = request.POST["pincode"]
        print(mobile,email,name,product_type,GST,address,pincode)
        if (Supplier.objects.filter(GST=GST).exists()):
            return redirect('/newSupplier/')
        s = Supplier(mobile=mobile,email=email,name=name,product_type=product_type,GST=GST,address=address,pincode=pincode)
        s.save()
        return redirect('/supplier/')

    return render(request, 'App/Admin/Supplier/newSupplier.html',context)

def supplier(request):
    sup = Supplier.objects.all()

    context = {
        'ls': sup,
    }
    return render(request, 'App/Admin/Dashboard/supplier.html',context)

def newEmployee(request):
    sup = Employee.objects.all()
    u = User.objects.all()
    length = len(u)+1
    context = {
        'ls': sup,
        'len' : length,
    }
    if request.method == 'POST':
        username = length
        first_name = request.POST["first_name"]
        Department = request.POST["Department"]
        Designation = request.POST["Designation"]
        email = request.POST["email"]
        mobile = request.POST["mobile"]
        line_manager = request.POST["line_manager"]
        doj = request.POST["doj"]
        address = request.POST["address"]
        pincode = request.POST["pincode"]
        pwd1 = 'verticurl'

        if (Employee.objects.filter(username=username).exists() and User.objects.filter(username=username).exists()):
            print("hi1")
            messages.info(request, "Username and email already exists!")
            return redirect('/newEmployee/')
        elif User.objects.filter(email=email).exists():  # checks whether email is already in use
            print("hi2")
            messages.info(request, "This email already exists!")
            return redirect('/newEmployee/')
        elif User.objects.filter(username=username).exists():
            print("hi3")
            messages.info(request, "Username already exists!")
            return redirect('/newEmployee/')
        else:
            print("hi4")
            user = User.objects.create_user(first_name=first_name, username=username,
                                            email=email, password=pwd1, is_staff=False,is_superuser=False )
            user.save()
            u = User.objects.get(username=username)
            emp = Employee(username = u,Department=Department,Designation=Designation,
                           mobile=mobile,line_manager=line_manager,doj=doj,
                           address=address,pincode=pincode)
            emp.save()
            return redirect('/employee/')


    return render(request, 'App/Admin/Employee/newEmployee.html',context)

def editSupplier(request,pk):
    sup = Supplier.objects.get(sid=pk)
    context = {
        'ls': sup,
    }
    if request.method == 'POST':
        print("hi1")
        name = request.POST["name"]
        email = request.POST["email"]
        mobile = request.POST["mobile"]
        product_type = request.POST["product_type"]
        GST = request.POST["GST"]
        address = request.POST["address"]
        pincode = request.POST["pincode"]
        print(mobile,email,name,product_type,GST,address,pincode)
        Supplier.objects.filter(sid = sup.sid).update(mobile=mobile,email=email,name=name,product_type=product_type,GST=GST,address=address,pincode=pincode)
        return redirect('/supplier/')
    return render(request, 'App/Admin/Supplier/editSupplier.html',context)

def viewSupplier(request, pk):
    sup = Supplier.objects.get(sid=pk)
    a = Stock.objects.filter(supplier = sup)
    context = {
        'ls': sup,
        'a' : a,
        'asset': 'Asset',
    }
    return render(request, 'App/Admin/Supplier/viewSupplier.html',context)

def employee(request):
    sup = Employee.objects.all()

    context = {
        'ls': sup,
        'active': 'badge badge-pill-success',
        'exp': 'badge badge-pill-danger',
        't': True,
    }
    return render(request, 'App/Admin/Dashboard/employee.html',context)

def editEmployee(request,pk):
    emp = User.objects.get(username = pk)
    sup = Employee.objects.get(username= emp)
    p = Employee.objects.all()
    sdate = sup.doj.strftime("%Y-%m-%d")
    print(p)
    context = {
        'ls': sup,
        'ps': p,
        'sdate' : sdate,
    }

    if request.method == 'POST':
        first_name = request.POST["first_name"]
        Department = request.POST["Department"]
        Designation = request.POST["Designation"]
        email = request.POST["email"]
        mobile = request.POST["mobile"]
        line_manager = request.POST["line_manager"]
        doj = request.POST["doj"]
        address = request.POST["address"]
        pincode = request.POST["pincode"]

        #Supplier.objects.filter(sid = sup.sid).update(mobile=mobile,email=email,name=name,product_type=product_type,GST=GST,address=address,pincode=pincode)

        User.objects.filter(username = emp).update(first_name = first_name, email = email)
        Employee.objects.filter(username=emp).update( Department=Department, Designation=Designation,
                       mobile=mobile, line_manager=line_manager, doj=doj,
                       address=address, pincode=pincode)
        return redirect('/employee/')
    return render(request, 'App/Admin/Employee/editEmployee.html',context)

def viewEmployee(request,pk):
    emp = User.objects.get(username=pk)
    sup = Employee.objects.get(username=emp)
    p = Employee.objects.all()
    sdate = sup.doj.strftime("%Y-%m-%d")
    a = Allocation.objects.filter(aid = emp)
    context = {
        'ls': sup,
        'ps': p,
        'sdate': sdate,
        'status' : 1,
        'a':a,
        'asset': 'Asset',
        'active': 'badge badge-pill-success',
        'exp': 'badge badge-pill-danger',
        'net': 'badge badge-pill-info',
    }
    return render(request, 'App/Admin/Employee/viewEmployee.html',context)

def newStock(request):
    sup = Stock.objects.all()
    con = Supplier.objects.exclude(product_type= 'Asset')
    ass = Supplier.objects.exclude(product_type= 'Consumables')

    length = len(sup) + 1
    context = {
        'len': length,
        'con': con,
        'ass' : ass,
    }
    if request.method == 'POST':
        product_name = request.POST["product_name"]
        product_price = request.POST["product_price"]
        product_type = request.POST["product_type"]
        dop = request.POST["dop"]
        supplier = request.POST["supplier"]
        print("hi1")

        print("hi2")
        print(product_type)
        if product_type == 'Asset':
            print("hi3")
            serial_number = request.POST["serial_number"]
            depreciation =request.POST["depreciation"]
            warranty_date = request.POST["warranty_date"]

            if (len(serial_number) == 0 or len(depreciation) == 0 or len(warranty_date) == 0):
                messages.info(request, "Don't leave the credentials empty!")
                return redirect('/newStock/')

            if (Asset.objects.filter(serial_number=serial_number).exists()):
                return redirect('/stock/')
            print(dop< warranty_date)
            if(dop < warranty_date):
                print("hi4")
                se = Supplier.objects.get(sid = supplier)
                s = Stock(id=length ,product_name=product_name, product_price=product_price
                          , product_type=product_type, dop=dop, supplier=se)
                s.save()
                ae = Stock.objects.get(id = length)
                a = Asset(aid = ae,serial_number=serial_number,depreciation=depreciation,warranty_date=warranty_date,status = 1,depActive =0,age=0)
                a.save()
                cash = Cash(sid = ae,price=product_price,date = dop,type = 'Purchase')
                cash.save()
                return redirect('/stock/')
            else:
                return redirect('/newStock/')


        else:
            new_quantity = request.POST["new_quantity"]
            new_expiry = request.POST["new_expiry"]
            min_count = request.POST["min_count"]

            if (len(new_expiry) == 0 or len(new_quantity) == 0 or len(min_count) == 0):
                messages.info(request, "Don't leave the credentials empty!")
                return redirect('/newStock/')
            if (dop < new_expiry):
                se = Supplier.objects.get(sid=supplier)
                s = Stock(id=length, product_name=product_name, product_price=product_price
                          , product_type=product_type, dop=dop, supplier=se)
                s.save()
                ae = Stock.objects.get(id = length)
                c = Consumables(cid=ae, old_quantity = 0,old_expiry=datetime.date(2000, 1, 1),new_expiry=new_expiry,new_quantity=new_quantity,min_count=min_count)
                c.save()
                cash = Cash(sid = ae,price=product_price,date = dop,type = 'Purchase')
                cash.save()
                return redirect('/stock/')
            else:
                return redirect('/newStock/')

    return render(request, 'App/Admin/Stock/newStock.html',context)

def editAsset(request,pk):
    su = Stock.objects.get(id=pk)
    emp = Asset.objects.get(aid=su)
    sdate = su.dop.strftime("%Y-%m-%d")
    con = Supplier.objects.exclude(product_type='Consumables')
    exp = emp.warranty_date.strftime("%Y-%m-%d")
    context = {
        'ls': emp,
        'sdate': sdate,
        'con': con,
        'exp': exp,
    }
    if request.method == 'POST':
        product_name = request.POST["product_name"]
        product_price = request.POST["product_price"]
        dop = request.POST["dop"]
        supplier = request.POST["supplier"]
        serial_number = request.POST["serial_number"]
        depreciation = request.POST["depreciation"]
        warranty_date = request.POST["warranty_date"]
        if (len(serial_number) == 0 or len(depreciation) == 0 or len(warranty_date) == 0):
            messages.info(request, "Don't leave the credentials empty!")
            return redirect('/newStock/')
        se = Supplier.objects.get(sid = supplier)
        if (dop < warranty_date):
            Stock.objects.filter(id=pk).update(product_name=product_name, product_price=product_price
                                               , dop=dop, supplier=se)
            Cash.objects.filter(sid = su).update(price = product_price)
            Asset.objects.filter(aid=su).update(serial_number=serial_number,depreciation=depreciation,warranty_date=warranty_date)
            return redirect('/stock/')
        else:
            return redirect('/newStock/')
    return render(request, 'App/Admin/Stock/editAsset.html',context)

def editConsumable(request,pk):
    su = Stock.objects.get(id = pk)
    emp = Consumables.objects.get(cid=su)
    sdate = su.dop.strftime("%Y-%m-%d")
    con = Supplier.objects.exclude(product_type= 'Asset')
    exp = emp.new_expiry.strftime("%Y-%m-%d")
    context = {
        'ls': emp,
        'sdate': sdate,
        'con': con,
        'exp': exp,
    }
    if  request.method == 'POST':
        product_name = request.POST["product_name"]
        product_price = request.POST["product_price"]
        dop = request.POST["dop"]
        supplier = request.POST["supplier"]
        new_quantity = request.POST["new_quantity"]
        new_expiry = request.POST["new_expiry"]
        min_count = request.POST["min_count"]
        se = Supplier.objects.get(sid = supplier)
        if (len(new_expiry) == 0 or len(new_quantity) == 0 or len(min_count) == 0):
            messages.info(request, "Don't leave the credentials empty!")
            return redirect('/newStock/')
        if (dop < new_expiry):
            Stock.objects.filter(id=pk).update( product_name=product_name, product_price=product_price
                          , dop=dop, supplier=se)

            Cash.objects.filter(sid = su).update(price = product_price)

            Consumables.objects.filter(cid = su).update(old_quantity = 0,old_expiry=datetime.date(2000, 1, 1),new_expiry=new_expiry,new_quantity=new_quantity,min_count=min_count)
            return redirect('/stock/')
        else:
            return redirect('/newStock/')
    return render(request, 'App/Admin/Stock/editConsumable.html',context)

def stock(request):
    a = Asset.objects.all()
    c = Consumables.objects.all()

    context ={
        'a':a,
        'c':c,
        'active': 'badge badge-pill-success',
        'exp' : 'badge badge-pill-danger',
        'net': 'badge badge-pill-info',
        'one': 1,
        'two': 2,
    }
    return render(request, 'App/Admin/Dashboard/stock.html',context)

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if (len(username) == 0 or len(password) == 0):
            messages.info(request, 'Do not leave Credentials empty!')
            return HttpResponseRedirect('/login/')
        else:
            if not User.objects.filter(username=username).exists():
                messages.info(request, 'Username does not exist.')
                return HttpResponseRedirect('/Login/')
            elif user is not None:
                if check_admin(user) and user.is_active == True:
                    auth.login(request, user)
                    return HttpResponseRedirect('/Admin_Dashboard/')
                elif check_teacher(user) and user.is_active == True:
                    auth.login(request, user)
                    return HttpResponseRedirect('/allocator_dashboard/')
                elif check_student(user) and user.is_active == True:
                    auth.login(request, user)
                    return HttpResponseRedirect('/employee_dashboard/')
                else:
                    return redirect('/Login/')

            else:
                messages.info(request, 'Invalid Credentials')
                return redirect('/Login/')
    return render(request, 'App/Login.html')

def logoutview(request):
    logout(request)
    return HttpResponseRedirect(reverse('Login'))

def newScrap(request):
    s = Asset.objects.filter(status = 1)
    context = {
        's':s,
    }
    global enter
    global r
    if 'search' in request.POST:
        enter = request.POST["enter"]
        print(enter)
        t = Stock.objects.get(id=enter)
        r = Asset.objects.get(aid=t)
        context = {
            's':s,
            'r':r,
        }
    if 'submit' in request.POST:
        if (Scrap.objects.filter(aid=r.aid).exists()):
            return redirect('/stock/')
        reason = request.POST["reason"]
        disposed_date = request.POST["disposed_date"]
        print(disposed_date,reason)
        t = Scrap(aid=r.aid,reason=reason,disposed_date=disposed_date)
        t.save()
        Asset.objects.filter(aid= r.aid).update(status = 0)
        return redirect('/stock/')


    return render(request, 'App/Admin/Stock/Scrap/newScrap.html',context)

def editScrap(request,pk):
    print(pk)
    r = Stock.objects.get(id =pk)
    s = Scrap.objects.get(aid = r)
    y = Asset.objects.get(aid = r)
    sdate = s.disposed_date.strftime("%Y-%m-%d")

    print(y)
    context ={
        's': s,
        'y':y,
        'sdate': sdate,
    }
    if 'submit' in request.POST:
        reason = request.POST["reason"]
        disposed_date = request.POST["disposed_date"]
        print(disposed_date,reason)
        Scrap.objects.filter(aid=r.id).update(reason=reason,disposed_date=disposed_date)
        Asset.objects.filter(aid= r.id).update(status = 0)
        return redirect('/stock/')
    return render(request, 'App/Admin/Stock/Scrap/editScrap.html',context)

def newService(request):
    s = Asset.objects.filter(status=1)
    context = {
        's': s,
    }
    global enter
    global r
    if 'search' in request.POST:
        enter = request.POST["enter"]
        print(enter)
        t = Stock.objects.get(id=enter)
        r = Asset.objects.get(aid=t)
        context = {
            's': s,
            'r': r,
        }
    if 'submit' in request.POST:
        sent_date = request.POST["sent_date"]
        received_date = request.POST["received_date"]
        price = request.POST["price"]
        if (Service.objects.filter(aid=r.aid,sent_date=sent_date).exists()):
            return redirect('/stock/')
        else:
            if sent_date < received_date:
                t= Service(aid=r.aid,sent_date=sent_date,received_date=received_date,price=price)
                t.save()
                cash = Cash(sid=r.aid, price=price, date=sent_date, type='Service')
                cash.save()
            else:
                return redirect('/newService/')

            return redirect('/stock/')
    return render(request, 'App/Admin/Stock/newService.html',context)

def newWarranty(request):
    s = Asset.objects.exclude(status=0)
    context = {
        's': s,
    }
    global enter
    global r
    if 'search' in request.POST:
        enter = request.POST["enter"]
        print(enter)
        t = Stock.objects.get(id=enter)
        r = Asset.objects.get(aid=t)
        war = r.warranty_date.strftime("%Y-%m-%d")
        context = {
            's': s,
            'r': r,
            'war' :war,
        }

    if 'submit' in request.POST:
        print("hi1")
        price = request.POST["price"]
        extension_date = request.POST["extension_date"]
        print(str(r.warranty_date))
        if str(r.warranty_date) < extension_date:
            print("hi2")
            t = Warranty(aid=r.aid,extension_date=extension_date,price=price)
            t.save()

            Asset.objects.filter(aid = r.aid).update(warranty_date = extension_date)
            cash = Cash(sid=r.aid, price=price, date=date.today(), type='Warranty Extension')
            cash.save()
        else:
            return redirect('/newWarranty/')

        return redirect('/stock/')


    return render(request, 'App/Admin/Stock/newWarranty.html',context)

def addStock(request):
    s = Consumables.objects.filter(old_quantity=0)
    context = {
        's': s,
    }
    global enter
    global r
    if 'search' in request.POST:
        enter = request.POST["enter"]
        print(enter)
        t = Stock.objects.get(id=enter)
        r = Consumables.objects.get(cid=t)
        sdate = r.cid.dop.strftime("%Y-%m-%d")
        exp = r.new_expiry.strftime("%Y-%m-%d")

        context = {
            's': s,
            'r': r,
            'sdate' :sdate,
            'exp' : exp
        }
    if 'submit' in request.POST:
        new_quantity = request.POST["new_quantity"]
        dop = request.POST["dop"]
        new_expiry = request.POST["new_expiry"]

        if str(r.old_expiry) < new_expiry and new_expiry > dop:
            Consumables.objects.filter(cid =r.cid).update(new_quantity=new_quantity,new_expiry=new_expiry,old_quantity = r.new_quantity,old_expiry=r.new_expiry)
            cash = Cash(sid=r.cid, date=date.today(), type='Consumable Addition',price = r.cid.product_price)
            cash.save()
            return redirect('/stock/')

        else:
            return redirect('/stock/')
    return render(request, 'App/Admin/Stock/addStock.html',context)

def allocate(request):
    sup = Employee.objects.all()

    context = {
        'ls' :sup,
    }

    global enter
    global r
    if 'search' in request.POST:
        enter = request.POST["enter"]
        print(enter)
        t = User.objects.get(username =enter)
        r = Employee.objects.get(username = t)
        context = {
            'ls': sup,
            'r': r,
        }
    if 'submit' in request.POST:
        final = request.POST["final"]
        t = Stock.objects.get(id = final)
        if t.product_type == 'Asset':
            print('Asset')
            y = Asset.objects.get(aid = t)
            if y.status ==1:
                a = Allocation(aid=r.username,stock = t,allocated_date = date.today(),return_date=datetime.date(2000, 1, 1),returned=0)
                a.save()
                Asset.objects.filter(aid=y.aid).update(status = 2)
                return redirect('/Admin_Dashboard/')
        else:
            print(t,'Consumables')
            y = Consumables.objects.get(cid = t)
            if y.old_quantity > 0:
                print("old")
                a = Allocation(aid=r.username,stock = t,allocated_date = date.today(),return_date=datetime.date(2000, 1, 1),returned=0)
                a.save()
                old =y.old_quantity-1
                Consumables.objects.filter(cid=y.cid).update(old_quantity = old)
                return redirect('/Admin_Dashboard/')

            else:
                print("new")
                a = Allocation(aid=r.username,stock = t,allocated_date = date.today(),return_date=datetime.date(2000, 1, 1),returned=0)
                a.save()
                new = y.new_quantity -1
                Consumables.objects.filter(cid=y.cid).update(new_quantity = new)
                return redirect('/Admin_Dashboard/')


    return render(request,'App/Admin/Allocate_and_deallocate/allocate.html',context)

def deallocate(request):
    s = Stock.objects.filter(product_type='Asset')
    a = Allocation.objects.filter(returned=0, stock_id__in=s)
    context = {}
    global final
    if 'search' in request.POST:
        final = request.POST["final"]
        print(final)
        try:
            q = a.filter(stock=final)
            print(q)
            context = {
                'q': q[0],
            }
        except:
            pass
    if 'submit' in request.POST:
        print("hi")
        a.filter(stock = final).update(returned =1,return_date = date.today())
        Asset.objects.filter(aid = final).update(status = 1)
        return redirect('/Admin_Dashboard/')

    return render(request,'App/Admin/Allocate_and_deallocate/deallocate.html',context)

def newAllocator(request):
    sup = User.objects.filter(is_staff = False)
    context = {
        'ls': sup,
    }
    global enter
    global r
    try:
        if 'search' in request.POST:
            enter = request.POST["enter"]
            print(enter)
            t = User.objects.get(username =enter)
            context = {
                'ls': sup,
                't': t,
            }
            print(t.username,t.first_name)
    except:
        pass

    if 'submit' in request.POST:
        User.objects.filter(username =enter).update(is_staff = True)
        return redirect('/Admin_Dashboard/')

    return render(request, 'App/Admin/Employee/newAllocator.html',context)

def allocationApproval(request):
    r = Allocation_approval.objects.filter(reason=0)
    context = {
        'ls': r,
    }
    return render(request, 'App/Admin/Approval/allocationApproval.html',context)

def a_allow(request,pk):
    print(pk)
    r = Allocation_approval.objects.get(all_req = pk)
    print(r.aid)
    a = Allocation(aid=r.aid, stock=r.stock, allocated_date=date.today(),return_date=datetime.date(2000, 1, 1), returned=0)
    a.save()
    t = Stock.objects.get(id=r.stock.id)
    p=Asset.objects.filter(aid=t).update(status = 2)
    Allocation_approval.objects.filter(all_req=pk).update(reason = 1)

    return redirect('/allocationApproval/')
    return render(request, 'App/Admin/Approval/a_allow.html')

def a_no(request,pk):
    print(pk)
    r = Allocation_approval.objects.filter(all_req=pk)
    print(r)
    Allocation_approval.objects.filter(all_req=pk).update(reason = 1)
    return redirect('/allocationApproval/')
    return render(request, 'App/Admin/Approval/a_no.html')

def depreciationApproval(request):
    asset = Asset.objects.all()
    ls = []
    ls1 = []
    for i in asset:
        to = date.today()
        fro = i.aid.dop
        age = (to - fro).days
        t = math.floor(age//365)
        if t > i.depActive:
            ls.append(i)
            u = i.aid.product_price - (i.aid.product_price * i.depreciation/100)
            ls1.append(u)
    ls2 = zip(ls,ls1)
    context = {
        'ls':ls2,
    }
    return render(request, 'App/Admin/Approval/depreciationApproval.html',context)

def editDepreciation(request,pk):
    su = Stock.objects.get(id=pk)
    emp = Asset.objects.get(aid=su)
    sdate = su.dop.strftime("%Y-%m-%d")
    con = Supplier.objects.exclude(product_type='Consumables')
    exp = emp.warranty_date.strftime("%Y-%m-%d")
    context = {
        'ls': emp,
        'sdate': sdate,
        'con': con,
        'exp': exp,
    }
    if request.method == 'POST':

        depreciation = request.POST["depreciation"]
        if (len(depreciation) == 0 ):
            messages.info(request, "Don't leave the credentials empty!")
            return redirect('/depreciationApproval/')
        Asset.objects.filter(aid=su).update( depreciation=depreciation)
        return redirect('/depreciationApproval/')

    return render(request, 'App/Admin/Stock/editDepreciation.html',context)

def loader(request,pk,dp):
    print(pk,dp)
    su = Stock.objects.get(id=pk)
    t =Asset.objects.get(aid=su)
    to = date.today()
    fro = t.aid.dop
    age = (to - fro).days
    th = math.floor(age // 365)
    print(age,th,t.depActive)
    price =t.aid.product_price - (t.aid.product_price * t.depreciation/100)
    Stock.objects.filter(id = pk).update(product_price = price)
    Asset.objects.filter(aid=su).update(depActive = th)

    return redirect('/depreciationApproval/')

    return render(request, 'App/Admin/Approval/loader.html')

def req(request,pk):
    print(pk)
    Request.objects.filter(id=pk).update(validation = 1)
    return redirect('/allocator_dashboard/')

    return render(request, 'App/Admin/Approval/loader.html')


def rap(request,pk):
    t = Request.objects.get(id=pk)
    print(t)
    r1 = t.request.split(':')
    emp = User.objects.get(username=t.aid)
    sto = Stock.objects.get(id=r1[0])
    print(emp)
    print(sto)

    a = Allocation_approval(aid=emp, stock=sto, request_date=date.today(), reason=0)
    a.save()
    Request.objects.filter(id=pk).update(validation=2)

    return redirect('/allocator_dashboard/')
    return render(request, 'App/Admin/Approval/loader.html')
def Admin_Dashboard(request):
    c = Consumables.objects.all()
    a = Allocation.objects.filter(returned = 1)
    w = Asset.objects.order_by('warranty_date')
    scr = Asset.objects.filter(status=0)
    ava =  Asset.objects.filter(status=1)
    all =  Asset.objects.filter(status=2)
    data = [len(ava),len(all),len(scr)]
    print(data)

    context = {
        'c' :c,
        'a' :a,
        'w' :w,
        'data': data,
    }



    return render(request, 'App/Admin/Dashboard/Admin_Dashboard.html',context)

def viewStock(request,pk):
    a = Asset.objects.get(aid = pk)
    pur = a.aid.dop.strftime("%Y-%m-%d")
    war = a.warranty_date.strftime("%Y-%m-%d")
    to = date.today()
    fro = a.aid.dop
    age = (to - fro).days
    sc = ''
    r = ''
    allo =''
    ser =''
    w=''
    try:
        sc = Scrap.objects.get(aid = a.aid)
        r = sc.disposed_date.strftime("%Y-%m-%d")

    except:
        pass

    try:
        allo = Allocation.objects.filter(stock = a.aid)
        print(allo)
    except:
        pass

    try:
        ser = Service.objects.filter(aid = a.aid)
    except:
        pass

    try:
        w = Warranty.objects.filter(aid = a.aid)
        print(w)
    except:
        pass
    context = {
        'a':a,
        'pur':pur,
        'war': war,
        'age' : age,
        'sc' : r,
        'allo': allo,
        'ser' :ser,
        'w':w,
        'active': 'badge badge-pill-success',
        'exp': 'badge badge-pill-danger',
        'net': 'badge badge-pill-info',
        'status': 1,
    }


    return render(request, 'App/Admin/Stock/viewStock.html',context)

def viewConsumable(request,pk):
    c = Consumables.objects.get(cid = pk)
    allo=''
    try:
        allo = Allocation.objects.filter(stock=c.cid)
        print(allo)
    except:
        pass
    context ={
        'c':c,
        'allo':allo,
    }
    return render(request, 'App/Admin/Stock/viewConsumable.html',context)

def employee_dashboard(request):
    id = request.user
    all = Allocation.objects.filter(aid=id, returned=0)
    print(id, all)
    t = []
    for i in all:
        to = date.today()
        fro = i.allocated_date
        d = (to - fro).days
        t.append(d)
    ls = zip(all, t)

    re = Request.objects.filter(aid = id)

    context = {
        'ls': ls,
        're' :re,
        '1':1,
        '2':2,
        'active': 'badge badge-pill-success',
        'exp': 'badge badge-pill-danger',
        'net': 'badge badge-pill-info',
    }
    return render(request, 'App/Employee/employee_dashboard.html',context)

def allocator_dashboard(request):
    c = Consumables.objects.all()
    w = Asset.objects.order_by('warranty_date')

    r = Request.objects.filter(validation = 0)

    context = {
        'c': c,
        'w': w,
        'r' :r,
    }

    return render(request, 'App/Allocator/allocator_dashboard.html',context)

def allocation_history(request):
    id = request.user
    all = Allocation.objects.filter(aid = id,returned =1)
    t =[]
    for i in all:
        to = i.return_date
        fro = i.allocated_date
        d = (to - fro).days
        print(i)
        print(d)
        t.append(d)
    ls = zip(all,t)
    context ={
        'ls':ls,
    }
    return render(request, 'App/Employee/allocation_history.html',context)

def edit_profile(request):
    id = request.user
    sup = ''
    try:
        sup = Employee.objects.get(username=id)
    except:
        pass
    p = Employee.objects.all()
    context = {
        'ls': sup,
        'ps': p,
    }

    if request.method == 'POST':
        mobile = request.POST["mobile"]
        address = request.POST["address"]
        pincode = request.POST["pincode"]
        print(mobile,address,pincode)
        Employee.objects.filter(username=id).update(mobile=mobile,address=address, pincode=pincode)
        return redirect('/employee_dashboard/')
    return render(request, 'App/Employee/edit_profile.html',context)

def request(request):
    re= Request.objects.all()
    s = Asset.objects.all()
    id = request.user
    print(id.first_name)
    length = len(re) + 1
    context ={
        'length':length,
        's': s,
        'one' :1,
    }
    if request.method == 'POST':
        reques = request.POST["reques"]
        print(reques)
        t = Request(id = length,aid =id,request=reques,validation =0,date= date.today(),remark='')
        t.save()
        return redirect('/employee_dashboard/')

    return render(request, 'App/Employee/request.html',context)

def change_password(request):
    print(User.username)
    if request.method == 'POST':
        op = request.POST['op']
        np = request.POST['np']
        user = auth.authenticate(username=User.username, password=op)
        if (len(op) == 0 or len(np) == 0):
            messages.info(request, 'Do not leave Credentials empty!')
            return HttpResponseRedirect('/login/')
        else:
            if  user == True:
                print("hi")

    return render(request, 'App/change_password.html')

def a_allocate(request):
    sup = Employee.objects.all()

    context = {
        'ls': sup,
    }

    global enter
    global r
    if 'search' in request.POST:
        enter = request.POST["enter"]
        print(enter)
        t = User.objects.get(username=enter)
        r = Employee.objects.get(username=t)
        context = {
            'ls': sup,
            'r': r,
        }
    if 'submit' in request.POST:
        final = request.POST["final"]
        t = Stock.objects.get(id=final)
        if t.product_type == 'Asset':
            print('Asset')
            y = Asset.objects.get(aid=t)
            if y.status == 1:
                '''a = Allocation(aid=r.username, stock=t, allocated_date=date.today(),
                               return_date=datetime.date(2000, 1, 1), returned=0)
                a.save()
                Asset.objects.filter(aid=y.aid).update(status=2)'''

                a = Allocation_approval(aid=r.username,stock=t,request_date=date.today(),reason=0)
                a.save()
                return redirect('/allocator_dashboard/')
        else:
            print(t, 'Consumables')
            y = Consumables.objects.get(cid=t)
            if y.old_quantity > 0:
                print("old")
                a = Allocation(aid=r.username, stock=t, allocated_date=date.today(),
                               return_date=datetime.date(2000, 1, 1), returned=0)
                a.save()
                old = y.old_quantity - 1
                Consumables.objects.filter(cid=y.cid).update(old_quantity=old)
                return redirect('/allocator_dashboard/')

            else:
                print("new")
                a = Allocation(aid=r.username, stock=t, allocated_date=date.today(),
                               return_date=datetime.date(2000, 1, 1), returned=0)
                a.save()
                new = y.new_quantity - 1
                Consumables.objects.filter(cid=y.cid).update(new_quantity=new)
                return redirect('/allocator_dashboard/')

    return render(request,'App/Allocator/Allocate_and_deallocate/a_allocate.html',context)

def a_deallocate(request):
    s = Stock.objects.filter(product_type='Asset')
    a = Allocation.objects.filter(returned=0, stock_id__in=s)
    context = {}
    global final
    if 'search' in request.POST:
        final = request.POST["final"]
        print(final)
        try:
            q = a.filter(stock=final)
            print(q)
            context = {
                'q': q[0],
            }
        except:
            pass
    if 'submit' in request.POST:
        a.filter(stock=final).update(returned=1, return_date=date.today())
        Asset.objects.filter(aid=final).update(status=1)
        return redirect('/allocator_dashboard/')

    return render(request,'App/Allocator/Allocate_and_deallocate/a_deallocate.html',context)

def a_view_stock(request):
    a = Asset.objects.all()
    c = Consumables.objects.all()

    context = {
        'a': a,
        'c': c,
        'active': 'badge badge-pill-success',
        'exp': 'badge badge-pill-danger',
        'net': 'badge badge-pill-info',
        'one': 1,
        'two': 2,
    }
    return render(request,'App/Allocator/a_view_stock.html',context)

def chart_allocation(request):
    c = Cash.objects.all()
    p = 0
    s = 0
    w = 0
    cu =0
    try:
        for i in c:
            if i.type == 'Purchase':
                p = p+1
            elif i.type == 'Service':
                s = s +1
            elif i.type == 'Warranty Extension':
                w = w +1
            elif i.type == 'Consumable Addition':
                cu = cu +1
            print(i.type)
    except:
        pass


    data = [p,cu,w,s]
    context ={
        'data': data,
    }
    return render(request,'App/Admin/Report/chart_allocation.html',context)

def chart_overall(request):
    s = len(Scrap.objects.all())
    a = len(Asset.objects.all())
    c = len(Consumables.objects.all())
    a = a-s

    data = [a,c,s]
    context ={
        'data':data,
    }

    return render(request,'App/Admin/Report/chart_overall.html',context)

def overallInventory(request):

    ls1 = []
    ls2 = []

    stock = ''
    try:
        stock = Stock.objects.all()
        for j in stock:
            if j.product_type == 'Asset':
                asset = Asset.objects.get(aid = j.id)
                ls2.append(asset)
                try:
                    a = Allocation.objects.filter(stock=j.id,returned = 0).count()
                    ls1.append(a)
                except:
                    pass


            else:
                con = Consumables.objects.get(cid = j.id)
                try:
                    a = Allocation.objects.filter(stock = j.id).count()
                    ls1.append(a)
                except:
                    pass
                ls2.append(con)
    except:
        pass

    ls = zip(ls2,ls1)
    context = {
        'ls': ls,
        'active': 'badge badge-pill-success',
        'Asset': 'Asset',
        '0' : 0,
    }


    return render(request,'App/Admin/Report/overallInventory.html',context)

def rasset(request):
    asset = Asset.objects.all()
    ls1 = []
    ls2 = []
    dat = []
    for j in asset:
        try:
            allocation = Allocation.objects.filter(stock=j.aid).order_by('-allocated_date')
            for i in allocation:
                if (i.stock.product_type == 'Asset'):
                    print(i.stock.id, i.allocated_date,i.stock.product_name,i.aid.first_name)
                    ls1.append(i)
                    ls2.append(j)
                    to = date.today()
                    fro = j.aid.dop
                    d= (to - fro).days
                    dat.append(d)
                    break
            else:
                print("hi")

                ls1.append(j)
                ls2.append(j)
                to = date.today()
                fro = j.aid.dop
                d = (to - fro).days
                dat.append(d)

        except:
            pass
    print(dat)
    ls = zip(ls1,ls2,dat)
    print(ls)
    context = {
        'ls' : ls,
        'active': 'badge badge-pill-success',
        'exp': 'badge badge-pill-danger',
        'net': 'badge badge-pill-info',
        'one': 1,
        'two': 2,
    }

    return render(request,'App/Admin/Report/rasset.html',context)

def rscrap(request):
    scrap = Scrap.objects.all()
    asset = Asset.objects.all()
    ls1 = []
    ls2 = []
    dat = []
    for i in  asset:
        for j in scrap:
            if (i.aid.id == j.aid.id):
                print(i.aid.id , j.aid.id)
                ls1.append(i)
                sc = Stock.objects.get(id = i.aid.id)
                t = Scrap.objects.get(aid = sc)
                ls2.append(t)

    ls = zip(ls1,ls2)
    context = {
        'ls': ls,
        'active': 'badge badge-pill-success',
        'exp': 'badge badge-pill-danger',
        'net': 'badge badge-pill-info',
        'zero': 0,

    }

    return render(request, 'App/Admin/Report/rscrap.html', context)

def rconsumable(request):
    c = Consumables.objects.all()
    context = {
        'c' :c,
        'active': 'badge badge-pill-success',
        'exp': 'badge badge-pill-danger',
        'net': 'badge badge-pill-info',
    }
    return render(request,'App/Admin/Report/rconsumable.html',context)

def bulk(request):
    context={}
    if request.method == "POST":
        try:
            my_uploaded_file = request.FILES['my_uploaded_file']
            ls1 = []
            ls2 = []
            pwd1 = 'verticurl'
            print(my_uploaded_file)
            file = my_uploaded_file.read().decode('UTF-8')
            file = file.splitlines()
            x = list(csv.reader(file))
            context = {
                'ls1': ls1,
                       }
            if str(my_uploaded_file) == 'sample_supplier.csv':
                for i in x:
                    if i == x[0]:
                        ls1 = x[0]
                        context = {
                            'ls1': ls1,
                        }
                        pass
                    else:
                        print(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7])

                        if (Supplier.objects.filter(GST=i[2]).exists()) or (Supplier.objects.filter(sid=i[0]).exists()):
                            i[8] = 'Duplicate entry'
                            ls2.append(i)
                        elif ((len(i[0])==0) or (len(i[1])==0) or (len(i[2])==0) or (len(i[3])==0) or (len(i[4])==0) or (len(i[5])==0) or (len(i[6])==0) or (len(i[7])==0)):
                            i[8] = 'Blank Entry'
                            ls2.append(i)
                        else:
                            s = Supplier(sid = i[0], name = i[1], GST = i[2],product_type = i[3],
                                         email = i[4], mobile = i[5], address = i[6], pincode =i[7])
                            s.save()
                        context = {
                            'ls1': ls1,
                            'ls2': ls2,
                        }
            if str(my_uploaded_file) == 'sample_consumable.csv':
                for i in x:
                    if i == x[0]:
                        ls1 = x[0]
                        context = {
                            'ls1': ls1,
                        }
                        pass
                    else:
                        if (Stock.objects.filter(id=i[0]).exists()):
                            i[8] = 'Duplicate entry'
                            ls2.append(i)
                        elif ((len(i[0])==0) or (len(i[1])==0) or (len(i[2])==0) or (len(i[3])==0) or (len(i[4])==0) or (len(i[5])==0) or (len(i[6])==0) or (len(i[7])==0)):
                            i[8] = 'Blank Entry'
                            ls2.append(i)
                        else:
                            print(i)
                            se = Supplier.objects.get(sid=i[3])
                            if se.product_type == 'Asset':
                                i[8] = 'Incorrect Supplier Entry'
                                ls2.append(i)
                            else:
                                r1 = i[6].split('-')
                                r1.reverse()
                                r1 = '-'.join(r1)

                                r2 = i[7].split('-')
                                r2.reverse()
                                r2 = '-'.join(r2)
                                print(i[2])
                                t = list(i[2])
                                m = []
                                for c in t:
                                    if c != ',':
                                        m.append(c)
                                m = ''.join(m)
                                s = Stock(id=i[0], product_name=i[1], product_price=float(m),product_type='Consumables', dop=r1, supplier=se,temp=0)
                                s.save()
                                ae = Stock.objects.get(id=i[0])
                                c = Consumables(cid=ae, old_quantity=0, old_expiry=datetime.date(2000, 1, 1),
                                                new_expiry=r2, new_quantity=i[4], min_count=i[5])
                                c.save()
                                cash = Cash(sid=ae, price=float(m), date=r1, type='Purchase')
                                cash.save()
                                continue


                        context = {
                            'ls1': ls1,
                            'ls2': ls2,
                        }
            if str(my_uploaded_file) == 'sample_asset.csv':
                for i in x:
                    if i == x[0]:
                        ls1 = x[0]
                        context = {
                            'ls1': ls1,
                        }
                        pass
                    else:
                        if (Stock.objects.filter(id=i[0]).exists()):
                            i[8] = 'Duplicate entry'
                            ls2.append(i)
                        elif ((len(i[0])==0) or (len(i[1])==0) or (len(i[2])==0) or (len(i[3])==0) or (len(i[4])==0) or (len(i[5])==0) or (len(i[6])==0) or (len(i[7])==0)):
                            i[8] = 'Blank Entry'
                            ls2.append(i)
                        else:
                            print(i)
                            se = Supplier.objects.get(sid=i[3])
                            if se.product_type == 'Consumables':
                                i[8] = 'Incorrect Supplier Entry'
                                ls2.append(i)
                            else:
                                r1 = i[6].split('-')
                                r1.reverse()
                                r1 = '-'.join(r1)

                                r2 = i[7].split('-')
                                r2.reverse()
                                r2 = '-'.join(r2)

                                t = list(i[2])
                                m = []
                                for c in t:
                                    if c != ',':
                                        m.append(c)
                                m = ''.join(m)

                                t1 = list(i[4])
                                m1 = []
                                for c1 in t1:
                                    if c1 != ',':
                                        m1.append(c1)
                                m1 = ''.join(m1)


                                s = Stock(id=i[0], product_name=i[1], product_price=float(m),product_type='Asset', dop=r1, supplier=se,temp=0)
                                s.save()
                                ae = Stock.objects.get(id=i[0])
                                a = Asset(aid=ae, serial_number=m1, depreciation=i[5],
                                          warranty_date=r2, status=1, depActive=0, age=0)
                                a.save()
                                cash = Cash(sid=ae, price=float(m), date=r1, type='Purchase')
                                cash.save()
                                continue


                        context = {
                            'ls1': ls1,
                            'ls2': ls2,
                        }
            if str(my_uploaded_file) == 'sample_employee.csv':
                for i in x:
                    if i == x[0]:
                        ls1 = x[0]
                        context = {
                            'ls1': ls1,
                        }
                        pass
                    else:
                        if User.objects.filter(username=i[0]).exists():
                            i[11] = 'Duplicate entry'
                            ls2.append(i)
                        elif ((len(i[0])==0) or (len(i[1])==0) or (len(i[2])==0) or (len(i[3])==0) or (len(i[4])==0) or (len(i[5])==0) or (len(i[6])==0) or (len(i[7])==0) or (len(i[8])==0)or (len(i[9])==0)):
                            i[11] = 'Blank Entry'
                            ls2.append(i)
                        else:
                            print(i)
                            r1 = i[7].split('-')
                            r1.reverse()
                            r1 = '-'.join(r1)

                            user = User.objects.create_user(first_name=i[1], username=i[0],
                                                            email=i[4], password=pwd1, is_staff=False,
                                                            is_superuser=False)
                            user.save()
                            u = User.objects.get(username=i[0])
                            emp = Employee(username=u, Department=i[2], Designation=i[3],
                                           mobile=i[5], line_manager=i[6], doj=r1,
                                           address=i[8], pincode=i[9])
                            emp.save()

                            if (len(i[10]) != 0):
                                y = Stock.objects.get(id=i[10])
                                print(y)
                                if Stock.objects.filter(id=i[10]).exists():

                                    if Asset.objects.filter(aid=y,status=1).exists():
                                        a = Allocation(aid=u, stock=y, allocated_date=date.today(),
                                                       return_date=datetime.date(2000, 1, 1), returned=0)

                                        a.save()

                                        Asset.objects.filter(aid=y).update(status=2)

                                    else:
                                        i[11] = 'No Stock'
                                        ls2.append(i)
                                else:
                                    i[11] = 'Incorrect stock ID'
                                    ls2.append(i)
                        context = {
                            'ls1': ls1,
                            'ls2': ls2,
                        }

        except:
            pass
    return render(request,'App/Admin/bulk.html',context)
