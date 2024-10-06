import argparse
import subprocess
import sys
import logging

from typing import Dict
from pathlib import Path

ZURL_PATH: Path = Path("C:/zurl").resolve()
SOFTWARE_DIR: Path = Path(f"{ZURL_PATH}/software")

logging.basicConfig(
    filename=f'{ZURL_PATH}/zurl.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
    )


def zurl_parsing(zurl_string:str) -> None:
    # Default args
    standard_keys = ["service", "ip", "port", "user", "password"]
    config_dict = {}

    try:
        if "zurl://" not in zurl_string:
            raise ValueError(f"ZURL format error: {zurl_string}")
        components = zurl_string[len("zurl://"):]
        components = components.split('/')
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        raise

    # first element only service name
    config_dict["service"] = components[0]
    
    # pars value
    for item in components:
        key_value = item.split('=')
        if len(key_value) == 2:
            key, value = key_value
            config_dict[key.strip()] = value.strip()
    
    # insert empty values other elements
    for key in standard_keys:
        if key not in config_dict:
            config_dict[key] = ""
    
    logging.debug(f"Config: {config_dict}")
    return config_dict


def args_parsing() -> None:
    parser = argparse.ArgumentParser(description='zabbix url for launching services from map')
    parser.add_argument(
        'zurl', 
        type=str, 
        help="format zurl://SERVICE_NAME/ip=IP_ADDR/user=USERNAME/password=PASSWORD/port=PORT")

    try:
        args = parser.parse_args(sys.argv[1:])
    except Exception as e:
        logging.error(f"Error args parsing: {str(e)}")
        raise

    zurl_args: str = getattr(args, "zurl")
    logging.debug(f"Start with args: {zurl_args}")

    return zurl_args


def winbox(**kwargs):
    """winbox64.exe <host> <login> <password>"""
    connect_args: list = [f"{SOFTWARE_DIR}/winbox.exe"]
    ip = connect_config.get('ip')
    user = connect_config.get('user')
    password = connect_config.get('password')
    
    connect_args.append(ip) if ip else None
    connect_args.append(user) if user else None
    connect_args.append(password) if password else None

    logging.info(f"start winbox: {ip} {user}")

    subprocess.Popen(connect_args)


def putty(**kwargs):
    """putty.exe -ssh user@host"""
    connect_args: list = [f"{SOFTWARE_DIR}/putty.exe", "-ssh"]
    ip = connect_config.get('ip')
    user = connect_config.get('user')
    port = connect_config.get('port')

    if ip:
        connect_args.append(ip)
    else:
        logging.error(f"Need IP address to connect putty ssh")
        raise
    if user:
        connect_args[2] = f"{user}@{ip}"
    if port:
        connect_args.append(f"-P")
        connect_args.append(f"{port}")
    logging.info(f"start putty: {ip} {user} {port}")
    subprocess.Popen(connect_args)


def vnc(**kwargs):
    """ vnc.exe ip:port"""
    """ default PORT=5900"""
    connect_args: list = [f"{SOFTWARE_DIR}/vnc.exe"]
    ip = connect_config.get('ip')
    port = connect_config.get('port')
    if ip:
        connect_args.append(ip)
    else:
        logging.error(f"Need IP address to connect vnc")
    if port:
        connect_args[1] = f"{ip}:{port}"
    logging.info(f"start vnc: {ip} {port}")
    subprocess.Popen(connect_args)


def rdp(**kwargs):
    """
    Path: `C:/Windows/system32/mstsc.exe`
    mstsc.exe [/v:<server[:port]>] [/admin] [/f[ullscreen]] 
    # [/w:<width> /h:<height>] [/public] | [/span] [/multimon] [/edit "connection file"] 
    # [/restrictedAdmin] [/remoteGuard] [/prompt] [/shadow:<sessionID> [/control] [/noConsentPrompt]]
    """
    connect_args: list = ["C:/Windows/system32/mstsc.exe"]
    ip = connect_config.get('ip')
    if ip:
        connect_args.append(f"/v:{ip}")
        connect_args.append(f"/f")
    else:
        logging.error(f"Need IP address to connect rdp")
    print(connect_args)
    logging.info(f"start rdp: {ip}")
    subprocess.Popen(connect_args)


def mtr(**kwargs):
    """ WinMTR.exe ip"""
    connect_args: list = [f"{SOFTWARE_DIR}/WinMTR.exe"]
    ip = connect_config.get('ip')
    print(ip)
    if ip:
        connect_args.append(ip)
    else:
        logging.error(f"Need IP address to WinMTR.exe")
    logging.info(f"start WinMTR: {ip}")
    subprocess.Popen(connect_args)


def start_service(connect_config: Dict[str, str]) -> None:
    service_name = connect_config.get('service')
    if service_name == 'winbox':
        winbox(**connect_config)
    elif service_name == 'putty':
        putty(**connect_config)
    elif service_name == 'vnc':
        vnc(**connect_config)
    elif service_name == 'rdp':
        rdp(**connect_config)
    elif service_name == 'mtr':
        mtr(**connect_config)
    else:
        logging.error(f"Unsupported service: {service_name}")
        raise


if __name__ == '__main__':
    args = args_parsing()
    connect_config = zurl_parsing(args)
    start_service(connect_config)
