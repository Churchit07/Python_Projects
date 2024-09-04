import mysql.connector as cnt
con=cnt.connect(host='localhost',user='root',password='root',database='MUJ_Lib')
cur=con.cursor()

def clrscr():
    for i in range (1,32):
        print()
def lines(lno):
    for i in range (1,lno+1):
        print()
    print("*"*40)
def database():
    sql="create database if not exists MUJ_Lib"
    cur.execute(sql)
    print("Database create suceefully")
    
    sql="use MUJ_Lib"
    cur.execute(sql)

    sql="create table if not exists users (userid varchar(20) primary key,password varchar(20),type varchar(10))"
    cur.execute(sql) 
    
    sql="create table if not exists books (b_id varchar(10) primary key,title varchar(20),author varchar(20),publication varchar(20),mrp int(10),keywords varchar(20),qty int(20))"
    cur.execute(sql)
    print("books table created successfully")

    sql="create table if not exists members (m_id varchar(20) primary key,name varchar(20),fname varchar(20),branch varchar(20),semester varchar(10))"
    cur.execute(sql)
    print("members table created successfully")

    sql="create table if not exists books_issued (m_id varchar(20),b_id varchar(20),issuedate varchar(20),returndate varchar(20),fine int(10),foreign key(m_id) references members(m_id),foreign key(b_id) references books(b_id))" 
    cur.execute(sql)
    print("books_issued table created successfully")

    sql="create table if not exists books_purchased (b_id varchar(20),qty int(20),purchase_date varchar(20),foreign key(b_id) references books(b_id))"
    cur.execute(sql)
    print("books_purchased table created successfully")

    sql="create table if not exists books_damaged (b_id varchar(20),qty int(20),damage_date varchar(20),foreign key(b_id) references books(b_id))"
    cur.execute(sql)
    print("books_damaged table created successfully")

    sql="insert into users(userid,password,type) values('{}','{}','{}')".format("1234","2005","admin")
    cur.execute(sql)
    con.commit()     
    
#database()

def aval_qty(bookid):
    sql="select qty from books where b_id='{}'".format(bookid)
    cur.execute(sql)
    bqty=cur.fetchone()
    
    if bqty==None:
        bqty=0
    else:
        bqty=bqty[0]

    
      


    sql="select count(*) from books_issued where b_id='{}' and returndate is Null".format(bookid)
    cur.execute(sql)
    iqty=cur.fetchone()
    if iqty==None:
        iqty=0
    else:
        iqty=iqty[0]

    
    sql="select sum(qty) from books_purchased where b_id='{}'".format(bookid)
    cur.execute(sql)
    pqty=cur.fetchone()
    if pqty==None:
        pqty=0
    else:
        pqty=pqty[0]

    
    sql="select sum(qty) from books_damaged where b_id='{}'".format(bookid)
    cur.execute(sql)
    dqty=cur.fetchone()
    if dqty==None:
        dqty=0
        
    else:
        dqty=dqty[0]
        
    

    if bqty==None:
        bqty=0

    if iqty==None:
        iqty=0

    if pqty==None:
        pqty=0

    if dqty==None:
        dqty=0   

    
    tqty=bqty+pqty-iqty-dqty
    return tqty 

    
def insert_books():
    book_id=input("enter book id ")
    title=input("enter book title ")
    author=input("enter book author ")
    publication=input("enter publication of book ")
    price=int(input("enter price of book "))
    keywords=input("enter keywords for books ")
    qty=int(input("quantity of books "))

    sql="insert into books(b_id,title,author,publication,mrp,keywords,qty) values('{}','{}','{}','{}','{}','{}','{}')".format(book_id,title,author,publication,price,keywords,qty)
    cur.execute(sql)
    con.commit()
    print("book insertion successful")

def delete_books():
    book_id=input("enter book id ")

    sql="delete from books where b_id='{}'".format(book_id)
    cur.execute(sql)
    con.commit()
    if cur.rowcount==0:
        print("book not found")
    else:
        print("book deleted succssfully")


def modify_book_records(bid,fldname):
    msg="Enter new " +fldname
    fldval=input(msg)
    sql="update books set {}='{}' where B_Id='{}'".format(fldname,fldval,bid)
    cur.execute(sql)
    con.commit()
    print(fldname,"modified successfully")


def modify_books():
    bid=input("Enter Book id ")
    flag=viewbook(bid)
    if flag==True:
        while True:
            print("enter 0 to exit")
            print("enter 1 to modify title")
            print("enter 2 to modify author")
            print("enter 3 to modify publication")
            print("enter 4 to modify price")
            print("enter 5 to modify keywords")
            print("enter 6 to modify quantity")
            choice=int(input("Enter your choice "))
            if choice==0:
                break
            if choice==1:
                modify_book_records(bookid,"Title")
            if choice==2:
                modify_book_records(bookid,"author")
            if choice==3:
                modify_book_records(bookid,"publication")    
            if choice==4:
                modify_book_records(bookid,"price")
            if choice==5:
                modify_book_records(bookid,"keywords")
            if choice==6:
                modify_book_records(bookid,"qty")    

def add_books():
     bid=input("Enter Book id ")
     flag=viewbook(bid)
     if flag==True:
         qty=int(input("enter additional number of books "))
         purchase_date=input("enter date of purchase ")
         sql="insert into books_purchased(b_id,qty,purchase_date) values('{}',{},'{}')".format(bookid,qty,purchase_date)
         cur.execute(sql)
         con.commit()
         print("data entered successfully")

def viewbook(mid):
    lines(5)
          
    sql="select * from members where m_id='{}'".format(mid)
    cur.execute(sql)
    bk=cur.fetchone()
    if bk==None:
        print("invalid member id")
        return(False)
    else:
        print("Details of Member".center(40),"*")
        print("*"*40)
        print("Member Id: ".ljust(30),bk[0])
        print("Name: ".ljust(30),bk[1])
        print("Father Name ".ljust(30),bk[2])
        print("Semester: ".ljust(30),bk[3])
        print("Branch: ".ljust(30),bk[4])
        return(True)


def viewbook(bid):
    lines(5)
          
    sql="select * from books where b_id='{}'".format(bid)
    cur.execute(sql)
    bk=cur.fetchone()
    if bk==None:
        print("invalid book id")
        return(False)
    else:
        print("Details of Book".center(40),"*")
        print("*"*40)
        print("Book Id: ".ljust(30),bk[0])
        print("Title: ".ljust(30),bk[1])
        print("Author: ".ljust(30),bk[2])
        print("Publication: ".ljust(30),bk[3])
        print("MRP: ".ljust(30),bk[4])
        print("Keywords: ".ljust(30),bk[5])
        print("Quantity: ".ljust(30),bk[6])
        return(True)
  
def add_damaged_books():
        bid=input("Enter Book id ")
        viewbook(bid)
        qty=int(input("Enter Damage Books-Qty"))
        damage_date=input("enter date of purchase ")
        sql="insert into books_damaged(b_id,qty,damage_date) values('{}',{},'{}')".format(bookid,qty,damage_date)
        cur.execute(sql)
        con.commit()
        print("data entered successfully")

    
def bookdetails():
    clrscr()
    while True:
        print("0 for exit")
        print("1 to insert new book")
        print("2 to delete a existing book")
        print("3 to modify a book")
        print("4 to insert additional books on existing titles")
        print("5 to add a damaged book")

        choice=int(input("enter your choice: "))
        if choice==0:
            break
        if choice==1:
            insert_books()
        if choice==2:
            delete_books()
        if choice==3:
            modify_books()
        if choice==4:
            add_books()
        if choice==5:
            add_damaged_books()
            
def insert_members():
    member_id=input("enter member id ")
    name=input("enter member name ")
    father_name=input("enter father name of member ")
    branch=input("enter branch of member ")
    semester=input("enter semester of member ")

    sql="insert into members(m_id,name,fname,branch,semester) values('{}','{}','{}','{}','{}')".format(member_id,name,father_name,branch,semester)
    cur.execute(sql)
    con.commit()
    print("member insertion successful")


def delete_members():
    member_id=input("enter member id ")

    sql="delete from members where m_id='{}'".format(member_id)
    cur.execute(sql)
    con.commit()
    if cur.rowcount==0:
        print("member not found")
    else:
        print("member deleted succssfully")


def modify_member_records(mid,fldname):
    msg="Enter new " +fldname
    fldval=input(msg)
    sql="update members set {}='{}' where m_id='{}'".format(fldname,fldval,mid)
    cur.execute(sql)
    con.commit()
    print(fldname,"modified successfully")


def modify_members():
    memberid=input("Enter member id ")
    sql="select * from members where m_id='{}'".format(memberid)
    cur.execute(sql)
    bk=cur.fetchone()
    if bk==None:
        print("invalid member id")
    else:
        print(bk)
        
        while True:
            print("enter 0 to exit")
            print("enter 1 to modify name")
            print("enter 2 to modify father name")
            print("enter 3 to modify branch")
            print("enter 4 to modify semester")
            choice=int(input("Enter your choice "))
            if choice==0:
                break
            if choice==1:
                modify_member_records(memberid,"Name")
            if choice==2:
                modify_member_records(memberid,"Fname")
            if choice==3:
                modify_member_records(memberid,"branch")    
            if choice==4:
                modify_member_records(memberid,"semester")

   
def memberdetails():
    while True:
        print("enter 0 for exit")
        print("enter 1 to insert new member")
        print("enter 2 to delete a existing member")
        print("enter 3 to modify a member details")

        choice=int(input("enter your choice"))
        if choice==0:
            break
        if choice==1:
            insert_members()
        if choice==2:
            delete_members()
        if choice==3:
            modify_members()


def books_issued():
    member_id=input("enter member id ")
    sql="select * from members where m_id='{}'".format(member_id)
    cur.execute(sql)
    gk=cur.fetchone()
    if gk==None:
        print("Member does not exist")
    else:
        print(gk)
        sql="select books.title,books_issued.b_id,books_issued.issuedate from books,books_issued where books.b_id=books_issued.b_id and m_id='{}' and returndate is Null".format(member_id)
        cur.execute(sql)
        gg=cur.fetchall()
        issuecount=0
        if gg==[]:
            print("No book issued to this member")
        else:
            for rec in gg:
                print(rec)
                issuecount=issuecount+1
        if issuecount>=2 :
           print("No more books can be issued to this member")
        else:
           bid=input("Enter Book id ")
           flag=viewbook(bid)
           if flag==True:
               qty=aval_qty(bid)
               print(qty)
               if qty>0:
                   kk=input("do you want to proceed? y for yes and n for no")
                   sql="select * from books_issued where m_id='{}' and b_id='{}' and returndate is Null".format(member_id,bookid)
                   cur.execute(sql)
                   dt=cur.fetchone()
                   if dt==None:
                       if kk in "Yy":
                           issuedate=input("enter issue date format yyyy-mm-dd")
                           sql="insert into books_issued(b_id,m_id,issuedate) values('{}','{}','{}')".format(bookid,member_id,issuedate)
                           cur.execute(sql)
                           con.commit()
                           print("Book issued sucessfully")
                       else:
                           print("Book not issued")
                   else:
                       print("this book is already issued before to this member")
               else:
                   print("book not available")
                   
               
                   

def books_returned():
    member_id=input("enter member id ")
    sql="select * from members where m_id='{}'".format(member_id)
    cur.execute(sql)
    gk=cur.fetchone()
    if gk==None:
        print("Member does not exist")
    else:
        print(gk)
        sql="select books.title,books_issued.b_id,books_issued.issuedate from books,books_issued where books.b_id=books_issued.b_id and m_id='{}' and returndate is Null".format(member_id)
        cur.execute(sql)
        gg=cur.fetchall()

        if gg==[]:
            print("No book issued to this member so cant return it.")
        else:
            for rec in gg:
                print(rec)
                
            bid=input("Enter Book id ")
            flag=viewbook(bid)
            if flag==True:
                kk=input("do you want to proceed? y for yes and n for no")
                sql="select * from books_issued where m_id='{}' and b_id='{}' and returndate is Null".format(member_id,bookid)
                cur.execute(sql)
                dt=cur.fetchone()
                if dt==None:
                    print("this book was not issued to you so you cant return it")
                else:
                    if kk in "Yy":
                        returndate=input("enter return date format yyyy-mm-dd")
                        sql="update books_issued set returndate='{}' where m_id='{}' and b_id='{}' and returndate is Null".format(returndate,member_id,bookid)
                        cur.execute(sql)
                        con.commit()
                        print("Book return sucessfully")
                    else:
                        print("Book not return")
                        
def books_purchased():
     bid=input("Enter Book id ")
     flag=viewbook(bid)
     if flag==True:
         print(bg)
         quanity=int(input("enter quantity of books purchased"))
         purchase_date=input("enter date of purchase")
         sql="insert into books_purchased(b_id,qty,purchase_date) values('{}',{},'{}')".format(book_id,qty,purchase_date)
         cur.execute(sql)
         con.commit()


def books_damaged():
     bid=input("Enter Book id ")
     flag=viewbook(bid)
     if flag==True:
         print(bg)
         quanity=int(input("enter quantity of books purchased"))
         damage_date=input("enter date of damage")
         sql="insert into books_damaged(b_id,qty,damage_date) values('{}',{},'{}')".format(book_id,qty,damage_date)
         cur.execute(sql)
         con.commit()           
        
                     

def mainmenu():
    clrscr()
    header()
    while True:
        print("0 for exit")
        print("1 for Book Details")
        print("2 for Member Details")
        print("3 for Books Issued")
        print("4 for Books Purchased")
        print("5 for Books Damaged")
        print("6 for Books Returned")

        choice=int(input("enter your choice: "))
        if choice==0:
            break
        if choice==1:
            bookdetails()
        if choice==2:
            memberdetails()
        if choice==3:
            books_issued()
        if choice==4:
            books_purchased()
        if choice==5:
            books_damaged()    
        if choice==6:
            books_returned()
            
            


def header():
    msg="Welcome to MUJ-Library Management System"
    print(msg.center(150,"*"))
    msg="Developed and Designed by Churchit Goyal,BTech II-Year"
    print(msg.center(150,"*"))

def is_user_valid():
    header()
    #puser_id=int(input("Enter userid: "))
    #pass_word=int(input("Enter password: "))

    puser_id="1234"
    pass_word="2005"

    sql="select * from users where userid={} and password={}".format(puser_id,pass_word)
    cur.execute(sql)
    py=cur.fetchone()

    if py==None:
        print("user data is invalid")

    else:
        mainmenu()


is_user_valid()







        
