from django.shortcuts import render
import pymysql
from AdminApp.Database import DBConnection
import base64

# Create your views here.
def index(request):
    return render(request,'index.html')

def login(request):
    return render(request,'AdminApp/Login.html')

def AdminHome(request):
    return render(request,'AdminApp/AdminHome.html')
    
def loginaction(request):
    uname=request.POST['uname']
    pwd=request.POST['pwd']
    if uname=='Admin' and pwd == 'Admin':
        return render(request,'AdminApp/AdminHome.html')
    else:
        context={'msg':'Login Failed...!!'}
        return render(request,'AdminApp/Login.html')

def AddCategory(request):
    return render(request,'AdminApp/AddCategory.html')


def categoryAction(request):
    uname=request.POST['cat']
    con=DBConnection()
    cur=con.cursor()
    cur.execute("select * from category where category='"+uname+"'")
    data=cur.fetchone()
    if data is not None:
        context={'msg':'Category Already Added...!!'}
        return render(request,'AdminApp/AddCategory.html',context)
    else:
        cur.execute("insert into category values(null,'"+uname+"')")
        con.commit()
        context={'msg':'Category Successfully Added...!!'}
        return render(request,'AdminApp/AddCategory.html',context)


def UploadProducts(request):

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
    return render(request,'AdminApp/AddProduct.html',context)

def productAction(request):
    if request.method == 'POST' and request.FILES['image']:
        category=request.POST['category']
        pname=request.POST['pname']
        pdesc=request.POST['pdesc']
        price=request.POST['price']
        data = request.FILES['image'].read()
        con=DBConnection()
        cur=con.cursor()
        cur.execute('insert into products values(null,%s,%s,%s,%s,%s)',(category,pname,price,pdesc,data))
        con.commit()
        context={'msg':'Product Successfully Added...!!'}
        return render(request,'AdminApp/AddProduct.html',context)

def ViewProducts(request):
    con=DBConnection()
    cur=con.cursor()
    cur.execute("select * from products")
    data=cur.fetchall()
    tdata="<table><tr><th>Product ID</th><th>Product Category</th><th>Product Name</th><th>Product Price</th><th>Description</th><th>Image</th></tr>"
    for d in data:
        tdata+="</tr><td>"+str(d[0])+"</td><td>"+str(d[1])+"</td><td>"+str(d[2])+"</td><td>"+str(d[3])+"</td><td>"+str(d[4])+"</td>" \
                 "<td><a href='/viewImage?id="+str(d[0])+"'>View Image</a></td></tr>"
    tdata+="</table>"
    context={'data':tdata}
    return render(request,'AdminApp/ViewProduct.html',context)

def viewImage(request):
    pid=request.GET['id']
    con=DBConnection()
    cur=con.cursor()
    cur.execute("select image from products where id='"+pid+"'")
    blob_data = cur.fetchone()[0]
    blob_base64 = base64.b64encode(blob_data).decode('utf-8')
    return render(request, 'AdminApp/ViewProduct.html', {'blob_base64': blob_base64})










