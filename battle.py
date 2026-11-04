def print_triangle1(rows):
    for i in range(rows, 0, -1):
        print("*" * i)
def triangle2(rows):
    for i in range(1, rows):
        for j in range(rows, 0, -1):
            if j > i:
                print(" ", end=' ')
            else:
                print("*", end=' ')
        print("")
    
    
tr1 = int(input("Input Rows : "))  
tr2 = int(input("Input Rows : "))  
print_triangle1(tr1) 
triangle2(tr2) 






# for baris in range(5):
#     for kolom in range(7):
#         print('o', end = ' ')
#     else:
#         print('')