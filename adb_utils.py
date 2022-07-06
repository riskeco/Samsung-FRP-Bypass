import subprocess
import time

def adb(cmd: str):
    return subprocess.call(f"adb {cmd}",shell=True)

def uploadAndRunFRPBypass():
    print("Pushing FRP bypasser binary")
    adb("push frp.bin /data/local/tmp/temp")
    print("Giving it 777 permissions")
    adb("shell chmod 777 /data/local/tmp/temp")
    print("Executing the binary")
    adb("shell /data/local/tmp/temp")

def manualFRPBypass():
    # Equivalent to uploading the frp.bin and executing it if the property ro.secure is set to 1
    print("Bypassing FRP...")
    cmds = []
    cmds.append("settings put global setup_wizard_has_run 1")
    cmds.append("settings put secure user_setup_complete 1")
    cmds.append("content insert --uri content://settings/secure --bind name:s:DEVICE_PROVISIONED --bind value:i:1")
    cmds.append("content insert --uri content://settings/secure --bind name:s:user_setup_complete --bind value:i:1")
    # The command with INSTALL_NON_MARKET_APPS seems not needed
    cmds.append("content insert --uri content://settings/secure --bind name:s:INSTALL_NON_MARKET_APPS --bind value:i:1")
    cmds.append("am start -c android.intent.category.HOME -a android.intent.action.MAIN")
    for cmd in cmds:
        adb(f"shell {cmd}")
    time.sleep(5)
    cmd = "am start -n com.android.settings/com.android.settings.Settings"
    adb(f"shell {cmd}")
    time.sleep(5)
    print("OK")
    print("For complete reset FRP, goto \'Backup and reset\' and make \'Factory data reset\'")
    print("Rebooting...")
    adb("shell reboot")
    print("OK")

def waitForDevice():
    print("Waiting for device with adb")
    adb("kill-server")
    adb("wait-for-device")

if __name__ == "__main__":
    waitForDevice()
    uploadAndRunFRPBypass() # Or manualFRPBypass()
    