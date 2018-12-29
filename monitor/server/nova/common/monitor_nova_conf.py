import os
import logging
from oslo_config import cfg
import MySQLdb
import socket
import time
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)

CONF = cfg.CONF
LOG = logging.getLogger(__name__)

def initalize_nova_conf(CONF):
    db = MySQLdb.connect(host='10.154.4.141',user='root',passwd='root',db='test')
    for opt_name in sorted(CONF._opts):
        sql="INSERT INTO current_value(date,hostname,ip,conf_name,current_value)"+ " VALUES" + "(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),hostname,ip,str(opt_name),str(getattr(CONF, opt_name)))
        cursor = db.cursor()
        try:
            cursor.execute(sql)
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
    for group_name in CONF._groups:
        group_attr = CONF.GroupAttr(CONF, CONF._get_group(group_name))
        for opt_name in sorted(CONF._groups[group_name]._opts):
            #opt = CONF._get_opt_info(opt_name, group_name)['opt']
            sql="INSERT INTO current_value(date,hostname,ip,conf_name,current_value)"+ " VALUES" + "(\"%s\",\"%s\",\"%s\",\"%s.%s\",\"%s\")" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),hostname,ip,str(group_name),str(opt_name),str(getattr(group_attr, opt_name)))
            #cursor = db.cursor()
            try:
                cursor.execute(sql)
                db.commit()
            except:
            # Rollback in case there is any error
                db.rollback()
    db.close()




def monitor_nova_conf(CONF,LOG):
    #import pdb;pdb.set_trace()
    LOG.setLevel(level = logging.DEBUG)
    if os.path.exists('/var/log/nova/test.log'):
        pass
    else:
        os.system('touch /var/log/nova/test.log')
    os.system('chmod 777 /var/log/nova/test.log')
    handler = logging.FileHandler("/var/log/nova/test.log")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    LOG.addHandler(handler)

    #CONF.log_opt_values(LOG, lvl)
    #LOG.debug('%-30s=%s',sorted(CONF._opts)[0],str(getattr(CONF,sorted(CONF._opts)[0])))
    db = MySQLdb.connect(host='10.154.4.141',user='root',passwd='root',db='test')
    for opt_name in sorted(CONF._opts):
            #opt = CONF._get_opt_info(opt_name)['opt']
        sql_opt_name_last_value="select current_value from current_value where conf_name='" + "%s\' and ip=\'%s\'"  % (str(opt_name),ip)
        #LOG.debug(str(sql_opt_name_last_value) + str('   >>>   ')+ str(getattr(CONF, opt_name)) )
        cursor = db.cursor()
        try:
            cursor.execute(sql_opt_name_last_value)
            data = cursor.fetchall()
            opt_name_last_value=data[0][0]
            #LOG.debug("*" * 80)
            #LOG.debug(str(opt_name_last_value) + str('   >>>   ')+ str(getattr(CONF, opt_name))) 
            if str(opt_name_last_value) != str(getattr(CONF, opt_name)):
	        sql="INSERT INTO nova_conf(date,hostname,ip,conf_name,last_value,new_value)"+ " VALUES" + "(\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\")" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),hostname,ip,str(opt_name),str(opt_name_last_value),str(getattr(CONF, opt_name)))
		cursor = db.cursor()
                try:
                    cursor.execute(sql)
                    db.commit()
                except:
                # Rollback in case there is any error
                    db.rollback()

                message ='%s changed from %s to %s' % (opt_name,opt_name_last_value,str(getattr(CONF, opt_name)))
                LOG.debug("*" * 80)
                LOG.debug(str(message))
                #LOG.debug("=" * 80)
                sql_update_opt_name_new_value="UPDATE current_value SET current_value="+ "\"%s\" WHERE conf_name=\"%s\" and ip=\'%s\'"  % (str(getattr(CONF, opt_name)), str(opt_name),ip)
		#LOG.debug(str(sql_update_opt_name_new_value))
		cursor = db.cursor()
                try:
                    cursor.execute(sql_update_opt_name_new_value)
                    db.commit()
                except:
                # Rollback in case there is any error
                    db.rollback()

        except:
                # Rollback in case there is any error
            db.rollback()


    for group_name in CONF._groups:
        group_attr = CONF.GroupAttr(CONF, CONF._get_group(group_name))
        for opt_name in sorted(CONF._groups[group_name]._opts):
            #sql="INSERT INTO test(hostname,host_ip)"+ " VALUES" + "(\"%s.%s\",\"%s\")" % (str(group_name), str(opt_name), str(getattr(group_attr, opt_name)))
            sql_group_opt_name_last_value="select current_value from current_value where hostname='" + "%s.%s\' and ip=\'%s\'"  % (str(group_name),str(opt_name),ip)
	    cursor = db.cursor()
            try:
                cursor.execute(sql_group_opt_name_last_value)
                data = cursor.fetchall()
                group_opt_name_last_value=data[0][0]
                db.commit()
		if str(group_opt_name_last_value) != str(getattr(group_attr, opt_name)):
		    sql="INSERT INTO nova_conf(date,hostname,ip,conf_name,last_value,new_value)"+ " VALUES" + "(\"%s\",\"%s\",\"%s\",\"%s.%s\",\"%s\",\"%s\")" % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),hostname,ip,str(group_name),str(opt_name),str(group_opt_name_last_value),str(getattr(group_attr, opt_name)))
                    cursor = db.cursor()
                    try:
                        cursor.execute(sql)
                        db.commit()
                    except:
                # Rollback in case there is any error
                        db.rollback()
                    message ='%s.%s changed from %s to %s' % (str(group_name),str(opt_name),str(group_opt_name_last_value),str(getattr(group_attr, opt_name)))
                    LOG.debug("*" * 80)
                    LOG.debug(str(message))
                    sql_update_group_opt_name_new_value="UPDATE current_value SET current_value="+ "\"%s\" WHERE comf_name=\"%s.%s\" and ip=\'%s\'"  % (str(getattr(group_attr, opt_name)),str(group_name), str(opt_name),ip)
                    #LOG.debug(str(sql_update_group_opt_name_new_value))
                    cursor = db.cursor()
                    try:
                        cursor.execute(sql_update_group_opt_name_new_value)
                        db.commit()
                    except:
                    # Rollback in case there is any error
                        db.rollback()

            except:
                # Rollback in case there is any error
                db.rollback()
            




    db.close()
