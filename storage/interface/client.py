"""Storage client interface."""
from abc import ABC, abstractmethod
from typing import List

from config.models.env import StorageConfig
from storage.models.client.key import StorageClientKey
from storage.models.client.medium import Medium
from storage.models.object.file.data import FileData
from storage.models.object.metadata import Metadata
from storage.models.object.models import Object
from storage.models.object.path import StorageKey


class StorageClientInterface(ABC):
    @abstractmethod
    def __init__(self, config: StorageConfig):
        self.config: StorageConfig

    @abstractmethod
    def get(self, key: StorageKey) -> FileData:
        ...

    @abstractmethod
    def stat(self, key: StorageKey) -> Object:
        ...

    @abstractmethod
    def put(self, obj: Object, data: FileData) -> None:
        ...

    @abstractmethod
    def remove(self, key: StorageKey) -> None:
        ...

    @abstractmethod
    def change(self, key: StorageKey, metadata: Metadata) -> None:
        ...

    @abstractmethod
    def list(self, prefix: StorageKey, recursive: bool = False) -> List[StorageKey]:
        ...

    @property
    @abstractmethod
    def name(self) -> StorageClientKey:
        ...

    @property
    @abstractmethod
    def medium(self) -> Medium:
        ...

    @abstractmethod
    def __contains__(self, key: StorageKey) -> bool:
        ...

    # Hash for Pioneer client management set replacement
    @abstractmethod
    def __hash__(self):
        ...

    # String representation for pathing
    @abstractmethod
    def __repr__(self) -> str:
        ...
