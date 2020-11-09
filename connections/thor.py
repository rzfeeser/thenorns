from typing import Any, Dict, Optional

#from netmiko import ConnectHandler
import paramiko   # required to call the bifrost

# the power of my ancestors
from nornir.core.configuration import Config

# we must cause ragnarok
CONNECTION_NAME = "ragnarok"

class Paramiko:
    """
    This plugin connects to the device using the Netmiko driver and sets the
    relevant connection.
    Inventory:
        extras: maps to argument passed to ``ConnectHandler``.
    """

    def open(
        self,
        hostname: Optional[str],
        username: Optional[str],
        password: Optional[str],
        port: Optional[int],
        platform: Optional[str],
        extras: Optional[Dict[str, Any]] = None,
        configuration: Optional[Config] = None,
    ) -> None:
        parameters = {
            "host": hostname,
            "username": username,
            "password": password,
            "port": port,
        }

        try:
            parameters[
                "ssh_config_file"
            ] = configuration.ssh.config_file  # type: ignore
        except AttributeError:
            pass

        #if platform is not None:
            # Look platform up in corresponding map, if no entry return the host.nos unmodified
            #platform = napalm_to_netmiko_map.get(platform, platform)
            #parameters["device_type"] = platform

        extras = extras or {}
        parameters.update(extras)
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy())
        connection = client.connect(**parameters)

        self.connection = connection

    def close(self) -> None:
        self.client.close()
