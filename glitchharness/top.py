import os
import glitchutils as gu
ret, s_out, s_err = gu.os_exec_subprocess(['adb', 'devices'])
print s_out
if len(s_out)==26:
	#wait
	print 'gg'
elif 'unauthorized' in s_out:
	print 'wait'
elif 'offline' 	in s_out:
	print 'restart adb server'
else:
	print 'ok'
