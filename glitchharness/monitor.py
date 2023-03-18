import glitchutils as gu
import subprocess
import time

gu.write_log(gu.log_filename,'\n\n\n\n\n\n\n\n')
cmdstr2='taskset 1 /system/bin/cat /proc/kmsg | grep glitchmin'
print '[+] KPROC: Monitoring /proc/kmsg for glitches'
cmdstr2_full = ['adb', '-s', gu.device_id, 'shell', 'su', '-c', '\"%s\"' % cmdstr2]
while True:
	kproc = subprocess.Popen(cmdstr2_full,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	while True:
		nextline = kproc.stdout.readline()
		if nextline == '':
			while True:
				ret, s_out, s_err = gu.os_exec_subprocess(['adb', 'devices'])
				#print s_out
				if len(s_out)==26:
					#wait
					print '		[-] WAITING: waiting for the device to reboot'
					time.sleep(10)
				elif 'unauthorized' in s_out:
					print '		[-] WAITING: waiting for the device to reboot'
					time.sleep(10)
				elif 'offline' 	in s_out:
					print '		[-] WAITING: waiting for the device to reboot'
					time.sleep(10)		
				else:
					print '		[-] ALIVE: device is ready!!!'
					break
			break
		gu.write_log(gu.log_filename,nextline.strip()+'\n')
		print nextline.strip()

