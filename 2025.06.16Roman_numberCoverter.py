# Convert an integer to /from a Roman numeral.
def convert_roman(input_value):
    roman_to_int_map = {
        'I': 1, 'V': 5, 'X': 10, 'L': 50,'C': 100, 'D': 500, 'M': 1000
    }

    int_to_roman_map = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
    ]

    def integer_to_roman(num):
        result = ''
        for value, numeral in int_to_roman_map:
            while num >= value:
                result += numeral
                num -= value
        return result

    def roman_to_integer(roman):
        roman = roman.upper()
        total = 0
        prev_value = 0
        for char in reversed(roman):
            value = roman_to_int_map[char]
            if value < prev_value:
                total -= value
            else:
                total += value
            prev_value = value
        return total

    #Input Section
choice = input("Enter 'R' to convert Roman to Integer or 'I' to convert Integer to Roman: ").strip().upper()

if choice == 'I':
    num = int(input("Enter an integer (1 to 3999): "))
    if 1 <= num <= 3999:
        print("Roman numeral:", integer_to_roman(num))
    else:
        print("Number out of range.")

elif choice == 'R':
    roman = input("Enter a Roman numeral: ").strip().upper()
    print("Integer value:", roman_to_integer(roman))

else:
    print("Invalid choice.")
