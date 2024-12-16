
def main(): 
    print("Cześć jestem kalkultorem wydruków! Jestem zajebisty! Da pan 5!")
    db = {
        "A4": 0.32, 
        "A3": 1.22,
        "A2": 2.33
    }
    list = (
        ("A4", 0.32), 
        ("A3", 1.22),
        ("A2", 2.33)
        )

    rq1 = ("A3", 32) 
    rq2 = ("A4", 32) 
    # list -> cena A4
    list[0][1] * rq1[1]
    for el in list: 
        if rq1[0] == el[0]:
            print(el[1] * rq1[1])
            break;
    print(rq1[1] * db[rq1[0]])

main()


