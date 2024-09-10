import os
import re
from datetime import date,timedelta
import pandas as pd
from flask import *
from flask_mail import *
import mysql.connector
db = mysql.connector.connect(host="localhost",user="root",password="root",port=3307,database="oss")
cur = db.cursor()
app=Flask('__name__')
app.config['products'] = "static/products"
app.secret_key="jbvdfvguisdf03r9238r34234654ZSCSDIOCVSL"
import random
import smtplib



def password_check(passwd):

    SpecialSym =['$', '@', '#', '%']
    val = True

    if len(passwd) < 6:
        print('length should be at least 6')
        val = False

    if len(passwd) > 20:
        print('length should be not be greater than 8')
        val = False

    if not any(char.isdigit() for char in passwd):
        print('Password should have at least one numeral')
        val = False

    if not any(char.isupper() for char in passwd):
        print('Password should have at least one uppercase letter')
        val = False

    if not any(char.islower() for char in passwd):
        print('Password should have at least one lowercase letter')
        val = False

    if not any(char in SpecialSym for char in passwd):
        print('Password should have at least one of the symbols $@#')
        val = False
    if val:
        return val

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/adminlog",methods=["POST","GET"])
def adminlog():
    if request.method == "POST":
        adminemail = request.form["adminemail"]
        adminpassword = request.form["adminpassword"]
        if adminemail =="admin@gmail.com" and adminpassword =="admin":
            return render_template("adminhome.html",admin=adminemail)
        msg = "Details are not valid"
        return render_template("adminlog.html",msg = msg)
    return render_template("adminlog.html")

@app.route('/addproducts',methods=["POST","GET"])
def addproducts():
    if request.method == "POST":
        category = request.form['category']
        productid = request.form['productid']
        category = request.form['category']
        productname = request.form['productname']
        productprice = request.form['productprice']
        productdescription = request.form['productdescription']
        productimage = request.files['productimage']

        imagename = productimage.filename

        cur.execute("select * from productlist where ProductId='%s' and Category='%s'"%(productid,category))
        d = cur.fetchall()
        db.commit()
        print(d)
        if d ==[]:
            path1 = "static/products/" + imagename
            sql = "insert into productlist(ProductId,Category,ProductName,ProductPrice,ProductDescription,ProductImage,Path) values(%s,%s,%s,%s,%s,%s,%s)"
            val = (productid,category,productname,productprice,productdescription,imagename,path1)
            cur.execute(sql,val)
            db.commit()
            productimage.save(os.path.join(app.config['products'], imagename))
            return render_template('addproducts.html')
        else:
            msg = "Details Already Exists"
            return render_template('addproducts.html',msg = msg)
    return render_template('addproducts.html')


@app.route("/viewproducts")
def viewproducts():
    sql="select distinct Category from productlist"
    # sql="select distinct * from productlist where Category in(select distinct Category from productlist)"
    cur.execute(sql)
    d = cur.fetchall()
    db.commit()
    d =[j for i in d for j in i]
    new=[]
    for i in d:
        sql="select * from productlist where Category='%s' limit 1"%(i)
        cur.execute(sql)
        data = cur.fetchall()
        db.commit()
        new.extend(data)
    data = new
    return render_template("viewproducts.html",data = list(data))


@app.route("/viewcategory",methods=["POST","GET"])
def viewcategory():
    if request.method == "POST":
        category = request.form['category']
        sql = "select * from productlist where Category='%s'"%(category)
        data = pd.read_sql_query(sql,db)
        return render_template("viewcategory.html",cols=data.columns.values,rows=data.values.tolist())




@app.route("/update",methods=["POST","GET"])
def update():
    if request.method=="POST":
        productid = request.form['productid']
        sql="select * from productlist where ID='%s'"%(productid)
        cur.execute(sql)
        dc = cur.fetchall()
        db.commit()
        return render_template("update.html",data = dc)

@app.route("/updateproductdetails",methods=["POST","GET"])
def updateproductdetails():
    print("abcdefgh")
    if request.method == "POST":
        print("mmmmmmmmmmmmmmmmmmmmmmmmmmm")
        productid = request.form['productid']
        category = request.form['category']
        productname = request.form['productname']
        productprice = request.form['productprice']
        productdescription = request.form['productdescription']

        print(productid,category,productname,productprice,productdescription)
        print("-----------------------------")
        sql = "update productlist set ProductName=%s,ProductPrice=%s,ProductDescription=%s where ProductId=%s and Category=%s"
        val = (productname,productprice,productdescription,productid,category)
        cur.execute(sql,val)
        db.commit()

        return redirect(url_for('viewproducts'))



@app.route("/deleteitem",methods=["POST","GET"])
def deleteitem():
    if request.method == "POST":
        productid = request.form['productid']
        print(productid)

        sql = "delete from productlist where ID='%s'"%(productid)
        cur.execute(sql)
        db.commit()
        return redirect(url_for('viewproducts'))


@app.route("/userreg",methods=["POST","GET"])
def userreg():
    if request.method == "POST":
        username = request.form['username']
        useremail = request.form['useremail']
        userage = request.form['userage']
        usercontact = request.form['usercontact']
        useraddress = request.form['useraddress']
        userpassword = request.form['userpassword']
        Confirmpassword = request.form['Confirmpassword']
        x = re.findall("[6-9]",usercontact[0])
        if x:
            if len(usercontact) == 10:
                regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                if (re.fullmatch(regex,useremail)):
                    print("valid")
                else:
                    msg="invalid Mail Id"
                    return render_template("userreg.html",msg=msg)
                if password_check(userpassword):
                    if userpassword == Confirmpassword:
                        sql="select * from userreg where Useremail='%s' and Userpassword = '%s'"%(useremail,userpassword)
                        cur.execute(sql)
                        d = cur.fetchall()
                        db.commit()
                        if d == []:
                            sql="insert into userreg(Username,Useremail,Userage,Usercontact,Useraddress,Userpassword)values(%s,%s,%s,%s,%s,%s)"
                            val =(username,useremail,userage,usercontact,useraddress,userpassword)
                            cur.execute(sql,val)
                            db.commit()
                            return render_template("userlogin.html")
                        msg = "Details already exists"
                        return render_template("userreg.html",msg = msg)
                    msg="Password and Confirm password not matched"
                    return render_template("userreg.html",msg = msg)
                else:
                    msg="invalid Password"
                    return render_template("userreg.html",msg=msg)



            else:
                msg="contact number length is less then 10 digits"
                return render_template("userreg.html",msg=msg)
        else:
            msg="Please Check the contact number"
            return render_template("userreg.html",msg=msg)


    return render_template("userreg.html")





@app.route("/userlogin",methods=["POST","GET"])
def userlogin():
    if request.method == "POST":
        useremail = request.form['useremail']
        session['useremail'] = useremail
        userpassword = request.form['userpassword']
        sql="select * from userreg where Useremail='%s' and Userpassword = '%s'"%(useremail,userpassword)
        cur.execute(sql)
        data = cur.fetchall()
        db.commit()

        if data !=[]:
            return render_template("userhome.html",admin=useremail)
        else:
            return render_template("userlogin.html",msg="details doesn't exist")
    return render_template("userlogin.html")

@app.route("/allcategory")
def allcategory():
    sql="select distinct Category from productlist"
    # sql="select distinct * from productlist where Category in(select distinct Category from productlist)"
    cur.execute(sql)
    d = cur.fetchall()
    db.commit()
    d =[j for i in d for j in i]
    new=[]
    for i in d:
        sql="select * from productlist where Category='%s' limit 1"%(i)
        cur.execute(sql)
        data = cur.fetchall()
        db.commit()
        new.extend(data)
    data = new
    print(data)
    return render_template("allcategory.html",data = new )

@app.route("/allproducts",methods=["POST","GET"])
def allproducts():
    if request.method == "POST":
        category = request.form['category']
        sql="select * from productlist where Category='%s'"%(category)
        data = pd.read_sql_query(sql,db)
        return render_template("allproducts.html",rows = data.values.tolist())

@app.route("/submitfeedback",methods=["POST","GET"])
def submitfeedback():
    if request.method == "POST":
        productid = request.form['productid']
        category = request.form['category']
        feedback = request.form['feedback']
        print(productid,category,feedback,session['useremail'])
        sql = "insert into feedback(Productid,Category,feedback,Useremail)values(%s,%s,%s,%s)"
        val = (productid,category,feedback,session['useremail'])
        cur.execute(sql,val)
        db.commit()

        return redirect(url_for('allcategory'))

@app.route("/additem",methods=["POST","GET"])
def additem():
    if request.method == "POST":
        productid = request.form["productid"]
        category = request.form['category']
        sql="select * from userorder where Productid='%s' and Useremail='%s'"%(productid,session['useremail'])
        data = pd.read_sql_query(sql,db)
        print(productid,category)
        print(data)
        if data.empty == True:
            sql="select * from productlist where Productid='%s' and Category='%s'"%(productid,category)
            cur.execute(sql)
            d = cur.fetchall()
            db.commit()
            print(d)
            productname = d[0][3]
            productdescr = d[0][5]
            productimage = d[0][6]
            actualcost = d[0][4]
            noofitems= 1
            totalprice = d[0][4]
            sql="insert into userorder(Productid,Category,Productname,Productprice,ProductDescription,Productimage,Useremail,Productcount,Totalprice)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val=(productid,category,productname,actualcost,productdescr,productimage,session['useremail'],noofitems,totalprice)
            cur.execute(sql,val)
            db.commit()
            sql="select * from userorder where Productid='%s' and Useremail='%s'"%(productid,session['useremail'])
            d= pd.read_sql_query(sql,db)
            db.commit()
            return render_template("allproducts.html",rows = d.values.tolist())
        else:
            sql="select * from userorder where Productid='%s' and Useremail='%s'"%(productid,session['useremail'])
            cur.execute(sql)
            d= cur.fetchall()
            db.commit()

            actualcost = d[0][4]
            noofitems= int(d[0][8]) + 1
            totalprice = int(d[0][9]) + int(actualcost)
            print(actualcost,noofitems,totalprice)
            sql="update userorder set Productcount='%s',Totalprice='%s' where Productid='%s' and Useremail='%s'"%(noofitems,totalprice,productid,session['useremail'])
            cur.execute(sql)
            db.commit()
            sql="select * from userorder where Productid='%s' and Useremail='%s'"%(productid,session['useremail'])
            data = pd.read_sql_query(sql,db)
            return render_template("allproducts.html",rows = data.values.tolist())
    return render_template("allproducts.html")

@app.route("/removeitem",methods=["POST","GET"])
def removeitem():
    productid = request.form["productid"]
    category = request.form['category']
    sql="select * from userorder where Productid='%s' and Useremail='%s'"%(productid,session['useremail'])
    data = pd.read_sql_query(sql,db)
    print(data)
    if data.empty == []:
        sql="select * from productlist where Productid='%s' and Category='%s'"%(productid,category)
        cur.execute(sql)
        d = cur.fetchall()
        db.commit()
        print(d)
        productname = d[0][3]
        productdescr = d[0][5]
        productimage = d[0][6]
        actualcost = d[0][4]
        noofitems= 1
        totalprice = d[0][4]
        sql="insert into userorder(Productid,Category,Productname,Productprice,ProductDescription,Productimage,Useremail,Productcount,Totalprice)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val=(productid,category,productname,actualcost,productdescr,productimage,session['useremail'],noofitems,totalprice)
        cur.execute(sql,val)
        db.commit()
        sql="select * from userorder where Productid=s' and Useremail='%s'"%(productid,session['useremail'])
        d= pd.read_sql_query(sql,db)
        db.commit()
        return render_template("allproducts.html",rows = d.values.tolist())
    else:
        sql="select * from userorder where Productid='%s' and Useremail='%s'"%(productid,session['useremail'])
        cur.execute(sql)
        d= cur.fetchall()
        db.commit()

        actualcost = d[0][4]
        noofitems= int(d[0][8]) - 1
        totalprice = int(d[0][9]) - int(actualcost)
        print(actualcost,noofitems,totalprice)
        sql="update userorder set Productcount='%s',Totalprice='%s' where Productid='%s' and Useremail='%s'"%(noofitems,totalprice,productid,session['useremail'])
        cur.execute(sql)
        db.commit()
        sql="select * from userorder where Productid='%s' and Useremail='%s'"%(productid,session['useremail'])
        data = pd.read_sql_query(sql,db)
        return render_template("allproducts.html",rows = data.values.tolist())



@app.route("/viewprofile")
def viewprofile():
    sql="select * from userreg where Useremail='%s'"%(session['useremail'])
    d =pd.read_sql_query(sql,db)
    return render_template("viewprofile.html",rows=d.values.tolist())


@app.route("/updateprofile/<d>")
def updateprofile(d = 0):
    sql="select * from userreg where Id='%s'"%(d)
    cur.execute(sql)
    d =  cur.fetchall()
    db.commit()
    return render_template("updateprofile.html",data=d)

@app.route("/addprofile",methods=["POST","GET"])
def addprofile():
    if request.method == "POST":
        username = request.form['username']
        useremail = request.form['useremail']
        userage = request.form['userage']
        usercontact = request.form['usercontact']
        useraddress = request.form['useraddress']
        userpassword = request.form['userpassword']
        sql="update userreg set Username=%s,Useremail=%s,Userage=%s,Usercontact=%s,Useraddress=%s,Userpassword=%s where Useremail=%s"
        val=(username,useremail,userage,usercontact,useraddress,userpassword,session['useremail'])
        cur.execute(sql,val)
        db.commit()

        return redirect(url_for('viewprofile'))



@app.route("/addtocart",methods=["POST","GET"])
def addtocart():
    if request.method == "POST":
        productid = request.form["productid"]
        category = request.form['category']
        sql="select * from userorder where Category='%s' and ProductId='%s'"%(category,productid)
        cur.execute(sql)
        d = cur.fetchall()
        db.commit()
        print(d)
        productname = d[0][3]
        items = d[0][8]
        imagename = d[0][6]
        totalprice = d[0][9]
        actualcost = d[0][4]
        otp = str(random.randint(000000,999999))
        sql="insert into mycart(Categoryname,ProductId,Productname,Productprice,NoofItems,Totalprice,Useremail,Imagename,Otp)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val=(category,productid,productname,actualcost,items,totalprice,session['useremail'],imagename,otp)
        cur.execute(sql,val)
        db.commit()
        sql="select * from userorder where Category='%s' and ProductId='%s'"%(category,productid)
        d = pd.read_sql_query(sql,db)
        return render_template("allproducts.html",rows = d.values.tolist(),msg="Product added to cart")

@app.route("/makeorder")
def makeorder():
    sql="select * from userorder where Useremail='%s'"%(session['useremail'])
    data=pd.read_sql_query(sql,db)

    return render_template("makeorder.html",rows=data.values.tolist())


@app.route("/removedata/<d>")
def removedata(d=0):
    print(d)
    sql="delete from userorder where ID='%s'"%(d)
    cur.execute(sql)
    db.commit()
    return redirect(url_for('makeorder'))

@app.route("/delitem/<d>")
def delitem(d=0):
    sql="delete from userorder where ID='%s'"%(d)
    cur.execute(sql)
    db.commit()
    return redirect(url_for('vieworders'))
    # sql="select * from userorder"
    # data=pd.read_sql_query(sql,db)
    # return render_template("vieworders.html",rows = data.values.tolist())


@app.route("/searchitem",methods=["POST","GET"])
def searchitem():
    if request.method == "POST":
        searchproduct = request.form['searchproduct']
        print(searchproduct)
        sql="select * from productlist where ProductName='%s'"%(searchproduct)
        data = pd.read_sql_query(sql,db)

        return render_template("searchitem.html",rows=data.values.tolist())

@app.route("/mycart")
def mycart():
    sql="select Id,ProductId,Productname,Productprice,NoofItems,TotalPrice,Imagename from mycart where Useremail='%s'"%(session['useremail'])
    data= pd.read_sql_query(sql,db)
    return render_template("mycart.html",rows=data.values.tolist())

@app.route("/carttoorder/<d>")
def carttoorder(d=''):
    print(d)
    sql="select * from mycart where Id='%s'"%(d)
    cur.execute(sql)
    d = cur.fetchall()
    db.commit()
    print(d)
    category = d[0][1]
    productid= d[0][2]
    productname =  d[0][3]
    productprice = d[0][4]
    noofitems = d[0][5]
    totalprice = d[0][6]
    useremail = d[0][7]
    imagename = d[0][8]
    desc = "pending"
    sql="insert into userorder(ProductId,Category,ProductName,ProductPrice,ProductDescription,ProductImage,Useremail,Productcount,Totalprice)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (productid,category,productname,productprice,desc,imagename,useremail,noofitems,totalprice)
    cur.execute(sql,val)
    db.commit()
    flash("Cart items available to make order","success")
    return redirect(url_for('mycart'))


@app.route("/removecart/<d>")
def removecart(d=0):
    print(d)
    sql="delete from mycart where Id='%s'"%(d)
    cur.execute(sql)
    db.commit()
    return redirect(url_for('mycart'))

@app.route("/onlinepayment",methods=["POST","GET"])
def onlinepayment():
    if request.method =="POST":
        cardname = request.form['cardname']
        cardnumber = request.form['cardnumber']
        cardcvv = request.form['cardcvv']
        carded = request.form['carded']
        today = date.today()
        delivarydate = today + timedelta(days=6)
        print(today,delivarydate)
        sql="select * from userorder where Useremail='%s'"%(session['useremail'])
        cur.execute(sql,db)
        daaaa = cur.fetchall()
        totalsum = sum(int(daaaa['Totalprice']))
        totalcount= sum(daaaa['Productcount'])
        productname=str(daaaa['ProductName'][1])
        sql = "insert into payment(cardname,cardnumber,cardcvv,carded,useremail,Expirydate,Productname,Productcount,Totalprice)values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (cardname,cardnumber,cardcvv,carded,session['useremail'],delivarydate,productname,totalcount,totalsum)
        cur.execute(sql,val)
        db.commit()
        sender_address = 'kalyansai358@gmail.com'
        sender_pass = 'mkxlshxbjwbupaob'
        content = "your Product will be delivered on {} for Product : {},Price : {},ProductCount:{}".format( delivarydate, productname, totalsum, totalcount)
        receiver_address = (session['useremail'])
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = "ONLINE SHOPPING SYSTEM"
        message.attach(MIMEText(content, 'plain'))
        ss = smtplib.SMTP('smtp.gmail.com', 587)
        ss.starttls()
        ss.login(sender_address, sender_pass)

        text = message.as_string()
        ss.sendmail(sender_address, receiver_address, text)
        ss.quit()

        flash("Order placed successfuly order will be delivered on {}".format(delivarydate),"success")
        return redirect(url_for("makeorder"))
    return render_template("onlinepayment.html")






@app.route("/paymentdetails")
def paymentdetails():
    sql="select id,useremail,Productname,Productcount,Totalprice,Expirydate from payment"
    c = pd.read_sql_query(sql,db)
    return render_template("paymentdetails.html",rows=c.values.tolist())






@app.route("/offlinepayment")
def offlinepayment():

    sql = "select Otp from mycart where Useremail='%s'"%(session['useremail'])
    cur.execute(sql)
    data = cur.fetchall()[0]
    sender_address = 'kalyansai358@gmail.com'
    sender_pass = 'mkxlshxbjwbupaob'
    content = "Your Otp For Products: {}".format(data)
    receiver_address = (session['useremail'])
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = "ONLINE SHOPPING SYSTEM"
    message.attach(MIMEText(content, 'plain'))
    ss = smtplib.SMTP('smtp.gmail.com', 587)
    ss.starttls()
    ss.login(sender_address, sender_pass)

    text = message.as_string()
    ss.sendmail(sender_address, receiver_address, text)
    ss.quit()


    today = date.today()
    delivarydate = today + timedelta(days=6)
    flash("Your order will be delivered on {}".format(delivarydate),"success")
    return redirect(url_for("makeorder"))


@app.route("/vieworders")
def vieworders():
    sql="select * from userorder"
    data=pd.read_sql_query(sql,db)
    return render_template("vieworders.html",rows = data.values.tolist())

@app.route("/viewfeedback/<d>")
def viewfeedback(d=''):
    print(d)
    sql="select * from feedback where ProductId=%s"%(d)
    data = pd.read_sql_query(sql,db)
    return render_template('feedback.html',rows = data.values.tolist())

@app.route("/sendmail",methods=["POST","GET"])
def sendmail():
    if request.method == "POST":
        useremail = request.form['useremail']
        print(useremail)
        session['user_email'] = useremail
        sql="select * from userreg where Useremail='%s'"%(useremail)
        cur.execute(sql)
        d = cur.fetchall()
        db.commit()
        print(d)
        if d == []:
            msg="invalid email"
            return render_template("forgotpassword.html",msg=msg,email="")
        else:
            sender_address = 'kalyansai358@gmail.com'
            sender_pass = 'mkxlshxbjwbupaob'
            content = "your Product will be delivered on {} for Product : {},Price : {},ProductCount:{}".format(
                delivarydate, productname, totalsum, totalcount)
            receiver_address = useremail
            message = MIMEMultipart()
            message['From'] = sender_address
            message['To'] = receiver_address
            message['Subject'] = "ONLINE SHOPPING SYSTEM"
            message.attach(MIMEText(content, 'plain'))
            ss = smtplib.SMTP('smtp.gmail.com', 587)

            ss.starttls()
            ss.login(sender_address, sender_pass)
            text = message.as_string()
            ss.sendmail(sender_address, receiver_address, text)
            ss.quit()
            return render_template("forgotpassword.html")


@app.route("/forgotpassword")
def forgotpassword():
    return render_template("forgotpassword.html",email="")

@app.route("/updatepassword",methods=["POST","GET"])
def updatepassword():
    if request.method == "POST":
        useremail = request.form['useremail']
        password = request.form['password']
        confirmpassword = request.form['confirmpassword']
        print(useremail)
        if password == confirmpassword:
            sql="update userreg set Userpassword='%s' where Useremail='%s'"%(password,session['user_email'])
            cur.execute(sql)
            db.commit()
            return redirect(url_for('userlogin'))
        else:
            return render_template("forgotpassword.html",msg="passwords are not matching")

if __name__=='__main__':
    app.run(debug=True)