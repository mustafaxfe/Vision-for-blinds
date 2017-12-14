#!/bin/bash

export GOOGLE_APPLICATION_CREDENTIALS="/home/pi/scripts/vision\ for\ blinds-952cefcb99f2.json"

nmcli dev wifi list >> conn.txt

cd "/home/pi/scripts/"

sudo /etc/init.d/network-manager restart

sudo systemctl restart networking.service

systemctl daemon-reload

ps cax | grep pulseaudio > /dev/null

if (ping -c 1 google.com >> /dev/null 2>&1) && [ $? -eq 0 ]; then

	sudo su pi -c 'exec ./simple_google_tts tr  "Sistem hazır"'

	sleep 5
	
	sudo su pi -c "python system.py"

else

	while ! (ping -c 1 google.com >> /dev/null 2>&1) || ! [ $? -eq 0 ]; do

		if ! (ping -c 1 google.com >> /dev/null 2>&1); then

			nmcli dev wifi list >> conn.txt

			if grep -q "erciyes" conn.txt ; then

				nmcli device wifi con "erciyes" password "123erciyes"

			else

				sudo su pi -c 'espeak -v tr "Telefonunuzda erciyes isimli şifresi 123erciyes olacak hotspot ayarını yapınız."'

			fi

		fi

		ps cax | grep pulseaudio > /dev/null

		if ! [ $? -eq 0 ]; then

			sudo su pi -c "pulseaudio -D"

		elif (ping -c 1 google.com >> /dev/null 2>&1) && [ $? -eq 0 ]; then

			sudo su pi -c 'exec ./simple_google_tts tr "Sistem Hazır"'
	
			sleep 5

			sudo su pi -c "python system.py"

			break

		fi

		sleep 10

	done

fi

