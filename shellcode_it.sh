xxd -c 1 $1 | awk '{print "\\x" $2;}' | tr '\n' ' ' | sed 's/ //g'
