import glitchutils as gu

cmdstr0='taskset 1 /data/local/tmp/pres.sh'
cmdstr1='taskset 1 /system/bin/insmod /data/local/tmp/glitchmin.ko PARAM_iter=6 PARAM_volt=1055000 PARAM_gdelay=5 PARAM_delaypre=8000 PARAM_gval=0xd0'


print '[+] PRESETTINGS: running /data/local/tmp/pres.sh'
out_pres=gu.adb_exec_cmd_one(gu.device_id, cmdstr0, adb_proc='adb')
print out_pres
ret,out=gu.adb_exec_cmd_one(gu.device_id, cmdstr1, adb_proc='adb')
print ret

