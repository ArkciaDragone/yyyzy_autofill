# YYYZY_Autofill

This software basically *repeats* yesterday's submission. Written purely in Python, it supports automated login and on/off campus form submission. The latest version is only tested for "on campus" situation.

How to use:
 - Fill the form manually (to provide the software the data to repeat) and wait till tomorrow
 - Install the requirements: `pip install -r requirements.txt`
 - Run the file

Note that this software assumes there is no case of leaving school. For that purpose a manual submission is required, and the next day the software will not repeat the previous day's submission but, for convenience, submit a new one with no leaving info.

Multiple parameters can be supplied to control the behavior of the software. To see all the options available, run the file with `-h`. For example, it's a good idea to add the software to crontab with the `-y` option.

Student ID and password are stored locally in `private.json`. Please keep it safe.

*By using this software, you understand and agree that the author does not assume any responsibility for possible consequences. See the license for complete terms.*