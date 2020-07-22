import serial
import sys
import time

def expect_response(expect, timeout=10):
	start_time = time.time()
	received = ser.read(ser.inWaiting()).decode('ascii')
	while expect not in received:
		time.sleep(0.01)
		received += ser.read(ser.inWaiting()).decode('ascii')
		if time.time() - start_time > timeout:
			raise Exception("Timeout waiting for response: " + expect)

def check_at(timeout=5):
	ser.write("AAAAT\r")
	ser.write("AAAAT\r")
	expect_response("OK", timeout=timeout)

def initialize():
	check_at()
	ser.write("ATQ0E0V1S0=0\r")
	expect_response("OK")
	ser.write("AT&&F\r")
	expect_response("OK")
	ser.write("AT&&FFL\r")
	expect_response("ERROR")

def send_ocmfldr(ocmfldr_data):
	lines = ocmfldr_data.split("\n")
	total_lines = len(lines)
	for idx, line in enumerate(lines):
		if len(line) == 0:
			continue
		assert line.startswith(":")

		if idx % 100 == 0:
			print "Sending {} / {}".format(idx, total_lines)
		ser.write("at&&f" + line + "\r\r")
		expect_response("OK")

def send_fw(fw_data):
	ser.write("at&&f\r")
	lines = fw_data.split("\n")
	total_lines = len(lines)
	for idx, line in enumerate(lines):
		if len(line) == 0:
			continue
		assert line.startswith("S")

		if idx % 100 == 0:
			print "Sending {} / {}".format(idx, total_lines)
		ser.write(line + "\r")
		expect_response("OK")
		ser.write("\r")

def apply_fw():
	ser.write("\x1A\r")
	ser.write("\r")
	while True:
		try:
			check_at(timeout=1)
		except Exception:
			continue
		break
	ser.write("AT~S?\r")
	expect_response("OK")
	ser.write("AT&F1S0=1&W0&F2S0=1&W1Y0Z\r")
	expect_response("OK")


if __name__ == '__main__':
	if len(sys.argv) < 3:
		print "Usage: fw_update.py serial_port firmware_file"
		sys.exit(1)

	serial_port = sys.argv[1]
	firmware_file = sys.argv[2]

	ser = serial.Serial(serial_port, 115200)

	print "Opened serial connection on {}, initializing...".format(serial_port)
	initialize()

	print "Initialization complete, reading ocmfldr.hex..."
	with open("ocmfldr.hex") as fh:
		ocmfldr_data = fh.read()

	print "Sending ocmfldr.hex..."
	send_ocmfldr(ocmfldr_data)

	print "Done sending ocmfldr.hex, reading {}...".format(firmware_file)
	with open(firmware_file) as fh:
		fw_data = fh.read()

	print "Sending {}...".format(firmware_file)
	send_fw(fw_data)

	print "Done sending {}, wrapping up...".format(firmware_file)
	apply_fw()

	print "Applied firmware"
