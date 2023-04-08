from base64 import encode
import json
import hashlib
import os
data = {}
class InStockState:
    def raise_price(obj):
        print("Продукт не участвует на торгах")
    def set_up(obj):
        obj.state_name='For_sale'
        Rewrite(obj.id,obj)
        print("Операция прошла успешно")
    def set_off(obj):
        print("нельзя снять с торгов продукт,который в них не учатсвует")
    def give_to_the_winner(obj):
        print("Нельзя отдать продукт со склада")
class ForSaleState:
    def raise_price(obj):
        sum=int(input("Поднять цену на :"))
        obj.price+=sum;
        Rewrite(obj.id,obj)
    def set_up(obj):
        print("Продукт не можеть быть повторно выставлен на торги")
    def set_off(obj):
        obj.state_name="in_stock"
        Rewrite(obj.id,obj)
        print("Операция прошла успешно")
    def give_to_the_winner(obj):
        if(obj.price==0):
            print("Нельзя отдать продукт бесплатно")
        elif obj.price>0:
            obj.state_name='Sold'
        Generator.Calculate_md5_hash(obj)
        Rewrite(obj.id,obj)
class SoldState:
    def raise_price(obj):
        print("Уже продан")
    def set_up(obj):
        print("Уже продан")
    def set_off(obj):
        print("Нелья снять с торгов проданный продукт")
    def give_to_the_winner(obj):
        print("Уже продан")
class Generator:
    def Calculate_md5_hash( obj):
        if obj.price>=1000:
            obj.honorary_code=hashlib.md5("Gold".encode("utf-8")).hexdigest()+str(obj.id)
        elif obj.price>=500 and obj.price<1000:
            obj.honorary_code=hashlib.md5("Silver".encode("utf-8")).hexdigest()+str(obj.id)
        else:
            obj.honorary_code=hashlib.md5("Bronze".encode("utf-8")).hexdigest()+str(obj.id)
class Product:
    def __init__(self,_id,_name,_price,_honorary_code,_state_name):
        self.id=_id
        self.name=_name
        self.price=_price
        self.honorary_code=_honorary_code
        self.state_name=_state_name;
    def raise_price(self):
        if self.state_name=='in_stock':
            InStockState.raise_price(self)
        elif self.state_name=='For_sale':
            ForSaleState.raise_price(self)
        elif self.state_name=='Sold':
            SoldState.raise_price(self)
    def set_up(self):
        if self.state_name=='in_stock':
            InStockState.set_up(self)
        elif self.state_name=='For_sale':
            ForSaleState.set_up(self)
        elif self.state_name=='Sold':
            SoldState.set_up(self)
    def set_off(self):
        if self.state_name=='in_stock':
            InStockState.set_off(self)
        elif self.state_name=='For_sale':
            ForSaleState.set_off(self)
        elif self.state_name=='Sold':
            SoldState.set_off(self)
    
    def give_to_the_winner(self):
        if self.state_name=='in_stock':
            InStockState.give_to_the_winner(self)
        elif self.state_name=='For_sale':
            ForSaleState.give_to_the_winner(self)
        elif self.state_name=='Sold':
            SoldState.give_to_the_winner(self)
    
class Load_data:
    products=[]
    def get_products(self):
        oper=True
        try:
            with open ('data.json')as read:
                pass
        except FileNotFoundError:
            oper=False
            print("Файл не существует")    
        if(os.stat('data.json').st_size==0):
            oper=False
            print("Файл пуст")      
        if oper==False:
            nums=int(input("Введите кол-во продуктов"))
            Write_to_file(nums);
        with open('data.json') as read:
            data=json.load(read)
            for obj in data['Product']:
                self.products.append(Product(obj['id'],obj['name'],obj['price'],obj['honorary_code'],obj['state_name']))
        return self.products

def Write_to_file(n):
    data['Product']=[];
    i=0;
    while i<n:
        print("Enter name a product")
        name=input();
        print("Enter price of product")
        price=int(input())
        data['Product'].append({
                    'id':i,
                    'name':name,
                    'price':price,
                    'honorary_code':'Null',
                    'state_name':'in_stock'
        })
        i+=1;
    with open('data.json','w') as write:
       json.dump(data,write)
def Rewrite(id,obj):
    with open('data.json') as read:
        data=json.load(read)
        for obj1 in data['Product']:
            if obj1['id']==id:
                data['Product'][id]={
                    'id':obj.id,
                    'name':obj.name,
                    'price':obj.price,
                    'honorary_code':obj.honorary_code,
                    'state_name':obj.state_name
                }
                break
    with open('data.json','w') as write:
       json.dump(data,write)
    pass
start=Load_data();
list1=[]
list1=start.get_products();
while True:
    for it in list1:
        if it.honorary_code=="Null":
            print(it.id,it.name,it.price,it.state_name,sep="|")
        else:
            print(it.id,it.name,it.price,it.state_name,it.honorary_code,sep="|")
    Id=input("Введите id продукта или (quit) для выхода: ")
    if Id=='quit':
        break;
    try:
        Id=int(Id)
        try:
            it=list1[Id]
        except:
            print("Id с таким товаром нет")
            continue
    except:
        print("Не корректный ввод")
        continue
    if it.honorary_code=="Null":
        print(it.id,it.name,it.price,it.state_name,sep="|")
    else:
        print(it.id,it.name,it.price,it.state_name,it.honorary_code,sep="|")
    ch=input('''
            1)Выставить продукт на аукцон
            2)Поднять цену
            3)Выдать победителю
            4)Снять с торгов
            5)Выход
    ''')
    match(ch):
        case '1':
            str1=it.set_up()
         
        case '2':
            str1=it.raise_price()
           
        case '3':
            str1=it.give_to_the_winner()
        
        case '4':
            str1=it.set_off()
        case '5':
            continue
        case _:
            print("Не корректный ввод")          
    
        
