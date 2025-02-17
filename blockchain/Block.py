from hashlib import sha256
from datetime import date, datetime
from blockchain.Transaction import Transaction


class Block:
    """
    A simple block class , it should have those properties and a miner class method, that increments the
    nonce until it reaches the difficulty (how many zeros should the hash have in front)
    You have to set: index, previous_hash, current_hash, difficulty
    """

    __index: int
    __nonce: int
    __data: str | None
    __previous_hash: str
    __current_hash: str
    __difficulty: int
    __timestamp: date
    __list_of_transaction: list[Transaction]

    def __init__(self, data: str):
        self.__data = data
        self.__timestamp = datetime.now()
        self.__current_hash = ""
        self.__list_of_transaction = []

    def get_index(self) -> int:
        return self.__index

    def get_current_hash(self) -> str:
        return self.__current_hash

    def get_previous_hash(self) -> str:
        return self.__previous_hash

    def get_data(self) -> str | None:
        return self.__data

    def get_timestamp(self) -> date:
        return self.__timestamp

    def get_nonce(self) -> int:
        return self.__nonce

    def get_difficulty(self) -> int:
        return self.__difficulty

    def get_list_of_transactions(self) -> list[Transaction]:
        return self.__list_of_transaction

    def set_transaction(self, new_amount: int, transaction_index: int) -> None:
        print("number of transcation: ", len(self.__list_of_transaction))
        print("new_amount", new_amount, "transaction_index:", transaction_index)
        if transaction_index is not None and new_amount is not None:
            transaction_index = int(transaction_index)
            self.__list_of_transaction[transaction_index].set_amount(new_amount)

    def set_list_of_transactions(self, list_of_transactions: list[Transaction]) -> None:
        self.__list_of_transaction = list_of_transactions

    def set_data(self, data: str | None) -> None:
        self.__data = data

    def set_index(self, index: int) -> None:
        self.__index = index

    def set_prev_hash(self, prev_hash: str) -> None:
        self.__previous_hash = prev_hash

    def set_difficulty(self, difficulty: int) -> None:
        self.__difficulty = difficulty

    def set_current_hash(self, current_hash: str) -> None:
        self.__current_hash = current_hash

    def set_nonce(self, nonce: int) -> None:
        self.__nonce = nonce

    def calculate_hash(self) -> str:
        all_transaction = "".join(str(tx) for tx in self.__list_of_transaction)
        block_string = f"{self.__index}{self.__previous_hash}{self.__data}{self.__nonce}{all_transaction}"
        return sha256(block_string.encode()).hexdigest()

    def start_mining(self):
        """
        Mines the block by incrementing nonce until the hash has the required number of leading zeros.
        """
        while not self.calculate_hash().startswith("0" * self.__difficulty):
            self.__nonce += 1

        self.__current_hash = self.calculate_hash()

    def get_block_info(self):
        return {
            "index": self.__index,
            "nonce": self.__nonce,
            "data": self.__data,
            "previous_hash": self.__previous_hash,
            "current_hash": self.__current_hash,
            "difficulty": self.__difficulty,
            "timestamp": str(self.__timestamp),
        }
