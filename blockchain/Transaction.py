class Transaction:
    """
    Represents a simple financial transaction between two people.

    Attributes:
    - __person_from: Sender's address (hex string).
    - __person_to: Receiver's address (hex string).
    - __currency: The type of currency being sent.
    - __amount: The amount of currency being sent.
    - __id: Unique transaction identifier (set later).
    """

    __person_from: str  # Address hex of sender
    __person_to: str  # Address hex of receiver
    __currency: str
    __amount: int
    __id: int

    def __init__(self, p_from: str, p_to: str, currency: str, amount: int) -> None:
        """
        Initializes a transaction.

        :param p_from: Sender's public address (hex).
        :param p_to: Receiver's public address (hex).
        :param currency: Type of currency used.
        :param amount: Amount of currency being transferred.
        """
        self.__person_from = p_from
        self.__person_to = p_to
        self.__currency = currency
        self.__amount = amount
        self.__id = -1

    def set_index(self, id: int) -> None:
        """Sets the unique transaction ID."""
        self.__id = id

    def get_index(self) -> int:
        """Returns the transaction ID."""
        return self.__id

    def get_person_from(self) -> str:
        """Returns the sender's address."""
        return self.__person_from

    def get_person_to(self) -> str:
        """Returns the receiver's address."""
        return self.__person_to

    def get_currency(self) -> str:
        """Returns the currency type used in the transaction."""
        return self.__currency

    def set_currency(self, currency: str) -> None:
        """Sets the currency type."""
        self.__currency = currency

    def get_amount(self) -> int:
        """Returns the transaction amount."""
        return self.__amount

    def set_amount(self, new_amount: int) -> None:
        """Updates the transaction amount."""
        self.__amount = new_amount

    def __str__(self) -> str:
        """Returns a readable transaction summary."""
        return f"{self.__person_from} sent {self.__amount} {self.__currency} to {self.__person_to}"
