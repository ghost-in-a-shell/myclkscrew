import glitchutils as gu
import time
import os
todolist=[['0xd8', '5', '7600', 40000], ['0xd8', '5', '7800', 40000], ['0xd8', '5', '8000', 40000], ['0xd8', '5', '8200', 40000], ['0xd8', '5', '8400', 40000], ['0xd8', '5', '8600', 40000], ['0xd8', '5', '8800', 40000], ['0xe0', '5', '7600', 40000], ['0xe0', '5', '7800', 40000], ['0xe0', '5', '8000', 40000], ['0xe0', '5', '8200', 40000], ['0xe0', '5', '8400', 40000], ['0xe0', '5', '8600', 40000], ['0xe0', '5', '8800', 40000]]




for group in todolist:
	gu.write_log(gu.log_filename,'paras  '+str(group)+'\n')
	for i in range(20):
		gu.fault_handler()	
		print '\n[+] REBOOT: rebooting'
		os.system('adb reboot')
		time.sleep(40)
		gu.fault_handler()
		print '\n[+] HEAT: running /temperctrl.py'
		os.system('python /home/wyx/glitchharness/temperctrl.py %d' % group[3])

		cmdstr1='taskset 1 /system/bin/insmod /data/local/tmp/glitchmin.ko PARAM_iter=15 PARAM_volt=1055000 PARAM_gdelay=%s PARAM_delaypre=%s PARAM_gval=%s' %(group[1],group[2],group[0])
		print '\n[+] GLITCHING: do the glitch!!!'


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
	



