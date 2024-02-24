import pymysql #Libraries to manipulate mysql
import numpy, pandas #Libraries for reading data from databases, storing it in main memory, and analyzing it.
import collections #Library for analyzing words stored in main memory.

shopping_db=pymysql.connect(user='root', passwd='39574rewop', host='127.0.0.1', db='Shopping_database', charset='utf8')
cursor = shopping_db.cursor(pymysql.cursors.DictCursor)

def checkcustomer(): #This works fine.
    #Restrict access by checking if the user's input exists in the database.
    isseller=input("Are you a seller?(y/n): ")
    user=input("Please enter your username: ")
    password=input("Please enter your password: ")

    if(isseller=='y'): #Check information in Seller relation if it is Seller
        sql="SELECT Id, password_user FROM Seller where id="+"'"+user+"'"+" and password_user="+"'"+password+"'"+";"
        cursor.execute(sql) #Execute SQL syntax in Python
        result = cursor.fetchall() #Get the result of the execution, fetchall is used to fetch all the data at once.
    else: # if Customer, get information from Customer relation
        sql="SELECT Id, password_user FROM Customer where id="+"'"+user+"'"+" and password_user="+"'"+password+"'"+";"
        cursor.execute(sql) #Execute SQL syntax in Python
        result = cursor.fetchall() #get the result of the execution, fetchall is used to fetch all data at once.
        #fetchone(), used to fetch only one row in one call, fetchmany(n) to fetch as many as n data
    
    if result==():
        print("Username or password does not match. ")
        return [0, user]
    else:
        return [1, user]
    
def register(): #Everything works.
    while(True):
        isregister=input("Do you want to register (y/n): ")
        if(isregister=='y'):
            iscustomer=input("Would you like to register as a consumer?(y/n)")
            if(iscustomer=='y' or iscustomer=='n'):
                # user=input("Please enter your username ")
                #The database will remove duplicates for you, but for your convenience, the application will check for duplicates.
                sql="SELECT * FROM Customer where Id="+"'"+user+"'"+";"
                cursor.execute(sql); result=cursor.fetchall();
                if(result!=()):
                    print("The username already exists, please enter it again.")
                else:
                    password=input("Please enter your password")
                    Phone_number=input("Please enter your cell phone number (only numbers, no -s)")
                    Gender=input("Please enter your gender (0 for male, 1 for female) ")
                    Age=input("Please enter your age")
                    
                    if(iscustomer=='y'): #Register data in consumer release
                        sql="insert into Customer(Id,password_user,Phone_number,Gender,Age) value('"+user+"','"+password
                        sql+="','"+Phone_number+"','"+Gender+"','"+Age+"');"
                        cursor.execute(sql);
                        shopping_db.commit()
                        return None
                    else: #Register data to the seller release
                        sql="insert into Seller(Id,password_user,Phone_number,Gender,Age) value('"+user+"','"+password
                        sql+="','"+Phone_number+"','"+Gender+"','"+Age+"');"
                        cursor.execute(sql);
                        shopping_db.commit()
                        return None
                    
        elif(isregister=='n'):
            #stop because the user is not registering.
        else:
            print("Please enter again. ")
    
def delete(user): #Everything works.
    while(True):
        isok=input("What do you want to delete? (1.browsing history, 2.cart, 3.cancel) ") #Select what the user wants to delete.
        
        if(isok=='3'):
            return None
        elif(isok=='1'): #Delete the search history corresponding to the user's username.
            sql="delete from Searchword where Customer_id="+"'"+user+"'"+";"
            cursor.execute(sql);
            shopping_db.commit() #The library automatically executes the transaction, so you only need to write commit without mentioning start.

        elif(isok=='2'): #Show the list of baskets and select the one you want to delete.
            sql="SELECT Product_name FROM Wishlist where Customer_id="+"'"+user+"'"+";"
            cursor.execute(sql); result = cursor.fetchall();
            print(result)
            
            # For the user's convenience, we should program to allow multiple products to be selected, but due to console limitations, we're only deleting one at a time.
            product=input("Which product do you want to delete? ");
            sql="delete from Wishlist where Customer_id="+"'"+user+"'"+"and Product_name="+"'"+product+"'"+";"
            cursor.execute(sql);
            shopping_db.commit()

def recommendation(user):
    # Read the data that matches the user's information and save it to the main memory.
    sql="SELECT Product_name FROM Wishlist where Customer_id="+"'"+user+"'"+";"
    result=cursor.execute(sql);
    Wishlist=pandas.DataFrame(result)
    
    sql="SELECT word FROM Searchword where Customer_id="+"'"+user+"'"+";"
    result=cursor.execute(sql);
    searchword=pandas.DataFrame(result)
    
    """ Not currently used, but commented out because it's likely to be used in the future
    sql="SELECT Product_name FROM Buylog where Customer_id="+"'"+user+"'"+";"
    result=cursor.execute(sql);
    Buylog=pandas.DataFrame(cursor.execute(sql))
    """
    
    #Suggest products based on the information you've read. Extract information about the single most interesting product and make product recommendations based on it
    word=collections.Counter(searchword["word"]).most_common(1)[0][0][0]
    wish=collections.Counter(Wishlist["Product_name"]).most_common(1)[0][0]
    
    if(word in wish): #I see that the user is considering a purchase based on how relevant the search term is to the cart.
        sql="SELECT * FROM Product where Name like "+"'%"+word+"%'"+";"
        result=cursor.execute(sql);
        print(pandas.DataFrame(result))
        
    return None

def addition(user): #test result 1 work, test result 2 also work, test result 3 also work
        isok=input("What do you want to add? (1.search history, 2.cart, 3.purchase history, 4.cancel) ") #Select the part the user wants to delete.
        
        if(isok=='4'):
            return None
        elif(isok=='1'): #Add the search history corresponding to the user's username. This should be done regardless of the user's request, but due to the nature of the prototype
            #currently, we add the search history based on the user's request.
            word=input("Please enter a search term. ")
            sql="insert into Searchword(Customer_id, Word) value('"+user+"'"+","+"'"+word+"')"+";"
            cursor.execute(sql);
            shopping_db.commit() #This library automatically executes the transaction, so we only need to write commit without mentioning start.

        elif(isok=='2'): #Add data to the shopping cart list.
            product=input("Please enter the name of the product to add");
            seller=input("Enter the seller ID of the product to add");
            
            sql="insert into Wishlist(Product_name,Customer_id,Seller_id) values ('"+product+"','"+user+"','"+seller+"')"+";"
            cursor.execute(sql);
            shopping_db.commit()
        elif(isok=='3'):
            product=input("Please enter the name of the product you purchased ");
            seller=input("Please enter the seller ID of the purchased product");
            
            sql="insert into Buylog(Product_name,Customer_id,Seller_id) values ('"+product+"','"+user+"','"+seller+"')"+";"
            cursor.execute(sql);
            shopping_db.commit()

def operation(user): #Execute the program when the login is successful, and access and delete only the part corresponding to the user's ID.
    #This is the part where the program is executed, which should be independent of the user's request, but since it's a prototype, it's not.
    # Execute the program according to the request.
    
    while(True):
        print("What do you want to do (enter a number): ")
        whattodo=input("0.recommend a product, 1.add information, 2.delete information, 3.stop)") #In this case, information is the user's history.
        
        if(whattodo=='0'):
            recommendation(user)
        elif(whattodo=='1'):
            addition(user) #implemented
        elif(whattodo=='2'):
            delete(user) #implemented
        elif(whattodo=='2'):
            return None
        elif(whattodo=='3'):
            break
        else:
            print("Please enter again. ") 
            
login=checkcustomer()

if(login[0]==1):
    operation(login[1]) #the part that runs the program
else:
    register() #Part that executes registration
