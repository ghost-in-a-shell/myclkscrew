import os
import time
import commands
import threading
import subprocess
import sys

def regulate_temperature(min_temp, max_temp, sleep_time=5):
	""" @TODO: To implement
	    - need to compile ubench for new phone
	"""
	curr_temp = get_temperature()

	# Kill all remnants of the tool first
	adb_exec_cmd_one("ZX1G42BS93", 'pkill -9 -f /data/local/tmp/dofever-v7a')
	time.sleep(1)

	# Temperature too low
	if curr_temp < min_temp:
	    while curr_temp < min_temp:
		t = ThreadAdbCmd('adb', "ZX1G42BS93", '/data/local/tmp/dofever-v7a', timeout=sleep_time)
		t.run(is_quiet=True)
		curr_temp = get_temperature()
		print '[-]       Ramping up temperature: curr_temp=%d' % curr_temp
		if curr_temp == 0:
		    return False


	# Temperature too high
	elif curr_temp > max_temp:
	    while curr_temp > max_temp - (max_temp - min_temp)/2:
		time.sleep(sleep_time)
		curr_temp = get_temperature()
		print '[-]       Cooling down temperature: curr_temp=%d' % curr_temp

	# Just in case
	adb_exec_cmd_one("ZX1G42BS93", 'pkill -9 -f /data/local/tmp/dofever-v7a')
	print '[-]   Temperature in required range. Continuing.'

	return True

class ThreadAdbCmd(object):
    """ Encapsulate an ADB command so that we can trap the timeout.
    """
    def __init__(self, pname, device_id, adbcmd, timeout=10):
        self.pname = pname
        self.device_id = device_id
        self.timeout = timeout
        self.adbcmd = adbcmd
        self.is_timeout = False
        self.output = ''

    def run(self, is_quiet=False):
        def target():
           _, self.output = adb_exec_cmd_one(self.device_id, self.adbcmd, self.pname)
        
        self.thrd = threading.Thread(target=target)
        self.thrd.start()
        self.thrd.join(self.timeout)
        if self.thrd.is_alive():
            adb_exec_cmd_one("ZX1G42BS93", 'pkill -9 -f /data/local/tmp/dofever-v7a')
            self.is_timeout = True
            if not is_quiet:
                print '[+] ERROR: adb cmd has timed out! Force-killing adb'
                print '[-]      (%s)' % self.adbcmd

def adb_exec_cmd_one(device_id, cmd_str, adb_proc='adb'):
    if 'echo' in cmd_str:
        full_cmd = '%s -s %s shell su -c \"%s\"' % (adb_proc, device_id, cmd_str)
        return 0, os_exec_commands(full_cmd)

    n_tries = 0
    while n_tries < 10:
        ret, s_out, s_err = \
            os_exec_subprocess([adb_proc, '-s', device_id, 'shell', 'su', \
                                '-c', '\"%s\"' % cmd_str])
        
        output = s_err if not s_out else s_out
        if not 'error: device not found' in output and \
           not 'daemon not running' in output and \
           not 'error: protocol fault (no status)' in output:
            break
        n_tries += 1
        time.sleep(5)

        if n_tries == 10:
            print '[-] ***adb_exec_cmd_one: <%s> <%s> <%s>' % (output, s_out, s_err)
            print ' '.join([adb_proc, '-s', device_id, 'shell', 'su', \
                            '-c', '\"%s\"' % cmd_str])

    if n_tries == 10:
        print '[-]   adb_exec_cmd_one: phone likely offline. Exiting.'
        exit()
    return ret, output.strip()

def os_exec_subprocess(c_lst):
    p = subprocess.Popen(c_lst, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.wait(), p.stdout.read(), p.stderr.read()


def os_exec_commands(cmd_str):
    """ subprocess.Popen cannot execute commands like "echo 1 > ...". As a
        workaround, we use the commands.getstatusoutput API.

        The limitation is this technique cannot return the success status of
        the adb shell command within the device.
    """
    n_tries = 0
    while n_tries < 10:
        status, output = commands.getstatusoutput(cmd_str)
        if not status:
            return output
        if not 'error: device not found' in output and \
           not 'error: protocol fault (no status)' in output:
            break
        n_tries += 1
        time.sleep(5)

        if n_tries == 10:
            print '[-] ****os_exec_commands:', status, output
            print cmd_str
            print '[-]   os_exec_commands: phone likely offline. Exiting.'
            exit()

    print '[-]   os_exec_commands: FAILED: status: %d (%s)' % (status, output)
    print '[-]       (%s)' % cmd_str

def get_temperature():
        #temp = run_adb_and_get_output('cat /sys/devices/virtual/thermal/thermal_zone0/temp')
	_,temp = adb_exec_cmd_one("ZX1G42BS93", 'cat /sys/devices/virtual/thermal/thermal_zone0/temp', 'adb')
	#print temp
	if not temp:
		temp=0
	else:
		temp=int(temp)
	
        return temp

def run_adb_and_get_output(cmdstr, is_output_string=False):
        t = ThreadAdbCmd('adb', "ZX1G42BS93", cmdstr)
        t.run()
        output = t.output
        if not is_output_string:
            if not output or not output.isdigit():
                return 0
            return int(output)
        return output

def force_kill_os(pname):
    _, cnt, _ = os_exec_subprocess(['pkill', '-c', '-9', '-f', pname])
    cnt = cnt.rstrip()
    if cnt and cnt.isdigit():
        if int(cnt) == 0:
            print '[-]   force_kill_os: FAILED: Did not kill process <%s>' % pname
        elif int(cnt) > 1:
            print '[-]   force_kill_os: FAILED: Kill more than 1 instance of <%s>: %d' % (pname, int(cnt))
    else:
        print '[-]   force_kill_os: ERROR: Unexpected output:', cnt


mintemp=34000
mintemp=int(sys.argv[1])
maxtemp=mintemp+1000
if regulate_temperature(mintemp, maxtemp, sleep_time=5):
	os.system("adb shell su -c \"cat /sys/devices/virtual/thermal/thermal_zone0/temp\"")
	print "prefectly done!"
else:
	os.system("adb shell su -c \"cat /sys/devices/virtual/thermal/thermal_zone0/temp\"")
	print "errrrrrrrrrrrrrrrrror"
time.sleep(5)
os._exit(0)
print "impossible"

