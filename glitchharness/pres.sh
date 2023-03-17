#!/system/bin/sh
stop thermal-engine
stop mpdecision
echo 1 > /sys/devices/system/cpu/cpu1/online
echo 1 > /sys/devices/system/cpu/cpu2/online
echo 0 > /sys/devices/system/cpu/cpu3/online
echo userspace > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
echo userspace > /sys/devices/system/cpu/cpu1/cpufreq/scaling_governor
echo userspace > /sys/devices/system/cpu/cpu2/cpufreq/scaling_governor
echo 2649600 > /sys/devices/system/cpu/cpu0/cpufreq/scaling_setspeed
echo 2649600 > /sys/devices/system/cpu/cpu1/cpufreq/scaling_setspeed
echo 2649600 > /sys/devices/system/cpu/cpu2/cpufreq/scaling_setspeed
echo 0 > /proc/sys/kernel/randomize_va_space
cat /sys/devices/virtual/thermal/thermal_zone0/temp    
