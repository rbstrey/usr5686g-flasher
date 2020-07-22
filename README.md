USR5686G Flasher
================

This repository contains tools for flashing a USR5686G modem with modified firmware.

Firmware is available from the manufacturer at [https://support.usr.com/support/product-template.asp?prod=5686g](https://support.usr.com/support/product-template.asp?prod=5686g)

Firmware Package Details
------------------------

The firmware package from the manufacturer contains two files:

* ocmfldr.hex - A smaller file, in [Intel hex](https://en.wikipedia.org/wiki/Intel_HEX) format
* svn545.hex - The main firmware, in [Motorola SREC](https://en.wikipedia.org/wiki/SREC_(file_format)) format

Both Ghidra and IDA should be able to directly import these files. Processor should be set to ARM.

Tools
-----

*fix_checksums.py* works with the svn545.hex file to update checksums after modifications are made to the data it contains. If checksums are not correct, the modem will reject the modified update at some point during the update process.

*fw_update.py* sends ocmfldr.hex and a specified file (normally svn545.hex) to the modem on a specified serial port.

Normal Modification + Update Process
------------------------------------

After examining the firmware in IDA or Ghidra, the svn545.hex update file can be directly edited. Then, checksums can be fixed up with fix_checksums.py, and the firmware update sent over serial to the device via fw_update.py.

It's important to be *very cautious* when creating and sending an update to the device. There is no easy recovery if an update is sent that breaks the serial console interface on the modem, so ensure all changes you make are triggered by a specific AT command (such as ATI) or that it can't trigger a crash.
