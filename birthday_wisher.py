# Main Logic of the program :-

import smtplib
import os
from email.message import EmailMessage
import imghdr
import datetime as dt
import pandas as pd
import random


month = dt.datetime.now().month
day = dt.datetime.now().day

current_tuple = (month, day)

# I need to compare current_tuple with the any of the month, day tuple and when that becomes equal
# I will shoot a birthday email to the person corresponding to the matching month and day.

# Now to compare a tuple we need to have tuple to compare it with.
# Hence, how about if we use 'in' operator in this case to check if current_tuple
# is existing in a dictionary (i.e. a dictionary which has the first keys as tuples.) ???

# One more thing to imagine or think of, here :-

# See, the birthdays' data could be put in the excel sheet and compared. Or a csv file and then compared
# Let us take an option of a .csv file and put the data into it.
# Then, we will create a dataframe out of it, using pandas. And, thereafter we'll create a dictionary with tuples and the keys and
# the whole datarows as values in the dictionary.

data_frame = pd.read_csv('birthday_data.csv')

# Now to create a dictionary as mentioned above to satisfy our needs :-

dictionary_birthday = { (data_row['Month'], data_row['Day']):data_row for (index, data_row) in data_frame.iterrows() }



if current_tuple in dictionary_birthday:


    EMAIL_ADDRESS = os.environ.get('Email_Address')
    EMAIL_PASSWORD = os.environ.get('Email_Password')

    msg = EmailMessage()
    # message from? :
    msg['From'] = EMAIL_ADDRESS

    birthday_person_details = dictionary_birthday[current_tuple]
    # message to ? :
    msg['To'] = birthday_person_details['Email']


    # message subject ? :
    msg['Subject'] = 'Happy Birthday!'



    # In the msg.set_content() as an argument we will have to input a string.
    # We want to have any one of the letters as the message, hence, first of all we will have to convert them
    # into strings.
    # Remember, we have to have strings and random strings out of the letters we have made.


    random_number = random.choice([1,2,3])

    with open(f'letter{random_number}.txt') as f:

        # Below is the string of the whole file :
        file_data = f.read()
        # In strings there is a method 'replace()' which replaces the word/setOfCharancters specified :
        file_data = file_data.replace('____', birthday_person_details['Name'])


    # message body? :
    msg.set_content(file_data)


    # I am creating a list of files to attach below so that in case we want to increase
    # the number of attachments, we can simply add the file's path into the list or the file's
    # name, if the file is in the same directory.

    files = ['91KnQY664BL._AC_SL1500_.jpg']

    for file in files:

        with open(file, 'rb') as image:
                file_data = image.read()
                file_name = image.name
                file_type = imghdr.what(image.name)

        msg.add_attachment(file_data, filename = file_name, maintype = 'image', subtype = file_type)



    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
