#! /usr/bin/env python2
import  numpy, socket, struct
import argparse
import sys
# Provide the SdrWrap interface, but speak to the rtl_tcp server
# instead of using the rtlsdr module.
# Issues:
#  * It seems the select() on the TCP socket in rtl_tcp only
#    happens at 1Hz, so rapid tuning required for gnuwaterfall
#    probably doesn't work by default.
#  * Gain adjustment is probably wrong

# Current command codes for rtl_tcp
SET_FREQUENCY = 0x01
SET_SAMPLERATE = 0x02
SET_GAINMODE = 0x03
SET_GAIN = 0x04
SET_FREQENCYCORRECTION = 0x05
SET_HIGHPASSFILTER = 0x0e
SET_LOWPASSFILTER = 0x0f

class RtlTCP(object):
    def __init__(self):
        # TODO: pass remote endpoint to constructor
        self.remote_host = "localhost"
        self.remote_port = 1234
        self.prev_fc = None
        self.prev_fs = None
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.remote_host, self.remote_port))
        self.prev_g = 10 # Sane default?
    def filter(self, lpf, hpf): # Taken from SdrWrap class
            self.__send_command(SET_LOWPASSFILTER, lpf)
            self.__send_command(SET_HIGHPASSFILTER, hpf)
        # TODO: should we be calling configure_highlight() here, or can we move
        # that out of this class?
    def __send_command(self, command, parameter):
        # rtl_tcp command format is little-endian:
        #   command code (uint8),
        #   parameter (uint32)
        cmd = struct.pack("<BI", command, parameter)
        self.conn.send(cmd)


if __name__=="__main__":
    # For testing...
#    sdr.tune(64e6,2e6,0)
 #   sdr.read_samples(1)
	parser = argparse.ArgumentParser(description='Filter IF')
	slicegroup = parser.add_argument_group('filtering',
    'Command rtl_Tcp to filter data  output by the IF.')
	slicegroup.add_argument('--low', dest='lowpass', default=None,
    help='Lowpass filter frequency.')
	slicegroup.add_argument('--high', dest='highpass', default=None,
    help='Highpass filter frequency.')

for i, arg in enumerate(sys.argv):
    if (arg[0] == '-') and arg[1].isdigit():
        sys.argv[i] = ' ' + arg
args = parser.parse_args()
#print args.include_freq
#From keenard's code
def freq_parse(s):
    suffix = 1
    if s.lower().endswith('k'):
        suffix = 1e3
    if s.lower().endswith('m'):
        suffix = 1e6
    if s.lower().endswith('g'):
        suffix = 1e9
    if suffix != 1:
        s = s[:-1]
    return float(s) * suffix




if (args.lowpass == 'None'):
        print "Must enter lowpass frequency!"
if (args.highpass == 'None'):
        print "Must enter highpass frequency!"


#slicegroup.add_argument('--res', dest='res_factor', default=None,
#    help='Resolution factor. Greater than 1 results in n-range scan')
#slicegroup.add_argument('--samples', dest='samples', default=None,
#    help='Number of samples')
#slicegroup.add_argument('--stepsize', dest='stepsize', default=None,
#    help='Duration to use, stopping at the end.')
sdr = RtlTCP()

print str(int(freq_parse(args.lowpass)))
print str(int(freq_parse(args.highpass)))

sdr.filter(int(freq_parse(args.lowpass)), int(freq_parse(args.highpass)))

