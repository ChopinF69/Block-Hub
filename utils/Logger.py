from enum import Enum


class LogLevel(Enum):
    Trace = 0
    Debug = 1
    Information = 2
    Warning = 3
    Error = 4
    Critical = 5


class Logger:
    COLORS = {
        LogLevel.Trace: "\033[90m",  # Gray
        LogLevel.Debug: "\033[94m",  # Blue
        LogLevel.Information: "\033[92m",  # Green
        LogLevel.Warning: "\033[93m",  # Yellow
        LogLevel.Error: "\033[91m",  # Red
        LogLevel.Critical: "\033[95m",  # Magenta
        "RESET": "\033[0m",  # Reset color
    }

    def __init__(self, file_path: str) -> None:
        self.__file_path = file_path
        pass

    def Log(self, level: LogLevel, message: str) -> None:
        color = Logger.COLORS.get(level, Logger.COLORS["RESET"])
        level_name = level.name.upper()
        log_entry = f"[{level_name}] {message}\n"

        with open(self.__file_path, "a") as f:
            f.write(log_entry)

        print(f"{color}{log_entry}{Logger.COLORS['RESET']}", end="")

    def end(self) -> None:
        """
        Clears the log file by deleting its contents.
        """
        open(self.__file_path, "w").close()
        print("\033[91m[LOGS CLEARED]\033[0m")
