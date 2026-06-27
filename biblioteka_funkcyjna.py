class Book:
    def __init__(self, title, author, total_copies, available_copies):
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.available_copies = available_copies
        self.reservations = []

    def __str__(self):
        return f"{self.title} - {self.author}, dostępne: {self.available_copies}/{self.total_copies}"


class User:
    def __init__(self, login, password, role):
        self._login = login
        self._password = password
        self.role = role

    @property
    def login(self):
        return self._login

    def check_password(self, password):
        return self._password == password


class Reader(User):
    def __init__(self, login, password):
        super().__init__(login, password, "czytelnik")
        self.borrowed_books = []
        self.extension_requests = []

    def borrow_book(self, book):
        self.borrowed_books.append(book)

    def request_extension(self, book_title):
        self.extension_requests.append(book_title)


class Librarian(User):
    def __init__(self, login, password):
        super().__init__(login, password, "bibliotekarz")


class Library:
    def __init__(self):
        self.books = []
        self.users = []

    def add_book(self, book):
        self.books.append(book)

    def add_user(self, user):
        self.users.append(user)

    def login_user(self):
        print("--- LOGOWANIE ---")

        for attempt in range(3):
            login = input("Login: ")
            password = input("Hasło: ")

            user = next(
                filter(
                    lambda u: u.login == login and u.check_password(password),
                    self.users
                ),
                None
            )

            if user:
                print("Zalogowano pomyślnie.")
                return user

            print(f"Nieprawidłowe dane. Pozostało prób: {2 - attempt}")

        print("Przekroczono limit prób. Program zakończony.")
        return None

    def show_catalog(self):
        print("\n--- KATALOG ---")
        list(map(lambda book: print(book), self.books))

    def find_book(self, title):
        return next(
            filter(lambda book: book.title.lower() == title.lower(), self.books),
            None
        )

    def borrow_book(self, reader):
        title = input("Podaj tytuł książki: ")
        book = self.find_book(title)

        if book is None:
            print("Nie znaleziono książki.")
        elif book.available_copies <= 0:
            print("Brak dostępnych sztuk.")
            decision = input("Czy chcesz zarezerwować tę książkę? (t/n): ")

            if decision.lower() == "t":
                book.reservations.append(reader.login)
                print("Książka została zarezerwowana.")
        else:
            book.available_copies -= 1
            reader.borrow_book(book)
            print("Książka została wypożyczona.")

    def show_my_borrowed_books(self, reader):
        print("\n--- MOJE WYPOŻYCZENIA ---")

        if not reader.borrowed_books:
            print("Nie masz wypożyczonych książek.")
        else:
            list(map(lambda book: print(book), reader.borrowed_books))

    def create_extension_request(self, reader):
        print("\n--- PROŚBA O PRZEDŁUŻENIE ---")

        if not reader.borrowed_books:
            print("Nie masz żadnych wypożyczonych książek.")
            return

        list(map(
            lambda item: print(f"{item[0]}. {item[1].title}"),
            enumerate(reader.borrowed_books, start=1)
        ))

        try:
            choice = int(input("Wybierz numer książki: "))
            if 1 <= choice <= len(reader.borrowed_books):
                book = reader.borrowed_books[choice - 1]
                reader.request_extension(book.title)
                print("Prośba o przedłużenie została wysłana.")
            else:
                print("Nieprawidłowy numer.")
        except ValueError:
            print("Wpisz poprawną liczbę.")

    def show_all_borrowed_books(self):
        print("\n--- WSZYSTKIE WYPOŻYCZENIA ---")

        readers = list(filter(lambda user: isinstance(user, Reader), self.users))
        borrowed = [
            (reader.login, book.title)
            for reader in readers
            for book in reader.borrowed_books
        ]

        if not borrowed:
            print("Brak aktualnych wypożyczeń.")
        else:
            list(map(
                lambda item: print(f"Użytkownik: {item[0]} | Książka: {item[1]}"),
                borrowed
            ))

    def show_extension_requests(self):
        print("\n--- PROŚBY O PRZEDŁUŻENIE ---")

        requests = [
            (user.login, request)
            for user in self.users
            if isinstance(user, Reader)
            for request in user.extension_requests
        ]

        if not requests:
            print("Brak próśb o przedłużenie.")
        else:
            list(map(
                lambda item: print(f"Użytkownik: {item[0]} | Książka: {item[1]}"),
                requests
            ))

    def handle_extension_requests(self):
        print("\n--- OBSŁUGA PRÓŚB ---")

        requests = [
            (user, request)
            for user in self.users
            if isinstance(user, Reader)
            for request in user.extension_requests
        ]

        if not requests:
            print("Brak próśb do obsłużenia.")
            return

        list(map(
            lambda item: print(f"{item[0]}. {item[1][0].login} - {item[1][1]}"),
            enumerate(requests, start=1)
        ))

        try:
            choice = int(input("Wybierz numer prośby: "))

            if 1 <= choice <= len(requests):
                user, book_title = requests[choice - 1]
                book = self.find_book(book_title)

                if book and book.reservations:
                    print(f"Uwaga: ta książka ma rezerwacje: {', '.join(book.reservations)}")

                decision = input("Zaakceptować prośbę? (t/n): ")

                if decision.lower() == "t":
                    print("Prośba zaakceptowana.")
                else:
                    print("Prośba odrzucona.")

                user.extension_requests.remove(book_title)
            else:
                print("Nieprawidłowy numer.")
        except ValueError:
            print("Wpisz poprawną liczbę.")

    def filter_catalog(self):
        phrase = input("Podaj frazę w tytule lub autorze: ").lower()

        results = list(filter(
            lambda book: phrase in book.title.lower() or phrase in book.author.lower(),
            self.books
        ))

        if not results:
            print("Brak wyników.")
        else:
            list(map(lambda book: print(book), results))

    def show_available_books(self):
        available = [book for book in self.books if book.available_copies > 0]

        if not available:
            print("Brak dostępnych książek.")
        else:
            list(map(lambda book: print(book), available))

    def sort_catalog(self):
        print("\nSortuj według:")
        print("1. Tytułu")
        print("2. Autora")
        print("3. Liczby dostępnych sztuk")

        choice = input("Wybierz opcję: ")

        sort_options = {
            "1": lambda book: book.title,
            "2": lambda book: book.author,
            "3": lambda book: book.available_copies
        }

        key_function = sort_options.get(choice)

        if key_function is None:
            print("Nieprawidłowy wybór.")
            return

        sorted_books = sorted(self.books, key=key_function)
        list(map(lambda book: print(book), sorted_books))

    def get_readers(self):
        return list(filter(lambda user: isinstance(user, Reader), self.users))

    def display_filtered_collection(self, collection, predicate):
        """Funkcja wyższego rzędu — przyjmuje funkcję jako argument."""
        filtered = list(filter(predicate, collection))
        list(map(lambda item: print(item), filtered))
        return filtered

    def show_statistics(self):
        print("\n--- STATYSTYKI BIBLIOTEKARZA ---")

        borrowed_counts = list(map(
            lambda book: (book.title, book.total_copies - book.available_copies),
            self.books
        ))

        most_popular = max(borrowed_counts, key=lambda item: item[1])

        active_borrows = sum(map(lambda item: item[1], borrowed_counts))

        readers_sorted = sorted(
            self.get_readers(),
            key=lambda reader: len(reader.borrowed_books),
            reverse=True
        )

        print(f"Najpopularniejsza książka: {most_popular[0]} ({most_popular[1]} wypożyczeń)")
        print(f"Liczba aktywnych wypożyczeń ogółem: {active_borrows}")

        print("\nCzytelnicy wg liczby wypożyczonych książek:")
        list(map(
            lambda reader: print(f"{reader.login}: {len(reader.borrowed_books)}"),
            readers_sorted
        ))


def reader_menu(library, reader):
    choice = ""

    while choice != "8":
        print("\n--- MENU CZYTELNIKA ---")
        print("1. Przeglądaj katalog")
        print("2. Wypożycz książkę")
        print("3. Moje wypożyczenia")
        print("4. Poproś o przedłużenie")
        print("5. Wyszukaj książkę")
        print("6. Pokaż dostępne książki")
        print("7. Sortuj katalog")
        print("8. Wyloguj")

        choice = input("Wybierz opcję: ")

        if choice == "1":
            library.show_catalog()
        elif choice == "2":
            library.borrow_book(reader)
        elif choice == "3":
            library.show_my_borrowed_books(reader)
        elif choice == "4":
            library.create_extension_request(reader)
        elif choice == "5":
            library.filter_catalog()
        elif choice == "6":
            library.show_available_books()
        elif choice == "7":
            library.sort_catalog()
        elif choice == "8":
            print("Wylogowano.")
        else:
            print("Nieprawidłowy wybór.")


def librarian_menu(library):
    choice = ""

    while choice != "7":
        print("\n--- MENU BIBLIOTEKARZA ---")
        print("1. Przeglądaj katalog")
        print("2. Lista wypożyczeń")
        print("3. Obsługa próśb o przedłużenie")
        print("4. Wyszukaj książkę")
        print("5. Sortuj katalog")
        print("6. Statystyki")
        print("7. Wyloguj")

        choice = input("Wybierz opcję: ")

        if choice == "1":
            library.show_catalog()
        elif choice == "2":
            library.show_all_borrowed_books()
        elif choice == "3":
            library.handle_extension_requests()
        elif choice == "4":
            library.filter_catalog()
        elif choice == "5":
            library.sort_catalog()
        elif choice == "6":
            library.show_statistics()
        elif choice == "7":
            print("Wylogowano.")
        else:
            print("Nieprawidłowy wybór.")


def create_library():
    library = Library()

    library.add_book(Book("Pan Tadeusz", "Adam Mickiewicz", 3, 3))
    library.add_book(Book("Lalka", "Bolesław Prus", 2, 2))
    library.add_book(Book("Quo Vadis", "Henryk Sienkiewicz", 4, 4))
    library.add_book(Book("Kamienie na szaniec", "Aleksander Kamiński", 1, 1))
    library.add_book(Book("Ferdydurke", "Witold Gombrowicz", 2, 2))

    library.add_user(Reader("jan", "1234"))
    library.add_user(Reader("anna", "abcd"))
    library.add_user(Reader("piotr", "haslo"))
    library.add_user(Librarian("admin", "admin"))

    return library


def main():
    library = create_library()
    user = library.login_user()

    if user is None:
        return

    if isinstance(user, Librarian):
        librarian_menu(library)
    elif isinstance(user, Reader):
        reader_menu(library, user)


main()