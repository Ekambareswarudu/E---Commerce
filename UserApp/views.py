from django.shortcuts import render
import pymysql
from AdminApp.Database import DBConnection
import base64
# Create your views here.
def login(request):
    return render(request,'UserApp/Login.html')

def register(request):
    return render(request,'UserApp/Register.html')

def regaction(request):
    name=request.POST['name']
    email=request.POST['email']
    mobile=request.POST['mobile']
    address=request.POST['address']
    username=request.POST['uname']
    password=request.POST['pwd']

    con=DBConnection()
    cur=con.cursor()
    cur.execute("select * from user where email='"+email+"'")
    data = cur.fetchone()
    if data is not None:
        context={'msg':'User Email Already Exist...!!!'}
        return render(request,'UserApp/Register.html',context)
    else:
        cur.execute("insert into user values(null,'"+name+"','"+email+"','"+mobile+"','"+address+"','"+username+"','"+password+"')")
        con.commit()
        context={'msg':'Registration Successful...!!!'}
        return render(request,'UserApp/Register.html',context)

def loginaction(request):
    username=request.POST['username']
    password=request.POST['password']
    con=DBConnection()
    cur = con.cursor()
    cur.execute("select * from user where username='"+username+"' and password='"+password+"'")
    data = cur.fetchone()
    tdata="<table><tr><th>Category</th><th>Product Name</th></tr>"
    global d
    if data is not None:
        uid=str(data[0])
        request.session['userid'] = uid
        request.session['email'] = data[2]
        cur = con.cursor()
        cur.execute("select * from search_history where user_id='"+uid+"'")
        d=cur.fetchall()
        cat = None
        if cat is not None:
            for dd in d:
                cat=dd[2]
            cur.execute("select count(category)>5, category, pname from search_history where category='"+cat+"'")
            data=cur.fetchall()
            for s in data:
                tdata+="<tr><td>"+str(s[1])+"</td><td>"+str(s[2])+"</td></tr>"
            tdata+="</table>"
        context={'data':tdata}
        return render(request,'UserApp/UserHome.html',context)
    else:
        context={'msg':'Login Failed...!!!'}
        return render(request,'UserApp/Login.html',context)

def UserHome(request):
    uid=request.session['userid']
    con=DBConnection()
    cur = con.cursor()
    cur.execute("select * from search_history where user_id='"+uid+"'")
    d=cur.fetchall()
    global cat
    for dd in d:
        cat=dd[2]
    cur.execute("select count(category)>5, category, pname from search_history where category='"+cat+"'")
    data=cur.fetchall()
    for s in data:
        tdata+="<tr><td>"+str(s[1])+"</td><td>"+str(s[2])+"</td></tr>"
    tdata+="</table>"
    context={'data':tdata}
    return render(request,'UserApp/UserHome.html')


def Profile(request):
    userid=request.session['userid']
    con=DBConnection()
    cur = con.cursor()
    cur.execute("select * from user where id='"+userid+"'")
    data = cur.fetchone()
    tabledata="<table><tr><th>Name</th><th>Email</th><th>Mobile</th><th>Address</th></tr>"
    if data is not None:
        tabledata+="<tr><td>"+str(data[1])+"</td><td>"+str(data[2])+"</td><td>"+str(data[3])+"</td><td>"+str(data[4])+"</td></tr>"

    tabledata+="</table>"
    context={'data':tabledata}
    return render(request,'UserApp/ViewProfile.html',context)

def Search(request):
    con=DBConnection()
    cur=con.cursor()
    cur.execute("select * from category")
    data=cur.fetchall()
    tabledata="<tr><th>Select Category</th><td><select name='category' required>" \
              "<option></option>"
    for d in data:
        tabledata+="<option>"+str(d[1])+"</option>"
    tabledata+="</select></td></tr>"
    context={'data':tabledata}
    return render(request,'UserApp/Search.html',context)

def SearchProduct(request):
    category=request.POST['category']
    con=DBConnection()
    cur=con.cursor()
    uuid=request.session['userid']
    cur.execute("select * from products where pname like'%"+category+"%' or category like '%"+category+"%'")
    data=cur.fetchall()
    tdata="<table><tr><th>Product ID</th><th>Product Category</th><th>Product Name</th><th>Product Price</th><th>Description</th><th>Image</th>" \
          "<th>Buy Product</th></tr>"
    global cate,pname
    for d in data:
        cate=d[1]
        pname=d[2]
        tdata+="</tr><td>"+str(d[0])+"</td><td>"+str(d[1])+"</td><td>"+str(d[2])+"</td><td>"+str(d[3])+"</td><td>"+str(d[4])+"</td>" \
                 "<td><a href='/userapp/viewImage?id="+str(d[0])+"'>View Image</a></td>" \
                  "<td><a href='/userapp/BuyProduct?ppid="+str(d[0])+"&price="+str(d[3])+"&pname="+str(d[2])+"'>Buy</a></td></tr>"
    tdata+="</table>"

    cur.execute("insert into search_history values(null,'"+uuid+"','"+cate+"','"+pname+"')")
    con.commit()

    context={'data':tdata}
    return render(request,'UserApp/ViewProduct.html',context)

def viewImage(request):
    pid=request.GET['id']
    con=DBConnection()
    cur=con.cursor()
    cur.execute("select image from products where id='"+pid+"'")
    blob_data = cur.fetchone()[0]
    blob_base64 = base64.b64encode(blob_data).decode('utf-8')
    return render(request, 'UserApp/ViewProduct.html', {'blob_base64': blob_base64})


def BuyProduct(request):
    product_pid=request.GET['ppid']
    product_price=request.GET['price']
    product_pname=request.GET['pname']
    context={'pid':product_pid,'price':product_price,'pname':product_pname}
    return render(request,'UserApp/BuyProduct.html', context)

def BuyAction(request):
    userid = request.session['userid']
    p_pid1 = request.POST['ppid']
    p_price1 = request.POST['price']
    p_pname1 = request.POST['pname']
    quantity = request.POST['quantity']

    con = DBConnection()
    cur = con.cursor()
    cur.execute("insert into buy_product values(null,'"+userid+"','"+p_pid1+"','"+p_pname1+"','"+p_price1+"','"+quantity+"')")
    con.commit()
    context = {'msg':'Product Purchased Successfully...!!'}
    return render(request,'UserApp/BuyProduct.html', context)

def ViewBookedProducts(request):
    userid=request.session['userid']
    con=DBConnection()
    cur=con.cursor()
    cur.execute("select * from buy_product pb, products p where pb.p_id=p.id and pb.user_id='"+userid+"'")
    data=cur.fetchall()
    tdata="<table><tr><th>Product ID</th><th>Product Category</th><th>Product Name</th><th>Product Price</th><th>Quantity</th><th>Description</th><th>Image</th>" \
          "</tr>"
    for d in data:
        tdata+="</tr><td>"+str(d[6])+"</td><td>"+str(d[7])+"</td><td>"+str(d[8])+"</td><td>"+str(d[9])+"</td><td>"+str(d[5])+"</td><td>"+str(d[10])+"</td>" \
                 "<td><a href='/userapp/viewImage?id="+str(d[6])+"'>View Image</a></td>" \
                  "</tr>"
    tdata+="</table>"
    context={'data':tdata}
    return render(request,'UserApp/ViewBuyProduct.html',context)
