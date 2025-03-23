from collections import UserDict
import re


class Field:
    # Base class for record fields.

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    

class Name(Field):
    # Class for storing contact name. Required field.
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty.")
        super().__init__(value)


class Phone(Field):
    # Class for storing phone numbers. Has format validation (10 digits).

    def __init__(self, value):
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)

    def __eq__(self, other):
        """Compare phone numbers by value, not object reference."""
        if isinstance(other, Phone):
            return self.value == other.value
        return False


class Record:
    # A class for storing contact information, including name and phone list.

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []


    def add_phone(self, phone):
        if isinstance(phone, str):  # If the passed phone number is a string, we create a Phone object
            phone = Phone(phone)
        if not isinstance(phone, Phone):
            raise ValueError("Phone must be an instance of Phone class.")
        self.phones.append(phone)
    

    def find_phone(self, phone):
        if isinstance(phone, str):
            phone = Phone(phone)
        for p in self.phones:
            if p == phone:
                return p
        return None


    def remove_phone(self, phone):
        phone_obj = self.find_phone(phone)  
        if phone_obj:
            self.phones.remove(phone_obj)
        else:
            raise ValueError("The phone number not found.")
    

    def edit_phone(self, old_phone, new_phone):
        try:
            new_phone_obj = Phone(new_phone)
        except:
            raise ValueError("The phone number is not valid.")

        phone_obj = self.find_phone(old_phone) 
        if phone_obj:
            self.remove_phone(old_phone)  
            self.add_phone(new_phone)
        else:
            raise ValueError("The phone number not found.")

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(str(p) for p in self.phones)}"
    

class AddressBook(UserDict):
    # A class for storing and managing records.

    def add_record(self, record):
        if not isinstance(record, Record):
            raise ValueError("Record must be an instance of Record class.")
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError("Record not found.")

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())
        


# Створення нової адресної книги
book = AddressBook()

# Створення запису для John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")

# Додавання запису John до адресної книги
book.add_record(john_record)

# Створення та додавання нового запису для Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
book.add_record(jane_record)

# Виведення всіх записів у книзі 
print(book)

# Знаходження та редагування телефону для John
john = book.find("John")
print("--------------------------------------")

print(john)
print("--------------------------------------")

john.edit_phone("1234567890", "11122233337")

print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555
print("--------------------------------------")

# Пошук конкретного телефону у записі John
found_phone = john.find_phone("5555555555")
print(f"{john.name}: {found_phone}")  # Виведення: John: 5555555555

# Видалення запису Jane
book.delete("Jane")
print("--------------------------------------")

print(book)