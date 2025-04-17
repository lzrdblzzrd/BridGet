import os
import pathlib
import shutil
import subprocess
import sys
import tarfile
import urllib.request

TOR_URL = "https://mirror.oldsql.cc/tor/dist/torbrowser/14.5/tor-expert-bundle-windows-x86_64-14.5.tar.gz"
BRIDGES_URL = "https://torscan-ru.ntc.party/relays.txt"
TOR_FILE = pathlib.Path("tor.exe")
TORRC_FILE = pathlib.Path("torrc")


def main():
    if not TOR_FILE.is_file():
        download_tor()
    if not TORRC_FILE.is_file():
        create_torrc()
    download_tor_bridges()
    run_tor()
    sys.exit(status=0)


def download_tor():
    try:
        urllib.request.urlretrieve(url=TOR_URL, filename="tor.tar.gz")
        with tarfile.open(name="tor.tar.gz") as tar:
            tar.extractall()
        shutil.move(src="tor/tor.exe", dst="tor.exe")
        shutil.move(src="data/geoip", dst="geoip")
        shutil.move(src="data/geoip6", dst="geoip6")
        for directory in ["data", "docs", "tor"]:
            shutil.rmtree(path=directory)
        os.remove(path="tor.tar.gz")

    except Exception as exception:
        print(exception)
        sys.exit(status=1)


def create_torrc():
    try:
        with open(file="torrc", mode="w") as file:
            file.write("""DataDirectory data
ClientOnly 1

GeoIPFile geoip
GeoIPv6File geoip6

UseBridges 1
# ExcludeNodes {ru}

%include bridges.conf
""")
    except Exception as exception:
        print(exception)
        sys.exit(status=2)


def download_tor_bridges():
    try:
        with urllib.request.urlopen(url=BRIDGES_URL) as response:
            bridges = response.read().decode(encoding="UTF-8").strip().split(sep="\n")
            with open(file="bridges.conf", mode="w") as file:
                for bridge in bridges:
                    file.write(f"Bridge {bridge}\n")
    except Exception as exception:
        print(exception)
        sys.exit(status=3)


def run_tor():
    try:
        subprocess.Popen(args=["tor", "-f", "torrc"], creationflags=subprocess.DETACHED_PROCESS)
    except Exception as exception:
        print(exception)
        sys.exit(status=4)


if __name__ == "__main__":
    main()
