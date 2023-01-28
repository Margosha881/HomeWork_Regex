import re
import os
import csv

regex = r"(\+7|8)\s*\(?(\d{3})\s*-?\)?\s*(\d{3})\s*-?(\d{2})\s*-?(\d{2})\s*\(?(доб.)?\s*(\d{4})?\)?"
subst = r"+7(\2)\3-\4-\5 \6\7"

folder = os.getcwd()
files = os.listdir()
for file in files:
    if '.csv' in file:
        path_to_file = os.path.join(folder, file)


def read_file():
    with open(path_to_file,encoding='utf-8') as f:
      rows = csv.reader(f, delimiter=",")
      contacts_list = list(rows)
    return contacts_list


def parse_contact_list(contacts_list):
    new_contacts_list = list()
    for contact in contacts_list:
        new_contact = list()
        full_name_str = ",".join(contact[:3])
        result = re.findall(r'(\w+)', full_name_str)
        while len(result) < 3:
            result.append('')
        new_contact += result
        new_contact.append(contact[3])
        new_contact.append(contact[4])
        phone_pattern = re.compile(regex)
        changed_phone = phone_pattern.sub(subst, contact[5])
        new_contact.append(changed_phone)
        new_contact.append(contact[6])
        new_contacts_list.append(new_contact)
    return new_contacts_list


def delete_duplicates_contact(new_contacts_list):
    phone_book = dict()
    for contact in new_contacts_list:
        if contact[0] in phone_book:
            contact_value = phone_book[contact[0]]
            for i in range(len(contact_value)):
                if contact[i]:
                    contact_value[i] = contact[i]
        else:
            phone_book[contact[0]] = contact
    return list(phone_book.values())


def write_data(new_contacts_list):
    with open("phonebook.csv", "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(new_contacts_list)


new_contacts_list = read_file()
new_parsed_list = parse_contact_list(new_contacts_list)
contact_book_values = delete_duplicates_contact(new_parsed_list)
write_data(contact_book_values)


