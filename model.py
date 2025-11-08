from collections import UserDict
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class Field:
    """Base class for all fields in the contact management system."""
    def __init__(self, value: str) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):  # No reason to modify class
    """Represents a contact's name. Inherits from Field."""


class Phone(Field):
    """Represents a phone number. Inherits from Field"""
    # pylint: disable=super-init-not-called
    def __init__(self, value: str) -> None:
        self.set_phone_number(value)

    def set_phone_number(self, phone: str) -> None:
        """Setter for phone number. Must be a string 10 digigts long"""
        # it will raise an exception in case of validtion error
        self.validate_phone_number(phone)
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
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    """Represents contact details for a person."""
    def __init__(self, name: str) -> None:
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __str__(self) -> str:
        phones = '; '.join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones}"

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
            raise ValueError(f"phone {prev_phone} doesnt exist")

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

    def get_all(self) -> list[Record]:
        """ Returns all records """
        return self.data.values()

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
            bday_date = record.birthday.date()
            # find the next birthday, add the year difference to the birthday 
            # date (it will handle 29th February)
            years_diff = today.year - bday_date.year
            next_bday = bday_date + relativedelta(years=(years_diff))
            if next_bday < today:  # if birthday is in the past, add 1 year
                next_bday = next_bday + relativedelta(years=1)

            # move congratulations to the next Monday if it's a weekend
            next_bday_day_of_week = next_bday.weekday()
            # if next birthday is Saturday, add 2 days (next Monday)
            if next_bday_day_of_week == 5:
                next_bday = next_bday + relativedelta(days=2)
            # if next birthday is Sunday, add 1 day (next Monday)
            elif next_bday_day_of_week == 6:
                next_bday = next_bday + relativedelta(days=1)
            # create a dict with celebrants per date
            if next_bday - today <= timedelta(days=7):
                date_celebrants = upcoming_birthdays_per_date.get(next_bday)
                if date_celebrants is None:
                    date_celebrants = []
                    upcoming_birthdays_per_date[next_bday] = date_celebrants

                date_celebrants.append(name)

            # create a list of celebrants per date sorted by date
            upcoming_birthdays_per_day = []
            
            for date in date_celebrants.keys().sort():
                upcoming_birthdays_per_day.append({
                    "day": date.strftime("%A"),  # Sunday, Monday, ...
                    "celebrants": date_celebrants.get(date)
                })
            
        return upcoming_birthdays_per_day
