from binascii import Error
import ecdsa
from blockchain.Transaction import Transaction
from utils.Logger import LogLevel, Logger

logger = Logger("./logs.log")


class Wallet:
    """
    This is a simple wallet class that holds the public key, private key, balance,
    and transaction history of a user.

    Attributes:
    - __public_key (str): The wallet's public address, derived from the private key.
    - __private_key (str): The private key used for signing transactions.
    - __balance (int): The balance of the wallet.
    - __transaction_history (list[Transaction]): A list of transactions associated with the wallet.
    """

    __public_key: str
    __private_key: str
    __balance: int
    __transaction_history: list[Transaction]

    def __init__(self):
        """
        Initializes the wallet with a zero balance and an empty transaction history.
        The wallet keys are generated later using `create_wallet()`.
        """
        self.__transaction_history = []
        self.__balance = 0

    def create_wallet(self):
        """
        Generates a new private and public key pair using ECDSA (Elliptic Curve Digital Signature Algorithm).
        The private key is used for signing, and the public key acts as the wallet address.
        """
        self.__sk = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)
        self.__private_key = self.__sk.to_string().hex()

        self.__vk = self.__sk.get_verifying_key()
        self.__public_key = self.__vk.to_string().hex()

        # logger.Log(LogLevel.Critical, f"Public Key (hex): {self.__public_key}")
        logger.Log(LogLevel.Critical, f"Private Key (hex): {self.__private_key}")

    def get_balance(self) -> int:
        """
        Returns the current balance of the wallet.

        :return: Wallet balance as an integer.
        """
        return self.__balance

    def add_to_balance(self, amount: int) -> None:
        """
        Adds funds to the wallet's balance.

        :param amount: The amount to add to the wallet balance.
        """
        self.__balance += amount

    def add_transaction(
        self, amount: int, currency: str, recipient_address: str
    ) -> None:
        """
        Adds a transaction to the wallet's transaction history.

        :param amount: The amount to be transferred.
        :param currency: The currency type.
        :param recipient_address: The recipient's public address.
        """
        new_transaction = Transaction(
            self.__public_key, recipient_address, currency, amount
        )
        new_transaction.set_index(len(self.__transaction_history) - 1)
        self.__transaction_history.append(new_transaction)

    def pay(self, amount: int, recipient_address: str) -> None:
        """
        Sends a payment from the wallet if sufficient balance is available.

        :param amount: The amount to send.
        :param recipient_address: The recipient's wallet address.
        :raises Error: If there are insufficient funds in the wallet.
        """
        if self.__balance >= amount:
            self.__balance -= amount
            self.add_transaction(amount, "my_currency", recipient_address)
            print(
                f"Paid {amount} to {recipient_address}. New balance: {self.__balance}"
            )
        else:
            raise Error("Not enough money")

    def get_transaction_history(self) -> list[Transaction]:
        """
        Retrieves the list of past transactions for this wallet.

        :return: A list of Transaction objects.
        """
        return self.__transaction_history

    def get_public_address(self) -> str:
        """
        Returns the wallet's public address (public key).

        :return: The public key as a string.
        """
        return self.__public_key


if __name__ == "__main__":
    wallet = Wallet()
    wallet.create_wallet()
