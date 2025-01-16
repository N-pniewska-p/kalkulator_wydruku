from dataclasses import dataclass
import json
import sys
VAT = 0.23
@dataclass
class Order:
    format:str
    amount:int

def calculate_price(order:Order, db : dict) -> float:
    cena_za_sztukę = db[order.format]
    return cena_za_sztukę * order.amount

def generuj_fakture(order_list: list, db: dict, rabat: float):
    price_netto = 0
    price_brutto = 0
    i=0
    print(f'{"lp":>3} | {"format":>6} | {"ilość":>12} | {"NETTO":>15} | {"BRUTTO":>15}')
    for order in order_list:
        i += 1
        order_price = (calculate_price(order,db) * (1-rabat))
        order_price_brutto = order_price * (1 + VAT)
        price_brutto += order_price_brutto
        price_netto += order_price
        print(f"{i:>3} | {order.format:>6} | {order.amount:>12} | {order_price:>15.2f} | {order_price_brutto:>15.2f}")
    print(f'{"":>20} | {"NETTO":>15} | {"BRUTTO":>15}')
    print(f"{'Wartość zamówienia':>20} | {price_netto:>15.2f} | {price_brutto:>15.2f}")        

   
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

def print_format(db,rabat):
    print("Dostępne formaty:")
    for format, price in db.items():
        print(f"format {format} : {price *(1-rabat):.2f}")

def print_order(list: list):
    i = 0
    for l in list:
        i += 1
        print(f"{i}) {l.format} : {l.amount}")
def check_yes_no(tekst):
    out = False
    while True:
        answer=input(tekst)
        if answer.strip().lower()=="tak": 
            out = True
            break
        elif answer.strip().lower()=="nie":
            out = False
            break
        elif answer.strip().lower()=="quit":
            exit()
    return out
def main(): 
    argv = sys.argv
    file_kody = "kody_rabatowe.json"
    if len(argv) < 2: 
        file_db = "koszty_wydruku.json" 
    else:
        file_db = sys.argv[1]
    if len(argv) < 3: 
        file_kody = "kody_rabatowe.json"
    else: 
        file_kody = sys.argv[2]
    try:
        file=open(file_db)
        db=json.load(file)
    except Exception as e:
        print(e) 
        db = {
        "A4": 0.32, 
        "A3": 1.22,
        "A2": 2.33
        }

        
    print("Cześć jestem kalkultorem wydruków!")
   
 
    while True:
            answer=input("Czy chcesz wprowadzić kod rabatowy? Tak/Nie\n")
            if answer.strip().lower()=="tak":
                try:
                    file=open(file_kody)
                    kod=json.load(file)
                except Exception as e:
                    print(e)
                    kod = {
                        "10KOD": 0.1,
                        "50KOD": 0.5
                    }
                while True:
                    answer=input("Podaj kod rabatowy:\n")
                    if answer.strip() in kod:
                        rabat = kod[answer.strip()]
                        print(f'Zostosowano zniżkę o {rabat * 100}%')
                        break
                    out = check_yes_no("Błędny kod rabatowy. Czy chcesz spróbować jeszcze raz? Tak/Nie\n")
                    if not out: 
                        rabat = 0
                        break
                break
            elif answer.strip().lower()=="nie":
                rabat = 0
                break
            elif answer.strip().lower()=="quit":
                exit()
            else:
                print("Błąd! Tylko odpowiedzi Tak/Nie.") 

    print_format(db, rabat)
    the_list=[]
    while True:
        request = input("Wprowadź komędę: \n[<format> <ilość>;] | Podsumuj | Clear | Quit\n")
        if request.strip().lower()=="podsumuj":
            finaly=generuj_fakture(the_list, db, rabat)
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

