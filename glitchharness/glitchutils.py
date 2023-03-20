import os
import commands
import subprocess
import threading
import time

#const
device_id='ZX1G42BS93'
log_filename='exp_log_multipara1'


#functions
def os_exec_subprocess(c_lst):
    p = subprocess.Popen(c_lst, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.wait(), p.stdout.read(), p.stderr.read()


def adb_exec_cmd_one(device_id, cmd_str, adb_proc='adb'):

    n_tries = 0
    while n_tries < 1:
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

def write_log(filename,content):
	def write_one(filename,content):
		with open(filename,'a+') as log:
			log.write(content)
	thread1 = threading.Thread(target=write_one, args=[filename,content])
	thread1.start()

def presets(quiet=True):
	cmdstr0='taskset 1 /data/local/tmp/pres.sh'
	if  not quiet:
		print '[+] SETTINGADBD: binding to core 1'
	_,out_adbd=adb_exec_cmd_one(device_id, 'pgrep adbd', adb_proc='adb')
	out_adbd_bind=adb_exec_cmd_one(device_id, 'taskset -ap 1 %s' % out_adbd, adb_proc='adb')
	if  not quiet:
		print out_adbd_bind
	if  not quiet:
		print '\n[+] PRESETTINGS: running /data/local/tmp/pres.sh'
	out_pres=adb_exec_cmd_one(device_id, cmdstr0, adb_proc='adb')
	if  not quiet:
		print out_pres
	time.sleep(0.5)

def fault_handler():
	print '[+] FAULT_HANDLER: checking device status'
	rebootflag=False
	while True:
		ret, s_out, s_err = os_exec_subprocess(['adb', 'devices'])
		#print s_out
		if len(s_out)==26:
			#wait
			print '		[-] WAITING: waiting for the device to reboot'
			time.sleep(10)
			rebootflag=True
		elif 'unauthorized' in s_out:
			print '		[-] WAITING: waiting for the device to reboot'
			time.sleep(10)
			rebootflag=True
		elif 'offline' 	in s_out:
			print '		[-] OFFLINE: reconnecting device'
			os.system('sudo chmod 777 /sys/bus/usb/drivers/usb/unbind')
			os.system('sudo echo \'1-12.4\' > /sys/bus/usb/drivers/usb/unbind')
			time.sleep(1)
			os.system('sudo chmod 777 /sys/bus/usb/drivers/usb/bind')
			os.system('sudo echo \'1-12.4\' > /sys/bus/usb/drivers/usb/bind')
			time.sleep(1)	
			rebootflag=True
			write_log(log_filename,'reboot\n\n\nreboot\n\n\n')		
		else:
			print '		[-] ALIVE: device is ready!!!'
			presets()
			if rebootflag:
				print '		[-] be kind to new device!'
				rebootflag=False
				time.sleep(15)
				fault_handler()
			break
