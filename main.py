from input.input import Input
from input.input import Type as TypeInput

def main():
    """ Chương trình chính """
    print("📅 Schedule Generator")
    print("1️⃣ Enter tasks manually")
    print("2️⃣ Load tasks from JSON file")

    choice = Input.inputNumber("👉 Choose an option (1-2): ", 1, 2)
    input_type = TypeInput.ENTER if choice == 1 else TypeInput.JSON

    scheduler = Input(input_type)
    scheduler.run()

if __name__ == "__main__":
    main()