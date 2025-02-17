import uuid
import time
from network.Network import Network
from services.UserManager import UserManager


class SessionManager:
    def __init__(self, sesion_timeout=1800) -> None:
        self.__sessions = {}  # session_id -> UserManager
        self.__sesion_timeout = sesion_timeout
        pass

    def generate_session(self, lst_of_names: list[str], difficulty: int):
        """
        Creates a new session (room) with a unique ID.

        :return: The session ID
        """
        session_id = str(uuid.uuid4())
        self.__sessions[session_id] = {
            "users": lst_of_names,
            "expiry": time.time() + self.__sesion_timeout,
            "user_manager": UserManager(Network(lst_of_names, difficulty)),
        }
        return session_id, self.__sessions[session_id]["user_manager"]

    def get_user_manager(self, session_id: str) -> UserManager:
        """
        Returns the UserManager for a given session.

        :param session_id: The session (room) ID as a string.
        :return: The UserManager instance or None if session doesn't exist.
        """
        return self.__sessions.get(session_id, {}).get("user_manager")

    def get_session_users(self, session_id):
        """
        Returns the list of users in a session.

        :param session_id: The session (room) ID
        :return: List of users in the session
        """
        return self.__sessions.get(session_id, {}).get("users", [])

    def cleanup_sessions(self):
        """
        Removes expired sessions.
        """
        expired_sessions = [
            s_id
            for s_id, data in self.__sessions.items()
            if time.time() > data["expiry"]
        ]
        for s_id in expired_sessions:
            del self.__sessions[s_id]

    def set_session(self, userManager: UserManager) -> None:
        self.__user_manager = userManager

    def get_session(self) -> UserManager:
        return self.__user_manager
