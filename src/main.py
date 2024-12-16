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
        person = order.split(" ")
        if len (person)!=2:
            print("Błąd! Poparwny zapis to : \"<format> <ilość>;")
            error_flag=True
            continue
        format = person[0]
        if not person[1].isdigit():
            print(f"Błąd! {person[1]} nie jest liczbą.")
            error_flag=True
            continue
        amount = int(person[1])
        if not format in db:
            print(f"Bład! Brak formatu {format} w bazie danych")
            error_flag=True
            continue
        order_list.append(Order(format=format,amount=amount))

    print(order_list)

    return error_flag, order_list

def print_format(db):
    for format, price in db.items():
        print(f"format {format} : {price}")

def print_order(list: list):
    print("")
    for l in list:
        print(f"{l.format}:{l.amount}")
    
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

        

    print("Cześć jestem kalkultorem wydruków! Jestem zajebisty! Da pan 5!")
   
    print_format(db)
    the_list=[]
    while True:

        request = input("Podaj format i ilość : ")
        if request.strip().lower()=="podsumuj":
            finaly=calculete_final_price(the_list, db)
            print(f"Twoja ostateczna cena to: {finaly:.2f}")
            continue 
        elif request.strip().lower()=="quit":
            exit()
        
        error_flag,temp_list=request_to_list(request=request, db=db)
        if error_flag:

            print_order(temp_list)
            while True:
                answer=input("Czy dodać poprawne elmenty? Tak/Nie\n")
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
        print_order(the_list)

main()

