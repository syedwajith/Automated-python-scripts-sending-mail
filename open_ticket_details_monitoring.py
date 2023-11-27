import mysql.connector
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def open_ticket_details():

    today_date_time = datetime.datetime.now().date()

    mydb = mysql.connector.connect(
        host = "otrs.futurenet.in",
        user = "readuser2",
        passwd = "6FbUDa5VM",
        database = "otrs5",
        charset = "utf8"
    )

    mycursor = mydb.cursor()

    query = """
        SELECT 
            #ticket.id AS ID,
            ticket.tn AS TICKET_ID,
            ticket.title AS SUBJECT,
            #article.a_body AS BODY_CONTENT,
            users.login AS USER_NAME,
            ticket_state.name AS TICKET_STATUS,
            #ticket.ticket_state_id AS TICKET_STATUS_ID,
            queue.name AS QUEUE_NAME,
            #ticket.queue_id AS Q_ID,
            ticket.create_time AS CREATE_TIME,
            ticket.change_time AS CHANGE_TIME
            
        FROM 
            ticket
        JOIN queue ON ticket.queue_id = queue.id
        JOIN article ON ticket.id = article.ticket_id
        JOIN users ON article.change_by = users.id
        JOIN article_sender_type ON article.article_sender_type_id = article_sender_type.id
        JOIN ticket_state ON ticket.ticket_state_id = ticket_state.id
        JOIN ticket_state_type ON ticket_state.type_id = ticket_state_type.id
        WHERE 
            queue.name IN ('MONITORING')
            #AND article_sender_type.name IN ('customer')
            AND ticket_state_type.name IN ('open')
            #AND article.create_time BETWEEN DATE_SUB(NOW(), INTERVAL 1 HOUR) AND NOW()
        ORDER BY TICKET_ID DESC;
    """

    mycursor.execute(query)
    myresult = mycursor.fetchall()

    #print(myresult)

    if myresult:
        s_no = 0
        table_data = []

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
            
                <b><p>List of open ticket details in monitoring</p></b>
            
                """ + ''.join(table) + """
                
            
            </br>
            
                </br>
            
                <p>This is a auto-generated mail.</p>
            
            </body>
            
            </html>
        """

        #print(html_content)

        subject  = "Monitoring queue open ticket details on "+ str(today_date_time) 
        msg = MIMEMultipart('alternative')
        to = 'rims.l1@futurenet.in'
        #cc = 'rims.tl@futurenet.in,rims@futurenet.in'
        msg['Subject'] = subject 
        msg['to'] = to
        #msg['cc'] = cc
        #rcpt = cc.split(",") + to.split(",")
        part1 = MIMEText(html_content, 'html','utf-8')
        msg.attach(part1)
        smtp_server = smtplib.SMTP('webmail.futurenet.in',25)
        smtp_server.starttls()
        smtp_server.login('otrs.report@futurenet.in','JwD@!3j@4HQB!@')
        smtp_server.sendmail('otrs.report@futurenet.in', to, msg.as_string())
        smtp_server.quit()

if __name__ == "__main__":
    open_ticket_details()