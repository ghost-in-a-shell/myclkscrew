import glitchutils as gu
import time
import os

cmdstr0='taskset 1 /data/local/tmp/pres.sh'
cmdstr1='taskset 1 /system/bin/insmod /data/local/tmp/glitchmin.ko PARAM_iter=6 PARAM_volt=1055000 PARAM_gdelay=5 PARAM_delaypre=8000 PARAM_gval=0xd0'

print '[+] SETTINGADBD: binding to core 1'
_,out_adbd=gu.adb_exec_cmd_one(gu.device_id, 'pgrep adbd', adb_proc='adb')
out_adbd_bind=gu.adb_exec_cmd_one(gu.device_id, 'taskset -ap 1 %s' % out_adbd, adb_proc='adb')
print out_adbd_bind

print '\n[+] PRESETTINGS: running /data/local/tmp/pres.sh'
out_pres=gu.adb_exec_cmd_one(gu.device_id, cmdstr0, adb_proc='adb')
print out_pres
time.sleep(0.5)

print '\n[+] HEAT: running /temperctrl.py'
os.system('python /home/wyx/glitchharness/temperctrl.py 39000')


print '\n[+] GLITCHING: do the glitch!!!'
while True:
	_,out_temp=gu.adb_exec_cmd_one(gu.device_id, 'cat /sys/devices/virtual/thermal/thermal_zone0/temp', adb_proc='adb')
	if out_temp is None:
		time.sleep(60)
		os.system('adb kill-server')
		time.sleep(0.5)
		os.system('adb start-server')
		continue
	print out_temp
	if int(out_temp)<30000:
		break
	gu.write_log(gu.log_filename,'temp'+str(out_temp)+'\n')
	time.sleep(0.5)
	ret,out=gu.adb_exec_cmd_one(gu.device_id, cmdstr1, adb_proc='adb')
	time.sleep(0.5)
	print out 



