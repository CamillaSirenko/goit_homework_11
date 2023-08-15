from collections import UserDict
import datetime

class Field:
    def __init__(self, name):
        self.name = name
        self._value = None

    def set_value(self, value):
        self._value = value

    def get_value(self):
        return self._value


class Name(Field):
    def __init__(self, value):
        super().__init__('Ім\'я')
        self.set_value(value)

    def set_value(self, value):
        if not value:
            raise ValueError("Ім'я не може бути порожнім")
        super().set_value(value)


class Phone(Field):
    def __init__(self, value):
        super().__init__('Телефон')
        self.value = []
        self.add_number(value)

    def add_number(self, number):
        if not all(char.isdigit() for char in number):
            raise ValueError("Номер телефону повинен складатися лише з цифр")
        self.value.append(number)

    def remove_number(self, number):
        if number in self.value:
            self.value.remove(number)

    def set_value(self, value):
        if not all(char.isdigit() for char in value):
            raise ValueError("Номер телефону повинен складатися лише з цифр")
        super().set_value(value)

    def get_value(self):
        return self.value


class Birthday(Field):
    def __init__(self, value):
        super().__init__('День народження')
        self.set_value(value)

    def set_value(self, value):
        if not isinstance(value, datetime.date):
            raise ValueError("День народження повинен бути об'єктом datetime.date")
        super().set_value(value)

    def get_value(self):
        return self._value


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.optional_fields = {}
        if phone:
            self.add_phone(phone)
        if birthday:
            self.add_birthday(birthday)

    def add_field(self, field):
        if isinstance(field, Field):
            self.optional_fields[field.name] = field

    def remove_field(self, field_name):
        if field_name in self.optional_fields:
            del self.optional_fields[field_name]

    def edit_field(self, field_name, new_value):
        if field_name in self.optional_fields:
            self.optional_fields[field_name].set_value(new_value)

    def add_phone(self, phone):
        if isinstance(phone, Phone):
            self.optional_fields['Телефон'] = phone

    def add_birthday(self, birthday):
        if isinstance(birthday, Birthday):
            self.optional_fields['День народження'] = birthday

    def days_to_birthday(self):
        if 'День народження' in self.optional_fields and self.optional_fields['День народження'].get_value():
            today = datetime.date.today()
            birthday = self.optional_fields['День народження'].get_value()
            next_birthday = datetime.date(today.year, birthday.month, birthday.day)
            if today > next_birthday:
                next_birthday = datetime.date(today.year + 1, birthday.month, birthday.day)
            days_remaining = (next_birthday - today).days
            return days_remaining


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.get_value()] = record

    def __iter__(self):
        self._iter_keys = iter(self.data.keys())
        return self

    def __next__(self):
        try:
            key = next(self._iter_keys)
            return self.data[key]
        except StopIteration:
            raise StopIteration

    def iterator(self, batch_size):
        iter_keys = iter(self.data.keys())
        while True:
            batch = [self.data[next(iter_keys)] for _ in range(batch_size)]
            if not batch:
                break
            yield batch


if __name__ == "__main__":
    name = Name('Білл')
    phone = Phone('1234567890')
    birthday = Birthday(datetime.date(1990, 8, 14))
    rec = Record(name, phone=phone, birthday=birthday)
    ab = AddressBook()
    ab.add_record(rec)

    assert isinstance(ab['Білл'], Record)
    assert isinstance(ab['Білл'].name, Name)
    assert isinstance(ab['Білл'].optional_fields['Телефон'], Phone)
    assert isinstance(ab['Білл'].optional_fields['День народження'], Birthday)
    assert ab['Білл'].optional_fields['Телефон'].get_value()[0] == '1234567890'
    assert ab['Білл'].days_to_birthday() == 365  # Change this based on current date and birthday

    print('Все Ок :)')