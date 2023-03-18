import glitchutils as gu
import time
import os

while True:
	print '\n[+] HEAT: running /temperctrl.py'
	os.system('python /home/wyx/glitchharness/temperctrl.py 45000')

	cmdstr1='taskset 1 /system/bin/insmod /data/local/tmp/glitchmin.ko PARAM_iter=6 PARAM_volt=1055000 PARAM_gdelay=5 PARAM_delaypre=8000 PARAM_gval=0xd0'
	print '\n[+] GLITCHING: do the glitch!!!'
	while True:
		gu.fault_handler()
		time.sleep(0.2)
		_,out_temp=gu.adb_exec_cmd_one(gu.device_id, 'cat /sys/devices/virtual/thermal/thermal_zone0/temp', adb_proc='adb')
		if out_temp is None:
			continue
		print out_temp
		if int(out_temp)<30000:
			break
		gu.write_log(gu.log_filename,'temp'+str(out_temp)+'\n')
		time.sleep(0.5)
		ret,out=gu.adb_exec_cmd_one(gu.device_id, cmdstr1, adb_proc='adb')
		time.sleep(1)
		print out 



