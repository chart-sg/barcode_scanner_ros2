# Barcode Scanner ROS2 
ROS2 adapter for a basic driverless USB barcode scanner. For this repo, the hardware used is the Datalogic Handheld Barcode Scanner.

## Background
The default behaviour for such devices is simply to emulate keyboard key strokes. The device reads the scanned barcode and decodes it into text which is then converted to key strokes. Your OS will receive the key strokes and converts it into text. 
** An important detail to note is that the key mapping is dependent on the keyboard language mapping settings, therefore the it is important to verify the key mapping parameter. 

## Parameter Verification

### Checking key mappinng
1. Identify the event_id that the USB barcode scanner parsers its data through. This can be done by listing all the input events and determining the new addition when the device is plugged in.
To list input devices:
```
ls /dev/input/
```

2.  Use the event device testing program on linux to check all the event code to key stroke mapping of the eventID determined earlier.
```
sudo evtest /dev/input/eventXX
```

3. With the information above, check or update the key_mapping parameter is the `barcode_scanner_script`. The key_mapping parameter is a string containing the various key strokes based on the event code number. 

Example:
If the key stroke `a` has an event code of `4`. The letter `a` will have to be the fifth character in the key_mapping string 


## Usage Instructions
1. Access to the port `/dev/input` must be given the user for the adapter to work.

`sudo chown <username> -R /dev/input` 

2. To run the adapter, run the following:
`ros2 run barcode_scanner_ros2 barcode_scanner_script`
