import sys

def recalculate_checksum(line):
	did_update = False

	line = line.strip()
	if len(line) == 0:
		return "", did_update
	assert line.startswith('S')

	checksummable = line[2:-2]
	assert len(checksummable) % 2 == 0

	byte_values = [
		int("".join(i), 16)
		for i in zip(checksummable[::2], checksummable[1::2])
	]

	byte_sum = 0
	for byte in byte_values:
		byte_sum += byte

	# One's complement
	checksum = (byte_sum ^ 0xFF) & 0xFF
	checksum_str = '{:02X}'.format(checksum)

	if checksum_str != line[-2:]:
		print "Fixing checksum mismatch for line {}".format(line)
		line = line[:-2] + checksum_str
		did_update = True

	return line + "\r", did_update


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "Usage: fix_checksums.py firmware_file"
		sys.exit(1)

	firmware_file = sys.argv[1]

	print "Reading {}...".format(firmware_file)
	with open(firmware_file) as fh:
		firmware_data = fh.read()

	print "Checking {}...".format(firmware_file)
	lines = []
	did_update = False
	for line in firmware_data.split("\n"):
		result, line_did_update = recalculate_checksum(line)
		did_update |= line_did_update
		lines.append(result)

	if did_update:
		print "Updating {}...".format(firmware_file)
		with open(firmware_file, 'w') as fh:
			fh.write("\n".join(lines))
	else:
		print "Checksums correct."
