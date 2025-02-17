from network.Peer import Peer
from services.Service import ServiceBlockChain
from typing import List, Tuple
from blockchain.Wallet import Wallet


class Network:
    """
    Simple class to display all the users and the data of the blockchain will be distributed
    such that every user will hold a copy of the blockchain ( a service )
    when the app starts, every user will have its own copy
    """

    __list_peer_service: list[tuple]  # list of (peer, service)
    __list_names = []
    __difficulty: int

    def __init__(self, list_of_names: list[str], difficulty: int) -> None:
        self.__list_peer_service = []
        self.__list_names = list_of_names
        self.__difficulty = difficulty
        for i in range(len(list_of_names)):
            wallet = Wallet()
            wallet.create_wallet()
            peer = Peer(list_of_names[i], wallet)
            peer.set_id(i)
            self.__list_peer_service.append((peer, ServiceBlockChain(difficulty)))

        pass

    def get_peers(self) -> List[Tuple["Peer", "ServiceBlockChain"]]:
        return self.__list_peer_service

    def get_wallets_addresses(self) -> list[str]:
        return [
            peer.get_wallet().get_public_address()
            for peer, _ in self.__list_peer_service
        ]

    def get_peers_names(self) -> list[str]:
        return self.__list_names

    def add_peer(self, name: str) -> str:
        self.__list_names.append(name)
        wallet = Wallet()
        wallet.create_wallet()
        peer = Peer(name, wallet)
        peer.set_id(len(self.__list_names) - 1)
        self.__list_peer_service.append((peer, ServiceBlockChain(self.__difficulty)))
        return wallet.get_public_address()

    def get_peer_on_public_address(self, public_address: str) -> Peer:
        for peer, _ in self.__list_peer_service:
            if peer.get_wallet().get_public_address() == public_address:
                return peer
        raise Exception("No peer on that public address")

    def make_transaction(
        self, public_address_1: str, public_address_2: str, amount: int, data: str
    ) -> None:
        for _, service in self.__list_peer_service:
            service.add_transaction(public_address_1, public_address_2, amount, data)
