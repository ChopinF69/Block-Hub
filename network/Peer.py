from blockchain.Wallet import Wallet


class Peer:
    """
    Represents a person in the network who holds a copy of the blockchain.

    Every Peer has:
    - A unique name.
    - A wallet to store funds and manage transactions.
    - A unique ID assigned later.

    The wallet is initialized when the Peer is created.
    """

    __name: str
    __id: int
    __wallet: Wallet

    def __init__(self, name: str, wallet: Wallet) -> None:
        """
        Initializes a Peer with a name and an associated Wallet.

        :param name: The name of the peer.
        :param wallet: The wallet associated with this peer.
        """
        self.__name = name
        self.__wallet = wallet
        self.__id = -1

    def set_id(self, id: int) -> None:
        """Sets the unique ID for the peer."""
        self.__id = id

    def get_id(self) -> int:
        """Returns the unique ID of the peer."""
        return self.__id

    def get_name(self) -> str:
        """Returns the name of the peer."""
        return self.__name

    def set_name(self, name: str) -> None:
        """Sets the name of the peer."""
        self.__name = name

    def get_wallet(self) -> Wallet:
        """Returns the wallet associated with this peer."""
        return self.__wallet

    def set_wallet(self, wallet: Wallet) -> None:
        """Sets the wallet for the peer."""
        self.__wallet = wallet
