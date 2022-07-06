import usb.core

SAMSUNG_GALAXY_ID_VENDOR = 0x04e8
SAMSUNG_GALAXY_ID_PRODUCT = 0x6860

USB_MODEM_CONFIGURATION = 0x2

def setUSBConfig(dev: usb.core.Device, config: int) -> bool:
    try:
        dev.reset()
        dev.set_configuration(config)
    except:
        return False
    return True


def samsungGalaxyToModemMode() -> bool:
    # Found on https://github.com/apeppels/galaxy-at-tool
    # We may need to run it twice...
    dev = usb.core.find(idVendor=SAMSUNG_GALAXY_ID_VENDOR, idProduct=SAMSUNG_GALAXY_ID_PRODUCT)
    if dev is None:
        print("No samsung device detected over USB")
        return False

    if dev is not None:
        print(f"Samsung device {dev.product} from {dev.manufacturer} detected with {dev.bNumConfigurations} available USB configurations")
        actualConfig = dev.get_active_configuration().bConfigurationValue
        print(f"Device is actually in USB configuration {actualConfig}")
        if actualConfig == USB_MODEM_CONFIGURATION:
            print(f"Device is already in modem mode (USB configuration {USB_MODEM_CONFIGURATION}), skipping USB switching")
            return True
        
        is_ok = setUSBConfig(dev, USB_MODEM_CONFIGURATION)
        if not is_ok:
            # We simply retry...
            print("Did not work the first time, retrying once")
            is_ok = setUSBConfig(dev, USB_MODEM_CONFIGURATION)

        if is_ok:
            print("USB Configuration sucessfully switched to modem mode")
        else:
            print(f"Unable to set USB configuration {USB_MODEM_CONFIGURATION}, it can happen if USB Debugging is already enabled")
        return is_ok
        
if __name__ == "__main__":
    samsungGalaxyToModemMode()