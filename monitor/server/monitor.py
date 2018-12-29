import socket
import MySQLdb
import MySQLdb.cursors

host = '10.154.4.141'
port = 9999
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.setsockopt()
s.bind((host, port))
s.listen(5)

while True:
    conn, addr = s.accept()
    print("connected with {}".format(addr))
    while True:
        data = conn.recv(10240)
        if not data: break
        #print('received ' + repr(data))	
        if data == "['nova-conf-change-list']":
	    print("print nova-conf-change-list")
            db = MySQLdb.connect(host='10.154.4.141',user='root',passwd='root',db='test')
            sql="select * from nova_conf" 
            #cursor = db.cursor(MySQLdb.cursors.DictCursor)  # dictionary
            cursor = db.cursor()
	    try:
                cursor.execute(sql)
                data1 = cursor.fetchall()   
		#print(data1)   #<type 'tuple'>
	        fields = cursor.description
  
                column_list = []
                for field in fields:
                    column_list.append(field[0])
		#print(column_list)
                data2 = (column_list,data1)
		#print(data2)
		conn.sendall(str(data2))
            except:
                # Rollback in case there is any error
                db.rollback()
                conn.sendall('%s is error !' % sql)
        #reply = raw_input("reply>>")
        #conn.sendall(reply.encode('utf-8'))
	#conn.sendall(str(data1))
	else:
	    error_message = "%s is error !" % data
	    conn.sendall(error_message)
