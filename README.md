# getIssueFromJIRA
get new issue from JIRA broad and send email for notification, with hard coded JQL 

In order to run it, you need Python with pip installed, and then install the dependencies if not installed yet

`pip install requests smtplib`

Please edit getissue(fake).yml with your own credentials and preferences, and reaname it to getissue.yml

Please use an external scheduling service to run it in interval

In windows, make a .bat file with content like below

`"C:/Users/your-name/AppData/Local/Programs/Python/Python37-32/python.exe" "c:/Users/your-name/Desktop/getissue.py"`

Open Task Scheduler and make it execute this .bat for a set time period

