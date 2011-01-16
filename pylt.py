#/usr/local/bin/python
#
# This is the PYLT baseclas which defines the fall-back methods
#

import sys
import time

class PyltError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		 return repr(self.value)

class pylt(object):

	def __init__(self):
		# Instrument identification, eg: "HP6626A"
		self.id = "undefined"
		self.spoll_cmd = 0x00
		self.spoll_data = 0x00
		if not hasattr(self, 'debug_fd'):
			self.debug_fd = sys.stderr

	# Raise a Pylt specific exception
	def fail(self, s):
		raise PyltError("(" + self.id + ") " + s)

	# Dump debug output
	def debug(self, s):
		self.debug_fd.write(self.id + ".DEBUG: " + s + "\n")
		self.debug_fd.flush()

	# Report any errors to f
	# Return True if there are any
	def errors(self, f=sys.stderr):
		sys.stderr.write(
		    "PYLT.WARN: [%s].errors() undefined\n" % self.id)
		return False

	# Read a response
	def rd(self):
		sys.stderr.write("PYLT.WARN: [%s].rd() undefined\n" % self.id)
		return None

	# Send a command
	def wr(self):
		sys.stderr.write("PYLT.WARN: [%s].wr() undefined\n" % self.id)

	# Ask a question
	# return None on timeout
	def ask(self, q, tmo = None):
		self.wr(q)
		if tmo != None and not self.wait_cmd(tmo, False):
			return None
		return self.rd()

	# Assert no errors
	def AOK(self):
		if self.errors():
			self.fail('Instrument reported errors')

	# Give a brief report of instrument state
	def report(self, f=sys.stdout):
		sys.stderr.write(
		    "PYLT.WARN: [%s].report() undefined\n" % self.id)

	# Reset instrument to known state
	def reset(self):
		sys.stderr.write(
		    "PYLT.WARN: [%s].reset() undefined\n" % self.id)

	# Wait until instrument is ready.
	# if fail is set, fail when timeout expires, else return False
	def wait_cmd(self, tmo = 10., fail = True):
		sys.stderr.write(
		    "PYLT.WARN: [%s].wait_cmd() undefined\n" % self.id)
		return True

	# Wait until instrument is ready, return false if not
	# if fail is set, fail when timeout expires, else return False
	def xwait_data(self, tmo = 10., fail = True):
		sys.stderr.write(
		    "PYLT.WARN: [%s].wait_data() undefined\n" % self.id)
		return True
	
	# Trigger intrument into action
	def trigg(self):
		sys.stderr.write(
		    "PYLT.WARN: [%s].trig() undefined\n" % self.id)

	def spoll(self):
		sys.stderr.write(
		    "PYLT.WARN: [%s].spoll() undefined\n" % self.id)
		return 0

	def wait_spoll(self, bits, dur = 10000.):
		print("WAITING FOR %02x" % bits)
		assert bits > 0 or "wait_spoll bits" == "must > 0"
		assert bits < 256 or "wait_spoll bits" == "must be < 256"
		obits = 256
		te = time.time() + dur
		x = 0
		dt = 0.001
		while time.time() < te:
			x = self.spoll()
			if x != obits:
				print("SPOLL CHG %02x -> %02x" % (obits, x))
				obits = x
			if x & bits:
				return True
			time.sleep(dt)
			if dt < 3:
				dt += dt
		return False

	def wait_cmd(self, dur = 10., fail=True):
		if self.wait_spoll(self.spoll_cmd, dur):
			return True
		if not fail:
			return False
		self.fail("Timeout waiting for cmd")

	def wait_data(self, dur = 10., fail=True):
		if self.wait_spoll(self.spoll_data, dur):
			return True
		if not fail:
			return False
		self.fail("Timeout waiting for data")