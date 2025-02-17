from network.Network import Network
from enum import Enum
from typing import Tuple
import random
from network.Peer import Peer
from utils.Logger import LogLevel, Logger

logger = Logger("./logs.log")


class LoginStatus(Enum):
    Fail = 0
    Success = 1
    WrongPassword = 2  # aici vreau sa fac parola de aia smecheroasa din 12 cuvinte
    NoPublicAddress = 3


class RegisterStatus(Enum):
    Fail = 0
    Success = 1
    AlreadyExists = (
        2  # here in long term if i make the register with the same name, i return this
    )


class UserManager:
    """
    Class that replicates the functionality in the dotnet framework
    """

    # __wallets_password: TypedDict[
    #    Tuple["str", "str"]
    # ]  # list of (public addresses, password)
    __network: Network  # list of tuples (peer, service) to have

    def __init__(self, network: Network) -> None:
        self.__network = network
        self.__wallets_password = {}
        for address in self.__network.get_wallets_addresses():
            password = self.generate_password()
            logger.Log(
                LogLevel.Critical, f"Public address : {address}, password : {password}"
            )
            print(address, password)
            # aici eu in loc sa salvez public_address salvez walletul
            self.__wallets_password[address] = password

    def login(self, public_address: str, password: str) -> LoginStatus:
        if public_address not in self.__wallets_password:
            return LoginStatus.NoPublicAddress
        if self.__wallets_password[public_address] != password:
            return LoginStatus.WrongPassword
        return LoginStatus.Success

    def register(self, name: str) -> Tuple[RegisterStatus, str]:
        if name in self.__network.get_peers_names():
            return RegisterStatus.AlreadyExists, ""
        public_address = self.__network.add_peer(name)
        password = self.generate_password()
        self.__wallets_password[public_address] = password
        return RegisterStatus.Success, password

    def generate_password(self) -> str:
        # here i just want a list of concateneted list of 10 words
        list_of_words = []
        with open("./listOfWords.txt", "r") as lines:
            for line in lines:
                list_of_words.append(line.strip())
        return "".join(random.sample(list_of_words, 10))

    def get_all_public_addresses(self):
        return self.__network.get_wallets_addresses()

    def get_peer_by_address(self, public_address: str) -> Peer:
        return self.__network.get_peer_on_public_address(public_address)

    def get_users_public_addresses(self) -> list:
        return [
            (
                peer.get_name(),
                peer.get_wallet().get_public_address(),
                peer.get_wallet().get_balance(),
            )
            for peer, _ in self.__network.get_peers()
        ]

    def add_money(self, public_address: str, amount: int) -> None:
        self.__network.get_peer_on_public_address(
            public_address
        ).get_wallet().add_to_balance(amount)

    def send_money(
        self,
        own_public_address: str,
        public_address_to_send: str,
        amount: int,
        data: str,
    ) -> None:
        # first i need to update the balance of the account that is receveing and the account that is sending
        self.__network.get_peer_on_public_address(own_public_address).get_wallet().pay(
            amount, public_address_to_send
        )
        self.__network.get_peer_on_public_address(
            public_address_to_send
        ).get_wallet().add_to_balance(amount)

        self.__network.make_transaction(
            own_public_address, public_address_to_send, amount, data
        )

    def get_network(self) -> Network:
        return self.__network
