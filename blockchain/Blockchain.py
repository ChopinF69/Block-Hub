from blockchain.Block import Block


class BlockChain:
    """
    A simple blockchain class that maintains a list of blocks.

    Attributes:
    - __blocks (list[Block]): The list of blocks in the blockchain.
    - __initial_block (Block): The first block in the blockchain (Genesis Block).
    - __difficulty (int): The mining difficulty level.
    - __curent_block (Block): The latest block added to the blockchain.
    """

    __blocks: list[Block]
    __initial_block: Block
    __difficulty: int
    __curent_block: Block

    def __init__(self, difficulty):
        """
        Initializes the blockchain with a given mining difficulty.
        Creates the genesis block and adds it to the chain.

        :param difficulty: The mining difficulty level.
        """
        self.__difficulty = difficulty
        self.__initial_block = self.create_genesis_block()
        self.__curent_block = self.__initial_block

        self.__blocks = []
        self.__blocks.append(self.__initial_block)

    def create_genesis_block(self) -> Block:
        """
        Creates the first block of the blockchain, known as the Genesis Block.
        This block has a predefined previous hash and is mined automatically.

        :return: The created Genesis Block.
        """
        new_block = Block("Genesis block")
        new_block.set_index(0)
        new_block.set_prev_hash(
            "0000000000000000000000000000000000000000000000000000000000000000"
        )
        new_block.set_difficulty(self.__difficulty)
        new_block.set_nonce(0)
        new_block.start_mining()
        return new_block

    def add_block(self, block_to_add: Block) -> None:
        """
        Adds a new block to the blockchain after setting its required properties.

        :param block_to_add: The block to be added to the chain.
        """
        block_to_add.set_index(self.__curent_block.get_index() + 1)
        block_to_add.set_prev_hash(self.__curent_block.get_current_hash())
        block_to_add.set_difficulty(self.__difficulty)
        block_to_add.set_nonce(0)
        block_to_add.start_mining()

        self.__blocks.append(block_to_add)
        self.__curent_block = block_to_add

    def update_block_data(self, index: int, data: str | None) -> None:
        """
        Updates the data of a specific block and re-mines it.

        :param index: The index of the block to be updated.
        :param data: The new data to be stored in the block.
        """
        self.__blocks[index].set_data(data)
        self.__blocks[index].start_mining()

    def update_block_transaction(
        self, index_block: int, new_amount: int, transaction_index: int
    ) -> None:
        """
        Updates a specific transaction in a block and re-mines it.

        :param index_block: The index of the block in the chain.
        :param new_amount: The updated transaction amount.
        :param transaction_index: The index of the transaction within the block.
        """
        print(
            "update_block_transaction: ",
            len(self.__blocks[index_block].get_list_of_transactions()),
        )
        self.__blocks[index_block].set_transaction(new_amount, transaction_index)

    def update_block_prev_hash(self, index: int) -> None:
        """
        Updates the previous hash of a block to maintain chain integrity.

        :param index: The index of the block to be updated.
        """
        self.__blocks[index].set_prev_hash(self.__blocks[index - 1].get_current_hash())

    def is_chain_valid(self) -> bool:
        """
        Validates the blockchain by checking if each block's hash and previous hash are correct.

        :return: True if the blockchain is valid, otherwise False.
        """
        for i in range(1, len(self.__blocks)):
            current_block = self.__blocks[i]
            prev_block = self.__blocks[i - 1]

            if current_block.__current_hash != current_block.calculate_hash():
                return False
            if current_block.__previous_hash != prev_block.__current_hash:
                return False
        return True

    def print_chain(self) -> None:
        """
        Prints details of all blocks in the blockchain.
        """
        for block in self.__blocks:
            print(block.get_block_info())

    def get_blocks(self) -> list[Block]:
        """
        Retrieves the list of all blocks in the blockchain.

        :return: A list of Block objects.
        """
        return self.__blocks

    def get_number_of_blocks(self) -> int:
        """
        Returns the total number of blocks in the blockchain.

        :return: The number of blocks in the chain.
        """
        return len(self.__blocks)

    def remine(self, index: int) -> None:
        """
        Re-mines a specific block to update its hash and ensure it meets the difficulty requirement.

        :param index: The index of the block to be re-mined.
        """
        self.__blocks[index].start_mining()
