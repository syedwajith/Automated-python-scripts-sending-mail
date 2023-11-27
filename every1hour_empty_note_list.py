import mysql.connector

import datetime

from datetime import timedelta

import smtplib

from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText


def empty_note_list():
    
    today_date_time = datetime.datetime.now()
    
    from_date_time = today_date_time - timedelta(hours = 1)

    from_date_time = from_date_time.strftime('%Y-%m-%d %H:%M:%S %p')
    
    to_date_time = today_date_time.strftime('%Y-%m-%d %H:%M:%S %p')
    
    
    
    mydb = mysql.connector.connect(
    
    host="otrs.futurenet.in",
    
    user="readuser2",
    
    passwd="6FbUDa5VM",
    
    database="otrs5",
    
    charset="utf8"
    
    )
    
    
    
    mycursor = mydb.cursor()
    
    
    
    query = """
    SELECT 
    	 ticket.tn AS TICKET_ID,
    	 ticket.title AS SUBJECT,
    	 users.login AS USER_NAME,
    	 ticket_state.name AS TICKET_STATUS,
 	     queue.name AS QUEUE_NAME,
    	 article.create_time AS CREATE_TIME,
    	 article.change_time AS CHANGE_TIME
    
    FROM 
    ticket
JOIN queue ON ticket.queue_id = queue.id
JOIN article ON ticket.id = article.ticket_id
JOIN users ON article.change_by = users.id
JOIN article_sender_type ON article.article_sender_type_id = article_sender_type.id
JOIN ticket_state ON ticket.ticket_state_id = ticket_state.id
JOIN article_attachment ON article.id = article_attachment.article_id
WHERE 
    queue.name IN ('MONITORING')
    AND article_sender_type.name IN ('agent')
    AND article.create_time = (
        SELECT 
		MAX(a1.create_time)
        FROM 
		article a1
        WHERE 
		a1.ticket_id = ticket.id
    )
    AND article.a_body IN ('')
    AND article_attachment.id = (
    		SELECT 
			id
    		FROM 
			article_attachment aa
    		WHERE 
			aa.article_id = article.id LIMIT 1
    		)
    AND article_attachment.content NOT IN (
	 		SELECT 
			 	aa1.content 
			FROM 	
				article_attachment aa1 
			WHERE 
				aa1.article_id = article.id 
				AND aa1.content LIKE '%<img alt=%'
			)
    AND article.create_time BETWEEN DATE_SUB(NOW(), INTERVAL 1 HOUR) AND NOW()
ORDER BY TICKET_ID DESC;
    """
    
    
    mycursor.execute(query)
    myresult = mycursor.fetchall()
    
    
    #print(myresult)
    
    
    s_no = 0
    
    table_data=[]
    
    
    
    for data in myresult:
    
        s_no += 1
    
        table_row = """
    
        <tr>
    
        <td style="padding: 10px; text-align: center;">"""+ str(s_no) +"""</td>
    
        <td style="padding: 10px; text-align: center;">"""+ str(data[0])+"""</td>
    
        <td style="padding: 10px; text-align: left;">"""+ str(data[1])+"""</td>
    
        <td style="padding: 10px; text-align: center;">"""+ str(data[2])+"""</td>
    
        <td style="padding: 10px; text-align: center;">"""+ str(data[3])+"""</td>
    
        <td style="padding: 10px; text-align: center;">"""+ str(data[4])+"""</td>

	    <td style="padding: 10px; text-align: center;">"""+ str(data[5])+"""</td>

	    <td style="padding: 10px; text-align: center;">"""+ str(data[6])+"""</td>

        </tr>
        """
    
    
        table_data.append(table_row)
    
        
    
    if len(table_data) == 0 :
    
        table = "Empty Notes are not available."
    
    else:
    
        table = """
        <table style="margin-left: auto; margin-right: auto;" border="1">
    
        <tr>
    
        <th style="text-align:center;">S.No</th>

        <th style="text-align:center;">TICKET_ID</th>
    
        <th style="text-align:center;">SUBJECT</th>
    
        <th style="text-align:center;">USER_NAME</th>

        <th style="textalign:center;">TICKET_STATUS</th>
    
        <th style="text-align:center;">QUEUE_NAME</th> 

        <th style="text-align:center;">CREATE_TIME</th>

        <th style="text-align:center;">CHANGE_TIME</th>
                  
        </tr>
    
        """+''.join(table_data)+"""
        </table>
        """
    
    
    
    html_content = """\
    
    	<!DOCTYPE html>
    	
    <html>
    	
    <head>
    	
    <style>
    	
    table, th, td {
      
    		border: 1px solid black;
      
    		border-collapse: collapse;
    
    	}
    
    	tr:nth-child(even) {
    		background-color: #f2f2f2;
    	}
    
    	</style>
    
    	</head>
    
    
    	<body>
    	
    <p>Dear sir,</p>
    
    	<b><p>List of empty Note list ticket details</p></b>
    
    	""" + ''.join(table) + """
    	
    
    </br>
    
    	</br>
    
    	<p>This is a auto-generated mail.</p>
    
    	</body>
    
    	</html>
    	
    """
    
    
    #print(html_content) 
    
    
    subject  = "Empty Note List Ticket Details between "+ str(from_date_time) + " and " + str(to_date_time) 
    
    msg = MIMEMultipart('alternative')
    
    to = 'rims.l1@futurenet.in'
    
    cc = 'rims.tl@futurenet.in,rims@futurenet.in'
    
    msg['Subject'] = subject 
    
    msg['to'] = to
    
    msg['cc'] = cc
    
    rcpt = cc.split(",") + to.split(",")
    
    part1 = MIMEText(html_content, 'html','utf-8')
    
    msg.attach(part1)
    
    smtp_server = smtplib.SMTP('webmail.futurenet.in',25)
    
    smtp_server.starttls()
    
    smtp_server.login('otrs.report@futurenet.in','JwD@!3j@4HQB!@')
    
    smtp_server.sendmail('otrs.report@futurenet.in',rcpt,msg.as_string())
    
    smtp_server.quit()
    
if __name__ == "__main__":
    empty_note_list()