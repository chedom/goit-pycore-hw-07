from collections import UserDict
from datetime import datetime
from dateutil.relativedelta import relativedelta
from datetime import timedelta

class Field:
    """Base class for all fields in the contact management system."""
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

class Name(Field): # No reason to modify class
    """Represents a contact's name. Inherits from Field."""

class Phone(Field):
    """Represents a phone number. Inherits from Field"""
    def __init__(self, value: str) -> None: # pylint: disable=super-init-not-called
        self.set_phone_number(value)

    def set_phone_number(self, phone: str) -> None:
        """Setter for phone number. Must be a string 10 digigts long"""
        self.validate_phone_number(phone) # it will raise an exception in case of validtion error
        self.value = phone

    def validate_phone_number(self, phone: str) -> None:
        """Validate for phone number. Must be a string 10 digigts long"""
        # if not re.fullmatch(r"\d{10}", value) ...
        if not phone.isdigit():
            raise ValueError("Phone number must contain only digits")
        if len(phone) != 10:
            raise ValueError("Phone number must be exactly 10 digits long")

class Birthday(Field):
    """ Represent the date of birthday of a contact. """
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "DD.MM.YYYY")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    """Represents contact details for a person."""
    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self) -> str:
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"

    def add_phone(self, phone: str) -> None:
        """Add phone number to a record."""
        self.phones.append(Phone(phone))

    def remove_phone(self, phone: str) -> None:
        """Remove a phone number for a record."""
        phone_to_remove = self.find_phone(phone)
        self.phones.remove(phone_to_remove)

    def edit_phone(self, prev_phone, new_phone: str) -> None:
        """Edit a phone number for a record."""
        phone_to_edit = self.find_phone(prev_phone)
        if phone_to_edit is None:
            return

        phone_to_edit.set_phone_number(new_phone)

    def find_phone(self, phone: str) -> Phone:
        """Find phone number across available phone numbers."""
        for p in self.phones:
            if p.value == phone:
                return p

        return None

    def add_birthday(self, birthday_raw: str) -> None:
        """ Add a  birthday for a record. """
        self.birthday = Birthday(birthday_raw)

class AddressBook(UserDict):
    """Represents address book."""
    def add_record(self, record: Record) -> None:
        """Add a new record."""
        self.data[record.name.value] = record

    def find(self, name: str) -> Record:
        """Find a record by name."""
        return self.get(name)

    def delete(self, name: str) -> None:
        """Delete a record by a name."""
        self.pop(name, None)

    def get_upcoming_birthdays(self):
        """
        Returns a list of upcoming birthdays from the given list of birthdays.
        """
        upcoming_birthdays_per_date = dict()
    
        today = datetime.today().date()

        for name, record in self.data.items():
            birthday_date = record.birthday.date()
            # find the next birthday, add the year difference to the birthday date (it will handle 29th February)
            next_birthday = birthday_date + relativedelta(years=(today.year - birthday_date.year))
            if next_birthday < today: # if birthday is in the past, add 1 year
                next_birthday = next_birthday + relativedelta(years=1)

            # move congratulations to the next Monday if it's a weekend
            next_birthday_day_of_week = next_birthday.weekday()
            if next_birthday_day_of_week == 5: # if next birthday is Saturday, add 2 days (next Monday)
                next_birthday = next_birthday + relativedelta(days=2)
            elif next_birthday_day_of_week == 6: # if next birthday is Sunday, add 1 day (next Monday)
                next_birthday = next_birthday + relativedelta(days=1)
            # create a dict with celebrants per date
            if next_birthday - today <= timedelta(days=7):
                date_celebrants = upcoming_birthdays_per_date.get(next_birthday)
                if date_celebrants is None:
                    date_celebrants = []
                    upcoming_birthdays_per_date[next_birthday] = date_celebrants

                date_celebrants.append(name)

            # create a list of celebrants per date sorted by date
            upcoming_birthdays_per_day = []
            
            for date in date_celebrants.keys().sort():
                upcoming_birthdays_per_day.append({
                    "day": date.strftime("%A"), # Sunday, Monday, ...
                    "contacts": date_celebrants.get(date)
                })
            
        return upcoming_birthdays_per_day
