#! /bin/sh	
stress -c 2 -m 5 -i 3 -t 10;
sleep 40; 	
stress -c 1 -m 2 -i 4 -t 15;
sleep 10; 	
stress -c 1 -m 2 -i 1 -t 5;
sleep 20; 	
stress -c 2 -m 7 -i 2 -t 20;
sleep 5; 	
stress -c 1 -m 3 -i 4 -t 10;
sleep 10; 	
stress -c 1 -m 4 -i 2 -t 5;
sleep 10; 





