import pymysql #mysql을 다룰 수 있는 라이브러리
import numpy, pandas #데이터베이스에서 데이터를 읽어서 이를 메인메모리에 저장 및 분석하기 위한 라이브러리
import collections #메인메모리에 저장된 단어를 분석하기 위한 라이브러리

shopping_db=pymysql.connect(user='root', passwd='39574rewop', host='127.0.0.1', db='Shopping_database', charset='utf8')
cursor = shopping_db.cursor(pymysql.cursors.DictCursor)

def checkcustomer(): #정상적으로 작동한다.
    #사용자가 입력한 내용이 DataBase에 있는가를 확인함으로써 접근을 제한한다.
    isseller=input("판매자입니까?(y/n): ")
    user=input("아이디를 입력해주세요: ")
    password=input("비밀번호를 입력해주세요: ")

    if(isseller=='y'):  #Seller인 경우 Seller relation에서 정보를 확인
        sql="SELECT Id, password_user FROM Seller where id="+"'"+user+"'"+" and password_user="+"'"+password+"'"+";"
        cursor.execute(sql) #파이썬에서 SQL 구문 실행하기
        result = cursor.fetchall() #실행결과를 가져오며, fetchall은 모든 데이터를 한 번에 가져올 때 사용한다.
    else: # Customer인 경우 Customer relation에서 정보를 확인
        sql="SELECT Id, password_user FROM Customer where id="+"'"+user+"'"+" and password_user="+"'"+password+"'"+";"
        cursor.execute(sql) #파이썬에서 SQL 구문 실행하기
        result = cursor.fetchall() #실행결과를 가져오며, fetchall은 모든 데이터를 한 번에 가져올 때 사용한다.
        #fetchone(), 한 번 호출에 하나의 행만 가져올 때 사용, fetchmany(n) n개만큼의 데이터를 가져올 때 사용
    
    if result==():
        print("아이디 또는 비밀번호가 일치하지 않습니다. ")
        return [0, user]
    else:
        return [1, user]
    
def register(): #모두 작동 된다.
    while(True):
        isregister=input("회원가입을 하시겠습니까?(y/n): ")
        if(isregister=='y'):
            iscustomer=input("소비자로 등록하시겠습니까?(y/n)")
            if(iscustomer=='y' or iscustomer=='n'):
                user=input("아이디를 입력하세요 ")
                #데이터베이스는 중복을 알아서 제거하지만, 사용자의 편의를 위해 어플리케이션에서 중복여부를 확인해준다.
                sql="SELECT * FROM Customer where Id="+"'"+user+"'"+";"
                cursor.execute(sql); result=cursor.fetchall();
                if(result!=()):
                    print("이미 존재하는 아이디입니다. 다시 입력해주시길 바랍니다. ")
                else:
                    password=input("비밀번호를 입력하세요")
                    Phone_number=input("휴대전화번호를 입력하세요(-없이 숫자만)")
                    Gender=input("성을 입력해주세요(0은 남자, 1은 여자) ")
                    Age=input("나이를 입력해주세요 ")
                    
                    if(iscustomer=='y'): #소비자 릴레이션에 데이터 등록
                        sql="insert into Customer(Id,password_user,Phone_number,Gender,Age) value('"+user+"','"+password
                        sql+="','"+Phone_number+"','"+Gender+"','"+Age+"');"
                        cursor.execute(sql);
                        shopping_db.commit()
                        return None
                    else: #판매자 릴레이션에 데이터 등록
                        sql="insert into Seller(Id,password_user,Phone_number,Gender,Age) value('"+user+"','"+password
                        sql+="','"+Phone_number+"','"+Gender+"','"+Age+"');"
                        cursor.execute(sql);
                        shopping_db.commit()
                        return None
                    
        elif(isregister=='n'):
            return None #회원가입을 하지 않기 때문에 중단한다
        else:
            print("다시 입력해주시길 바랍니다. ")
    
def delete(user): #모두 작동된다.
    while(True):
        isok=input("무엇을 삭제하시겠습니까?(1.검색기록, 2.장바구니, 3.취소) ") #사용자가 삭제하고 싶은 부분을 선택한다.
        
        if(isok=='3'):
            return None
        elif(isok=='1'): #사용자의 아이디에 해당되는 검색기록을 삭제한다.
            sql="delete from Searchword where Customer_id="+"'"+user+"'"+";"
            cursor.execute(sql);
            shopping_db.commit() #해당 라이브러리는 transaction이 자동적으로 실행되기 때문에 start 언급없이 commit만 작성하면 된다.

        elif(isok=='2'): #장바구니 목록을 보여주고 그 중 삭제하고 싶은 부분을 선택한다.
            sql="SELECT Product_name FROM Wishlist where Customer_id="+"'"+user+"'"+";"
            cursor.execute(sql); result = cursor.fetchall();
            print(result)
            
            #사용자의 편의를 위해서는 여러 상품을 선택할 수 있도록 프로그래밍을 해야 하지만, 콘솔의 한계상 현재는 1개씩만 삭제하도록 설정했다.
            product=input("어떤 상품을 삭제하시겠습니까? ");
            sql="delete from Wishlist where Customer_id="+"'"+user+"'"+"and Product_name="+"'"+product+"'"+";"
            cursor.execute(sql);
            shopping_db.commit()

def recommendation(user):
    #사용자의 정보에 맞는 데이터를 읽고 이를 메인메모리에 저장한다.
    sql="SELECT Product_name FROM Wishlist where Customer_id="+"'"+user+"'"+";"
    result=cursor.execute(sql);
    Wishlist=pandas.DataFrame(result)
    
    sql="SELECT word FROM Searchword where Customer_id="+"'"+user+"'"+";"
    result=cursor.execute(sql);
    searchword=pandas.DataFrame(result)
    
    """ 현재는 사용하지 않지만, 차후 사용할 수 있을 가능성이 높기 때문에 주석으로 처리함
    sql="SELECT Product_name FROM Buylog where Customer_id="+"'"+user+"'"+";"
    result=cursor.execute(sql);
    Buylog=pandas.DataFrame(cursor.execute(sql))
    """
    
    #읽어온 정보를 바탕으로 상품 추천하기. 가장 관심있는 상품 1개에 대한 정보를 추출하고 이를 바탕으로 상품 추천하기
    word=collections.Counter(searchword["word"]).most_common(1)[0][0]
    wish=collections.Counter(Wishlist["Product_name"]).most_common(1)[0][0]
    
    if(word in wish): #사용자가 구매를 고려하고 있음을 검색어와 장바구니의 연관성이 얼마나 있는가로 보았다.
        sql="SELECT * FROM Product where Name like "+"'%"+word+"%'"+";"
        result=cursor.execute(sql);
        print(pandas.DataFrame(result))
        
    return None

def addition(user): #테스트 결과 1번 work, 2번도 work, 3번도 work
        isok=input("무엇을 추가하시겠습니까?(1.검색기록, 2.장바구니, 3.구매기록, 4.취소) ") #사용자가 삭제하고 싶은 부분을 선택한다.
        
        if(isok=='4'):
            return None
        elif(isok=='1'): #사용자의 아이디에 해당되는 검색기록을 추가한다. 원래는 사용자의 요청과 관계없이 진행되어야 하지만, 프로토타입 특성상
            #현재는 사용자의 요청에 따라 검색기록을 추가한다.
            word=input("검색단어를 입력하세요. ")
            sql="insert into Searchword(Customer_id, Word) value('"+user+"'"+","+"'"+word+"')"+";"
            cursor.execute(sql);
            shopping_db.commit() #해당 라이브러리는 transaction이 자동적으로 실행되기 때문에 start 언급없이 commit만 작성하면 된다.

        elif(isok=='2'): #장바구니 목록에 데이터를 추가한다.
            product=input("추가할 상품의 이름을 입력하세요 ");
            seller=input("추가할 상품의 판매자 아이디를 입력하세요 ");
            
            sql="insert into Wishlist(Product_name,Customer_id,Seller_id) values ('"+product+"','"+user+"','"+seller+"')"+";"
            cursor.execute(sql);
            shopping_db.commit()
        elif(isok=='3'):
            product=input("구매한 상품의 이름을 입력하세요 ");
            seller=input("구매한 상품의 판매자 아이디를 입력하세요 ");
            
            sql="insert into Buylog(Product_name,Customer_id,Seller_id) values ('"+product+"','"+user+"','"+seller+"')"+";"
            cursor.execute(sql);
            shopping_db.commit()

def operation(user): #로그인이 성공했을때 프로그램을 실행하여, 사용자의 아이디에 해당하는 부분만 접근 및 삭제를 수행한다.
    #프로그램이 실행되는 부분으로, 원래는 사용자의 요청과 무관하게 진행되어야 하는 부분이지만 현재는 프로토타입이기 때문에
    #요청에 따라 프로그램을 수행한다.
    
    while(True):
        print("무엇을 하시겠습니까(번호를 입력하세요): ")
        whattodo=input("0.상품 추천하기, 1.정보 추가하기, 2.정보 삭제하기 3.그만하기)") #여기서 정보는 사용자의 기록을 말한다.
        
        if(whattodo=='0'):
            recommendation(user)
        elif(whattodo=='1'):
            addition(user) #구현완료
        elif(whattodo=='2'):
            delete(user) #구현완료
        elif(whattodo=='2'):
            return None
        elif(whattodo=='3'):
            break
        else:
            print("다시 입력해주시길 바랍니다. ") 
            
login=checkcustomer()

if(login[0]==1):
    operation(login[1]) #프로그램을 실행하는 부분
else:
    register() #회원가입을 실행하는 부분
