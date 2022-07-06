from usbswitcher import samsungGalaxyToModemMode
from at_utils import enableADB
from adb_utils import waitForDevice, uploadAndRunFRPBypass

def main():
    samsungGalaxyToModemMode()
    enableADB()
    waitForDevice()
    uploadAndRunFRPBypass()

if __name__ == "__main__":
    main()