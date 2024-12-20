from dataclasses import dataclass
import json
import sys
@dataclass
class Order:
    format:str
    amount:int


def calculete_final_price(order_list: list, db: dict):
    prices = 0
    for order in order_list:
        prices += calculate_price(order,db)
    return prices
        
def calculate_price(order:Order, db : dict) -> float:
    cena_za_sztukę = db[order.format]
    return cena_za_sztukę * order.amount
   
def request_to_list(request: str, db : dict):
    order_list=[]
    error_flag=False
    for order in request.split(";"):
        person = order.strip().split(" ")
        if len (person)!=2:
            print(f"Błąd! '{order.strip()}' nie jest w odpowiednim zapisie. Poparwny zapis to : \"[<format> <ilość>;]\"")
            error_flag=True
            continue
        format = person[0]
        if not person[1].isdigit():
            print(f"Błąd! \"{person[1]}\" nie jest liczbą.")
            error_flag=True
            continue
        amount = int(person[1])
        if not format in db:
            print(f"Bład! Brak formatu \"{format}\" w bazie danych")
            error_flag=True
            continue
        order_list.append(Order(format=format,amount=amount))
    return error_flag, order_list

def print_format(db):
    print("Dostępne formaty:")
    for format, price in db.items():
        print(f"format {format} : {price}")

def print_order(list: list):
    i = 0
    for l in list:
        i += 1
        print(f"{i}) {l.format} : {l.amount}")
    
def main(): 
    argv = sys.argv
    if len(argv) < 2: 
        file_name = "koszty_wydruku.json" 
    else:
        file_name = sys.argv[1]
    try:
        file=open(file_name)
        db=json.load(file)
    except Exception as e:
        print(e) 
        db = {
        "A4": 0.32, 
        "A3": 1.22,
        "A2": 2.33
        }

        

    print("Cześć jestem kalkultorem wydruków!")
   
    print_format(db)
    the_list=[]
    while True:
        request = input("Wprowadź komędę: \n[<format> <ilość>;] | Podsumuj | Clear | Quit\n")
        if request.strip().lower()=="podsumuj":
            finaly=calculete_final_price(the_list, db)
            print(f"Twoja ostateczna cena to: {finaly:.2f}")
            continue 
        elif request.strip().lower()=="quit":
            exit()
        elif request.strip().lower()=="clear":
            the_list.clear()
            continue            
        
        error_flag,temp_list=request_to_list(request=request, db=db)
        if error_flag and bool(temp_list):
            print("Poprawne elementy:")
            print_order(temp_list)
            while True:
                answer=input("Czy dodać poprawne elmenty? Tak | Nie\n")
                if answer.strip().lower()=="tak": 
                    break
                elif answer.strip().lower()=="nie":
                    temp_list.clear()
                    break
                elif answer.strip().lower()=="quit":
                    exit()
                else:
                    print("Błąd! Tylko odpowiedzi Tak/Nie.")
        the_list.extend(temp_list)
        print("Lista dodanych pozycji:")
        print_order(the_list)

main()

