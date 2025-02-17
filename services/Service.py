from blockchain.Block import Block
from blockchain.Blockchain import BlockChain
import copy

from blockchain.Transaction import Transaction


class ServiceBlockChain:
    """
    Singleton class to pass around the blockchain object
    """

    __blockchain: BlockChain
    __layers: list

    def __init__(self, difficulty: int) -> None:
        self.__blockchain = BlockChain(difficulty)
        self.__layers = []
        # self.initialize()
        pass

    def initialize(self) -> None:
        block1 = Block(data="alex")
        block2 = Block(data="theo")

        transactions = [
            Transaction("p_from1", "p_to1", "dollar", 25),
            Transaction("p_from2", "p_to2", "euro", 20),
            Transaction("p_from3", "p_to3", "leva", 15),
            Transaction("p_from4", "p_to4", "ron", 22),
            Transaction("p_from5", "p_to5", "pound", 35),
        ]
        for i in range(len(transactions)):
            transactions[i].set_index(i)
        block1.set_list_of_transactions(
            [
                transactions[0],
                transactions[1],
                transactions[2],
            ],
        )

        block2.set_list_of_transactions(
            [
                transactions[3],
                transactions[4],
            ],
        )

        self.__blockchain.add_block(block1)
        self.__blockchain.add_block(block2)

    def get_instance(self) -> BlockChain:
        return self.__blockchain

    def get_old_blocks(self) -> list:
        return self.__layers

    def get_latest_blocks(self) -> list[Block]:
        return self.__blockchain.get_blocks()

    def update_blocks_data(
        self,
        block_index: int,
        data: str | None,
    ) -> None:
        # here i want to update the block with the index specified
        # and after that block i need to update all the blocks nonce
        # self.__layers.append(self.__blockchain.get_blocks()) # wrong because it copies references, not actual copies
        self.__layers = []
        self.__layers.append(copy.deepcopy(self.__blockchain.get_blocks()))
        self.__blockchain.update_block_data(block_index, data)  # here already remined

        for i in range(block_index, self.__blockchain.get_number_of_blocks()):
            # here i need to update the nonce, the previous_hash and the current_hash
            self.__blockchain.remine(i)
            self.__blockchain.update_block_prev_hash(i)

    def update_blocks_transaction_amount(
        self, block_index: int, new_amount: int, transaction_index: int
    ):
        self.__layers = []
        self.__layers.append(copy.deepcopy(self.__blockchain.get_blocks()))
        self.__blockchain.update_block_transaction(
            block_index, new_amount, transaction_index
        )
        for i in range(block_index, self.__blockchain.get_number_of_blocks()):
            self.__blockchain.remine(i)
            self.__blockchain.update_block_prev_hash(i)

    def get_block_transactions(self, block_index: int) -> list[Transaction]:
        return self.__blockchain.get_blocks()[block_index].get_list_of_transactions()

    def add_transaction(
        self, public_address_1: str, public_address_2, amount: int, data: str
    ) -> None:
        transaction = Transaction(public_address_1, public_address_2, "euro", amount)
        transaction.set_index(0)
        block = Block(data)
        block.set_list_of_transactions([transaction])
        self.__blockchain.add_block(block)
