# ===================================
# Terminal Based Python Utility 
# to Migrate Redis Keys From 
# 1 Instance/DB -> 1 Instance/DB
# Ver 1.0
# Author: vinrosete
# ====================================
#!/usr/bin/python
import sys, getopt, redis

def main(argv):

   _dest_redis = ''
   _dest_port = 6379
   _dest_db = 0
   _orig_redis = ''
   _orig_port = 6379
   _orig_db = 0
   _key_name = 0
   _key_found = 0

   try:
      opts, args = getopt.getopt(argv,"hd:p:x:f:o:y:s:k:",["destination=","dport=","destinationdb","origin=","oport","origindb","key"])
   except getopt.GetoptError:
      print 'portdis.py -d <destination host> -x <destination port> -f <destination db> -o <origin host> -y <origin port> -s <origin db> -k <Key Name Pattern>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'portdis.py -d <destination host> -x <destination port> -f <destination db> -o <origin host> -y <origin port> -s <origin db> -k <Key Name Pattern>'
         sys.exit()
      elif opt in ("-d", "--destination"):
         _dest_redis = arg
      elif opt in ("-o", "--origin"):
         _orig_redis = arg
      elif opt in ("-x","--dport"):
	 _dest_port = arg
      elif opt in ("-f","--destinationdb"):
	 _dest_db = arg
      elif opt in ("-s","--origindb"):
	 _orig_db = arg
      elif opt in ("-y","--oport"):
         _orig_port = arg
      elif opt in ("-k","--key"):
         _key_name = arg
	 _key_found = 1
         
   if _key_found == 0 :
      print 'Error: Missing `--key` `-k` argument ';	  
      sys.exit()

   print 'Destination Host is ', _dest_redis
   print 'Destination Port is ', _dest_port
   print 'Destination DB is ', _dest_db
   print 'Origin Host is ', _orig_redis
   print 'Origin Port is ', _orig_port
   print 'Origin DB is ', _orig_db
   print 'Key Pattern is '+_key_name

   br = redis.StrictRedis(host=_dest_redis, port=_dest_port, db=_dest_db)

   r = redis.StrictRedis(host=_orig_redis, port=_orig_port, db=_orig_db)

   keys = r.keys(_key_name)

   for key in keys:

	type = r.type(key)

	print type+'\t'+key

	if(type == 'hash'):

		hkeys = r.hkeys(key)

		for hkey in hkeys:

			val = r.hget(key, hkey)

			br.hset(key, hkey, val)

	elif(type == 'zset'):

		zval = r.zrange(key, 0 , -1);
    
        	for v in zval:
            
            		br.zadd(key, 0, v);

	elif(type == 'list'):

		val = r.lrange(key, 0 , -1)

		for v in val:

			br.rpush(key, v)

	elif(type == 'set'):

		val = r.smembers(key)

		for v in val:

			br.sadd(key, v)

	elif(type == 'string'):

		val = r.get(key)

		br.set(key, val)

	else:
		print 'key [%s] not in 4 type'%key

   print 'Process Completed'

if __name__ == "__main__":
   main(sys.argv[1:])
   
#EOF
