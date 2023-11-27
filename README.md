# Automated-python-scripts-sending-mail

Using crontab to run the scripts automatically.

commands :

    --> $crontab -e
    Select the text editor and then,
    -->$00 * * * * user/bin/python3 /home/user/report/every1hour_empty_note_list.py
    -->$* * * * * user/bin/python3 /home/user/report/open_ticket_details_monitoring.py
