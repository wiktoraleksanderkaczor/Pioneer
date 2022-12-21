import ipaddress
import socket
from typing import Union

from pydantic import AnyUrl
from zeroconf import ServiceBrowser, ServiceInfo, ServiceListener, Zeroconf

from config.discovery import fqdn_service, service
from config.env import env
from role.distribution import Distributed


class ObjectStashListener(ServiceListener):
    def update_service(self, zc: Zeroconf, type_: str, name: AnyUrl) -> None:
        info: Union[ServiceInfo, None] = zc.get_service_info(type_, name)
        if info:
            print(f"Service {name} updated, service info: {info}")

    def remove_service(self, zc: Zeroconf, type_: str, name: AnyUrl) -> None:
        info: Union[ServiceInfo, None] = zc.get_service_info(type_, name)
        if info:
            print(f"Service {name} removed, service info: {info}")
            Distributed.peers.remove(name)
            for obj in Distributed.distributed_objects:
                obj.removeNodeFromCluster(name)

    def add_service(self, zc: Zeroconf, type_: str, name: AnyUrl) -> None:
        info: Union[ServiceInfo, None] = zc.get_service_info(type_, name)
        if not info:
            return

        # Validate service type
        if type_ != fqdn_service:
            return

        # Validate IP address
        addresses = [socket.inet_ntoa(addr) for addr in info.addresses]
        addresses = [addr for addr in addresses if not ipaddress.ip_address(addr).is_loopback]
        if not addresses:
            return

        # Decode properties
        properties = {k.decode(): v.decode() for k, v in info.properties.items()}

        # Validate cluster name
        if properties.get("cluster", "") != env.cluster.name:
            return

        # Add service to list of peers
        print(f"Service {name} added, service info: {info}")
        Distributed.peers.append(name)
        for obj in Distributed.distributed_objects:
            obj.addNodeToCluster(name)


class ObjectStashCoordinator:
    def __init__(self) -> None:
        # Initialise zeroconf and listeners
        self.zeroconf = Zeroconf(interfaces=["0.0.0.0"])
        self.listener = ObjectStashListener()
        self.browser = ServiceBrowser(self.zeroconf, fqdn_service, self.listener)

        # Register service
        self.service = service
        self.zeroconf.register_service(self.service, cooperating_responders=True)

    def __del__(self):
        self.zeroconf.unregister_service(self.service)
        self.zeroconf.close()
        del self
