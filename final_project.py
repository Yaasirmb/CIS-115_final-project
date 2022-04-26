import requests
from bs4 import BeautifulSoup

# ISBN final project
# Author: Yaasir M.B.
# To Do:

# Write to file and read from file.
# Finish search function.
# Add search function to main menu.
# Add logging?



def book_search(isbn13):
    # Spoofing the user agent.
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}
    # This site only works with ISBN-13s for some reason.
    response = requests.get(f"https://www.isbnsearcher.com/books/{isbn13}", headers=headers)

    print(response.status_code)
    soup = BeautifulSoup(response.text, 'lxml')
    book_title = soup.find('h1')
    title = book_title.text
    #title = re.search('\>(.+)\<', book_title)
    # print(title.group(1))
    # List containing all "col-8 col-sm-9 mb-1" classes
    book_info = soup.find_all(class_='col-8')

    language = book_info[2].text
    category = book_info[3].text
    page_count = book_info[4].text
    publish_date = book_info[5].text
    author = book_info[6].text
    
    print("Here's some information about your book :) \n ")
    print('Title:', title)
    print('Language:', language)
    print('Category:', category)
    print('Page count:', page_count)
    print('Published:', publish_date)
    print('Author', author)

def isbn_13_chk_dgt(isbn_num_13):
    """ Function that calculates the check digit for a 13 digit ISBN number."""
    total = 0
    check_num = 0
    num_list = list(isbn_num_13)

    # If the user accidentally enters the check digit, remove it before continuing.
    if len(num_list) == 13:
        num_list.pop(-1)
    elif len(num_list) == 12:
        pass
    else:
        print("There was an error while trying to calculate your ISBN 13 check digit.")

    # Iterate over the even indecies of the list.
    for num in num_list[::2]:
        total += int(num)

    # Iterate over the odd indecies of the list.
    for num in num_list[1::2]:
        total += int(num) * 3

    modulo_result = total % 10

    if modulo_result == 0:
        pass
    elif modulo_result == 10:
        check_num = 'X'
    else:
        check_num += 10 - modulo_result

    return check_num


def isbn_10_chk_dgt(isbn_num_10):
    """ Function that calculates the check digit for a 10 digit ISBN number."""
    total = 0
    check_num = 0
    start = 10
    num_list = list(isbn_num_10)

    # If the user accidentally enters the check digit, remove it before continuing.
    if len(num_list) == 10:
        num_list.pop(-1)
    elif len(num_list) == 9:
        pass
    else:
        print("There was an error while trying to calculate your ISBN 13 check digit.")

    for num in num_list:
        total += int(num) * start
        start -= 1

    modulo_result = total % 11

    if modulo_result == 0:
        pass
    elif modulo_result == 10:
        check_num = 'X'
    else:
        check_num += 11 - modulo_result

    return check_num
  

def isbn_10_to_13(isbn_num_10):
    """ Function that converts isbn 10 number to isbn 13. """
    num_list = list(isbn_num_10)
    # Remove check digit from isbn 10 number
    num_list.pop(-1)
    pad = ['9', '7', '8']

    isbn_13 = pad + num_list

    # Calculate the new check digit.
    check_digit = isbn_13_chk_dgt(isbn_13)
    isbn_13.append(str(check_digit))
    # Convert the check digit from a list to a string.
    isbn_13 = ''.join(isbn_13)

    return isbn_13

def isbn_13_to_10(isbn_num_13):
    """ Function that converts isbn 13 number to isbn 10. """
    num_list = list(isbn_num_13)
    
    pad = ['9', '7', '8']
    # Make sure this is a valid isbn 13 number.
    if num_list[:3] == pad:
        for num in pad:
            num_list.remove(num)

    if len(num_list) == 13:
        # Remove the check digit from the isbn 13 
        # so the new one can get calculated
        num_list.pop(-1)

    check_digit = isbn_10_chk_dgt(num_list)
    num_list.append(str(check_digit))

    isbn_13 = ''.join(num_list)

    return isbn_13

testnum13 = '9781861972712'
testnum10 = '1861972717'

#print(isbn_10_to_13(testnum10))




# Not fully working
while True:

    print("""
    1. Verify the check digit of an ISBN-10
    2. Verify the check digit of an ISBN-13
    3. Convert an ISBN-10 to an ISBN-13
    4. Convert an ISBN-13 to an ISBN-10
    5. Exit \n """)

    user = input("Please select an option by entering the number of the menu item you'd like to use: ")

    if user == '1':
        isbn_num = input('Enter your ISBN-10 number without the dashes: ')
        print('Your check digit is ',  isbn_10_chk_dgt(isbn_num))
    elif user == '2':
        isbn_num = input('Enter your ISBN-13 number without the dashes: ')
        print('Your check digit is ', isbn_13_chk_dgt(isbn_num))
    elif user == '3':
        isbn_num = input('Enter your ISBN-10 number without the dashes: ')
        print('Your ISBN 13 number is ', isbn_10_to_13(isbn_num))
    elif user == '4':
        isbn_num = input('Enter your ISBN-13 number without the dashes: ')
        print('Your ISBN 10 number is ', isbn_13_to_10(isbn_num))
    elif user == '5':
        break
