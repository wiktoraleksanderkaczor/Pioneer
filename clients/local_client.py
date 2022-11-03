import os
from typing import List

from ..storage import Capability, StorageClient
from ..validation import JSONish, Key


class LocalCLient(StorageClient):
    client_name: str = "Local"
    capabilities: List[Capability] = [Capability.BASIC]

    def __init__(self, container: str, region: str = None, secure: bool = True):
        super().__init__(container, region, secure)

    def create_container(self) -> bool:
        os.mkdir(self.container)
        return self.container_exists(self.container)

    def container_exists(self) -> bool:
        return os.path.isdir(self.container)

    def object_exists(self, key: Key) -> bool:
        return os.path.isfile(key)

    def get_object(self, key: Key) -> JSONish:
        with open(key, "r") as infile:
            return JSONish(infile)
