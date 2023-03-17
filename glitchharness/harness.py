import os
import commands
import subprocess
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


device_id='ZX1G42BS93'
cmdstr1='taskset 1 /system/bin/insmod /data/local/tmp/glitchmin.ko PARAM_iter=6 PARAM_volt=1055000 PARAM_gdelay=5 PARAM_delaypre=8000 PARAM_gval=0xd0'
ret,out=adb_exec_cmd_one(device_id, cmdstr1, adb_proc='adb')
print ret
print out
