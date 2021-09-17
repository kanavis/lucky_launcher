""" Platform """
import platform


class Platform:
    @property
    def system(self) -> str:
        return platform.system().lower()

    @property
    def is_windows(self) -> bool:
        return self.system == 'windows'

    @property
    def is_mac(self) -> bool:
        return self.system == 'darwin'


plat = Platform()
