def christmasstree(n):
    z = n - 1
    x = 1
    for i in range(n):
        print(' ' * z + '*' * x + ' ' * z)
        x += 2
        z -= 1

try:
        n = int(input("Enter an odd number between 5 and 101: "))
        if 5 < n < 101 and n % 2 != 0:
            christmasstree(n)
        else:
            print("Oi! Please enter an odd number between 5 and 101.")
except ValueError:
        print("Please provide a valid integer.")
