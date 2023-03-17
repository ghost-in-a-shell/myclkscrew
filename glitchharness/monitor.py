import glitchutils as gu
import subprocess
import time

gu.write_log(gu.log_filename,'\n\n\n\n\n\n\n\n')
cmdstr2='taskset 1 /system/bin/cat /proc/kmsg | grep glitchmin'
print '[+] KPROC: Monitoring /proc/kmsg for glitches'
cmdstr2_full = ['adb', '-s', gu.device_id, 'shell', 'su', '-c', '\"%s\"' % cmdstr2]
kproc = subprocess.Popen(cmdstr2_full,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
while True:
	nextline = kproc.stdout.readline()
	gu.write_log(gu.log_filename,nextline.strip()+'\n')
	print nextline.strip()

