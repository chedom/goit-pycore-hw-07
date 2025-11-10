import handlers
from model import AddressBook


def parse_input(user_input: str) -> (str, list[str]):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()

    return cmd, *args


def main():
    contacts = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        if user_input == "":
            print("You havent specified any command.")
            continue

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(handlers.add_contact(args, contacts))
        elif command == "change":
            print(handlers.change_contact(args, contacts))
        elif command == "phone":
            print(handlers.show_phone(args, contacts))
        elif command == "all":
            print(handlers.show_all_phone(contacts))
        elif command == "add-birthday":
            print(handlers.add_birthday(args, contacts))
        elif command == "show-birthday":
            print(handlers.show_birthday(args, contacts))
        elif command == "birthdays":
            print(handlers.birthdays(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
