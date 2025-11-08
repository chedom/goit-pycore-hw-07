from functools import wraps
from model import AddressBook, Record


def input_error(func):
    @wraps(func) # preserve function's metadate
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError, KeyError) as e:
            return f"Verify the argument for the command: {e}"

    return inner


@input_error
def add_contact(args: list[str], book: AddressBook) -> None:
    """ Add new contact to the contact list """
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."

    record.add_phone(phone)

    return message


@input_error
def change_contact(args: list[str], book: AddressBook) -> str:
    """ Change the phone of specified name, it works only if name has already existed """
    name, prev_phone, new_phone, *_ = args

    record = book.find(name)
    if record is None:
        raise ValueError(f"Contact {name} doesnt exist.")

    record.edit_phone(prev_phone, new_phone)

    return "Contact changed."


@input_error
def show_phone(args: list[str], book: AddressBook) -> str:
    """ Returns phone number for specified name """
    name, *_ = args

    record = book.find(name)
    if record is None:
        raise ValueError(f"Contact {name} doesnt exist.")
    # assume that record has implemented (__str__) custom string representation
    return str(record)


@input_error
def show_all_phone(book: AddressBook) -> str:
    """ List all contacts """
    # assume that record has implemented (__str__) custom string representation
    formated_contacts = [str(record) for record in book.get_all()]

    return "\n".join(formated_contacts)


@input_error
def add_birthday(args: list[str], book: AddressBook) -> str:
    """ Add birthday for a contact """ 
    name, bday, *_ = args

    record = book.find(name)
    if record is None:
        raise ValueError(f"Contact {name} doesnt exist.")

    record.add_birthday(bday)


@input_error
def show_birthday(args: list[str], book: AddressBook) -> str:
    """ Add birthday for a contact """ 
    name, *_ = args

    record = book.find(name)
    if record is None:
        raise ValueError(f"Contact {name} doesnt exist.")

    bday = record.birthday
    if bday is None:
        return "Birthday is not specified for the contat"

    return bday.strftime("%d.%m.%Y")


@input_error
def birthdays(book: AddressBook) -> str:
    """ List celebrants for the next 7 days. """
    upcoming_birthdays = book.get_upcoming_birthdays()
    if not upcoming_birthdays:
        return "No upcoming birhdays"

    formated_bdays = []

    for day_celebrants in upcoming_birthdays:
        celebrants = ', '.join(day_celebrants.celebrants)
        msg = f"For the day {day_celebrants.day} next celebrants: {celebrants}"
        formated_bdays.append(msg)

    return "\n".join(formated_bdays)
