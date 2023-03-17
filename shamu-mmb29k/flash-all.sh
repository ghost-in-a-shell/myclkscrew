#!/bin/sh

# Copyright 2012 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

fastboot flash bootloader bootloader-shamu-moto-apq8084-71.15.img
fastboot reboot-bootloader
sleep 5
fastboot flash radio radio-shamu-d4.01-9625-05.32+fsg-9625-02.109.img
fastboot reboot-bootloader
sleep 5
fastboot -w update image-shamu-mmb29k.zip
