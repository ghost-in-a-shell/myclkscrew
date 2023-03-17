ccflags-y += -fno-stack-protector -fno-pic -Wno-unused-function
obj-m += glitchmin.o
glitchmin-objs := main.o glitch_sd805.o

CROSS_COMPILE=/home/wyx/ndk/arm-eabi-4.8/bin/arm-eabi-
KERNEL_DIR=/home/wyx/images_kernel/msm-android-msm-shamu-3.10-marshmallow

all:
	make -C ${KERNEL_DIR} M=$(PWD) ARCH=arm PLATFORM=shamu CROSS_COMPILE=${CROSS_COMPILE} modules

clean:
	make -C ${KERNEL_DIR} M=$(PWD) clean
